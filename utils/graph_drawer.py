from graphviz import Digraph

def draw_dfa(dfa, filename="afd"):
    dot = Digraph(comment="DFA", format="png")
    dot.attr(rankdir="LR")

    for estado in dfa["transiciones"]:
        shape = "doublecircle" if estado in dfa["finales"] else "circle"
        dot.node(estado, shape=shape)

    dot.node("inicio", shape="point")
    dot.edge("inicio", dfa["inicio"])

    for origen, transiciones in dfa["transiciones"].items():
        for simbolo, destino in transiciones.items():
            dot.edge(origen, destino, label=simbolo)

    output_path = dot.render(filename, cleanup=True)
    return output_path