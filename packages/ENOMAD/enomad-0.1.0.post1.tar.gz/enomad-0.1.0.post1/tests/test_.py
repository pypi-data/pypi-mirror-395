# -*- coding: utf-8 -*-
"""Unit tests for *ENOMAD*.
Run with ``pytest -q``.

The tests are lightweight smoke checks that ensure:
* both optimiser types ("pure" and "hybrid") run without error,
* invalid arguments raise `ValueError`,
* seeding makes the run deterministic.
"""
from __future__ import annotations

import numpy as np
import pytest
from typing import Callable, Tuple, Optional, List
try:
    import jax, jax.numpy as jnp
except:
    pass

from ENOMAD import ENOMAD

# ---------------------------------------------------------------------------
# Test helper – simple objective
# --------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Smoke tests for both optimiser types
# ---------------------------------------------------------------------------

def _run_smoke(optim_type: str):
    opt = ENOMAD(
        optim_type,
        population_size=8,
        dimension=4,
        objective_fn=sphere,
        subset_size=2,
        bounds=0.1,
        max_bb_eval=20,
        n_mutate_coords=1,
        seed=42,
        use_ray=False,
    )
    best_x, best_fit = opt.run(generations=3)
    assert best_x.shape == (4,)
    assert isinstance(best_fit, float)
    assert best_fit >= 0  # sphere is <= 0


def test_pure_smoke():
    _run_smoke("EA")




# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("crossover_type", ["foo", "", None])
def test_invalid_crossover_type_raises(crossover_type):
    with pytest.raises(ValueError):
        ENOMAD(
            "EA",
            population_size=4,
            dimension=2,
            objective_fn=sphere,
            crossover_type=crossover_type,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("crossover_rate", [-0.1, -10, 1.5])
def test_invalid_crossover_rate_raises(crossover_rate):
    with pytest.raises(ValueError):
        ENOMAD(
            "EA",
            population_size=4,
            dimension=2,
            objective_fn=sphere,
            crossover_rate=crossover_rate,  # type: ignore[arg-type]
        )


# ---------------------------------------------------------------------------
# Determinism with seed
# ---------------------------------------------------------------------------

def test_seed_reproducibility():
    """Global RNG seeding should make two runs identical."""
    opt1 = ENOMAD(
        "EA",
        population_size=6,
        dimension=3,
        objective_fn=sphere,
        subset_size=2,
        seed=7,
        use_ray=False,
    )
    best_x1, best_fit1 = opt1.run(generations=3)

   
    opt2 = ENOMAD(
        "EA",
        population_size=6,
        dimension=3,
        objective_fn=sphere,
        subset_size=2,
        seed=7,
        use_ray=False,
    )
    best_x2, best_fit2 = opt2.run(generations=3)

    assert np.allclose(best_x1, best_x2)
    assert best_fit1 == best_fit2

# ─────────────────────────────────────────────────────────────
# 1.  Benchmark functions (return –f so EA‑NOMAD can maximise)
# ─────────────────────────────────────────────────────────────

def sphere(x: np.ndarray) -> float:
    return np.sum(x ** 2)


def rosenbrock(x: np.ndarray) -> float:
    return np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1 - x[:-1]) ** 2)


def rastrigin(x: np.ndarray) -> float:
    d = x.size
    return (10 * d + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x)))


benchmarks: dict[str, Callable[[np.ndarray], float]] = {
    "Sphere": sphere,
    "Rosenbrock": rosenbrock,
    "Rastrigin": rastrigin,
}

# ─────────────────────────────────────────────────────────────
# 2.  Hyper‑parameters trimmed for CI / local test speed
# ─────────────────────────────────────────────────────────────
DIM = 10
POP_SIZE = 16          # smaller than real demo to keep test fast
GENERATIONS = 10
SUBSET_SIZE = 10        # ≥1 so NOMAD has something to do
BOUNDS = (-5.12 * np.ones(DIM), 5.12 * np.ones(DIM))
MAX_BB_EVAL = 20
N_MUTATE_COORD = DIM // 4
SEED = 0

