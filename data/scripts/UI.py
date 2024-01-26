import pygame

pygame.init()


class ButtonGroup:
    def __init__(self) -> None:
        self.button_list = []

    def add(self, button) -> None:
        self.button_list.append(button)

    def draw(self, screen) -> None:
        for button in self.button_list:
            button.draw(screen)

    def handle(self, event) -> None:
        for button in self.button_list:
            button.handle_event(event)

    def check_hover(self, mouse_pos: tuple[int, int]) -> None:
        for button in self.button_list:
            button.hover_check(mouse_pos)


class Button:
    def __init__(self, pos, width: int, height: int, img, hover_img, color: pygame.Color,
                 group: ButtonGroup, text_offsetX: int = 0, text_offsetY: int = 0):

        self._image = pygame.transform.scale(img, (width, height))
        self.nt_hover_image = self._image
        self._hover_image = self._image
        if hover_img is not None:
            self._hover_image = pygame.transform.scale(hover_img, (width, height))
        if color is not None:
            self._image.set_colorkey(color)
            self._hover_image.set_colorkey(color)
        self.text_list = []

        self._rect = self._image.get_rect(center=pos)
        self._is_hovered = False

        if group is not None:
            group.add(self)

    def draw(self, screen) -> None:
        current_image = self._hover_image if self._is_hovered else self._image
        screen.blit(current_image, self._rect.topleft)
        for i in self.text_list:
            i.draw(screen)

    def hover_check(self, mouse_pos: tuple[int, int]) -> None:
        self._is_hovered = self._rect.collidepoint(mouse_pos)
        if self._is_hovered:
            self._image = self._hover_image
        else:
            self._image = self.nt_hover_image

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._is_hovered:
            return True
            # pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
        return False

    def add(self, text) -> None:
        self.text_list.append(text)

    @property
    def rect(self):
        return self._rect


class DopText:
    def __init__(self, text_offsetX: int, text_offsetY: int, button: Button, text_color: pygame.Color, text: str,
                 text_size: int, ):
        self.textfX = text_offsetX
        self.textfY = text_offsetY
        self._text = text
        self._rect = button.rect
        self._text_color = text_color
        self._font = pygame.font.Font(None, text_size)
        button.add(self)

    def draw(self, screen):
        text_surf = self._font.render(self._text, True, self._text_color)
        text_rect = text_surf.get_rect(center=self._rect.center).move(self.textfX, self.textfY)
        screen.blit(text_surf, text_rect)

    def retext(self, screen, newtext: str):
        self._text = newtext
        self.draw(screen)
