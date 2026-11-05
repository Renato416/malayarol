import pygame
import sys
from core.background import AnimatedBackground
from ui.window import DiceWindow
from ui.button import Button
from ui.character_panel import CharacterPanel
from entities.dice import D20, D6
from scenarios.school_scenario import SchoolScenario
from scenarios.simple_scenario import SimpleScenario

def main():
    pygame.init()
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Lanzador de Dados - Pygame")

    clock = pygame.time.Clock()
    bg = AnimatedBackground(speed_x=0.05, speed_y=0.05)
    font = pygame.font.SysFont(None, 24)

    windows = []
    panel_open = True
    btn_toggle_rect = pygame.Rect(0, 20, 30, 60)
    nav_width = 80 
    
    # Cargar los dos escenarios (el segundo usa bosque.png)
    scenarios = [SchoolScenario(), SimpleScenario("bosque.png")]
    current_scenario_idx = 0
    
    # Botones en la barra izquierda para cambiar mapa
    btn_sc1 = Button(10, 20, 60, 40, "E1", font)
    btn_sc2 = Button(10, 75, 60, 40, "E2", font)
    
    # Panel de personajes
    char_panel_width = 110
    char_panel = CharacterPanel(0, 40, char_panel_width, height - 80, font)

    def get_panel_rect():
        current_panel_width = screen.get_width() // 4
        if current_panel_width < 320: 
            current_panel_width = 320
        return pygame.Rect(screen.get_width() - (current_panel_width if panel_open else 0), 0, current_panel_width, screen.get_height())

    def add_window(dice_class):
        if not panel_open: return
        win_w = 300
        if len(windows) >= 2:
            windows.pop() 
        new_win = DiceWindow(0, 0, dice_class)
        new_win.scale = win_w / new_win.base_w
        new_win.rect.width = win_w
        new_win.rect.height = new_win.base_h * new_win.scale
        new_win.update_layout()
        windows.append(new_win)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        panel_rect = get_panel_rect()
        btn_toggle_rect.x = panel_rect.x - 30
        
        btn_d20_rect = pygame.Rect(panel_rect.x + 20, 20, 60, 60) if panel_open else pygame.Rect(-100, -100, 0, 0)
        btn_d6_rect = pygame.Rect(panel_rect.x + 90, 20, 60, 60) if panel_open else pygame.Rect(-100, -100, 0, 0)

        current_scenario = scenarios[current_scenario_idx]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if char_panel.handle_event(event):
                continue

            if btn_sc1.handle_event(event):
                current_scenario_idx = 0
            elif btn_sc2.handle_event(event):
                current_scenario_idx = 1

            current_scenario.handle_event(event)

            handled = False
            if panel_open:
                for w in reversed(windows):
                    if w.handle_event(event):
                        handled = True
                        break
                    
            if not handled and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if getattr(current_scenario, 'invisible_button_rect', None) and current_scenario.invisible_button_rect.collidepoint(event.pos):
                    print("¡Clic en las escaleras!")
                    
                if btn_toggle_rect.collidepoint(event.pos):
                    panel_open = not panel_open
                elif panel_open:
                    if btn_d20_rect.collidepoint(event.pos):
                        add_window(D20)
                    elif btn_d6_rect.collidepoint(event.pos):
                        add_window(D6)

        win_w = 300
        for i, w in enumerate(windows):
            w.rect.x = panel_rect.x + (panel_rect.width - win_w) // 2
            w.rect.y = 100 if i == 0 else 420
            w.update_layout()

        bg.update(dt)
        current_scenario.update(dt)
        
        if panel_open:
            for w in windows:
                w.update(dt)
            
        windows = [w for w in windows if w.is_active]

        # 1. Fondo Animado
        bg.draw(screen)
        
        # 2. Barra de Navegación Izquierda
        pygame.draw.line(screen, (255, 255, 255), (nav_width, 0), (nav_width, screen.get_height()), 2)
        btn_sc1.draw(screen)
        btn_sc2.draw(screen)

        # 3. Cálculo del área del escenario
        padding = 30
        char_x = nav_width + 15
        scenario_left = char_x + char_panel_width + padding
        max_w = panel_rect.x - scenario_left - padding
        max_h = screen.get_height() - (padding * 2)
        
        if max_w > 0 and max_h > 0:
            scened_w, scened_h = current_scenario.get_scaled_size(max_w, max_h)
            
            center_x = scenario_left + (max_w // 2)
            center_y = padding + (max_h // 2)
            
            scenario_rect = pygame.Rect(0, 0, scened_w, scened_h)
            scenario_rect.center = (center_x, center_y)
            
            # Alinear la ventana de personajes con la altura real del escenario
            char_panel.update_position(char_x, scenario_rect.y, scenario_rect.height)
            
            # Dibujar el escenario y su marco
            current_scenario.draw(screen, scenario_rect)
            pygame.draw.rect(screen, (255, 255, 255), scenario_rect, width=3, border_radius=20)

            # Dibujar la ventana de personajes (después del escenario para renderizar fichas sobre la interfaz)
            char_panel.draw(screen)

        # 4. Botón Desplegable
        pygame.draw.rect(screen, (100, 100, 180), btn_toggle_rect, border_bottom_left_radius=10, border_top_left_radius=10)
        toggle_text = font.render(">" if panel_open else "<", True, (255, 255, 255))
        screen.blit(toggle_text, (btn_toggle_rect.centerx - toggle_text.get_width()//2, btn_toggle_rect.centery - toggle_text.get_height()//2))

        # 5. Panel Derecho
        if panel_open:
            pygame.draw.line(screen, (255, 255, 255), (panel_rect.x, 0), (panel_rect.x, screen.get_height()), 2)
            
            pygame.draw.rect(screen, (255, 255, 255), btn_d20_rect, width=2, border_radius=5)
            text_d20 = font.render("D20", True, (255, 255, 255))
            screen.blit(text_d20, (btn_d20_rect.centerx - text_d20.get_width()//2, btn_d20_rect.centery - text_d20.get_height()//2))

            pygame.draw.rect(screen, (255, 255, 255), btn_d6_rect, width=2, border_radius=5)
            text_d6 = font.render("D6", True, (255, 255, 255))
            screen.blit(text_d6, (btn_d6_rect.centerx - text_d6.get_width()//2, btn_d6_rect.centery - text_d6.get_height()//2))

            for w in windows:
                w.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()