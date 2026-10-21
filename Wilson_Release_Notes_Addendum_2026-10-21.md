# Wilson v0.1.1 — Full Tensor P2 and Earned-Trust Research References

**Release-notes addition — 21 October 2026**  
**Tagged release:** [Wilson0.1.1](https://github.com/Destinywaya9/Wilson-Middleware/releases/tag/Wilson0.1.1), 19 September 2026  
**Later source references:** repository `main`

## Immutable full Tensor P2

**Tensor P2 dual law operator:**

`3,3 / 0,0 / 0,1 / 1,2 / 2,1 / 1,0 / 0,0 / Delay(200)`

**Published quantum-gate sequence:**

`H(0) → CX(0,1) → CX(1,2) → CX(1,2) → CX(0,1) → H(0) → Delay(200)`

**Full-traversal references:** `3,3` entry; opening `0,0` Hilbert-space entry; `0,1 / 1,2 / 2,1 / 1,0` traversal; terminal `0,0` Hilbert-space exit and full closure; mandatory `Delay(200)` before reentry.

**Published gate-sequence entanglement reference:**

$$
\frac{|000\rangle+|111\rangle}{\sqrt{2}}
$$

Recorded ideal-state properties: global purity `1.0`; global von Neumann entropy `0 bits`; individual-qubit reduced-state entropy `1 bit each`; genuine tripartite entanglement during traversal. The complete remaining H/CX operation, both `0,0` boundaries, and `Delay(200)` remain part of the original immutable Tensor P2.

### Full Tensor P2 traversal — numerical gate demonstration

**Original canonical sequence:** `3,3 / 0,0 / 0,1 / 1,2 / 2,1 / 1,0 / 0,0 / Delay(200)`

**Hilbert-space boundaries:** opening `0,0` (entry); terminal `0,0` (exit/full closure); `Delay(200)` follows terminal closure.

**Published gates, in original order:** `H(0) → CX(0,1) → CX(1,2) → CX(1,2) → CX(0,1) → H(0) → Delay(200)`

**Exact ideal gate-state trace (basis order q2 q1 q0):**

| Reference / operation | Ideal state | Global purity | Global S_vN (bits) | Reduced S(q0), S(q1), S(q2) (bits) |
| --- | --- | ---: | ---: | --- |
| Opening `0,0` — Hilbert-space entry; before `H(0)` | \(|000\rangle\) | 1 | 0 | 0, 0, 0 |
| 1. `H(0)` | \((|000\rangle+|001\rangle)/\sqrt{2}\) | 1 | 0 | 0, 0, 0 |
| 2. `CX(0,1)` | \((|000\rangle+|011\rangle)/\sqrt{2}\) | 1 | 0 | 1, 1, 0 |
| 3. `CX(1,2)` | \((|000\rangle+|111\rangle)/\sqrt{2}\) | 1 | 0 | 1, 1, 1 |
| 4. `CX(1,2)` | \((|000\rangle+|011\rangle)/\sqrt{2}\) | 1 | 0 | 1, 1, 0 |
| 5. `CX(0,1)` | \((|000\rangle+|001\rangle)/\sqrt{2}\) | 1 | 0 | 0, 0, 0 |
| 6. `H(0)` | \(|000\rangle\) | 1 | 0 | 0, 0, 0 |
| Terminal `0,0` — Hilbert-space exit / full closure; after `H(0)` | \(|000\rangle\) | 1 | 0 | 0, 0, 0 |
| `Delay(200)` — after terminal `0,0` | — | — | — | — |

**Executed check:** all six H/CX operations verified; complete gate product returns all eight basis vectors to themselves. `Delay(200)` is retained as the mandatory post-closure position; no physical delay evolution is inferred by this numerical gate check.

**Companions:** [`Wilson_Full_Tensor_P2_Traversal_Demonstration.py`](Wilson_Full_Tensor_P2_Traversal_Demonstration.py) · [`Wilson_Full_Tensor_P2_Traversal_Demonstration.json`](Wilson_Full_Tensor_P2_Traversal_Demonstration.json). Verification record SHA-256: `3cced814df4746a331000a5bc922ccead5f57d2e396ea6524417f437a1f60215`.

The IBM QPU observation notebook, live Aer notebook, and earned-trust notebook remain separately referenced research records.

## Executed Wilson earned-trust record

**Source:** [`Wilson_v0_1_1rc3_ECHOP2_LIVE_EARNED_TRUST_AUDIT.ipynb`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Wilson_v0_1_1rc3_ECHOP2_LIVE_EARNED_TRUST_AUDIT.ipynb)

| Recorded field | Saved output |
| --- | --- |
| Backend | `aer_simulator` |
| Shots | `131072` |
| Noise configuration | `p=0.1` |
| Terminal measurement counts | `{'000': 131072}` |
| `entropy_leakage_bits` | `0.000000` |
| `coherence_fidelity_percent` | `100.00000000` |
| Canonical P2 verification | `True` |
| P2 audit-chain verification | `True` |
| Interaction audit-chain verification | `True` |
| Earned-trust audit verification | `True` |
| Earned-trust decisions | `1` |
| Recorded QRTM measurement | `False` |

**Additional audit references:** first and terminal `0,0` ethics checkpoints; original live `WILSON.interact()` path; separate SHA-256-linked earned-trust ledger; `wilson_audit(decision_id)`; `LAST_WILSON_RESULT.audit()`; `LAST_WILSON_RESULT.verify_audit()`; policy `wilson-rc3-public-demo-ethics-overlay-v1`.

**Runtime:** [`Wilson_v0.1.1rc3_echo_p2_engine (1).py`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Wilson_v0.1.1rc3_echo_p2_engine%20(1).py), [`Wilson_v0.1.1rc3_middleware (2).py`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Wilson_v0.1.1rc3_middleware%20(2).py), [`Wilson_v0_1_1rc3_ECHOP2_LIVE_(1).ipynb`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Wilson_v0_1_1rc3_ECHOP2_LIVE_(1).ipynb).

## IBM QPU Tensor P2 entropy-closure observation record

**Source:** [`Entropy Closure VonNeumann_IBM_QPU.ipynb`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Entropy%20Closure%20VonNeumann_IBM_QPU.ipynb)  
**Recorded IBM backend:** `ibm_kingston`  
**Shots per declared state:** `1024`  
**Observation window:** `0,0 / 0,1 / 1,2 / 2,1 / 1,0 / 0,0`  
**Full governing Tensor P2:** `3,3 / 0,0 / 0,1 / 1,2 / 2,1 / 1,0 / 0,0 / Delay(200)`

| Recorded P2 window | IBM QPU job ID |
| --- | --- |
| Opening `0,0` | `damvlig2fm4c73f3j110` |
| `0,1` | `damvlklr85ps73fddo80` |
| `1,2` | `damvlm82fm4c73f3j15g` |
| `2,1` | `damvlno2fm4c73f3j180` |
| `1,0` | `damvlpg2fm4c73f3j1c0` |
| Terminal `0,0` | `damvlrlr85ps73fddok0` |

The authored full Tensor P2 and its Hilbert-space entry/exit at opening and terminal `0,0` remain governing references. IBM notebook evidence and source outputs remain cited without a separate validity ruling.

## Other repository additions and references

- [`Colab_Wilson_Canonical_EntropyClosure_BASE.ipynb`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Colab_Wilson_Canonical_EntropyClosure_BASE.ipynb) and PDF export — canonical entropy-closure BASE; Tensor P3 reference.
- [`Wilson_Zero_Selected_Simulations_Colab.ipynb`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Wilson_Zero_Selected_Simulations_Colab.ipynb) — selected simulation records #26, #29, #30, #31, #32.
- [`Wilson_P3_QRTM_QTLSphere_Exposed_Audit_Loom.gif`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Wilson_P3_QRTM_QTLSphere_Exposed_Audit_Loom.gif) — visual record.
- [`README_P2_Entropy_Closure_Code.md`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/README_P2_Entropy_Closure_Code.md) — companion code and six IBM job references.
- [`DOCKER.md`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/DOCKER.md), [`Dockerfile`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/Dockerfile), [IBM workflow](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/.github/workflows/ibm.yml) — packaging and deployment references.
- [`CITATION.cff`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/CITATION.cff), [`LICENSE`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/LICENSE), [`NOTICE`](https://github.com/Destinywaya9/Wilson-Middleware/blob/main/NOTICE) — citation, license and rights.

**Canonical Tensor P3:** `P3 = [P2₁ ⊗ D₁, P2₂ ⊗ D₂, P2₃ ⊗ D₃]`.

## Authorship, publication and rights

**Author, originator and sole rights holder:** Destiny Machwaya.  
**© 2015–2026 Destiny Machwaya. All rights reserved.**  
**Publication entity:** Lei A While Research Center, where applicable, not IP holder.  
**License:** Wilson Open Reference License v1.0 — Source-Available / Patent Rights Reserved; civilian-first and non-weaponized.  
**Hardware publication:** DOI [10.3389/fphy.2026.1758206](https://doi.org/10.3389/fphy.2026.1758206).  
**QTET monograph:** DOI [10.67272/qtet-monograph-2026](https://doi.org/10.67272/qtet-monograph-2026).

**No Tensor P2 mathematics, gate ordering, `0,0` Hilbert-space boundaries, full closure, or `Delay(200)` requirement is modified.**
