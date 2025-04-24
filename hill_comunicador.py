import socket #permite la comunicacion entre computadoras en red
import threading #hilos para trabajar en paralelo
import tkinter as tk #Herramientas de interfaz
from tkinter import messagebox, scrolledtext
import numpy as np #libreria para gestionar operaciones con matricez :p
#Ademas de estas librerias importadas, se instalo una extension llamada py installer para empaquetar en .exe mediante comando:
# pyinstaller --onefile --noconsole hill_comunicador.py

# Jair Castillo Javier Solis 

#  ALFABETO Z28 (con espacio, letra ñ y guión bajo)
alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ_ "

# CIFRADO / DESCIFRADO 
# Convierte texto a numeros en base a su indice en el alfabeto
def texto_a_numeros(texto):
    texto = texto.upper().replace(" ", "_") #Se reemplazan los espacios en el mensaje por guiones bajos
    texto = "".join([letra if letra in alfabeto else '_' for letra in texto]) #Si existe algun caracter invalido, tambien lo reemplaza por guion bajo
    return [alfabeto.index(letra) for letra in texto]

def numeros_a_texto(numeros): #Lo contrario, se convierte los numeros en texto en base al mismo indice
    return "".join(alfabeto[num] for num in numeros)


def cifrado_hill(texto, K):

    # convierte el texto a numeros. Asegura que el total de números sea par (rellenando con guion bajo si es necesario).
    #Forma bloques de 2x1 (como columnas).
    #Aplica la formula: C = K*P mod 28
    #Devuelve el texto cifrado

    numeros = texto_a_numeros(texto)
    while len(numeros) % 2 != 0:
        numeros.append(alfabeto.index("_"))  
    P = np.array(numeros).reshape(-1, 2).T
    C = np.dot(K, P) % 28
    return numeros_a_texto(C.T.flatten())

def inversa_modular(matriz, mod):

    # Calcula la matriz inversa en Z28, necesaria para descifrar. Pasos:
    # Calcula el determinante de la matriz. Obtiene su inversa modular (det-1 mod 28).
    # Multiplica por la matriz adjunta y aplica mod 28.
    det = int(round(np.linalg.det(matriz)))
    det_inv = pow(det, -1, mod)
    adjunta = np.round(det * np.linalg.inv(matriz)).astype(int) % mod
    return (det_inv * adjunta) % mod

def descifrar_hill(texto, K):

    #Descifra un mensaje cifrado: 
    #Convierte el texto a números.
    # Calcula la matriz inversa K-1 mod 28.
    #Aplica la fórmula: P = K-1 * C mod 28
    #Convierte los numeros descifrados a texto

    numeros = [alfabeto.index(c) for c in texto]
    K_inv = inversa_modular(K, 28)
    texto_descifrado = []
    for i in range(0, len(numeros), 2):
        bloque = np.array([[numeros[i]], [numeros[i+1]]])
        descifrado = np.dot(K_inv, bloque) % 28
        texto_descifrado.extend(descifrado.flatten())
    return numeros_a_texto(texto_descifrado)

K = np.array([[5, 8], [17, 3]])  # Clave fija, se puede variar pero se tiene que empaquetar de nuevo, debe ser invertible en Z28

# VENTANA CLIENTE 
# Crea una ventana cliente donde el usuario: Escribe la IP del servidor. Ingresa el mensaje a cifrar. Envía el mensaje cifrado al servidor.