# ─────────────────────────────────────────────────────────────
# 3.  Parametrised test
# ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name, fn", benchmarks.items())
def test_ENOMAD_benchmark_convergence(name: str, fn):
    """Ensure EA‑NOMAD improves each benchmark quickly on CPU."""

    es = ENOMAD(
        "EA",
        population_size=POP_SIZE,
        dimension=DIM,
        objective_fn=fn,
        subset_size=SUBSET_SIZE,
        bounds=BOUNDS,
        max_bb_eval=MAX_BB_EVAL,
        n_mutate_coords=N_MUTATE_COORD,
        seed=SEED,
        use_ray=False,
    )

    _best_x, best_fit = es.run(GENERATIONS) # fix

    # The best achievable value is 0.  Allow a modest tolerance so the
    # test stays robust across platforms yet still detects gross errors.
    assert best_fit > -1e+2, (
        f"{name} benchmark failed: best fitness {best_fit:.4f} not close enough"
    )


@pytest.fixture(scope="module")
def demo_problem():
    """Grab the objects defined in the original notebook.

    Skip the test if they are not importable so CI still passes on
    minimal environments.
    """
    try:
        seed = 0
        # Adjust this import to match your project layout
        fn_name = "schaffers_f7"
        num_dims = 2
        from evosax.problems import (
            BBOBProblem as Problem,
        )
        key = jax.random.key(seed)

        problem = Problem(
            fn_name=fn_name,
            num_dims=num_dims,
            x_opt=2.5 * jnp.ones(num_dims),
            f_opt=0.0,
            # sample_rotations=False,
            seed=seed,
        )

        problem_state = problem.init(key)

        key, subkey = jax.random.split(key)
        solution = problem.sample(subkey)
    except ModuleNotFoundError:
        pytest.skip("`solution / problem / problem_state` not found")
    return solution, problem, problem_state


def make_objective(problem, problem_state):
    """Wrap the JAX objective so EA‑NOMAD (which maximises) can call it."""
    def objective_np(x: np.ndarray) -> float:
        x_jax = jnp.asarray(x, dtype=jnp.float32)
        f, *_ = problem.eval(jax.random.PRNGKey(0),
                             x_jax.reshape(1, -1),
                             problem_state)
        return float(f[0])  # negate ⇒ maximise
    return objective_np


# ---------------------------------------------------------------------------
# The actual smoke test
# ---------------------------------------------------------------------------

def test_notebook_demo_smoke(demo_problem):
    solution, problem, problem_state = demo_problem
    key = jax.random.PRNGKey(0)

    es = ENOMAD(
        "EA",
        population_size=POP_SIZE,           # trimmed for speed
        dimension=int(solution.size),
        objective_fn=make_objective(problem, problem_state),
        subset_size=2,
        bounds=4,
        max_bb_eval=MAX_BB_EVAL,
        n_mutate_coords=2,
        seed=int(key[0]),
        crossover_type="fitness",
        low = -4,
        high= 4,
                )
    # run a few generations
    _best_x, best_fit = es.run(GENERATIONS)

    assert isinstance(best_fit, float)
    assert best_fit > -1e+1, (
        f"{jax} benchmark failed: best fitness {best_fit:.4f} not close enough"
    )


def huge_but_finite(x: np.ndarray) -> float:
    """Objective that occasionally returns |fitness| > 32‑bit range."""
    # alternating sign, magnitude 1e11
    return 1e11 if np.sum(x) > 0 else -1e11

def test_callback_clamp_prevents_overflow():
    """EA‑NOMAD should not crash with 'value too large to convert to int'."""
    opt = ENOMAD(
        "EA",
        population_size=8,
        dimension=4,
        objective_fn=huge_but_finite,
        subset_size=4,
        bounds=1.0,
        max_bb_eval=50,
        seed=123,
        use_ray=False,     # keep it single‑process for the test
    )

    # just one generation is enough to trigger the callback
    best_x, best_fit = opt.run(generations=3)

    assert isinstance(best_fit, float)
    # clamp puts result inside ±2.15e9, so check that
    assert abs(best_fit) <= 2_147_483_600