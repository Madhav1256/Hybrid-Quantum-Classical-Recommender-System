# Phase 1 Presentation Content

Below is the structured data and bullet points for your PowerPoint presentation. You can copy and paste this text directly into your slides.

---

### **Slide 1: Title Slide**
**Title:** Phase 1: Foundation of the Hybrid Quantum-Classical Recommender System
**Subtitle:** Input Modeling, System Architecture, and Evaluation Strategy
**Framework:** Classical-GNN Quantum-Ranking Hybrid (CG-QRH)

---

### **Slide 2: Input Modelling**
* **The Challenge:** Raw e-commerce data (Amazon All_Beauty, RetailRocket) exhibits >99.99% sparsity, making it impossible to pass directly into a Quantum circuit.
* **The Model:** We modeled the interactions as a **Bipartite Graph** (Users $\leftrightarrow$ Items) using implicit feedback (ratings/views as edges).
* **ID Translation:** Complex alphanumeric IDs (e.g., ASINs) are dynamically mapped to contiguous integer spaces, enabling matrix operations.
* **Target Schema:** The ultimate schema is a PyTorch Geometric `HeteroData` structure, natively optimized for Graph Neural Networks.

---

### **Slide 3: Input Modelling: Data Preparation**
* **K-Core Filtering Strategy:** Applied an iterative 5-core threshold to eliminate extreme sparsity.
* **Execution Script:** `src/data_processing/amazon_loader.py`
* **Raw Input:** `data/raw/.../All_Beauty.jsonl` (701,528 interactions)
* **Final Output:** `data/processed/amazon_all_beauty/graph.pt` (PyTorch HeteroData graph)

*(Visual Recommendation: Add a dark-mode screenshot or text block showing our exact pipeline output below)*
**Pipeline Output Proof:**
> `Applying 5-core filtering...`
> `Iteration 1: (11359, 4)`
> `...`
> `Iteration 19: (3315, 4)`
> `Final shape after 5-core filtering: (3315, 4)`
> `Building PyTorch Geometric HeteroData graph...`
> `Data processing complete! Processed 357 users and 479 items.`

---

### **Slide 4: Methodology Flow**
* **Goal:** Avoid the "Inference Latency" bottleneck by mathematically decoupling representation from ranking.
* **Step 1 (Classical Embedding):** The sparse bipartite graph is processed by LightGCN to generate low-dimensional dense embeddings for users and items.
* **Step 2 (Classical Filtering):** Real-time Approximate Nearest Neighbor search (FAISS) extracts the Top 100 relevant candidates in $O(1)$ time.
* **Step 3 (Quantum Optimization):** The candidates are formulated into a **QUBO Matrix** representing a Maximum Marginal Relevance (MMR) objective.
* **Step 4 (Quantum Execution):** A D-Wave Quantum Annealer samples the QUBO to output the final Top K list, balancing relevance with maximum diversity.

---

### **Slide 5: System Design / Architecture**
*(Visual Recommendation: Insert the Mermaid flowcharts from `docs/phase1_system_architecture.md` here)*
* **Data Layer:** Extractor scripts $\rightarrow$ Filter Pipeline $\rightarrow$ `graph.pt`.
* **Classical Layer (GPU):** PyTorch LightGCN $\rightarrow$ Candidate Pool Generation.
* **Quantum Layer (QPU):** Candidate Subsets $\rightarrow$ QUBO Formulation $\rightarrow$ D-Wave Ocean SDK API.
* **Decoupled Serving:** By restricting Quantum usage strictly to combinatorial diversity ranking on a small candidate pool, the architecture ensures millisecond real-world inference times.

---

### **Slide 6: Validation**
* **The Validation Core:** We must definitively prove the Quantum Annealer provides a tangible advantage over a purely classical pipeline.
* **Baseline Test (Classical Only):** 
  * LightGCN + FAISS. 
  * *Expectation:* High relevance, but susceptible to "filter bubbles" (items are too similar).
* **Hybrid Test (CG-QRH System):** 
  * LightGCN + D-Wave. 
  * *Expectation:* A statistically significant increase in Catalog Coverage and Diversity, with only a marginal, acceptable trade-off in baseline relevance.

---

### **Slide 7: Verification**
* **Data Integrity Checks:** Ensure graph generation correctly maps string IDs to tensor indices without off-by-one mapping errors.
* **QUBO Sanity Verification:** Mathematically assert that the objective function correctly penalizes identical items (cosine similarity $\approx$ 1) and rewards high-relevance dot-products before sending to the QPU.
* **System Resilience:** Implemented graceful fallbacks ensuring that if the D-Wave Leap API rate-limits are reached, the system defaults to Simulated Annealing.

---

### **Slide 8: Validation Metrics and Test Plan**
* **Execution Script:** `src/evaluation/metrics.py` (Contains mathematical logic for automated scoring).
* **Relevance Metrics (Evaluating the Classical GNN):**
  * **Hit Ratio (HR@K):** Did the user's true interacted item appear in the Top K list? (Retrieval success).
  * **NDCG@K:** Was the true item ranked near the top? (Ranking precision).
* **Diversity Metrics (Evaluating the Quantum Advantage):**
  * **Intra-List Diversity (ILD@K):** The average pairwise distance ($1 - \text{Cosine Similarity}$) among all items in a user's final Top K list.

*(Visual Recommendation: Add this code snippet from our metrics.py to show the exact mathematical execution)*
**Metrics Implementation Proof:**
> `def intra_list_diversity_at_k(recommended_list, item_embeddings, k):`
> `    # Calculates avg pairwise distance (1 - cosine similarity)`
> `    ...`
> `    distance = 1.0 - (dot_product / (norm_i * norm_j))`
> `    diversity_sum += distance`

---

### **Slide 9: Thank You**
* **Questions & Answers**
* **Next Steps:** Proceeding to Phase 2 (Developing and Training the PyTorch Classical GNN).
