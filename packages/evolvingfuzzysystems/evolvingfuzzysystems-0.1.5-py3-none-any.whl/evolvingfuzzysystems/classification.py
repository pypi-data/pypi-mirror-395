"""
ENFSUni0Evolving
================

Python implementation of an evolving neuro-fuzzy classifier inspired by:

- Autonomous Data Partitioning Algorithm (ADPA)
  (Angelov & Gu, Information Sciences, 2018)
- Uni/Null-uninorm based fuzzy neurons as used in Souza & Lughofer
- Recursive Least Squares (RLS) learning for the consequent layer
  (similar spirit to your MATLAB code: Q, v update)

High-level structure
--------------------

- Each *data cloud* (ADPA prototype) becomes a fuzzy rule.
- Antecedent of each rule:
    * Center c_r (R^d)
    * Scalar radius / sigma_r (float)
    * Support count
    * Uni-null uninorm parameters (g1_r, g2_r, z_r)
    * Weight vector w_r (per-feature relevance in the neuron)
- Firing level of rule r for input x:
    1) Compute per-feature Gaussian memberships a_{r,j}(x_j)
    2) Combine via UniNullNeuron:
           h_j = w_{r,j} * a_{r,j} + (1 - w_{r,j}) * z_r
           y_r = U2-uninorm( h_1, ..., h_d ; g1_r, g2_r, z_r )
- Consequent layer:
    - Let φ(x) = [1, y_1(x), ..., y_R(x)]  (bias + rule activations)
    - Class scores: s(x) = φ(x)^T W   (W in R^{(R+1) x C})
    - Prediction: argmax_c s_c(x)
    - W and covariance P are updated by recursive least squares (RLS)
      with forgetting factor λ.

The class provides:
    - predict_one(x), predict(X)
    - learn_one(x, y), partial_fit(X, y)
    - attribute n_rules_ (number of rules)
    - history_n_rules (for plotting evolution)

Author: Dr. Paulo Vitor de Campos Souza.
@article{DECAMPOSSOUZA2021231,
title = {An evolving neuro-fuzzy system based on uni-nullneurons with advanced interpretability capabilities},
journal = {Neurocomputing},
volume = {451},
pages = {231-251},
year = {2021},
issn = {0925-2312},
doi = {https://doi.org/10.1016/j.neucom.2021.04.065},
url = {https://www.sciencedirect.com/science/article/pii/S092523122100607X},
author = {Paulo Vitor {de Campos Souza} and Edwin Lughofer},
keywords = {Evolving neuro-fuzzy system (ENFS-Uni0), Uni-nullneurons, On-line interpretability of fuzzy rules, Degree of rule changes, Incremental feature importance levels, Indicator-based recursive weighted least squares (I-RWLS)},
abstract = {This paper proposes a hybrid architecture based on neural networks, fuzzy systems, and n-uninorms for solving pattern classification problems, termed as ENFS-Uni0 (short for evolving neuro-fuzzy system based on uni-nullneurons). The model can produce knowledge in an on-line (single-pass) and evolving learning context in a particular form of neuro-fuzzy rules representing the dependencies among input features through IF-THEN type relations. The rules antecedents are thereby realized through uni-nullneurons, which are constructed from n-uninorms, leading to the possibility to express both, AND- and OR-connections (and a mixture of these) among the single antecedent parts of a rule (and thus achieving an advanced interpretability aspect of the rules). The neurons’ evolution is done through an extended version of an autonomous data partition method (ADPA). On-line interpretation of the timely evolution of rules is addressed by (i) a concept for tracking the degree of changes of the rules over data stream samples, which may indicate experts/operators how much dynamics is in the process and may be used as a structural active learning component to request operator’s feedback in the case of significant changes and (ii) a concept for updating feature weights incrementally. These weights express the (possibly changing) impact degrees of features on the classification problem: features with low weights can be seen as unimportant and masked out when showing rules to an expert (→ rule length reduction). The rules’ consequents are represented by certainty vectors and are recursively updated by an indicator-based recursive weighted least squares (I-RWLS) approach (one RWLS estimator per class) where the weights are given through the neuron activation levels in order to gain stable local learning. The model proposed in this paper was successfully compared to related hybrid and evolving approaches in the literature for classifying binary and multi-class patterns. The results obtained by the proposed model show an outperformance of the related works in terms of higher accuracy trend lines over time, while offering a high degree of interpretability through coherent neuro-fuzzy rules to solve the classification problems.}
}
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

import numpy as np


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

class FuzzyUtils:
    
    """
    Static utility class containing mathematical operations for 
    fuzzy membership, distance calculations, and neuron aggregations.
    """
    
    @staticmethod
    def chebyshev_distance(x: np.ndarray, y: np.ndarray) -> float:
        """Chebyshev (L-infinity) distance between two vectors."""
        return float(np.max(np.abs(x - y)))
    
    @staticmethod
    def gaussian_membership(x: np.ndarray, center: np.ndarray, sigma: float) -> np.ndarray:
        """
        Per-feature Gaussian membership.
    
        a_j = exp( - (x_j - c_j)^2 / (2 * sigma^2) )
    
        We use a single scalar sigma per rule (shared by all dimensions) as in
        many cloud-based evolving models.
        """
        sigma_eff = max(sigma, 1e-6)
        diff2 = (x - center) ** 2
        return np.exp(-diff2 / (2.0 * sigma_eff**2))
    
    @staticmethod
    def nuninorm(x: float, y: float, g1: float, g2: float, z: float) -> float:
        """
        2-uninorm (U2)
    
        We follow the structure:
    
            if (x <= z && y < z):
                u2 = z * U( x/z, y/z, g1/z )
            elif (x > z && y > z):
                u2 = z + (1-z) * U( (x-z)/(1-z), (y-z)/(1-z), (g2-z)/(1-z) )
            else:
                if z > 0.5: u2 = min(x,y)
                else:       u2 = max(x,y)
    
        where U is a base uninorm, here instantiated by a product t-norm
        (could be changed if needed).
        """
    
        # basic T-norm (product) for the internal composition
        def base_u(a: float, b: float, g: float) -> float:
            # simple symmetric uninorm built from product t-norm:
            # U(a,b) = a*b + (1-a)*(1-b) * something... but to keep it simple
            # and monotone in both arguments, we use product t-norm behavior
            # and ignore g in this simplified version:
            return a * b
    
        # avoid degenerate z
        if z <= 0.0:
            z = 1e-3
        if z >= 1.0:
            z = 1.0 - 1e-3
    
        if x <= z and y < z:
            # lower region
            return z * base_u(x / z, y / z, g1 / z)
        elif x > z and y > z:
            # upper region
            return z + (1.0 - z) * base_u(
                (x - z) / (1.0 - z),
                (y - z) / (1.0 - z),
                (g2 - z) / (1.0 - z),
            )
        else:
            # mixed region
            if z > 0.5:
                return min(x, y)
            else:
                return max(x, y)
    
    @staticmethod
    def orneuron(fuzzy_output, weights):
        # Implements OR logic here
        return (
            np.sum(np.array(fuzzy_output) * weights) / np.sum(weights)
            if np.sum(weights) > 0
            else 0
        )
    
    @staticmethod
    def uninullneuron(
        a: np.ndarray,
        w: np.ndarray,
        g1: float,
        g2: float,
        z: float,
    ) -> float:
        """
        UniNullNeuron
    
            h(i) = w(i)*a(i) + (1-w(i))*z
            y = z
            for i:
                y = nuninorm(y, h(i), g1, g2, z)
    
        Inputs:
          a : array of per-feature membership degrees (0..1)
          w : array of weights (0..1), same size as a
          g1, g2, z : uninorm parameters
    
        Output:
          scalar neuron output y in [0,1]
        """
        a = np.asarray(a, dtype=float)
        w = np.asarray(w, dtype=float)
        h = w * a + (1.0 - w) * z
    
        y = z
        for hi in h:
            y = FuzzyUtils.nuninorm(float(y), float(hi), float(g1), float(g2), float(z))
        return float(y)
    
    @staticmethod
    def rule_similarity(
        center_i: np.ndarray, sigma_i: float, center_j: np.ndarray, sigma_j: float
    ) -> float:
        """
        Simple similarity between two Gaussian rules, inspired by Edwin's cluster
        similarity: high if centers are close relative to their spreads.
    
        We use:
            sim = exp( - ||c_i - c_j||^2 / (sigma_i^2 + sigma_j^2 + eps) )
    
        in [0,1], where 1 means identical centers.
        """
        diff2 = float(np.sum((center_i - center_j) ** 2))
        denom = sigma_i**2 + sigma_j**2 + 1e-6
        return math.exp(-diff2 / denom)


# ---------------------------------------------------------------------------
# Data structure for one rule
# ---------------------------------------------------------------------------


@dataclass
class Uni0Rule:
    center: np.ndarray  # shape (d,)
    sigma: float
    support: int
    w: np.ndarray  # shape (d,) - weights for neuron
    g1: float
    g2: float
    z: float
    class_counts: np.ndarray  # shape (n_classes,)

    def update_label_stats(self, y: int) -> None:
        self.class_counts[y] += 1

    @property
    def dominant_class(self) -> int:
        return int(np.argmax(self.class_counts))


# ---------------------------------------------------------------------------
# Main model
# ---------------------------------------------------------------------------


class ENFS_Uni0:
    """
    Evolving Neuro-Fuzzy System with UniNull Uninorm Neurons (classification).

    - ADPA-like evolving clustering in the input space:
        * Each prototype -> one fuzzy rule.
    - Antecedents with Gaussian membership + UniNull neuron.
    - Consequent layer trained with RLS (global linear layer over rule outputs).
    """

    def __init__(
        self,
        n_features: int,
        n_classes: int,
        lambda_ff: float = 0.99,
        q0: float = 1.0,
        sim_threshold: float = 0.95,
        max_rules: Optional[int] = 10,
        random_state: Optional[int] = None,
        **kwargs,
    ):
        """
        Parameters
        ----------
        n_features : int
            Number of input features.
        n_classes : int
            Number of classes.
        lambda_ff : float, default=0.99
            Forgetting factor for RLS (close to 1).
        q0 : float, default=1.0
            Initial value for the covariance matrix P = q0 * I.
        sim_threshold : float, default=0.95
            Similarity threshold for pruning very similar rules.
        max_rules : int or None, default=None
            Maximum number of rules; if exceeded, least-supported rule is pruned.
        random_state : int or None
            Seed for reproducible random initialization.
        kwargs : dict
            Ignored extra keyword arguments (for backward compatibility).
        """
        self.n_features = int(n_features)
        self.n_classes = int(n_classes)

        self.lambda_ff = float(lambda_ff)
        self.q0 = float(q0)
        self.sim_threshold = float(sim_threshold)
        self.max_rules = max_rules

        self.rng = np.random.default_rng(random_state)

        # ADPA global statistics
        self.global_mean: Optional[np.ndarray] = None  # shape (d,)
        self.global_X: Optional[float] = None  # E[||x||^2]
        self.K: int = 0  # number of samples seen

        # Set of rules (data clouds)
        self.rules: List[Uni0Rule] = []

        # RLS parameters for consequent layer:
        #   W: shape (M, C) where M = (#rules + 1) for bias
        #   P: shape (M, M)
        self.W: Optional[np.ndarray] = None
        self.P: Optional[np.ndarray] = None

        # History
        self.history_n_rules: List[int] = []

    # ------------------------------------------------------------------
    # Public API (for streaming experiments)
    # ------------------------------------------------------------------

    @property
    def n_rules_(self) -> int:
        """Number of rules currently in the system."""
        return len(self.rules)

    def predict_one(self, x: np.ndarray) -> int:
        x = np.asarray(x, dtype=float).ravel()
        if self.n_rules_ == 0 or self.W is None:
            return 0
        scores = self._forward_scores(x)
        return int(np.argmax(scores))

    def learn_one(self, x: np.ndarray, y: int) -> None:
        x = np.asarray(x, dtype=float).ravel()
        self._update_one(x, int(y))

    # Batch versions (not needed for stream experiments, but convenient)
    def predict(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        y_hat = [self.predict_one(x) for x in X]
        return np.array(y_hat, dtype=int)

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=int)
        for xi, yi in zip(X, y):
            self.learn_one(xi, int(yi))

    # ------------------------------------------------------------------
    # Core internal methods
    # ------------------------------------------------------------------

    def _update_one(self, x: np.ndarray, y: int) -> None:
        """
        Single-sample update:
        - ADPA-style update of clouds/rules (create or adapt rule)
        - update label stats
        - compute rule outputs via UniNullNeuron
        - update RLS parameters W, P
        - apply pruning / rule limit
        """
        # Update ADPA and possibly create/modify rules
        rule_index = self._adpa_update(x, y)

        # Update label stats of the winning rule
        if rule_index is not None and 0 <= rule_index < self.n_rules_:
            self.rules[rule_index].update_label_stats(y)

        # If we have at least one rule, update RLS
        if self.n_rules_ > 0:
            z_vec = self._compute_rule_outputs(x)  # shape (R,)
            self._rls_update(z_vec, y)

        # Record history of rule count
        self.history_n_rules.append(self.n_rules_)

    # ------------------------------------------------------------------
    # ADPA-like evolving clustering
    # ------------------------------------------------------------------

    def _adpa_update(self, x: np.ndarray, y: int) -> Optional[int]:
        """
        EvolvingVersion-like update (ADPA-style) for ONE new sample x.

        Returns:
            index of the winning / updated rule (or newly created one).
        """
        x = np.asarray(x, dtype=float)
        # d = self.n_features

        # First sample: initialize global stats and first rule
        if self.K == 0:
            self.global_mean = x.copy()
            self.global_X = float(np.sum(x**2))
            self.K = 1

            self._create_rule(center=x, sigma=1.0, y=y)
            return 0

        # Update global stats
        t = self.K + 1
        self.global_mean = (self.global_mean * (t - 1) + x) / t
        self.global_X = (self.global_X * (t - 1) + float(np.sum(x**2))) / t
        self.K = t

        # Compute VC and SIGMA (global radius)
        mean_norm2 = float(np.sum(self.global_mean**2))
        VC = math.sqrt(max(2.0 * (self.global_X - mean_norm2), 1e-12))
        SIGMA = VC / 2.0

        if self.n_rules_ == 0:
            self._create_rule(center=x, sigma=SIGMA, y=y)
            return 0

        # Distances of centers and x to global mean in Chebyshev metric
        centers = np.stack([r.center for r in self.rules], axis=0)  # (R,d)
        dist_centers = np.max(np.abs(centers - self.global_mean), axis=1)
        dist_x = float(np.max(np.abs(x - self.global_mean)))

        # Condition for creating a NEW rule (data cloud)
        if float(np.min(dist_centers)) > dist_x or float(np.max(dist_centers)) < dist_x:
            rule_idx = self.n_rules_
            self._create_rule(center=x, sigma=SIGMA, y=y)
            # After creating: prune by similarity / max_rules
            self._maybe_prune(rule_idx)
            return rule_idx

        # Otherwise, try to adapt nearest center
        dist2 = np.max(np.abs(centers - x), axis=1)
        pos = int(np.argmin(dist2))
        V = float(dist2[pos])

        if V < SIGMA:
            # Update that center
            r = self.rules[pos]
            new_support = r.support + 1
            r.center = (r.center * r.support + x) / new_support
            r.support = new_support
            # Update sigma as a moving value (simplified)
            r.sigma = 0.8 * r.sigma + 0.2 * SIGMA if r.sigma > 0 else SIGMA
            return pos
        else:
            # Create new rule
            rule_idx = self.n_rules_
            self._create_rule(center=x, sigma=SIGMA, y=y)
            self._maybe_prune(rule_idx)
            return rule_idx

    def _create_rule(self, center: np.ndarray, sigma: float, y: int) -> None:
        
        r"""
        Create a new rule with:

        - given center, sigma
        - support = 1
        - random weights w \in [0,1]
        - random uninorm parameters g1, g2, z with 0 <= g1 < z < g2 <= 1
        - class_counts initialized with 1 for class y
        - expand RLS (W,P) dimensions accordingly
        """
        center = np.asarray(center, dtype=float).ravel()

        # Random uninorm parameters (rule-wise)
        g1 = float(self.rng.uniform(0.0, 0.5))
        g2 = float(self.rng.uniform(0.5, 1.0))
        if g2 <= g1:
            g2 = min(g1 + 0.1, 0.99)
        z = float(self.rng.uniform(g1, g2))

        # Random weights for neuron (feature relevance), in [0,1]
        w = self.rng.uniform(0.0, 1.0, size=self.n_features)

        class_counts = np.zeros(self.n_classes, dtype=float)
        class_counts[y] += 1.0

        rule = Uni0Rule(
            center=center,
            sigma=float(max(sigma, 1e-3)),
            support=1,
            w=w,
            g1=g1,
            g2=g2,
            z=z,
            class_counts=class_counts,
        )
        self.rules.append(rule)

        # Expand RLS dimensions: new design vector length = (#rules + 1)
        self._expand_rls_matrices()

    # ------------------------------------------------------------------
    # RLS for consequent layer
    # ------------------------------------------------------------------

    def _expand_rls_matrices(self) -> None:
        """
        Ensure that W and P have the right dimension M = (#rules + 1),
        where the first element corresponds to the bias term.

        When a new rule is added:
            - W is extended with an additional row of zeros.
            - P is extended with a new row/column and initialized with q0 on
              the new diagonal element.
        """
        M = self.n_rules_ + 1  # bias + R rules

        if self.W is None or self.P is None:
            # Initialize from scratch
            self.W = np.zeros((M, self.n_classes), dtype=float)
            self.P = self.q0 * np.eye(M, dtype=float)
            return

        old_M = self.W.shape[0]
        if M == old_M:
            return

        # Expand W
        W_new = np.zeros((M, self.n_classes), dtype=float)
        W_new[:old_M, :] = self.W
        self.W = W_new

        # Expand P
        P_new = np.zeros((M, M), dtype=float)
        P_new[:old_M, :old_M] = self.P
        P_new[-1, -1] = self.q0
        self.P = P_new

    def _rls_update(self, z_vec: np.ndarray, y: int) -> None:
        """
        Perform one RLS update with:
        - design vector phi = [1, z_vec]   (shape (M,))
        - one-hot target for class y
        """
        if self.W is None or self.P is None:
            self._expand_rls_matrices()

        # Build design vector
        z_vec = np.asarray(z_vec, dtype=float).ravel()
        phi = np.empty(self.n_rules_ + 1, dtype=float)
        phi[0] = 1.0
        phi[1:] = z_vec

        # One-hot target
        y_target = np.zeros(self.n_classes, dtype=float)
        y_target[y] = 1.0

        # Current prediction (scores) before update
        scores = phi @ self.W  # shape (C,)
        error = y_target - scores  # shape (C,)

        # Standard RLS update
        P = self.P
        lambda_ff = self.lambda_ff

        # K = P * phi / (lambda + phi^T * P * phi)
        P_phi = P @ phi  # shape (M,)
        denom = lambda_ff + float(phi @ P_phi)
        if denom <= 1e-12:
            # numerical safeguard
            denom = 1e-12
        K = P_phi / denom  # shape (M,)

        # W_new = W + K * error^T
        self.W = self.W + np.outer(K, error)

        # P_new = (P - K * phi^T * P) / lambda
        self.P = (P - np.outer(K, phi) @ P) / lambda_ff

        # NaN protection
        if not np.all(np.isfinite(self.W)):
            self.W[:] = 0.0
        if not np.all(np.isfinite(self.P)):
            self.P = self.q0 * np.eye(self.P.shape[0], dtype=float)

    # ------------------------------------------------------------------
    # Forward computation of rule outputs
    # ------------------------------------------------------------------

    def _compute_rule_outputs(self, x: np.ndarray) -> np.ndarray:
        """
        Compute y_r(x) for all rules r using:

        - per-feature Gaussian membership
        - UniNullNeuron with rule-specific {w, g1, g2, z}
        """
        x = np.asarray(x, dtype=float).ravel()
        if self.n_rules_ == 0:
            return np.zeros(0, dtype=float)

        outputs = np.zeros(self.n_rules_, dtype=float)
        for idx, r in enumerate(self.rules):
            a = FuzzyUtils.gaussian_membership(x, r.center, r.sigma)
            # y_r = uninullneuron(a, r.w, r.g1, r.g2, r.z)
            y_r = FuzzyUtils.orneuron(a, r.w)
            outputs[idx] = y_r

        # Optional: normalize to avoid extremely large/small scales
        s = float(np.sum(outputs))
        if s > 0.0:
            outputs /= s
        return outputs

    def _forward_scores(self, x: np.ndarray) -> np.ndarray:
        """
        Compute class scores s(x) = phi(x)^T * W without updating anything.
        """
        z_vec = self._compute_rule_outputs(x)
        if self.W is None:
            # no training yet, return zeros
            return np.zeros(self.n_classes, dtype=float)
        phi = np.empty(self.n_rules_ + 1, dtype=float)
        phi[0] = 1.0
        phi[1:] = z_vec
        return phi @ self.W  # shape (C,)

    # ------------------------------------------------------------------
    # Pruning / Rule limit
    # ------------------------------------------------------------------

    def _maybe_prune(self, new_rule_idx: int) -> None:
        """
        After creating a new rule:
        - prune very similar rules (similarity-based),
        - enforce max_rules if needed.
        """
        if self.n_rules_ <= 1:
            return

        # 1) Similarity-based pruning: if new rule is too similar to an
        #    existing one, we drop the newer one (or we could drop the older).
        r_new = self.rules[new_rule_idx]
        for j in range(self.n_rules_ - 1):
            r_old = self.rules[j]
            sim = FuzzyUtils.rule_similarity(r_new.center, r_new.sigma, r_old.center, r_old.sigma)
            if sim >= self.sim_threshold:
                # very similar: remove the new rule
                self._remove_rule(new_rule_idx)
                return

        # 2) Enforce maximum number of rules
        if self.max_rules is not None and self.n_rules_ > self.max_rules:
            # remove rule with smallest support (least used)
            supports = np.array([r.support for r in self.rules], dtype=int)
            to_remove = int(np.argmin(supports))
            self._remove_rule(to_remove)

    def _remove_rule(self, idx: int) -> None:
        """
        Remove rule at index idx and adjust W and P accordingly.
        """
        if idx < 0 or idx >= self.n_rules_:
            return

        # Remove rule from list
        del self.rules[idx]

        if self.W is None or self.P is None:
            return

        # We must remove one dimension from RLS state:
        # dimension 0 = bias, dimensions [1..R] = rules
        dim_to_remove = idx + 1  # +1 for bias at index 0

        # Remove row from W
        self.W = np.delete(self.W, dim_to_remove, axis=0)

        # Remove row/column from P
        self.P = np.delete(self.P, dim_to_remove, axis=0)
        self.P = np.delete(self.P, dim_to_remove, axis=1)

        # If no rules left, reset RLS
        if self.n_rules_ == 0:
            self.W = None
            self.P = None
            self.K = 0
            self.global_mean = None
            self.global_X = None
