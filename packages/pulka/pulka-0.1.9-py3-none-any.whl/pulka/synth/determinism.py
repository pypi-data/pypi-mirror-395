"""Deterministic helpers for synthetic dataset generation."""

from __future__ import annotations

import base64
import hashlib
import math
import random
from collections.abc import Iterable
from dataclasses import dataclass

SPEC_ID_PREFIX = "pulka-v1-"
_DIGEST_SIZE = 16


def normalized_spec_hash(normalized_spec: str) -> bytes:
    """Return the canonical 128-bit hash for ``normalized_spec``."""

    digest = hashlib.blake2b(normalized_spec.encode("utf-8"), digest_size=_DIGEST_SIZE)
    return digest.digest()


def spec_id(normalized_spec: str) -> str:
    """Return the stable identifier for ``normalized_spec``."""

    digest = normalized_spec_hash(normalized_spec)
    token = base64.b32encode(digest).decode("ascii").lower().rstrip("=")
    return f"{SPEC_ID_PREFIX}{token[:20]}"


def derive_seed(root: bytes, *parts: str | int | bytes) -> bytes:
    """Derive a deterministic seed from ``root`` and supplemental ``parts``."""

    hasher = hashlib.blake2b(root, digest_size=_DIGEST_SIZE)
    for part in parts:
        if isinstance(part, bytes):
            data = part
        elif isinstance(part, int):
            data = part.to_bytes(16, byteorder="big", signed=False)
        else:
            data = part.encode("utf-8")
        hasher.update(len(data).to_bytes(2, "big"))
        hasher.update(data)
    return hasher.digest()


def seed_bytes_to_int(seed: bytes) -> int:
    """Convert a seed byte-string into an integer suitable for ``random.Random``."""

    return int.from_bytes(seed, byteorder="big", signed=False)


@dataclass
class DeterministicRNG:
    """Pure-Python PRNG wrapper based on :class:`random.Random`."""

    seed: bytes

    def __post_init__(self) -> None:
        self._rng = random.Random(seed_bytes_to_int(self.seed))
        self._box_muller_extra: float | None = None

    def random(self) -> float:
        """Return ``U(0, 1)``."""

        return self._rng.random()

    def uniform(self, low: float, high: float) -> float:
        """Return ``U(low, high)``."""

        return low + (high - low) * self.random()

    def normal(self, mean: float, stddev: float) -> float:
        """Return ``N(mean, stddev)`` via Box-Muller transform."""

        if self._box_muller_extra is not None:
            value = self._box_muller_extra
            self._box_muller_extra = None
        else:
            u1 = self.random()
            u2 = self.random()
            # Guard against log(0)
            u1 = max(u1, 1e-12)
            radius = math.sqrt(-2.0 * math.log(u1))
            theta = 2.0 * math.pi * u2
            value = radius * math.cos(theta)
            self._box_muller_extra = radius * math.sin(theta)
        return mean + stddev * value

    def exponential(self, lam: float) -> float:
        """Return exponential(lambda)."""

        if lam <= 0:
            raise ValueError("lambda must be positive for exponential distribution")
        u = max(self.random(), 1e-12)
        return -math.log(u) / lam

    def gamma(self, shape: float, scale: float) -> float:
        """Return Gamma(shape, scale) using Marsaglia-Tsang."""

        if shape <= 0 or scale <= 0:
            raise ValueError("shape and scale must be positive for gamma distribution")
        if shape < 1:
            # Use Johnk's generator
            while True:
                u = self.random()
                b = (math.e + shape) / math.e
                p = b * self.random()
                if p <= 1:
                    x = p ** (1 / shape)
                    if self.random() <= math.exp(-x):
                        return scale * x
                else:
                    x = -math.log((b - p) / shape)
                    if self.random() <= x ** (shape - 1):
                        return scale * x
        d = shape - 1 / 3
        c = 1 / math.sqrt(9 * d)
        while True:
            x = self.normal(0.0, 1.0)
            v = (1 + c * x) ** 3
            if v <= 0:
                continue
            u = self.random()
            if u < 1 - 0.0331 * (x**4) or math.log(u) < 0.5 * x * x + d * (1 - v + math.log(v)):
                return scale * d * v

    def beta(self, a: float, b: float) -> float:
        """Return Beta(a, b) via Gamma sampling."""

        if a <= 0 or b <= 0:
            raise ValueError("shape parameters must be positive for beta distribution")
        x = self.gamma(a, 1.0)
        y = self.gamma(b, 1.0)
        return x / (x + y)

    def randbytes(self, length: int) -> bytes:
        """Return ``length`` random bytes."""

        if length < 0:
            raise ValueError("length must be non-negative")
        return bytes(self._rng.getrandbits(8) for _ in range(length))

    def randint(self, a: int, b: int) -> int:
        """Return integer in ``[a, b]`` inclusive."""

        return self._rng.randint(a, b)

    def pareto(self, alpha: float) -> float:
        """Return Pareto(alpha)."""

        if alpha <= 0:
            raise ValueError("alpha must be positive for Pareto distribution")
        u = 1.0 - self.random()
        u = max(u, 1e-12)
        return u ** (-1.0 / alpha)

    def zipf(self, alpha: float, max_k: int = 1_000_000) -> int:
        """Return Zipf(alpha) within ``[1, max_k]`` using rejection sampling."""

        if alpha <= 1:
            raise ValueError("alpha must be > 1 for Zipf distribution")
        while True:
            u = self.random()
            v = self.random()
            x = math.floor(u ** (-1.0 / (alpha - 1)))
            if x < 1:
                continue
            t = (1 + 1 / x) ** (alpha - 1)
            if v * x * (t - 1) / (alpha - 1) <= 1:
                return min(x, max_k)

    def poisson(self, lam: float) -> int:
        """Return Poisson(lambda) using Knuth's algorithm for small lambda."""

        if lam <= 0:
            raise ValueError("lambda must be positive for poisson distribution")
        if lam < 20:
            limit = math.exp(-lam)
            k = 0
            p = 1.0
            while p > limit:
                k += 1
                p *= self.random()
            return k - 1
        # Rejection method (Atkinson's algorithm)
        beta = math.pi / math.sqrt(3.0 * lam)
        alpha = beta * lam
        k = 0
        while True:
            u = self.random()
            x = (alpha - math.log((1.0 - u) / u)) / beta
            n = math.floor(x + 0.5)
            if n < 0:
                continue
            v = self.random()
            y = alpha - beta * x
            lhs = y + math.log(v / ((1.0 + math.exp(y)) ** 2))
            rhs = lam + n * math.log(lam) - math.lgamma(n + 1)
            if lhs <= rhs:
                k = n
                break
        return k

    def categorical(self, weights: Iterable[float]) -> int:
        """Sample an index from the provided ``weights`` sequence."""

        total = 0.0
        cumulative: list[float] = []
        for w in weights:
            if w < 0:
                raise ValueError("weights must be non-negative")
            total += w
            cumulative.append(total)
        if not cumulative:
            raise ValueError("weights must not be empty")
        if total <= 0:
            raise ValueError("total weight must be positive")
        target = self.random() * total
        for idx, cutoff in enumerate(cumulative):
            if target <= cutoff:
                return idx
        return len(cumulative) - 1


__all__ = [
    "DeterministicRNG",
    "SPEC_ID_PREFIX",
    "derive_seed",
    "normalized_spec_hash",
    "seed_bytes_to_int",
    "spec_id",
]
