export const tasks = [
  {
    id: "production",
    title: "Production Planning",
    description:
      "A small production planning problem. We want to decide how many units of two products to produce in order to maximize profit while respecting resource limits.",

    explanation: {
      variables: [
        "x₁ — number of units of product A",
        "x₂ — number of units of product B",
      ],
      objective:
        "Each unit of product A gives 3 units of profit, and each unit of product B gives 2 units of profit. That is why the objective function is 3x₁ + 2x₂.",
      constraints: [
        "x₁ + x₂ ≤ 4 — together, products A and B cannot use more than 4 units of the shared resource.",
        "x₁ ≤ 2 — we can produce at most 2 units of product A.",
        "x₂ ≤ 3 — we can produce at most 3 units of product B.",
        "x₁, x₂ ≥ 0 — we cannot produce a negative number of products.",
      ],
    },

    formulation: {
      objective: "Maximize: z = 3x₁ + 2x₂",
      constraints: [
        "x₁ + x₂ ≤ 4",
        "x₁ ≤ 2",
        "x₂ ≤ 3",
        "x₁, x₂ ≥ 0",
      ],
    },

    varsCnt: 2,
    target: "MAXIMIZE",
    objective: [3, 2],
    constraints: [
      { coefs: [1, 1], rhs: 4, sign: "LESS_OR_EQUAL" },
      { coefs: [1, 0], rhs: 2, sign: "LESS_OR_EQUAL" },
      { coefs: [0, 1], rhs: 3, sign: "LESS_OR_EQUAL" },
    ],
  },

  {
    id: "diet",
    title: "Diet Problem",
    description:
      "A diet or coverage problem. We want to minimize the total cost while satisfying minimum required amounts of two nutrients.",

    explanation: {
      variables: [
        "x₁ — amount of food A",
        "x₂ — amount of food B",
      ],
      objective:
        "Food A costs 3 units per portion, and food B costs 5 units per portion. Since we want the cheapest valid diet, we minimize 3x₁ + 5x₂.",
      constraints: [
        "2x₁ + x₂ ≥ 8 — the diet must provide at least 8 units of nutrient 1.",
        "x₁ + 3x₂ ≥ 9 — the diet must provide at least 9 units of nutrient 2.",
        "x₁, x₂ ≥ 0 — we cannot choose negative amounts of food.",
      ],
    },

    formulation: {
      objective: "Minimize: z = 3x₁ + 5x₂",
      constraints: [
        "2x₁ + x₂ ≥ 8",
        "x₁ + 3x₂ ≥ 9",
        "x₁, x₂ ≥ 0",
      ],
    },

    varsCnt: 2,
    target: "MINIMIZE",
    objective: [3, 5],
    constraints: [
      { coefs: [2, 1], rhs: 8, sign: "GREATER_OR_EQUAL" },
      { coefs: [1, 3], rhs: 9, sign: "GREATER_OR_EQUAL" },
    ],
  },
];