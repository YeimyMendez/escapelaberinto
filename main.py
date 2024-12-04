import pygame
import sys
from utils import dibujar_laberinto, mover_jugador, mover_enemigo, verificar_colisiones

# Inicialización de Pygame
pygame.init()

# Tamaño de los bloques y configuración de la pantalla
bloque_tamaño = 50
laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 'S'],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

filas = len(laberinto)
columnas = len(laberinto[0])
ANCHO = columnas * bloque_tamaño
ALTO = filas * bloque_tamaño + 50  # Espacio adicional para el texto
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Escape del Laberinto Espacial")

# Configuración del tiempo
TIEMPO_LIMITE = 60  # Segundos
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 24)

# Cargar imágenes
nave = pygame.image.load("assets/spaceship.png")
nave = pygame.transform.scale(nave, (bloque_tamaño, bloque_tamaño))
enemigo = pygame.image.load("assets/enemy.png")
enemigo = pygame.transform.scale(enemigo, (bloque_tamaño, bloque_tamaño))
fondo_original = pygame.image.load("assets/background.jpg")
fondo = pygame.transform.scale(fondo_original, (ANCHO, ALTO - 50))

# Posiciones iniciales
jugador_pos = [1, 1]  # Fila, Columna
enemigo_pos = [5, 5]

# Bucle principal
tiempo_inicio = pygame.time.get_ticks()
ejecutando = True
while ejecutando:
    pantalla.fill((0, 0, 0))
    pantalla.blit(fondo, (0, 50))

    # Dibujar laberinto
    dibujar_laberinto(pantalla, laberinto, bloque_tamaño, enemigo, nave, jugador_pos, enemigo_pos)

    # Mostrar tiempo restante
    tiempo_actual = pygame.time.get_ticks()
    tiempo_transcurrido = (tiempo_actual - tiempo_inicio) // 1000
    tiempo_restante = max(0, TIEMPO_LIMITE - tiempo_transcurrido)
    texto_tiempo = fuente.render(f"Tiempo restante: {tiempo_restante}s", True, (255, 255, 255))
    pantalla.blit(texto_tiempo, (10, 10))

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False

    # Mover jugador y enemigo
    mover_jugador(evento, jugador_pos, laberinto)
    mover_enemigo(enemigo_pos, jugador_pos, laberinto)

    # Verificar colisiones
    if verificar_colisiones(jugador_pos, enemigo_pos):
        print("¡Has sido atrapado por el enemigo! Perdiste.")
        ejecutando = False

    # Verificar si el jugador llegó a la salida
    if laberinto[jugador_pos[0]][jugador_pos[1]] == 'S':
        print("¡Has encontrado la salida! Ganaste.")
        ejecutando = False

    # Verificar si se acabó el tiempo
    if tiempo_restante == 0:
        print("¡Se acabó el tiempo! Perdiste.")
        ejecutando = False

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()
