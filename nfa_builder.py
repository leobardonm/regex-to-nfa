class State:
    def __init__(self):
        self.transitions = {}  # símbolo -> lista de estados destino

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)


class NFA:
    def __init__(self, start_state, accept_state, states):
        self.start_state = start_state
        self.accept_state = accept_state
        self.states = states

    @staticmethod
    def from_symbol(symbol):
        start = State()
        end = State()
        start.add_transition(symbol, end)
        return NFA(start, end, {start, end})


def construir_nfa(postfix_expr, alfabeto):
    stack = []

    for char in postfix_expr:
        if char in alfabeto:
            stack.append(NFA.from_symbol(char))

        elif char == '*':
            nfa = stack.pop()
            start = State()
            end = State()
            start.add_transition('ε', nfa.start_state)
            start.add_transition('ε', end)
            nfa.accept_state.add_transition('ε', nfa.start_state)
            nfa.accept_state.add_transition('ε', end)

            nuevos_estados = nfa.states.union({start, end})
            stack.append(NFA(start, end, nuevos_estados))

        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept_state.add_transition('ε', nfa2.start_state)
            nuevos_estados = nfa1.states.union(nfa2.states)
            stack.append(NFA(nfa1.start_state, nfa2.accept_state, nuevos_estados))

        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            end = State()
            start.add_transition('ε', nfa1.start_state)
            start.add_transition('ε', nfa2.start_state)
            nfa1.accept_state.add_transition('ε', end)
            nfa2.accept_state.add_transition('ε', end)

            nuevos_estados = nfa1.states.union(nfa2.states).union({start, end})
            stack.append(NFA(start, end, nuevos_estados))

        else:
            raise ValueError(f"Símbolo no reconocido en postfija: {char}")

    if len(stack) != 1:
        raise ValueError("Expresión postfija inválida")

    return stack[0]