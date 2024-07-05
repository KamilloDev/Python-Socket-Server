import socket
import threading
import pygame
from pygame.locals import *

def send_message():
    message = f"{username}: {input_box.text}"
    if message:
        client_socket.send(message.encode('utf-8'))
        input_box.text = ""

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_history.append(message)
        except:
            break

# Initialize Pygame
pygame.init()

# Set up the Pygame window
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chat Room")

# Set up fonts
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 28)

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Input box class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = input_font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    send_message()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = input_font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Create the socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.207.1.146', 5555))

# Get the username from the user
username = input("Enter your username: ")

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Input box for typing messages
input_box = InputBox(10, HEIGHT-40, WIDTH-20, 30)

# List to store chat history
chat_history = []

# Run the Pygame main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_box.handle_event(event)

    input_box.update()

    # Draw the background
    screen.fill(WHITE)

    # Draw chat history
    y = 10
    for message in chat_history:
        text_surface = font.render(message, True, BLACK)
        screen.blit(text_surface, (10, y))
        y += text_surface.get_height() + 5

    # Draw the input box
    input_box.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
