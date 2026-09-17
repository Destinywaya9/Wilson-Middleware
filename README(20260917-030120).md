# Wilson v0.1 — Open Reference Middleware

**Authored and owned by Destiny Machwaya**

Wilson is a source-available, auditable middleware reference implementation designed to sit between a user/request stream and a replaceable underlying AI model.

Wilson is not the underlying language model.

The reference implementation exposes its middleware decisions, Tensor P2 traversal state, QRTM observation channel, P3/QTL-Sphere audit context, ethics checkpoints, model-call boundary, and optional IBM Quantum QPU evidence so reviewers can inspect what Wilson did versus what the base model did.

> **License status:** Source-available. Patent rights reserved.  
> See `WILSON_OPEN_REFERENCE_LICENSE_v1.0.txt`.

---

## What Wilson Demonstrates

The public reference implementation is intended to make Wilson inspectable rather than opaque.

It demonstrates:

- immutable Tensor P2 middleware traversal;
- explicit QRTM observation and quantization;
- P3 audit context;
- D12 / QTL-Sphere visual registry;
- `0 = M_E` audit reference;
- mandatory ethics enforcement at every canonical `0,0`;
- an additional request-entry ethics check;
- an output ethics check before emission;
- replaceable open-model adapters;
- optional IBM Quantum QPU measurement evidence;
- separate hash-chained middleware, ethics, and QPU ledgers;
- reproducible audit receipts and SHA-256 artifact verification.

The base model can be replaced without changing Wilson's middleware contract.

---

## Canonical Tensor P2

The reference implementation preserves the canonical Tensor P2 traversal:

```text
3,3 / 0,0 / 0,1 / 1,2 / 2,1 / 1,0 / 0,0 / Delay(200)
```

Within this release:

- `3,3` is the bounded triadic entry condition.
- the first `0,0` is the folded total-state reference after entry;
- `0,1`, `1,2`, `2,1`, and `1,0` are traversal states;
- the final `0,0` is the lawful terminal return condition;
- `Delay(200)` is post-return temporal spacing, not a new state.

The middleware does not adapt, rewrite, optimize, or learn a replacement Tensor P2 kernel.

---

## Zero and the Echo Meridian

The public audit layer follows:

```text
0 = M_E
```

Zero is not treated as emptiness, null, absence, or a separate external coordinate.

The D12 / QTL-Sphere visualization is an audit/display layer. It does **not** invent an undisclosed Wilson-event-to-D12 traversal rule.

Where no canonical event-to-direction rule is disclosed, the ledger states that explicitly.

---

## Tensor P3 Audit Context

The canonical form is:

```text
P3 = [P2_1 ⊗ D_1, P2_2 ⊗ D_2, P2_3 ⊗ D_3]
```

The public reference visualization uses the disclosed directional clustering:

```text
P3_1: ±X, ±Y
P3_2: ±Z, XY±
P3_3: YZ±, ZX±
```

The visualization is for auditability and does not redefine Tensor P3.

---

## QRTM

QRTM is exposed as an explicit observation channel.

The public middleware does **not** infer QRTM from hidden model activations, user sentiment, mood classification, or a concealed text-to-QRTM model.

A request provides an explicit review observation such as:

```text
phase_rad
admissible
spike_flag
```

The reference adapter then performs the disclosed bounded quantization and audit steps.

A QRTM rejection is recorded separately from an ethics rejection.

---

## Mandatory Ethics Checkpoints

Wilson's reference architecture requires ethics evaluation at every canonical `0,0`.

That means ethics is checked at:

1. request entry;
2. opening `0,0` reference;
3. terminal `0,0` return; and
4. output before emission.

The reference ethics policy is versioned and hashed.

It contains:

- a paraphrased Three Laws of Robotics profile; and
- a Ten Commandments policy profile.

Rules that do not map meaningfully to a software action are recorded as `NOT_APPLICABLE` rather than silently reinterpreted.

Every ethics evaluation is written to an independent hash-chained ethics ledger.

A failed mandatory ethics checkpoint prevents the associated model action or output emission.

See:

```text
docs/ETHICS.md
Wilson_Ethics_Policy.json
Wilson_Ethics_Checkpoint_Ledger.csv
```

---

## Middleware Boundary

The intended execution path is:

```text
request + explicit QRTM observation
        ↓
Wilson middleware
        ↓
ethics + P2/QRTM audit
        ↓
replaceable base model
        ↓
output ethics audit
        ↓
response
```

Optional IBM Quantum evidence is attached as a separate measurement/audit lane.

The QPU does not:

- rewrite Tensor P2;
- create Wilson actions;
- alter the ethics policy;
- become a reinforcement signal;
- modify QRTM admissibility;
- override a rejected middleware decision.

---

## Open Model Demonstration

The Colab reference can use a replaceable open model.

The current default demonstration adapter is configured for a small instruction-tuned open model suitable for Colab review.

Reviewers may replace the model adapter while leaving Wilson unchanged.

The public test compares:

```text
direct base-model output
vs.
Wilson-admitted base-model output
```

for deterministic runs so reviewers can verify that Wilson is acting as middleware rather than silently rewriting admitted model responses.

---

## IBM Quantum QPU

The QPU-ready Colab notebook is configured to run the hardware path automatically when the IBM credential exists.

Add this secret in Colab:

```text
IBM_QUANTUM_TOKEN
```

The notebook reads it with:

```python
from google.colab import userdata

token = userdata.get("IBM_QUANTUM_TOKEN")
print("IBM Quantum token loaded:", bool(token))
```

The QPU lane is enabled by default in the QPU-ready notebook.

No API token should ever be committed to the repository, printed to logs, placed in an issue, or pasted into public output.

Hardware evidence may include:

