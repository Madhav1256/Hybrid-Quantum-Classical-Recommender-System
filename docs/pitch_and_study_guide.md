# Phase 1 Pitch & Study Guide: CG-QRH System

Use this guide to master the concepts behind your presentation. It provides the "script" for your slides, the underlying technical "Why," and the answers to questions your reviewers might ask.

---

## 🎤 The "Elevator Pitch" (Memorize This)
> *"Current recommender systems suffer from 'filter bubbles'—they recommend highly relevant but extremely similar items. Pure quantum computers can solve the combinatorial math to fix this, but they physically cannot handle millions of sparse e-commerce interactions due to memory (QRAM) limits. Our project, the **Classical-GNN Quantum-Ranking Hybrid (CG-QRH)**, solves this by splitting the workload: A classical Graph Neural Network compresses the massive data into dense embeddings to find the Top 100 relevant items, and a Quantum Annealer performs the NP-Hard combinatorial math to pick the final Top 10 most diverse items. We get Quantum accuracy without the latency."*

---

## 📝 Slide-by-Slide Speaker Notes

### Slide 1: Title Slide
* **What to say:** Introduce yourself, your team, and your guide. State the project title clearly. 
* **Key emphasis:** Emphasize the word **Hybrid**. This isn't just a quantum project; it's a realistic engineering architecture bridging GPUs (Classical) and QPUs (Quantum).

### Slide 2: Input Modelling (The Challenge)
* **What to say:** "To build a recommender, we use datasets like Amazon All_Beauty. The problem is sparsity. In a matrix of all users vs. all items, 99.99% of the cells are empty (most users haven't bought most items). Quantum circuits cannot process 99.99% empty matrices efficiently."
* **Technical term to know:** *Bipartite Graph*. It means a graph with two types of nodes (Users and Items). Edges only exist between a User and an Item (you can't have an edge between two users).

### Slide 3: Data Preparation (The 5-Core Filter)
* **What to say:** "To give our classical neural network a fighting chance to learn, we built an automated Python pipeline that applies a **5-core filter**. This iteratively strips out users and items with fewer than 5 interactions."
* **Why it matters:** If a user only clicked 1 item, a neural network can't learn their preferences. By filtering 700k sparse interactions down to 3.3k dense interactions, we guarantee high-quality data.

### Slide 4: Methodology Flow (The Core Innovation)
* **What to say:** "This is the heart of our project. We decoupled representation from ranking. Step 1: Classical LightGCN finds patterns. Step 2: FAISS grabs the Top 100 candidates instantly. Step 3 & 4: We translate those 100 items into a QUBO matrix and let the Quantum Annealer find the absolute best combination of relevance and diversity."
* **Technical term to know:** *QUBO* (Quadratic Unconstrained Binary Optimization). It's a mathematical equation that Quantum Annealers natively solve. 

### Slide 5: System Architecture
* **What to say:** Walk through the pipeline left to right. "Data goes into the GPU. The GPU feeds candidates to the QPU. The QPU gives the final result to the user."
* **Key emphasis:** Real-world feasibility. By only sending 100 items to the Quantum computer instead of 100,000, our system runs in milliseconds. 

### Slide 6: Validation (Proving it works)
* **What to say:** "How do we know the Quantum part actually helps? We will run an A/B test against a purely classical baseline. We expect the classical model to have slightly better accuracy, but the Hybrid model to have significantly better diversity."

### Slide 7: Verification (Sanity Checks)
* **What to say:** "Before we trust the Quantum results, we verify our pipeline. We have mathematical assertions that ensure our QUBO equation is actually penalizing similar items correctly before we spend expensive cloud credits on the D-Wave QPU."

### Slide 8: Metrics (The Math)
* **What to say:** Explain what NDCG and ILD mean in plain English.
* **NDCG (Normalized Discounted Cumulative Gain):** It measures *Relevance*. If the user wanted a Red Shirt, did we put it at rank #1 or rank #10? Higher is better.
* **ILD (Intra-List Diversity):** It measures *Variety*. Are all 10 recommended items Red Shirts? (Low ILD). Or did we recommend a Red Shirt, Blue Jeans, and a Hat? (High ILD).

---

## 🛡️ Defending the Project (Q&A Prep)

**Q1: Why not just use a Quantum Neural Network for the whole thing?**
> **Answer:** "Current NISQ-era (Noisy Intermediate-Scale Quantum) computers lack the QRAM to load a 100,000-item matrix. Even if they could, encoding that much sparse data into quantum angles causes the circuit to become too deep, introducing noise and destroying the result. Classical GPUs are fundamentally better at processing large sparse graphs."

**Q2: Why use LightGCN instead of standard Matrix Factorization?**
> **Answer:** "Standard Matrix Factorization doesn't capture high-order connectivity (e.g., User A bought Item 1, User B bought Item 1 and Item 2 -> therefore User A might like Item 2). LightGCN captures these deep graph relationships natively without the heavy non-linear math of standard neural networks."

**Q3: What does the QUBO equation actually do?**
> **Answer:** "It's a balancing act. The equation is: Maximize Relevance (user-item dot product) MINUS Diversity Penalty (item-item cosine similarity). The Quantum Annealer tries to find the binary array of 1s and 0s (which items to keep) that results in the lowest possible energy state of that equation."

**Q4: What if you can't get access to the D-Wave Quantum hardware?**
> **Answer:** "We have built a fallback in our architecture. If the D-Wave Leap API rate-limits us, our code automatically falls back to 'Simulated Annealing' running on our classical CPU, ensuring the pipeline never breaks."
