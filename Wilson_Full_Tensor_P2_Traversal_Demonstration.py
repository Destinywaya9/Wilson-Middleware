"""Exact ideal demonstration of the published Tensor P2 H/CX operation.

Research, mathematics, and rights: Destiny Machwaya.
Copyright (c) 2015-2026 Destiny Machwaya. All rights reserved.

This companion checks the six published gates, preserves both canonical 0,0
Hilbert-space boundary references, and retains the post-closure Delay(200).
It is a new numerical verification, not a new P2 operation or an IBM QPU run.
"""

from __future__ import annotations

import hashlib
import json
from math import log2, sqrt
from pathlib import Path

import numpy as np

P2 = ('3,3', '0,0', '0,1', '1,2', '2,1', '1,0', '0,0', 'Delay(200)')
GATES = ('H(0)', 'CX(0,1)', 'CX(1,2)', 'CX(1,2)', 'CX(0,1)', 'H(0)')
ALL_OPERATIONS = GATES + ('Delay(200)',)
DISPLAY = (
    '|000>',
    '(|000> + |001>)/sqrt(2)',
    '(|000> + |011>)/sqrt(2)',
    '(|000> + |111>)/sqrt(2)',
    '(|000> + |011>)/sqrt(2)',
    '(|000> + |001>)/sqrt(2)',
    '|000>',
)
EXPECTED_AMPLITUDES = (
    {0: 1.0},
    {0: 1/sqrt(2), 1: 1/sqrt(2)},
    {0: 1/sqrt(2), 3: 1/sqrt(2)},
    {0: 1/sqrt(2), 7: 1/sqrt(2)},
    {0: 1/sqrt(2), 3: 1/sqrt(2)},
    {0: 1/sqrt(2), 1: 1/sqrt(2)},
    {0: 1.0},
)
EXPECTED_Q_ENTROPIES = (
    (0, 0, 0),
    (0, 0, 0),
    (1, 1, 0),
    (1, 1, 1),
    (1, 1, 0),
    (0, 0, 0),
    (0, 0, 0),
)


def apply_h0(psi):
    output = np.zeros(8, dtype=complex)
    for x, value in enumerate(psi):
        b0 = x & 1
        output[x & ~1] += value / sqrt(2)
        output[(x & ~1) | 1] += value * (1 if b0 == 0 else -1) / sqrt(2)
    return output


def apply_cx(psi, control, target):
    output = np.zeros(8, dtype=complex)
    for x, value in enumerate(psi):
        y = x ^ (1 << target) if x & (1 << control) else x
        output[y] += value
    return output


def apply_gate(psi, gate):
    if gate == 'H(0)':
        return apply_h0(psi)
    if gate == 'CX(0,1)':
        return apply_cx(psi, 0, 1)
    if gate == 'CX(1,2)':
        return apply_cx(psi, 1, 2)
    raise ValueError(gate)


def density(psi):
    return np.outer(psi, np.conj(psi))


def entropy(rho):
    values = np.linalg.eigvalsh((rho + rho.conj().T) / 2).real
    values = np.clip(values, 0.0, 1.0)
    return 0.0 if abs(sum(-v*log2(v) for v in values if v > 1e-13)) < 1e-12 else float(sum(-v*log2(v) for v in values if v > 1e-13))


def reduced_density(psi, q):
    result = np.zeros((2, 2), dtype=complex)
    for x in range(8):
        for y in range(8):
            if ((x ^ y) & ~(1 << q)) == 0:
                result[(x >> q) & 1, (y >> q) & 1] += psi[x] * np.conj(psi[y])
    return result


def state_metrics(psi, step, expression, state):
    rho = density(psi)
    return dict(
        step=step,
        operation=expression,
        ideal_representation=state,
        global_purity=float(round(np.trace(rho @ rho).real, 12)),
        global_von_neumann_entropy_bits=entropy(rho),
        reduced_entropy_q0_bits=entropy(reduced_density(psi, 0)),
        reduced_entropy_q1_bits=entropy(reduced_density(psi, 1)),
        reduced_entropy_q2_bits=entropy(reduced_density(psi, 2)),
    )


