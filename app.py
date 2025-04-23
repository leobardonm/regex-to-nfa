from utils.input_handler import leer_alfabeto, leer_expresion_regular
from utils.formatter import insertar_concatenaciones
from utils.postfix import convertir_a_postfija
from nfa_builder import construir_nfa
from dfa_converter import construir_dfa
from simular_dfa import simular_dfa
from utils.graph_drawer import draw_dfa
from gui.simulador_dfa_gui import mostrar_interfaz_dfa

def imprimir_nfa_legible(nfa):
    state_names = {state: f"S{i}" for i, state in enumerate(nfa.states)}

    print("\n=== NFA generado ===")
    for state in nfa.states:
        origen = state_names[state]
        for simbolo, destinos in state.transitions.items():
            for destino in destinos:
                destino_nombre = state_names[destino]
                print(f"{origen} --{simbolo}--> {destino_nombre}")

    print(f"\nEstado inicial: {state_names[nfa.start_state]}")
    print(f"Estado de aceptación: {state_names[nfa.accept_state]}")


def imprimir_dfa(dfa):
    print("\n=== AFD generado ===")
    print("Estado inicial:", dfa["inicio"])
    print("Estados de aceptación:", dfa["finales"])
    print("\nTransiciones:")
    for estado, transiciones in dfa["transiciones"].items():
        for simbolo, destino in transiciones.items():
            print(f"{estado} --{simbolo}--> {destino}")


# TODO: asegurar que solo se ejecuta si este archivo es el principal
if __name__ == "__main__":
    print("=== Conversor de ER a AFD ===")
    alfabeto = leer_alfabeto()
    er = leer_expresion_regular(alfabeto)

    er_concatenada = insertar_concatenaciones(er, alfabeto)
    postfija = convertir_a_postfija(er_concatenada)

    print("\nExpresión con concatenaciones explícitas:", er_concatenada)
    print("Expresión en postfija:", postfija)

    nfa = construir_nfa(postfija, alfabeto)
    imprimir_nfa_legible(nfa)

    dfa = construir_dfa(nfa, alfabeto)
    imprimir_dfa(dfa)

    palabra = input("\nIntroduce una palabra para simular: ")
    simular_dfa(dfa, palabra)
    draw_dfa(dfa, "afd")
    mostrar_interfaz_dfa(dfa)

