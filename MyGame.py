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
        self.rect.x = 80
        self.rect.y = 80
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

    def get_pos(self):
        return [self.rect.x, self.rect.y]

    def update(self):
        if w - 90 >= self.rect.x + self.up_x >= 0 and h - 60 >= self.rect.y + self.up_y >= -10:
            self.rect = self.rect.move(self.up_x, self.up_y)
        if self.up_y != 0 or self.up_x != 0:
            self.image = self.images[self.count % len(self.images)]
            self.count += 1
        else:
            self.image = self.images[1]
        for semka in sprite_foods:
            if pygame.sprite.collide_mask(self, semka):
                sprite_foods.remove(semka)
                statistic.eating(10)
        for stick in sprite_sticks:
            if pygame.sprite.collide_mask(self, stick):
                sprite_sticks.remove(stick)
                statistic.take_stick()

    def get_d(self):
        return [self.up_x, self.up_y]


class Semki(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("food.png"), (40, 40))

    def __init__(self, group, range_x=-1, range_y=0, up_render=[]):
        super().__init__(group)
        self.image = Semki.image
        self.rect = self.image.get_rect()
        if range_x == -1:
            self.rect.x = random.randrange(w)
            self.rect.y = random.randrange(h)
        else:
            up_x_render = up_render[0]
            up_y_render = up_render[0]
            if up_x_render > 0:
                self.rect.x = random.randint(range_x + up_x_render, range_x + 2 * up_x_render)
            elif up_x_render < 0:
                self.rect.x = random.randint(range_x + 3 * up_x_render, up_x_render + 2 * range_x)
            else:
                self.rect.x = random.randrange(w)
            if up_y_render > 0:
                self.rect.y = random.randint(range_y + up_y_render, range_y + 2 * up_y_render)
            elif up_y_render < 0:
                self.rect.y = random.randint(range_y + 2 * up_y_render, up_y_render + range_y)
            else:
                self.rect.y = random.randrange(h)

        self.up_x = 0
        self.up_y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def world_is_running(self, up_x, up_y):
        self.up_x += up_x
        self.up_y += up_y

    def update(self):
        self.rect = self.rect.move(self.up_x, self.up_y)

    def get_position(self):
        print(str(str(self.rect.x) + ' ' + str(self.rect.y)))


class Stick(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("stick.png"), (40, 40))

    def __init__(self, group, range_x=-1, range_y=0, up_render=[]):
        super().__init__(group)
        self.image = Stick.image
        self.rect = self.image.get_rect()
        if range_x == -1:
            self.rect.x = random.randrange(w)
            self.rect.y = random.randrange(h)
        else:
            up_x_render = up_render[0]
            up_y_render = up_render[0]
            if up_x_render > 0:
                self.rect.x = random.randint(range_x + up_x_render, range_x + 2 * up_x_render)
            elif up_x_render < 0:
                self.rect.x = random.randint(range_x + 3 * up_x_render, up_x_render + 2 * range_x)
            else:
                self.rect.x = random.randrange(w)
            if up_y_render > 0:
                self.rect.y = random.randint(range_y + up_y_render, range_y + 2 * up_y_render)
            elif up_y_render < 0:
                self.rect.y = random.randint(range_y + 2 * up_y_render, up_y_render + range_y)
            else:
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
        self.health = 40
        self.hungry = 40
        self.stick_count = 9

    def render(self):
        font = pygame.font.Font(None, 20)

        pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(10, 10, 80, 15), 3)
        pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(10, 10, self.health, 15), 0)
        text = font.render('health', True, pygame.Color("white"))
        screen.blit(text, [10, 10])

        pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(10, 30, 80, 15), 3)
        pygame.draw.rect(screen, pygame.Color("blue"), pygame.Rect(10, 30, self.hungry, 15), 0)
        text = font.render('hungry', True, pygame.Color("white"))
        screen.blit(text, [10, 30])

        text = font.render('Count of sticks: ' + str(self.stick_count), True, pygame.Color("white"))
        screen.blit(text, [10, 50])

    def eating(self, food_value):
        if self.hungry + food_value >= 80:
            self.hungry = 80
        else:
            self.hungry += food_value

    def less_static(self):
        if self.hungry > 0:
            self.hungry -= 10
        else:
            self.health -= 10
        if self.health <= 0:
            exit()

    def take_stick(self):
        self.stick_count += 1

    def get_stick_count(self, plus=0):
        self.stick_count += plus
        return self.stick_count


class Nest(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("nest.png"), (70, 70))

    def __init__(self, group):
        super().__init__(group)
        self.image = Nest.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.up_x = 0
        self.up_y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def set_nest(self, position):
        self.rect = position


