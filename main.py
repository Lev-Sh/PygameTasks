import pygame
import sys
import os
import random

# import math

pygame.init()
pygame.display.set_mode((1, 1))
SIZE = WIDTH, HEIGHT = 600, 400
BACKGROUND = pygame.Color('black')
COLOR = pygame.Color('yellow')
FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name: str, path: str = 'data', colorway: None | pygame.Color | str | int = None) -> pygame.Surface:
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorway is not None:
        image = image.convert()
        if colorway == -1:
            colorway = image.get_at((0, 0))
        image.set_colorkey(colorway)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename, fullchar: str = '.') -> list[str]:
    filename = os.path.join('data/levels', filename)
    with open(filename, 'r', encoding='utf-8') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, fullchar), level_map))


item_image = load_image('apple.png', 'data/images')

tile_images = {
    'wall': load_image('box.png', 'data/images'),
    'appbox': load_image('apple_box.png', 'data/images'),
    'latucc_box': load_image('latucc_box.png', 'data/images'),
    'holodilnik': load_image('holodilnik.png', 'data/images'),
    'polystena': load_image('polystena.png', 'data/images'),
    'electric_stove': load_image('electro_doska.png', 'data/images'),
    'empty': load_image('floor.png', 'data/images'),
    'empty2': load_image('floor3.png', 'data/images'),
    'ladder': load_image('ladder.png', 'data/images')

}
customers_images = {
    'customer_1': load_image('customer_1.png', 'data/images')
}

all_customers = []
player_image = load_image('player.png', 'data/images')

