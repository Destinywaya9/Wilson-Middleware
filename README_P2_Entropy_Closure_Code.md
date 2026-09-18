# Tensor P2 Entropy Closure — companion simulation code

**Author:** Destiny Machwaya  
**Affiliation:** Lei A While Research Center, Wahiawa, Hawaii, United States  
**Copyright © 2015–2026 Destiny Machwaya.**

Python companions to the manuscript draft *Tensor P2 Entropy Closure*.

These files are **not** the published hardware campaign:

Machwaya, D. (2026). Hardware demonstration of a fixed Tensor P2 kernel: zero-entropy leakage and stable coherence across dual microcontroller platforms. *Frontiers in Physics*. https://doi.org/10.3389/fphy.2026.1758206

Cite that paper for the dual-platform microcontroller result. Use this repository for the manuscript’s Von Neumann entropy simulations.

## Files

| File | Manuscript appendix | What it runs |
|---|---|---|
| `p2_entropy_depolarization_1_0.py` | Appendix A | Depolarization at `1,0` only, readout after final `0,0` |
| `p2_entropy_noise_sweep_1_0.py` | Appendix B | Six localized channels at `1,0`, same final readout |
| `requirements-p2-entropy.txt` | — | `numpy`, `pandas`, `matplotlib` |

Window used by both scripts:

`0,0 → 0,1 → 1,2 → 2,1 → 1,0 → 0,0`

Noise is applied only at `1,0`. Final `0,0` is the closure/reset readout.

## Run

```bash
pip install -r requirements-p2-entropy.txt
python p2_entropy_depolarization_1_0.py
python p2_entropy_noise_sweep_1_0.py
```

Outputs written to the working directory: CSV tables and PNG plots.

## Civilian-first

Public-benefit scientific use. Not for harm, coercion, surveillance, or weaponization.
