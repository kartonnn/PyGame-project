import pygame
import sys
import os
import time
import random


from data.golovolomki.mathgame import Mathgame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'door', 'stone'}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def load_image(name, colorkey=(255, 255, 255)):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        image.set_colorkey(colorkey)
    return image


def load_images(path, size):
    images = []
    for i in os.listdir('data/' + path):
        images.append(pygame.transform.scale(load_image(path + '/' + i, WHITE), (size, size)))
    return images


class Game:
    def __init__(self, round_number):
        pygame.init()
        pygame.display.set_caption('котопёс')
        self.screen = pygame.display.set_mode((640, 640))
        self.display = pygame.Surface((320, 320))

        self.clock = pygame.time.Clock()

        if round_number == 1:
            self.golovolomka_type = provoda
            self.tile_size = self.display.get_height() / 12
        elif round_number == 2:
            self.golovolomka_type = mathgame
            self.tile_size = self.display.get_height() / 17
        elif round_number == 3:
            self.golovolomka_type = slova
            self.tile_size = self.display.get_height() / 19

        self.coins = []
        self.collected_coins_sum = 0

        self.golovolomki = []
        self.golovolomki_completed = False
        self.golovolomka_passed = False

        self.door_rect = None

        self.exit_acsess = [False, False]

        self.movement_1 = [False, False]
        self.movement_2 = [False, False]

        self.assets = {
            'cat': pygame.transform.scale(load_image('player.png', WHITE), (25, 25)),
            'dog': pygame.transform.scale(load_image('dog.png', WHITE), (25, 25)),
            'decor': load_images('decor', self.tile_size),
            'door': load_images('door',  self.tile_size),
            'stone': load_images('stone',  self.tile_size)
        }

        self.tilemap = Tilemap(self, round_number)
        self.cat, self.dog = self.tilemap.render(1)

        self.jump_acsess_cat = True
        self.jump_acsess_dog = True

    def run(self):
        running = True
        while running:
            self.display.fill((0, 0, 0))
            self.exit_acsess = [False, False]
            self.tilemap.render()

            for coin in self.coins:
                coin.update()

            self.cat.update(self.tilemap, (self.movement_1[1] - self.movement_1[0], 0))
            self.cat.render(self.display)
            self.dog.update(self.tilemap, (self.movement_2[1] - self.movement_2[0], 0))
            self.dog.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        self.cat.pos[0] > self.display.get_height() or self.cat.pos[0] < 0 or \
                        self.cat.pos[1] > self.display.get_width() or \
                        self.dog.pos[0] > self.display.get_height() or self.dog.pos[0] < 0 or \
                        self.dog.pos[1] > self.display.get_width() or \
                        self.exit_acsess[0] and self.exit_acsess[1] and self.golovolomki_completed or\
                        self.golovolomki_completed and not self.golovolomka_passed:
                    running = False
                    time.sleep(3)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement_1[0] = True
                    if event.key == pygame.K_a:
                        self.movement_2[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement_1[1] = True
                    if event.key == pygame.K_d:
                        self.movement_2[1] = True
                    if event.key == pygame.K_UP and self.jump_acsess_cat:
                        self.jump_acsess_cat = False
                        self.cat.velocity[1] = -4
                    if event.key == pygame.K_w and self.jump_acsess_dog:
                        self.jump_acsess_dog = False
                        self.dog.velocity[1] = -4

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement_1[0] = False
                    if event.key == pygame.K_a:
                        self.movement_2[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement_1[1] = False
                    if event.key == pygame.K_d:
                        self.movement_2[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(80)

        print(5 - len(self.coins))
        pygame.quit()


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        for rect in tilemap.rects:
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        for coin in self.game.coins:
            if entity_rect.colliderect(coin.rect):
                self.game.collected_coins_sum += 1
                self.game.coins.remove(coin)

        if not entity_rect.colliderect(self.game.golovolomki[0][0]) and\
                not entity_rect.colliderect(self.game.golovolomki[1][0]):
            self.game.golovolomki[0][1], self.game.golovolomki[1][1] = False, False
        else:

            if entity_rect.colliderect(self.game.golovolomki[0][0]) and not self.game.golovolomki[0][1]:
                self.game.golovolomki[0][1] = True
            elif entity_rect.colliderect(self.game.golovolomki[0][0]):
                self.game.golovolomki[0][1] = False
            if entity_rect.colliderect(self.game.golovolomki[1][0]) and not self.game.golovolomki[1][1]:
                self.game.golovolomki[1][1] = True
            elif entity_rect.colliderect(self.game.golovolomki[1][0]):
                self.game.golovolomki[1][1] = False

        if not self.game.golovolomki_completed and self.game.golovolomki[1][1] and self.game.golovolomki[0][1]:
            self.game.golovolomka_passed = self.game.golovolomka_type(self.game)
            self.game.movement_1[1], self.game.movement_1[0] = False, False
            self.game.movement_2[1], self.game.movement_2[0] = False, False
            self.game.golovolomki_completed = True

        if entity_rect.colliderect(self.game.door_rect):
            if self.type == 'cat':
                self.game.exit_acsess[0] = True
            else:
                self.game.exit_acsess[1] = True

        for rect in tilemap.rects:
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
            if self.type == 'cat':
                self.game.jump_acsess_cat = True
            else:
                self.game.jump_acsess_dog = True

    def render(self, surf):
        surf.blit(self.game.assets[self.type], (self.pos[0], self.pos[1]))


def load_level(filename, round_number):
    filename = f'data/maps/{round_number}_round/' + filename
    with open(filename, mode="r", encoding="utf-8") as f:
        level = [i.strip() for i in f.readlines()]
    return level


class Tilemap:
    def __init__(self, game, round_number=1):
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = []
        self.rects = []
        if round_number == 1:
            number = random.randrange(1, 9)
        elif round_number == 2:
            number = random.randrange(21, 22)
        elif round_number == 3:
            number = random.randrange(30, 30)
        print(number)
        self.level = load_level(f'map{number}.txt', round_number)

    def render(self, fl=0):
        print(self.level)
        for y in range(len(self.level)):
            for x in range(len(self.level)):
                if self.level[y][x] == '.':
                    pass
                elif self.level[y][x] == '#':
                    self.game.display.blit(self.game.assets['stone'][2],
                                           (x * self.game.tile_size, y * self.game.tile_size))
                    if fl:
                        self.rects.append(
                            pygame.Rect(x * self.game.tile_size, y * self.game.tile_size,
                                        self.game.tile_size, self.game.tile_size))

                elif self.level[y][x] == 'c':
                    if fl:
                        self.game.coins.append(Coin(self.game, (x * self.game.tile_size, y * self.game.tile_size)))

                elif self.level[y][x] == 'e':
                    self.game.display.blit(self.game.assets['door'][1],
                                           (x * self.game.tile_size, y * self.game.tile_size))
                    self.game.door_rect = pygame.Rect(x * self.game.tile_size, y * self.game.tile_size,
                                                      self.game.tile_size, self.game.tile_size)

                elif self.level[y][x] == 'g':
                    if fl:
                        self.game.golovolomki.append([pygame.Rect(x * self.game.tile_size,
                                                                  (y + 0.8) * self.game.tile_size,
                                                                  self.game.tile_size - 1,
                                                                  0.2 * self.game.tile_size), False])
                    if not self.game.golovolomki_completed:
                        pygame.draw.rect(self.game.display, (0, 250, 20),
                                         pygame.Rect(x * self.game.tile_size, (y + 0.8) * self.game.tile_size,
                                                     self.game.tile_size - 1, 0.2 * self.game.tile_size))

                elif self.level[y][x] == '1' and fl:
                    cat = PhysicsEntity(self.game, 'cat', (x * self.game.tile_size, y * self.game.tile_size),
                                        (self.game.tile_size, self.game.tile_size))
                elif self.level[y][x] == '2' and fl:
                    dog = PhysicsEntity(self.game, 'dog', (x * self.game.tile_size, y * self.game.tile_size),
                                        (self.game.tile_size, self.game.tile_size))
        return (cat, dog) if fl else (None, None)


class Coin:
    def __init__(self, game, pos):
        self.game = game
        self.game.display.blit(self.game.assets['decor'][0], (pos[0], pos[1]))
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], self.game.tile_size, self.game.tile_size)

    def update(self):
        self.game.display.blit(self.game.assets['decor'][0], (self.pos[0], self.pos[1]))


def mathgame(game):
    running = True
    score = 0
    answer = ''
    start_time = time.time()
    game_duration = 30
    question, correct_answer = generate_question()
    golovolomka_pased = False
    font = pygame.font.Font(None, 52)

    while running:
        game.screen.fill(BLACK)
        time_left = game_duration - (time.time() - start_time)
        if time_left <= 0:
            score_surf_end = font.render(f'score: {score}', True, WHITE)
            if score < 10:
                result_end = font.render(f'your score is too small', True, WHITE)
            else:
                result_end = font.render(f'you passed', True, WHITE)
                golovolomka_pased = True
            game.screen.blit(result_end, (game.screen.get_width() // 2 - 250, game.screen.get_height() // 2 - 40))
            game.screen.blit(score_surf_end, (game.screen.get_width() // 2 - 100, game.screen.get_height() // 2 - 100))
            pygame.display.update()
            time.sleep(3)
            running = False
            continue

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
        question_surf = font.render(question, True, WHITE)
        game.screen.blit(question_surf, (50, 50))
        answer_surf = font.render(answer, True, WHITE)
        game.screen.blit(answer_surf, (50, 100))
        score_surf = font.render(f'score: {score}', True, WHITE)
        game.screen.blit(score_surf, (50, 150))
        time_surf = font.render(f'time: {int(time_left)}', True, WHITE)
        game.screen.blit(time_surf, (50, 200))

        pygame.display.flip()

    return golovolomka_pased


def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return f"{num1} x {num2}", num1 * num2


class Square:
    def __init__(self, pos, color, game):
        self.rect = pygame.Rect(pos[0], pos[1], 40, 40)
        self.color = color
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color, self.rect)


def provoda(game):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    square_positions = [(100, i * 150 + 100) for i in range(4)]
    random.shuffle(square_positions)

    line_positions = [(game.screen.get_width() - 140, i * 150 + 100) for i in range(4)]
    random.shuffle(line_positions)
    lines = []
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

        game.screen.fill((0, 0, 0))
        for pos, color in zip(square_positions + line_positions, colors * 2):
            pygame.draw.rect(game.screen, color, (pos[0], pos[1], 40, 40))
        if dragging and current_line_start:
            pygame.draw.line(game.screen, current_color, current_line_start, pygame.mouse.get_pos(), 5)
        for line in lines:
            pygame.draw.line(game.screen, line[2], line[0], line[1], 5)
        if len(lines) == 4:
            font = pygame.font.SysFont(None, 100)
            text = font.render('Done!', True, (0, 255, 0))
            game.screen.blit(text, (game.screen.get_width() // 2 - text.get_width() // 2,
                                    game.screen.get_height() // 2 - text.get_height() // 2))
            running = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)
    time.sleep(3)
    return True

def slova(game):
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
        game.screen.fill((217, 113, 11))
        game.screen.blit(text_surface, (250, 50))
        y_coord = 350
        pygame.draw.line(game.screen, BLACK, (100, y_coord), (700, y_coord), 5)

        for i, letter in enumerate(shuffled_letters):
            letter_surf = font.render(letter, True, BLACK)
            if letter in selected_letters:
                letter_rects[letter].center = (230 + selected_letters.index(letter) * 60, 320)
            else:
                letter_rects[letter].center = (230 + i * 60, 450)
            game.screen.blit(letter_surf, letter_rects[letter].topleft)

        if ''.join(selected_letters) == word:
            game_finished = True

        if game_finished:
            done_surf = font.render('Done', True, (15, 10, 10))
            done_rect = done_surf.get_rect(center=(game.screen.get_width() // 2 - 50,
                                                   game.screen.get__height() // 2 - 70))
            game.screen.blit(done_surf, done_rect)
            running = False

        pygame.display.flip()
    time.sleep(3)
    return True

Game(2).run()