#!/usr/bin/env python3
"""
python tests/gyro/gyro_dat_plot.py --file ./tests/gyro/GyroA50HzData.dat --save ./tests/gyro/GyroA50HzData.png
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def load_gyro_dat(file_path: os.PathLike | str) -> np.ndarray:
    """Load big-endian float32 triples from a .dat file into an (N, 3) array.

    Truncates trailing values if the total count is not a multiple of 3.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read as big-endian float32
    raw = np.fromfile(str(file_path), dtype=np.dtype(">f4"))
    if raw.size == 0:
        raise ValueError(f"Empty or unreadable file: {file_path}")

    if (raw.size % 3) != 0:
        raise ValueError(
            f"Value count {raw.size} is not a multiple of 3 (expected groups of 3 floats)."
        )

    data = raw.reshape(-1, 3)
    return data


def plot_gyro(time_s: np.ndarray, data: np.ndarray, title: str = "Gyro Data", save: str | None = None) -> None:
    if data.shape[1] != 3:
        raise ValueError("Expected data with shape (N, 3)")
    
    # data = np.rad2deg(data)  # Convert from radians to degrees

    plt.figure(figsize=(12, 5))
    labels = ["X", "Y", "Z"]
    colors = ["tab:blue", "tab:orange", "tab:green"]

    # Plot signals and compute means
    means = []
    for i in range(3):
        plt.plot(time_s, data[:, i], label=labels[i], color=colors[i])
        m = float(np.mean(data[:, i])) if data.shape[0] > 0 else float("nan")
        means.append(m)
    # Mean lines
    for i in range(3):
        plt.hlines(means[i], xmin=time_s[0], xmax=time_s[-1], colors=colors[i], linestyles="--", alpha=1, linewidth=3)

    plt.xlabel("Time [s]")
    plt.ylabel("Value (deg/s)")
    plt.title(title)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()

    # Add a statistics text box
    stats = (
        f"Means:\n"
        f"  X: {means[0]:.6f}\n"
        f"  Y: {means[1]:.6f}\n"
        f"  Z: {means[2]:.6f}"
    )
    # Place textbox at top-right inside axes
    ax = plt.gca()
    ax.text(
        0.995,
        0.98,
        stats,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.75),
    )
    plt.tight_layout()

    if save:
        out = Path(save)
        out.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out, dpi=150)
        print(f"Saved plot to: {out}")
    else:
        plt.show()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Parse and plot big-endian float32 gyro .dat files (XYZ triples)")
    p.add_argument("--file", "-f", type=str, default="GyroA50HzData.dat", help="Path to .dat file (default: GyroA50HzData.dat)")
    p.add_argument("--save", type=str, default=None, help="Save plot to this path instead of showing")
    p.add_argument("--csv", type=str, default=None, help="Optionally export data to CSV (time_s,X_deg_s,Y_deg_s,Z_deg_s)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    dat_path = Path(args.file)
    data = load_gyro_dat(dat_path)
    title = f"Gyro Data\n{dat_path.name}"
    print(data)

    # Time slicing
    fs = 50.0  # Default sampling rate in Hz
    n = data.shape[0]
    t = np.arange(n) / float(fs)

    # Optional CSV export (degrees per second, consistent with plot)
    if args.csv:
        out = Path(args.csv)
        out.parent.mkdir(parents=True, exist_ok=True)
        # data_deg = np.rad2deg(data)
        arr = np.column_stack([t, data])
        header = "time_s,X_deg_s,Y_deg_s,Z_deg_s"
        np.savetxt(out, arr, delimiter=",", header=header, comments="")
        print(f"Saved CSV to: {out}")

    plot_gyro(t, data, title=title, save=args.save)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
