# Generador de Autómatas Finitos Deterministas desde Expresiones Regulares

## Descripción General
Este proyecto implementa una aplicación en Python que permite generar y visualizar Autómatas Finitos Deterministas (AFD) a partir de expresiones regulares. La aplicación cuenta con una interfaz gráfica que permite al usuario ingresar una expresión regular y un alfabeto, visualizar el AFD resultante y probar palabras para verificar si pertenecen al lenguaje.

## Características Principales
- Interfaz gráfica moderna y fácil de usar
- Visualización dinámica del AFD
- Animación del proceso de validación de palabras
- Manejo robusto de errores
- Resaltado visual del recorrido del autómata

## Requisitos del Sistema
- Python 3.x
- Graphviz (para la visualización de autómatas)
- Tkinter (incluido en Python)
- Pillow (para el manejo de imágenes)

## Instalación
1. Clonar el repositorio
2. Instalar las dependencias:
```bash
pip install graphviz pillow
```
3. Asegurarse de tener Graphviz instalado en el sistema:
   - Windows: Descargar de [Graphviz](https://graphviz.org/download/)
   - macOS: `brew install graphviz`
   - Linux: `sudo apt-get install graphviz`

## Uso
1. Ejecutar la aplicación:
```bash
python main_gui.py
```
2. Ingresar el alfabeto separado por comas (ejemplo: "a,b,c")
3. Ingresar la expresión regular usando los operadores:
   - `*` para la estrella de Kleene
   - `|` para la unión
   - `.` para la concatenación
   - `()` para agrupación
4. Hacer clic en "Generar AFD"
5. Ingresar palabras para probar si son aceptadas por el autómata

## Implementación Técnica

### 1. Procesamiento de la Expresión Regular
El proceso de conversión de expresión regular a AFD se realiza en varias etapas:

a) **Preprocesamiento** (`utils/formatter.py`):
- Inserción de concatenaciones explícitas
- Validación de símbolos y operadores
- Manejo de espacios y caracteres especiales

b) **Conversión a Notación Postfija** (`utils/postfix.py`):
- Implementación del algoritmo Shunting Yard
- Manejo de precedencia de operadores
- Validación de paréntesis balanceados

### 2. Construcción del AFN
La construcción del AFN (`nfa_builder.py`) implementa el algoritmo de Thompson:
- Construcción de AFNs básicos para símbolos
- Implementación de operaciones:
  - Concatenación
  - Unión
  - Estrella de Kleene
- Manejo de estados y transiciones epsilon

### 3. Conversión a AFD
La conversión de AFN a AFD (`dfa_converter.py`) utiliza el algoritmo de subconjuntos:
- Cálculo de ε-clausuras
- Construcción de la tabla de transiciones
- Minimización de estados
- Identificación de estados finales

### 4. Visualización
La interfaz gráfica (`gui/simulador_dfa_gui.py`) proporciona:
- Visualización del AFD usando Graphviz
- Animación del proceso de validación
- Resaltado de estados y transiciones
- Feedback visual del resultado

## Estructura del Proyecto
```
.
├── gui/
│   └── simulador_dfa_gui.py
├── utils/
│   ├── formatter.py
│   ├── postfix.py
│   └── graph_drawer.py
├── nfa_builder.py
├── dfa_converter.py
├── simular_dfa.py
└── main_gui.py
```

## Ejemplos de Uso

### Ejemplo 1: Números Binarios
- Alfabeto: `0,1`
- Expresión: `(0|1)*`
- Descripción: Acepta cualquier cadena de ceros y unos

### Ejemplo 2: Palabras que Terminan en 'a'
- Alfabeto: `a,b`
- Expresión: `(a|b)*.a`
- Descripción: Acepta cualquier palabra que termine en 'a'



## Limitaciones y Consideraciones
- La aplicación está optimizada para expresiones regulares de complejidad moderada
- El tamaño del alfabeto puede afectar el rendimiento de la visualización
- Se recomienda usar paréntesis para evitar ambigüedades en las expresiones

## Contribuciones y Mejoras Futuras
- Implementación de minimización de AFD
- Soporte para más operadores de expresiones regulares
- Mejoras en la visualización para autómatas grandes
- Exportación de autómatas en diferentes formatos

## Autores
José Leobardo Navarro Márquez 

Regina Martínez Vázquez

## Licencia
Este proyecto es parte de la actividad integradora del curso TC2037 - Implementación de métodos computacionales. 
