from aalpy.base import SUL


class SystemDCSULST(SUL):
    def __init__(self, T, system_sul):
        super().__init__()
        self.T = T
        self.system_sul = system_sul
        self.membership_queries = 0
        self.system_queries = 0
        self.label_mapper = {
            True: "+",
            False: "-",
            None: "?"
        }

    def query(self, word):
        self.T.reset_to_initial()
        m_labels = []
        b_labels = []
        if len(word) == 0:
            m_labels.append(self.T.initial_state.is_accepting)
            b_labels.append(False)
        else:
            for letter in word:
                m_labels.append(self.T.step(letter))
            if any(m_labels):
                last_true = len(m_labels) - 1 - m_labels[::-1].index(True)
                b_labels = list(self.system_sul.query(word[:last_true + 1])) + [False] * (len(word) - last_true - 1)
            else:
                b_labels = [False] * len(word)

        self.T.reset_to_initial()
        b_labels = [self.label_mapper[x] for x in b_labels]
        final = [in_b if in_m else "?" for in_m, in_b in zip(m_labels, b_labels)]
        return final

    def pre(self):
        self.system_sul.pre()
        self.T.reset_to_initial()

    def post(self):
        self.system_sul.post()
        self.T.reset_to_initial()

    def step(self, letter):
        t_out = self.T.step(letter)
        system_out = self.label_mapper[self.system_sul.step(letter)]
        if not t_out:
            return "?"
        return system_out


if __name__ == '__main__':
    from aalpy.utils import load_automaton_from_file
    from aalpy.base.SUL import CacheSUL
    from rers_sul_s_t import RERSSULST
    system_sul = CacheSUL(RERSSULST(benchmark="m199", t_type="3", for_T=False, is_prefix_closed=False, is_suffix_closed=False))
    T = load_automaton_from_file(f'data/m199/T3.dot', automaton_type='dfa')
    sul = SystemDCSULST(T, system_sul)
    word = ('ai1_ce2', 'usr2_ai2_re6', 'ai1_ce3', 'usr2_ai4_re2', 'assert', 'usr1_ai1_re1')
    print(sul.query(word))
    sul.pre()
    for c in word:
        print(sul.step(c))
    sul.post()
