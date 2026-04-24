import pygame
from game_object import GameObject 
from game_object import Point 

class Wall(GameObject):
    def __init__(self, tile_width):
        super().__init__([],(89, 57, 31), tile_width)
        self.level = 0
        self.load_level()

    def load_level(self):
        f = open("levels/level{}.txt".format(self.level), "r")
        row = -1
        col = -1
        for line in f:
            row = row + 1
            col = -1
            for c in line:
                col = col + 1
                if c == '#':
                    self.points.append(Point(col * self.tile_width, row * self.tile_width))
        f.close()

    def next_level(self):
        self.points = []
        self.level = (self.level + 1) % 3
        self.load_level()
      
    def hit_wall(self,head):
      for point in self.points:
        if point.X==head.X and point.Y==head.Y:
          return True
      return False

        

