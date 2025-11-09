from random import sample
from selection import SelectNumber
from copy import deepcopy

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

def pattern(row_num: int, col_num: int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE

def shuffle(samp: range) -> list:
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list]:
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]

def remove_numbers(grid: list[list], mode='easy') -> None:
    num_of_cells = GRID_SIZE * GRID_SIZE
    if mode == 'easy':
        empties = num_of_cells * 3 // 7
    elif mode == 'medium':
        empties = num_of_cells * 3 // 6
    elif mode == 'hard':
        empties = num_of_cells * 3 // 5
    else:
        empties = num_of_cells * 3 // 7

    for i in sample(range(num_of_cells), empties):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        grid[row][col] = 0

def select_mode(screen, pygame):
    clock = pygame.time.Clock()
    width, height = screen.get_size()

    # define mode buttons
    btn_w, btn_h = 180, 60
    padding = 20
    total_height = 3*btn_h + 2*padding
    start_y = (height - total_height) // 2
    btn_x = (width - btn_w) // 2

    buttons = [
        ("Easy", pygame.Rect(btn_x, start_y, btn_w, btn_h)),
        ("Medium", pygame.Rect(btn_x, start_y + btn_h + padding, btn_w, btn_h)),
        ("Hard", pygame.Rect(btn_x, start_y + 2*(btn_h + padding), btn_w, btn_h)),
    ]

    title_font = pygame.font.SysFont('Avenir Next', 60)
    title_surface = title_font.render("Sudoku", True, (250, 120, 160))
    title_rect = title_surface.get_rect(center=(width//2, start_y - 60))  # above first button

    selecting = True
    selected_mode = "easy"  # default
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for mode, rect in buttons:
                    if rect.collidepoint(mx, my):
                        selected_mode = mode.lower()
                        selecting = False

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255,245,238, 180))
        screen.blit(overlay, (0, 0))

        # draw title
        screen.blit(title_surface, title_rect)

        # draw buttons
        for mode, rect in buttons:
            pygame.draw.rect(screen, (129, 19, 49), rect, border_radius=12)
            btn_font = pygame.font.SysFont('Avenir Next', 30)
            text_surface = btn_font.render(mode, True, (255, 255, 255))
            screen.blit(text_surface, (rect.centerx - text_surface.get_width()//2,
                                       rect.centery - text_surface.get_height()//2))

        pygame.display.flip()
        clock.tick(30)

    return selected_mode

class Grid:
    BASE_WIDTH = 1200
    BASE_HEIGHT = 900
    BASE_CELL_SIZE = 100
    BASE_BTN_AREA_OFFSET = 50
    BASE_BTN_W = 80
    BASE_BTN_H = 80
    BASE_FONT_SIZE = 50
    BASE_FONT_SMALL = 25
    BASE_NUM_X_OFFSET = 35
    BASE_NUM_Y_OFFSET = 12

    def __init__(self, pygame, window_size=(1200, 900), mode='easy'):
        self.mode = mode
        self.pygame = pygame
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid, mode=self.mode)
        self.occupied = self.pre_occupied_cells()
        self.win = False

        self.cell_size = self.BASE_CELL_SIZE
        self.num_x_offset = self.BASE_NUM_X_OFFSET
        self.num_y_offset = self.BASE_NUM_Y_OFFSET
        self.line_coordinates = []
        self.grid_pixel = 900
        self.font_small = None
        self.game_font = None
        self.selection = None

        w, h = window_size
        self.resize(w, h)

    def restart(self, mode=None):
        if mode:
            self.mode = mode
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        remove_numbers(self.grid, mode=self.mode)
        self.occupied = self.pre_occupied_cells()
        self.win = False

    def check_grids(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def is_cell_pre_occupied(self, x:int, y:int) -> bool:
        return (y, x) in self.occupied

    def get_mouse_click(self, x:int, y:int) -> None:
        if 0 <= x < self.grid_pixel and 0 <= y < self.grid_pixel:
            grid_x, grid_y = x // self.cell_size, y // self.cell_size
            if 0 <= grid_x < 9 and 0 <= grid_y < 9:
                if not self.is_cell_pre_occupied(grid_x, grid_y):
                    self.set_cell(grid_x, grid_y, self.selection.selected_number)
        self.selection.button_clicked(x, y)
        if self.check_grids():
            self.win = True

    def pre_occupied_cells(self) -> list[tuple]:
        return [(y, x) for y in range(9) for x in range(9) if self.get_cell(x, y) != 0]

    def __draw_lines(self, surface) -> None:
        for i in range(1, 9):
            start = (0, i * self.cell_size)
            end = (self.grid_pixel, i * self.cell_size)
            color = (255, 106, 128) if i % 3 == 0 else (0, 0, 0)
            width = max(2, self.cell_size//20) if i % 3 == 0 else max(1, self.cell_size//40)
            self.pygame.draw.line(surface, color, start, end, width)
        for i in range(1, 10):
            start = (i * self.cell_size, 0)
            end = (i * self.cell_size, self.grid_pixel)
            color = (255, 106, 128) if i % 3 == 0 else (0, 0, 0)
            width = max(2, self.cell_size//20) if i % 3 == 0 else max(1, self.cell_size//40)
            self.pygame.draw.line(surface, color, start, end, width)

    def __draw_numbers(self, surface) -> None:
        for y in range(9):
            for x in range(9):
                val = self.get_cell(x, y)
                if val != 0:
                    if (y, x) in self.occupied:
                        color = (0, 0, 0)
                    else:
                        color = (0, 0, 0)
                    if val != self.__test_grid[y][x]:
                        color = (255, 0, 0)
                    surface.blit(self.game_font.render(str(val), False, color),
                                 (x * self.cell_size + self.num_x_offset,
                                  y * self.cell_size + self.num_y_offset))

    def draw_all(self, pg, surface):
        self.__draw_lines(surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg, surface)

    def get_cell(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
        self.grid[y][x] = value

    def resize(self, new_width: int, new_height: int) -> None:
        scale = min(new_width / self.BASE_WIDTH, new_height / self.BASE_HEIGHT)
        self.cell_size = max(10, int(self.BASE_CELL_SIZE * scale))
        self.grid_pixel = self.cell_size * 9
        self.num_x_offset = max(1, int(self.BASE_NUM_X_OFFSET * scale))
        self.num_y_offset = max(1, int(self.BASE_NUM_Y_OFFSET * scale))
        
        font_size = max(12, int(self.BASE_FONT_SIZE * scale))
        small_size = max(10, int(self.BASE_FONT_SMALL * scale))
        self.game_font = self.pygame.font.SysFont('Avenir Next', font_size)
        self.font_small = self.pygame.font.SysFont('Avenir Next', small_size)

        btn_area_offset = int(self.BASE_BTN_AREA_OFFSET * scale)
        btn_origin_x = self.grid_pixel + btn_area_offset
        btn_w = max(20, int(self.BASE_BTN_W * scale))
        btn_h = max(20, int(self.BASE_BTN_H * scale))

        if self.selection is None:
            self.selection = SelectNumber(self.pygame, self.game_font, origin_x=btn_origin_x,
                                          btn_w=btn_w, btn_h=btn_h, scale=scale)
        else:
            self.selection.resize(origin_x=btn_origin_x, font=self.game_font,
                                  btn_w=btn_w, btn_h=btn_h, scale=scale)
    