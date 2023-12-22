import pygame
import sys
import os

pygame.init()
pygame.display.set_mode((1, 1))
SIZE = WIDTH, HEIGHT = 600, 400
BACKGROUND = pygame.Color('black')
COLOR = pygame.Color('yellow')
FPS = 60


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
    # else:
    # image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('box.png', 'data/images'),
    'empty': load_image('grass.png', 'data/images')
}
player_image = load_image('mar.png', 'data/images')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            tiles_blocks_group.add(self)


class Player(pygame.sprite.Sprite):
    player_image = load_image('mar.png', 'data/images')

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, mx: int, my: int):
        old_block = self.x, self.y
        self.rect.move_ip(mx * tile_width, my * tile_height)
        if pygame.sprite.spritecollideany(self, tiles_blocks_group):
            self.rect.move_ip(-mx * tile_width, -my * tile_height)


def load_level(filename, fullchar: str = '.') -> list[str]:
    filename = os.path.join('data/levels', filename)
    with open(filename, 'r', encoding='utf-8') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, fullchar), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x + 1, y + 1


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["НАЖМИТЕ ЛЮБУЮ КЛАВИШУ",
                  "ЧТО БЫ НАЧАТЬ"]

    fon = pygame.transform.scale(load_image('fon.jpg', 'data/images'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
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


if __name__ == '__main__':
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    start_screen()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_blocks_group = pygame.sprite.Group()

    running = True
    started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill(BACKGROUND)
                pl, xs, ys = generate_level(load_level('level1.dat'))
                started = True
            elif event.type == pygame.KEYDOWN and started:
                match event.key:
                    case pygame.K_w:
                        pl.move(0, -1)
                    case pygame.K_s:
                        pl.move(0, 1)
                    case pygame.K_a:
                        pl.move(-1, 0)
                    case pygame.K_d:
                        pl.move(1, 0)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
