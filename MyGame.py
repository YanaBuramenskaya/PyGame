import pygame
import random

size = w, h = 400, 400


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
        self.mask = pygame.mask.from_surface(self.image)

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
        if w - 90 >= self.rect.x + self.up_x >= 0 and h - 60 >= self.rect.y + self.up_y >= -10:
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
        self.up_x = 0
        self.up_y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def world_is_running(self, up_x, up_y):
        self.up_x += up_x
        self.up_y += up_y

    def update(self):
        self.rect = self.rect.move(self.up_x, self.up_y)


class BackGround(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("world.jpg"), (w * 3, h * 3))

    def __init__(self, group):
        super().__init__(group)
        self.image = BackGround.image
        self.rect = self.image.get_rect()
        self.rect.x = -400
        self.rect.y = -400
        self.up_x = 0
        self.up_y = 0

    def world_is_running(self, up_x, up_y):
        self.up_x += up_x
        self.up_y += up_y

    def update(self):
        self.rect = self.rect.move(self.up_x, self.up_y)


class Statistic:

    def __init__(self):
        self.health = 80
        self.hungry = 80

    def render(self):
        pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(10, 10, 80, 15), 3)
        pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(10, 10, self.health, 15), 0)
        font = pygame.font.Font(None, 20)
        text = font.render('health', True, pygame.Color("white"))
        screen.blit(text, [10, 10])

        pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(10, 30, 80, 15), 3)
        pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(10, 30, self.hungry, 15), 0)
        font = pygame.font.Font(None, 20)
        text = font.render('hungry', True, pygame.Color("white"))
        screen.blit(text, [10, 30])


pygame.init()

egg_flag = 1

size = w, h = 400, 400
screen = pygame.display.set_mode(size)
running = True

# bird1 = pygame.transform.scale(bird1, (90, 70))

sprite_bird = pygame.sprite.Group()
Bird(sprite_bird)

sprite_foods = pygame.sprite.Group()
for i in range(5):
    Semki(sprite_foods)

sprite_ground = pygame.sprite.Group()
BackGround(sprite_ground)

statistic = Statistic()

fps = 10  # количество кадров в секунду
clock = pygame.time.Clock()

while running:  # главный игровой цикл
    screen.fill(pygame.Color("white"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for sprite in sprite_bird:
                    sprite.fly(0, -5)
                for sprite in sprite_foods:
                    sprite.world_is_running(0, 3)
                for sprite in sprite_ground:
                    sprite.world_is_running(0, 3)
            if event.key == pygame.K_DOWN:
                for sprite in sprite_bird:
                    sprite.fly(0, 5)
                for sprite in sprite_foods:
                    sprite.world_is_running(0, -3)
                for sprite in sprite_ground:
                    sprite.world_is_running(0, -3)
            if event.key == pygame.K_LEFT:
                for sprite in sprite_bird:
                    sprite.fly(-5, 0, 1)
                for sprite in sprite_foods:
                    sprite.world_is_running(3, 0)
                for sprite in sprite_ground:
                    sprite.world_is_running(3, 0)
            if event.key == pygame.K_RIGHT:
                for sprite in sprite_bird:
                    sprite.fly(5, 0, 1)
                for sprite in sprite_foods:
                    sprite.world_is_running(-3, 0)
                for sprite in sprite_ground:
                    sprite.world_is_running(-3, 0)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                for sprite in sprite_bird:
                    sprite.fly(0, 5)
                for sprite in sprite_foods:
                    sprite.world_is_running(0, -3)
                for sprite in sprite_ground:
                    sprite.world_is_running(0, -3)
            if event.key == pygame.K_DOWN:
                for sprite in sprite_bird:
                    sprite.fly(0, -5)
                for sprite in sprite_foods:
                    sprite.world_is_running(0, 3)
                for sprite in sprite_ground:
                    sprite.world_is_running(0, 3)
            if event.key == pygame.K_LEFT:
                for sprite in sprite_bird:
                    sprite.fly(5, 0)
                for sprite in sprite_foods:
                    sprite.world_is_running(-3, 0)
                for sprite in sprite_ground:
                    sprite.world_is_running(-3, 0)
            if event.key == pygame.K_RIGHT:
                for sprite in sprite_bird:
                    sprite.fly(-5, 0)
                for sprite in sprite_foods:
                    sprite.world_is_running(3, 0)
                for sprite in sprite_ground:
                    sprite.world_is_running(3, 0)

    sprite_ground.draw(screen)
    sprite_ground.update()

    sprite_foods.draw(screen)
    sprite_foods.update()

    statistic.render()

    sprite_bird.draw(screen)
    sprite_bird.update()

    clock.tick(fps)
    pygame.display.flip()
    # временная задержка

pygame.quit()
