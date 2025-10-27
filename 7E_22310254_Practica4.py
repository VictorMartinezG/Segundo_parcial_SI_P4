# ===========================================
# INTERACTIVO DEL JUEGO "CLUE"

import random

# ==============================
# 1. Datos base del juego
# ==============================

culpables = [
    "Sofía Navarro",
    "Diego Torres",
    "Mariana Vega",
    "Raúl Méndez",
    "Lucas Herrera"
]

armas = [
    "Candelabro",
    "Cuchillo de cocina",
    "Jeringa con toxina",
    "Tijeras de podar",
    "Base de cristal"
]

lugares = [
    "Sala principal",
    "Cocina",
    "Biblioteca",
    "Invernadero",
    "Suite privada"
]

# ==============================
# 2. Finales por culpable 
# ==============================

final_por_culpable = {
    "Sofía Navarro": lambda arma, lugar: f"FINAL — 'La verdad entre páginas'\nDurante una investigación silenciosa entre el silencio, Sofía aprovechó un descuido para cometer el crimen. Utilizó {arma} en {lugar}, moviéndose con cuidado pero dejando pistas que delatan su culpabilidad.",
    "Lucas Herrera": lambda arma, lugar: f"FINAL — 'Venenos y patrones'\nLucas, en su frustracion, manipuló {arma}. Sus planes turbios se mezclaron con el crimen, dejando pistas evidentes para un detective atento en {lugar}.",
    "Diego Torres": lambda arma, lugar: f"FINAL — 'Cuchillo en la cocina'\nDurante una acalorada discusión sobre una receta robada, Diego perdió el control. Tomó {arma} y cometió el crimen en {lugar}, dejando rastros que lo delatan.",
    "Raúl Méndez": lambda arma, lugar: f"FINAL — 'Ramos y hierro'\nRaúl, entre los negocios, no pudo contener su enojo. Con {arma} cometió el crimen en {lugar}, dejando pistas de su presencia.",
    "Mariana Vega": lambda arma, lugar: f"FINAL — 'Negocios bajo la luz'\nMariana, en {lugar}, tomó {arma} durante una reunión tensa. Sus acciones dejaron evidencia que solo un detective astuto podría notar."
}


# ==============================
# 3. Selección secreta
# ==============================

culpable_real = random.choice(culpables)
arma_real = random.choice(armas)
lugar_real = random.choice(lugares)

index_final = (culpables.index(culpable_real) +
               armas.index(arma_real) +
               lugares.index(lugar_real)) % 5

# ==============================
# 4. Función de coincidencia flexible
# ==============================

