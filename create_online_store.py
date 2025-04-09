from aalpy.automata import DfaState, Dfa
from aalpy.utils import make_input_complete
from utils import get_intersection_dfa, minimize_dfa
def create_session_dfa(i, users, products):
    q0 = DfaState("q0")
    q1 = DfaState("q1")
    q2 = DfaState("q2")
    q3 = DfaState("q3", is_accepting=True)
    q4 = DfaState("q4", is_accepting=True)
    q0.transitions[f"S{i}"] = q1
    for u in range(users):
        q1.transitions[f"L{i}{u}"] = q2
    q2.transitions[f"O{i}"] = q1
    q3.transitions[f"O{i}"] = q1
    for p in range(products):
        q2.transitions[f"A{i}{p}"] = q2
        q3.transitions[f"A{i}{p}"] = q2
        q2.transitions[f"R{i}{p}"] = q3
        q3.transitions[f"R{i}{p}"] = q3
    q2.transitions[f"C{i}"] = q4
    q3.transitions[f"C{i}"] = q4
    return Dfa(q0, [q0, q1, q2, q3, q4])

def create_product_dfa(p, s, n):
    states = [DfaState(f"q{i}", is_accepting=True) for i in range(n+1)]
    for i in range(n):
        states[i].transitions[f"A{s}{p}"] = states[i+1]
        states[i+1].transitions[f"R{s}{p}"] = states[i]
    dfa = Dfa(states[0], states)
    make_input_complete(dfa, missing_transition_go_to="sink_state")
    return dfa

def create_t():
    A = create_session_dfa(0, 1, 1)

    make_input_complete(A, missing_transition_go_to="sink_state")
    B = create_product_dfa(0, 0, 2)
    diff = set(A.get_input_alphabet()) - set(B.get_input_alphabet())
    for a in diff:
        B.initial_state.transitions[a] = B.initial_state
    make_input_complete(B, missing_transition_go_to="self_loop")
    T = get_intersection_dfa(A, B)
    return T

def create_bug_example_1():
    q0 = DfaState("q0")
    q1 = DfaState("q1")
    q2 = DfaState("q2")
    q3 = DfaState("q3", is_accepting=True)
    q0.transitions["A00"] = q1
    q1.transitions["A00"] = q2
    q2.transitions["R00"] = q3
    dfa = Dfa(q0, [q0, q1, q2, q3])
    return dfa


T = create_t()
E = create_bug_example_1()
diff = set(T.get_input_alphabet()) - set(E.get_input_alphabet())
for a in diff:
    E.initial_state.transitions[a] = E.initial_state
make_input_complete(E, missing_transition_go_to="self_loop")

B = get_intersection_dfa(E, T)
B = minimize_dfa(B)

print(T)
print(B)
print(E)