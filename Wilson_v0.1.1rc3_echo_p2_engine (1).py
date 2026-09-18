from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any

from .audit import sha256_text
from .canon import P2_FULL


P2_SEQUENCE = tuple(P2_FULL)
ECHOP2_GATE_SEQUENCE = (
    "3,3:init",
    "H(0)",
    "CX(0,1)",
    "CX(1,2)",
    "CX(1,2)",
    "CX(0,1)",
    "H(0)",
    "Delay(200)",
)
EXPECTED_CLOSURE_STATE = "000"
DEFAULT_SHOTS = 131072
DEFAULT_DEPOLARIZING_P = 0.1


def compute_entropy_and_fidelity(counts: dict[str, int]) -> tuple[float, float]:
    """Return the existing Wilson/EchoP2 measurement readout.

    entropy: Shannon entropy of the measured bit-string distribution, in bits.
    fidelity: maximum measured outcome probability, in percent.
    """
    total = int(sum(int(v) for v in counts.values()))
    if total <= 0:
        raise ValueError("measurement counts are empty")

    probs = [float(v) / float(total) for v in counts.values()]
    entropy = -sum(p * math.log2(p) for p in probs if p > 0.0)
    if abs(entropy) < 1e-15:
        entropy = 0.0
    fidelity = max(probs) * 100.0
    return float(entropy), float(fidelity)


def _normalize_counts(counts: dict[Any, Any]) -> dict[str, int]:
    return {str(k).replace(" ", ""): int(v) for k, v in counts.items()}


def build_echo_p2_circuit(*, name: str = "wilson_echo_p2", delay_value: int = 200):
    """Build Destiny Machwaya's supplied EchoP2 demonstration circuit exactly."""
    from qiskit import QuantumCircuit

    if int(delay_value) != 200:
        raise ValueError("Tensor P2 Delay(200) must remain 200.")

    qc = QuantumCircuit(3, 3, name=name)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()
    qc.delay(200, 0)
    qc.delay(200, 1)
    qc.delay(200, 2)
    qc.measure([0, 1, 2], [0, 1, 2])

    qc.metadata = {
        "kernel": "Tensor P2 / EchoP2",
        "p2_sequence": list(P2_SEQUENCE),
        "gate_sequence": list(ECHOP2_GATE_SEQUENCE),
        "entry_stage": "3,3",
        "terminal_closure_stage": "0,0",
        "delay_value": 200,
    }
    return qc


def build_depolarizing_noise_model(*, probability: float = DEFAULT_DEPOLARIZING_P):
    """Build the exact single-/two-qubit depolarizing noise model supplied for EchoP2."""
    from qiskit_aer.noise import NoiseModel, depolarizing_error

    p = float(probability)
    if not (0.0 <= p <= 1.0):
        raise ValueError("depolarizing probability must be between 0 and 1")

    noise_model = NoiseModel()
    single_qubit_error = depolarizing_error(p, 1)
    two_qubit_error = depolarizing_error(p, 2)
    noise_model.add_all_qubit_quantum_error(single_qubit_error, ["h"])
    noise_model.add_all_qubit_quantum_error(two_qubit_error, ["cx"])
    return noise_model


