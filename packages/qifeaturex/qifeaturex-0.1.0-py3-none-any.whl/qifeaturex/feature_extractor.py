from typing import Sequence, Optional
import numpy as np
import pandas as pd

from .features import entropy_features, entanglement_features, coherence_features

def extract_features(
    states: Sequence[np.ndarray],
    dims: Optional[tuple] = None,
    feature_kinds: Optional[Sequence[str]] = None,
    base: int = 2,
) -> pd.DataFrame:
    """
    Main user-facing function.

    states: list/sequence of density matrices or statevectors
    dims: tuple like (dA, dB) for bipartite systems
    feature_kinds: list among ["entropy", "entanglement", "coherence"]
    """
    if feature_kinds is None:
        feature_kinds = ["entropy", "entanglement", "coherence"]

    rows = []
    for idx, rho in enumerate(states):
        row = {"sample_id": idx}
        if "entropy" in feature_kinds:
            row.update(entropy_features(rho, dims=dims, base=base))
        if "entanglement" in feature_kinds:
            if dims is None:
                if hasattr(rho, "shape") and rho.shape[0] == 4:
                    dims_use = (2, 2)
                else:
                    dims_use = dims
            else:
                dims_use = dims
            row.update(entanglement_features(rho, dims=dims_use, base=base))
        if "coherence" in feature_kinds:
            row.update(coherence_features(rho, base=base))

        rows.append(row)

    return pd.DataFrame(rows)
