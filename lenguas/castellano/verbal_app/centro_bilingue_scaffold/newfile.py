# ============================================
# ENTRENADOR DE PÁRRAFOS ACADÉMICOS
# ============================================

def menu():
    print("\n📚 ENTRENADOR DE PÁRRAFOS")
    print("1. Ver todas las técnicas")
    print("2. Buscar técnica por número")
    print("3. Practicar (modo aleatorio)")
    print("0. Salir")


# =========================
# BASE DE DATOS
# =========================

tecnicas = {
    1: {
        "tipo": "Tesis",
        "ejemplo": "La redacción universitaria en Colombia requiere el dominio de estrategias argumentativas que permitan articular pensamiento crítico.",
        "explicacion": "Sujeto: 'La redacción universitaria en Colombia'. Verbo: 'requiere'. Complemento directo: 'el dominio...'. Subordinada: 'que permitan...'"
    },
    2: {
        "tipo": "Definición",
        "ejemplo": "Un párrafo argumentativo es una unidad textual que presenta una idea central respaldada por evidencia.",
        "explicacion": "Oración copulativa: Sujeto + verbo 'es' + atributo. Subordinada relativa: 'que presenta...'"
    },
    3: {
        "tipo": "Ejemplificación",
        "ejemplo": "Por ejemplo, el uso de citas académicas fortalece la credibilidad del texto.",
        "explicacion": "Marcador discursivo + oración simple con sujeto explícito y verbo 'fortalece'."
    },
    4: {
        "tipo": "Argumentativo",
        "ejemplo": "El uso de fuentes confiables es fundamental, ya que garantiza la validez de la información.",
        "explicacion": "Oración compuesta: principal + subordinada causal ('ya que...')."
    },
    5: {
        "tipo": "Contraargumento",
        "ejemplo": "Algunos consideran que escribir bien no es necesario; sin embargo, es esencial en la academia.",
        "explicacion": "Dos proposiciones unidas por conector adversativo ('sin embargo')."
    },
    6: {
        "tipo": "Transición",
        "ejemplo": "En este sentido, es necesario analizar la estructura del texto académico.",
        "explicacion": "Conector + oración impersonal + subordinada ('analizar...')."
    },
    7: {
        "tipo": "Descripción",
        "ejemplo": "El texto académico presenta claridad, coherencia y precisión.",
        "explicacion": "Oración simple con enumeración de complementos directos."
    },
    8: {
        "tipo": "Cita indirecta",
        "ejemplo": "Según diversos autores, la escritura académica construye conocimiento.",
        "explicacion": "Complemento circunstancial de fuente + oración principal."
    },
    9: {
        "tipo": "Análisis",
        "ejemplo": "Esto permite observar que la coherencia depende de la organización del discurso.",
        "explicacion": "Oración principal + subordinada sustantiva ('que...')."
    },
    10: {
        "tipo": "Conclusión",
        "ejemplo": "En conclusión, dominar los párrafos mejora la escritura académica.",
        "explicacion": "Conector + sujeto en infinitivo + verbo principal."
    }
}


# =========================
# FUNCIONES
# =========================

def mostrar_todas():
    print("\n📖 TODAS LAS TÉCNICAS\n")
    for num, data in tecnicas.items():
        print(f"{num}. Tipo: {data['tipo']}")
        print(f"   ✍️ Ejemplo: {data['ejemplo']}")
        print(f"   🔍 Sintaxis: {data['explicacion']}\n")


def buscar_tecnica():
    try:
        num = int(input("Ingresa número (1-10): "))
        if num in tecnicas:
            data = tecnicas[num]
            print(f"\n📌 Técnica {num}: {data['tipo']}")
            print(f"✍️ {data['ejemplo']}")
            print(f"🔍 {data['explicacion']}\n")
        else:
            print("❌ No existe")
    except:
        print("❌ Entrada inválida")


def practicar():
    import random
    num = random.choice(list(tecnicas.keys()))
    data = tecnicas[num]

    print("\n🎯 MODO PRÁCTICA")
    print(f"Tipo de párrafo: {data['tipo']}")
    input("✍️ Escribe un ejemplo y presiona ENTER...")

    print("\n📌 Ejemplo sugerido:")
    print(data["ejemplo"])
    print("\n🔍 Explicación:")
    print(data["explicacion"])


# =========================
# PROGRAMA PRINCIPAL
# =========================

while True:
    menu()
    opcion = input("Selecciona opción: ")

    if opcion == "1":
        mostrar_todas()
    elif opcion == "2":
        buscar_tecnica()
    elif opcion == "3":
        practicar()
    elif opcion == "0":
        print("👋 Hasta luego")
        break
    else:
        print("❌ Opción inválida")