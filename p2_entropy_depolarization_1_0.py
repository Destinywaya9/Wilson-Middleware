"""
Tensor P2 Entropy Closure — Appendix A
Localized depolarization at 1,0, readout after final 0,0.

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
P_DEPOL = 0.01
N_QUBITS = 3
D = 2 ** N_QUBITS

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


def depolarize_at_1_0(rho, p):
    return (1 - p) * rho + p * np.eye(D, dtype=complex) / D


def von_neumann_entropy(rho, base=2):
    rho = (rho + rho.conj().T) / 2
    vals = np.linalg.eigvalsh(rho)
    vals = np.clip(vals.real, 0.0, None)
    vals = vals[vals > 1e-14]
    return float(-np.sum(vals * np.log(vals)) / np.log(base))


def purity(rho):
    return float(np.trace(rho @ rho).real)


records = []

for step, label in enumerate(P2_WINDOW):
    rho = pure_density(label)
    event = "P2 state"

    if label == "1,0":
        rho = depolarize_at_1_0(rho, P_DEPOL)
        event = "1,0 localized depolarization"

    if step == len(P2_WINDOW) - 1 and label == "0,0":
        rho = pure_density("0,0")
        event = "final 0,0 forced closure"

    eigvals = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    eigvals = np.clip(eigvals.real, 0.0, None)

    records.append({
        "step": step,
        "P2_state": label,
        "event": event,
        "trace": np.trace(rho).real,
        "purity": purity(rho),
        "S_vN_bits": von_neumann_entropy(rho),
        "eigenvalues": np.round(eigvals, 12),
    })

df = pd.DataFrame(records)

print("P2 window: first 0,0 to final 0,0")
print(f"Depolarization only at 1,0, p = {P_DEPOL}")
print(f"Hilbert dimension d = {D}")
print(df.to_string(index=False))

final = df.iloc[-1]
print("\nFinal output:")
print(f"Final state: {final['P2_state']}")
print(f"Final event: {final['event']}")
print(f"Trace: {final['trace']}")
print(f"Purity: {final['purity']}")
print(f"Von Neumann entropy, bits: {abs(final['S_vN_bits'])}")
print(f"Eigenvalues: {final['eigenvalues']}")

df.to_csv("p2_entropy_depolarization_1_0.csv", index=False)

plt.figure(figsize=(9, 4.5))
plt.plot(df["step"], df["S_vN_bits"].abs(), marker="o")
plt.xticks(df["step"], df["P2_state"])
plt.xlabel("P2 node")
plt.ylabel("Von Neumann entropy S(rho), bits")
plt.title("P2 Entropy: First 0,0 to Final 0,0")
plt.tight_layout()
plt.savefig("p2_entropy_depolarization_1_0.png", dpi=180, bbox_inches="tight")
plt.show()
