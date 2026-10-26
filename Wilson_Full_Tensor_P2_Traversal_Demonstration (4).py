"""Full Tensor P2 quantum traversal, entanglement, and entropy closure.

Author, originator, and sole research rights holder: Destiny Machwaya.
Copyright (c) 2015-2026 Destiny Machwaya. All rights reserved.

Canonical Tensor P2:
    3,3 / 0,0 / 0,1 / 1,2 / 2,1 / 1,0 / 0,0 / Delay(200)

Author-supplied gates, in q0, q1, q2 order:
    0,0,0; 0,1,0; 1,2,0; 2,1,0; 1,0,0; 0,0,0
    Delay(200) follows the final 0,0,0.

Zero is folded infinity, folded total-state simultaneity, and the Echo
Meridian within the existing four-dimensional architecture. The opening
and final 0,0 are entry and return to that same folded total-state.
No finite state vector, binary string, or added coordinate defines zero.

The original supplied H/CX correspondence is retained as its own sourced
field. Author gate coordinates are never parsed into guessed CX arguments.
All six original H/CX factors are executed in their supplied order. The
finite Hilbert input is the |000> input already present in the supplied
companion. It is not a new preparation, an identification of 0_Q with a
binary ket, or a substitute for the authored zero or quantum circuit.
The P2 states and author gate triples remain explicit at every position;
finite Hilbert amplitudes and density matrices have their own fields.

The file calculates the quantum state before and after every supplied
operation, full and reduced density matrices and their spectra, global
purity, global von Neumann entropy, and individual-qubit reduced entropy.
The supplied tripartite-entanglement reference is checked against the
executed density-state trajectory. Terminal closure is the output of all
six operations. An additional exact operator calculation checks return
across the complete finite Hilbert space, beyond the source input alone.

No QPU job is submitted. No physical evolution during Delay(200) is
inferred; its mandatory post-closure position remains in the full trace.
Destiny Machwaya's original zero, 4D architecture, P2, and P3 are unchanged.
Python standard library only. Run this file to write its companion JSON.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import copysign, log2, sqrt
from pathlib import Path
from typing import NamedTuple


P2 = ('3,3', '0,0', '0,1', '1,2', '2,1', '1,0', '0,0', 'Delay(200)')
QUBIT_ORDER = ('q0', 'q1', 'q2')
GATES = ((0, 0, 0), (0, 1, 0), (1, 2, 0),
         (2, 1, 0), (1, 0, 0), (0, 0, 0))
DELAY = 200

# Original supplied gate sequence; no gate is inferred from a P2 coordinate.
SOURCE_H_CX_GATES = ('H(0)', 'CX(0,1)', 'CX(1,2)',
                     'CX(1,2)', 'CX(0,1)', 'H(0)')
SOURCE_FILE_SHA256 = 'b249539738dac3eef9da18778bd5fa119a96353a0e51667089d5cee634dfbd9a'
SOURCE_RECORD_SHA256 = '3cced814df4746a331000a5bc922ccead5f57d2e396ea6524417f437a1f60215'

# The supplied companion's finite Hilbert input, in q0,q1,q2 basis order.
# This is not a definition or finite replacement for folded zero.
SOURCE_HILBERT_INPUT = (1, 0, 0, 0, 0, 0, 0, 0)
BASIS_LABELS_Q0_Q1_Q2 = tuple(f'{index:03b}' for index in range(8))
SOURCE_EXPECTED_REDUCED_ENTROPIES = (
    (0, 0, 0), (0, 0, 0), (1, 1, 0), (1, 1, 1),
    (1, 1, 0), (0, 0, 0), (0, 0, 0),
)


FOLDED_ZERO_FORMS = (
    '0 = folded infinity = folded total-state simultaneity',
    r'0_N = 0 + \sum_{n=1}^{N}(n + (-n)) = 0',
    r'0_Q = \lim_{N\to\infty}[0 + \sum_{n=1}^{N}(n + (-n))]',
    '0_Q != empty set; 0_Q != absence',
    '0_Q = {..., -3, -2, -1, 0, 1, 2, 3, ...}^{parallel}',
    'parallel = simultaneous lawful coexistence, not sequence or ordinary addition',
    'pi_n(0_Q) = n; rho(n) = 0_Q; rho(pi_n(0_Q)) = 0_Q',
)


def validate_definition(p2, gates, qubit_order, delay, source_operations):
    """Require the exact authored order and original supplied correspondence."""
    expected_p2 = ('3,3', '0,0', '0,1', '1,2', '2,1', '1,0', '0,0', 'Delay(200)')
    expected_gates = ((0, 0, 0), (0, 1, 0), (1, 2, 0),
                      (2, 1, 0), (1, 0, 0), (0, 0, 0))
    expected_operations = ('H(0)', 'CX(0,1)', 'CX(1,2)',
                           'CX(1,2)', 'CX(0,1)', 'H(0)')
    if tuple(p2) != expected_p2:
        raise ValueError('The full canonical Tensor P2 order has been altered.')
    if tuple(qubit_order) != ('q0', 'q1', 'q2'):
        raise ValueError('Author gate coordinates must remain in q0, q1, q2 order.')
    if (len(gates) != 6 or any(len(gate) != 3 for gate in gates)
            or any(type(value) is not int for gate in gates for value in gate)
            or tuple(tuple(gate) for gate in gates) != expected_gates):
        raise ValueError('The six authored gate triples have been altered.')
    if type(delay) is not int or delay != 200:
        raise ValueError('Mandatory Delay(200) must follow terminal closure.')
    if tuple(source_operations) != expected_operations:
        raise ValueError('The original supplied H/CX correspondence has been altered.')
    if tuple(f'{gate[0]},{gate[1]}' for gate in gates) != tuple(p2[1:-1]):
        raise ValueError('Gate references no longer follow the internal P2 traversal.')
    return True


def identity_matrix(scale=1):
    return tuple(tuple(scale if row == col else 0 for col in range(8))
                 for row in range(8))


def multiply(left, right):
    return tuple(tuple(sum(left[row][k] * right[k][col] for k in range(8))
                       for col in range(8)) for row in range(8))


def transpose(matrix):
    return tuple(tuple(matrix[col][row] for col in range(8)) for row in range(8))


class ExactOperator(NamedTuple):
    """An operator numerator / sqrt(2)**denominator_power."""
    numerator: tuple
    denominator_power: int

    def after(self, earlier):
        return ExactOperator(multiply(self.numerator, earlier.numerator),
                             self.denominator_power + earlier.denominator_power)

    def is_unitary(self):
        return (multiply(transpose(self.numerator), self.numerator)
                == identity_matrix(2 ** self.denominator_power))

    def is_identity(self):
        power = self.denominator_power
        return power % 2 == 0 and self.numerator == identity_matrix(2 ** (power // 2))

    def as_record(self):
        return {'integer_numerator': [list(row) for row in self.numerator],
                'denominator': f'sqrt(2)**{self.denominator_power}',
                'denominator_power': self.denominator_power,
                'basis_order': list(QUBIT_ORDER)}


def permutation_matrix(destinations):
    return tuple(tuple(int(row == destinations[col]) for col in range(8))
                 for row in range(8))


def source_operator(operation):
    """Exact matrices of the supplied H/CX realization, in q0,q1,q2 order.

    These matrices encode those sourced operations. They do not encode 0_Q
    or convert the author's gate-coordinate values into binary states.
    """
    if operation == 'H(0)':
        numerator = tuple(tuple(
            0 if row % 4 != col % 4 else (-1 if row >= 4 and col >= 4 else 1)
            for col in range(8)) for row in range(8))
        return ExactOperator(numerator, 1)
    if operation == 'CX(0,1)':
        return ExactOperator(permutation_matrix((0, 1, 2, 3, 6, 7, 4, 5)), 0)
    if operation == 'CX(1,2)':
        return ExactOperator(permutation_matrix((0, 1, 3, 2, 4, 5, 7, 6)), 0)
    raise ValueError(f'Operation is not in the original supplied realization: {operation}')


class ExactHilbertState(NamedTuple):
    """Exact amplitudes of the supplied finite Hilbert realization."""
    numerator: tuple
    denominator_power: int

    def evolved_by(self, operator):
        numerator = tuple(sum(operator.numerator[row][col] * self.numerator[col]
                              for col in range(8)) for row in range(8))
        return ExactHilbertState(numerator,
                                 self.denominator_power + operator.denominator_power)

    def density_numerator(self):
        return tuple(tuple(left * right for right in self.numerator)
                     for left in self.numerator)

    def equals(self, other):
        """Compare real amplitudes exactly, including the retained phase/sign."""
        difference = self.denominator_power - other.denominator_power
        if difference % 2:
            return False
        if difference >= 0:
            return self.numerator == tuple(value * 2 ** (difference // 2)
                                           for value in other.numerator)
        return other.equals(self)

    def as_record(self):
        return {'integer_numerators': list(self.numerator),
                'denominator': f'sqrt(2)**{self.denominator_power}',
                'denominator_power': self.denominator_power,
                'basis_order': list(QUBIT_ORDER),
                'basis_labels_q0_q1_q2': list(BASIS_LABELS_Q0_Q1_Q2)}


def spectrum(matrix, tolerance=1e-14):
    """Eigenvalues of the small real symmetric source density matrices.

    Jacobi diagonalization supplies the spectra actually used by entropy().
    Exact integer/rational density matrices are retained separately.
    """
    size = len(matrix)
    values = [[float(value) for value in row] for row in matrix]
    for _ in range(100 * size * size):
        off_diagonal, row, col = max(
            (abs(values[i][j]), i, j) for i in range(size) for j in range(i + 1, size))
        if off_diagonal <= tolerance:
            result = sorted(values[i][i] for i in range(size))
            if any(value < -1e-12 or value > 1 + 1e-12 for value in result):
                raise ArithmeticError('Computed density spectrum is outside [0,1].')
            return tuple(0.0 if abs(value) < tolerance else
                         1.0 if abs(value - 1) < tolerance else value for value in result)
        cross = values[row][col]
        tau = (values[col][col] - values[row][row]) / (2 * cross)
        tangent = copysign(1.0, tau) / (abs(tau) + sqrt(1 + tau * tau))
        cosine = 1 / sqrt(1 + tangent * tangent)
        sine = tangent * cosine
        values[row][row] -= tangent * cross
        values[col][col] += tangent * cross
        values[row][col] = values[col][row] = 0.0
        for index in range(size):
            if index not in (row, col):
                left, right = values[index][row], values[index][col]
                values[index][row] = values[row][index] = cosine * left - sine * right
                values[index][col] = values[col][index] = sine * left + cosine * right
    raise ArithmeticError('Density eigensolver did not converge.')


def entropy(eigenvalues):
    result = -sum(value * log2(value) for value in eigenvalues if value > 1e-13)
    return 0.0 if abs(result) < 1e-12 else float(result)


def rational_matrix_record(numerator, denominator):
    return {'integer_numerator': [list(row) for row in numerator],
            'integer_denominator': denominator}


def quantum_snapshot(state):
    """Calculate density-state and entanglement observables from amplitudes."""
    numerator = state.density_numerator()
    denominator = 2 ** state.denominator_power
    density = tuple(tuple(Fraction(value, denominator) for value in row)
                    for row in numerator)
    trace = sum(density[index][index] for index in range(8))
    purity = sum(density[i][j] * density[j][i] for i in range(8) for j in range(8))
    eigenvalues = spectrum(density)
    reduced_records, reduced_entropies, ranks = {}, [], []
    for index, qubit in enumerate(QUBIT_ORDER):
        mask = 1 << (2 - index)
        reduced = [[0, 0], [0, 0]]
        for left in range(8):
            for right in range(8):
                if ((left ^ right) & ~mask) == 0:
                    reduced[int(bool(left & mask))][int(bool(right & mask))] += numerator[left][right]
        reduced_values = tuple(tuple(Fraction(value, denominator) for value in row)
                               for row in reduced)
        reduced_spectrum = spectrum(reduced_values)
        reduced_entropy = entropy(reduced_spectrum)
        reduced_entropies.append(reduced_entropy)
        ranks.append(sum(value > 1e-12 for value in reduced_spectrum))
        reduced_records[qubit] = {
            'density_matrix_exact': rational_matrix_record(reduced, denominator),
            'density_eigenvalues': list(reduced_spectrum),
            'von_neumann_entropy_bits': reduced_entropy,
            'density_rank': ranks[-1],
        }
    projector_verified = multiply(numerator, numerator) == tuple(
        tuple(denominator * value for value in row) for row in numerator)
    # In the supplied pure three-qubit trajectory, rank 2 across every
    # one-qubit/complement partition verifies the recorded tripartite property.
    tripartite = projector_verified and trace == 1 and all(rank == 2 for rank in ranks)
    return {
        'amplitudes_exact': state.as_record(),
        'global_density_matrix_exact': rational_matrix_record(numerator, denominator),
        'trace': float(trace),
        'global_purity': float(purity),
        'global_density_eigenvalues': list(eigenvalues),
        'global_von_neumann_entropy_bits': entropy(eigenvalues),
        'reduced_entropy_q0_q1_q2_bits': reduced_entropies,
        'reduced_states': reduced_records,
        'exact_normalization_verified': trace == 1,
        'exact_pure_density_projector_verified': projector_verified,
        'genuine_tripartite_entanglement': tripartite,
    }


def validate_trace(rows):
    if len(rows) != 8 or [row['position'] for row in rows] != list(range(1, 9)):
        raise ValueError('The complete trace must retain all eight ordered positions.')
    internal = rows[1:-1]
    validate_definition(
        [row['p2_reference'] for row in rows],
        [row['gate_q0_q1_q2'] for row in internal],
        QUBIT_ORDER, rows[-1].get('delay'),
        [row['source_H_CX_operation'] for row in internal],
    )
    if rows[0].get('stage') != 'bounded triadic entry':
        raise ValueError('The 3,3 entry has been omitted or replaced.')
    if (rows[1].get('boundary') != 'Hilbert-space entry'
            or rows[-2].get('boundary') != 'Hilbert-space exit / full closure'):
        raise ValueError('Both 0,0 Hilbert-space boundaries must remain explicit.')
    if rows[-1].get('stage') != 'mandatory post-closure Delay(200)':
        raise ValueError('Delay(200) must remain after the terminal 0,0.')
    if any('quantum_before' not in row or 'quantum_after' not in row for row in internal):
        raise ValueError('Every supplied operation requires executed before/after quantum data.')
    return True


def verify():
    definition_verified = validate_definition(P2, GATES, QUBIT_ORDER, DELAY, SOURCE_H_CX_GATES)
    rows = [{'position': 1, 'p2_reference': '3,3', 'gate_q0_q1_q2': None,
             'stage': 'bounded triadic entry'}]
    cumulative = ExactOperator(identity_matrix(), 0)
    initial_state = ExactHilbertState(SOURCE_HILBERT_INPUT, 0)
    quantum_state = initial_state
    initial_snapshot = quantum_snapshot(initial_state)
    snapshots = [initial_snapshot]
    evolved_states = [initial_state]
    prefix_checks = []
    executed = []
    roles = ('folded total-state reference after entry', 'differentiated traversal',
             'relational transition', 'inversion-paired transition',
             'return-directed traversal', 'return to folded total-state reference')
    for index, (reference, coordinates, operation, role) in enumerate(
            zip(P2[1:-1], GATES, SOURCE_H_CX_GATES, roles), 2):
        operator = source_operator(operation)
        before = cumulative
        quantum_before = snapshots[-1]
        quantum_state = quantum_state.evolved_by(operator)
        evolved_states.append(quantum_state)
        quantum_after = quantum_snapshot(quantum_state)
        snapshots.append(quantum_after)
        cumulative = operator.after(cumulative)
        unitary = cumulative.is_unitary()
        if not unitary:
            raise ArithmeticError(f'Exact operator verification failed at P2 position {index}.')
        row = {'position': index, 'p2_reference': reference,
               'gate_q0_q1_q2': list(coordinates), 'stage': role,
               'source_H_CX_operation': operation,
               'operator_before': before.as_record(),
               'operator_after': cumulative.as_record(),
               'quantum_before': quantum_before,
               'quantum_after': quantum_after,
               'exact_prefix_unitarity_verified': unitary}
        if index == 2:
            row.update(boundary='Hilbert-space entry', folded_reference='0_Q')
        elif index == 7:
            row.update(boundary='Hilbert-space exit / full closure', folded_reference='0_Q')
        rows.append(row)
        executed.append(operation)
        prefix_checks.append(unitary)
    rows.append({'position': 8, 'p2_reference': 'Delay(200)', 'gate_q0_q1_q2': None,
                 'stage': 'mandatory post-closure Delay(200)', 'delay': DELAY})
    trace_verified = validate_trace(rows)
    closed_return = cumulative.is_identity()
    if not closed_return:
        raise ArithmeticError('The complete original supplied H/CX operator did not close exactly.')
    state_return = quantum_state.equals(initial_state)
    entropies_verified = all(
        all(abs(actual - expected) < 1e-12 for actual, expected in zip(
            snapshot['reduced_entropy_q0_q1_q2_bits'], expected_entropies))
        for snapshot, expected_entropies in zip(snapshots, SOURCE_EXPECTED_REDUCED_ENTROPIES))
    ghz = ExactHilbertState((1, 0, 0, 0, 0, 0, 0, 1), 1)
    ghz_verified = (evolved_states[3].equals(ghz)
                    and rows[3]['quantum_after']['genuine_tripartite_entanglement'])
    global_metrics_verified = all(
        snapshot['exact_normalization_verified']
        and snapshot['exact_pure_density_projector_verified']
        and abs(snapshot['global_purity'] - 1.0) < 1e-12
        and snapshot['global_von_neumann_entropy_bits'] == 0.0
        for snapshot in snapshots)
    checks = {'full_P2_and_author_gate_coordinates_preserved': definition_verified,
              'generated_trace_preserves_all_eight_positions': trace_verified,
              'all_six_source_operations_retained_in_order': tuple(executed) == SOURCE_H_CX_GATES,
              'all_six_operator_prefixes_unitary_exactly': all(prefix_checks),
              'complete_opening_to_final_operator_is_identity_exactly': closed_return,
              'full_source_quantum_trajectory_executed': len(snapshots) == 7,
              'computed_full_and_reduced_density_at_each_boundary_and_operation':
                  all('reduced_states' in snapshot for snapshot in snapshots),
              'computed_global_purity_and_entropy_match_supplied_trajectory': global_metrics_verified,
              'computed_reduced_entropies_match_supplied_trajectory': entropies_verified,
              'source_tripartite_entanglement_reference_verified_from_evolution': ghz_verified,
              'terminal_source_amplitudes_return_exactly_without_reassignment': state_return}
    if not all(checks.values()):
        raise ArithmeticError('Full quantum traversal check failed: ' +
                              ', '.join(name for name, passed in checks.items() if not passed))
    record = {
        'research_author_originator_and_sole_rights_holder': 'Destiny Machwaya',
        'copyright': 'Copyright (c) 2015-2026 Destiny Machwaya. All rights reserved.',
        'record_kind': 'Executed full source Hilbert-state, density, entanglement, and entropy traversal',
        'canonical_P2': ' / '.join(P2),
        'qubit_order': list(QUBIT_ORDER),
        'author_gate_sequence_q0_q1_q2': [list(gate) for gate in GATES],
        'hilbert_space_interval': 'opening 0,0 through final 0,0, including both boundaries',
        'folded_zero': {'canonical_forms': list(FOLDED_ZERO_FORMS),
                        'shared_reference_identity': 'M_E == 0_Q; 0 == M_E',
                        'architectural_dimension': 4,
                        'directional_indexing': 'T_i = I_res(0,D_i), i=1,...,12',
                        'initial_reference': '0_Q', 'terminal_reference': '0_Q',
                        'provenance': 'The author definition is unchanged; assistant representations were repaired.'},
        'canonical_P3': 'P3 = [P2_1 tensor D_1, P2_2 tensor D_2, P2_3 tensor D_3]',
        'traversal_trace': rows,
        'source_Hilbert_entry': {
            'source': 'The |000> finite Hilbert input in the originally supplied companion',
            'basis_order': list(QUBIT_ORDER),
            'snapshot': initial_snapshot,
            'relationship_to_canonical_zero':
                'A source finite Hilbert input; the authored folded total-state definition is unchanged.'},
        'quantum_traversal': {
            'executed_operation_count': len(executed),
            'evaluated_snapshots': len(snapshots),
            'metrics_computed_this_run': True,
            'source_reference': '(|000> + |111>)/sqrt(2)',
            'source_reference_P2_position': 4,
            'source_reference_P2_state': '1,2',
            'terminal_snapshot': snapshots[-1],
            'terminal_amplitudes_equal_source_entry_exactly': state_return,
            'terminal_density_comes_from': 'Sequential execution of every supplied operation',
            'physical_QPU_run': False,
            'noise_channel_applied': False},
        'operator_audit': {'source_H_CX_sequence': list(SOURCE_H_CX_GATES),
                           'input_independent': True,
                           'method': 'Exact integer operator multiplication with explicit sqrt(2) factors',
                           'complete_operator': cumulative.as_record(),
                           'full_Hilbert_space_return_verified_exactly': closed_return,
                           'scope': 'The complete originally supplied H/CX realization; no gate factors removed.'},
        'preserved_source_entanglement_record': {
            'reference': '(|000> + |111>)/sqrt(2)',
            'global_purity': 1.0, 'global_von_neumann_entropy_bits': 0.0,
            'reduced_entropy_q0_q1_q2_bits': [1.0, 1.0, 1.0],
            'recorded_property': 'Genuine tripartite entanglement during traversal',
            'provenance': 'Supplied research result; also verified by the quantum evolution in this run.',
            'verified_from_evolved_quantum_state_this_run': ghz_verified},
        'post_closure': {'required': True, 'operation': 'Delay(200)', 'value': DELAY,
                         'placement': 'after final 0,0,0 and before reentry',
                         'physical_delay_evolution_simulated': False},
        'sources': {'monograph_DOI': '10.67272/qtet-monograph-2026',
                    'axiomatic_work': 'Axiomatic Folded-State Recurrence, Triadic Closure, and Invariant Dimensional Embedding',
                    'gate_coordinates': 'Author-supplied q0,q1,q2 sequence in this session',
                    'H_CX_correspondence': 'Original supplied Wilson release record and source companion',
                    'original_companion_source_sha256': SOURCE_FILE_SHA256,
                    'original_verification_record_sha256': SOURCE_RECORD_SHA256},
        'checks': checks,
        'verification_assertions_passed': all(checks.values()),
        'new_QPU_execution': False,
    }
    payload = json.dumps(record, sort_keys=True, ensure_ascii=True, separators=(',', ':'))
    record['record_sha256'] = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    return record


def main():
    record = verify()
    print('FULL P2:', record['canonical_P2'])
    print('Gate coordinate order: q0, q1, q2')
    print('Zero: folded infinity / folded total-state simultaneity / Echo Meridian within 4D')
    print('Finite Hilbert input: the |000> input already present in the supplied companion')
    for row in record['traversal_trace']:
        coordinates = row['gate_q0_q1_q2']
        gate_text = ','.join(map(str, coordinates)) if coordinates is not None else '-'
        print(row['position'], '| P2:', row['p2_reference'], '| Gate:', gate_text,
              '|', row['stage'])
        if 'quantum_after' in row:
            for label, key in (('before', 'quantum_before'), ('after', 'quantum_after')):
                quantum = row[key]
                print('   ', label, row['source_H_CX_operation'],
                      '| purity:', quantum['global_purity'],
                      '| global S_vN:', quantum['global_von_neumann_entropy_bits'],
                      '| S(q0,q1,q2):', quantum['reduced_entropy_q0_q1_q2_bits'])
    print('Original supplied H/CX correspondence:', ' -> '.join(SOURCE_H_CX_GATES))
    print('Complete opening-to-final 0,0 operator return: VERIFIED EXACTLY')
    print('All eight canonical positions and all six author gate triples: VERIFIED')
    print('Quantum amplitudes, density matrices, spectra, purity, and entropies: CALCULATED')
    print('Supplied tripartite-entanglement reference: VERIFIED FROM EVOLUTION')
    print('Terminal amplitudes return exactly after all six supplied operations: VERIFIED')
    print('Mandatory Delay(200): after final 0,0,0 and before reentry')
    print('Source entanglement reference:', record['preserved_source_entanglement_record']['reference'])
    print('Record SHA256:', record['record_sha256'])
    output = Path(__file__).with_suffix('.json')
    output.write_text(json.dumps(record, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    print('Saved:', output.name)


if __name__ == '__main__':
    main()
