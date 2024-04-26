# Importing libraries
import pygame 
import sys
import random

# Initialize pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Computer Science Assessment [Python Dinosaur Game]") # Game window name

# Load dinosaur images
dino_img1 = pygame.image.load("images/dino1.png").convert_alpha()
dino_img2 = pygame.image.load("images/dino2.png").convert_alpha()
dino_images = [dino_img1, dino_img2] # I'm having 2 dinosaur images because switching between 2 gives a running effect


# Load cloud image
cloud_img = pygame.image.load("images/cloud.png").convert_alpha()

# Load cactus images
cactus_imgs = [pygame.image.load(f"images/cactus{i}.png").convert_alpha() for i in range(1, 6)]
# I'm spawning random cactus in the format from cactus1 to cactus6

# Player settings
player_rect = dino_img1.get_rect(topleft=(50, SCREEN_HEIGHT - 110))
player_jump = False
player_velocity_y = 0
JUMP_HEIGHT = -20 # You can increase the jumping height by decreasing this value


# Cloud settings
clouds = [{"rect": cloud_img.get_rect(topleft=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT // 2))),
           "speed": random.randint(1, 5)} for _ in range(5)]

# Score
score = 0
font = pygame.font.Font(None, 36)

# Animation variables
frame = 0
animation_speed = 10  # Decreasing this value will increase the running animation effect not the actual speed

# Function to generate random cactus
def generate_object():
    cactus_img = random.choice(cactus_imgs)
    cactus_rect = cactus_img.get_rect(midbottom=(SCREEN_WIDTH, SCREEN_HEIGHT - 10))
    return cactus_img, cactus_rect

# Generate initial cactus
cactus_img, cactus_rect = generate_object()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player_jump:
                player_jump = True
                player_velocity_y = JUMP_HEIGHT

    # Update player position
    if player_jump:
        player_rect.y += player_velocity_y
        player_velocity_y += 1
        if player_rect.y >= SCREEN_HEIGHT - 110:
            player_jump = False
            player_rect.y = SCREEN_HEIGHT - 110

    # Update cloud position
    for cloud in clouds:
        cloud["rect"].x -= cloud["speed"]
        if cloud["rect"].right < 0:
            cloud["rect"].left = SCREEN_WIDTH
            cloud["rect"].top = random.randint(0, SCREEN_HEIGHT // 2)

    # Update cactus position
    cactus_velocity_x = -7  # Increased running speed
    cactus_rect.x += cactus_velocity_x
    if cactus_rect.right < 0:
        cactus_img, cactus_rect = generate_object()
        cactus_rect.x = SCREEN_WIDTH
        score += 1

    # Check collision
    if player_rect.colliderect(cactus_rect):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Animation
    if frame % animation_speed == 0:
        frame = 0
    player_image = dino_images[frame // (animation_speed // len(dino_images))]
    frame += 1

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw clouds
    for cloud in clouds:
        screen.blit(cloud_img, cloud["rect"])

    # Draw player
    screen.blit(player_image, player_rect)

    # Draw cactus
    screen.blit(cactus_img, cactus_rect)

    # Draw score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)
