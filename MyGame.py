import pygame
import random


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # отрисовка поля

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(self.left + i * self.cell_size,
                                                                            self.top + j * self.cell_size,

                                                                            self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        for i in range(self.height):
            for j in range(self.width):
                if self.left + j * self.cell_size <= mouse_pos[0] < self.left + (
                        j + 1) * self.cell_size and self.top + i * self.cell_size <= mouse_pos[1] < self.top + (
                        i + 1) * self.cell_size:
                    return (i, j)
        return None


def load_image(filename):
    filename = "data/" + filename
    return pygame.image.load(filename)


class Bird(pygame.sprite.Sprite):
    frame1 = pygame.transform.scale(load_image("bird1.png"), (90, 70))
    frame2 = pygame.transform.scale(load_image("bird2.png"), (90, 70))
    frame3 = pygame.transform.scale(load_image("bird3.png"), (90, 70))
    frame4 = pygame.transform.scale(load_image("bird4.png"), (90, 70))

    frame1_left = pygame.transform.scale(load_image("bird1_left.png"), (90, 70))
    frame2_left = pygame.transform.scale(load_image("bird2_left.png"), (90, 70))
    frame3_left = pygame.transform.scale(load_image("bird3_left.png"), (90, 70))
    frame4_left = pygame.transform.scale(load_image("bird4_left.png"), (90, 70))

    def __init__(self, group):
        super().__init__(group)
        self.count = 0
        self.frames_right = [Bird.frame1, Bird.frame2, Bird.frame3, Bird.frame4]
        self.frames_left = [Bird.frame1_left, Bird.frame2_left, Bird.frame3_left, Bird.frame4_left]
        self.images = self.frames_right
        self.image = self.images[self.count % len(self.images)]
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 5
        self.up_x = 0
        self.up_y = 0

    def fly(self, up_x, up_y, swap_fremes_flag=0):
        self.up_x += up_x
        self.up_y += up_y
        if not swap_fremes_flag:
            return
        if up_x < 0:
            self.images = self.frames_left
        if up_x > 0:
            self.images = self.frames_right

    def update(self):
        self.rect = self.rect.move(self.up_x, self.up_y)
        if self.up_y != 0 or self.up_x != 0:
            self.image = self.images[self.count % len(self.images)]
            self.count += 1
        else:
            self.image = self.images[1]


class Semki(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("food.png"), (40, 40))

    def __init__(self, group):
        super().__init__(group)
        self.image = Semki.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(w)
        self.rect.y = random.randrange(h)

    def update(self):
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   random.randrange(3) - 1)


pygame.init()

size = w, h = 400, 400
screen = pygame.display.set_mode(size)
running = True

# bird1 = pygame.transform.scale(bird1, (90, 70))

sprite_bird = pygame.sprite.Group()
Bird(sprite_bird)

sprite_foods = pygame.sprite.Group()
for i in range(5):
    Semki(sprite_foods)

fps = 10  # количество кадров в секунду
clock = pygame.time.Clock()

board = Board(10, 10)

while running:  # главный игровой цикл
    screen.fill(pygame.Color("white"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for sprite in sprite_bird:
                    sprite.fly(0, -5)
            if event.key == pygame.K_DOWN:
                for sprite in sprite_bird:
                    sprite.fly(0, 5)
            if event.key == pygame.K_LEFT:
                for sprite in sprite_bird:
                    sprite.fly(-5, 0, 1)
            if event.key == pygame.K_RIGHT:
                for sprite in sprite_bird:
                    sprite.fly(5, 0, 1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                for sprite in sprite_bird:
                    sprite.fly(0, 5)
            if event.key == pygame.K_DOWN:
                for sprite in sprite_bird:
                    sprite.fly(0, -5)
            if event.key == pygame.K_LEFT:
                for sprite in sprite_bird:
                    sprite.fly(5, 0)
            if event.key == pygame.K_RIGHT:
                for sprite in sprite_bird:
                    sprite.fly(-5, 0)
    sprite_foods.draw(screen)
    sprite_foods.update()
    board.render()
    sprite_bird.draw(screen)
    sprite_bird.update()
    clock.tick(fps)
    pygame.display.flip()
    # временная задержка

pygame.quit()
