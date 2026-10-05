# Review 2 Pitch & Study Guide: Literature Survey & Gaps

This guide is specifically tailored to your **Review 2** presentation (`Review_2_new.pptx`). Review 2 is all about proving to the jury that you have deeply read the existing research, identified its flaws, and designed your project to fix those specific flaws.

---

## 🎤 The "Review 2" Elevator Pitch
> *"In our literature survey of 11 recent papers, we found a recurring theme: quantum recommenders are mostly theoretical. They run on simulators, use tiny toy datasets with only 500 features, and assume the existence of 'QRAM' to load data instantly. In the real world, e-commerce data is >99.9% sparse, and QRAM doesn't exist at scale. Our project, CG-QRH, is designed to fix these exact gaps by moving the heavy data-loading to a Classical GPU, and reserving the Quantum Computer strictly for the combinatorial ranking math it was built for."*

---

## 📝 Slide-by-Slide Speaker Notes

### Slide 2 & 3: Literature Survey (Applied & Theoretical)
* **What to say:** "We analyzed 11 state-of-the-art papers published between 2024 and 2025. Papers 1-6 attempt to apply quantum to recommenders, while papers 7-11 are purely theoretical."
* **The key takeaway to highlight:** Point out that almost all of them rely on **simulators** or tiny datasets (like the QuantumCLEF dataset with only 1.9K users). None of them are testing on massive, real-world e-commerce datasets like Amazon. 

### Slide 4: Research Gaps Identified (CRITICAL SLIDE)
*This is the most important slide in Review 2. You need to sound highly critical of current research.*
* **Gap 1: Latency is ignored.** "Researchers are running full quantum circuits for a single recommendation. That takes too long for Amazon. *Our fix:* Keep quantum strictly offline/batched."
* **Gap 2: Toy Datasets.** "Current papers use datasets that are artificially dense. Real data is 99.9% sparse. *Our fix:* We use a classical GNN to absorb that sparsity."
* **Gap 3: No Fair Classical Ablation.** "Many papers claim Quantum is better, but they don't test it against a strong classical baseline like Simulated Annealing. *Our fix:* We will test Quantum Annealing directly against Simulated Annealing on the exact same QUBO."
* **Gap 4: Using Quantum where GPUs win.** "GPUs are already perfect at learning representations (embeddings). Quantum should only be used for NP-Hard combinatorial problems. *Our fix:* We only use Quantum for the Top-K diversity ranking."

### Slide 5: Objectives and Expected Outcomes
* **What to say:** "Based on these gaps, our objectives are clear."
  * **O1 (Classical):** Build a LightGCN model to handle the >99.9% sparse data and generate embeddings.
  * **O2 (Quantum):** Formulate the Top-K selection as a QUBO (balancing relevance vs diversity) and solve it on D-Wave.
  * **O3 (Evaluation):** Run a rigorous ablation study (comparing Greedy vs. Simulated Annealing vs. Quantum) to honestly prove where the gain comes from.

### Slide 6: Methodology: CG-QRH
* **What to say:** "This brings us to our proposed solution: The Classical-GNN Quantum-Ranking Hybrid. The Navy Blue steps are classical (Graph -> LightGCN -> Top 100 Candidates). The Gold step is Quantum (QUBO -> D-Wave -> Top 10 List). By decoupling these, we solve the QRAM bottleneck and the latency issues found in our literature survey."

---

## 🛡️ Defending the Gaps (Q&A Prep)

**Q1: What do you mean by "No fair classical ablation" (Gap 3)?**
> **Answer:** "An ablation study means removing a piece of the system to see if it still works. Many quantum papers compare their Quantum algorithm against a very weak classical algorithm. To be fair, we must test the Quantum Annealer against a Classical CPU running 'Simulated Annealing' on the exact same QUBO equation. If the Quantum hardware doesn't beat Simulated Annealing, then the hardware isn't actually helping."

**Q2: What is QRAM and why is it a problem in the literature?**
> **Answer:** "QRAM stands for Quantum Random Access Memory. Many theoretical papers (like papers 7 and 9 in our survey) assume we can instantly load massive amounts of data into a quantum state. Physically, large-scale QRAM does not exist yet. That's why our system relies on classical GPUs to process the massive data, avoiding the QRAM bottleneck entirely."
