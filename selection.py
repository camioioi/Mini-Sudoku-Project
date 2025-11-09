class SelectNumber:
    def __init__(self, pygame, font, origin_x: int = 950, btn_w: int = 80, btn_h: int = 80, scale: float = 1.0):
       self.pygame = pygame
       self.my_font = font
       self.selected_number = 0

       self.color_selected = (255, 255, 255)
       self.color_normal = (129, 19, 49)

       self.btn_w = btn_w
       self.btn_h = btn_h
       self.origin_x = origin_x

       self.scale = scale
       y0 = int(50 * scale)
       step = int(100 * scale)
       self.btn_positions = [
           (self.origin_x, y0),
           (self.origin_x + int(100 * scale), y0),

           (self.origin_x, y0 + step),
           (self.origin_x + int(100 * scale), y0 + step),

           (self.origin_x, y0 + 2*step),
           (self.origin_x + int(100 * scale), y0 + 2*step),

           (self.origin_x, y0 + 3*step),
           (self.origin_x + int(100 * scale), y0 + 3*step),

           (self.origin_x + int(100 * scale), y0 + 4*step)
       ]

    def resize(self, origin_x: int, font, btn_w: int, btn_h: int, scale: float):
       self.origin_x = origin_x
       self.btn_w = btn_w
       self.btn_h = btn_h
       self.my_font = font
       self.scale = scale

       y0 = int(50 * scale)
       step = int(100 * scale)
       self.btn_positions = [
           (self.origin_x, y0),
           (self.origin_x + int(100 * scale), y0),

           (self.origin_x, y0 + step),
           (self.origin_x + int(100 * scale), y0 + step),

           (self.origin_x, y0 + 2*step),
           (self.origin_x + int(100 * scale), y0 + 2*step),

           (self.origin_x, y0 + 3*step),
           (self.origin_x + int(100 * scale), y0 + 3*step),

           (self.origin_x + int(100 * scale), y0 + 4*step)
       ]

    def draw(self, pygame, surface):
        for index, pos in enumerate(self.btn_positions):
            # draw rect outline
            pygame.draw.rect(surface, self.color_normal, [pos[0], pos[1], self.btn_w, self.btn_h], width = max(2, self.btn_w//15), border_radius = max(2, self.btn_w//10))

            # hover highlight
            if self.button_hover(pos):
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width = max(2, self.btn_w//15), border_radius = max(2, self.btn_w//10))
                text_surface = self.my_font.render(str(index + 1), False, self.color_selected)
            else:
                text_surface = self.my_font.render(str(index + 1), False, self.color_normal)

            # selected highlight
            if self.selected_number > 0 and self.selected_number - 1 == index:
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width = max(2, self.btn_w//15), border_radius = max(2, self.btn_w//10))
                text_surface = self.my_font.render(str(index + 1), False, self.color_selected)

            # place number text centered-ish inside button
            text_x = pos[0] + max(5, (self.btn_w - text_surface.get_width()) // 2)
            text_y = pos[1] + max(0, (self.btn_h - text_surface.get_height()) // 2)
            surface.blit(text_surface, (text_x, text_y))

    def button_clicked(self, mouse_x: int, mouse_y: int) -> None:
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.selected_number = index + 1

    def button_hover(self, pos:tuple) -> bool | None:
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True
        return False

    def on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        return pos[0] < mouse_x < pos[0] + self.btn_w and pos[1] < mouse_y < pos[1] + self.btn_h
