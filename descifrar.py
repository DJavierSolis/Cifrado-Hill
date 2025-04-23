import numpy as np

# Alfabeto en Z27
alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ "

# Función para calcular la inversa modular de una matriz en Z27
def inversa_modular(matriz, mod):
    det = int(round(np.linalg.det(matriz)))  # Determinante de la matriz
    det_inv = pow(det, -1, mod)  # Inversa modular del determinante en Z27
    
    # Matriz adjunta
    adjunta = np.round(det * np.linalg.inv(matriz)).astype(int) % mod
    
    # Matriz inversa en Z27
    return (det_inv * adjunta) % mod

# Ingresar el mensaje cifrado
cifrado_texto = input("Ingrese el mensaje cifrado: ").upper()

# Ingresar la matriz clave
print("\nIngrese la matriz clave (2x2):")
K = np.zeros((2,2), dtype=int)
for i in range(2):
    K[i] = list(map(int, input(f"Fila {i+1}: ").split()))

# Convertir texto cifrado a números
cifrado_numeros = [alfabeto.index(letra) for letra in cifrado_texto]

# Calcular la inversa de la matriz en Z27
try:
    K_inv = inversa_modular(K, 27)
except ValueError:
    print("❌ La matriz no tiene inversa en Z27. Prueba con otra.")
    exit()

# Descifrar por bloques de 2
descifrado_numeros = []
for i in range(0, len(cifrado_numeros), 2):
    bloque = np.array([[cifrado_numeros[i]], [cifrado_numeros[i+1]]])  # Crear columna 2x1
    descifrado_bloque = np.dot(K_inv, bloque) % 27  # Multiplicar por K^-1 y aplicar mod 27
    descifrado_numeros.extend(descifrado_bloque.flatten())  # Guardar resultados

# Convertir números descifrados a texto
descifrado_texto = "".join(alfabeto[num] for num in descifrado_numeros)

print("\nTexto descifrado:", descifrado_texto)
