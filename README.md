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

Blog, Tutorials, and Notes each have their own navigation tab. All three collections also appear together
at `/writing/`, with the two most recent entries on the homepage.
Set `draft: true` in a post's frontmatter to keep it out of the built site and sitemap.
Published articles retain their `/blog/`, `/notes/`, or `/tutorials/` URLs.

All support Markdown and LaTeX math through KaTeX:

```md
Inline math: $W_2(\mu, \nu)$

$$
\partial_t \rho_t + \nabla \cdot(\rho_t v_t) = 0.
$$
```

Put static files in `public/assets/`. Post images and GIFs can go in `public/assets/posts/`.

## Research and publications

Edit `src/data/publications.ts` to add or update papers. The Research and Publications pages use the same list;
the first two entries also appear on the homepage. The homepage and Publications page additionally show `upcomingPublications`,
which currently contains the Elliptic Schedules for Diffusion Models placeholder. When it is on arXiv, move it into `publications`
with its authors, link, and figure.

Publication thumbnails live in `public/assets/publications/`. They are cropped from the papers' figures,
with descriptive alt text and dimensions in the shared publication data:

| Image | Source |
| --- | --- |
| `long-context-overview.png` | Figure 1, page 1 of [arXiv:2606.16447v2](https://arxiv.org/abs/2606.16447v2) |
| `mean-robust-uncertainty.png` | Figure 1, page 8 of [arXiv:2207.10820v5](https://arxiv.org/abs/2207.10820v5) |
| `decision-focused-overview.png` | Figure 1, page 8 of [arXiv:2305.19225v4](https://arxiv.org/abs/2305.19225v4) |

The research overview lives in `src/pages/research.astro` and is temporarily omitted from navigation and the sitemap.
A future research animation can be added there,
alongside its explanation. The previous schematic animation is no longer displayed.

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
