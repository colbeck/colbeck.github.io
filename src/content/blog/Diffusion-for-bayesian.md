---
title: "Diffusion for bayesian inverse problems"
date: 2026-05-18
summary: "Notes on diffusion models, Bayesian inverse problems, posterior sampling, and generative priors."
tags: ["writing", "research"]
---

More recently, I've been interested in the problem of inference-time adaptation of generative models. In particular, I've been thinking a lot about this in terms of the Bayesian inference sampling problem of sampling from the posterior given a prior and likelihood,

$$
p(x\mid y) \propto p(y\mid x)p(x).
$$

## **Relationship to other modern Bayesian inference problems**

If you take a course on Bayesian inference, you'll learn many methods of sampling from the posterior and assumptions under which some methods are more or less preferable. One thing this discussion clarified for me was *the special case assumptions* we have been operating under in this regime, and how they are different from the assumptions that are made in other Bayesian inference setups. To put simply, we have

- $p(x)$ prior
- $p(y\mid x)$ likelihood
- $p(x\mid y)$ posterior

Many classical MCMC methods assume that we can evaluate an unnormalized posterior density, typically through access to the prior and likelihood, or at least their product up to a constant. They then produce approximate samples from the posterior, with the approximation coming from finite runtime, discretization, convergence issues, etc. Some methods, like Langevin or HMC, additionally require gradient information.

Simulation-based inference, or SBI, addresses a different problem. In particular, it is often the setting where I have access to a prior and the ability to simulate observations from the likelihood, but I may not be able to evaluate the likelihood density itself. In other words, I can sample

$$
x \sim p(x), \qquad y \sim p(y\mid x),
$$

but I may not have a tractable expression for $p(y\mid x)$.

**Our problem** is different again: specifically, how to sample from the posterior distribution $p(x\mid y)$ assuming access to the likelihood $p(y\mid x)$ and perhaps its gradients, but only implicit access to the prior through a sampler, in our case via a diffusion model or related generative prior. So the prior is not necessarily available as a tractable density $p(x)$, even though we may be able to sample from it or access score-like information through the generative model.

## **Relationship to classical inverse problems**

Today I spoke with one of my collaborators Taylan to see if I could get a better idea of what he was interested in, and where he saw the bigger picture direction of our work moving. He gave me a little history of inverse problems, which I am embarrassed to say I am quite ignorant to, and provided some nice perspective on what we are doing.

As I understand it, the most general components of an "inverse problem," or more specifically a **linear inverse problem**, are as follows:

1. $y = O u + \epsilon$, where
   1. $u$ is the vector, function, or state I want to recover
   2. $\epsilon$ is noise
   3. $O$ is a linear map or operator
   4. $y$ are noisy measurements of $u$
2. prior assumptions on $u$. These can look like
   1. a regularizer $R(u)$
      1. example is sparsity, $R(u) = \|Wu\|_0$
      2. a PDE that $u$ approximately satisfies $\partial_t u = \mathcal{F}[u]$, which could lead to a regularizer like $R(u) := \|\partial_t u - \mathcal{F}[u]\|^2$
   2. a prior distribution $p(u)$

Note: in this case $u$ need not be finite-dimensional. For example, $u = u(t,x)$ may be a time-parameterized function on $\mathbb{R}^d$, and our prior information may come from the fact that it approximately satisfies a PDE.

The transformation $O$ often represents a non-invertible, underdetermined, smoothing, or noisy observation process, making the inverse problem ill-posed. This means that solutions may not exist, may not be unique, or may depend unstably on the observations $y$. In many underdetermined cases, there may be infinitely many $u$'s which are consistent with the observations. This is where the prior comes in: it gives us a way to prefer *"more likely"* $u$'s which generate, or approximately generate, our observations.

Historically, practitioners would hand-design these prior regularizers for the specific inverse problems they worked in, whether that be MRI images, where wavelet transformations of real MRI images often lead to sparse representations of data, weather forecasting, where physical dynamics are described by PDEs, or Kalman filtering, where the prior dynamics come from a state-space model.

We discussed a specific example of a Kalman filter for something like:

1. $du_t = F u_t\,dt + dW_t$ as the prior dynamics
2. $y_{t_k} = G u_{t_k} + \epsilon_k$ as the measurements

Here $W_t$ is Brownian motion, and $\epsilon_k$ is the observation noise.

## **"Solving" linear inverse problems**

Suppose our measurements are simple linear measurements,

$$
y = Ax + \epsilon.
$$

One might go about solving a linear inverse problem a few different ways.

1. Optimization to ensure measurement consistency in the case our prior can be described by some regularizer $R(x)$.
   1. $\min_x \ \|y - Ax\|^2 + \lambda R(x)$
   2. $\min_x R(x) \quad \text{s.t.} \quad \|y - Ax\|^2 < \delta$
2. In the case our prior is some distribution $p(x)$,
   1. compute some MAP estimate of $p(x\mid y) \propto p(y\mid x)p(x)$
   2. sample from $p(x\mid y)$

There is also a nice connection between the two views. For example, if

$$
y = Ax + \eta, \qquad \eta \sim \mathcal{N}(0,\sigma^2 I),
$$

and if the prior can be written as something like

$$
p(x) \propto \exp(-\lambda R(x)),
$$

then the MAP estimate corresponds to solving an optimization problem of the form

$$
\min_x \frac{1}{2\sigma^2}\|y - Ax\|^2 + \lambda R(x).
$$

So classical regularization can often be viewed as MAP estimation under an appropriate prior. But sampling from the full posterior is different from just computing a MAP estimate: it gives not only one plausible reconstruction, but a distribution over plausible reconstructions. This is especially important in ill-posed inverse problems, where there may be many different $x$'s that explain the same observations.
