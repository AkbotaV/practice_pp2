import pygame
import os

#pygame.init()
#pygame.mixer.init()

tracks=[f for f in os.listdir('music/')]
screen=pygame.display.set_mode((700,400))
#pygame.display.set_caption("Music Player")

print(tracks)
