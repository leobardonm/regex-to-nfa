def leer_alfabeto():
    entrada = input("Introduce el alfabeto (símbolos separados por comas, ej. a,b,c): ")
    simbolos = entrada.replace(" ", "").split(",")
    
    if any(len(s) != 1 for s in simbolos):
        print("Error: cada símbolo debe ser un carácter.")
        return leer_alfabeto()
    
    return simbolos

def leer_expresion_regular(alfabeto):
    entrada = input("Introduce la expresión regular (usa . CONCATENACION , | UNION , * CERRADURA , paréntesis): ")
    operadores = set(['.', '|', '*', '(', ')'])
    simbolos_validos = set(alfabeto).union(operadores)
    # Verificar que los símbolos de la expresión regular sean válidos
    for c in entrada:
        if c not in simbolos_validos:
            print(f"Símbolo inválido: '{c}'")
            return leer_expresion_regular(alfabeto)
    
    return entrada
