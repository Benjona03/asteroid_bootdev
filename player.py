import pygame

from constants import PLAYER_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from constants import LINE_WIDTH

from circleshape import CircleShape

from constants import PLAYER_TURN_SPEED
from constants import PLAYER_SPEED

from shot import Shot

class Player(CircleShape):
    def __init__(self, x , y) -> None:
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen , "white" , self.triangle(), LINE_WIDTH)

    def rotate(self , dt ):
         self.rotation = self.rotation + (PLAYER_TURN_SPEED * dt)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shot_cooldown_timer -= dt

        if keys[pygame.K_a]: # Links
            self.rotate(-dt)
        if keys[pygame.K_d]: # Rechts
            self.rotate( dt)
        if keys[pygame.K_w]: # Vorwerts
            self.move( dt)
        if keys[pygame.K_s]: # Rückwerts
            self.move( -dt)

        if keys[pygame.K_SPACE]: #Schießen
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return

        else:
            self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
            neuer_schuss = Shot(self.position.x, self.position.y)
            shot_unit_vector = pygame.Vector2(0, 1)
            shot_rotated_vector = shot_unit_vector.rotate(self.rotation)
            shot_rotated_with_speed_vector = shot_rotated_vector * PLAYER_SHOOT_SPEED
            neuer_schuss.velocity = shot_rotated_with_speed_vector
