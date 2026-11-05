import pygame
import random
import math

class D20:
    def __init__(self, x, y, radius=70, is_gray=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.value = 20
        self.is_rolling = False
        self.roll_timer = 0.0
        self.roll_duration = 1.0
        self.is_gray = is_gray
        self.blink_timer = 0.0
        self.winning_face_idx = -1
        self.tension = 0.0 
        
        self.font = pygame.font.SysFont(None, int(radius * 0.5))
        
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0
        self.spin_x = 0.0
        self.spin_y = 0.0
        self.spin_z = 0.0

        phi = (1 + math.sqrt(5)) / 2
        verts = [
            (-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0),
            (0, -1, phi), (0, 1, phi), (0, -1, -phi), (0, 1, -phi),
            (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1)
        ]
        
        length = math.sqrt(1 + phi**2)
        self.base_vertices = [(vx/length, vy/length, vz/length) for vx, vy, vz in verts]
        
        self.faces = [
            (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
            (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
            (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
            (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
        ]
        self.face_numbers = list(range(1, 21))

    def roll(self):
        self.is_rolling = True
        self.roll_timer = self.roll_duration
        self.winning_face_idx = -1
        self.spin_x = random.uniform(10, 25)
        self.spin_y = random.uniform(10, 25)
        self.spin_z = random.uniform(10, 25)

    def _rotate_3d(self, x, y, z):
        y1 = y * math.cos(self.angle_x) - z * math.sin(self.angle_x)
        z1 = y * math.sin(self.angle_x) + z * math.cos(self.angle_x)
        x2 = x * math.cos(self.angle_y) + z1 * math.sin(self.angle_y)
        z2 = -x * math.sin(self.angle_y) + z1 * math.cos(self.angle_y)
        x3 = x2 * math.cos(self.angle_z) - y1 * math.sin(self.angle_z)
        y3 = x2 * math.sin(self.angle_z) + y1 * math.cos(self.angle_z)
        return x3, y3, z2

    def update(self, dt):
        if self.is_rolling:
            self.roll_timer -= dt
            friction = max(0.1, self.roll_timer / self.roll_duration)
            self.angle_x += self.spin_x * dt * friction
            self.angle_y += self.spin_y * dt * friction
            self.angle_z += self.spin_z * dt * friction
            
            if self.roll_timer <= 0:
                self.is_rolling = False
                self.value = random.randint(1, 20)
                self.blink_timer = 0.0
                
                max_nz = -float('inf')
                front_face_idx = 0
                for i, face in enumerate(self.faces):
                    v1 = self._rotate_3d(*self.base_vertices[face[0]])
                    v2 = self._rotate_3d(*self.base_vertices[face[1]])
                    v3 = self._rotate_3d(*self.base_vertices[face[2]])
                    nz = (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
                    if nz > max_nz:
                        max_nz = nz
                        front_face_idx = i
                self.winning_face_idx = front_face_idx
                
                random.shuffle(self.face_numbers)
                current_val_idx = self.face_numbers.index(self.value)
                self.face_numbers[current_val_idx], self.face_numbers[front_face_idx] = self.face_numbers[front_face_idx], self.face_numbers[current_val_idx]
        else:
            self.blink_timer += dt

    def draw(self, surface):
        transformed = [self._rotate_3d(*v) for v in self.base_vertices]
        faces_to_draw = []
        vib_x = random.uniform(-15, 15) * self.tension if not self.is_rolling else 0
        vib_y = random.uniform(-15, 15) * self.tension if not self.is_rolling else 0
        base_x = self.x + vib_x
        base_y = self.y + vib_y

        for i, face in enumerate(self.faces):
            v1, v2, v3 = [transformed[idx] for idx in face]
            nz = (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
            if nz > 0:
                avg_z = (v1[2] + v2[2] + v3[2]) / 3
                light = max(0.3, min(1.0, nz / 1.5))
                if self.is_gray:
                    base_r, base_g, base_b = 130, 115, 150
                else:
                    base_r, base_g, base_b = 112, 52, 212
                r, g, b = int(base_r * light), int(base_g * light), int(base_b * light)
                if not self.is_rolling and i == self.winning_face_idx:
                    blink = (math.sin(self.blink_timer * 8) + 1) / 2
                    r = int(r + (220 - r) * blink)
                    g = int(g + (220 - g) * blink)
                    b = int(b + (255 - b) * blink)

                color = (r, g, b)
                border_color = (180, 170, 210)
                pts2d = [(base_x + v[0] * self.radius, base_y + v[1] * self.radius) for v in (v1, v2, v3)]
                cx = sum(p[0] for p in pts2d) / 3
                cy = sum(p[1] for p in pts2d) / 3
                faces_to_draw.append((avg_z, pts2d, color, border_color, self.face_numbers[i], cx, cy, nz))

        faces_to_draw.sort(key=lambda item: item[0])
        for _, pts2d, color, border, num, cx, cy, nz in faces_to_draw:
            pygame.draw.polygon(surface, color, pts2d)
            pygame.draw.polygon(surface, border, pts2d, 2)
            if nz > 0.4:
                text_surf = self.font.render(str(num), True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(cx, cy))
                surface.blit(text_surf, text_rect)


class D6(D20):
    def __init__(self, x, y, radius=70, is_gray=False):
        super().__init__(x, y, radius, is_gray)
        self.value = 6
        
        # Vertices de un cubo
        length = math.sqrt(3) # Para normalizar al radio
        verts = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]
        self.base_vertices = [(vx/length, vy/length, vz/length) for vx, vy, vz in verts]
        
        # Caras del cubo (2 triángulos por cara)
        self.faces = [
            (0, 1, 2), (0, 2, 3), # Frente
            (1, 5, 6), (1, 6, 2), # Derecha
            (5, 4, 7), (5, 7, 6), # Atrás
            (4, 0, 3), (4, 3, 7), # Izquierda
            (3, 2, 6), (3, 6, 7), # Arriba
            (4, 5, 1), (4, 1, 0)  # Abajo
        ]
        # Asociar números a las caras (1 número por par de triángulos)
        self.face_pairs = [[0,1], [2,3], [4,5], [6,7], [8,9], [10,11]]
        self.face_numbers = list(range(1, 7))

    def update(self, dt):
        if self.is_rolling:
            self.roll_timer -= dt
            friction = max(0.1, self.roll_timer / self.roll_duration)
            self.angle_x += self.spin_x * dt * friction
            self.angle_y += self.spin_y * dt * friction
            self.angle_z += self.spin_z * dt * friction
            
            if self.roll_timer <= 0:
                self.is_rolling = False
                self.value = random.randint(1, 6)
                self.blink_timer = 0.0
                
                max_nz = -float('inf')
                front_pair_idx = 0
                
                for i, pair in enumerate(self.face_pairs):
                    f = self.faces[pair[0]]
                    v1 = self._rotate_3d(*self.base_vertices[f[0]])
                    v2 = self._rotate_3d(*self.base_vertices[f[1]])
                    v3 = self._rotate_3d(*self.base_vertices[f[2]])
                    nz = (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
                    if nz > max_nz:
                        max_nz = nz
                        front_pair_idx = i
                        
                self.winning_face_idx = front_pair_idx
                random.shuffle(self.face_numbers)
                curr_idx = self.face_numbers.index(self.value)
                self.face_numbers[curr_idx], self.face_numbers[front_pair_idx] = self.face_numbers[front_pair_idx], self.face_numbers[curr_idx]
        else:
            self.blink_timer += dt

    def draw(self, surface):
        transformed = [self._rotate_3d(*v) for v in self.base_vertices]
        faces_to_draw = []
        vib_x = random.uniform(-15, 15) * self.tension if not self.is_rolling else 0
        vib_y = random.uniform(-15, 15) * self.tension if not self.is_rolling else 0
        base_x = self.x + vib_x
        base_y = self.y + vib_y

        for i, pair in enumerate(self.face_pairs):
            f1, f2 = self.faces[pair[0]], self.faces[pair[1]]
            
            # Usar primer triángulo para normal
            v1, v2, v3 = [transformed[idx] for idx in f1]
            nz = (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0])
            
            if nz > 0:
                avg_z = sum(transformed[idx][2] for idx in set(f1+f2)) / 4
                light = max(0.3, min(1.0, nz / 1.5))
                
                if self.is_gray:
                    base_r, base_g, base_b = 130, 115, 150
                else:
                    base_r, base_g, base_b = 112, 52, 212
                r, g, b = int(base_r * light), int(base_g * light), int(base_b * light)
                
                if not self.is_rolling and i == self.winning_face_idx:
                    blink = (math.sin(self.blink_timer * 8) + 1) / 2
                    r = int(r + (220 - r) * blink)
                    g = int(g + (220 - g) * blink)
                    b = int(b + (255 - b) * blink)

                color = (r, g, b)
                border_color = (180, 170, 210)
                
                # Obtener los 4 puntos del cuadrado (removiendo duplicados)
                quad_idxs = list(dict.fromkeys(f1 + f2))
                # Ordenar los vértices para hacer un polígono convexo
                pts2d = [(base_x + transformed[idx][0] * self.radius, base_y + transformed[idx][1] * self.radius) for idx in quad_idxs]
                
                cx = sum(p[0] for p in pts2d) / 4
                cy = sum(p[1] for p in pts2d) / 4
                
                # Truco simple: ordenar por ángulo desde el centro para asegurar que el cuadrado se dibuje bien
                pts2d = sorted(pts2d, key=lambda p: math.atan2(p[1]-cy, p[0]-cx))
                
                faces_to_draw.append((avg_z, pts2d, color, border_color, self.face_numbers[i], cx, cy, nz))

        faces_to_draw.sort(key=lambda item: item[0])
        for _, pts2d, color, border, num, cx, cy, nz in faces_to_draw:
            pygame.draw.polygon(surface, color, pts2d)
            pygame.draw.polygon(surface, border, pts2d, 2)
            if nz > 0.4:
                text_surf = self.font.render(str(num), True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(cx, cy))
                surface.blit(text_surf, text_rect)