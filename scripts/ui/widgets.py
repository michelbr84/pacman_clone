import pygame

from scripts import config

_DEFAULT_FONT_SIZE = 24


def _font(size=_DEFAULT_FONT_SIZE):
    return pygame.font.Font(config.FONT_PATH, size)


class Button:
    def __init__(self, rect, label, on_click, font=None):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.font = font or _font()
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, screen):
        color = config.YELLOW if self.hover else (180, 180, 180)
        pygame.draw.rect(screen, color, self.rect, 2, border_radius=6)
        text = self.font.render(self.label, True, color)
        screen.blit(text, text.get_rect(center=self.rect.center))


class Slider:
    def __init__(self, rect, label, value, on_change, min_v=0.0, max_v=1.0):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.value = value
        self.on_change = on_change
        self.min_v = min_v
        self.max_v = max_v
        self.dragging = False
        self.font = _font(18)

    def _set_from_mouse(self, mx):
        t = (mx - self.rect.left) / max(1, self.rect.width)
        t = max(0.0, min(1.0, t))
        self.value = self.min_v + t * (self.max_v - self.min_v)
        self.on_change(self.value)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._set_from_mouse(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._set_from_mouse(event.pos[0])
        elif event.type == pygame.KEYDOWN:
            step = (self.max_v - self.min_v) * 0.05
            if event.key == pygame.K_LEFT:
                self.value = max(self.min_v, self.value - step)
                self.on_change(self.value)
            elif event.key == pygame.K_RIGHT:
                self.value = min(self.max_v, self.value + step)
                self.on_change(self.value)

    def draw(self, screen):
        pygame.draw.rect(screen, (90, 90, 90), self.rect, 0, border_radius=4)
        t = (self.value - self.min_v) / max(1e-9, self.max_v - self.min_v)
        fill = self.rect.copy()
        fill.width = int(self.rect.width * t)
        pygame.draw.rect(screen, config.YELLOW, fill, 0, border_radius=4)
        label = self.font.render(
            f"{self.label}: {int(self.value * 100)}%", True, config.WHITE
        )
        screen.blit(label, (self.rect.left, self.rect.top - 22))


class Toggle:
    """Cycles through a list of option strings on click / Enter."""

    def __init__(self, rect, label, options, index, on_change):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.options = options
        self.index = index
        self.on_change = on_change
        self.font = _font(18)
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.index = (self.index + 1) % len(self.options)
                self.on_change(self.options[self.index])

    def draw(self, screen):
        color = config.YELLOW if self.hover else (180, 180, 180)
        pygame.draw.rect(screen, color, self.rect, 2, border_radius=6)
        label = self.font.render(
            f"{self.label}: {self.options[self.index]}", True, color
        )
        screen.blit(label, label.get_rect(center=self.rect.center))


class Menu:
    """Keyboard-navigable container of focusable widgets."""

    def __init__(self, widgets):
        self.widgets = widgets
        self.index = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.index = (self.index - 1) % len(self.widgets)
            elif event.key == pygame.K_DOWN:
                self.index = (self.index + 1) % len(self.widgets)
            elif event.key == pygame.K_RETURN:
                w = self.widgets[self.index]
                if isinstance(w, Button):
                    w.on_click()
                elif isinstance(w, Toggle):
                    w.index = (w.index + 1) % len(w.options)
                    w.on_change(w.options[w.index])
        # Forward events to the focused widget (so sliders respond to arrows too).
        focused = self.widgets[self.index]
        if isinstance(focused, Slider):
            focused.handle_event(event)
        for w in self.widgets:
            if w is not focused:
                w.handle_event(event)
            elif not isinstance(w, Slider):
                w.handle_event(event)

    def draw(self, screen):
        for i, w in enumerate(self.widgets):
            if hasattr(w, "hover"):
                w.hover = w.hover or (i == self.index)
            w.draw(screen)