def full_gate_unitary():
    outputs = []
    for index in range(8):
        psi = np.eye(8, dtype=complex)[:, index]
        for gate in GATES:
            psi = apply_gate(psi, gate)
        outputs.append(psi)
    return np.column_stack(outputs)


def verify():
    assert P2 == ('3,3', '0,0', '0,1', '1,2', '2,1', '1,0', '0,0', 'Delay(200)')
    assert GATES == ('H(0)', 'CX(0,1)', 'CX(1,2)', 'CX(1,2)', 'CX(0,1)', 'H(0)')
    psi = np.eye(8, dtype=complex)[:, 0]
    rows = [state_metrics(psi, 'opening 0,0', 'Hilbert-space entry reference / before H(0)', DISPLAY[0])]
    for index, gate in enumerate(GATES, 1):
        psi = apply_gate(psi, gate)
        expected = np.zeros(8, dtype=complex)
        for basis, amp in EXPECTED_AMPLITUDES[index].items():
            expected[basis] = amp
        assert np.allclose(psi, expected, atol=1e-12), ('state', index)
        row = state_metrics(psi, index, gate, DISPLAY[index])
        assert row['global_purity'] == 1.0
        assert row['global_von_neumann_entropy_bits'] == 0.0
        assert np.allclose(
            [row['reduced_entropy_q0_bits'], row['reduced_entropy_q1_bits'], row['reduced_entropy_q2_bits']],
            EXPECTED_Q_ENTROPIES[index], atol=1e-12,
        )
        rows.append(row)
    assert np.allclose(full_gate_unitary(), np.eye(8), atol=1e-12)
    rows.append(state_metrics(psi, 'terminal 0,0', 'Hilbert-space exit / full closure reference / after H(0)', '|000>'))
    # Delay is retained as an explicitly numbered canonical post-closure position;
    # this numerical check makes no assumption about physical delay-time evolution.
    record = {
        'research_author_and_rights_holder': 'Destiny Machwaya',
        'copyright': 'Copyright (c) 2015-2026 Destiny Machwaya. All rights reserved.',
        'record_kind': 'Ideal published H/CX numerical verification; not QPU hardware',
        'canonical_P2': ' / '.join(P2),
        'canonical_positions': list(P2),
        'hilbert_space_entry_reference': 'opening 0,0',
        'hilbert_space_exit_reference': 'terminal 0,0',
        'published_H_CX_gate_sequence': ' -> '.join(GATES),
        'post_closure': 'Delay(200)',
        'gate_trace': rows,
        'all_six_gates_evaluated': True,
        'gate_unitary_identity_check_all_eight_basis_vectors': True,
        'verification_assertions_passed': True,
    }
    payload = json.dumps(record, sort_keys=True, ensure_ascii=True, separators=(',', ':'))
    record['record_sha256'] = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    return record


if __name__ == '__main__':
    record = verify()
    print('FULL P2:', record['canonical_P2'])
    print('OPENING 0,0 — Hilbert-space entry')
    for row in record['gate_trace']:
        print(row['step'], row['operation'], row['ideal_representation'],
              'S_vN:', row['global_von_neumann_entropy_bits'],
              'S_q0/q1/q2:', row['reduced_entropy_q0_bits'],
              row['reduced_entropy_q1_bits'], row['reduced_entropy_q2_bits'])
    print('TERMINAL 0,0 — Hilbert-space exit/full closure')
    print('Delay(200) — mandatory after terminal 0,0')
    print('All 6 H/CX gates and all 8 basis vector returns verified.')
    print('Record SHA256:', record['record_sha256'])
    out = Path(__file__).with_suffix('.json')
    out.write_text(json.dumps(record, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    print('Saved:', out)
