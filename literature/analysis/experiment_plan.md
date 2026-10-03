# Experiment and Ablation Plan

To ensure a scientifically defensible outcome and prevent manufacturing a fake quantum advantage, the following experimental protocol is established.

## 1. Datasets
* **Amazon Reviews 2023 (Beauty & Electronics):** Retaining long-tail items (filtering only users $<5$ interactions, rather than the standard $<50$ used in quantum literature).
* **RetailRocket (E-commerce):** Highly sparse implicit feedback data.

## 2. Baselines
1. **Matrix Factorization (BPR-MF):** Standard linear baseline.
2. **LightGCN:** SOTA classical sparse message-passing.
3. **Classical Greedy MMR (Maximal Marginal Relevance):** The classical equivalent to our Quantum QUBO ranking.

## 3. Strict Ablation Protocol

To answer: *"Is the improvement actually caused by the quantum component?"*

| Model Variant | Representation | Ranking Algorithm | Purpose |
|---------------|----------------|-------------------|---------|
| **Classical Only** | LightGCN | Greedy Classical | Establishes the classical ceiling. |
| **Simulated Annealing** | LightGCN | Classical Simulated Annealing | Tests if the QUBO formulation itself causes the lift, rather than quantum tunneling. |
| **Hybrid Quantum** | LightGCN | D-Wave Quantum Annealer (or QAOA) | The proposed solution. |

*If the Simulated Annealing classical variant matches the Quantum Annealer's NDCG/Diversity scores, we will honestly report that the advantage lies in the mathematical QUBO formulation, not the quantum hardware.*

## 4. Metrics Evaluated
* **Accuracy:** NDCG@10, Recall@10, MAP@10.
* **Diversity:** Intra-List Diversity (ILD), Coverage.
* **Systems:** End-to-end Inference Latency (ms), Training Time (hrs).

## 5. Scaling Experiments
1. **Candidate Scaling:** Pass 50, 100, 200, and 500 candidates to the Quantum Ranker. Measure where classical greedy ranking begins to fail versus the quantum solver.
2. **Sparsity Analysis:** Bucket users into cold (<10 interactions), warm (10-50), and active (>50). Measure quantum ranking lift across these cohorts.
