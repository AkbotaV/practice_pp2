import pygame
import random
from game_object import GameObject, Point

field_lifetime=8000
effect_duratiion=5000

class Powerup(GameObject):
  def __init__(self,tile_width,worm,wall):
    self.kind=random.choice(["speed","slow","shield"])
    self.spawn_time=pygame.time.get_ticks()
    self.tile_width=tile_width

    if self.kind == "speed":
            color = (255, 200, 40)    # золотой
    elif self.kind == "slow":
            color = (0, 220, 220)     # cyan
    else:
            color = (255, 80, 160)    # розовый (shield)

    while True:
            x = random.randrange(0, 400, tile_width)
            y = random.randrange(0, 300, tile_width)

            ok = True
            for p in worm.points:
                if p.X == x and p.Y == y:
                    ok = False
                    break
            for p in wall.points:
                if p.X == x and p.Y == y:
                    ok = False
                    break
            if ok:
                break

    super().__init__([Point(x, y)], color, tile_width)
    
  def can_collect(self, head):
        for point in self.points:
            if point.X == head.X and point.Y == head.Y:
                return True
        return False

  def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > field_lifetime