def new_drop(pos, direction):
    if random.randint(0, 1):
        if direction == 'top':
            up_x = 0
            up_y = - 50
        if direction == 'bottom':
            up_x = 0
            up_y = 50
        if direction == 'left':
            up_y = 0
            up_x = -50
        if direction == 'right':
            up_y = 0
            up_x = 50
        try:
            if random.randint(0, 1):
                Semki(sprite_foods, pos[0], pos[1], [up_x, up_y])
            if random.randint(0, 1):
                Stick(sprite_sticks, pos[0], pos[1], [up_x, up_y])
        except ValueError:
            print(pos[0][1], up_x, up_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        d = target.get_d()
        self.dx = -d[0]
        self.dy = -d[1]


camera = Camera()

pygame.init()

egg_flag = 1

screen = pygame.display.set_mode(size)
running = True

# bird1 = pygame.transform.scale(bird1, (90, 70))

sprite_bird = pygame.sprite.Group()
Bird(sprite_bird)

sprite_foods = pygame.sprite.Group()
for i in range(5):
    Semki(sprite_foods, -1, 0, [0, 0])

sprite_sticks = pygame.sprite.Group()
for i in range(5):
    Stick(sprite_sticks)

sprite_ground = pygame.sprite.Group()
BackGround(sprite_ground)

sprite_nest = pygame.sprite.Group()
Nest(sprite_nest)

all_sprites = pygame.sprite.Group(sprite_ground, sprite_foods, sprite_sticks)
statistic = Statistic()

fps = 10  # количество кадров в секунду
clock = pygame.time.Clock()

time = 0

moved = [0, 0]
flying_x = 0
flying_y = 0

we_have_egg_flag = 0
we_have_nest_flag = 0

while running:  # главный игровой цикл
    screen.fill(pygame.Color("white"))
    all_sprites = pygame.sprite.Group(sprite_ground, sprite_foods, sprite_sticks, sprite_nest)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for sprite in sprite_bird:
                    sprite.fly(0, -5)
                flying_y += 3
                # change_world(0, 3)
            if event.key == pygame.K_DOWN:
                for sprite in sprite_bird:
                    sprite.fly(0, 5)
                flying_y += -3
                # change_world(0, -3)
            if event.key == pygame.K_LEFT:
                for sprite in sprite_bird:
                    sprite.fly(-5, 0, 1)
                flying_x += 3
                # change_world(3, 0)
            if event.key == pygame.K_RIGHT:
                for sprite in sprite_bird:
                    sprite.fly(5, 0, 1)
                flying_x += -3
                # change_world(-3, 0)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                for sprite in sprite_bird:
                    sprite.fly(0, 5)
                flying_y += -3
                # change_world(0, -3)
            if event.key == pygame.K_DOWN:
                for sprite in sprite_bird:
                    sprite.fly(0, -5)
                flying_y += 3
                # change_world(0, 3)
            if event.key == pygame.K_LEFT:
                for sprite in sprite_bird:
                    sprite.fly(5, 0)
                flying_x += -3
                # change_world(-3, 0)
            if event.key == pygame.K_RIGHT:
                for sprite in sprite_bird:
                    sprite.fly(-5, 0)
                flying_y += 3
                # change_world(3, 0)
            if event.key == pygame.K_SPACE:
                if statistic.get_stick_count() >= 10:
                    statistic.get_stick_count(-10)
                    we_have_nest_flag = 1
                    for sprite in sprite_nest:
                        for sprite_b in sprite_bird:
                            sprite.set_nest(sprite_b.get_pos())

    for sprite in sprite_bird:
        camera.update(sprite)

    for sprite in all_sprites:
        camera.apply(sprite)

    sprite_ground.draw(screen)
    # sprite_ground.update()

    if we_have_nest_flag:
        sprite_nest.draw(screen)
        #sprite_nest.update()

    sprite_foods.draw(screen)
    # sprite_foods.update()

    sprite_sticks.draw(screen)
    # sprite_sticks.update()

    statistic.render()

    sprite_bird.draw(screen)
    sprite_bird.update()

    moved[0] += flying_x
    moved[0] += flying_y

    if time % 150 == 0:
        statistic.less_static()

    for i in range(len(moved)):
        if abs(moved[i]) >= 50:
            if i == 0 and moved[i] > 0:
                for sprite in sprite_bird:
                    new_drop(sprite.get_pos(), 'left')
            if i == 0 and moved[i] < 0:
                for sprite in sprite_bird:
                    new_drop(sprite.get_pos(), 'right')
            if i == 1 and moved[i] > 0:
                for sprite in sprite_bird:
                    new_drop(sprite.get_pos(), 'top')
            if i == 1 and moved[i] < 0:
                for sprite in sprite_bird:
                    new_drop(sprite.get_pos(), 'bottom')
            moved[i] = 0
    time += 1
    clock.tick(fps)
    pygame.display.flip()
    # временная задержка

pygame.quit()
