# ===========================================
# CLUE 
# ===========================================

import random
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, font

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
    "Sofía Navarro": lambda arma, lugar: f"FINAL — 'La verdad entre páginas'\nDurante una investigación silenciosa entre estantes, Sofía aprovechó un descuido para cometer el crimen. Utilizó {arma} en {lugar}, moviéndose con cuidado pero dejando pistas que delatan su culpabilidad.",
    "Lucas Herrera": lambda arma, lugar: f"FINAL — 'Venenos y patrones'\nLucas, en su frustración, manipuló {arma}. Sus planes turbios se mezclaron con el crimen, dejando pistas evidentes para un detective atento en {lugar}.",
    "Diego Torres": lambda arma, lugar: f"FINAL — 'Cuchillo en la cocina'\nDurante una acalorada discusión sobre una receta robada, Diego perdió el control. Tomó {arma} y cometió el crimen en {lugar}, dejando rastros que lo delatan.",
    "Raúl Méndez": lambda arma, lugar: f"FINAL — 'Ramos y hierro'\nRaúl, entre las urgencias del jardín, no pudo contener su enojo. Con {arma} cometió el crimen en {lugar}, dejando pistas de su presencia.",
    "Mariana Vega": lambda arma, lugar: f"FINAL — 'Negocios bajo la luz'\nMariana, en {lugar}, tomó {arma} durante una reunión tensa. Sus acciones dejaron evidencia que solo un detective astuto podría notar."
}

# ==============================
# 3. Selección secreta 
# ==============================

culpable_real = random.choice(culpables)
arma_real = random.choice(armas)
lugar_real = random.choice(lugares)

# ==============================
# 4. Función de coincidencia flexible 
# ==============================

def encontrar_coincidencia(palabra, lista):
    palabra = (palabra or "").lower().strip()
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
# 5. Pistas narrativas 
# ==============================

def generar_seis_pistas():
    otros_personajes = [p for p in culpables if p != culpable_real]
    otros_armas = [a for a in armas if a != arma_real]
    otros_lugares = [l for l in lugares if l != lugar_real]

    pistas = []

    pistas.append(f"Se dice que alguien fue visto manipulando un objeto similar a {arma_real} cerca de la {random.choice(lugares)}.")
    pistas.append(f"Vecinos escucharon una discusión acalorada cerca de la {lugar_real} justo antes del incidente.")
    pistas.append(f"{random.choice(otros_personajes)} fue visto con un {random.choice(otros_armas)} rondando la {random.choice(otros_lugares)}.")
    pistas.append(f"Alguien dejó un rastro de tierra que lleva hacia la {random.choice(lugares)}, aunque no fue concluyente.")
    pistas.append(f"Una testigo menciona que algo con brillo de {arma_real.split()[0]} fue visto cerca de la {random.choice(lugares)}.")
    pistas.append(f"Se rumora que {random.choice(otros_personajes)} tiene secretos financieros, razón por la que varios sospechan de él/ella.")

    return pistas

# ==============================
# 6. Interfaz gráfica 
# ==============================

class ClueGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("CLUE - Misterio Interactivo")
        self.master.configure(bg="#1b1b1b")
        self.interrogaciones_validas = 0
        self.pistas_registradas = []

        self.titulo_font = font.Font(family="Georgia", size=18, weight="bold")
        self.sub_font = font.Font(family="Georgia", size=14)
        self.texto_font = font.Font(family="Courier New", size=12)

        header = tk.Frame(master, bg="#111111", padx=10, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="CLUE - Misterio", bg="#ED0F0F", fg="#f2f2f2", font=self.titulo_font).pack()

        main = tk.Frame(master, bg="#121212", padx=12, pady=12)
        main.pack(fill="both", expand=True)

        pistas_frame = tk.Frame(main, bg="#151515", bd=1, relief="solid", padx=8, pady=8)
        pistas_frame.pack(fill="x", pady=(0,10))

        tk.Label(pistas_frame, text="Pistas iniciales", bg="#151515", fg="#e6e6e6", font=self.sub_font).pack(anchor="w")
        pistas_box = tk.Frame(pistas_frame, bg="#151515")
        pistas_box.pack(fill="x", pady=(6,0))

        self.todas_pistas = generar_seis_pistas()
        self.pistas_iniciales_mostradas = random.sample(self.todas_pistas, 2)

        for p in self.pistas_iniciales_mostradas:
            lbl = tk.Label(pistas_box, text="•  " + p, bg="#151515", fg="#d7d7d7", font=self.texto_font, wraplength=700, justify="left")
            lbl.pack(anchor="w", pady=2)

        salida_frame = tk.Frame(main, bg="#101010")
        salida_frame.pack(fill="both", expand=True, pady=(0,10))

        self.salida = scrolledtext.ScrolledText(salida_frame, width=90, height=18, bg="#0f0f0f", fg="#eaeaea", font=self.texto_font, padx=8, pady=8)
        self.salida.pack(fill="both", expand=True)
        self._escribir_intro()

        botones = tk.Frame(main, bg="#121212")
        botones.pack()

        btn_style = {"bg":"#2b2b2b","fg":"#f2f2f2","activebackground":"#3a3a3a","activeforeground":"#ffffff","width":18,"height":1,"bd":0}
        self.btn_culpable = tk.Button(botones, text="Preguntar: Culpable", command=self.preguntar_culpable, **btn_style)
        self.btn_culpable.grid(row=0, column=0, padx=6, pady=6)
        self.btn_arma = tk.Button(botones, text="Preguntar: Arma", command=self.preguntar_arma, **btn_style)
        self.btn_arma.grid(row=0, column=1, padx=6, pady=6)
        self.btn_lugar = tk.Button(botones, text="Preguntar: Lugar", command=self.preguntar_lugar, **btn_style)
        self.btn_lugar.grid(row=0, column=2, padx=6, pady=6)
        self.btn_ver = tk.Button(botones, text="Ver pistas registradas", command=self.mostrar_pistas_registradas, **btn_style)
        self.btn_ver.grid(row=1, column=0, padx=6, pady=6)
        self.btn_acusar = tk.Button(botones, text="Acusar (finalizar)", command=self.hacer_acusacion, **btn_style)
        self.btn_acusar.grid(row=1, column=1, padx=6, pady=6)
        self.btn_reiniciar = tk.Button(botones, text="Reiniciar partida", command=self.reiniciar_partida, **btn_style)
        self.btn_reiniciar.grid(row=1, column=2, padx=6, pady=6)

        footer = tk.Frame(master, bg="#0f0f0f", pady=6)
        footer.pack(fill="x")
        tk.Label(footer, text="Interrogaciones válidas: 0 / 5", bg="#0f0f0f", fg="#cfcfcf", font=self.sub_font).pack()
        self.footer_label = footer.winfo_children()[0]

    def _escribir_intro(self):
        intro = (
            "Bienvenido al juego CLUE (versión visual). \n"
            "Tienes 5 oportunidades para interrogar (culpable / arma / lugar).\n"
            "Lee las pistas iniciales, registra la información y finalmente realiza una acusación.\n\n"
            "Culpables: " + ", ".join(culpables) + "\n"
            "Armas: " + ", ".join(armas) + "\n"
            "Lugares: " + ", ".join(lugares) + "\n\n"
            "Las pistas aparecen en la parte superior. Solo se muestran 2 pistas iniciales aleatorias.\n"
            "Cada interrogación válida se guarda y podrás ver el resumen antes de acusar.\n"
            "Buena suerte, detective.\n\n"
        )
        self.salida.insert(tk.END, intro)
        for p in self.pistas_iniciales_mostradas:
            self.salida.insert(tk.END, "- " + p + "\n")
        self.salida.see(tk.END)

    def registrar_pista(self, texto):
        self.pistas_registradas.append(texto)
        self.salida.insert(tk.END, "\n" + texto + "\n")
        self.salida.see(tk.END)
        self.footer_label.config(text=f"Interrogaciones válidas: {self.interrogaciones_validas} / 5")

    def preguntar_culpable(self):
        if self.interrogaciones_validas >= 5:
            messagebox.showinfo("Límite alcanzado", "Ya realizaste las 5 interrogaciones.")
            return
        nombre = simpledialog.askstring("Interrogación - Culpable", "¿A quién sospechas?", parent=self.master)
        if not nombre:
            return
        sospechoso = encontrar_coincidencia(nombre, culpables)
        if sospechoso is None:
            messagebox.showwarning("No reconocido", "No reconozco ese nombre. Intenta otra vez.")
            return
        self.interrogaciones_validas += 1
        if sospechoso == culpable_real:
            pista = f"{sospechoso} parece nervioso... algo esconde."
        else:
            pista = f"{sospechoso} fue visto lejos del crimen; parece inocente."
        self.registrar_pista(pista)

    def preguntar_arma(self):
        if self.interrogaciones_validas >= 5:
            messagebox.showinfo("Límite alcanzado", "Ya realizaste las 5 interrogaciones.")
            return
        texto = simpledialog.askstring("Interrogación - Arma", "¿Qué arma crees que usó?", parent=self.master)
        if not texto:
            return
        arma = encontrar_coincidencia(texto, armas)
        if arma is None:
            messagebox.showwarning("No reconocido", "No reconozco esa arma. Intenta otra vez.")
            return
        self.interrogaciones_validas += 1
        if arma == arma_real:
            pista = f"El {arma} tiene huellas recientes."
        else:
            pista = f"No se encontró ningún {arma} en la escena."
        self.registrar_pista(pista)

    def preguntar_lugar(self):
        if self.interrogaciones_validas >= 5:
            messagebox.showinfo("Límite alcanzado", "Ya realizaste las 5 interrogaciones.")
            return
        texto = simpledialog.askstring("Interrogación - Lugar", "¿Dónde crees que ocurrió el crimen?", parent=self.master)
        if not texto:
            return
        lugar = encontrar_coincidencia(texto, lugares)
        if lugar is None:
            messagebox.showwarning("No reconocido", "No reconozco ese lugar. Intenta otra vez.")
            return
        self.interrogaciones_validas += 1
        if lugar == lugar_real:
            pista = f"En la {lugar} se hallaron rastros sospechosos."
        else:
            pista = f"La {lugar} estaba vacía durante el crimen."
        self.registrar_pista(pista)

    def mostrar_pistas_registradas(self):
        if not self.pistas_registradas:
            messagebox.showinfo("Pistas", "Aún no has registrado pistas.")
            return
        texto = "\n".join(self.pistas_registradas)
        messagebox.showinfo("Pistas registradas", texto)

    def hacer_acusacion(self):
        culp = simpledialog.askstring("Acusación final", "Acusa a un culpable:", parent=self.master)
        arma = simpledialog.askstring("Acusación final", "Indica el arma usada:", parent=self.master)
        lugar = simpledialog.askstring("Acusación final", "Indica el lugar del crimen:", parent=self.master)

        c = encontrar_coincidencia(culp, culpables)
        a = encontrar_coincidencia(arma, armas)
        l = encontrar_coincidencia(lugar, lugares)

        if not all([c, a, l]):
            messagebox.showerror("Error", "No entendí completamente tu acusación. Asegúrate de escribir nombres válidos.")
            return

        if c == culpable_real and a == arma_real and l == lugar_real:
            historia = final_por_culpable[culpable_real](arma_real, lugar_real)
            self.salida.insert(tk.END, "\n\n¡Has resuelto el misterio!\n" + historia + "\n")
            messagebox.showinfo("Resultado", "Has resuelto el misterio. ¡Felicidades!")
        else:
            resumen = f"Has fallado en tu acusación.\n\nEl verdadero culpable fue:\n{culpable_real}, en {lugar_real}, con {arma_real}.\n\nHistoria final:\n{final_por_culpable[culpable_real](arma_real, lugar_real)}"
            self.salida.insert(tk.END, "\n\n" + resumen + "\n")
            messagebox.showinfo("Resultado", "Acusación incorrecta. Solo puedes reiniciar el juego usando el botón 'Reiniciar partida'.")

        # BLOQUEAR TODAS LAS ACCIONES EXCEPTO REINICIAR
        self.btn_culpable.config(state="disabled")
        self.btn_arma.config(state="disabled")
        self.btn_lugar.config(state="disabled")
        self.btn_ver.config(state="disabled")
        self.btn_acusar.config(state="disabled")

    def reiniciar_partida(self):
        confirmar = messagebox.askyesno("Reiniciar", "¿Deseas reiniciar la partida? Se generará un nuevo caso.")
        if confirmar:
            self.master.destroy()
            root = tk.Tk()
            app = ClueGUI(root)
            root.mainloop()

# ==============================
# 7. Ejecutar la GUI
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = ClueGUI(root)
    root.mainloop()