#Internamente: Cifra el mensaje. Crea un socket TCP. Se conecta al servidor usando la IP y puerto 9999. Envía el mensaje. Espera la respuesta del servidor. Muestra la confirmación o el error.
def abrir_cliente():
    cliente = tk.Toplevel()
    cliente.title("Cliente - Cifrar y Enviar")
    cliente.geometry("500x400")
    cliente.configure(bg="#8B0000")

    tk.Label(cliente, text="IP del servidor:", bg="#8B0000", fg="white", font=("Arial", 11)).pack(pady=5)
    ip_entry = tk.Entry(cliente, font=("Arial", 11), width=30)
    ip_entry.insert(0, "192.168.1.10")
    ip_entry.pack(pady=3)

    tk.Label(cliente, text="Mensaje a cifrar:", bg="#8B0000", fg="white", font=("Arial", 12)).pack(pady=5)
    entrada = tk.Entry(cliente, font=("Arial", 12), width=40)
    entrada.pack(pady=5)

    resultado_cifrado = tk.StringVar()
    confirmacion = tk.StringVar()

    def enviar():
        texto = entrada.get().strip()
        ip_destino = ip_entry.get().strip()

        if not texto or not ip_destino:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos.")
            return

        cifrado = cifrado_hill(texto, K)
        resultado_cifrado.set(f"Cifrado: {cifrado}")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip_destino, 9999))
            sock.send(cifrado.encode())
            respuesta = sock.recv(1024).decode()
            sock.close()
            confirmacion.set(f"✔ {respuesta}")
        except Exception as e:
            confirmacion.set(f"❌ Error: {e}")

    tk.Button(cliente, text="Cifrar y Enviar", font=("Arial", 12), bg="white", fg="#8B0000", command=enviar).pack(pady=15)
    tk.Label(cliente, textvariable=resultado_cifrado, bg="#8B0000", fg="white", font=("Courier", 12)).pack(pady=5)
    tk.Label(cliente, textvariable=confirmacion, bg="#8B0000", fg="lightgreen", font=("Arial", 11, "italic")).pack(pady=10)
    tk.Label(cliente, text="Jair Castillo", bg="#8B0000", fg="white", font=("Arial", 8, "italic")).place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)

# VENTANA SERVIDOR
#Crea la ventana del servidor que: Escucha conexiones en el puerto 9999. 
#Muestra en un cuadro de texto: IP del cliente conectado. Mensaje cifrado recibido. Resultado descifrado. Responde con “Mensaje recibido correctamente”.
# La función iniciar_servidor() se ejecuta en un hilo paralelo para que no congele la ventana.
def abrir_servidor():
    servidor = tk.Toplevel()
    servidor.title("Servidor - Descifrar y Confirmar")
    servidor.geometry("500x400")
    servidor.configure(bg="#8B0000")

    log = scrolledtext.ScrolledText(servidor, width=60, height=20, font=("Courier", 10), bg="#330000", fg="white")
    log.pack(pady=20)

    tk.Label(servidor, text="Jair Castillo", bg="#8B0000", fg="white", font=("Arial", 8, "italic")).place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)

    def iniciar_servidor():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 9999))
        server.listen(1)
        log.insert(tk.END, "Servidor esperando conexión...\n")

        while True:
            cliente, addr = server.accept()
            log.insert(tk.END, f"Conexión desde {addr}\n")
            data = cliente.recv(1024).decode()
            log.insert(tk.END, f"Mensaje cifrado: {data}\n")
            try:
                descifrado = descifrar_hill(data, K)
                log.insert(tk.END, f"Descifrado: {descifrado}\n\n")
                cliente.send("Mensaje recibido correctamente".encode())
            except:
                cliente.send("Error al descifrar el mensaje.".encode())
            cliente.close()

    threading.Thread(target=iniciar_servidor, daemon=True).start()

# VENTANA PRINCIPAL
root = tk.Tk() #Carga la pantalla inicial donde se elige el rol
root.title("Hill Z28 - Comunicador")
root.geometry("400x250")
root.configure(bg="#8B0000")

tk.Label(root, text="Selecciona un rol:", bg="#8B0000", fg="white", font=("Arial", 14, "bold")).pack(pady=30)
tk.Button(root, text="🟢 Cliente", font=("Arial", 12), bg="white", fg="#8B0000", width=20, command=abrir_cliente).pack(pady=10)
tk.Button(root, text="🔴 Servidor", font=("Arial", 12), bg="white", fg="#8B0000", width=20, command=abrir_servidor).pack(pady=10)
tk.Label(root, text="Jair Castillo", bg="#8B0000", fg="white", font=("Arial", 8, "italic")).place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)

root.mainloop()
