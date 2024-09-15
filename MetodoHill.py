import numpy as np

# Diccionario para encriptar: convierte letras a números
diccionario_encryt = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
    'M': 12, 'N': 13, 'Ñ': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22,
    'W': 23, 'X': 24, 'Y': 25, 'Z': 26, '_': 27
}

#devuelve el número de pares clave-valor en el diccionario. En este caso, debería devolver 28.
modulo_utilizado = len(diccionario_encryt)
# Diccionario para desencriptar: convierte números a letras
diccionario_decrypt = {str(i): ch for ch, i in diccionario_encryt.items()}

# Matriz llave fija (Cambiar a gusto)
key = np.array([[4, 3, 1], [2, 2, 1], [1, 1, 1]])

def mod_inv(a, m):
    """ Encuentra el inverso modular de a módulo m usando el algoritmo extendido de Euclides. """
    m0, x0, x1 = m, 0, 1  # Inicializa variables: m0 es el módulo original, x0 y x1 son coeficientes para el inverso
    if m == 1:
        return 0  # Si el módulo es 1, el inverso es siempre 0, ya que no hay inverso en este caso
    
    while a > 1:
        q = a // m  # Encuentra el cociente entero de la división de a entre m
        m, a = a % m, m  # Actualiza a como el residuo de la división, y m como el valor antiguo de a
        x0, x1 = x1 - q * x0, x0  # Actualiza los coeficientes x0 y x1 según el algoritmo extendido de Euclides
    
    if x1 < 0:
        x1 += m0  # Asegura que el inverso sea positivo ajustando si es negativo
    
    return x1  # Retorna el inverso modular


def invert_matrix_mod(matrix, mod):
    matrix = np.array(matrix)
    det = int(round(np.linalg.det(matrix)))  # Determinante de la matriz
    
    if det == 0:
        raise ValueError("La matriz no es invertible.")
    
    det_inv = mod_inv(det, mod)  # Inverso modular del determinante
    
    matrix_inv = np.linalg.inv(matrix)  # Inversa de la matriz en números reales
    matrix_inv = np.round(matrix_inv).astype(int)  # Redondear a enteros

    # Aplicar el inverso modular a la matriz inversa
    matrix_inv_mod = (matrix_inv * det_inv) % mod
    return matrix_inv_mod

def encriptar(message, key):
    """ Encripta un mensaje usando una matriz llave.
    
    Args:
        message (str): Mensaje a encriptar.
        key (array): Matriz llave para encriptación.

    Returns:
        str: Mensaje encriptado.
    """
    message = message.upper()
    size = len(key)

    # Si el tamaño del mensaje es menor que el tamaño de la clave, añadir 'X' 
    while len(message) % size != 0:
        message += 'X'

    ciphertext = ''
    for i in range(0, len(message), size):
        block = message[i:i + size]
        matrix_mensaje = np.array([diccionario_encryt[char] for char in block])
        matrix_mensaje = np.reshape(matrix_mensaje, (size, 1))
        cifrado = np.matmul(key, matrix_mensaje) % modulo_utilizado  # Usar módulo 28
        ciphertext += ''.join(diccionario_decrypt[str(int(num))] for num in cifrado.flatten())

    return ciphertext

def desencriptar(message, key):
    size = len(key)
    
    try:
        # Intentar calcular la matriz inversa
        matrix_inversa = invert_matrix_mod(key, modulo_utilizado)  # Usar módulo 28
        matrix_inversa = np.array(matrix_inversa).astype(float)
    except Exception as e:
        print(f"Error al calcular la matriz inversa: {e}")
        return ""

    plaintext = ''
    for i in range(0, len(message), size):
        block = message[i:i + size]
        matrix_mensaje = np.array([diccionario_encryt[char] for char in block])
        matrix_mensaje = np.reshape(matrix_mensaje, (size, 1))
        cifrado = np.matmul(matrix_inversa, matrix_mensaje) % modulo_utilizado  # Usar módulo 28
        plaintext += ''.join(diccionario_decrypt[str(int(num))] for num in cifrado.flatten())

    # Eliminación del relleno de 'X'
    plaintext = plaintext.rstrip('X')
    return plaintext

if __name__ == "__main__":
    message = input("Escriba el mensaje a Encriptar: \n")
    print("Mensaje original:", message)

    encrypted = encriptar(message, key)
    print("Mensaje encriptado:", encrypted)

    decrypted = desencriptar(encrypted, key)
    print("Mensaje desencriptado:", decrypted)
    
    print("Diccionario Utilizado: {}\nModulo #{}".format(diccionario_encryt, modulo_utilizado))