def encontrar_coincidencia(palabra, lista):
    palabra = palabra.lower().strip()
    reemplazos = (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"))
    for a,b in reemplazos:
        palabra = palabra.replace(a,b)
    for item in lista:
        normalizado = item.lower()
        for a,b in reemplazos:
            normalizado = normalizado.replace(a,b)
        if palabra in normalizado or normalizado in palabra:
            return item
    return None

# ==============================
# 5. Introducción
# ==============================

print("=====================================")
print(" BIENVENIDO AL JUEGO DE MISTERIO CLUE ")
print("=====================================")
print("Hay un crimen que resolver. Tienes 5 oportunidades para interrogar.")
print("Puedes preguntar sobre:")
print("- Culpables:", ", ".join(culpables))
print("- Armas:", ", ".join(armas))
print("- Lugares:", ", ".join(lugares))
print("-------------------------------------")

# ==============================
# 5.1 Dar 2 pistas iniciales narrativas
# ==============================

# Lista de pistas narrativas
pistas_narrativas = []

otros_personajes = [p for p in culpables if p != culpable_real]
otros_armas = [a for a in armas if a != arma_real]
otros_lugares = [l for l in lugares if l != lugar_real]
# Pista verdadera
pistas_narrativas.append(
    f" Pista: Se vio a alguien manipular el '{arma_real}' cerca de la '{random.choice(otros_lugares)}'. Observa bien cómo actuaba."
)

# Pista falsa

pistas_narrativas.append(
    f" Pista: {random.choice(otros_personajes)} fue visto en la '{lugar_real}' jugando con un '{random.choice(otros_armas)}'."
)

# Elegir aleatoriamente el orden de las dos pistas
pistas_iniciales = random.sample(pistas_narrativas, 2)

print("\n Aquí tienes 2 pistas iniciales para empezar:")
for pista in pistas_iniciales:
    print("-", pista)
print("-------------------------------------\n")

# ==============================
# 6. Interrogaciones
# ==============================

pistas = []
interrogaciones_validas = 0

while interrogaciones_validas < 5:
    print(f"\n Interrogación {interrogaciones_validas + 1}/5 ")
    tipo = input("¿Quieres preguntar sobre (culpable / arma / lugar)? ").strip().lower()

    if tipo == "culpable":
        entrada = input("¿A quién sospechas? ").strip()
        sospechoso = encontrar_coincidencia(entrada, culpables)
        if sospechoso is None:
            print(" No reconozco ese nombre. Verifica tu escritura.")
            continue
        interrogaciones_validas += 1
        if sospechoso == culpable_real:
            pista = f" {sospechoso} parece nervioso… algo esconde."
        else:
            pista = f" {sospechoso} fue visto lejos del crimen, parece inocente."
        print(pista)
        pistas.append(pista)

    elif tipo == "arma":
        entrada = input("¿Qué arma crees que usó? ").strip()
        arma = encontrar_coincidencia(entrada, armas)
        if arma is None:
            print(" No reconozco esa arma. Intenta con otra descripción.")
            continue
        interrogaciones_validas += 1
        if arma == arma_real:
            pista = f" El {arma} tiene huellas recientes."
        else:
            pista = f" No se encontró ningún {arma} en la escena."
        print(pista)
        pistas.append(pista)

    elif tipo == "lugar":
        entrada = input("¿Dónde crees que ocurrió el crimen? ").strip()
        lugar = encontrar_coincidencia(entrada, lugares)
        if lugar is None:
            print(" No reconozco ese lugar. Intenta con otro nombre.")
            continue
        interrogaciones_validas += 1
        if lugar == lugar_real:
            pista = f" En la {lugar} se hallaron rastros sospechosos."
        else:
            pista = f" La {lugar} estaba vacía durante el crimen."
        print(pista)
        pistas.append(pista)

    else:
        print(" Solo puedes preguntar sobre 'culpable', 'arma' o 'lugar'.")

# ==============================
# 7. Mostrar pistas antes de acusación
# ==============================

print("\n Resumen de tus pistas:")
for p in pistas:
    print("-", p)

print("\n Ya realizaste tus 5 interrogaciones.")
print("Es momento de hacer tu acusación final.\n")

# ==============================
# 8. Acusación final
# ==============================

culpable_acusado = encontrar_coincidencia(input(" Acusa a un culpable: "), culpables)
arma_acusada = encontrar_coincidencia(input(" Indica el arma usada: "), armas)
lugar_acusado = encontrar_coincidencia(input(" Indica el lugar del crimen: "), lugares)

print("\n=====================================")
print("  RESULTADOS DEL CASO  ")
print("=====================================")

if not all([culpable_acusado, arma_acusada, lugar_acusado]):
    print(" No entendí completamente tu acusación. Se cancela el caso.")
else:
    if (culpable_acusado == culpable_real and
        arma_acusada == arma_real and
        lugar_acusado == lugar_real):
        print(" ¡Has resuelto el misterio! ¡Eres un gran detective! 🕵️‍♂️")
        print(final_por_culpable[culpable_real](arma_real, lugar_real))
    else:
        print(" Has fallado en tu acusación.")
        print("El verdadero culpable fue:")
        print(f"{culpable_real}, en {lugar_real}, con {arma_real}.")
        print("\nHistoria final:")
        print(final_por_culpable[culpable_real](arma_real, lugar_real))


print("\nGracias por jugar CLUE ")