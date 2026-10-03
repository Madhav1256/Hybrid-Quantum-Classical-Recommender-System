# Hybrid Quantum-Classical Recommender System for Large-Scale E-Commerce

This repository contains the code, data pipelines, and literature analysis for developing and evaluating a hybrid quantum-classical recommender system.

## Project Structure

* **`literature/`**: Contains the foundational research papers and our rigorous gap/methodology analysis.
* **`data/`**: Datasets (raw and processed, e.g., Amazon Reviews, RetailRocket).
* **`notebooks/`**: Jupyter notebooks for EDA, prototyping, and result visualization.
* **`src/`**: Core source code.
  * `classical_models/`: Classical GNNs, Matrix Factorization, LightGCN.
  * `quantum_models/`: QUBO formulations, QAOA, and Quantum Annealer interfaces (D-Wave).
  * `data_processing/`: Scripts for graph construction, dataset sparsity handling, and classical-to-quantum encoding.
  * `evaluation/`: End-to-end evaluation metrics (NDCG, Recall, ILD, latency).
* **`scripts/`**: Executable scripts for running large-scale training and evaluation pipelines.

## Methodology

This project explicitly focuses on a **Classical-GNN Quantum-Ranking Hybrid (CG-QRH)** architecture:
1. **Classical Representation**: A classical Graph Neural Network (GNN) handles the >99.9% sparse interaction data to generate high-quality user and item embeddings.
2. **Quantum Combinatorial Ranking**: A Quantum Annealer (or QAOA) receives the classical candidates and solves a Maximum Marginal Relevance (MMR) QUBO formulation to optimize both accuracy and diversity in the Top-K list.

For full rationale, see `literature/analysis/proposed_methodology.md`.

## Datasets

This project evaluates the CG-QRH architecture on highly sparse, real-world e-commerce datasets:

1. **Amazon Reviews 2023 (`All_Beauty`):**
   * **Users:** 631,986
   * **Items:** 112,565
   * **Interactions:** 701,528
   * **Sparsity:** 0.99999014
   * Provides explicit feedback and metadata.

2. **RetailRocket:**
   * **Users:** 1,407,580
   * **Items:** 235,061
   * **Interactions:** 2,756,101
   * **Sparsity:** 0.99999167
   * Provides implicit feedback (Views, Add-to-Carts, Transactions).