class EchoP2AerEngine:
    """Minimal EchoP2 closure/noise engine used by the public Wilson live demo.

    Runtime is intentionally limited to:
      EchoP2 -> depolarizing noise stream -> counts -> entropy/coherence readout.
    """

    expected_p2_sequence = P2_SEQUENCE
    expected_gate_sequence = ECHOP2_GATE_SEQUENCE

    def __init__(
        self,
        *,
        shots: int = DEFAULT_SHOTS,
        depolarizing_probability: float = DEFAULT_DEPOLARIZING_P,
        output_dir: str | None = None,
    ):
        self.shots = int(shots)
        if self.shots <= 0:
            raise ValueError("shots must be positive")
        self.depolarizing_probability = float(depolarizing_probability)
        if not (0.0 <= self.depolarizing_probability <= 1.0):
            raise ValueError("depolarizing probability must be between 0 and 1")
        self.output_dir = Path(output_dir) if output_dir else None
        self.run_index = 0
        if self.output_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, *, tag: str = "p2-closure") -> dict[str, Any]:
        from qiskit import qasm3, transpile
        from qiskit_aer import AerSimulator

        run_index = self.run_index
        self.run_index += 1

        qc = build_echo_p2_circuit(name=f"wilson_echo_p2_{run_index:04d}")
        qc.metadata["audit_tag"] = str(tag)

        noise_model = build_depolarizing_noise_model(
            probability=self.depolarizing_probability
        )
        simulator = AerSimulator(noise_model=noise_model)
        transpiled_qc = transpile(qc, simulator)

        source_qasm = qasm3.dumps(qc)
        transpiled_qasm = qasm3.dumps(transpiled_qc)

        submitted_at = time.time()
        job = simulator.run(transpiled_qc, shots=self.shots)
        result = job.result()
        completed_at = time.time()
        counts = _normalize_counts(result.get_counts())

        total = int(sum(counts.values()))
        if total <= 0:
            raise RuntimeError("EchoP2 simulation returned no measurement counts")

        entropy_bits, fidelity_percent = compute_entropy_and_fidelity(counts)
        probabilities = {
            state: float(count) / float(total)
            for state, count in counts.items()
        }
        dominant_state = max(counts, key=counts.get)
        p000 = float(counts.get(EXPECTED_CLOSURE_STATE, 0)) / float(total)

        job_id_attr = getattr(job, "job_id", None)
        if callable(job_id_attr):
            try:
                job_id = str(job_id_attr())
            except Exception:
                job_id = f"aer-{run_index:04d}"
        else:
            job_id = f"aer-{run_index:04d}"

        noise_source = f"AER_DEPOLARIZING_P_{self.depolarizing_probability:g}"

        record = {
            "audit_tag": str(tag),
            "run_index": run_index,
            "backend_name": "aer_simulator",
            "job_id": job_id,
            "submitted_at_unix": submitted_at,
            "completed_at_unix": completed_at,
            "shots": total,
            "kernel": "Tensor P2 / EchoP2",
            "p2_sequence": " / ".join(P2_SEQUENCE),
            "gate_sequence": " / ".join(ECHOP2_GATE_SEQUENCE),
            "entry_stage": "3,3",
            "terminal_closure_stage": "0,0",
            "delay_value": 200,
            "delay_unit": "qiskit_default",
            "noise_source": noise_source,
            "noise_stream_present": True,
            "noise_stream_kind": "depolarizing",
            "depolarizing_probability": self.depolarizing_probability,
            "synthetic_noise_injected": True,
            "aer_noise_model_used": True,
            "pauli_tomography": False,
            "counts": counts,
            "probabilities": probabilities,
            "entropy_leakage_bits": entropy_bits,
            "coherence_fidelity_percent": fidelity_percent,
            "expected_closure_state": EXPECTED_CLOSURE_STATE,
            "expected_closure_probability": p000,
            "dominant_state": dominant_state,
            "closure_state_ok": dominant_state == EXPECTED_CLOSURE_STATE,
            "source_circuit_sha256": sha256_text(source_qasm),
            "transpiled_circuit_sha256": sha256_text(transpiled_qasm),
            "transpiled_depth": int(transpiled_qc.depth()),
            "transpiled_size": int(transpiled_qc.size()),
        }

        if self.output_dir:
            stem = f"{run_index:04d}_{str(tag).replace(' ', '_').replace(':', '_')}"
            (self.output_dir / f"{stem}_source.qasm").write_text(
                source_qasm, encoding="utf-8"
            )
            (self.output_dir / f"{stem}_transpiled.qasm").write_text(
                transpiled_qasm, encoding="utf-8"
            )
            (self.output_dir / f"{stem}_measurement.json").write_text(
                json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
            )

        return record


# Backward-compatible names for callers that imported the rc2 constants.
P2_QPU_SEQUENCE = P2_SEQUENCE
P2_QPU_GATE_SEQUENCE = ECHOP2_GATE_SEQUENCE
