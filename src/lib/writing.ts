import { getCollection } from "astro:content";

export async function getWriting() {
  const [blog, notes, tutorials] = await Promise.all([
    getCollection("blog", ({ data }) => !data.draft),
    getCollection("notes", ({ data }) => !data.draft),
    getCollection("tutorials", ({ data }) => !data.draft),
  ]);

  return [
    ...blog.map((entry) => ({ ...entry, href: `/blog/${entry.id}/`, label: "Essay" })),
    ...notes.map((entry) => ({ ...entry, href: `/notes/${entry.id}/`, label: "Paper note" })),
    ...tutorials.map((entry) => ({ ...entry, href: `/tutorials/${entry.id}/`, label: "Tutorial" })),
  ].sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}
