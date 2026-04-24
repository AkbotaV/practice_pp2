from game_object import GameObject
from game_object import Point
import pygame
import random


class Food(GameObject): 
  def __init__(self, tile_width,worm,wall): 

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
