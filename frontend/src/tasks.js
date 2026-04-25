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

  {
    id: "reddy-mikks",
    title: "Reddy Mikks Paint Factory",
    description:
      "A paint factory produces exterior and interior paint. We want to decide how many tons of each paint to produce in order to maximize daily profit under material and market limits.",
  
    explanation: {
      variables: [
        "x₁ — tons of exterior paint",
        "x₂ — tons of interior paint",
      ],
      objective:
        "Each ton of exterior paint gives 5 units of profit, and each ton of interior paint gives 4 units of profit. Therefore, we maximize 5x₁ + 4x₂.",
      constraints: [
        "6x₁ + 4x₂ ≤ 24 — raw material M1 limit.",
        "x₁ + 2x₂ ≤ 6 — raw material M2 limit.",
        "-x₁ + x₂ ≤ 1 — interior paint cannot exceed exterior paint by more than 1 ton.",
        "x₂ ≤ 2 — maximum demand for interior paint is 2 tons.",
        "x₁, x₂ ≥ 0 — production quantities cannot be negative.",
      ],
    },
  
    formulation: {
      objective: "Maximize: z = 5x₁ + 4x₂",
      constraints: [
        "6x₁ + 4x₂ ≤ 24",
        "x₁ + 2x₂ ≤ 6",
        "-x₁ + x₂ ≤ 1",
        "x₂ ≤ 2",
        "x₁, x₂ ≥ 0",
      ],
    },
  
    varsCnt: 2,
    target: "MAXIMIZE",
    objective: [5, 4],
    constraints: [
      { coefs: [6, 4], rhs: 24, sign: "LESS_OR_EQUAL" },
      { coefs: [1, 2], rhs: 6, sign: "LESS_OR_EQUAL" },
      { coefs: [-1, 1], rhs: 1, sign: "LESS_OR_EQUAL" },
      { coefs: [0, 1], rhs: 2, sign: "LESS_OR_EQUAL" },
    ],
}, 
{
  id: "blending",
  title: "Blending Problem",
  description:
    "A company blends two raw materials to produce exactly 10 units of a final mixture. The goal is to minimize total cost while satisfying a minimum quality requirement.",

  explanation: {
    variables: [
      "x₁ — units of raw material A",
      "x₂ — units of raw material B",
    ],
    objective:
      "Material A costs 4 units per unit, and material B costs 6 units per unit. Since we want the cheapest valid blend, we minimize 4x₁ + 6x₂.",
    constraints: [
      "x₁ + x₂ = 10 — the final mixture must contain exactly 10 units.",
      "0.3x₁ + 0.7x₂ ≥ 5 — the mixture must satisfy the minimum quality requirement.",
      "x₁, x₂ ≥ 0 — we cannot use negative amounts of materials.",
    ],
  },

  formulation: {
    objective: "Minimize: z = 4x₁ + 6x₂",
    constraints: [
      "x₁ + x₂ = 10",
      "0.3x₁ + 0.7x₂ ≥ 5",
      "x₁, x₂ ≥ 0",
    ],
  },

  varsCnt: 2,
  target: "MINIMIZE",
  objective: [4, 6],
  constraints: [
    { coefs: [1, 1], rhs: 10, sign: "EQUAL" },
    { coefs: [0.3, 0.7], rhs: 5, sign: "GREATER_OR_EQUAL" },
  ],
},

