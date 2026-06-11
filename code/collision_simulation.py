import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 1200, 650  # Ukuran layar baru
BACKGROUND_COLOR = (240, 248, 255)  # Light blue background
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
PINK = (255, 182, 193)
GRAY = (200, 200, 200)
DARK_GRAY = (169, 169, 169)
RED = (220, 20, 60)
GREEN = (34, 139, 34)

# Load background image
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
ball_image = pygame.image.load("football.png")

# Screen and clock setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulasi Tumbukan Bola")
clock = pygame.time.Clock()

# Slider class for user inputs
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label, color=GRAY):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.handle = pygame.Rect(x + (initial_val - min_val) / (max_val - min_val) * w - h // 2, y, h, h)
        self.active = False
        self.label = label

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.ellipse(screen, DARK_GRAY if not self.active else GREEN, self.handle)
        label_text = font.render(f"{self.label}: {self.value:.2f}", True, BLACK)
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle.collidepoint(event.pos):
            self.active = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.active = False

        if self.active and event.type == pygame.MOUSEMOTION:
            mouse_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            self.handle.centerx = mouse_x
            self.value = self.min_val + (mouse_x - self.rect.left) / self.rect.width * (self.max_val - self.min_val)

# Ball class
class Ball:
    BASE_RADIUS = 20

    def __init__(self, x, y, mass, color, velocity):
        self.x = x
        self.y = y
        self.mass = mass
        self.color = color
        self.velocity = velocity

    @property
    def radius(self):
        return max(10, Ball.BASE_RADIUS * math.sqrt(self.mass))

    def draw(self, screen):
        # Scale the ball image based on the radius
        scaled_image = pygame.transform.scale(ball_image, (int(self.radius * 2), int(self.radius * 2)))
        # Draw the ball image centered on its position
        screen.blit(scaled_image, (int(self.x - self.radius), int(self.y - self.radius)))

    def move(self):
        self.x += self.velocity

# Button class
class Button:
    def __init__(self, x, y, w, h, color, text, font, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text
        self.font = font
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2,
                                   self.rect.centery - text_surface.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

# Initialize objects
ball1 = Ball(WIDTH // 4, HEIGHT // 2, 0.5, BLUE, 2)  # Posisi bola 1
ball2 = Ball(3 * WIDTH // 4, HEIGHT // 2, 1.5, PINK, -1)  # Posisi bola 2

# Initialize Timer
start_time = None  
elapsed_time = 0 

sliders = [
    Slider(100, 515, 200, 10, 0.1, 5.0, 0.5, "Mass 1 (Kg)"),
    Slider(400, 515, 200, 10, 0.1, 5.0, 1.5, "Mass 2 (Kg)"),
    Slider(100, 580, 200, 10, -10.0, 10.0, 2.0, "Velocity 1 (m/s)"),
    Slider(400, 580, 200, 10, -10.0, 10.0, -1.0, "Velocity 2 (m/s)"),
    Slider(700, 514, 200, 10, 0.0, 1.0, 1.0, "Elasticity")
]

# Button actions
def start_simulation():
    global simulating, start_time
    simulating = True
    ball1.mass = sliders[0].value
    ball2.mass = sliders[1].value
    ball1.velocity = sliders[2].value
    ball2.velocity = sliders[3].value
    start_time = pygame.time.get_ticks()  # Catat waktu saat simulasi dimulai

def reset_simulation():
    global simulating, start_time, elapsed_time
    simulating = False
    ball1.x, ball2.x = WIDTH // 4, 3 * WIDTH // 4
    ball1.velocity, ball2.velocity = sliders[2].value, sliders[3].value
    start_time = 0  # Reset waktu awal simulasi
    elapsed_time = 0  # Reset waktu berjalan

def toggle_pause():
    global simulating, elapsed_time, start_time
    simulating = not simulating
    if not simulating:
        elapsed_time += (pygame.time.get_ticks() - start_time) / 1000  # Tambahkan waktu saat ini ke total waktu berjalan

font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 36)

# Buttons
buttons = [
    Button(1015, 490, 100, 40, GREEN, "Play", font, start_simulation),
    Button(1015, 540, 100, 40, RED, "Restart", font, reset_simulation),
    Button(1015, 590, 100, 40, DARK_GRAY, "Pause", font, toggle_pause)  # Tombol Pause
]

running = True
simulating = False

while running:
    screen.blit(background_image, (0, 0))  # Gambar background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for slider in sliders:
            slider.handle_event(event)
        for button in buttons:
            button.handle_event(event)

        if simulating:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 
    # Update massa dan ukuran bola berdasarkan slider
    ball1.mass = sliders[0].value
    ball2.mass = sliders[1].value

    # Perbarui kecepatan juga saat simulasi belum berjalan
    if not simulating:
        ball1.velocity = sliders[2].value
        ball2.velocity = sliders[3].value

    if simulating:
        if abs(ball1.x - ball2.x) <= ball1.radius + ball2.radius:
            m1, m2 = ball1.mass, ball2.mass
            v1, v2 = ball1.velocity, ball2.velocity
            e = sliders[4].value

            if e >= 0.7:
                v1_final = ((m1 - e * m2) * v1 + (1 + e) * m2 * v2) / (m1 + m2)
                v2_final = ((m2 - e * m1) * v2 + (1 + e) * m1 * v1) / (m1 + m2)
                ball1.velocity, ball2.velocity = v1_final, v2_final
            elif 0.2 <= e < 0.7:
                momentum1 = m1 * v1
                momentum2 = m2 * v2
                if abs(momentum1) > abs(momentum2):
                    ball1.velocity = v1 * 0.5
                    ball2.velocity = 0
                else:
                    ball2.velocity = v2 * 0.5
                    ball1.velocity = 0
            elif e < 0.2:
                ball1.velocity = ball2.velocity = 0

        ball1.move()
        ball2.move()

        if abs(ball1.velocity) < 0.01:
            ball1.velocity = 0
        if abs(ball2.velocity) < 0.01:
            ball2.velocity = 0

    # Gambar objek di layar
    ball1.draw(screen)
    ball2.draw(screen)

    for slider in sliders:
        slider.draw(screen, font)
    for button in buttons:
        button.draw(screen)
# Gambarkan waktu berjalan
    time_text = font.render(f"Time Elapsed: {elapsed_time:.2f} s", True, BLACK)
    screen.blit(time_text, (700, 550))  # Atur posisi teks di layar
    
    # Tambahkan keterangan di bawah masing-masing bola
    label_ball1 = font.render("Bola 1", True, BLACK)
    label_ball2 = font.render("Bola 2", True, BLACK)
    screen.blit(label_ball1, (ball1.x - ball1.radius, ball1.y + ball1.radius + 5))
    screen.blit(label_ball2, (ball2.x - ball2.radius, ball2.y + ball2.radius + 5))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
