# Research Gaps in Hybrid Quantum-Classical Recommender Systems

This document ranks the strongest research gaps based purely on evidence from the 2024–2026 literature.

---

### Gap 1: The Data-Loading and Shot-Count Overhead is Ignored in Inference

**Evidence:**
Papers such as *Graph Neural Networks on Quantum Computers* (2024) and *Collaborative Filtering using Variational Quantum Hopfield Associative Memory* (2025) report parameter reductions, but evaluate on ideal simulators without calculating the latency of Amplitude/Angle encoding or the necessity of repeated measurements (shots).

**Why it matters:**
In large-scale e-commerce, latency is critical (e.g., <100ms SLA). If a quantum model requires 1,024 shots per user-item candidate, it is functionally useless for real-time ranking, negating any theoretical parameter advantage.

**Unresolved:**
How to design a hybrid architecture where the quantum component is invoked *offline* (e.g., during asynchronous batch embedding generation) rather than *online* during real-time inference.

**How our project addresses it:**
By decoupling the quantum representation learning from the real-time serving layer. We will use the quantum component strictly for offline user/item embedding generation, storing the results in a classical vector database for real-time ANN (Approximate Nearest Neighbor) retrieval.

---

### Gap 2: Evaluation on Artificially Dense, Toy Datasets

**Evidence:**
*Quantum Semi-Random Forests for Qubit-Efficient Recommender Systems* (2025) and *CRUISE on Quantum Computing for Feature Selection in Recommender Systems* (2024) rely on severely truncated, dense subsets of Amazon and MovieLens data to fit within <20 qubit constraints.

**Why it matters:**
Filtering out long-tail items and cold-start users transforms the e-commerce recommendation problem into a trivial dense matrix problem, which classical algorithms (like SVD or ALS) already solve perfectly in milliseconds. 

**Unresolved:**
Can quantum algorithms actually handle the extreme sparsity ($>99.9\%$) of unmodified e-commerce data?

**How our project addresses it:**
We will test on unmodified, highly sparse datasets (Amazon Reviews 2023, RetailRocket). To handle this on limited qubits, our hybrid model will use a classical Graph Neural Network (GNN) to perform the high-dimensional sparse-to-dense message passing, reserving the quantum component for a low-dimensional highly-entangled interaction crossing layer.

---

### Gap 3: "Decorative" Quantum Layers Failing Fair Classical Ablation

**Evidence:**
Many hybrid VQC (Variational Quantum Circuit) papers fail to compare the VQC against a classical neural network with the exact same architecture, bottleneck size, and parameter count. 

**Why it matters:**
Without a matched-parameter classical baseline, it is impossible to know if the performance gain is due to "quantum entanglement" or simply the mathematical regularization effect of passing data through a low-rank bottleneck.

**Unresolved:**
Rigorous proof of functional quantum advantage in applied hybrid architectures.

**How our project addresses it:**
We explicitly design a "Classical Equivalent Ablation". If our hybrid model replaces a classical dense layer with a 10-qubit VQC (which has roughly 30 trainable rotation parameters), our baseline will be a classical PyTorch model with a 30-parameter dense layer to prove whether the quantum Hilbert space representation is actually doing the heavy lifting.

---

### Gap 4: Misalignment of Quantum Strengths with Recommendation Bottlenecks

**Evidence:**
*Performance-Driven QUBO for Recommender Systems on Quantum Annealers* (2024) and *Consensus ranking by quantum annealing* (2025) demonstrate that quantum annealers are excellent at combinatorial optimization (ranking, feature selection). Yet, much of the gate-based literature forces quantum circuits into the role of basic dot-product representation learning, where classical GPUs reign supreme.

**Why it matters:**
Using a quantum computer to do basic matrix multiplication is inefficient. Quantum systems excel at sampling complex distributions and solving combinatorial spaces.

**Unresolved:**
Using quantum computing for the *Candidate Ranking* phase as a combinatorial optimization problem rather than a representation learning problem.

**How our project addresses it:**
If justified by our dataset scaling analysis, we will formulate the final Top-K list generation as a Quadratic Unconstrained Binary Optimization (QUBO) problem, maximizing relevance while explicitly penalizing similarity (to enforce diversity). This offloads the combinatorial diversity-ranking problem to a Quantum Annealer, a task where classical systems struggle at scale.
