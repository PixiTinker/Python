import pygame
import math
import random
import sys


def heart_position(rad):
    
    #The heart parametric equation a(x,y) don't forget this 
    
    
    
    return (math.sin(rad) ** 3,
            -(15 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)))

def scale_and_translate(pos, sx, sy, dx, dy):
    return (dx + pos[0] * sx, dy + pos[1] * sy)

def hsl_to_rgb(h, s, l):
   
    s /= 100.0
    l /= 100.0
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs(((h / 60.0) % 2) - 1))
    m = l - c/2.0
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return (int((r + m)*255), int((g + m)*255), int((b + m)*255))


pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smoke Heart")
clock = pygame.time.Clock()

# Trails be careful with this one
fade_surface = pygame.Surface((width, height))
fade_surface.set_alpha(25)  # trail effect 3rd
fade_surface.fill((0, 0, 0))


font = pygame.font.SysFont("Tangerine", 64)  

# Points 

trace_count = 60
size1, size2 = 210, 13
size11, size12 = 150, 9
dr = 0.1

points_origin = []
# 1
i = 0.0
while i < math.tau:
    points_origin.append(scale_and_translate(heart_position(i), size1, size2, 0, 0))
    i += dr
# 2
i = 0.0
while i < math.tau:
    points_origin.append(scale_and_translate(heart_position(i), size11, size12, 0, 0))
    i += dr
# 3
i = 0.0
while i < math.tau:
    points_origin.append(scale_and_translate(heart_position(i), 90, 5, 0, 0))
    i += dr

heart_points_count = len(points_origin)
target_points = [(0, 0)] * heart_points_count

def pulse(kx, ky):
    global target_points
    target_points = [ (kx * pt[0] + width/2, ky * pt[1] + height/2) for pt in points_origin ]

# 1/1
particles = []
for i in range(heart_points_count):
    x = random.random() * width
    y = random.random() * height
    sat = int(40 * random.random() + 60)  
    lig = int(60 * random.random() + 20)    
    color = hsl_to_rgb(0, sat, lig)
    particle = {
        "vx": 0.0,
        "vy": 0.0,
        "R": 2,
        "speed": random.random() + 5,
        "q": random.randrange(heart_points_count),
        "D": 1 if i % 2 == 0 else -1,
        "force": 0.2 * random.random() + 0.7,
        "color": color,
        "trace": [{"x": x, "y": y} for _ in range(trace_count)]
    }
    particles.append(particle)

config = {"traceK": 0.4, "timeDelta": 0.01}
time_val = 0.0


running = True
while running:
    clock.tick(60) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  
    screen.blit(fade_surface, (0, 0))
    

    n = -math.cos(time_val)
    k_val = (1 + n) * 0.5
    pulse(k_val, k_val)
    if math.sin(time_val) < 0:
        delta = 9
    elif n > 0.8:
        delta = 0.2
    else:
        delta = 1
    time_val += delta * config["timeDelta"]

    for particle in particles:
        # Target point 
        q_index = particle["q"]
        qx, qy = target_points[q_index]
        
        dx = particle["trace"][0]["x"] - qx
        dy = particle["trace"][0]["y"] - qy
        length = math.sqrt(dx * dx + dy * dy) or 0.001  

        if length < 10:
            if random.random() > 0.95:
                particle["q"] = random.randrange(heart_points_count)
            else:
                if random.random() > 0.99:
                    particle["D"] *= -1
                particle["q"] = (particle["q"] + particle["D"]) % heart_points_count

        # Acceleration starts from
        particle["vx"] += (-dx / length) * particle["speed"]
        particle["vy"] += (-dy / length) * particle["speed"]

        
        particle["trace"][0]["x"] += particle["vx"]
        particle["trace"][0]["y"] += particle["vy"]

        
        particle["vx"] *= particle["force"]
        particle["vy"] *= particle["force"]

        
        for k in range(len(particle["trace"]) - 1):
            T = particle["trace"][k]
            N = particle["trace"][k+1]
            N["x"] -= config["traceK"] * (N["x"] - T["x"])
            N["y"] -= config["traceK"] * (N["y"] - T["y"])

        # 1x1 rectangle
        for pt in particle["trace"]:
            
            pygame.draw.rect(screen, particle["color"], (int(pt["x"]), int(pt["y"]), 1, 1))

    text_surface = font.render("I   Miss   You", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width//2, int(height * 0.9)))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
