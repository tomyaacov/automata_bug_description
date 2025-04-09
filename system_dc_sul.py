from aalpy.base import SUL


class SystemDCSUL(SUL):
    def __init__(self, M, system_sul):
        super().__init__()
        self.M = M
        self.system_sul = system_sul
        self.membership_queries = 0
        self.system_queries = 0

    def query(self, word: tuple) -> list:
        self.M.reset_to_initial()
        m_labels = []
        b_labels = []
        if len(word) == 0:
            m_labels.append(self.M.initial_state.is_accepting)
            b_labels.append(False)
        else:
            for letter in word:
                m_labels.append(self.M.step(letter))
            if any(m_labels):
                last_true = len(m_labels) - 1 - m_labels[::-1].index(True)
                # if last_true == len(word) - 2:  # TODO: fix bug after
                #     last_true += 1
                #     m_labels[last_true] = True
                b_labels = list(self.system_sul.query(word[:last_true + 1])) + [False] * (len(word) - last_true - 1)
            else:
                b_labels = [False] * len(word)

        self.M.reset_to_initial()
        b_labels = ["+" if x else "-" for x in b_labels]
        final = [in_b if in_m else "?" for in_m, in_b in zip(m_labels, b_labels)]
        return final

    def pre(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def step(self, letter):
        raise NotImplementedError