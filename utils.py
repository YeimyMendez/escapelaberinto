import pygame
import heapq
import time

# Definir una variable de tiempo para controlar la velocidad
ultimo_movimiento = time.time()  # Almacena el último momento en que se movió el enemigo
intervalo_movimiento = 0.5  # Intervalo en segundos (0.5 segundos por movimiento)

# Definir los 4 movimientos posibles (arriba, abajo, izquierda, derecha)
MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def dibujar_laberinto(pantalla, laberinto, bloque_tamaño, enemigo, nave, jugador_pos, enemigo_pos):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[fila])):
            x = columna * bloque_tamaño
            y = fila * bloque_tamaño + 50  # Desplazar por el texto superior

            if laberinto[fila][columna] == 1:
                pygame.draw.rect(pantalla, (0, 0, 0), (x, y, bloque_tamaño, bloque_tamaño))
            elif laberinto[fila][columna] == 0:
                pygame.draw.rect(pantalla, (100, 100, 100), (x, y, bloque_tamaño, bloque_tamaño))
            elif laberinto[fila][columna] == 'S':
                pygame.draw.rect(pantalla, (0, 255, 0), (x, y, bloque_tamaño, bloque_tamaño))

    # Dibujar jugador y enemigo
    pantalla.blit(nave, (jugador_pos[1] * bloque_tamaño, jugador_pos[0] * bloque_tamaño + 50))
    pantalla.blit(enemigo, (enemigo_pos[1] * bloque_tamaño, enemigo_pos[0] * bloque_tamaño + 50))

def mover_jugador(evento, jugador_pos, laberinto):
    if evento.type == pygame.KEYDOWN:
        nueva_pos = list(jugador_pos)
        if evento.key == pygame.K_UP:
            nueva_pos[0] -= 1
        elif evento.key == pygame.K_DOWN:
            nueva_pos[0] += 1
        elif evento.key == pygame.K_LEFT:
            nueva_pos[1] -= 1
        elif evento.key == pygame.K_RIGHT:
            nueva_pos[1] += 1

        if laberinto[nueva_pos[0]][nueva_pos[1]] != 1:  # Verificar si no es una pared
            jugador_pos[0], jugador_pos[1] = nueva_pos[0], nueva_pos[1]

def a_star(laberinto, inicio, objetivo):
    # Función para calcular el valor heurístico (distancia Manhattan)
    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Inicializar las estructuras
    open_list = []
    heapq.heappush(open_list, (0, inicio))  # Empujar la posición de inicio
    came_from = {}  # Diccionario que mantiene el camino
    g_score = {inicio: 0}  # Costo acumulado desde el inicio
    f_score = {inicio: heuristica(inicio, objetivo)}  # Costo estimado (g + h)

    while open_list:
        _, actual = heapq.heappop(open_list)

        # Si hemos llegado al objetivo, reconstruir el camino
        if actual == objetivo:
            path = []
            while actual in came_from:
                path.append(actual)
                actual = came_from[actual]
            path.reverse()
            return path  # Retorna el camino de regreso al objetivo

        # Explorar los vecinos
        for dx, dy in MOVIMIENTOS:
            vecino = (actual[0] + dx, actual[1] + dy)
            if 0 <= vecino[0] < len(laberinto) and 0 <= vecino[1] < len(laberinto[0]) and laberinto[vecino[0]][vecino[1]] != 1:
                # Calculamos los costos g y f
                tentative_g_score = g_score[actual] + 1
                if vecino not in g_score or tentative_g_score < g_score[vecino]:
                    came_from[vecino] = actual
                    g_score[vecino] = tentative_g_score
                    f_score[vecino] = tentative_g_score + heuristica(vecino, objetivo)
                    heapq.heappush(open_list, (f_score[vecino], vecino))

    return []  # Si no se encuentra un camino

def mover_enemigo(enemigo_pos, jugador_pos, laberinto):
    global ultimo_movimiento

    if time.time() - ultimo_movimiento > intervalo_movimiento:  # Verificar si ha pasado el intervalo
        # Usar A* para obtener el camino
        camino = a_star(laberinto, tuple(enemigo_pos), tuple(jugador_pos))

        if camino:
            siguiente_pos = camino[1]  # Tomamos la siguiente posición del camino

            # Mover el enemigo un paso
            if enemigo_pos[0] < siguiente_pos[0]:
                enemigo_pos[0] += 1
            elif enemigo_pos[0] > siguiente_pos[0]:
                enemigo_pos[0] -= 1

            if enemigo_pos[1] < siguiente_pos[1]:
                enemigo_pos[1] += 1
            elif enemigo_pos[1] > siguiente_pos[1]:
                enemigo_pos[1] -= 1

        ultimo_movimiento = time.time()  # Actualizar el tiempo del último movimiento



def verificar_colisiones(jugador_pos, enemigo_pos):
    return jugador_pos == enemigo_pos
