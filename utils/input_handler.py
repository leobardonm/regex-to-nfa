def leer_alfabeto():
    entrada = input("Introduce el alfabeto (símbolos separados por comas, ej. a,b,c): ")
    simbolos = entrada.replace(" ", "").split(",")
    
    if any(len(s) != 1 for s in simbolos):
        print("Error: cada símbolo debe ser un carácter.")
        return leer_alfabeto()
    
    return simbolos

def leer_expresion_regular(alfabeto):
    entrada = input("Introduce la expresión regular (usa ., |, *, paréntesis): ")
    entrada = entrada.replace(" ", "")  # Elimina espacios si los hay
    
    operadores = set(['.', '|', '*', '(', ')'])
    simbolos_validos = set(alfabeto).union(operadores)

    for c in entrada:
        if c not in simbolos_validos:
            print(f"Símbolo inválido: '{c}' (usa solo '*' ASCII, no ∗ matemático)")
            return leer_expresion_regular(alfabeto)
    
    return entrada



print(leer_expresion_regular(leer_alfabeto()))