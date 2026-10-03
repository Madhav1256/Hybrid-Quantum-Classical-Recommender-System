# Literature Gap Analysis: Hybrid Quantum-Classical Recommender Systems

## 1. Analysis of Existing Papers

A comprehensive review of the 11 highly relevant research papers (published 2024–2026) reveals a nascent but rapidly evolving field. While the theoretical foundations for quantum speedups in linear systems (e.g., *An Exponential Separation Between Quantum and Quantum-Inspired Classical Algorithms*, 2024) and tensor decompositions (*Quantum Algorithms for tensor-SVD*, 2024) are solidifying, applied quantum recommender systems suffer from systemic methodological issues.

Most applied papers (e.g., *Quantum Semi-Random Forests for Qubit-Efficient Recommender Systems*, 2025; *Collaborative Filtering using Variational Quantum Hopfield Associative Memory*, 2025) rely on downsampled, dense subsets of traditional datasets (like MovieLens or small slices of Amazon Reviews). Because of the limitations of NISQ (Noisy Intermediate-Scale Quantum) devices, circuits are restricted to `<20` qubits on state-vector simulators, which naturally enforces severe data dimensionality reduction prior to any quantum processing.

## 2. Methodological Weaknesses (Datasets & Scaling)

**The "Large-Scale E-Commerce" Illusion:**
None of the applied papers reviewed demonstrate genuine "large-scale e-commerce recommendation." 
* **Tiny Datasets:** Papers regularly claim applicability to e-commerce but validate on datasets with a few hundred users and items. 
* **Data Leakage & Splitting:** Because the models require dense data to function, researchers often aggressively filter out users with fewer than 50 interactions. This entirely destroys the long-tail and cold-start distributions that represent the actual challenge of e-commerce.
* **Lack of Real-world Sparsity:** Real e-commerce sparsity is often $>99.9\%$. The subsets tested in these papers frequently exhibit artificial densities of $5\% - 10\%$.

## 3. Quantum-Specific Weaknesses

**Ignoring the QRAM and Data-Loading Bottleneck:**
Theoretical papers (*Quantum Algorithms for tensor-SVD*) assume the existence of Quantum Random Access Memory (QRAM) to achieve logarithmic time complexity. In applied hybrid models (*Graph Neural Networks on Quantum Computers*), the cost of classically computing state preparation angles and loading classical e-commerce data into quantum states (Amplitude or Angle Encoding) often exceeds the time it would take to just perform the forward pass classically. This preprocessing cost is routinely excluded from the "computational advantage" claims.

**Simulator vs. Hardware Reality:**
With the exception of papers utilizing D-Wave Quantum Annealers (*Consensus ranking by quantum annealing*, *Performance-Driven QUBO for Recommender Systems*), almost all gate-based quantum recommender models are evaluated on ideal simulators. They completely ignore:
* Shot count (the statistical cost of measuring the output distribution).
* Decoherence and gate error rates (which destroy the theoretical representation capability of Variational Quantum Circuits at depth).

## 4. Hybrid Architecture Flaws: The "Decorative" Quantum Layer

In many proposed hybrid frameworks (like *Quantum Cognition-Inspired EEG-based Recommendation via Graph Neural Networks*), the quantum component (usually a VQC) is inserted as a dense non-linear mapping layer between classical embeddings and the classical output layer. 
* **Decorative Usage:** Because these VQCs are small (e.g., 8 qubits) and have limited entanglement capability, they often act simply as a low-rank bottleneck or a source of regularization.
* **Unfair Comparisons:** Authors frequently compare a Hybrid Classical-VQC model against a classical model with a completely different number of parameters. When a classical neural network is constrained to the exact same parameter count and bottleneck size as the VQC, the "quantum advantage" usually disappears.

## 5. Classical Recommender Weaknesses

Traditional recommender limitations (Cold-start, Sparsity, Popularity Bias) are largely ignored by the current quantum literature, which focuses merely on matching classical RMSE or NDCG scores. 
However, **ranking optimization** (where sorting millions of candidates is a combinatorial challenge) and **feature selection** (*Estimating Quantum Execution Requirements for Feature Selection*) are realistic bottlenecks where quantum annealing and QUBO formulations show actual, measurable promise over classical approximations.

## 6. Evaluation Mistakes

* **Lack of Ranking Metrics:** Papers focusing on matrix factorization equivalents often report only RMSE/MAE. E-commerce requires ranking (NDCG@K, Recall@K).
* **Missing Inference Cost:** Papers boast about lower parameter counts in quantum models but fail to report that evaluating a VQC requires 1,000+ shots (executions) per user-item pair, making real-time e-commerce inference mathematically impossible under current paradigms.

## 7. Conclusions on Scalability

The claim of "large-scale" in gate-based quantum recommender literature is currently **unsupported**. Theoretical scalability exists mathematically, but applied scalability is entirely bounded by I/O bottlenecks (classical-to-quantum encoding). 

However, **Quantum Annealing for Consensus Ranking and QUBO formulations** (*Performance-Driven QUBO for Recommender Systems on Quantum Annealers*) represent a **partially demonstrated** scalability, as D-Wave architectures can currently map thousands of variables, making them the most viable candidate for near-term large-scale hybrid integration.
