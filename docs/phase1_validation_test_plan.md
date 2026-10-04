# Phase 1: Verification, Validation & Test Plan

This document outlines the evaluation strategy for the **Classical-GNN Quantum-Ranking Hybrid (CG-QRH)** system. We must rigorously prove that the Quantum Annealer increases recommendation diversity without destroying the relevance ranking learned by the classical GNN.

## 1. Validation Metrics

The evaluation is split into Ranking Quality (Relevance) and Diversity Quality. We will measure these on a hold-out test set (e.g., the last interacted item per user).

### A. Ranking Quality (Relevance)
* **Hit Ratio (HR@K):** Did the true interacted item appear in the Top K list? Measures basic retrieval success.
* **Normalized Discounted Cumulative Gain (NDCG@K):** Was the true interacted item ranked near the top of the list? Measures ranking precision.

### B. Diversity Quality (Quantum Advantage)
* **Intra-List Diversity (ILD@K):** The average pairwise distance ($1 - \text{Cosine Similarity}$) between all items in a user's Top K recommended list. This is the primary metric the Quantum MMR formulation aims to maximize.
* **Catalog Coverage:** The percentage of total available items that are recommended at least once across all users.

### C. System Metrics
* **QPU Access Time:** The actual time (in microseconds) spent executing on the D-Wave Quantum Processing Unit.
* **End-to-End Latency:** The total time from Classical Candidate Generation $\rightarrow$ QUBO Formulation $\rightarrow$ Quantum Result.

## 2. Test Plan & Baselines

To prove the validity of our hybrid architecture, we will execute the following comparative test plan:

### Test 1: Classical Baseline (GNN Only)
* **Execution:** LightGCN -> FAISS -> Top K (No Quantum).
* **Expected Result:** High NDCG, but low ILD (the "filter bubble" effect where all recommended items are nearly identical).

### Test 2: Hybrid System (CG-QRH)
* **Execution:** LightGCN -> FAISS Top 100 Candidates -> QUBO Diversity Optimization -> D-Wave Quantum Annealer -> Top K.
* **Expected Result:** A statistically significant increase in ILD and Catalog Coverage with a minimal, acceptable drop in NDCG.

### Test 3: System Verification Tests (Unit Tests)
1. **Embedding Verification:** Assert that GNN output embeddings correctly map to the FAISS index IDs without off-by-one errors.
2. **QUBO Sanity Check:** Assert that the generated QUBO matrix penalizes identical items (high similarity) and rewards highly relevant items.
3. **Quantum Fallback:** Ensure the system smoothly falls back to Simulated Annealing (using `dimod.SimulatedAnnealingSampler`) if the D-Wave Leap API is rate-limited.
