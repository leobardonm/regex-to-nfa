from nfa_builder import construir_nfa, imprimir_nfa_legible
from utils.formatter import insertar_concatenaciones
from utils.postfix import convertir_a_postfija  # si ya lo tienes

# Paso 1: alfabeto y ER
alfabeto = ['a', 'b']
regex = "ab*"
regex_conc = insertar_concatenaciones(regex, alfabeto)  # → "a.b*"
postfija = convertir_a_postfija(regex_conc)              # → "ab*."

# Paso 2: construir NFA
nfa = construir_nfa(postfija, alfabeto)

# Paso 3: imprimir de forma legible
imprimir_nfa_legible(nfa)
