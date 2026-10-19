export interface Publication {
  title: string;
  authors?: string[];
  venue: string;
  summary?: string;
  links: { label: string; href: string }[];
  image?: { src: string; alt: string; width: number; height: number };
}

export const upcomingPublications: Publication[] = [
  {
    title: "Elliptic Schedules for Diffusion Models",
    venue: "Coming soon",
    links: [],
  },
];

export const publications: Publication[] = [
  {
    title: "Training and Evaluating Diffusion Policies with Long Context Lengths",
    authors: [
      "Abhinav Agarwal",
      "Adam Wei",
      "Taylan Kargin",
      "Michael Zeng",
      "Cole Becker",
      "Arif Kerem Dayı",
      "Pablo Parrilo",
      "Asuman Ozdaglar",
      "Russ Tedrake",
    ],
    venue: "arXiv preprint, 2026",
    image: {
      src: "/assets/publications/long-context-overview.png",
      alt: "Paper figure showing the long-context diffusion policy architecture and variable history training.",
      width: 1204,
      height: 560,
    },
    summary:
      "A study of how observation history, architecture, and data scale affect diffusion policies, with a training method that learns across multiple context lengths.",
    links: [
      { label: "Paper", href: "https://arxiv.org/abs/2606.16447" },
      { label: "Project", href: "https://dp-with-long-context.github.io/" },
    ],
  },
  {
    title: "Mean Robust Optimization",
    authors: ["Irina Wang", "Cole Becker", "Bart Van Parys", "Bartolomeo Stellato"],
    venue: "Mathematical Programming, 213, 1235–1277, 2025",
    image: {
      src: "/assets/publications/mean-robust-uncertainty.png",
      alt: "Paper figure comparing uncertainty sets formed from all data points and from a single cluster.",
      width: 960,
      height: 470,
    },
    summary:
      "A framework that uses clustered data to balance computational cost and conservatism in robust optimization, with finite-sample performance guarantees.",
    links: [
      { label: "Paper", href: "https://arxiv.org/abs/2207.10820" },
      { label: "Journal", href: "https://doi.org/10.1007/s10107-024-02170-4" },
    ],
  },
  {
    title: "Learning Decision-Focused Uncertainty Sets in Robust Optimization",
    authors: ["Irina Wang", "Cole Becker", "Bart Van Parys", "Bartolomeo Stellato"],
    venue: "arXiv preprint, 2023 · Revised July 2024",
    image: {
      src: "/assets/publications/decision-focused-overview.png",
      alt: "Paper diagram showing an optimization layer and an evaluation metric that updates the uncertainty-set parameters.",
      width: 1120,
      height: 240,
    },
    summary:
      "Learning uncertainty sets by differentiating through robust optimization problems to improve decision performance while providing constraint-satisfaction guarantees.",
    // This version includes Cole in the author list; later revisions have different authorship.
    links: [{ label: "Paper (2024 version)", href: "https://arxiv.org/abs/2305.19225v4" }],
  },
];
