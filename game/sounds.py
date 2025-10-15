import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load sounds
PADDLE_HIT_SOUND = pygame.mixer.Sound("game/assets/paddle_hit.wav")
WALL_BOUNCE_SOUND = pygame.mixer.Sound("game/assets/wall_bounce.wav")
SCORE_SOUND = pygame.mixer.Sound("game/assets/score.wav")
