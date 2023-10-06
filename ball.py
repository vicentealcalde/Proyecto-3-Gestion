import pygame
import math
import time
import random
 
# Función para reiniciar el juego
def reiniciar_juego():
    # Restablece las variables del juego
    global ball_x, ball_y, angle_degrees, initial_speed, angle_radians, initial_speed_x, initial_speed_y, pressed_enter, show_line, current_player
    ball_x = 50
    ball_y = HEIGHT - 50
    angle_degrees = 45
    initial_speed = 30
    angle_radians = math.radians(angle_degrees)
    initial_speed_x = initial_speed * math.cos(angle_radians)
    initial_speed_y = -initial_speed * math.sin(angle_radians)
    pressed_enter = False
    show_line = True
    current_player = 1  # Comienza con el jugador 1

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movimiento Parabólico")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Posición y dimensiones de la pelota
ball_radius = 10
ball_x = 50
ball_y = HEIGHT - 50
angle_degrees = 45  # Ángulo de disparo en grados
initial_speed = 30   # Velocidad inicial

# Gravedad
gravity = 0.5

# Convierte el ángulo de disparo a radianes
angle_radians = math.radians(angle_degrees)

# Velocidad inicial en las componentes x e y
initial_speed_x = initial_speed * math.cos(angle_radians)
initial_speed_y = -initial_speed * math.sin(angle_radians)

# Coordenadas del objetivo en el otro lado del campo
target_x = WIDTH - 50
target_y = HEIGHT - 50
target_radius = 15

# Variables del obstáculo
obstacle_width = 60
obstacle_height = 20
obstacle_x = random.randint(0, WIDTH - obstacle_width)
obstacle_y = random.randint(20, 150)

# Variable para rastrear si se ha presionado Enter para comenzar el movimiento
pressed_enter = False
# Variable para rastrear si se ha presionado Enter para mostrar u ocultar la línea
show_line = True
# Variable para rastrear si la pelota está detenida por colisión con el obstáculo
ball_stopped = False
# Variable para rastrear al jugador actual (1 o 2)
current_player = 1

# Tiempo para mostrar la línea de inicio (en segundos)
start_line_duration = 3.0  # Cambia este valor según tus preferencias

# Marca el tiempo de inicio
start_time = time.time()

# Bucle principal del juego
while True:  # Bucle que reinicia el juego hasta que se anote un gol
    running = True  # Bandera para el bucle del juego
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not pressed_enter:
                    # Si se presiona Enter y el movimiento no ha comenzado
                    pressed_enter = True
                    angle_radians = math.radians(angle_degrees)
                    initial_speed_x = initial_speed * math.cos(angle_radians)
                    initial_speed_y = -initial_speed * math.sin(angle_radians)
                elif event.key == pygame.K_DOWN:
                    # Reduce el ángulo de disparo
                    angle_degrees -= 5
                    angle_radians = math.radians(angle_degrees)
                elif event.key == pygame.K_UP:
                    # Aumenta el ángulo de disparo
                    angle_degrees += 5
                    angle_radians = math.radians(angle_degrees)
                elif event.key == pygame.K_SPACE and not ball_stopped:
                    # Realiza un disparo si se presiona la barra espaciadora y la pelota no está detenida
                    current_player = 3 - current_player  # Cambia al otro jugador (1 <-> 2)
                    pressed_enter = False  # Permite al nuevo jugador presionar Enter para disparar

        if pressed_enter and not ball_stopped:
            # Actualiza la posición de la pelota en función del tiempo si se ha presionado Enter
            show_line = False
            ball_x += initial_speed_x 
            ball_y += initial_speed_y

            # Aplica gravedad
            initial_speed_y += gravity

            # Verifica si la pelota ha colisionado con el objetivo
            distance_to_target = math.sqrt((ball_x - target_x)**2 + (ball_y - target_y)**2)
            if distance_to_target < ball_radius + target_radius:
                print(f"¡Gol del jugador {current_player}! La pelota ha alcanzado el objetivo.")
                time.sleep(2)  # Espera 2 segundos antes de reiniciar el juego
                reiniciar_juego()

            # Verifica si la pelota ha colisionado con el obstáculo
            if (obstacle_x < ball_x < obstacle_x + obstacle_width and
                obstacle_y < ball_y < obstacle_y + obstacle_height):
                initial_speed_x = 1
                initial_speed_y = 1
                print(f"La pelota del jugador {current_player} ha golpeado el obstáculo.")
               

        # Dibuja la pantalla
        screen.fill(WHITE)

        # Dibuja la línea roja que parte desde el centro del círculo
        if show_line:
            line_length = 20
            line_end_x = ball_x + line_length * math.cos(angle_radians)
            line_end_y = ball_y - line_length * math.sin(angle_radians)
            pygame.draw.line(screen, RED, (ball_x, ball_y), (line_end_x, line_end_y), 2)

        # Dibuja la pelota
        pygame.draw.circle(screen, BLUE, (int(ball_x), int(ball_y)), ball_radius)

        # Dibuja el objetivo
        pygame.draw.circle(screen, RED, (int(target_x), int(target_y)), target_radius)

        # Dibuja el obstáculo
        pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

        # Dibuja el texto para indicar el jugador actual
        font = pygame.font.Font(None, 36)
        text = font.render(f"Jugador {current_player}", True, BLUE)
        text_rect = text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(text, text_rect)

        # Actualiza la pantalla
        pygame.display.flip()

        # Verifica si la pelota ha alcanzado el suelo
        if ball_y >= HEIGHT - ball_radius:
            print(f"La pelota del jugador {current_player} ha alcanzado el suelo.")
            time.sleep(2)  # Espera 2 segundos antes de reiniciar el juego
            reiniciar_juego()

        # Agrega un pequeño retraso para ralentizar la visualización
        time.sleep(0.02)  # Ajusta el valor según la velocidad deseada

    # Salir del juego
    pygame.quit()



