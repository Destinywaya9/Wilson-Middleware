# Wilson Public Review Protocol

Wilson v0.1 is intended to be inspectable without trusting the author or the notebook UI.

## Review sequence

1. Read `wilson_middleware/policy/Wilson_Ethics_Policy.json`.
2. Run `python -m pytest -q` from the repository root.
3. Run `python audit/verify_wilson_public_audit.py example_outputs`.
4. Inspect the deterministic reference notebook and reference outputs.
5. For real model/QPU review, open `colab/Wilson_Public_Review_QPU_READY.ipynb` in a fresh Colab GPU runtime.
6. Store the IBM Quantum token only in Colab Secrets as `IBM_QUANTUM_TOKEN`.
7. Use Runtime → Run all. The real-model and QPU lanes are already enabled.
8. Preserve the executed notebook and complete `qtet_outputs/` directory.
9. Run the independent verifier against that hardware output directory.
10. Inspect raw IBM counts, circuit manifest, source QASM, transpiled ISA QASM, middleware ledger, ethics ledger, and public audit receipt.

## Required checks

A public review should verify that:

- Tensor P2 hash is unchanged;
- request ethics rejection prevents model invocation;
- every `0,0` has a mandatory ethics checkpoint;
- all `0,0` rows commit to the same policy SHA-256 recorded in the receipt;
- output ethics check occurs before emission;
- QRTM rejection is distinguishable from ethics rejection;
- QPU evidence references existing middleware row hashes;
- QPU results do not alter P2, QRTM, ethics decisions, or model output;
- middleware, ethics, and QPU ledgers independently verify;
- receipt artifact hashes match the actual files.
