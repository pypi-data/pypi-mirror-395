from typing import Sequence, Optional, Tuple
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from ..feature_extractor import extract_features

class QIFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Sklearn-compatible transformer that converts quantum states
    into feature vectors using QIFeatureX.
    """

    def __init__(
        self,
        dims: Optional[Tuple[int, int]] = None,
        feature_kinds: Optional[Sequence[str]] = None,
        base: int = 2,
    ):
        self.dims = dims
        self.feature_kinds = feature_kinds
        self.base = base
        self._feature_names = None

    def fit(self, X, y=None):
        df = extract_features(
            states=X,
            dims=self.dims,
            feature_kinds=self.feature_kinds,
            base=self.base,
        )
        self._feature_names = [col for col in df.columns if col != "sample_id"]
        return self

    def transform(self, X):
        df = extract_features(
            states=X,
            dims=self.dims,
            feature_kinds=self.feature_kinds,
            base=self.base,
        )
        if self._feature_names is None:
            self._feature_names = [col for col in df.columns if col != "sample_id"]
        return df[self._feature_names].to_numpy(dtype=float)

    def get_feature_names_out(self, input_features=None):
        if self._feature_names is None:
            return np.array([])
        return np.array(self._feature_names)
