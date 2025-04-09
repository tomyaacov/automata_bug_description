from aalpy.utils import load_automaton_from_file, make_input_complete, save_automaton_to_file
from data.counter_examples import counter_examples_dict
from data.alphabet import alphabet
from aalpy.automata import DfaState, Dfa
from utils import minimize_dfa, get_intersection_dfa
import sys



for benchmark in ["m185"]:
    T = load_automaton_from_file(f'data/{benchmark}/T.dot', automaton_type='dfa')
    for s in T.states:
        s.is_accepting = True
        for a in list(s.transitions.keys()):
            if a not in alphabet[benchmark]:
                s.transitions.pop(a)
    T = minimize_dfa(T)
    save_automaton_to_file(T, f'data/{benchmark}/T1.dot', 'dot')
    word = counter_examples_dict[benchmark]["1"][0][1]
    word = list(set(word))

    print("A")
    sys.stdout.flush()
    states = [DfaState("")]
    states_dict = {"": states[0]}
    counter = 0
    while counter < len(states):
        for i, a in enumerate(word):
            if str(i) in states[counter].state_id:
                continue
            new_state_id = "".join(sorted(list(states[counter].state_id + str(i))))
            if new_state_id in states_dict:
                current_s = states_dict[new_state_id]
            else:
                current_s = DfaState(new_state_id)
                states.append(current_s)
                states_dict[new_state_id] = current_s
            states[counter].transitions[a] = current_s
            # states[counter].transitions[a] = DfaState(states[counter].state_id + str(i))
        counter += 1
    print("B")
    sys.stdout.flush()
    for s in states:
        if len(s.state_id) == len(word):
            s.is_accepting = True
        else:
            s.is_accepting = False

    initial_state = states[0]
    dfa = Dfa(initial_state, states)
    print("C")
    sys.stdout.flush()
    alphabet_t = T.get_input_alphabet()
    alphabet_dfa = dfa.get_input_alphabet()
    diff = list(set(alphabet_t) - set(alphabet_dfa))
    for a in diff:
        dfa.initial_state.transitions[a] = dfa.initial_state
    make_input_complete(dfa, missing_transition_go_to="self_loop")
    print("D")
    # print(len(dfa.states))
    # sys.stdout.flush()
    # dfa = minimize_dfa(dfa)
    # print(len(dfa.states))
    # print("E")
    sys.stdout.flush()
    dfa = get_intersection_dfa(dfa, T)
    print("F")
    sys.stdout.flush()
    save_automaton_to_file(dfa, f'data/{benchmark}/T2.dot', 'dot')


    # trigger_letters = diff
    # states = [DfaState("0"), DfaState("1")]
    # states[0].is_accepting = False
    # states[1].is_accepting = True
    # for a in alphabet_t:
    #     if a in trigger_letters:
    #         states[0].transitions[a] = states[1]
    #         states[1].transitions[a] = states[1]
    #     else:
    #         states[0].transitions[a] = states[0]
    #         states[1].transitions[a] = states[0]
    #
    # dfa2 = Dfa(states[0], states)
    # dfa2 = get_intersection_dfa(dfa2, T)
    # save_automaton_to_file(dfa2, f'data/{benchmark}/T3.dot', 'dot')



    T_assert = load_automaton_from_file(f'data/{benchmark}/T.dot', automaton_type='dfa')
    for s in T_assert.states:
        s.is_accepting = False
        for a in list(s.transitions.keys()):
            if a not in alphabet[benchmark]:
                s.transitions.pop(a)
    T_assert = minimize_dfa(T_assert)
    T_assert.states.append(DfaState("1"))
    T_assert.states[-1].is_accepting = True
    T_assert.states[0].transitions["assert"] = T_assert.states[-1]
    for a in list(T_assert.states[0].transitions.keys()):
        if a != "assert":
            T_assert.states[-1].transitions[a] = T_assert.states[0]
        else:
            T_assert.states[-1].transitions[a] = T_assert.states[-1]
    make_input_complete(T_assert, missing_transition_go_to="self_loop")
    save_automaton_to_file(T_assert, f'data/{benchmark}/T3.dot', 'dot')

    # states = [DfaState("")]
    # counter = 0
    # while counter < len(states):
    #     for i, a in enumerate(word):
    #         if str(i) in states[counter].state_id:
    #             continue
    #         states[counter].transitions[a] = DfaState(states[counter].state_id + str(i))
    #         states.append(states[counter].transitions[a])
    #     counter += 1
    #
    # for s in states:
    #     if len(s.state_id) == len(word):
    #         s.is_accepting = True
    #     else:
    #         s.is_accepting = False
    #
    # initial_state = states[0]
    # dfa = Dfa(initial_state, states)
    # make_input_complete(dfa, missing_transition_go_to="self_loop")
    # dfa.states.append(DfaState("sink"))
    # alphabet_t = T.get_input_alphabet()
    # alphabet_dfa = dfa.get_input_alphabet()
    # diff = list(set(alphabet_t) - set(alphabet_dfa))
    # for a in diff:
    #     dfa.initial_state.transitions[a] = dfa.states[-1]
    # make_input_complete(dfa, missing_transition_go_to="sink_state")
    # dfa = minimize_dfa(dfa)
    # dfa = get_intersection_dfa(dfa, T)
    # save_automaton_to_file(dfa, f'data/{benchmark}/T4.dot', 'dot')
    #
    # T_assert = load_automaton_from_file(f'data/{benchmark}/T.dot', automaton_type='dfa')
    # for s in T_assert.states:
    #     s.is_accepting = True
    #     for a in list(s.transitions.keys()):
    #         if a not in alphabet[benchmark]:
    #             s.transitions.pop(a)
    # T_assert = minimize_dfa(T_assert)
    # T_assert.states[0].transitions["assert"] = T_assert.states[0]
    # make_input_complete(T_assert, missing_transition_go_to="self_loop")
    # save_automaton_to_file(T_assert, f'data/{benchmark}/T5.dot', 'dot')


