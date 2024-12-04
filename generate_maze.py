import random

def generar_laberinto(filas, columnas):
    # Crear la cuadrícula inicial (todas paredes)
    laberinto = [[1 for _ in range(columnas)] for _ in range(filas)]

    # Función auxiliar para obtener vecinos válidos
    def obtener_vecinos(x, y):
        vecinos = []
        if x > 1: vecinos.append((x - 2, y))  # Arriba
        if x < filas - 2: vecinos.append((x + 2, y))  # Abajo
        if y > 1: vecinos.append((x, y - 2))  # Izquierda
        if y < columnas - 2: vecinos.append((x, y + 2))  # Derecha
        return vecinos

    # Empezar en una celda inicial aleatoria
    inicio_x, inicio_y = random.randrange(1, filas, 2), random.randrange(1, columnas, 2)
    laberinto[inicio_x][inicio_y] = 0  # Marcar como espacio
    pila = [(inicio_x, inicio_y)]  # Pila para DFS

    while pila:
        x, y = pila[-1]
        vecinos = [(nx, ny) for nx, ny in obtener_vecinos(x, y) if laberinto[nx][ny] == 1]

        if vecinos:
            # Elegir un vecino al azar
            nx, ny = random.choice(vecinos)
            # Eliminar la pared entre la celda actual y el vecino
            laberinto[(x + nx) // 2][(y + ny) // 2] = 0
            laberinto[nx][ny] = 0  # Marcar el vecino como visitado
            pila.append((nx, ny))  # Avanzar al vecino
        else:
            pila.pop()  # Retroceder si no hay vecinos no visitados

    # Colocar la entrada y salida
    laberinto[1][0] = 0  # Entrada
    laberinto[filas - 2][columnas - 1] = 'S'  # Salida

    return laberinto
