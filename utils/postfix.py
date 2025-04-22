def convertir_a_postfija(expresion):
    salida = []
    pila = []

    # Definir precedencias
    precedencia = {
        '*': 3,
        '.': 2,
        '|': 1
    }

    for c in expresion:
        if c.isalnum():  # letra o número
            salida.append(c)
        elif c == '(':
            pila.append(c)
        elif c == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()  # quitar el '('
        else:  # operador: *, ., |
            while (
                pila and pila[-1] != '(' and
                precedencia.get(c, 0) <= precedencia.get(pila[-1], 0)
            ):
                salida.append(pila.pop())
            pila.append(c)

    while pila:
        salida.append(pila.pop())

    return ''.join(salida)
