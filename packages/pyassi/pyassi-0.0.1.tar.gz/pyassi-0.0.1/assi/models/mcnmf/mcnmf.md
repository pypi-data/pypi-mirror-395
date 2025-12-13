### Introduction

Nonnegative matrix factorization techniques for separation of acoustic source mixtures become a widely used method over the last decades. It became popular after its application to the image decomposition into the physically meaningful parts [1]. It is based on decomposition of nonegative matrix $\mathbf{V}$ into the product of two lower rank nonnegative matrices $\mathbf{W}$ and $\mathbf{H}$ which is called basis (dictionary) and activation matrix correspondingly. The nonngeativity of the matrices in this dimensionality reduction technique allow only addittive combination of basis parts that is "compatible with the intuitive notion of combining parts to form a whole" [1].


The general principle of NMF-based acoustic source separation algorithms is based on the decomposition of the spectrogramms $\mathbf{V}$ of the observed signal mixtures onto basis of spectral components activated in different time frames [2].

### Single channel NMF
In the single channel case the factorization is usually applied to the modulus (squared) of the complex valued STFT $\mathbf{V}=|\mathbf{X}|^2$ of the recorded signal [3] (see Fig. 1 from [2]).

![Single channel NMF diagram](SCNMF.png)

 The matrix $\mathbf{V}$ have the size $F \times N$, and matrices $\mathbf{W}$ and $\mathbf{H}$ have sizes $F\times K$ and $K\times N$ correspondingly, where the K is the number of basis(latent) components. The separation of sound sources is reduced to the obtaining the decomposition matrices and minimization of difference given by the cost function $d(x,y)$ between $\mathbf{V}$ and estimated $\mathbf{W}\mathbf{H}$:
 $$
    D(\mathbf{V} | \mathbf{W}, \mathbf{H}) = \sum_f\sum_n d(\mathbf{V}_{fn}, [\mathbf{W}\mathbf{H}]_{fn})
 $$
 
 It is usually used Euclidian distance, Kullback-Leibler divergence as a cost funtion in NMF [4] and more often Itakura-Saito (IS) divergence [5] because of its property of $d(x,y) = d(\alpha x, \alpha y)$ useful for the possibility of treatment low and high frequencies equally:
 $$
    d_{IS}(x, y) = \frac{x}{y} - \log{\frac{x}{y}} - 1
 $$

The chosen cost function for the measure of factorization performance implicitly assumes probability distribution [5, 6] in sense that minimizing the divergence $D(\mathbf{V} | \mathbf{W}, \mathbf{H})$ is equivalent to maximizing the log-likelihood $\log p(\mathbf{V} | \mathbf{W}, \mathbf{H})$  of estimation $\mathbf{W}$, $\mathbf{H}$ in Gaussian model:
$$
    p(\mathbf{V} | \mathbf{W}, \mathbf{H})= \prod_{f} \prod_{n} \mathcal{N}_c (\mathbf{X}_{fn}| 0, [\mathbf{W}\mathbf{H}]_{fn}), \\
    \mathcal{N}_c(x|0, \hat{x}) \propto \frac{1}{\hat{x}} \exp\left(-\frac{|x|^2}{\hat{x}^2}\right).
$$
Here $\hat{x}$ denotes the estimated with NMF value. More explicitly, in such model it is assumed that the sound can be decomposed into the basis of elementary (latent) components:
$$
    x_{f,n} = \sum_k c_{k,f,n}, \quad c_{k,f,n} \sim \mathcal{N}_c(x|0, w_{f,k}h_{f,n})
$$

In the elemntary case each of the component represent separated source, however for real sources different clustering techniques or incorporation of some prior information about sources is used for grouping the components and forming estimated sources [2].


### Multi-channel NMF

In case of existing several channels, it is possible to account information carried not only by absolute value difference between channels spectrograms, but also the phase difference which can especially helps with clustering according to spatial properties [6]. For this purpose it is usually used semi nonnegative matrix factorization for complex-valued mixtures. 

Denoting $\mathbf{x}_{fn}$ the vector of length $M$ of STFT values at some time-frequency slot, where $M$ microphones. Then the multivariate complex Gaussian distribution is used :
$$
    \mathcal{N}_c(\mathbf{x}_{fn}|0, \mathbf{\hat X}_{fn}) \propto \frac{1}{\det\mathbf{\hat X}_{fn}} 
    \exp\left(\mathbf{x}_{fn}^H \mathbf{\hat X}^{-1}_{fn} \mathbf{x}_{fn}\right).
$$
Here $\mathbf{\hat X}_{ij}$ is an $M \times M$ covariance matrix that should be Hermitian positive definite. Let 
$ \mathbf{X}_{fn} = \mathbf{x}_{fn} \mathbf{x}_{fn}^H $. 
Usually the the assumption of time invariant source spatial characteristics is used and the $ \mathbf{\hat X}_{fn} $ is modelled using the Hermitian positive semidefinite spatial covariance matrix $\mathbf{R}_{fk}$ such that
$$
    \mathbf{\hat X}_{fn} = \sum_k R_{fk} h_{fk} w_{kn} 
