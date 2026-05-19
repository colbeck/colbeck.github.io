# colebecker.me

Academic website for Cole Becker, built with Astro and hosted on GitHub Pages.

## Local development

```bash
npm install
npm run dev
```

Build the static site with:

```bash
npm run build
```

Preview the production build with:

```bash
npm run preview
```

## Writing

General blog posts live in `src/content/blog/*.md`. Technical tutorials live in `src/content/tutorials/*.md`.
Paper notes live in `src/content/notes/*.md`.

Both support Markdown and LaTeX math through KaTeX:

```md
Inline math: $W_2(\mu, \nu)$

$$
\partial_t \rho_t + \nabla \cdot(\rho_t v_t) = 0.
$$
```

Put static files in `public/assets/`. Post images and GIFs can go in `public/assets/posts/`.

Regenerate the research-page Gaussian-mixture contour SVGs with:

```bash
python3 scripts/generate_mixture_contours.py
```

## Portrait

Put your homepage photo at:

```text
public/assets/profile.jpg
```

The homepage uses that file automatically. If it is missing, the site shows an initials fallback.

## CV

Replace `public/assets/cv.pdf` with the current CV. The navigation links directly to that PDF.

## Deployment

The site deploys with GitHub Actions from `.github/workflows/deploy.yml`. In the GitHub repository settings, set Pages source to **GitHub Actions**.

The custom domain is configured through `public/CNAME`:

```text
colebecker.me
```

At the domain registrar, configure the apex domain with GitHub Pages A records:

```text
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Optionally configure `www` as a CNAME pointing to `colbeck.github.io`.
