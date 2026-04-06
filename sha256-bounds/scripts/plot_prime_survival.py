#!/usr/bin/env python3
"""
Deterministic plotting probe for source-prime survival in SHA-256 constants.

The script tests a narrower claim than plain phi-lattice alignment:
whether the real source pairing between the first 64 primes and the
SHA-256 round constants preserves local structure in theta' space better
than deterministic controls.
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PHI = (1.0 + math.sqrt(5.0)) / 2.0
TWO32 = 1 << 32
K_VALUES = (0.2, 0.45, 0.8)
PERSISTENCE_KS = (0.45, 0.8)
MOTIF_DEPTHS = (1, 2, 3)
K_SWEEP = (0.2, 0.3, 0.45, 0.6, 0.8)
SHIFT_CONTROL = 17

SHA256_CONSTANTS = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
    0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
    0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
    0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
]


def frac(value: float) -> float:
    return value - math.floor(value)


def theta_prime(value: int, k_value: float) -> float:
    return frac(PHI * (frac(value / PHI) ** k_value))


def circular_distance(a_value: float, b_value: float) -> float:
    delta = abs(a_value - b_value) % 1.0
    return delta if delta <= 0.5 else 1.0 - delta


def rotate(values: list[int], offset: int) -> list[int]:
    offset %= len(values)
    return values[offset:] + values[:offset]


def first_primes(count: int) -> list[int]:
    primes: list[int] = []
    candidate = 2
    while len(primes) < count:
        is_prime = True
        limit = int(candidate ** 0.5)
        for prime in primes:
            if prime > limit:
                break
            if candidate % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1
    return primes


def first_nonprimes(count: int) -> list[int]:
    composites: list[int] = []
    candidate = 4
    while len(composites) < count:
        for divisor in range(2, int(candidate ** 0.5) + 1):
            if candidate % divisor == 0:
                composites.append(candidate)
                break
        candidate += 1
    return composites


def nth_root_constant(value: int, degree: int) -> int:
    getcontext().prec = 80
    decimal_value = Decimal(value)
    guess = decimal_value ** (Decimal(1) / Decimal(degree))
    for _ in range(14):
        guess = ((degree - 1) * guess + decimal_value / (guess ** (degree - 1))) / degree
    fractional = guess - int(guess)
    return int(fractional * TWO32)


def cube_root_constant(value: int) -> int:
    return nth_root_constant(value, 3)


def first_semiprimes(count: int) -> list[int]:
    semiprimes: list[int] = []
    candidate = 4
    while len(semiprimes) < count:
        factor_count = 0
        residue = candidate
        divisor = 2
        while divisor * divisor <= residue and factor_count <= 2:
            while residue % divisor == 0:
                factor_count += 1
                residue //= divisor
                if factor_count > 2:
                    break
            divisor += 1
        if residue > 1:
            factor_count += 1
        if factor_count == 2:
            semiprimes.append(candidate)
        candidate += 1
    return semiprimes


def prime_slice(start: int, count: int) -> list[int]:
    primes = first_primes(start + count)
    return primes[start:start + count]


def rankdata(values: list[float]) -> list[int]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0] * len(values)
    for rank, index in enumerate(order):
        ranks[index] = rank
    return ranks


def spearman_rho(xs: list[float], ys: list[float]) -> float:
    rank_x = rankdata(xs)
    rank_y = rankdata(ys)
    n_values = len(xs)
    distance_sq = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n_values))
    return 1.0 - (6.0 * distance_sq) / (n_values * (n_values * n_values - 1))


def nearest_neighbor_signature(values: list[float]) -> list[int]:
    signature: list[int] = []
    for i_value, value in enumerate(values):
        best_index = -1
        best_distance = None
        for j_value, other in enumerate(values):
            if i_value == j_value:
                continue
            distance = circular_distance(value, other)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_index = j_value
        signature.append(best_index)
    return signature


def k_nearest_signatures(values: list[float], depth: int) -> list[tuple[int, ...]]:
    signatures: list[tuple[int, ...]] = []
    for i_value, value in enumerate(values):
        distances: list[tuple[float, int]] = []
        for j_value, other in enumerate(values):
            if i_value == j_value:
                continue
            distance = circular_distance(value, other)
            distances.append((distance, j_value))
        distances.sort()
        signatures.append(tuple(index for _, index in distances[:depth]))
    return signatures


def nearest_neighbor_overlap(xs: list[float], ys: list[float]) -> int:
    left = nearest_neighbor_signature(xs)
    right = nearest_neighbor_signature(ys)
    return sum(1 for left_index, right_index in zip(left, right) if left_index == right_index)


def compute_metrics(sources: list[int], targets: list[int], k_value: float) -> dict[str, object]:
    source_theta = [theta_prime(value, k_value) for value in sources]
    target_theta = [theta_prime(value, k_value) for value in targets]
    return {
        "source_theta": source_theta,
        "target_theta": target_theta,
        "rho": spearman_rho(source_theta, target_theta),
        "nn_overlap": nearest_neighbor_overlap(source_theta, target_theta),
    }


def build_shift_spectrum(sources: list[int], targets: list[int], k_value: float) -> dict[str, list[float]]:
    rhos: list[float] = []
    overlaps: list[float] = []
    for offset in range(len(targets)):
        metrics = compute_metrics(sources, rotate(targets, offset), k_value)
        rhos.append(float(metrics["rho"]))
        overlaps.append(float(metrics["nn_overlap"]))
    return {"rho": rhos, "nn_overlap": overlaps}


def motif_overlap_fraction(
    sources: list[int],
    targets: list[int],
    depths: tuple[int, ...],
    persistence_ks: tuple[float, ...],
) -> dict[int, float]:
    source_theta = {
        k_value: [theta_prime(value, k_value) for value in sources]
        for k_value in persistence_ks
    }
    target_theta = {
        k_value: [theta_prime(value, k_value) for value in targets]
        for k_value in persistence_ks
    }

    overlap_by_depth: dict[int, float] = {}
    for depth in depths:
        source_signatures = {
            k_value: k_nearest_signatures(values, depth)
            for k_value, values in source_theta.items()
        }
        target_signatures = {
            k_value: k_nearest_signatures(values, depth)
            for k_value, values in target_theta.items()
        }

        overlap_total = 0
        normalizer = len(sources) * len(persistence_ks) * depth
        for index in range(len(sources)):
            for k_value in persistence_ks:
                source_set = set(source_signatures[k_value][index])
                target_set = set(target_signatures[k_value][index])
                overlap_total += len(source_set & target_set)
        overlap_by_depth[depth] = overlap_total / normalizer
    return overlap_by_depth


def single_k_motif_stats(
    sources: list[int],
    targets: list[int],
    depth: int,
    k_value: float,
) -> dict[str, float]:
    real_score = motif_overlap_fraction(sources, targets, (depth,), (k_value,))[depth]
    shifted_scores = []
    for offset in range(1, len(targets)):
        shifted_targets = rotate(targets, offset)
        shifted = motif_overlap_fraction(sources, shifted_targets, (depth,), (k_value,))
        shifted_scores.append(shifted[depth])

    shift_mean = float(np.mean(shifted_scores))
    return {
        "real_overlap": real_score,
        "shift_mean": shift_mean,
        "amplification_ratio": real_score / shift_mean if shift_mean > 0.0 else float("nan"),
        "absolute_lift": real_score - shift_mean,
    }


def plot_shift_spectrum(output_dir: Path, sources: list[int], targets: list[int]) -> None:
    shifts = np.arange(len(targets))
    colors = {0.2: "#1b9e77", 0.45: "#d95f02", 0.8: "#7570b3"}
    figure, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, constrained_layout=True)

    for k_value in K_VALUES:
        spectrum = build_shift_spectrum(sources, targets, k_value)
        rho_values = np.array(spectrum["rho"])
        overlap_values = np.array(spectrum["nn_overlap"])

        axes[0].plot(shifts, rho_values, color=colors[k_value], linewidth=2, label=f"k = {k_value:.2f}")
        axes[0].scatter([0], [rho_values[0]], color=colors[k_value], s=60, zorder=3)
        axes[0].axhline(rho_values[1:].mean(), color=colors[k_value], linestyle=":", linewidth=1)

        axes[1].plot(shifts, overlap_values, color=colors[k_value], linewidth=2, label=f"k = {k_value:.2f}")
        axes[1].scatter([0], [overlap_values[0]], color=colors[k_value], s=60, zorder=3)
        axes[1].axhline(overlap_values[1:].mean(), color=colors[k_value], linestyle=":", linewidth=1)

    axes[0].set_title("Prime pairing vs all cyclic re-pairings")
    axes[0].set_ylabel("Spearman rho")
    axes[0].legend(loc="upper right")
    axes[0].grid(alpha=0.25)

    axes[1].set_ylabel("Nearest-neighbor overlap")
    axes[1].set_xlabel("Cyclic shift of SHA-256 constants")
    axes[1].grid(alpha=0.25)

    figure.suptitle("Shift 0 is the real prime-to-constant pairing; dotted lines are mean nonzero shifts")
    figure.savefig(output_dir / "prime_survival_shift_spectrum.png", dpi=180)
    plt.close(figure)


def plot_rank_transfer(output_dir: Path, prime_sources: list[int]) -> None:
    k_value = 0.8
    panel_specs = [
        ("Primes, real SHA pairing", prime_sources, SHA256_CONSTANTS),
        ("Primes, cyclic shift 17", prime_sources, rotate(SHA256_CONSTANTS, SHIFT_CONTROL)),
        ("Nonprimes, cube-root constants", first_nonprimes(64), [cube_root_constant(v) for v in first_nonprimes(64)]),
        ("Integers 2..65, cube-root constants", list(range(2, 66)), [cube_root_constant(v) for v in range(2, 66)]),
    ]

    figure, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True, sharey=True, constrained_layout=True)
    for axis, (title, sources, targets) in zip(axes.flat, panel_specs):
        metrics = compute_metrics(sources, targets, k_value)
        source_theta = metrics["source_theta"]
        target_theta = metrics["target_theta"]
        source_order = np.argsort(np.array(source_theta))
        target_ranks = np.array(rankdata(target_theta))
        x_values = np.arange(len(sources))
        y_values = target_ranks[source_order]

        axis.plot(x_values, x_values, color="#bbbbbb", linewidth=1.5, linestyle=":")
        axis.plot(x_values, y_values, color="#1f78b4", linewidth=1.5)
        axis.scatter(x_values, y_values, color="#1f78b4", s=16)
        axis.set_title(
            f"{title}\n"
            f"rho = {float(metrics['rho']):.3f}, nn = {int(metrics['nn_overlap'])}"
        )
        axis.grid(alpha=0.2)

    axes[1, 0].set_xlabel("Source rank in theta' space")
    axes[1, 1].set_xlabel("Source rank in theta' space")
    axes[0, 0].set_ylabel("Target rank in theta' space")
    axes[1, 0].set_ylabel("Target rank in theta' space")
    figure.suptitle("At k = 0.8, source-order survival shows up as a diagonal trend")
    figure.savefig(output_dir / "prime_survival_rank_transfer_k0_80.png", dpi=180)
    plt.close(figure)


def plot_summary_metrics(output_dir: Path) -> list[dict[str, float]]:
    datasets = [
        ("Primes", first_primes(64), SHA256_CONSTANTS),
        ("Nonprimes", first_nonprimes(64), [cube_root_constant(v) for v in first_nonprimes(64)]),
        ("Integers 2..65", list(range(2, 66)), [cube_root_constant(v) for v in range(2, 66)]),
    ]
    colors = {0.2: "#1b9e77", 0.45: "#d95f02", 0.8: "#7570b3"}
    bar_width = 0.22
    x_positions = np.arange(len(datasets))
    summary_rows: list[dict[str, float]] = []

    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
    for offset_index, k_value in enumerate(K_VALUES):
        rho_values = []
        nn_values = []
        for label, sources, targets in datasets:
            metrics = compute_metrics(sources, targets, k_value)
            rho_values.append(float(metrics["rho"]))
            nn_values.append(int(metrics["nn_overlap"]))
            summary_rows.append(
                {
                    "dataset": label,
                    "k": k_value,
                    "rho": float(metrics["rho"]),
                    "nn_overlap": int(metrics["nn_overlap"]),
                }
            )
        offsets = x_positions + (offset_index - 1) * bar_width
        axes[0].bar(offsets, rho_values, width=bar_width, color=colors[k_value], label=f"k = {k_value:.2f}")
        axes[1].bar(offsets, nn_values, width=bar_width, color=colors[k_value], label=f"k = {k_value:.2f}")

    for axis in axes:
        axis.set_xticks(x_positions)
        axis.set_xticklabels([label for label, _, _ in datasets])
        axis.grid(axis="y", alpha=0.2)

    axes[0].set_title("Order retention by source set")
    axes[0].set_ylabel("Spearman rho")
    axes[0].legend(loc="upper left")

    axes[1].set_title("Neighborhood retention by source set")
    axes[1].set_ylabel("Nearest-neighbor overlap")

    figure.suptitle("Prime-derived constants stand out most in the telephoto lens")
    figure.savefig(output_dir / "prime_survival_summary_metrics.png", dpi=180)
    plt.close(figure)
    return summary_rows


def plot_motif_amplification(output_dir: Path) -> list[dict[str, float]]:
    datasets = [
        ("Primes", first_primes(64), SHA256_CONSTANTS),
        ("Nonprimes", first_nonprimes(64), [cube_root_constant(v) for v in first_nonprimes(64)]),
        ("Integers 2..65", list(range(2, 66)), [cube_root_constant(v) for v in range(2, 66)]),
    ]
    colors = {
        "Primes": "#1f78b4",
        "Nonprimes": "#33a02c",
        "Integers 2..65": "#e31a1c",
    }
    x_positions = np.arange(len(MOTIF_DEPTHS))
    width = 0.24
    rows: list[dict[str, float]] = []

    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
    for dataset_index, (label, sources, targets) in enumerate(datasets):
        real_scores = motif_overlap_fraction(sources, targets, MOTIF_DEPTHS, PERSISTENCE_KS)
        shift_scores = {
            depth: []
            for depth in MOTIF_DEPTHS
        }
        for offset in range(1, len(targets)):
            shifted_targets = rotate(targets, offset)
            shifted = motif_overlap_fraction(sources, shifted_targets, MOTIF_DEPTHS, PERSISTENCE_KS)
            for depth in MOTIF_DEPTHS:
                shift_scores[depth].append(shifted[depth])

        lift_values = []
        ratio_values = []
        for depth in MOTIF_DEPTHS:
            shift_mean = float(np.mean(shift_scores[depth]))
            real_value = real_scores[depth]
            ratio_value = real_value / shift_mean if shift_mean > 0.0 else float("nan")
            lift_values.append(real_value - shift_mean)
            ratio_values.append(ratio_value)
            rows.append(
                {
                    "dataset": label,
                    "depth": depth,
                    "real_overlap": real_value,
                    "shift_mean": shift_mean,
                    "amplification_ratio": ratio_value,
                }
            )

        offsets = x_positions + (dataset_index - 1) * width
        axes[0].bar(offsets, ratio_values, width=width, color=colors[label], label=label)
        axes[1].bar(offsets, lift_values, width=width, color=colors[label], label=label)

    for axis in axes:
        axis.set_xticks(x_positions)
        axis.set_xticklabels([f"G{depth}" for depth in MOTIF_DEPTHS])
        axis.grid(axis="y", alpha=0.2)

    axes[0].axhline(1.0, color="#555555", linestyle=":", linewidth=1)
    axes[0].set_title("Amplification ratio")
    axes[0].set_ylabel("Real overlap / mean shifted overlap")
    axes[0].legend(loc="upper right")

    axes[1].axhline(0.0, color="#555555", linestyle=":", linewidth=1)
    axes[1].set_title("Absolute lift")
    axes[1].set_ylabel("Real overlap - mean shifted overlap")

    figure.suptitle(
        "Motif amplification across the persistent lens family "
        f"k in {PERSISTENCE_KS}"
    )
    figure.savefig(output_dir / "prime_survival_motif_amplification.png", dpi=180)
    plt.close(figure)
    return rows


def plot_stronger_controls(output_dir: Path) -> list[dict[str, float]]:
    odd_nonprimes = [value for value in first_nonprimes(256) if value % 2 == 1][:64]
    control_families = [
        ("SHA primes cube-3", first_primes(64), SHA256_CONSTANTS),
        ("Same primes sqrt", first_primes(64), [nth_root_constant(v, 2) for v in first_primes(64)]),
        ("Same primes fifth", first_primes(64), [nth_root_constant(v, 5) for v in first_primes(64)]),
        ("Next 64 primes cube-3", prime_slice(64, 64), [cube_root_constant(v) for v in prime_slice(64, 64)]),
        ("Odd nonprimes cube-3", odd_nonprimes, [cube_root_constant(v) for v in odd_nonprimes]),
        ("Semiprimes cube-3", first_semiprimes(64), [cube_root_constant(v) for v in first_semiprimes(64)]),
    ]
    palette = ["#1f78b4", "#33a02c", "#6a3d9a", "#ff7f00", "#b15928", "#e31a1c"]
    rows: list[dict[str, float]] = []
    x_positions = np.arange(len(control_families))
    width = 0.22

    figure, axes = plt.subplots(1, 2, figsize=(15, 5), constrained_layout=True)
    for depth_index, depth in enumerate(MOTIF_DEPTHS):
        ratios = []
        lifts = []
        for label, sources, targets in control_families:
            real_scores = motif_overlap_fraction(sources, targets, (depth,), PERSISTENCE_KS)
            shift_values = []
            for offset in range(1, len(targets)):
                shifted_targets = rotate(targets, offset)
                shifted_scores = motif_overlap_fraction(sources, shifted_targets, (depth,), PERSISTENCE_KS)
                shift_values.append(shifted_scores[depth])
            shift_mean = float(np.mean(shift_values))
            real_value = real_scores[depth]
            ratio_value = real_value / shift_mean if shift_mean > 0.0 else float("nan")
            lift_value = real_value - shift_mean
            ratios.append(ratio_value)
            lifts.append(lift_value)
            rows.append(
                {
                    "family": label,
                    "depth": depth,
                    "real_overlap": real_value,
                    "shift_mean": shift_mean,
                    "amplification_ratio": ratio_value,
                    "absolute_lift": lift_value,
                }
            )

        offsets = x_positions + (depth_index - 1) * width
        axes[0].bar(offsets, ratios, width=width, color=palette[depth_index], label=f"G{depth}")
        axes[1].bar(offsets, lifts, width=width, color=palette[depth_index], label=f"G{depth}")

    for axis in axes:
        axis.set_xticks(x_positions)
        axis.set_xticklabels([label for label, _, _ in control_families], rotation=20, ha="right")
        axis.grid(axis="y", alpha=0.2)

    axes[0].axhline(1.0, color="#555555", linestyle=":", linewidth=1)
    axes[0].set_title("Amplification ratio by control family")
    axes[0].set_ylabel("Real overlap / mean shifted overlap")
    axes[0].legend(loc="upper right")

    axes[1].axhline(0.0, color="#555555", linestyle=":", linewidth=1)
    axes[1].set_title("Absolute lift by control family")
    axes[1].set_ylabel("Real overlap - mean shifted overlap")

    figure.suptitle("Stronger deterministic controls for source and transform specificity")
    figure.savefig(output_dir / "prime_survival_stronger_controls.png", dpi=180)
    plt.close(figure)
    return rows


def plot_family_transform_sweep(output_dir: Path) -> list[dict[str, float]]:
    odd_nonprimes = [value for value in first_nonprimes(256) if value % 2 == 1][:64]
    families = [
        ("First 64 primes", first_primes(64)),
        ("Next 64 primes", prime_slice(64, 64)),
        ("Odd nonprimes", odd_nonprimes),
        ("Semiprimes", first_semiprimes(64)),
        ("Integers 2..65", list(range(2, 66))),
    ]
    transforms = [
        ("sqrt", lambda values: [nth_root_constant(v, 2) for v in values]),
        ("cube-3", lambda values: [nth_root_constant(v, 3) for v in values]),
        ("fifth", lambda values: [nth_root_constant(v, 5) for v in values]),
    ]

    best_lift = {1: np.zeros((len(families), len(transforms))), 2: np.zeros((len(families), len(transforms)))}
    best_k = {1: np.zeros((len(families), len(transforms))), 2: np.zeros((len(families), len(transforms)))}
    rows: list[dict[str, float]] = []

    for family_index, (family_label, sources) in enumerate(families):
        for transform_index, (transform_label, transform_fn) in enumerate(transforms):
            targets = transform_fn(sources)
            for depth in (1, 2):
                best_stats = None
                best_k_value = None
                for k_value in K_SWEEP:
                    stats = single_k_motif_stats(sources, targets, depth, k_value)
                    if best_stats is None or stats["absolute_lift"] > best_stats["absolute_lift"]:
                        best_stats = stats
                        best_k_value = k_value
                assert best_stats is not None
                best_lift[depth][family_index, transform_index] = best_stats["absolute_lift"]
                best_k[depth][family_index, transform_index] = best_k_value
                rows.append(
                    {
                        "family": family_label,
                        "transform": transform_label,
                        "depth": depth,
                        "best_k": best_k_value,
                        "best_lift": best_stats["absolute_lift"],
                        "best_ratio": best_stats["amplification_ratio"],
                        "real_overlap": best_stats["real_overlap"],
                        "shift_mean": best_stats["shift_mean"],
                    }
                )

    figure, axes = plt.subplots(2, 2, figsize=(12, 7.5), constrained_layout=True)
    cmap_lift = "YlGnBu"
    cmap_k = "magma"

    for row_index, depth in enumerate((1, 2)):
        lift_ax = axes[row_index, 0]
        k_ax = axes[row_index, 1]

        lift_image = lift_ax.imshow(best_lift[depth], cmap=cmap_lift, aspect="auto")
        k_image = k_ax.imshow(best_k[depth], cmap=cmap_k, aspect="auto", vmin=min(K_SWEEP), vmax=max(K_SWEEP))

        lift_ax.set_title(f"G{depth} max absolute lift")
        k_ax.set_title(f"G{depth} best k")

        for axis in (lift_ax, k_ax):
            axis.set_xticks(np.arange(len(transforms)))
            axis.set_xticklabels([label for label, _ in transforms])
            axis.set_yticks(np.arange(len(families)))
            axis.set_yticklabels([label for label, _ in families])

        for family_index in range(len(families)):
            for transform_index in range(len(transforms)):
                lift_value = best_lift[depth][family_index, transform_index]
                k_value = best_k[depth][family_index, transform_index]
                lift_ax.text(
                    transform_index,
                    family_index,
                    f"{lift_value:.3f}",
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=8,
                )
                k_ax.text(
                    transform_index,
                    family_index,
                    f"{k_value:.2f}",
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=8,
                )

        figure.colorbar(lift_image, ax=lift_ax, fraction=0.046, pad=0.04)
        figure.colorbar(k_image, ax=k_ax, fraction=0.046, pad=0.04)

    figure.suptitle("Family x transform sweep over k in {0.2, 0.3, 0.45, 0.6, 0.8}")
    figure.savefig(output_dir / "prime_survival_family_transform_sweep.png", dpi=180)
    plt.close(figure)
    return rows


def verify_sha_constants() -> None:
    derived = [cube_root_constant(value) for value in first_primes(64)]
    if derived != SHA256_CONSTANTS:
        raise ValueError("Derived cube-root constants do not match official SHA-256 constants.")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = repo_root / "out" / "prime_survival"
    output_dir.mkdir(parents=True, exist_ok=True)

    verify_sha_constants()
    prime_sources = first_primes(64)

    plot_shift_spectrum(output_dir, prime_sources, SHA256_CONSTANTS)
    plot_rank_transfer(output_dir, prime_sources)
    summary_rows = plot_summary_metrics(output_dir)
    motif_rows = plot_motif_amplification(output_dir)
    control_rows = plot_stronger_controls(output_dir)
    sweep_rows = plot_family_transform_sweep(output_dir)

    best_prime_row = max(
        (row for row in summary_rows if row["dataset"] == "Primes"),
        key=lambda row: row["rho"],
    )
    best_motif_row = max(
        (row for row in motif_rows if row["dataset"] == "Primes"),
        key=lambda row: row["amplification_ratio"],
    )
    best_control_g1 = max(
        (row for row in control_rows if row["depth"] == 1),
        key=lambda row: row["amplification_ratio"],
    )
    best_sweep_g1 = max(
        (row for row in sweep_rows if row["depth"] == 1),
        key=lambda row: row["best_lift"],
    )
    best_sweep_g2 = max(
        (row for row in sweep_rows if row["depth"] == 2),
        key=lambda row: row["best_lift"],
    )
    print(f"Saved plots in {output_dir}")
    print(
        "Best prime-source order retention: "
        f"k={best_prime_row['k']:.2f}, rho={best_prime_row['rho']:.3f}, "
        f"nn_overlap={int(best_prime_row['nn_overlap'])}"
    )
    print(
        "Best prime-source motif amplification: "
        f"G{int(best_motif_row['depth'])} = {best_motif_row['amplification_ratio']:.3f} "
        f"(real overlap {best_motif_row['real_overlap']:.3f}, "
        f"shift mean {best_motif_row['shift_mean']:.3f})"
    )
    print(
        "Strongest G1 family across deterministic controls: "
        f"{best_control_g1['family']} = {best_control_g1['amplification_ratio']:.3f}"
    )
    print(
        "Strongest sweep G1 lift: "
        f"{best_sweep_g1['family']} + {best_sweep_g1['transform']} at k={best_sweep_g1['best_k']:.2f} "
        f"(lift {best_sweep_g1['best_lift']:.3f}, ratio {best_sweep_g1['best_ratio']:.3f})"
    )
    print(
        "Strongest sweep G2 lift: "
        f"{best_sweep_g2['family']} + {best_sweep_g2['transform']} at k={best_sweep_g2['best_k']:.2f} "
        f"(lift {best_sweep_g2['best_lift']:.3f}, ratio {best_sweep_g2['best_ratio']:.3f})"
    )


if __name__ == "__main__":
    main()
