import tkinter as tk
from tkinter import messagebox
from utils.formatter import insertar_concatenaciones
from utils.postfix import convertir_a_postfija
from nfa_builder import construir_nfa
from dfa_converter import construir_dfa
from simular_dfa import simular_dfa
from utils.graph_drawer import draw_dfa
import time
import math
from PIL import Image, ImageTk
import os


class AFDApp:
    def __init__(self):
        self.dfa = None
        self.alfabeto = []
        self.animacion_activa = False
        self.posiciones_estados = {}
        self.imagen_afd = None
        self.transiciones_lineas = {}

        self.root = tk.Tk()
        self.root.title("Generador de AFD desde ER")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2E2E2E')  # Fondo oscuro

        self.build_interface()

        self.root.mainloop()

    def build_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2E2E2E')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame izquierdo para controles
        left_frame = tk.Frame(main_frame, width=300, bg='#2E2E2E')
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Alfabeto
        tk.Label(left_frame, text="Alfabeto (separado por comas):", bg='#2E2E2E', fg='white').pack()
        self.alfabeto_entry = tk.Entry(left_frame, width=40)
        self.alfabeto_entry.pack(pady=5)

        # Expresión regular
        tk.Label(left_frame, text="Expresión regular:", bg='#2E2E2E', fg='white').pack()
        self.er_entry = tk.Entry(left_frame, width=40)
        self.er_entry.pack(pady=5)

        # Botón para generar AFD
        tk.Button(left_frame, text="Generar AFD", command=self.generar_afd).pack(pady=10)

        # Entrada de palabra
        tk.Label(left_frame, text="Palabra a simular:", bg='#2E2E2E', fg='white').pack()
        self.palabra_entry = tk.Entry(left_frame, width=30)
        self.palabra_entry.pack()

        # Botón para simular
        tk.Button(left_frame, text="Simular palabra", command=self.simular).pack(pady=10)

        # Resultado
        self.resultado_label = tk.Label(left_frame, text="", font=("Arial", 12), 
                                      wraplength=300, justify="center", bg='#2E2E2E', fg='white')
        self.resultado_label.pack(pady=20)

        # Frame derecho para la animación
        right_frame = tk.Frame(main_frame, bg='#2E2E2E')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame para mostrar la palabra
        self.palabra_frame = tk.Frame(right_frame, bg='#2E2E2E', height=50)
        self.palabra_frame.pack(fill=tk.X, pady=10)
        
        self.caracteres_frame = tk.Frame(self.palabra_frame, bg='#2E2E2E')
        self.caracteres_frame.pack(expand=True)

        # Canvas para la animación
        self.canvas = tk.Canvas(right_frame, bg='white', width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def actualizar_palabra(self, palabra, indice_actual):
        for widget in self.caracteres_frame.winfo_children():
            widget.destroy()
            
        for i, char in enumerate(palabra):
            bg_color = '#FFD700' if i == indice_actual else '#2E2E2E'
            fg_color = 'black' if i == indice_actual else 'white'
            label = tk.Label(self.caracteres_frame, 
                           text=char,
                           font=("Courier", 24, "bold"),
                           bg=bg_color,
                           fg=fg_color,
                           width=2)
            label.pack(side=tk.LEFT, padx=1)

    def mostrar_imagen_afd(self, estado_resaltado=None, transicion_resaltada=None):
        if not self.dfa:
            return

        # Generar nueva imagen con los resaltados
        img_path = draw_dfa(self.dfa, "afd_gui", estado_resaltado, transicion_resaltada)
        
        if os.path.exists(img_path):
            # Limpiar canvas
            self.canvas.delete("all")
            
            # Cargar la imagen
            image = Image.open(img_path)
            
            # Calcular el factor de escala para ajustar la imagen al canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width, image_height = image.size
            
            # Calcular escala manteniendo la proporción
            scale = min(canvas_width/image_width, canvas_height/image_height)
            
            # Redimensionar la imagen
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convertir la imagen para Tkinter
            self.imagen_afd = ImageTk.PhotoImage(image)
            
            # Calcular posición centrada
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            
            # Mostrar la imagen
            self.canvas.create_image(x, y, anchor=tk.NW, image=self.imagen_afd)
            
            # Eliminar el archivo temporal después de cargarlo
            os.remove(img_path)

    def generar_afd(self):
        entrada_alfabeto = self.alfabeto_entry.get().replace(" ", "")
        simbolos = entrada_alfabeto.split(",")
        
        # Validar que cada símbolo sea un solo carácter
        if any(len(s) != 1 for s in simbolos):
            messagebox.showerror("Error", "Cada símbolo del alfabeto debe ser un solo carácter.")
            return
            
        self.alfabeto = simbolos
        expresion = self.er_entry.get().replace(" ", "")
        
        if not expresion or not self.alfabeto:
            messagebox.showerror("Error", "Debes ingresar un alfabeto y una expresión regular.")
            return
            
        # Validar símbolos de la expresión regular
        operadores = set(['*', '|', '.', '(', ')'])
        simbolos_validos = set(self.alfabeto).union(operadores)
        simbolos_invalidos = [c for c in expresion if c not in simbolos_validos]
        
        if simbolos_invalidos:
            messagebox.showerror("Error", 
                f"Símbolos inválidos en la expresión: {', '.join(simbolos_invalidos)}\n"
                "Solo usa los símbolos del alfabeto y los operadores: *, |, ., (, )")
            return

        try:
            expresion_conc = insertar_concatenaciones(expresion, self.alfabeto)
            postfija = convertir_a_postfija(expresion_conc)
            nfa = construir_nfa(postfija, self.alfabeto)
            self.dfa = construir_dfa(nfa, self.alfabeto)
            messagebox.showinfo("AFD generado", "✅ El AFD fue construido correctamente.")
            self.mostrar_imagen_afd()
        except Exception as e:
            messagebox.showerror("Error al construir el AFD", str(e))

    def animar_recorrido(self, palabra):
        if not self.dfa:
            return

        # Mostrar la palabra inicialmente
        self.actualizar_palabra(palabra, -1)
        self.mostrar_imagen_afd()  # Mostrar AFD sin resaltados
        self.root.update()
        time.sleep(1)

        estado_actual = self.dfa["inicio"]
        self.mostrar_imagen_afd(estado_resaltado=(estado_actual, "#92c5fc"))  # Amarillo
        self.root.update()
        time.sleep(1)

        for i, simbolo in enumerate(palabra):
            # Actualizar el carácter resaltado
            self.actualizar_palabra(palabra, i)
            self.root.update()
            time.sleep(0.5)

            transiciones = self.dfa["transiciones"].get(estado_actual, {})
            if simbolo not in transiciones:
                self.mostrar_imagen_afd(estado_resaltado=(estado_actual, "#FF4444"))  # Rojo
                self.root.update()
                time.sleep(1)
                return False

            # Resaltar la transición actual y el estado
            self.mostrar_imagen_afd(
                estado_resaltado=(estado_actual, "#92c5fc"),  # Estado actual en amarillo
                transicion_resaltada=(estado_actual, simbolo)  # Resaltar transición
            )
            self.root.update()
            time.sleep(1)

            estado_actual = transiciones[simbolo]
            self.mostrar_imagen_afd(estado_resaltado=(estado_actual, "#92c5fc"))  # Nuevo estado en amarillo
            self.root.update()
            time.sleep(1)

        # Mostrar el último carácter
        self.actualizar_palabra(palabra, len(palabra))
        self.root.update()
        time.sleep(0.5)

        # Verificar si es estado final
        color_final = "#44FF44" if estado_actual in self.dfa["finales"] else "#FF4444"  # Verde o Rojo
        self.mostrar_imagen_afd(estado_resaltado=(estado_actual, color_final))
        self.root.update()
        time.sleep(1)

        return estado_actual in self.dfa["finales"]

    def simular(self):
        palabra = self.palabra_entry.get()
        if not self.dfa:
            messagebox.showerror("Error", "Primero debes generar el AFD.")
            return

        # Realizar la animación
        resultado = self.animar_recorrido(palabra)
        
        # Mostrar el resultado
        if resultado:
            self.resultado_label.config(text="✅ Palabra aceptada")
        else:
            self.resultado_label.config(text="❌ Palabra rechazada")


if __name__ == "__main__":
    AFDApp()
