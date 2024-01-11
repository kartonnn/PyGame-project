#by karton
import pygame
import sys
import random

pygame.init()
width, height = 1200, 675
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Провода")
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
square_positions = [(100, i * 150 + 100) for i in range(4)]
random.shuffle(square_positions)

line_positions = [(width - 140, i * 150 + 100) for i in range(4)]
random.shuffle(line_positions)
lines = []


class Square:
    def __init__(self, pos, color):
        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
running = True
dragging = False
current_line_start = None
current_color = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for pos, color in zip(square_positions + line_positions, colors * 2):
                square_rect = pygame.Rect(pos[0], pos[1], 40, 40)
                if square_rect.collidepoint(event.pos):
                    dragging = True
                    current_line_start = pos
                    current_color = color
                    break
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            for pos, color in zip(line_positions, colors):
                line_rect = pygame.Rect(pos[0], pos[1], 40, 40)
                if line_rect.collidepoint(event.pos) and current_color == color:
                    lines.append((current_line_start, pos, current_color))
                    dragging = False
                    break
            dragging = False

    screen.fill((0, 0, 0))
    for pos, color in zip(square_positions + line_positions, colors * 2):
        pygame.draw.rect(screen, color, (pos[0], pos[1], 40, 40))
    if dragging and current_line_start:
        pygame.draw.line(screen, current_color, current_line_start, pygame.mouse.get_pos(), 5)
    for line in lines:
        pygame.draw.line(screen, line[2], line[0], line[1], 5)
    if len(lines) == 4:
        font = pygame.font.SysFont(None, 100)
        text = font.render('Done!', True, (0, 255, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
