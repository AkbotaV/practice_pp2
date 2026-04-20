import pygame
import os
from datetime import datetime

pygame.init()

screen = pygame.display.set_mode((750, 550))
pygame.display.set_caption("Mickey Clock")
running = True
clock = pygame.time.Clock()

images_folder = os.path.join(os.path.dirname(__file__), "images")

background = pygame.image.load(os.path.join(images_folder, "clock.png"))
left_hand = pygame.image.load(os.path.join(images_folder, "left_h.png"))
right_hand = pygame.image.load(os.path.join(images_folder, "right_h.png"))

left_hand = pygame.transform.scale(left_hand, (270, 240))
right_hand = pygame.transform.scale(right_hand, (300, 100))
background = pygame.transform.scale(background, (750, 550))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    now = datetime.now()
    minutes = now.minute
    seconds = now.second
    minute_angle = -minutes * 6 -90
    second_angle = -seconds * 6 +50

    rotated_left = pygame.transform.rotate(left_hand, second_angle)
    rotated_right = pygame.transform.rotate(right_hand, minute_angle)
    left_rect = rotated_left.get_rect(center=(375, 275))
    right_rect = rotated_right.get_rect(center=(375, 275))
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    screen.blit(rotated_left, left_rect)
    screen.blit(rotated_right, right_rect)
    clock.tick(60)
    
    pygame.display.flip()

pygame.quit()