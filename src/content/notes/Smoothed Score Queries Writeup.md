---
title: "Smoothed Score Queries and Complexity of Sampling"
date: 2026-06-11
authors: ["Jingbo Liu"]
# venue: "Example Venue"
year: 2026
summary: "How smoothed-score queries improve the condition-number dependence of Gaussian sampling."
tags: ["sampling"]
paperUrl: "https://arxiv.org/pdf/2605.27769"
---
This is a recent work by Jingbo Liu I found to be very thought-provoking: maybe we can use the score function for something other than diffusion-based sampling! Below I try to summarize my main takeaways.

## 1. Gaussian Sampling Setup

**Target distribution.**

$$
q = \mathcal{N}(0,\Sigma)
  = \mathcal{N}(0,\Lambda^{-1}),
\qquad
\Lambda \coloneqq \Sigma^{-1} \succ 0
\quad \text{(precision matrix).}
$$

- **Goal:** Sample from $q$.
- **Method:** Approximate $\Lambda^{-1/2}Z$ for $Z \sim \mathcal{N}(0,I)$.
- **Why:** If $Y=\Lambda^{-1/2}Z$, then $Y\sim\mathcal{N}(0,\Lambda^{-1})$ because $\operatorname{Cov}(Y)=\Lambda^{-1/2}I\Lambda^{-1/2}=\Lambda^{-1}$.
- **Assume:** $\operatorname{spec}(\Lambda)\subseteq[1,\kappa]$; up to diagonalization, its eigenvalues lie between $1$ and $\kappa$.

---

## 2. Approximate $\Lambda^{-1/2}Z$ with Non-Annealed Score $s_0$

**Non-annealed score.** For $q=\mathcal{N}(0,\Lambda^{-1})$,

$$
s_0(x)\triangleq\nabla\log q(x)=-\Lambda x.
$$

- **Idea:** Since $s_0(x)=-\Lambda x$, score queries give polynomial approximations $\Lambda^{-1/2}Z\approx p(\Lambda)Z$, where $p(\Lambda)Z=a_0Z+a_1\Lambda Z+\cdots+a_k\Lambda^kZ$.
- **Need:** $p(\lambda)\approx\lambda^{-1/2}$ uniformly for $\lambda\in[1,\kappa]$.
- **Known:** Chebyshev polynomials achieve this with degree $k=\widetilde{O}(\sqrt{\kappa})$.
- **Conclusion:** Non-annealed score access samples from $q$ using $\widetilde{O}(\sqrt{\kappa})$ queries.

---

## 3. Paper Contribution: Smoothed Score $s_\tau$

**Smoothed score.**

$$
q_\tau=q*\mathcal{N}(0,\tau I)
=\mathcal{N}(0,\Lambda^{-1}+\tau I),
\qquad
s_\tau(x)=-(\Lambda^{-1}+\tau I)^{-1}x.
$$

**Algorithm 1 big idea:**

- **Score $\Rightarrow$ resolvent:** $\tau Z+\tau^2s_\tau(Z)=(\Lambda+\tau^{-1}I)^{-1}Z$.
- **Idea:** Approximate $\Lambda^{-1/2}$ by $\sum_{j\in J}c_j(\Lambda+\alpha_jI)^{-1}$ for some $c_j,\alpha_j>0$.
- **Succeeds if:** $r(\lambda)\triangleq\sum_{j\in J}\frac{c_j}{\lambda+\alpha_j}\approx\lambda^{-1/2}$ uniformly for $\lambda\in[1,\kappa]$, since each eigenvector is mapped as $v\mapsto r(\lambda)v$.
- **Why reasonable:** $x^{-1/2}=\int_0^\infty\frac{1}{\pi}\alpha^{-1/2}\frac{1}{x+\alpha}\,d\alpha$, so a change of variables and finite quadrature give a sum of shifted inverses.

---

## 4. Algorithm 1: Exact Rational Sampler

> **Algorithm 1: Exact Rational Sampler**
>
> **Input:** $\delta_{\mathrm{TV}}\in(0,1)$ and $\kappa\geq1$.
>
> 1. Set $\eta=\frac{\delta_{\mathrm{TV}}}{4\sqrt d}$, compute $h,M,N,J,\alpha_j,c_j$ as in Section B.1 of the paper, and set $\tau_j\coloneqq\alpha_j^{-1}$.
> 2. Draw $Z\sim\mathcal{N}(0,I_d)$.
> 3. For each $j\in J$, query $s_{\tau_j}(Z)$ and form $X_j=\tau_jZ+\tau_j^2s_{\tau_j}(Z)$.
> 4. Output $Y=\sum_{j\in J}c_jX_j$.

Since $X_j=(\Lambda+\alpha_jI)^{-1}Z$, the output is $Y=r(\Lambda)Z\approx\Lambda^{-1/2}Z$.

> **Theorem 1**
>
> For a centered target $q=\mathcal{N}(0,\Lambda^{-1})$ with $\operatorname{spec}(\Lambda)\subseteq[1,\kappa]$, Algorithm 1 satisfies
>
> $$
> d_{\mathrm{TV}}\!\left(\mathcal{L}(Y),q\right)
> \leq\delta_{\mathrm{TV}},
> \qquad
> |J|
> =
> O\!\left(
> \left[
> \log\kappa+
> \log\!\left(\frac{e\sqrt d}{\delta_{\mathrm{TV}}}\right)
> \right]
> \log\!\left(\frac{e\sqrt d}{\delta_{\mathrm{TV}}}\right)
> \right)
> $$
>
> using exact smoothed-score queries. The condition-number dependence improves from roughly $\sqrt{\kappa}$ to $\log\kappa$.

---

## 5. Polynomial vs. Rational Oracle Access

### Ordinary Score: Polynomial Access

- **One query:** $s_0(v)=-\Lambda v$.
- **After $k$ queries:** $p_k(\Lambda)Z=\sum_{\ell=0}^k a_\ell\Lambda^\ell Z$.
- **Scalar basis:** $1,x,x^2,\ldots,x^k$.

### Smoothed Score: Rational Access

- **One query at $\tau=\alpha^{-1}$:** $(\Lambda+\alpha I)^{-1}v$.
- **After $k$ queries:** $r_k(\Lambda)Z=\sum_{j=1}^k c_j(\Lambda+\alpha_jI)^{-1}Z$.
- **Scalar basis:** $\frac{1}{x+\alpha_1},\ldots,\frac{1}{x+\alpha_k}$.

### Why This Matters

$$
p_k(x)\approx x^{-1/2}:
\quad k=\widetilde{O}(\sqrt{\kappa})
\qquad\text{vs.}\qquad
r_k(x)\approx x^{-1/2}:
\quad k=O(\log\kappa).
$$

Shifted inverses capture the inverse-like shape of $x^{-1/2}$ directly.

---

## 6. Main Point of the Paper

- **Claim:** Rational functions are a richer approximation class than polynomials. Smoothed-score queries provide access to rational functions, while non-annealed score queries provide access only to polynomials.
- **Consequence:** Smoothed scores reduce the condition-number dependence of Gaussian sampling from $\widetilde{O}(\sqrt{\kappa})$ to roughly $O(\log\kappa)$, up to additional logarithmic factors in dimension and accuracy.
