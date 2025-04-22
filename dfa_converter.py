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

    # Mapear conjuntos de estados del NFA a estados nombrados del DFA
    estado_dfa = {}
    transiciones_dfa = {}
    estados_dfa = []

    # Estado inicial del DFA = ε-cierre del estado inicial del NFA
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
            if not cierre:
                continue

            cierre_frozen = frozenset(cierre)
            if cierre_frozen not in estado_dfa:
                estado_dfa[cierre_frozen] = f"D{contador}"
                estados_dfa.append(cierre_frozen)
                queue.append(cierre_frozen)
                contador += 1

            transiciones_dfa[nombre_actual][simbolo] = estado_dfa[cierre_frozen]

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



def imprimir_dfa(dfa):
    print("\n=== AFD generado ===")
    print("Estado inicial:", dfa["inicio"])
    print("Estados de aceptación:", dfa["finales"])
    print("\nTransiciones:")

    for estado, transiciones in dfa["transiciones"].items():
        for simbolo, destino in transiciones.items():
            print(f"{estado} --{simbolo}--> {destino}")

            