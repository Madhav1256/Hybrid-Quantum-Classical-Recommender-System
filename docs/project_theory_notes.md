# Comprehensive Theory Notes: CG-QRH Project

This document serves as the master reference for all theoretical concepts and keywords underlying the **Classical-GNN Quantum-Ranking Hybrid (CG-QRH)** system.

---

## 1. Recommender Systems Theory

### Core Concepts
* **Collaborative Filtering (CF):** A technique that makes predictions about a user's interests by collecting preferences from many users. Underlying assumption: *If person A has the same opinion as person B on an issue, A is more likely to have B's opinion on a different issue than a randomly chosen person.*
* **Implicit vs. Explicit Feedback:**
  * *Explicit:* Direct ratings (e.g., 5-stars on Amazon).
  * *Implicit:* Indirect behavior (e.g., clicks, cart adds, watch time). RetailRocket uses implicit feedback. It is harder to model because you only know what they *liked*, not what they *disliked*.
* **Sparsity:** The ratio of empty cells in a user-item matrix. E-commerce datasets are extremely sparse (>99.99%) because a user interacts with a tiny fraction of the catalog.
* **The "Filter Bubble":** A state where an algorithm only recommends highly similar items (e.g., 10 identical black shirts). This maximizes accuracy but hurts user discovery.

### Key Metrics
* **Hit Ratio (HR@K):** A binary metric. If the target item is anywhere in the Top K recommendations, HR = 1, else 0.
* **Normalized Discounted Cumulative Gain (NDCG@K):** Measures ranking quality. It gives higher scores if relevant items appear at rank #1 vs rank #10. "Discounted" means the value of an item drops logarithmically the lower it appears in the list.
* **Intra-List Diversity (ILD):** Measures how different the items in a recommendation list are from *each other*. Calculated using $1 - \text{Cosine Similarity}$ across all pairs in the Top-K list.

---

## 2. Graph Neural Networks (GNNs)

Current state-of-the-art classical recommenders use graphs rather than simple matrices.

### Core Concepts
* **Bipartite Graph:** A graph with two sets of nodes (Users and Items). Edges only connect a User to an Item (never User-to-User or Item-to-Item).
* **High-Order Connectivity:** 
  * 1st-order: User A bought Item 1.
  * 2nd-order: Item 1 was also bought by User B.
  * 3rd-order: User B also bought Item 2. *(Therefore, recommend Item 2 to User A).*
* **Message Passing:** The algorithm where nodes update their own "embedding" (vector representation) by aggregating the embeddings of their neighbors.

### LightGCN (Our Classical Model)
* **What it is:** A simplified, highly efficient Graph Convolutional Network designed specifically for recommenders.
* **Why it's special:** Standard GNNs use heavy math (non-linear activation functions, feature transformations). LightGCN proved that for collaborative filtering, you can remove all that heavy math and *only* use neighborhood aggregation (message passing). It trains faster and performs better on sparse data.
* **BPR Loss (Bayesian Personalized Ranking):** The training function. It forces the model to score an item the user *did* interact with higher than a random item they *didn't* interact with.

---

## 3. Quantum Computing & Optimization Theory

The true innovation of this project is applying Quantum mechanics to solve the math that classical computers struggle with.

### Quantum Basics
* **Qubit:** The basic unit of quantum information. Unlike a classical bit (0 or 1), a qubit exists in a *Superposition* of both 0 and 1 simultaneously until measured.
* **QRAM (Quantum RAM) Limitation:** Currently, we cannot load massive datasets (like 700k e-commerce interactions) directly into a quantum state. This is why our architecture uses a classical GNN for the heavy lifting.

### Quantum Annealing vs. Gate-Based Quantum
* **Gate-Based (e.g., IBM Q):** Uses logic gates (like classical computers) to run complex algorithms (Shor's, Grover's). High error rates (noise) currently limit their depth.
* **Quantum Annealing (e.g., D-Wave):** Specialized quantum computers that do *one* thing perfectly: find the global minimum of a complex equation. They use quantum fluctuations to escape "local minima" (sub-optimal solutions). **We use this.**

### Combinatorial Optimization & QUBO
* **NP-Hard Problem:** A class of mathematical problems that scale exponentially. Selecting the 10 most relevant *and* most diverse items out of 100 candidates requires evaluating trillions of combinations. Classical computers must guess (greedy algorithms).
* **QUBO (Quadratic Unconstrained Binary Optimization):** 
  * The mathematical format required by the D-Wave Annealer. 
  * *Binary:* The answer must be 1s and 0s (1 = item selected, 0 = not selected).
  * *Unconstrained:* There are no hard rules (like "you must pick exactly 10"), instead, we use *penalties* in the math to guide the system.
* **MMR (Maximum Marginal Relevance):** The specific formula we convert into a QUBO. 
  * $\text{Relevance} - \text{Diversity Penalty}$. 
  * We want to maximize the user's preference while penalizing the system if it picks two items that are too similar.

---

## 4. The CG-QRH Architecture Summary

* **Classical GNN:** Handles sparsity, learns preferences, and filters millions of items down to 100 candidates using an ANN (Approximate Nearest Neighbor) index like FAISS.
* **Quantum Annealer:** Takes those 100 candidates, builds a QUBO, and solves the NP-Hard combinatorial math to find the absolute best Top 10 list that balances Relevance and Diversity.
* **The Result:** The speed and scale of a Classical GPU, combined with the optimization perfection of a Quantum QPU.
