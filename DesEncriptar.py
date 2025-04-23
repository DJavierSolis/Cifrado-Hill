import numpy as np
import tkinter as tk
from tkinter import Toplevel, messagebox

# Definimos el alfabeto en Z27 (con letras A-Z, Ñ y espacio)
alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ "

# Convertir texto a números en Z27
def texto_a_numeros(texto):
    # Reemplazar caracteres no válidos por '?'
    texto = "".join([letra if letra in alfabeto else ' ' for letra in texto.upper()])
    
    # Convertir el texto a números de acuerdo al alfabeto
    return [alfabeto.index(letra) for letra in texto]

# Convertir números a texto
def numeros_a_texto(numeros):
    return "".join(alfabeto[num] for num in numeros)

# Función de cifrado Hill en Z27
def cifrado_hill(texto, K):
    numeros = texto_a_numeros(texto)
    
    # Ajustar el tamaño de la matriz (rellenar con espacio si es necesario)
    while len(numeros) % len(K) != 0:
        numeros.append(alfabeto.index(" "))  # Relleno con espacio
    
    # Convertir lista a matriz
    P = np.array(numeros).reshape(-1, len(K)).T

    # Multiplicar por la matriz clave en Z27
    C = np.dot(K, P) % 27
    
    # Convertir a lista de números y luego a texto
    cifrado = numeros_a_texto(C.T.flatten())
    return cifrado

# Función para abrir ventana flotante con el texto encriptado
def abrir_ventana_flotante():
    texto_ingresado = mensaje.get().strip()  # Obtener el texto del Entry y quitar espacios extra

    # Convertir texto ingresado, donde los caracteres no válidos serán reemplazados por '?'
    texto_cifrado = cifrado_hill(texto_ingresado, K)  # Encriptar texto

    # Crear ventana flotante con el texto cifrado
    ventana_flotante = Toplevel(root)
    ventana_flotante.title("Texto Cifrado")
    ventana_flotante.geometry("350x150")
    ventana_flotante.attributes('-topmost', True)  # Mantener en primer plano

    etiqueta = tk.Label(ventana_flotante, text=f"Cifrado: {texto_cifrado}", font=("Arial", 12))
    etiqueta.pack(pady=20)

# Ventana principal
root = tk.Tk()
root.title("Ventana Encriptar")
root.geometry("400x300")

# Matriz clave 2x2 (debe ser invertible en Z27)
K = np.array([[5, 8], [17, 3]])

# Etiqueta y campo de entrada
tk.Label(root, text="Ingresa Frase:", font=("Times New Roman", 12)).pack(pady=10)
mensaje = tk.Entry(root, font=("Times New Roman", 12), width=30)
mensaje.pack(pady=5)

# Botón para encriptar
boton = tk.Button(root, text="Encriptar", command=abrir_ventana_flotante)
boton.pack(pady=20)

root.mainloop()
