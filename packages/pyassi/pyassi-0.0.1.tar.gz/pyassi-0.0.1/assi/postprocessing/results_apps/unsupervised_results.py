from typing import Any, Annotated

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json
import pandas as pd
from pydantic import BaseModel, ConfigDict

from assi.datastorage import DataStorage
from assi.nodes import SerializedTorchTensor
import torchaudio
import torch

import uvicorn
import asyncio

templates = Jinja2Templates(directory=Path(__file__).parent / "web" / "templates")


class MetadataRow(BaseModel):
    rel_file_path_posix: str
    num_frames: int

    ConfigDict(extra="allow")


class Audiofile(BaseModel):
    num_channels: int
    sample_rate: int
    stft: Annotated[torch.Tensor, SerializedTorchTensor]
    waveform: Annotated[torch.Tensor, SerializedTorchTensor]


class DetectionResults(BaseModel):
    frame_offsets: list[int]
    scores: list[float]


def _vite_assets(dist_folder: Path) -> dict[str, dict[str, Any]]:
    manifest_path = dist_folder / ".vite" / "manifest.json"
    manifest: dict = json.loads(manifest_path.read_text())

    return {entry["name"]: entry for _, entry in manifest.items()}


def create_app(
    results_table: pd.DataFrame,
    data_storage: DataStorage,
    groupby: list[str] | None = None,
    development: bool = False,
) -> FastAPI:
    data_storage.check_integrity()
    metadata = data_storage.metadata

    app = FastAPI()

    if groupby is None:
        groupby = []
    groups = {group: metadata[group].unique().tolist() for group in groupby}

    @app.get("/groups")
    def get_groups() -> dict[str, list[Any]]:
        return groups

    @app.post("/audio_list")
    def get_audio_list(
        selected: dict[str, Any],
    ) -> list[MetadataRow]:
        # select rows that match the selected criteria
        mask = pd.Series(True, index=metadata.index)  # start with all True
        for col, val in selected.items():
            mask &= metadata[col] == val

        filtered_metadata = metadata[mask]
        list_of_records = (
            filtered_metadata.to_dict(  # pyrefly: ignore[no-matching-overload]
                orient="records"
            )
        )

        return [MetadataRow.model_validate(item) for item in list_of_records]

    @app.post("/audio_file")
    def get_audio_file(
        rel_file_path_posix: str,
    ) -> Audiofile:
        if rel_file_path_posix not in metadata["rel_file_path_posix"].values:
            raise ValueError(
                f"rel_file_path_posix '{rel_file_path_posix}' not found in metadata."
            )

        audio_file_path = data_storage.dataset_base_folder / rel_file_path_posix

        waveform, sample_rate = torchaudio.load(audio_file_path)
        num_channels = waveform.shape[0]

        stft = torchaudio.transforms.Spectrogram(n_fft=512, hop_length=256, power=2.0)(
            waveform
        )

        return Audiofile(
            num_channels=num_channels,
            sample_rate=sample_rate,
            stft=stft,
            waveform=waveform,
        )

    @app.post("/detection_result")
    def get_detection_result(
        rel_file_path_posix: str,
    ) -> DetectionResults:
        if rel_file_path_posix not in results_table["rel_file_path_posix"].values:
            raise ValueError(
                f"rel_file_path_posix '{rel_file_path_posix}' not found in results_table."
            )

        filtered_results_table = results_table[
            results_table["rel_file_path_posix"] == rel_file_path_posix
        ]
        filtered_results_table.sort_values(  # pyrefly: ignore[no-matching-overload]
            by=["frame_offset"], inplace=True
        )

        return DetectionResults(
            scores=filtered_results_table["score"].tolist(),
            frame_offsets=filtered_results_table["frame_offset"].tolist(),
        )

    web_folder = Path(__file__).parent / "web"

    # add static files for js builds
    if not development:
        dist_folder = web_folder / "dist"
        assets = _vite_assets(dist_folder)

        # mount static files
        app.mount("/static", StaticFiles(directory=web_folder / "dist"), name="static")

        def url_for_static(request: Request, path: str):
            return request.url_for("static", path=path)

        @app.get("/", response_class=HTMLResponse)
        async def root(request: Request):
            required_assets = assets["unsupervised_results"]
            return templates.TemplateResponse(
                request=request,
                name="index.jinja2",
                context={
                    "script_src": url_for_static(request, required_assets["file"]),
                    "css_files": [
                        url_for_static(request, css) for css in required_assets["css"]
                    ],
                },
            )

    if development:

        @app.get("/", response_class=HTMLResponse)
        async def root(request: Request):
            return templates.TemplateResponse(
                request=request,
                name="index.jinja2",
                context={
                    "script_src": "http://127.0.0.1:5174/src/unsupervised-results.ts"
                },
            )

    # create OpenAPI schema
    if development:
        folder = web_folder / "src" / "unsupervised-results"
        folder.mkdir(parents=True, exist_ok=True)
        with open(folder / "api-openapi.json", "w") as f:
            json.dump(app.openapi(), f, indent=2)

    return app


_app_tasks = set()


def run_app(
    results_table: pd.DataFrame,
    data_storage: DataStorage,
    groupby: list[str] | None = None,
    async_auto_start: bool = True,
) -> uvicorn.Server:
    app = create_app(
        results_table=results_table, data_storage=data_storage, groupby=groupby
    )

    config = uvicorn.Config(app, port=0, access_log=False)
    server = uvicorn.Server(config)
    if async_auto_start:
        loop = asyncio.get_running_loop()
        task = loop.create_task(server.serve())
        task.add_done_callback(_app_tasks.discard)
        _app_tasks.add(task)

    return server