apple_image = load_image('apple.png', 'data/images')
beef_image = load_image('beef.png', 'data/images')
cooked_beef_image = load_image('beef_cooked.png', 'data/images')
bulka_image = load_image('bulka.png', 'data/images')
latucc_image = load_image('latucc.png', 'data/images')
customers_can_response = {
    'None': load_image('None.png', 'data/images'),
    'apple_image': apple_image,
    # 'bulka_image': bulka_image,
    'latucc': latucc_image,
    'beef_image': beef_image,
    'cooked_beef_image': cooked_beef_image
}
customers_can_response_list = ['apple', 'beef', 'beef_cooked', 'latucc']
tile_width = tile_height = 40


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == ',':
                Tile('empty2', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'a':
                Tile('appbox', x, y)
            elif level[y][x] == 'l':
                Tile('latucc_box', x, y)
            elif level[y][x] == '^':
                Tile('ladder', x, y)
            elif level[y][x] == '|':
                Tile('holodilnik', x, y)
            elif level[y][x] == '-':
                Tile('polystena', x, y)
            elif level[y][x] == '=':
                Tile('electric_stove', x, y)
            elif level[y][x] == '@':
                Tile('empty2', x, y)
                new_player = Player(x, y)

    return new_player, x + 1, y + 1


def start_screen():
    intro_text = ["...."]

    fon = pygame.transform.scale(load_image('fon.png', 'data/images'), (WIDTH, HEIGHT))
    start_btns = pygame.transform.scale(load_image('start_btn.png', 'data/images'), (80, 80))

    screen.blit(fon, (0, 0))
    screen.blit(start_btns, (WIDTH / 2 - 80, HEIGHT / 2 - 80))

    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for se in pygame.event.get():
            if se.type == pygame.QUIT:
                terminate()
            elif se.type == pygame.KEYDOWN or \
                    se.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            tiles_blocks_group.add(self)
        if tile_type == 'appbox':
            apple_box_group.add(self)
        if tile_type == 'latucc_box':
            latucc_box_group.add(self)
            # tiles_blocks_group.add(self)
        if tile_type == 'holodilnik':
            holodilnik_group.add(self)
            # tiles_blocks_group.add(self)
        if tile_type == 'electric_stove':
            electro_plate_group.add(self)
            # tiles_blocks_group.add(self)


# class AppleBox(pygame.sprite.Sprite):

#   def __init__(self, x , y):
#       super().__init__(apple_box_group, all_sprites)
#       self.image = tile_images['appbox']
#       self.rect = self.image.get_rect().move(
#           tile_width * (x + 2) + 5, tile_height * (y - 2) + 5)

#   def get_apple(self):
#       pl.inventory = "apple"
#       create(1)

class Dialogue(pygame.sprite.Sprite):
    def __init__(self, x, y, resp):
        super().__init__(dialogue_group, all_sprites)
        create(1, dropped=True, item=resp, x=(x + 0.8), y=(y - 0.6), workings=False)
        resp = ''
        self.image = load_image(f'dialogue.png', 'data/images')
        self.rect = self.image.get_rect().move(
            tile_width * (x + 0.6) + 5, tile_height * (y - 0.7) + 5)

    def change(self, im):
        self.image = customers_can_response[im]


class Customer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(customer_group, tiles_blocks_group, all_sprites)
        self.image = load_image('None.png', 'data/images')
        self.response = ''
        self.rect = self.image.get_rect().move(
            tile_width * 0 + 15, tile_height * 0 + 5)
        self.prev_awake = 0
        self.d = None
        self.k_of_activity = random.randrange(1, 5)
        self.x = 0
        self.y = 0

    def update(self):
        if pygame.sprite.spritecollideany(self, items_group):
            if len(pygame.sprite.spritecollide(self, items_group, 0)) > 1:
                if self.response == pygame.sprite.spritecollide(self, items_group, 0)[1].name:
                    print('toched')

                    pygame.sprite.spritecollide(self, items_group, 1)[1].dropped = True
                    print("ACCEPTED")

                    self.prev_awake = pygame.time.get_ticks()
                    self.gone()
        if not self.prev_awake == 0 and pygame.time.get_ticks() - self.prev_awake > 4000:
            self.awake(2, 2)
            self.prev_awake = 0

    # def moving(self, mx, my):
    #    self.rect.move_ip(mx * tile_width, my * tile_height)
    #    self.x += mx * tile_width
    #    self.y += my * tile_height
    #    if pygame.sprite.spritecollideany(self, tiles_blocks_group):
    #        self.rect.move_ip(-mx * tile_width, -my * tile_height)
    #        self.x += -mx * tile_width
    #        self.y += -my * tile_height

    def awake(self, pos_x, pos_y):
        self.response = customers_can_response_list[random.randrange(0, len(customers_can_response_list))]
        print(self.response)
        self.image = customers_images['customer_1']

        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        all_customers.append(self)
        self.d = Dialogue(pos_x, pos_y, self.response)

    def gone(self):
        self.image = load_image('None.png', 'data/images')
        self.d.change('None')


class Player(pygame.sprite.Sprite):
    player_image = load_image('player.png', 'data/images')

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.inventory = "apple"
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.items = []

    def move(self, mx: float, my: float):
        self.items[len(self.items) - 1].update(pl.x, pl.y)
        self.image = player_image
        # old_block = self.x, self.y
        self.rect.move_ip(mx * tile_width, my * tile_height)
        self.x += mx * tile_width
        self.y += my * tile_height
        if pygame.sprite.spritecollideany(self, tiles_blocks_group):
            self.rect.move_ip(-mx * tile_width, -my * tile_height)
            self.x += -mx * tile_width
            self.y += -my * tile_height

    def get_item(self):

        if pygame.sprite.spritecollideany(self, apple_box_group):
            self.inventory = "apple"
            create(1, False, self.inventory, pl.x, pl.y, True)
        elif pygame.sprite.spritecollideany(self, holodilnik_group):
            self.inventory = "beef"
            create(1, False, self.inventory, pl.x, pl.y, True)
        elif pygame.sprite.spritecollideany(self, latucc_box_group):
            self.inventory = "latucc"
            create(1, False, self.inventory, pl.x, pl.y, True)
        elif pygame.sprite.spritecollideany(self, items_group):
            self.inventory = pygame.sprite.spritecollide(self, items_group, 0)[0].name
            pygame.sprite.spritecollide(self, items_group, 0)[0].dropped = False

    def drop(self):
        if pygame.sprite.spritecollide(self, items_group, 0):
            pygame.sprite.spritecollide(self, items_group, 0)[0].dropped = True
            # pl.inventory = "None"
            # print(pl.inventory)

    def cook_item(self):
        if pygame.sprite.spritecollideany(self, electro_plate_group):
            pygame.sprite.spritecollide(self, items_group, 0)[0].cook()


class Timer:
    def __init__(self):
        self.started = False
        self.tm = 0
        self.secundes = 0
        self.minutes = 0
        self.replace()

    def start(self, time: int):
        self.tm = time
        self.secundes = 0
        self.minutes = 0
        self.started = True
        self.replace()
        self.update()

    def replace(self):
        s = self.tm
        while s > 60:
            s -= 60
            self.minutes += 1
        self.secundes = s

    def update(self):
        if self.started:
            font = pygame.font.SysFont(name='NewRoman', size=36)
            text = font.render(f"{self.minutes}:{int(self.secundes)}", True, (0, 0, 0))
            screen.blit(text, (450, 20))
            pygame.display.flip()
            self.tm -= 0.02
            self.replace()


class Item(pygame.sprite.Sprite):

    def __init__(self, x, y, item: str, working):
        super().__init__(items_group, player_group, all_sprites)
        self.name = item
        self.working = working
        if working:
            self.image = self.item_images()
            self.rect = self.image.get_rect().move(
                tile_width * x + 2, tile_height * y + 2)
            self.x = tile_width * x + 1
            self.y = tile_height * y + 1
            self.offsetX = -1.3
            self.offsetY = -4.79

            self.speed = 1
            self.dropped = False
        else:
            self.image = self.item_images()
            self.rect = self.image.get_rect().move(
                tile_width * x + 2, tile_height * y + 2)

    def item_images(self):
        match self.name:
            case "None":
                return load_image('None.png', 'data/images')
            case "apple":
                return load_image('apple.png', 'data/images')
            case "latucc":
                return load_image('latucc.png', 'data/images')
            case "beef":
                return load_image('beef.png', 'data/images')
            case "cooked_beef":
                return load_image('beef_cooked.png', 'data/images')
        return load_image('apple.png', 'data/images')

    def update(self, xx, yy):
        if not self.dropped:
            direction_x = (xx - (self.offsetX * tile_width) - self.x)
            direction_y = (yy - (self.offsetY * tile_height) - self.y)

            if direction_x > 1 or direction_x < -1:
                self.rect.move_ip(direction_x, 0)
                self.x += direction_x

            if direction_y > 1 or direction_y < -1:
                self.rect.move_ip(0, direction_y)
                self.y += direction_y

    def cook(self):
        print("cook", self.name)
        if self.name == "beef":
            self.image = cooked_beef_image
            self.name = "beef_cooked"


def create(count: int, dropped, item: str, x, y, workings: bool):
    for i in range(count):
        if dropped:
            item = Item(x=x, y=y, item=item, working=workings)
        else:
            item = Item(pl.x / tile_width, pl.y / tile_height, item, workings)
        if workings:
            item.dropped = dropped
            print(item.image, item.name, item.dropped, item.x, item.y, pl.x, pl.y)
            items_group.draw(screen)
            pl.items.append(item)


if __name__ == '__main__':
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    start_screen()
    start_time = 0
    armed = False
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_blocks_group = pygame.sprite.Group()
    items_group = pygame.sprite.Group()
    # functionals blocks
    apple_box_group = pygame.sprite.Group()
    holodilnik_group = pygame.sprite.Group()
    electro_plate_group = pygame.sprite.Group()
    latucc_box_group = pygame.sprite.Group()
    # Customers and dialogues
    customer_group = pygame.sprite.Group()
    dialogue_group = pygame.sprite.Group()

    running = True
    started = False
    space_clicked = False
    level_time = 1
    c = Customer()
    t = Timer()
    pl = Player(100, 100)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not started:

                screen.fill(BACKGROUND)
                pl, xs, ys = generate_level(load_level('level1.dat'))
                apple_box_group.draw(screen)
                holodilnik_group.draw(screen)
                electro_plate_group.draw(screen)
                c.awake(1, 1)
                create(2, True, "apple", pl.x, pl.y, True)
                create(2, True, "beef", pl.x, pl.y, True)
                t.start(60)
                started = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                pl.cook_item()
            if keys[pygame.K_SPACE] and not armed:
                pl.get_item()
                armed = True
            if keys[pygame.K_q] and armed:
                pl.drop()
                armed = False
            if keys[pygame.K_w]:
                player_image = load_image('player.png', 'data/images')
                pl.move(0, -0.2)
            elif keys[pygame.K_s]:
                player_image = load_image('player_180.png', 'data/images')
                pl.move(0, 0.2)
            elif keys[pygame.K_a]:
                player_image = load_image('player_270.png', 'data/images')
                pl.move(-0.2, 0)
            elif keys[pygame.K_d]:
                player_image = load_image('player_90.png', 'data/images')
                pl.move(0.2, 0)
        if started:
            for a in pl.items:
                a.update(pl.x, pl.y)
            for b in all_customers:
                b.update()
            t.update()
        tiles_group.draw(screen)
        customer_group.draw(screen)
        dialogue_group.draw(screen)
        electro_plate_group.draw(screen)
        holodilnik_group.draw(screen)
        player_group.draw(screen)

        items_group.draw(screen)
        # pygame.display.flip()
        clock.tick(FPS)
    terminate()
