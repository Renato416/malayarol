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
    # =========================================================
    # 1. CONFIGURACIÓN INICIAL DE PYGAME Y VENTANA
    # =========================================================
    pygame.init()
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Lanzador de Dados - Pygame")

    clock = pygame.time.Clock()
    bg = AnimatedBackground(speed_x=0.05, speed_y=0.05)
    font = pygame.font.SysFont(None, 24)

    # =========================================================
    # 2. VARIABLES DE INTERFAZ Y PANELES
    # =========================================================
    windows = []
    panel_open = True
    btn_toggle_rect = pygame.Rect(0, 20, 30, 60)
    nav_width = 80 
    
    # =========================================================
    # 3. CARGA DE ESCENARIOS (MAPAS)
    # =========================================================
    scenarios = [SchoolScenario(), SimpleScenario("bosque.png")]
    current_scenario_idx = 0
    
    # Botones en la barra izquierda para cambiar mapa
    btn_sc1 = Button(10, 20, 60, 40, "E1", font)
    btn_sc2 = Button(10, 75, 60, 40, "E2", font)
    
    # Panel de personajes (Barra de Jugadores)
    char_panel_width = 110
    char_panel = CharacterPanel(0, 40, char_panel_width, font)

    # =========================================================
    # 4. FUNCIONES AUXILIARES DE INTERFAZ
    # =========================================================
    def get_panel_rect():
        """Calcula el tamaño y posición del panel lateral derecho."""
        current_panel_width = screen.get_width() // 4
        if current_panel_width < 320: 
            current_panel_width = 320
        return pygame.Rect(screen.get_width() - (current_panel_width if panel_open else 0), 0, current_panel_width, screen.get_height())

    def add_window(dice_class):
        """Agrega una nueva ventana de dado (D20 o D6)."""
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

    # =========================================================
    # 5. BUCLE PRINCIPAL DEL JUEGO
    # =========================================================
    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        # Actualizar área del panel derecho y botones dinámicos
        panel_rect = get_panel_rect()
        btn_toggle_rect.x = panel_rect.x - 30
        btn_d20_rect = pygame.Rect(panel_rect.x + 20, 20, 60, 60) if panel_open else pygame.Rect(-100, -100, 0, 0)
        btn_d6_rect = pygame.Rect(panel_rect.x + 90, 20, 60, 60) if panel_open else pygame.Rect(-100, -100, 0, 0)

        current_scenario = scenarios[current_scenario_idx]

        # ---------------------------------------------------------
        # 5A. MANEJO DE EVENTOS (CLICS Y TECLADO)
        # ---------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Eventos del panel de personajes (Arrastrar fichas, botones +/-)
            if char_panel.handle_event(event):
                continue

            # Eventos de los botones de cambio de escenario
            if btn_sc1.handle_event(event):
                current_scenario_idx = 0
                char_panel.reset()  # <- Fuerza a los personajes a reiniciarse
            elif btn_sc2.handle_event(event):
                current_scenario_idx = 1
                char_panel.reset()  # <- Fuerza a los personajes a reiniciarse

            # Eventos propios del mapa (botones de habitaciones, etc)
            current_scenario.handle_event(event)

            # Eventos de las ventanas de dados
            handled = False
            if panel_open:
                for w in reversed(windows):
                    if w.handle_event(event):
                        handled = True
                        break
                    
            # Eventos de botones generales (abrir panel, generar dados)
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

        # ---------------------------------------------------------
        # 5B. ACTUALIZACIÓN LÓGICA (ANIMACIONES Y POSICIONES)
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # 5C. DIBUJO DE INTERFAZ (RENDERIZADO)
        # ---------------------------------------------------------
        
        # Capa 1: Fondo Animado
        bg.draw(screen)
        
        # Capa 2: Barra de Navegación Izquierda (Botones de Mapa)
        pygame.draw.line(screen, (255, 255, 255), (nav_width, 0), (nav_width, screen.get_height()), 2)
        btn_sc1.draw(screen)
        btn_sc2.draw(screen)

        # Capa 3: Área del Escenario Central y Panel de Personajes
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
            
            # Dibujar el mapa (escenario)
            current_scenario.draw(screen, scenario_rect)
            pygame.draw.rect(screen, (255, 255, 255), scenario_rect, width=3, border_radius=20)

            # Dibujar el panel de personajes (Barra de jugadores)
            char_panel.update_position(char_x, scenario_rect.y)
            char_panel.draw(screen)

        # Capa 4: Botón Desplegable del Panel Derecho (< / >)
        pygame.draw.rect(screen, (100, 100, 180), btn_toggle_rect, border_bottom_left_radius=10, border_top_left_radius=10)
        toggle_text = font.render(">" if panel_open else "<", True, (255, 255, 255))
        screen.blit(toggle_text, (btn_toggle_rect.centerx - toggle_text.get_width()//2, btn_toggle_rect.centery - toggle_text.get_height()//2))

        # Capa 5: Panel Derecho (Dados y Lanzador)
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

        # Mostrar todo en pantalla
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()