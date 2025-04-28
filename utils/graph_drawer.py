from graphviz import Digraph
import json
import os

def draw_dfa(dfa, filename="afd", estado_resaltado=None, transicion_resaltada=None):
    dot = Digraph(comment="DFA", format="png", engine='dot')
    dot.attr(rankdir="LR")

    # Configurar el estilo de los nodos
    dot.attr('node', shape='circle', style='filled', fillcolor='white', 
             fontname='Arial', width='0.5', height='0.5')

    # Agregar estados
    for estado in dfa["transiciones"]:
        shape = "doublecircle" if estado in dfa["finales"] else "circle"
        # Determinar el color del estado
        if estado_resaltado and estado == estado_resaltado[0]:
            fillcolor = estado_resaltado[1]  # El color especificado
        else:
            fillcolor = "white"
        
        dot.node(estado, estado, shape=shape, style='filled', fillcolor=fillcolor)

    # Agregar estado inicial
    dot.node("inicio", "", shape="point")
    dot.edge("inicio", dfa["inicio"])

    # Agregar transiciones
    for origen, transiciones in dfa["transiciones"].items():
        for simbolo, destino in transiciones.items():
            # Determinar el color y grosor de la transición
            if (transicion_resaltada and 
                origen == transicion_resaltada[0] and 
                simbolo == transicion_resaltada[1]):
                # Transición resaltada
                color = "red"
                penwidth = "2.0"
            else:
                # Transición normal
                color = "black"
                penwidth = "1.0"
            
            dot.edge(origen, destino, 
                    label=simbolo, 
                    color=color, 
                    penwidth=penwidth)

    # Renderizar la imagen
    img_path = dot.render(filename, cleanup=True)
    
    return img_path