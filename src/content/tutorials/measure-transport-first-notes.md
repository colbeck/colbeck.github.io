---
title: "First Notes on Dynamical Measure Transport"
date: 2026-05-18
summary: "A starter tutorial post showing how math, figures, and exposition will look on the site."
tags: ["transport", "sampling", "tutorial"]
---

This is an example tutorial post. It is written in ordinary Markdown and supports inline math such as $W_2(\mu, \nu)$ and display math such as

$$
\partial_t \rho_t + \nabla \cdot(\rho_t v_t) = 0.
$$

The continuity equation is a useful way to view transport dynamically: a density $\rho_t$ evolves under a velocity field $v_t$.

## A Template for Future Tutorials

You can use posts like this for derivations, implementation notes, and visual explanations. A typical tutorial might include:

- the mathematical setup,
- a derivation or proof sketch,
- a computational example,
- figures, animations, or code snippets.

For example, a simple controlled objective might look like

$$
\inf_{(\rho_t, v_t)} \int_0^1 \int \frac{1}{2}\|v_t(x)\|^2 \rho_t(x)\,dx\,dt
$$

subject to fixed endpoints $\rho_0 = \mu$ and $\rho_1 = \nu$.

> Replace this starter post with a real tutorial once the site structure feels right.
