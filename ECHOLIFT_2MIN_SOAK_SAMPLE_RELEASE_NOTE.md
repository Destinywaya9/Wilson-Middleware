# EchoLift 2-Minute Soak — Public Inspection Sample

**Author:** Destiny Machwaya  
**Affiliation:** Lei A While Research Center, Wahiawā, Hawaiʻi  
**Copyright © 2015–2026 Destiny Machwaya. All rights reserved.**

This repository releases a **sample EchoLift soak sketch** so that Tensor P2 step order and the radiation-hardening / Z-conditioning path can be inspected and rerun.

It is **not** the hardware campaign published in:

> Machwaya, D. (2026). Hardware demonstration of a fixed Tensor P2 kernel: zero-entropy leakage and stable coherence across dual microcontroller platforms. *Frontiers in Physics*.  
> https://doi.org/10.3389/fphy.2026.1758206

Do not cite this sketch as that result. Do not treat its serial completion line as the paper’s 32-bit leakage measurement, dual-platform replication (RP2040 QCC Echo-Origin / ESP32-S3 EchoLift Harmony), video record, SHA-256 session hashes, or independent observation.

## What this file is

- An openly reproducible interrogation sample
- A readable Tensor P2 walk: `3,3 → 0 → 0,1 → 1,2 → 2,1 → 1,0 → Delay`
- EchoLift-style radiation conditioning: Gaussian Z error, periodic SEU kick, Z-banking, virtual \(R_z\)
- A 2-minute wall-clock soak loop

## What this file is not

- The published Frontiers run
- The sealed kernel internals used in that study
- A claim of 0.00% entropy leakage at device resolution
- A substitute for the 30-minute or 60-minute soaks

The journal article is the citable hardware demonstration. This release is a public inspection surface for P2 sequencing and radiation-hardening code.

## Suggested citation of the publication

Machwaya, D. (2026). Hardware demonstration of a fixed Tensor P2 kernel: zero-entropy leakage and stable coherence across dual microcontroller platforms. *Frontiers in Physics*. https://doi.org/10.3389/fphy.2026.1758206

## Suggested citation of this sample

Machwaya, D. (2026). EchoLift 2-minute soak — public inspection sample (Tensor P2 walk and radiation-hardening code). GitHub release. Inspection sample only; not the published hardware campaign.
