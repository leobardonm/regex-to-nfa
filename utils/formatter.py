def insertar_concatenaciones(expr, alfabeto):
    resultado = ""
    for i in range(len(expr)):
        c1 = expr[i]
        resultado += c1

        if i + 1 < len(expr):
            c2 = expr[i + 1]
            if (
                (c1 in alfabeto or c1 == ')' or c1 == '*') and
                (c2 in alfabeto or c2 == '(')
            ):
                resultado += '.'
    return resultado