import pygame
import sys
from button import ImageButton

pygame.init()
weight, height = 1600, 914
screen = pygame.display.set_mode((weight, height))
pygame.display.set_caption('КОТОПЁС')
main_bg = pygame.image.load('bg.jfif')
FPS = 60
clock = pygame.time.Clock()
cursor_image = pygame.image.load('cursor.png')
pygame.mouse.set_visible(False)
sound = pygame.mixer.Sound('Panthetic - crimewave - sped up.mp3')
sound.play()


def main_menu():
    running = True
    start_button = ImageButton(weight / 2 - (252 / 2), 200, 252, 74, 'PLAY', 'start button.png ', 'start button 2.png',
                               'negromkiy-korotkiy-klik.mp3')
    options_button = ImageButton(weight / 2 - (252 / 2), 350, 252, 74, 'OPTIONS', 'start button.png ', 'start button 2.png',
                                 'negromkiy-korotkiy-klik.mp3')
    exit_button = ImageButton(weight / 2 - (252 / 2), 500, 252, 74, 'EXITE', 'start button.png ', 'start button 2.png',
                              'negromkiy-korotkiy-klik.mp3')

    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_bg, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('КОТОПЁС', True, ('red'))
        text_rect = text_surface.get_rect(center=(weight / 2, 50))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == start_button:
                new_game()
            if event.type == pygame.USEREVENT and event.button == options_button:
                settings_menu()
            if event.type == pygame.USEREVENT and event.button == exit_button:
                sys.exit()
            for btn in [start_button, options_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, options_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        if pygame.mouse.get_focused():
            mouse_position = pygame.mouse.get_pos()
            screen.blit(cursor_image, mouse_position)
        pygame.display.flip()
        clock.tick(FPS)


def settings_menu():
    audio_button = ImageButton(weight / 2 - (252 / 2), 200, 252, 74, 'AUDIO', 'start button.png ', 'start button 2.png',
                               'negromkiy-korotkiy-klik.mp3')
    video_button = ImageButton(weight / 2 - (252 / 2), 350, 252, 74, 'VIDEO', 'start button.png ', 'start button 2.png',
                               'negromkiy-korotkiy-klik.mp3')
    back_button = ImageButton(weight / 2 - (252 / 2), 500, 252, 74, 'BACK', 'start button.png ', 'start button 2.png',
                              'negromkiy-korotkiy-klik.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_bg, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('SETTINGS', True, ('red'))
        text_rect = text_surface.get_rect(center=(weight / 2 - (252/2), 50))
        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back_button:
                main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.USEREVENT and event.button == video_button:
                video()
                for btn in [audio_button, video_button, back_button]:
                    btn.set_pos(weight / 2 - (252 / 2))

            for btn in [audio_button, video_button, back_button]:
                btn.handle_event(event)

        for btn in [audio_button, video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        if pygame.mouse.get_focused():
            mouse_position = pygame.mouse.get_pos()
            screen.blit(cursor_image, mouse_position)
        pygame.display.flip()
    clock.tick(FPS)


def new_game():
    back_button = ImageButton(weight / 2 - (252 / 2), 500, 252, 74, 'BACK', 'start button.png ', 'start button 2.png',
                              'negromkiy-korotkiy-klik.mp3')
    new_game_button = ImageButton(weight / 2 - (252 / 2), 300, 252, 74, 'NEW GAME', 'start button.png ', 'start button 2.png',
                              'negromkiy-korotkiy-klik.mp3')
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_bg, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('GAME', True, ('red'))
        text_rect = text_surface.get_rect(center=(weight / 2, 50))
        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            for btn in [back_button]:
                btn.handle_event(event)
            if event.type == pygame.USEREVENT and event.button == back_button:
                main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        for btn in [back_button, new_game_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
        if pygame.mouse.get_focused():
            mouse_position = pygame.mouse.get_pos()
            screen.blit(cursor_image, mouse_position)
        pygame.display.flip()
    clock.tick(FPS)


def video():
    fullhd_button = ImageButton(weight / 2 - (252 / 2), 200, 252, 74, 'FULL HD', 'start button.png ', 'start button 2.png',
                               'negromkiy-korotkiy-klik.mp3')
    nine_button = ImageButton(weight / 2 - (252 / 2), 350, 252, 74, '1600x914', 'start button.png ', 'start button 2.png',
                               'negromkiy-korotkiy-klik.mp3')
    twel_button = ImageButton(weight / 2 - (252 / 2), 500, 252, 74, '1280x800', 'start button.png ', 'start button 2.png',
                              'negromkiy-korotkiy-klik.mp3')
    back_button = ImageButton(weight / 2 - (252 / 2), 650, 252, 74, 'BACK', 'start button.png ', 'start button 2.png',
                              'negromkiy-korotkiy-klik.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_bg, (0, 0))
        font = pygame.font.Font(None, 72)
        text_surface = font.render('VIDEO SETTINGS', True, ('red'))
        text_rect = text_surface.get_rect(center=(weight / 2, 50))
        screen.blit(text_surface, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            for btn in [fullhd_button, twel_button, back_button, nine_button]:
                 btn.handle_event(event)

            if event.type == pygame.USEREVENT and event.button == back_button:
                settings_menu()
            if event.type == pygame.USEREVENT and event.button == twel_button:
                change_video_mode(1280, 800)
            if event.type == pygame.USEREVENT and event.button == fullhd_button:
                change_video_mode(1920, 1080, pygame.FULLSCREEN)
            if event.type == pygame.USEREVENT and event.button == nine_button:
                change_video_mode(1600, 914)

        for btn in [fullhd_button, twel_button, back_button, nine_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        if pygame.mouse.get_focused():
            mouse_position = pygame.mouse.get_pos()
            screen.blit(cursor_image, mouse_position)
        pygame.display.flip()
        clock.tick(FPS)


def change_video_mode(w, h, fullscreen=0):
    global weight, height, screen, main_bg
    weight, height = w, h
    screen = pygame.display.set_mode((weight, height), fullscreen)
    main_bg = pygame.image.load(f'bg{weight}.png')

#def change_audio_mode():


if __name__ == '__main__':
    main_menu()
