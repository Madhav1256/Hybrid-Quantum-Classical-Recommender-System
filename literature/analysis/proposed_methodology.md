# Proposed Methodology: Hybrid Quantum–Classical Recommender System

Based on the rigorous gap analysis of 2024-2026 literature, we propose an architecture that explicitly avoids the "decorative VQC" trap and the "real-time inference latency" bottleneck. 

Our proposed architecture is the **Classical-GNN Quantum-Ranking Hybrid (CG-QRH)**.

## 1. Classical Layer: Candidate Generation & Representation

Current literature demonstrates that quantum circuits cannot efficiently process raw, high-dimensional, highly sparse e-commerce interaction matrices due to QRAM limitations and angle-encoding costs.

**Solution:**
We use a classical **Graph Neural Network (LightGCN)** to handle the high-dimensional sparse message-passing. 
1. **Input:** Raw user-item bipartite graph (highly sparse).
2. **Processing:** LightGCN performs 3 layers of message passing on classical GPUs.
3. **Output:** Low-dimensional (e.g., $d=16$) dense embeddings for users and items.
4. **Candidate Generation (Classical):** A classical Approximate Nearest Neighbor (ANN) search retrieves the top 100 candidate items for a user in real-time.

## 2. Quantum Layer: Combinatorial Diversity Ranking (QUBO)

The true bottleneck in modern e-commerce is not finding relevant items, but selecting a Top-10 list that maximizes *both* relevance to the user and *diversity* of the items, which is a known NP-Hard combinatorial optimization problem (Maximum Marginal Relevance).

**Solution:**
Instead of using a gate-based VQC for simple representation, we utilize a **Quantum Annealer (e.g., D-Wave)** to solve the combinatorial ranking.

* **Formulation:** The top 100 classical candidates are formulated into a Quadratic Unconstrained Binary Optimization (QUBO) matrix.
* **Objective Function:** 
  $$ \min_{x} \left( - \sum_{i=1}^{100} R_i x_i + \lambda \sum_{i,j} S_{ij} x_i x_j \right) $$
  Where $R_i$ is the classical GNN relevance score of item $i$, $S_{ij}$ is the classical similarity between items $i$ and $j$, and $x_i \in \{0, 1\}$ dictates if item $i$ is in the final Top-K list.
* **Quantum Execution:** This matrix is passed to the Quantum Annealer (or a simulated QAOA circuit if gate-based hardware is required).

## 3. Why this solves the research gaps:

1. **No Inference Latency on Gate-Based Simulators:** By using Quantum Annealing for the combinatorial ranking step, we utilize hardware that natively scales to thousands of variables, solving the QUBO in milliseconds.
2. **Real-world Sparsity:** Handled completely by the classical GNN.
3. **Justified Quantum Role:** The quantum component is solving a provably NP-Hard combinatorial problem (diversity ranking) that classical greedy algorithms only approximate. It is not a decorative non-linear layer.

## 4. Alternative VQC Architecture (If Gate-based is required)

If the project is strictly constrained to gate-based quantum computers (IBM Q, Pennylane), the methodology will pivot to an **Offline Quantum Kernel Embedding**:
* **Training:** A Quantum Kernel computes the exact Hilbert-space inner products between the 16-dimensional classical GNN embeddings of the hardest long-tail items.
* **Serving:** These quantum-refined embeddings are cached classically. Real-time inference remains $O(1)$ classical lookup. This directly solves the **Gap 1 (Inference Latency)** while providing quantum entanglement benefits.
