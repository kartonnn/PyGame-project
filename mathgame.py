#by karton
import pygame
import random
import time

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Математическая головоломка")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font(None, 52)

running = True
score = 0
question = ''
answer = ''
start_time = time.time()
game_duration = 30


def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return f"{num1} x {num2}", num1 * num2

question, correct_answer = generate_question()

while running:
    screen.fill(WHITE)
    time_left = game_duration - (time.time() - start_time)
    if time_left <= 0:
        font1 = pygame.font.Font(None, 100)
        score_surf_end = font1.render(f'Ваш счет: {score}', True, BLACK)
        screen.blit(score_surf_end, (screen_width // 2 - 280, screen_height // 2 - 100))
        pygame.display.update()
        time.sleep(3)
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if answer == str(correct_answer):
                    score += 1
                    question, correct_answer = generate_question()
                answer = ''
            elif event.key == pygame.K_BACKSPACE:
                answer = answer[:-1]
            else:
                answer += event.unicode
    question_surf = font.render(question, True, BLACK)
    screen.blit(question_surf, (50, 50))
    answer_surf = font.render(answer, True, BLACK)
    screen.blit(answer_surf, (50, 100))
    score_surf = font.render(f'Счет: {score}', True, BLACK)
    screen.blit(score_surf, (50, 150))
    time_surf = font.render(f'Время: {int(time_left)}', True, BLACK)
    screen.blit(time_surf, (50, 200))

    pygame.display.flip()

pygame.quit()