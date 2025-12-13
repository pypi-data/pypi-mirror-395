# QIFeatureX 🔮  
### Quantum Information Feature Engineering Library

[![PyPI version](https://badge.fury.io/py/qifeaturex.svg)](https://badge.fury.io/py/qifeaturex)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-early--alpha-purple)

QIFeatureX is an open-source **Quantum Information Feature Engineering** library that converts **quantum states** (pure vectors or density matrices) into **machine-learning-ready numerical feature vectors**. It enables ML-driven analysis of entanglement, coherence, entropy, nonlocality, and quantum similarity without heavy symbolic calculations.

QIFeatureX is designed for research in **quantum computing**, **quantum communication**, **quantum sensing**, **quantum machine learning**, and **condensed matter physics**.

---

## ✨ Key Features
- 📌 Convert quantum states → structured ML feature tables
- 📌 Support for pure states (`|ψ⟩`) and density matrices (`ρ`)
- 📌 Entanglement metrics: concurrence, negativity, log-negativity, tangle
- 📌 Entropy metrics: von Neumann, Rényi-2, linear entropy
- 📌 Coherence measures: ℓ₁-coherence, relative entropy of coherence
- 📌 Mutual information & bipartite correlations
- 📌 Bell-CHSH violation measurement
- 📌 Quantum similarity distances: trace distance, fidelity, Bures, Hilbert-Schmidt
- 📌 Fully compatible with **scikit-learn pipelines**

---

## 🚀 Installation

```bash
pip install qifeaturex

### 2. Right below that section, paste the Basic Usage example block:

```markdown
---

## 🧠 Basic Usage Example

```python
import numpy as np
from qifeaturex import extract_features
from qifeaturex.ml import QIFeatureExtractor
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

def bell_state_phi_plus():
    psi = np.zeros(4, dtype=complex)
    psi[0] = psi[3] = 1/np.sqrt(2)
    return psi

# Create a Bell state and convert to density matrix
psi = bell_state_phi_plus()
rho = np.outer(psi, psi.conj())

# Extract features
df = extract_features([rho], dims=(2,2))
print(df)

