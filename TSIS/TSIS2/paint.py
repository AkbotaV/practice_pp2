import pygame
import math
from datetime import datetime


pygame.init()
running=True
screen=pygame.display.set_mode((500,400))
another_layer=pygame.Surface((500,400))
clock=pygame.time.Clock()


tool=0
tools_count=11
#0.pencil  1.rect  2.fill 3.circle 4.eraser 5.Square 6.Right triangle 7.Equilateral triangle 8.rhombus 9.line 10.text

background_color=(255,255,255)
eraser_color=background_color
screen.fill(background_color)
another_layer.blit(screen, (0, 0))
colors=[
  (255,0,0),
  (0,255,0),
  (0, 0, 255),
  (0,0,0)
]
color_index=2
color=colors[color_index]

brush_sizes = [2, 5, 10]
brush_index = 0
brush_size = brush_sizes[brush_index]


x1 = y1 = x2 = y2 = 0
isMouseDown = False
queue=[]


font = pygame.font.SysFont("arial", 28)
text_active = False
text_value = ""
text_pos = (0, 0)


def getRectangle(x1, y1, x2, y2):
    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x1 - x2)
    h = abs(y1 - y2)
    return (x, y, w, h)

def getSquare(x1, y1, x2, y2):
    side = min(abs(x2 - x1), abs(y2 - y1))
    return (x1, y1, side, side)

def getCircle(x1, y1, x2, y2):
    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    return radius

def step(screen, x, y, origin_color, fill_color):
    if x < 0 or y < 0: return False
    if x >= 500 or y >= 400: return False
    if screen.get_at((x, y)) != origin_color: return False
    queue.append((x, y))
    screen.set_at((x, y), fill_color)

def saveCanvas():
    time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "paint_" + time + ".jpeg"
    pygame.image.save(screen, filename)
    print("saved:", filename)

while running:
  for event in pygame.event.get():
    
    if event.type==pygame.QUIT:
              running=False

    if event.type==pygame.KEYDOWN:
              if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                  saveCanvas()
              if event.key == pygame.K_1:
                  brush_size = 2
              elif event.key == pygame.K_2:
                  brush_size = 5
              elif event.key == pygame.K_3:
                  brush_size = 10

              if event.key == pygame.K_r:
                  color = colors[0]
              elif event.key == pygame.K_g:
                  color = colors[1]
              elif event.key == pygame.K_b:
                  color = colors[2]
              elif event.key == pygame.K_k:
                  color = colors[3]

              if text_active:
                    if event.key == pygame.K_RETURN:
                        text_surface = font.render(text_value, True, color)
                        screen.blit(text_surface, text_pos)
                        another_layer.blit(screen, (0, 0))
                        text_active = False
                        text_value = ""

                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_value = ""

                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]

                    else:
                        text_value += event.unicode

    if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                  isMouseDown=True
                  x1,y1=event.pos
                  x2,y2=event.pos

                  if tool == 2:  #fill
                      origin_color = screen.get_at((x1, y1))

                      if origin_color != color:
                          queue.append((x1, y1))
                          screen.set_at((x1, y1), color) 

                          while len(queue) > 0:
                              cur = queue[0]
                              queue.pop(0)

                              step(screen, cur[0] + 1, cur[1], origin_color, color)
                              step(screen, cur[0] - 1, cur[1], origin_color, color)
                              step(screen, cur[0], cur[1] + 1, origin_color, color)
                              step(screen, cur[0], cur[1] - 1, origin_color, color)

                          another_layer.blit(screen, (0, 0))
                  elif tool == 10:
                      text_active = True
                      text_value = ""
                      text_pos = event.pos

                elif event.button==3:
                  tool = (tool + 1) % tools_count

    
    if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:

                if tool == 1:
                    pygame.draw.rect(screen,color, pygame.Rect(getRectangle(x1, y1, x2, y2)),brush_size)

                elif tool == 3:
                    r = getCircle(x1, y1, x2, y2)
                    pygame.draw.circle(screen, color, (x1, y1), r, brush_size)

                  
                elif tool == 5:
                    pygame.draw.rect(screen, color, getSquare(x1, y1, x2, y2), brush_size)

                elif tool == 6:
                    points = [(x1, y1), (x2, y1), (x1, y2)]
                    pygame.draw.polygon(screen, color, points, brush_size)

                elif tool == 7:
                  side = abs(x2 - x1)
                  h = int(side * math.sqrt(3) / 2)
                  points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - h)]
                  pygame.draw.polygon(screen, color, points, brush_size)

                elif tool == 8:
                  cx = (x1 + x2) // 2
                  cy = (y1 + y2) // 2
                  points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                  pygame.draw.polygon(screen, color, points, brush_size)


                elif tool == 9:
                   pygame.draw.line(screen, color, (x1, y1), (x2, y2), brush_size)

                another_layer.blit(screen, (0, 0))
            isMouseDown = False



    if event.type == pygame.MOUSEMOTION:
      
                if isMouseDown:

                    if tool == 0:  # pencil
                        old_x, old_y = x2, y2
                        x2, y2 = event.pos
                        pygame.draw.line(screen, color, (old_x, old_y), (x2, y2), brush_size)

                    elif tool == 1:  # rectangle preview
                        x2, y2 = event.pos
                        screen.blit(another_layer, (0, 0))
                        pygame.draw.rect(screen, color, pygame.Rect(getRectangle(x1, y1, x2, y2)),brush_size)

                    elif tool == 3:  # circle preview
                        x2, y2 = event.pos
                        screen.blit(another_layer, (0, 0))
                        r = getCircle(x1, y1, x2, y2)
                        pygame.draw.circle(screen, color, (x1, y1), r, brush_size)

                    elif tool == 4:  # eraser
                        old_x, old_y = x2, y2
                        x2, y2 = event.pos
                        pygame.draw.line(screen, background_color, (old_x, old_y), (x2, y2), brush_size)
                      
                    elif tool == 5:
                        x2, y2 = event.pos
                        screen.blit(another_layer, (0, 0))
                        pygame.draw.rect(screen, color, getSquare(x1, y1, x2, y2), brush_size)

                    elif tool == 6:
                        x2, y2 = event.pos
                        screen.blit(another_layer, (0, 0))
                        points = [(x1, y1), (x2, y1), (x1, y2)]
                        pygame.draw.polygon(screen, color, points, brush_size)

                    elif tool == 7:
                        x2, y2 = event.pos
                        screen.blit(another_layer, (0, 0))
                        side = abs(x2 - x1)
                        h = int(side * math.sqrt(3) / 2)
                        points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - h)]
                        pygame.draw.polygon(screen, color, points, brush_size)

                    elif tool == 8:
                        x2, y2 = event.pos
                        screen.blit(another_layer, (0, 0))
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2
                        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                        pygame.draw.polygon(screen, color, points, brush_size)


                    elif tool == 9:
                        x2, y2 = event.pos
                        screen.blit(another_layer, (0, 0))
                        pygame.draw.line(screen, color, (x1, y1), (x2, y2), brush_size)


    if text_active:
        screen.blit(another_layer, (0, 0))
        text_surface = font.render(text_value, True, color)
        screen.blit(text_surface, text_pos)
    pygame.display.flip()


  clock.tick(60)

pygame.quit()
  