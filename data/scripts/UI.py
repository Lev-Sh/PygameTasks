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
    def __init__(self, pos, width: int, height: int, img, hover_img, color: pygame.Color, text: str, text_size: int,
                 text_color: pygame.Color, group: ButtonGroup):
        self._text = text
        self._text_color = text_color

        self._font = pygame.font.Font(None, text_size)

        self._image = pygame.transform.scale(img, (width, height))
        self._hover_image = self._image
        if hover_img is not None:
            self._hover_image = pygame.transform.scale(hover_img, (width, height))
        if color is not None:
            self._image.set_colorkey(color)
            self._hover_image.set_colorkey(color)

        self._rect = self._image.get_rect(center=pos)
        self._is_hovered = False

        if group is not None:
            group.add(self)

    def draw(self, screen) -> None:
        current_image = self._hover_image if self._is_hovered else self._image
        screen.blit(current_image, self._rect.topleft)
        text_surf = self._font.render(self._text, True, self._text_color)
        text_rect = text_surf.get_rect(center=self._rect.center)
        screen.blit(text_surf, text_rect)

    def hover_check(self, mouse_pos: tuple[int, int]) -> None:
        self._is_hovered = self._rect.collidepoint(mouse_pos)

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._is_hovered:
            return True
            # pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
        return False
