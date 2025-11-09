import pygame
import os
from grid import Grid, select_mode

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (400, 100)
pygame.init()

screen = pygame.display.set_mode((1200, 900), pygame.RESIZABLE)
pygame.display.set_caption("Sudoku!!")

mode_selected = select_mode(screen, pygame)
grid = Grid(pygame, window_size=(1200, 900), mode=mode_selected)

win_screen_active = False
start_ticks = pygame.time.get_ticks()
elapsed_before_pause = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # resize
        if event.type == pygame.VIDEORESIZE:
            w, h = event.w, event.h
            screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
            grid.resize(w, h)

        # mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            sel = grid.selection
            last_button_bottom = max(pos[1]+sel.btn_h for pos in sel.btn_positions)
            padding = max(8, int(12 * (sel.scale if hasattr(sel, "scale") else 1.0)))

            # Timer position
            timer_x = sel.btn_positions[0][0]
            timer_y = last_button_bottom + padding
            timer_surface = grid.font_small.render("Time: 00:00", True, (10,10,10))
            timer_height = timer_surface.get_height()

            # Restart button below the timer
            restart_w = max(60, int(sel.btn_w * 1.1))
            restart_h = max(28, int(sel.btn_h * 0.7))
            restart_x = timer_x
            restart_y = timer_y + timer_height + padding
            restart_rect = pygame.Rect(restart_x, restart_y, restart_w, restart_h)

            if restart_rect.collidepoint(mx, my):
                mode_selected = select_mode(screen, pygame)
                grid.restart(mode_selected)
                win_screen_active = False
                start_ticks = pygame.time.get_ticks()
                elapsed_before_pause = 0
                continue

            if not grid.win:
                grid.get_mouse_click(mx, my)

        # space to restart after win
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.win:
                mode_selected = select_mode(screen, pygame)
                grid.restart(mode_selected)
                win_screen_active = False
                start_ticks = pygame.time.get_ticks()
                elapsed_before_pause = 0

    if grid.win and not win_screen_active:
        win_screen_active = True

    # timer
    if not grid.win:
        elapsed_ms = pygame.time.get_ticks() - start_ticks + elapsed_before_pause
    else:
        if elapsed_before_pause == 0:
            elapsed_before_pause = pygame.time.get_ticks() - start_ticks
        elapsed_ms = elapsed_before_pause

    total_seconds = int(elapsed_ms // 1000)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_text = f"{minutes:02}:{seconds:02}"

    screen.fill((255, 233, 236))
    grid.draw_all(pygame, screen)

    sel = grid.selection
    last_button_bottom = max(pos[1]+sel.btn_h for pos in sel.btn_positions)
    padding = max(8, int(12 * (sel.scale if hasattr(sel, "scale") else 1.0)))

    timer_surface = grid.font_small.render(f"Time: {time_text}", True, (10, 10, 10))
    timer_x = sel.btn_positions[0][0]
    timer_y = last_button_bottom + padding
    screen.blit(timer_surface, (timer_x, timer_y))

    # Restart button below timer
    restart_w = max(60, int(sel.btn_w*1.1))
    restart_h = max(28, int(sel.btn_h*0.7))
    restart_x = timer_x
    restart_y = timer_y + timer_surface.get_height() + padding

    restart_rect = pygame.Rect(restart_x, restart_y, restart_w, restart_h)
    pygame.draw.rect(screen, (129,19,49), restart_rect, border_radius=8)

    btn_font = pygame.font.SysFont('Avenir Next', 25)
    btn_text = btn_font.render("Restart", True, (255,255,255))
    screen.blit(btn_text, (restart_rect.centerx - btn_text.get_width()//2, restart_rect.centery - btn_text.get_height()//2))

    if win_screen_active:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,160))
        screen.blit(overlay, (0,0))

        box_width = min(700, int(screen.get_width()*0.6))
        box_height = min(380, int(screen.get_height()*0.45))
        box_x = (screen.get_width()-box_width)//2
        box_y = (screen.get_height()-box_height)//2

        pygame.draw.rect(screen, (255,245,238), (box_x, box_y, box_width, box_height), border_radius=18)
        pygame.draw.rect(screen, (129,19,49), (box_x, box_y, box_width, box_height), width=4, border_radius=18)

        won_surface = grid.game_font.render("You Win!", True, (250,120,160))
        screen.blit(won_surface, won_surface.get_rect(center=(screen.get_width()//2, box_y + box_height//3)))

        instr_surface = grid.font_small.render("Press SPACE to Restart", True, (227,115,131))
        screen.blit(instr_surface, instr_surface.get_rect(center=(screen.get_width()//2, box_y + box_height//2)))

        final_surface = grid.font_small.render(f"Final Time: {time_text}", True, (0,0,0))
        screen.blit(final_surface, final_surface.get_rect(center=(screen.get_width()//2, box_y + box_height//2 + 40)))

    pygame.display.flip()

pygame.quit()

