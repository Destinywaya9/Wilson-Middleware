from __future__ import annotations

import json
import time
from typing import Any, Optional, Protocol

from .audit import HashChain, sha256_text
from .canon import P2_FULL
from .models import BaseModelAdapter


class P2ClosureEngine(Protocol):
    expected_p2_sequence: tuple[str, ...]
    expected_gate_sequence: tuple[str, ...]

    def run(self, *, tag: str = "p2-closure") -> dict[str, Any]: ...


class WilsonMiddleware:
    """Minimal Wilson public middleware.

    Runtime only:
        Tensor P2 / EchoP2 closure execution
        -> entropy + coherence measurement
        -> external model may connect
        -> live user/model interaction
        -> fresh P2/noise audit before candidate release
        -> repeat

    QRTM, Tensor P3 spatial indexing, ethics adapters, and other Wilson layers
    are intentionally outside this minimal runtime path.
    """

    def __init__(
        self,
        p2_engine: P2ClosureEngine,
        model: Optional[BaseModelAdapter] = None,
        *,
        log_plaintext: bool = True,
        time_fn=time.time,
    ):
        self.p2_engine = p2_engine
        self.model: Optional[BaseModelAdapter] = None
        self.log_plaintext = bool(log_plaintext)
        self._time_fn = time_fn

        self.audit_chain = HashChain("prev_audit_hash", "audit_row_hash")
        self.interaction_chain = HashChain("prev_row_hash", "row_hash")

        self.environment_locked = False
        self.environment_generation = 0
        self.latest_measurement: dict[str, Any] | None = None
        self.bootstrap_measurement: dict[str, Any] | None = None

        # P2 runs and is measured immediately. No model is connected yet.
        bootstrap = self._enforce_p2(tag="environment-bootstrap")
        self.bootstrap_measurement = dict(bootstrap)

        if model is not None:
            self.attach_model(model)

    def _expected_p2_sequence(self) -> tuple[str, ...]:
        return tuple(getattr(self.p2_engine, "expected_p2_sequence", P2_FULL))

    def _expected_gate_sequence(self) -> tuple[str, ...]:
        seq = getattr(self.p2_engine, "expected_gate_sequence", ())
        return tuple(seq)

    def _validate_measurement(self, record: dict[str, Any]) -> tuple[bool, list[str]]:
        errors: list[str] = []
        expected_p2 = self._expected_p2_sequence()
        expected_gates = self._expected_gate_sequence()

        if tuple(expected_p2) != tuple(P2_FULL):
            errors.append("engine P2 sequence does not match canonical Tensor P2")

        if str(record.get("p2_sequence", "")) != " / ".join(expected_p2):
            errors.append("P2 sequence mismatch")

        if expected_gates and str(record.get("gate_sequence", "")) != " / ".join(expected_gates):
            errors.append("EchoP2 gate sequence mismatch")

        if record.get("entry_stage") != "3,3":
            errors.append("3,3 entry missing")

        if record.get("terminal_closure_stage") != "0,0":
            errors.append("terminal 0,0 closure missing")

        if int(record.get("delay_value", -1)) != 200:
            errors.append("Delay(200) missing or altered")

        if not str(record.get("noise_source", "")).strip():
            errors.append("noise stream provenance missing")

        if bool(record.get("pauli_tomography", False)):
            errors.append("Pauli tomography is outside this runtime")

        counts = record.get("counts") or {}
        if not counts or sum(int(v) for v in counts.values()) <= 0:
            errors.append("measurement counts missing")

        if record.get("entropy_leakage_bits") is None:
            errors.append("entropy measurement missing")

        if record.get("coherence_fidelity_percent") is None:
            errors.append("coherence measurement missing")

        if record.get("expected_closure_state") != "000":
            errors.append("expected closure state mismatch")

        # No arbitrary entropy/fidelity threshold is introduced here.
        # The measured terminal closure outcome must remain the dominant state.
        if not bool(record.get("closure_state_ok", False)):
            errors.append("terminal 0,0 / 000 is not the dominant measured closure state")

        return (len(errors) == 0), errors

    def _enforce_p2(self, *, tag: str) -> dict[str, Any]:
        try:
            record = dict(self.p2_engine.run(tag=tag))
            valid, errors = self._validate_measurement(record)
        except Exception as exc:
            self.environment_locked = False
            self.audit_chain.append({
                "timestamp_unix": self._time_fn(),
                "audit_tag": tag,
                "p2_enforced": False,
                "environment_locked": False,
                "error": f"{type(exc).__name__}: {exc}",
            })
            raise RuntimeError(f"Tensor P2 closure failed during {tag}: {exc}") from exc

        self.environment_locked = bool(valid)
        if valid:
            self.environment_generation += 1
            self.latest_measurement = record

        audit_row = self.audit_chain.append({
            "timestamp_unix": self._time_fn(),
            "audit_tag": tag,
            "p2_enforced": bool(valid),
            "environment_locked": bool(valid),
            "environment_generation": self.environment_generation,
            "validation_errors": "|".join(errors),
            "backend_name": record.get("backend_name"),
            "job_id": record.get("job_id"),
            "shots": record.get("shots"),
            "p2_sequence": record.get("p2_sequence"),
            "gate_sequence": record.get("gate_sequence"),
            "terminal_closure_stage": record.get("terminal_closure_stage"),
            "delay_value": record.get("delay_value"),
            "delay_unit": record.get("delay_unit"),
            "noise_source": record.get("noise_source"),
            "noise_stream_kind": record.get("noise_stream_kind"),
            "depolarizing_probability": record.get("depolarizing_probability"),
            "counts_json": json.dumps(
                record.get("counts") or {}, sort_keys=True, separators=(",", ":")
            ),
            "entropy_leakage_bits": record.get("entropy_leakage_bits"),
            "coherence_fidelity_percent": record.get("coherence_fidelity_percent"),
            "expected_closure_probability": record.get("expected_closure_probability"),
            "dominant_state": record.get("dominant_state"),
            "closure_state_ok": record.get("closure_state_ok"),
            "source_circuit_sha256": record.get("source_circuit_sha256"),
            "transpiled_circuit_sha256": record.get("transpiled_circuit_sha256"),
        })

        if not valid:
            raise RuntimeError(
                "Tensor P2 closure measurement did not validate: " + "; ".join(errors)
            )

        return {**record, "audit_row_hash": audit_row["audit_row_hash"]}

    def attach_model(self, model: BaseModelAdapter) -> dict[str, Any]:
        if not self.environment_locked or self.latest_measurement is None:
            raise RuntimeError(
                "External model cannot connect before Tensor P2 closure and "
                "coherence/entropy measurement complete."
            )
        self.model = model
        return {
            "model_connected": True,
            "model_id": model.model_id,
            "model_revision": model.revision,
            "model_backend": model.backend,
            "p2_environment_generation": self.environment_generation,
            "p2_audit_root": self.audit_chain.last_hash,
        }

    connect_model = attach_model

    def interact(self, text: str, request_id: Optional[str] = None) -> dict[str, Any]:
        if self.model is None:
            raise RuntimeError("No external model is connected to Wilson.")
        if not self.environment_locked:
            raise RuntimeError(
                "Tensor P2 environment is not locked. Run audit_now() before model execution."
            )
        if not str(text).strip():
            raise ValueError("live user input is empty")

        event_id = len(self.interaction_chain.rows)
        request_id = request_id or f"live-{event_id:06d}"

        pre_measurement = dict(self.latest_measurement or {})
        pre_audit_root = self.audit_chain.last_hash
        pre_generation = self.environment_generation

        # The model is already connected inside a measured P2 environment.
        candidate = self.model.generate(text)

        # Fresh EchoP2 execution audits the active noise stream before release.
        try:
            post_measurement = self._enforce_p2(tag=f"interaction:{request_id}")
            response_emitted = True
            status = "EMITTED_AFTER_P2_CLOSURE"
            response = candidate
            failure_text = ""
        except Exception as exc:
            post_measurement = None
            response_emitted = False
            status = "WITHHELD_P2_CLOSURE_FAILED"
            response = ""
            failure_text = f"{type(exc).__name__}: {exc}"

        row = self.interaction_chain.append({
            "event_id": event_id,
            "request_id": request_id,
            "timestamp_unix": self._time_fn(),
            "model_id": self.model.model_id,
            "model_revision": self.model.revision,
            "model_backend": self.model.backend,
            "p2_locked_before_model": True,
            "p2_generation_before_model": pre_generation,
            "p2_audit_root_before_model": pre_audit_root,
            "pre_entropy_leakage_bits": pre_measurement.get("entropy_leakage_bits"),
            "pre_coherence_fidelity_percent": pre_measurement.get("coherence_fidelity_percent"),
            "pre_noise_source": pre_measurement.get("noise_source"),
            "model_candidate_sha256": sha256_text(candidate),
            "post_p2_closure_complete": bool(post_measurement is not None),
            "post_entropy_leakage_bits": (
                post_measurement.get("entropy_leakage_bits") if post_measurement else None
            ),
            "post_coherence_fidelity_percent": (
                post_measurement.get("coherence_fidelity_percent") if post_measurement else None
            ),
            "post_noise_source": post_measurement.get("noise_source") if post_measurement else None,
            "post_counts_json": json.dumps(
                post_measurement.get("counts") if post_measurement else {},
                sort_keys=True,
                separators=(",", ":"),
            ),
            "p2_audit_root_after_model": self.audit_chain.last_hash,
            "interaction_status": status,
            "response_emitted": response_emitted,
            "failure": failure_text,
            "request_text": text if self.log_plaintext else "[HASH_ONLY]",
            "request_sha256": sha256_text(text),
            "model_output": response if self.log_plaintext else (
                "[HASH_ONLY]" if response_emitted else ""
            ),
            "model_output_sha256": sha256_text(response) if response_emitted else "",
        })
        return row

    handle = interact

    def audit_now(self, *, tag: str = "manual-live-audit") -> dict[str, Any]:
        return self._enforce_p2(tag=tag)

    def live_status(self) -> dict[str, Any]:
        measurement = self.latest_measurement or {}
        return {
            "p2_environment_locked": self.environment_locked,
            "environment_generation": self.environment_generation,
            "model_connected": self.model is not None,
            "model_id": self.model.model_id if self.model else None,
            "backend_name": measurement.get("backend_name"),
            "job_id": measurement.get("job_id"),
            "noise_source": measurement.get("noise_source"),
            "noise_stream_kind": measurement.get("noise_stream_kind"),
            "depolarizing_probability": measurement.get("depolarizing_probability"),
            "shots": measurement.get("shots"),
            "entropy_leakage_bits": measurement.get("entropy_leakage_bits"),
            "coherence_fidelity_percent": measurement.get("coherence_fidelity_percent"),
            "expected_closure_probability": measurement.get("expected_closure_probability"),
            "dominant_state": measurement.get("dominant_state"),
            "counts": measurement.get("counts"),
            "p2_audit_root": self.audit_chain.last_hash,
            "interaction_root": self.interaction_chain.last_hash,
        }

    @property
    def rows(self):
        return self.interaction_chain.rows

    @property
    def audit_rows(self):
        return self.audit_chain.rows

    def verify_kernel(self) -> bool:
        return tuple(self._expected_p2_sequence()) == tuple(P2_FULL)

    def verify_chain(self) -> bool:
        return self.interaction_chain.verify()

    def verify_audit_chain(self) -> bool:
        return self.audit_chain.verify()
