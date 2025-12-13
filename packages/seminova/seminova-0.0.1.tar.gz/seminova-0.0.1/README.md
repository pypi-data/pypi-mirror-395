# **seminova**

### *Python bindings for an experimental SuperNova IVC (Rust backend)*

`seminova` is a Python wrapper around an experimental Rust implementation of **SuperNova-style IVC folding**, with direct R1CS construction from Python.
It’s not a full zkSNARK or anything close to production, but it works, it’s fast, and it’s great to play around with folding proofs with it.

---

## ⚠️ Disclaimer

This **isn’t** the complete SuperNova protocol from the Microsoft paper. It’s basically a trimmed-down toolkit to play with the folding part.

* ❌ not fully sound
* ❌ not zero-knowledge
* ❌ not meant for production at all
* ✔️ great for learning and experimentation
* ✔️ fast enough for small/medium circuits
* ✔️ useful if you want to understand IVC

---

# What Works Today

* Build R1CS matrices directly from Python (no ceremony)
* Create `PyR1CS` objects and fold them together
* Basic satisfiability checks (non-zk)
* Incrementally update proofs with new folded instances
* Access commitments, digests, witness/instance bytes

---

# Future Plans

* zero-knowledge (hiding commitments)
* point proof gadgets
* DSL for augmented circuits
* more like an actual SuperNova
* probably not a subnova anymore

---

# Source

Repository: https://github.com/debxylen/seminova

---

# License

MIT.

---

# Credits

The rust backend is sourced from the MIT-licensed implementation from:
[https://github.com/jules/supernova](https://github.com/jules/supernova)
