---
title: "Diffusion for bayesian inverse problems"
date: 2026-05-19
summary: ""
tags: ["writing", "research"]
---

More recently, I've been interested in the problem of inference time adaptation of flow-based generative models. In particular I've been thinking a lot about this in terms of the bayesian inference sampling problem of sampling from the posterior given a prior and likelihood.
 $$ p(x\mid y) \propto p(y\mid x) p(x).$$ 
**Relationship to other modern bayesian inference problems**

If you take a course on bayesian inference, you'll learn many methods of sampling from the posterior and assumptions under which some methods are more or less preferable. One thing this discussion clarified for me, was *the special case assumptions* we have been operating under in this regime, and how they are different from the assumptions that are made in other bayesian inference setups. To put simply we have
- $p(x)$ prior
- $p(y\mid x)$ likelihood
- $p(x\mid y)$ posterior
MCMC methods assume we have access to the prior and likelihood, and thus have an un-normalized expression for the posterior. They produce approximate samples for the posterior using these expressions. Simulation based inference (SBI) addresses a different problem, in particular one where I have access to a prior, and ability only to sample from likelihoods. **Our problem** is almost the reverse: specifically how to sample from the posterior distribution $p(x\mid y)$ assuming access to likelihood $p(y\mid x)$ and its gradients, and a sampler (in our case via diffusion) for $p(x)$.

**Relationship to classical inverse problems**

Today I spoke with one of my collaborators Taylan to see if I could get a better idea of what he was interested in, and where he saw the bigger picture direction of our work moving in.He gave me a little history of inverse problems which I am embarrassed to say I am quite ignorant to, and provided some nice perspective on what we are doing. 

As I understand it, the most general components of an "inverse problem" or more specifically a **linear inverse problem** are as follows:
1. $y = O u + \epsilon$, where 
	1. $u$ is the vector I want to recover
	2. $\epsilon$ is noise
	3. $O$ is a linear map or transformation
	4. $y$ are noisy measurements of $u$
2. prior assumptions on $u$. Can look like
	1. a regularizer $R(x)$ 
		1. example is sparsity $R(x) = \|Wx\|_0$
		2. A PDE that $u$ satisfies $\partial_t u = \mathcal{F}[u]$ --> $R(x) :=  \|\partial_t u - \mathcal{F}[u]\|^2$
	2. a prior distribution $p(x)$
Note*, in this case $u$ need not be finite dimensional, $u = u(t,x)$ may be a time-parameterized function on $\mathbb{R}^d$ and our prior is a PDE it satisfied.

The transformation $O$ tends to represent an underdetermined system, making this problem ill-posed which means there are **infinite** such vectors $u$ which could have produced our observations/measurements $y$. This is where the prior comes in, it gives us *"more likely"* $u$ which generate our observations. Historically, practitioners would "make up" these prior regularizers for the specific inverse problems they would work in, whether that be MRI images (wavelet transformations of "real mri images" lead to highly sparse representations of data), weather forecasting (PDEs), Kalman filtering (ODE).

We discussed a specific example of a Kalman filter for:
1. $\partial_t u_t = F u_t + dw_t$ *prior*
2. $y_{t_k} = G u_{t_k} + \epsilon_k$ *measurements*

**"Solving" Linear inverse problems**
Suppose our measurements are simple linear measurements $$y = Ax + \epsilon,$$one might go about solving a linear inverse problem a few different ways

1. Optimization to ensure measurement consistency in the case our prior can be described by some $R(x)$ regularizer.
	1. $\text{min}_x \ \|y-Ax\|^2 + \lambda R(x)\|$
	2. $\text{min}_x R(x) \mid s.t. \ ||y-Ax||^2 < \epsilon$
2. in the case our prior is some distribution $p(x)$
	1. some MAP estimate of $p(x\mid y) \propto p(y\mid x) p(x)$
	2. sample from $p(x\mid y)$ 

**Moving back to our problem**
