def epsilon_closure(states):
    """Calcula el ε-cierre de un conjunto de estados"""
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        for next_state in state.transitions.get('ε', []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure


def move(states, symbol):
    """Retorna el conjunto de estados alcanzables desde 'states' usando 'symbol'"""
    result = set()
    for state in states:
        for next_state in state.transitions.get(symbol, []):
            result.add(next_state)
    return result

def construir_dfa(nfa, alfabeto):
    from collections import deque

    estado_dfa = {}  # Mapea conjuntos de estados NFA -> nombre de estado DFA (D0, D1, etc.)
    transiciones_dfa = {}  # Transiciones del DFA
    estados_dfa = []  # Conjuntos de estados

    inicial = frozenset(epsilon_closure({nfa.start_state}))
    estado_dfa[inicial] = "D0"
    estados_dfa.append(inicial)
    queue = deque([inicial])
    contador = 1

    while queue:
        actual = queue.popleft()
        nombre_actual = estado_dfa[actual]
        transiciones_dfa[nombre_actual] = {}

        for simbolo in alfabeto:
            mov = move(actual, simbolo)
            cierre = epsilon_closure(mov)
            cierre_frozen = frozenset(cierre)

            if not cierre:
                transiciones_dfa[nombre_actual][simbolo] = "trampa"  # Ir a estado trampa
                continue

            if cierre_frozen not in estado_dfa:
                estado_dfa[cierre_frozen] = f"D{contador}"
                estados_dfa.append(cierre_frozen)
                queue.append(cierre_frozen)
                contador += 1

            transiciones_dfa[nombre_actual][simbolo] = estado_dfa[cierre_frozen]

    # Estado trampa 
    transiciones_dfa["trampa"] = {}
    for simbolo in alfabeto:
        transiciones_dfa["trampa"][simbolo] = "trampa"  # Loop sobre sí mismo

    # Identificar estados finales del DFA
    finales_dfa = []
    for estados in estados_dfa:
        if nfa.accept_state in estados:
            finales_dfa.append(estado_dfa[estados])

    return {
        "transiciones": transiciones_dfa,
        "inicio": "D0",
        "finales": finales_dfa
    }
