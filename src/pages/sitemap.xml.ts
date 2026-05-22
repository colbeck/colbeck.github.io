import { getCollection } from "astro:content";
import type { APIRoute } from "astro";

const staticPages = ["/", "/research/", "/publications/", "/blog/", "/tutorials/", "/notes/"];

function escapeXml(value: string) {
  return value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

export const GET: APIRoute = async ({ site }) => {
  const baseUrl = site ?? new URL("https://colebecker.me");
  const [blogPosts, tutorials, notes] = await Promise.all([
    getCollection("blog", ({ data }) => !data.draft),
    getCollection("tutorials", ({ data }) => !data.draft),
    getCollection("notes", ({ data }) => !data.draft),
  ]);

  const urls = [
    ...staticPages.map((path) => ({ path })),
    ...blogPosts.map((post) => ({ path: `/blog/${post.id}/`, lastmod: post.data.date })),
    ...tutorials.map((post) => ({ path: `/tutorials/${post.id}/`, lastmod: post.data.date })),
    ...notes.map((note) => ({ path: `/notes/${note.id}/`, lastmod: note.data.date })),
  ];

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls
  .map(({ path, lastmod }) => {
    const loc = escapeXml(new URL(path, baseUrl).toString());
    const lastmodTag = lastmod ? `\n    <lastmod>${lastmod.toISOString().slice(0, 10)}</lastmod>` : "";
    return `  <url>\n    <loc>${loc}</loc>${lastmodTag}\n  </url>`;
  })
  .join("\n")}
</urlset>`;

  return new Response(body, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
    },
  });
};
