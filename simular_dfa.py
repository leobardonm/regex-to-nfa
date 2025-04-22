def simular_dfa(dfa, palabra):
    estado_actual = dfa["inicio"]

    print("\nRecorrido del AFD:")
    for simbolo in palabra:
        print(f"{estado_actual} --{simbolo}--> ", end="")

        if simbolo not in dfa["transiciones"][estado_actual]:
            print("❌ Transición no definida.")
            return False

        estado_actual = dfa["transiciones"][estado_actual][simbolo]
        print(estado_actual)

    if estado_actual in dfa["finales"]:
        print(f"\n✅ Palabra aceptada. Estado final: {estado_actual}")
        return True
    else:
        print(f"\n❌ Palabra no aceptada. Estado final: {estado_actual}")
        return False
