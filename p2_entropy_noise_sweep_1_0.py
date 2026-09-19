"""
Tensor P2 Entropy Closure — Appendix B
Localized noise-channel robustness sweep at 1,0, readout after final 0,0.

Author: Destiny Machwaya
Lei A While Research Center, Wahiawa, Hawaii, United States
Copyright © 2015–2026 Destiny Machwaya.

Companion code for the manuscript draft:
Tensor P2 Entropy Closure.

This file is simulation code for the manuscript. It is not the dual-platform
hardware campaign published as:

Machwaya, D. (2026). Hardware demonstration of a fixed Tensor P2 kernel:
zero-entropy leakage and stable coherence across dual microcontroller
platforms. Frontiers in Physics. https://doi.org/10.3389/fphy.2026.1758206
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

P2_WINDOW = ["0,0", "0,1", "1,2", "2,1", "1,0", "0,0"]
N_QUBITS = 3
D = 2 ** N_QUBITS
P_NOISE = 0.01

P2_ENCODING = {
    "0,0": "000",
    "0,1": "001",
    "1,0": "010",
    "1,2": "011",
    "2,1": "100",
    "3,3": "101",
}


def ket_from_bitstring(bitstring):
    index = int(bitstring, 2)
    v = np.zeros((D, 1), dtype=complex)
    v[index, 0] = 1.0
    return v


def pure_density(label):
    v = ket_from_bitstring(P2_ENCODING[label])
    return v @ v.conj().T


def von_neumann_entropy(rho, base=2):
    rho = (rho + rho.conj().T) / 2
    vals = np.linalg.eigvalsh(rho)
    vals = np.clip(vals.real, 0.0, None)
    vals = vals[vals > 1e-14]
    if len(vals) == 0:
        return 0.0
    return float(-np.sum(vals * np.log(vals)) / np.log(base))


def purity(rho):
    return float(np.trace(rho @ rho).real)


def report_density(rho):
    eigvals = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    eigvals = np.clip(eigvals.real, 0.0, None)
    return {
        "trace": float(np.trace(rho).real),
        "purity": purity(rho),
        "S_vN_bits": abs(von_neumann_entropy(rho)),
        "eigenvalues": np.round(eigvals, 12),
    }


I1 = np.array([[1, 0], [0, 1]], dtype=complex)
X1 = np.array([[0, 1], [1, 0]], dtype=complex)
Z1 = np.array([[1, 0], [0, -1]], dtype=complex)


def expand_single_qubit_operator(op, target, n_qubits):
    ops = []
    for q in range(n_qubits):
        if q == target:
            ops.append(op)
        else:
            ops.append(I1)
    full = ops[0]
    for next_op in ops[1:]:
        full = np.kron(full, next_op)
    return full


def apply_kraus_channel(rho, kraus_ops):
    out = np.zeros_like(rho, dtype=complex)
    for K in kraus_ops:
        out += K @ rho @ K.conj().T
    return out


def depolarizing_channel(rho, p):
    return (1 - p) * rho + p * np.eye(D, dtype=complex) / D


def bit_flip_channel(rho, p, target_qubit=0):
    X = expand_single_qubit_operator(X1, target_qubit, N_QUBITS)
    return (1 - p) * rho + p * (X @ rho @ X.conj().T)


def phase_flip_channel(rho, p, target_qubit=0):
    Z = expand_single_qubit_operator(Z1, target_qubit, N_QUBITS)
    return (1 - p) * rho + p * (Z @ rho @ Z.conj().T)


def amplitude_damping_channel(rho, gamma, target_qubit=0):
    K0_1q = np.array([
        [1, 0],
        [0, np.sqrt(1 - gamma)],
    ], dtype=complex)
    K1_1q = np.array([
        [0, np.sqrt(gamma)],
        [0, 0],
    ], dtype=complex)
    K0 = expand_single_qubit_operator(K0_1q, target_qubit, N_QUBITS)
    K1 = expand_single_qubit_operator(K1_1q, target_qubit, N_QUBITS)
    return apply_kraus_channel(rho, [K0, K1])


def phase_damping_channel(rho, gamma, target_qubit=0):
    K0_1q = np.sqrt(1 - gamma) * I1
    K1_1q = np.sqrt(gamma) * np.array([
        [1, 0],
        [0, 0],
    ], dtype=complex)
    K2_1q = np.sqrt(gamma) * np.array([
        [0, 0],
        [0, 1],
    ], dtype=complex)
    K0 = expand_single_qubit_operator(K0_1q, target_qubit, N_QUBITS)
    K1 = expand_single_qubit_operator(K1_1q, target_qubit, N_QUBITS)
    K2 = expand_single_qubit_operator(K2_1q, target_qubit, N_QUBITS)
    return apply_kraus_channel(rho, [K0, K1, K2])


NOISE_CHANNELS = {
    "none": lambda rho: rho,
    "depolarizing_at_1_0": lambda rho: depolarizing_channel(rho, P_NOISE),
    "bit_flip_at_1_0": lambda rho: bit_flip_channel(rho, P_NOISE, target_qubit=0),
    "phase_flip_at_1_0": lambda rho: phase_flip_channel(rho, P_NOISE, target_qubit=0),
    "amplitude_damping_at_1_0": lambda rho: amplitude_damping_channel(rho, P_NOISE, target_qubit=0),
    "phase_damping_at_1_0": lambda rho: phase_damping_channel(rho, P_NOISE, target_qubit=0),
}

all_records = []
final_records = []

for channel_name, channel_fn in NOISE_CHANNELS.items():
    step_records = []

    for step, label in enumerate(P2_WINDOW):
        rho = pure_density(label)
        event = "P2 state"

        if label == "1,0":
            rho = channel_fn(rho)
            event = f"{channel_name}"

        if step == len(P2_WINDOW) - 1 and label == "0,0":
            rho = pure_density("0,0")
            event = "final 0,0 forced closure"

        metrics = report_density(rho)
        row = {
            "channel": channel_name,
            "step": step,
            "P2_state": label,
            "event": event,
            "trace": metrics["trace"],
            "purity": metrics["purity"],
            "S_vN_bits": metrics["S_vN_bits"],
            "eigenvalues": metrics["eigenvalues"],
        }
        step_records.append(row)
        all_records.append(row)

    final_records.append(step_records[-1].copy())

df_all = pd.DataFrame(all_records)
df_final = pd.DataFrame(final_records)

print("\n================ FINAL P2 ROBUSTNESS OUTPUT ================")
print("Window: first 0,0 -> final 0,0")
print("Noise site: 1,0 only")
print(f"Noise probability / gamma: {P_NOISE}")
print(f"Hilbert dimension: {D}")
print("\nFinal forced 0,0 results by noise channel:")
print(
    df_final[
        ["channel", "P2_state", "trace", "purity", "S_vN_bits", "eigenvalues"]
    ].to_string(index=False)
)
print("============================================================")

df_all.to_csv("p2_noise_sweep_all_steps.csv", index=False)
df_final.to_csv("p2_noise_sweep_final_outputs.csv", index=False)

plt.figure(figsize=(10, 5))
for channel_name in NOISE_CHANNELS.keys():
    subset = df_all[df_all["channel"] == channel_name]
    plt.plot(subset["step"], subset["S_vN_bits"], marker="o", label=channel_name)
plt.xticks(range(len(P2_WINDOW)), P2_WINDOW)
plt.xlabel("P2 node")
plt.ylabel("Von Neumann entropy S(rho), bits")
plt.title("P2 Entropy Robustness Sweep: Noise Localized at 1,0")
plt.legend()
plt.tight_layout()
plt.savefig("p2_entropy_noise_sweep_1_0.png", dpi=180, bbox_inches="tight")
plt.show()
