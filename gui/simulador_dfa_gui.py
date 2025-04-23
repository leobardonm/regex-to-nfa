import tkinter as tk
from tkinter import messagebox
from utils.formatter import insertar_concatenaciones
from utils.postfix import convertir_a_postfija
from nfa_builder import construir_nfa
from dfa_converter import construir_dfa
from simular_dfa import simular_dfa
from visualizer.graph_drawer import draw_dfa


class AFDApp:
    def __init__(self):
        self.dfa = None
        self.alfabeto = []

        self.root = tk.Tk()
        self.root.title("Generador de AFD desde ER")
        self.root.geometry("600x450")

        self.build_interface()

        self.root.mainloop()

    def build_interface(self):
        # Alfabeto
        tk.Label(self.root, text="Alfabeto (separado por comas):").pack()
        self.alfabeto_entry = tk.Entry(self.root, width=40)
        self.alfabeto_entry.pack(pady=5)

        # Expresión regular
        tk.Label(self.root, text="Expresión regular:").pack()
        self.er_entry = tk.Entry(self.root, width=40)
        self.er_entry.pack(pady=5)

        # Botón para generar AFD
        tk.Button(self.root, text="Generar AFD", command=self.generar_afd).pack(pady=10)

        # Entrada de palabra
        tk.Label(self.root, text="Palabra a simular:").pack()
        self.palabra_entry = tk.Entry(self.root, width=30)
        self.palabra_entry.pack()

        # Botón para simular
        tk.Button(self.root, text="Simular palabra", command=self.simular).pack(pady=10)

        # Botón para mostrar grafo
        tk.Button(self.root, text="Mostrar grafo del AFD", command=self.mostrar_grafo).pack()

        # Resultado
        self.resultado_label = tk.Label(self.root, text="", font=("Arial", 12), wraplength=500, justify="center")
        self.resultado_label.pack(pady=20)

    def generar_afd(self):
        entrada_alfabeto = self.alfabeto_entry.get().replace(" ", "")
        self.alfabeto = entrada_alfabeto.split(",")

        expresion = self.er_entry.get()
        if not expresion or not self.alfabeto:
            messagebox.showerror("Error", "Debes ingresar un alfabeto y una expresión regular.")
            return

        try:
            expresion_conc = insertar_concatenaciones(expresion, self.alfabeto)
            postfija = convertir_a_postfija(expresion_conc)
            nfa = construir_nfa(postfija, self.alfabeto)
            self.dfa = construir_dfa(nfa, self.alfabeto)
            messagebox.showinfo("AFD generado", "✅ El AFD fue construido correctamente.")
        except Exception as e:
            messagebox.showerror("Error al construir el AFD", str(e))

    def simular(self):
        palabra = self.palabra_entry.get()
        if not self.dfa:
            messagebox.showerror("Error", "Primero debes generar el AFD.")
            return
        resultado = simular_dfa(self.dfa, palabra, gui=True)
        self.resultado_label.config(text=resultado)

    def mostrar_grafo(self):
        if not self.dfa:
            messagebox.showerror("Error", "Primero debes generar el AFD.")
            return
        path = draw_dfa(self.dfa, "afd_gui")
        import os, webbrowser
        if os.path.exists(path):
            webbrowser.open(f"file://{os.path.abspath(path)}")


if __name__ == "__main__":
    AFDApp()
