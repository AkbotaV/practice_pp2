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

    def add_obstacles(self, worm):
        import random
        count = 5 + self.level * 2  

        attempts = 0
        added = 0
        while added < count and attempts < 500:
            attempts += 1
            x = random.randrange(20, 380, self.tile_width)  
            y = random.randrange(20, 280, self.tile_width)

            ok = True

            
            for p in worm.points:
                if p.X == x and p.Y == y:
                    ok = False
                    break

            
            for p in self.points:
                if p.X == x and p.Y == y:
                    ok = False
                    break

            
            head = worm.points[0]
            if abs(head.X - x) < self.tile_width * 3 and abs(head.Y - y) < self.tile_width * 3:
                ok = False

            if ok:
                self.points.append(Point(x, y))
                added += 1
        

