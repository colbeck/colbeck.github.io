import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const blog = defineCollection({
  loader: glob({ base: "./src/content/blog", pattern: "**/*.md" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().optional(),
  }),
});

const tutorials = defineCollection({
  loader: glob({ base: "./src/content/tutorials", pattern: "**/*.md" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().optional(),
  }),
});

const notes = defineCollection({
  loader: glob({ base: "./src/content/notes", pattern: "**/*.md" }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    authors: z.array(z.string()),
    venue: z.string().optional(),
    year: z.number().optional(),
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    paperUrl: z.url().optional(),
    codeUrl: z.url().optional(),
    draft: z.boolean().optional(),
  }),
});

export const collections = { blog, tutorials, notes };
