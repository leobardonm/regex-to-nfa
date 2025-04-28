def convertir_a_postfija(expresion):
    """
    Convierte una expresión regular de notación infija a postfija usando el algoritmo Shunting Yard.
    
    La función maneja los siguientes operadores con sus respectivas precedencias:
    - '*' (Kleene star): precedencia 3
    - '.' (concatenación): precedencia 2
    - '|' (unión): precedencia 1
    - '(' y ')': paréntesis para agrupar
    
    Ejemplos:
        "a.b" -> "ab."
        "a|b" -> "ab|"
        "a*" -> "a*"
        "(a.b)*" -> "ab.*"
        "a.(b|c)" -> "abc|."
    
    Args:
        expresion (str): Expresión regular en notación infija con concatenaciones explícitas
        
    Returns:
        str: Expresión regular en notación postfija
        
    Raises:
        ValueError: Si hay paréntesis desbalanceados o un operador inválido
    """
    salida = []
    pila = []
    parentesis_count = 0

    # Definir precedencias de operadores
    precedencia = {
        '*': 3,  # Kleene tiene la mayor precedencia
        '.': 2,  # Concatenación es siguiente
        '|': 1   # Unión tiene la menor precedencia
    }

    for c in expresion:
        if c.isalnum():  # Símbolo del alfabeto
            salida.append(c)
        elif c == '(':
            pila.append(c)
            parentesis_count += 1
        elif c == ')':
            if parentesis_count <= 0:
                raise ValueError("Error: Paréntesis de cierre sin su correspondiente apertura")
            
            # Desapilar hasta encontrar el '('
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
                
            if not pila:
                raise ValueError("Error: Paréntesis desbalanceados")
                
            pila.pop()  # Quitar el '('
            parentesis_count -= 1
        elif c in precedencia:  # Operador
            # Desapilar operadores de mayor o igual precedencia
            while (pila and pila[-1] != '(' and 
                   precedencia.get(c, 0) <= precedencia.get(pila[-1], 0)):
                salida.append(pila.pop())
            pila.append(c)
        else:
            raise ValueError(f"Error: Operador no reconocido '{c}'")

    # Verificar paréntesis balanceados
    if parentesis_count > 0:
        raise ValueError("Error: Hay paréntesis sin cerrar")

    # Desapilar operadores restantes
    while pila:
        if pila[-1] == '(':
            raise ValueError("Error: Paréntesis desbalanceados")
        salida.append(pila.pop())

    return ''.join(salida)