- backend name;
- IBM job ID;
- requested and returned shots;
- raw counts;
- source circuit SHA-256;
- transpiled ISA circuit SHA-256;
- QASM files;
- transpiled circuit depth and size;
- target QRTM observable;
- measured observable;
- residual;
- middleware event hash associated with the hardware measurement.

Local shot proxies and real hardware results are labeled differently and must not be conflated.

---

## Audit Ledgers

Wilson uses separate evidence chains.

### 1. Middleware Execution Ledger

Records execution facts such as:

- request/event ID;
- Tensor P2 sequence location;
- explicit QRTM observation;
- quantized QRTM value;
- admission/rejection;
- model-call state;
- model input/output hashes;
- P3 audit context;
- previous-row hash;
- current-row hash.

### 2. Ethics Checkpoint Ledger

Records:

- event ID;
- checkpoint type;
- P2 position;
- individual policy-rule result;
- policy version;
- policy SHA-256;
- decision;
- previous-row hash;
- current-row hash.

### 3. QPU Evidence Ledger

Records hardware or proxy evidence separately from the middleware execution record.

The QPU ledger attaches evidence to an existing middleware event; it does not rewrite that event.

### 4. Public Audit Join

A convenience view joins the ledgers for visualization.

The joined view is not the canonical source of truth. The separate ledgers and their hashes are.

---

## Independent Verification

The repository includes a standalone verifier:

```bash
python audit/verify_wilson_public_audit.py
```

The verifier can independently recompute:

- middleware hash-chain validity;
- ethics hash-chain validity;
- ethics-policy hash;
- QPU evidence-chain validity;
- audit receipt roots;
- artifact SHA-256 values.

The verifier is intentionally separate from the notebook.

---

## Colab Quick Start

1. Open the QPU-ready notebook from `colab/`.
2. Add `IBM_QUANTUM_TOKEN` to Colab Secrets.
3. Select a GPU runtime if running the real open model.
4. Run all cells.

The notebook is configured so the real-model and IBM-QPU lanes are enabled by default.

If a required external dependency or credential is missing, the notebook should fail visibly rather than silently substituting a real-hardware claim.

---

## Local Installation

Install the packaged wheel:

```bash
pip install dist/wilson_open_middleware-0.1.0-py3-none-any.whl
```

Or install from source:

```bash
pip install -e .
```

Run the tests:

```bash
pytest -q
```

---

## Repository Layout

```text
.
├── README.md
├── WILSON_OPEN_REFERENCE_LICENSE_v1.0.txt
├── GOVERNANCE.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── RELEASE_NOTES.md
├── CITATION.cff
├── pyproject.toml
├── wilson/
│   └── ... middleware package
├── colab/
│   └── ... public QPU-ready notebook
├── audit/
│   └── verify_wilson_public_audit.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ETHICS.md
│   ├── MODEL_ADAPTERS.md
│   ├── PUBLIC_REVIEW.md
│   ├── QPU.md
│   ├── QRTM.md
│   └── QTL_SPHERE_AUDIT.md
├── example_outputs/
│   └── ... reference ledgers, receipts, and figures
└── tests/
    └── ... public reference tests
```

---

## License

Wilson v0.1 is **source-available**.

It is **not** released under Apache-2.0, MIT, GPL, AGPL, or another standard OSI open-source license.

The governing license is:

```text
WILSON OPEN REFERENCE LICENSE v1.0
Source-Available / Patent Rights Reserved
```

The license grants limited copyright permissions for inspection, research, education, testing, evaluation, interoperability work, internal development, and compliant redistribution.

It does **not** grant patent rights.

Public availability of the source does not transfer ownership of Wilson, QTET, Tensor P2, Tensor P3, QRTM, QTL-Sphere, the Echo Meridian, related research, underlying inventions, patent applications, or associated patent rights.

Read the complete license before using or redistributing Wilson.

> The custom license is an authored licensing instrument and should be reviewed by qualified intellectual-property counsel before a public production release, especially where pending or planned patent filings may be affected.

---

## Governance

The reference release is civilian-first and intended for transparent, non-weaponized, non-surveillance use.

See `GOVERNANCE.md` for the project's stated governance principles.

---

## Third-Party Components

Wilson can interoperate with third-party:

- open-source AI models;
- Qiskit;
- IBM Quantum services;
- Python libraries;
- datasets and tooling.

Those components remain subject to their own licenses and terms.

This repository does not relicense third-party software.

---

## Public Review

Independent review, replication, criticism, falsification, security analysis, benchmarking, and interoperability testing are encouraged within the license terms.

Reviewers should clearly distinguish:

- Wilson from the underlying base model;
- canonical Tensor P2 from visualization scaffolding;
- QRTM input from inferred signals;
- model behavior from middleware behavior;
- proxy/simulator measurements from real IBM QPU results;
- P3/QTL-Sphere audit display from undisclosed canonical traversal rules;
- canonical ethics policy from reviewer-modified policies.

See:

```text
Wilson_Public_Review_Protocol.md
docs/PUBLIC_REVIEW.md
```

---

## Authorship and Citation

**Destiny Machwaya**  
Physicist, Principal Investigator, and Researcher  
Creator of Quantum Time-Energy Theory (QTET), QTL-Sphere, Tensor P2/P3, QRTM, and Wilson.

When citing the software, use the repository's `CITATION.cff` metadata and the tagged release/version being evaluated.

---

## Version

```text
Wilson v0.1
Open Reference Middleware
Source-Available / Patent Rights Reserved
```

The software is an early public reference implementation intended for inspection, reproducibility, testing, and research.

It should not be represented as safety-certified, production-certified, clinically validated, or suitable for safety-critical deployment without independent validation appropriate to that domain.
