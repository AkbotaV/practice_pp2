from game_object import GameObject
from game_object import Point
import pygame
import random


class Food(GameObject): 
  def __init__(self, tile_width,worm,wall): 
    self.weight = random.randint(1, 3)

        # Different colors and lifetime for different food
    if self.weight == 1:
            color = (255, 0, 0)       # red
            self.lifetime = 100000      # 100 seconds
    elif self.weight == 2:
            color = (255, 165, 0)     # orange-yellow
            self.lifetime = 40000      # 40 seconds
    else:
            color = (128, 0, 128)     # purple
            self.lifetime = 3000      # 3 seconds

        # Save spawn time
    self.spawn_time = pygame.time.get_ticks()

    while True:
        x = random.randrange(0, 400, tile_width)
        y = random.randrange(0, 300, tile_width)

        ok = True
        for p in worm.points:
            if p.X == x and p.Y == y:
                ok = False

        for p in wall.points:
            if p.X == x and p.Y == y:
                ok = False

        if ok:
            break

    super().__init__([Point(x, y)], color , tile_width)

  def can_eat(self,head_location):
        result=None
        for point in self.points:
            if point.X==head_location.X and point.Y == head_location.Y:
                result=point
                break
        return  result

  def is_expired(self):
            return pygame.time.get_ticks() - self.spawn_time > self.lifetime

class Poison_food(GameObject):
    def __init__(self,tile_width,worm,wall):
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 6000
        while True:

            x = random.randrange(0, 400, tile_width)
            y = random.randrange(0, 300, tile_width)

            ok=True

            for p in worm.points:
                if p.X==x and p.Y==y:
                    ok=False
                    break
            for p in wall.points:
                if p.X==x and p.Y==y:
                    ok=False
                    break
            if ok:
                break
        super().__init__([Point(x,y)],(120,20,20),tile_width) #brown red


    def can_eat(self,head_location):
        result=None
        for point in self.points:
            if point.X==head_location.X and point.Y == head_location.Y:
                result=point
                break
        return  result

    def is_expired(self):
            return pygame.time.get_ticks() - self.spawn_time > self.lifetime