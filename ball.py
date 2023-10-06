import pygame
import math
import time
import sys

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
def configurar_ventana(width, height):
    return pygame.display.set_mode((width, height))

# Función para reiniciar el juego para un jugador
def reiniciar_juego(jugador):
    jugador['ball_x'] = 50 if jugador['numero'] == 1 else WIDTH - 50
    jugador['ball_y'] = HEIGHT - 50
    jugador['angle_degrees'] = 45
    jugador['angle_radians'] = math.radians(jugador['angle_degrees'])
    jugador['initial_speed'] = 30
    jugador['gravity'] = 0.5
    jugador['pressed_enter'] = False
    jugador['show_line'] = True
    jugador['ball_stopped'] = False

# Dibuja la pantalla del juego
def dibujar_pantalla(screen, jugador):
    screen.fill(WHITE)

    if jugador['show_line']:
        line_length = 20
        line_end_x = jugador['ball_x'] + line_length * math.cos(jugador['angle_radians'])
        line_end_y = jugador['ball_y'] - line_length * math.sin(jugador['angle_radians'])
        pygame.draw.line(screen, RED, (jugador['ball_x'], jugador['ball_y']), (line_end_x, line_end_y), 2)


    pygame.draw.circle(screen, BLUE, (int(jugador['ball_x']), int(jugador['ball_y'])), jugador['ball_radius'])
    pygame.draw.circle(screen, RED, (int(jugador['target_x']), int(jugador['target_y'])), jugador['ball_radius'])


    font = pygame.font.Font(None, 36)
    text = font.render(f"Jugador {jugador['numero']}", True, BLUE)
    text_rect = text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(text, text_rect)

    pygame.display.flip()

# Función principal del juego
def jugar_juego():
    # Configuración de jugadores
    jugador1 = {
        'numero': 1,
        'ball_radius': 10,
        'ball_x': 50,
        'ball_y': HEIGHT - 50,
        'angle_degrees': 45,
        'angle_radians': math.radians(45),
        'initial_speed': 30,
        'gravity': 0.5,
        'pressed_enter': False,
        'show_line': True,
        'ball_stopped': False,
        'current': True,
        'target_x': WIDTH - 50,
        'target_y': HEIGHT - 50
    }

    jugador2 = {
        'numero': 2,
        'ball_radius': 10,
        'ball_x': WIDTH - 50,
        'ball_y': HEIGHT - 50,
        'angle_degrees': 135,
        'angle_radians': math.radians(45),
        'initial_speed': 30,
        'gravity': 0.5,
        'pressed_enter': False,
        'show_line': True,
        'ball_stopped': False,
        'current': False,
        'target_x':  50,
        'target_y': HEIGHT - 50
    }

    jugadores = [jugador1, jugador2]
    screen = configurar_ventana(WIDTH, HEIGHT)
    pygame.display.set_caption("Movimiento Parabólico")

    reiniciar_juego(jugador1)
    reiniciar_juego(jugador2)

    # Tiempo para mostrar la línea de inicio (en segundos)
    start_line_duration = 3.0  # Cambia este valor según tus preferencias

    # Marca el tiempo de inicio
    start_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Solo el jugador actual procesa eventos de teclado
        jugador_actual = jugadores[0] if jugadores[0]['current'] else jugadores[1]
        keys = pygame.key.get_pressed()
        if not jugador_actual['ball_stopped']:
            if keys[pygame.K_RETURN] and not jugador_actual['pressed_enter']:
                # Si se presiona Enter y el movimiento no ha comenzado
                jugador_actual['pressed_enter'] = True
                jugador_actual['angle_radians'] = math.radians(jugador_actual['angle_degrees'])
                jugador_actual['initial_speed_x'] = jugador_actual['initial_speed'] * math.cos(jugador_actual['angle_radians'])
                jugador_actual['initial_speed_y'] = -jugador_actual['initial_speed'] * math.sin(jugador_actual['angle_radians'])
            elif keys[pygame.K_DOWN]:
                # Reduce el ángulo de disparo
                jugador_actual['angle_degrees'] -= 2
                jugador_actual['angle_radians'] = math.radians(jugador_actual['angle_degrees'])
            elif keys[pygame.K_UP]:
                # Aumenta el ángulo de disparo
                jugador_actual['angle_degrees'] += 2
                jugador_actual['angle_radians'] = math.radians(jugador_actual['angle_degrees'])

        if jugador_actual['pressed_enter'] and not jugador_actual['ball_stopped']:
            # Actualiza la posición de la pelota en función del tiempo si se ha presionado Enter
            jugador_actual['show_line'] = False
            jugador_actual['ball_x'] += jugador_actual['initial_speed_x']
            jugador_actual['ball_y'] += jugador_actual['initial_speed_y']

            # Aplica gravedad
            jugador_actual['initial_speed_y'] += jugador_actual['gravity']

            # Verifica si la pelota ha colisionado con el suelo
            if jugador_actual['ball_y'] >= HEIGHT - jugador_actual['ball_radius']:
                print(f"La pelota del jugador {jugador_actual['numero']} ha alcanzado el suelo.")
                time.sleep(2)  # Espera 2 segundos antes de reiniciar el juego
                reiniciar_juego(jugador_actual)
                # Cambiar al otro jugador
                jugador_actual['current'] = not jugador_actual['current']

        # Dibuja la pantalla solo para el jugador actual
        dibujar_pantalla(screen, jugador_actual)

        # Agrega un pequeño retraso para ralentizar la visualización
        time.sleep(0.02)  # Ajusta el valor según la velocidad deseada

if __name__ == "__main__":
    jugar_juego()

