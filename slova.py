#by karton
import pygame
import random
import sys

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Собери слово")

BLACK = (0, 0, 0)

font = pygame.font.Font(None, 42)
text = 'СОБЕРИ СЛОВО'
text_surface = font.render(text, True, BLACK)

words = ['КАСТРЮЛЯ', 'ОГЭ', 'ЛИСА', 'МИШКА', 'КОЗЁЛ', 'ФРАНЦИЯ', 'КАРТОН']
word = random.choice(words)
shuffled_letters = random.sample(word, len(word))
selected_letters = []
letter_rects = {}
game_finished = False


for i, letter in enumerate(shuffled_letters):
    letter_surf = font.render(letter, True, BLACK)
    letter_rect = letter_surf.get_rect(center=(50 + i * 60, 550))
    letter_rects[letter] = letter_rect


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for letter, rect in letter_rects.items():
                if rect.collidepoint(event.pos):
                    if letter in selected_letters:
                        selected_letters.remove(letter)
                    else:
                        selected_letters.append(letter)
                    break
    screen.fill((217, 113, 11))
    screen.blit(text_surface, (250, 50))
    y_coord = 350
    pygame.draw.line(screen, BLACK, (100, y_coord), (700, y_coord), 5)

    for i, letter in enumerate(shuffled_letters):
        letter_surf = font.render(letter, True, BLACK)
        if letter in selected_letters:
            letter_rects[letter].center = (230 + selected_letters.index(letter) * 60, 320)
        else:
            letter_rects[letter].center = (230 + i * 60, 450)
        screen.blit(letter_surf, letter_rects[letter].topleft)

    if ''.join(selected_letters) == word:
        game_finished = True

    if game_finished:
        done_surf = font.render('Done', True, (20, 140, 5))
        done_rect = done_surf.get_rect(center=(screen_width // 2 - 50, screen_height // 2 - 70))
        screen.blit(done_surf, done_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