$$
Then the NMF is formulated to minimize the multichannel divergence with the multichannel IS cost function:
 $$
    D(\mathbf{V} | \mathbf{R}, \mathbf{W}, \mathbf{H}) = \sum_f\sum_n d(\mathbf{X}_{fn}, \mathbf{\hat X}_{fn})
 $$

In general, the minimization of $D$ can be realized using the Expectation Maximization algorithms or multiplicative update rules (MU) [4,5], where update rules, obtained from minimizing some auxiliary function, applied to initializied decomposition matrices $\mathbf{W}$, $\mathbf{H}$ [6].

The clustering of the basis component can be implemented in different ways [2,8] including sequential pair-wise merges accoring to minimum distance as well as integrated into NMF update rules approach [6]. It is usually assumed that the basis components are shared between sources and the clustering reduces to estimation for matrix of $z_{lk}$ elements, indicating whether the $k$-th matrix belongs to the $l$-th cluster, so the modified decomposition:  
$$
    \mathbf{\hat X}_{fn} = \sum_k \sum_l (R_{fl} Z_{lk}) h_{fk} w_{kn} 
$$
The estimated source images can be finally obtained via multichannel Wiener filter:
$$
    \tilde{y}_{fn}^{(l)} = \left( \sum_{k=1}^{K} z_{lk} t_{fk} v_{kn} \right) H_{fl}
$$

It should be noted that the sparsity of the spectrograms are assumed for the NMF-based algorithms. This requirement is also reffered as W-disjoint orthogonality of the sources [3,7]. As example, the disappointing results can be observed for the case when the signals from two sources are overlapping and both signals are associated to the one source (see [9] and [example](https://www.irisa.fr/metiss/ozerov/multi_ntf_demo.html)). In order to prevent it, activation matrix $\mathbf{H}$ is usually constrained to be sparse [3], that can means that at most part of the time only the single component is active. 

The method is also used in combination with NN for sound event classification problems (in DCASE probelms) for approximate strong labels for the weakly labeled data in an unsupervised manner [11,12,13] or jointly combinatorial model of DNN and NMF for speech separation [10].

<!-- Then the multichannel IS divergence [6]:
$$
d_{IS}(\mathbf{X}_{ij}, \mathbf{\hat X}_{ij}) = \log \mathcal{N}_c(\mathbf{x}_{ij}|0, \mathbf{X}_{ij}) - \log \mathcal{N}_c(\mathbf{x}_{ij}|0, \mathbf{\hat X}_{ij}) = \\
= \text{tr}(\mathbf{X}_{ij} \mathbf{\hat X}_{ij}^{-1}) - \log \det \mathbf{X}_{ij} \mathbf{\hat X}_{ij}^{-1} - M
$$ -->


References
___

- [1] Lee, D. D., & Seung, H. S. (1999). Learning the parts of objects by non-negative matrix factorization. nature, 401(6755), 788-791.
- [2] Makino, S. (Ed.). (2018). Audio source separation (Vol. 433). Berlin, Germany: Springer.
- [3] Virtanen, T. (2007). Monaural sound source separation by nonnegative matrix factorization with temporal continuity and sparseness criteria. IEEE transactions on audio, speech, and language processing, 15(3), 1066-1074.
- [4] Lee D., Seung H. S. Algorithms for non-negative matrix factorization //Advances in neural information processing systems. – 2000. – Т. 13.
- [5] Févotte, C., Bertin, N., & Durrieu, J. L. (2009). Nonnegative matrix factorization with the Itakura-Saito divergence: With application to music analysis. Neural computation, 21(3), 793-830.
- [6] Sawada, H., Kameoka, H., Araki, S., & Ueda, N. (2013). Multichannel extensions of non-negative matrix factorization with complex-valued data. IEEE Transactions on Audio, Speech, and Language Processing, 21(5), 971-982.
- [7] Takeda, Kazuma, et al. "Underdetermined BSS with multichannel complex NMF assuming W-disjoint orthogonality of source." TENCON 2011-2011 IEEE Region 10 Conference. IEEE, 2011.
- [8] Ozerov, A., & Févotte, C. (2009). Multichannel nonnegative matrix factorization in convolutive mixtures for audio source separation. IEEE transactions on audio, speech, and language processing, 18(3), 550-563.
- [9] Ozerov, Alexey, et al. "Multichannel nonnegative tensor factorization with structured constraints for user-guided audio source separation." 2011 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2011.
- [10] Nie, S., Liang, S., Liu, W., Zhang, X., & Tao, J. (2018). Deep learning based speech separation via NMF-style reconstructions. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 26(11), 2043-2055.
- [11] Lee, S., & Pang, H. S. (2020). Feature extraction based on the non-negative matrix factorization of convolutional neural networks for monitoring domestic activity with acoustic signals. IEEE Access, 8, 122384-122395.
- [12] Chan, T. K., Chin, C. S., & Li, Y. (2021). Semi-supervised NMF-CNN for sound event detection. IEEE Access, 9, 130529-130542.
- [13] Bisot, V., Essid, S., & Richard, G. (2017, March). Overlapping sound event detection with supervised nonnegative matrix factorization. In 2017 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 31-35). IEEE.
