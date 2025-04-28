def insertar_concatenaciones(expr, alfabeto):
    """
    Inserta el operador de concatenación '.' explícitamente en una expresión regular.
    
    Se inserta '.' en los siguientes casos:
    - Entre dos símbolos del alfabeto: 'ab' -> 'a.b'
    - Entre símbolo y paréntesis abierto: 'a(b' -> 'a.(b'
    - Entre paréntesis cerrado y símbolo: ')a' -> ').a'
    - Entre paréntesis cerrado y abierto: ')(' -> ').('
    - Entre asterisco y símbolo: '*a' -> '*.a'
    - Entre asterisco y paréntesis abierto: '*(' -> '*.('
    
    Args:
        expr (str): Expresión regular sin concatenaciones explícitas
        alfabeto (list): Lista de símbolos válidos del alfabeto
        
    Returns:
        str: Expresión regular con concatenaciones explícitas
    """
    resultado = ""
    
    for i in range(len(expr)):
        c1 = expr[i]
        resultado += c1
        
        # Si no es el último carácter, revisar si necesita concatenación
        if i + 1 < len(expr):
            c2 = expr[i + 1]
            
            # El primer carácter es un símbolo, paréntesis cerrado o asterisco
            es_c1_valido = (c1 in alfabeto or c1 == ')' or c1 == '*')
            # El segundo carácter es un símbolo o paréntesis abierto
            es_c2_valido = (c2 in alfabeto or c2 == '(')
            
            # Si ambas condiciones se cumplen, insertar concatenación
            if es_c1_valido and es_c2_valido:
                resultado += '.'
                
    return resultado