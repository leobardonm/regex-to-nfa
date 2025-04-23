def simular_dfa(dfa, palabra, gui=False):
    estado_actual = dfa["inicio"]
    recorrido = [estado_actual]

    for simbolo in palabra:
        transiciones = dfa["transiciones"].get(estado_actual, {})
        if simbolo not in transiciones:
            recorrido.append(f"(sin '{simbolo}')")
            msg = f"❌ Palabra rechazada\nRecorrido: {' → '.join(recorrido)}"
            return msg if gui else print(msg)

        estado_actual = transiciones[simbolo]
        recorrido.append(estado_actual)

    if estado_actual in dfa["finales"]:
        msg = f"✅ Palabra aceptada\nRecorrido: {' → '.join(recorrido)}"
    else:
        msg = f"❌ Palabra no aceptada\nRecorrido: {' → '.join(recorrido)}"

    return msg if gui else print(msg)