{
  id: "portfolio",
  title: "Portfolio Allocation",
  description:
    "An investor wants to allocate money between three assets in order to maximize expected return while keeping total risk under control.",

  explanation: {
    variables: [
      "x₁ — amount invested in asset A",
      "x₂ — amount invested in asset B",
      "x₃ — amount invested in asset C",
    ],
    objective:
      "Assets A, B, and C have expected returns of 0.08, 0.11, and 0.06. Therefore, we maximize 0.08x₁ + 0.11x₂ + 0.06x₃.",
    constraints: [
      "x₁ + x₂ + x₃ ≤ 100 — the total investment budget is 100 units.",
      "0.2x₁ + 0.5x₂ + 0.1x₃ ≤ 30 — total risk must not exceed 30 units.",
      "x₂ ≤ 40 — at most 40 units can be invested in the riskiest asset.",
      "x₁, x₂, x₃ ≥ 0 — investment amounts cannot be negative.",
    ],
  },

  formulation: {
    objective: "Maximize: z = 0.08x₁ + 0.11x₂ + 0.06x₃",
    constraints: [
      "x₁ + x₂ + x₃ ≤ 100",
      "0.2x₁ + 0.5x₂ + 0.1x₃ ≤ 30",
      "x₂ ≤ 40",
      "x₁, x₂, x₃ ≥ 0",
    ],
  },

  varsCnt: 3,
  target: "MAXIMIZE",
  objective: [0.08, 0.11, 0.06],
  constraints: [
    { coefs: [1, 1, 1], rhs: 100, sign: "LESS_OR_EQUAL" },
    { coefs: [0.2, 0.5, 0.1], rhs: 30, sign: "LESS_OR_EQUAL" },
    { coefs: [0, 1, 0], rhs: 40, sign: "LESS_OR_EQUAL" },
  ],
},

{
  id: "floating-point",
  title: "Floating-Point LP Demo",
  description:
    "A small LP with decimal coefficients. This task is useful for checking whether the solver handles floating-point values correctly.",

  explanation: {
    variables: [
      "x₁ — amount of activity A",
      "x₂ — amount of activity B",
    ],
    objective:
      "Activity A gives 2.75 units of profit, and activity B gives 3.4 units of profit. Therefore, we maximize 2.75x₁ + 3.4x₂.",
    constraints: [
      "0.5x₁ + 1.25x₂ ≤ 7.5 — first fractional resource limit.",
      "1.2x₁ + 0.8x₂ ≤ 6.4 — second fractional resource limit.",
      "x₁, x₂ ≥ 0 — activity levels cannot be negative.",
    ],
  },

  formulation: {
    objective: "Maximize: z = 2.75x₁ + 3.4x₂",
    constraints: [
      "0.5x₁ + 1.25x₂ ≤ 7.5",
      "1.2x₁ + 0.8x₂ ≤ 6.4",
      "x₁, x₂ ≥ 0",
    ],
  },

  varsCnt: 2,
  target: "MAXIMIZE",
  objective: [2.75, 3.4],
  constraints: [
    { coefs: [0.5, 1.25], rhs: 7.5, sign: "LESS_OR_EQUAL" },
    { coefs: [1.2, 0.8], rhs: 6.4, sign: "LESS_OR_EQUAL" },
  ],
},

{
  id: "resource-allocation",
  title: "Simple Resource Allocation",
  description:
    "A company produces three products using two limited resources. The goal is to decide how many units of each product to produce in order to maximize profit.",

  explanation: {
    variables: [
      "x₁ — units of product A",
      "x₂ — units of product B",
      "x₃ — units of product C",
    ],
    objective:
      "Products A, B, and C give profits of 6, 4, and 5 units. Therefore, we maximize 6x₁ + 4x₂ + 5x₃.",
    constraints: [
      "2x₁ + x₂ + 3x₃ ≤ 60 — usage of resource 1 is limited.",
      "x₁ + 2x₂ + x₃ ≤ 40 — usage of resource 2 is limited.",
      "x₃ ≤ 15 — product C has a demand limit.",
      "x₁, x₂, x₃ ≥ 0 — production quantities cannot be negative.",
    ],
  },

  formulation: {
    objective: "Maximize: z = 6x₁ + 4x₂ + 5x₃",
    constraints: [
      "2x₁ + x₂ + 3x₃ ≤ 60",
      "x₁ + 2x₂ + x₃ ≤ 40",
      "x₃ ≤ 15",
      "x₁, x₂, x₃ ≥ 0",
    ],
  },

  varsCnt: 3,
  target: "MAXIMIZE",
  objective: [6, 4, 5],
  constraints: [
    { coefs: [2, 1, 3], rhs: 60, sign: "LESS_OR_EQUAL" },
    { coefs: [1, 2, 1], rhs: 40, sign: "LESS_OR_EQUAL" },
    { coefs: [0, 0, 1], rhs: 15, sign: "LESS_OR_EQUAL" },
  ],
  }
];