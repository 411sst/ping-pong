import pygame
from .paddle import Paddle
from .ball import Ball
from .sounds import PADDLE_HIT_SOUND

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.winning_score = 5  # default to "Best of 5"

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()

        # ✅ Collision check right after moving
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width  # prevent overlap
            self.ball.velocity_x *= -1
            PADDLE_HIT_SOUND.play()

        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width  # prevent overlap
            self.ball.velocity_x *= -1
            PADDLE_HIT_SOUND.play()

        # Score conditions
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)


    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score == self.winning_score or self.ai_score == self.winning_score:
            winner = "Player Wins!" if self.player_score == self.winning_score else "AI Wins!"
            winner_text = self.font.render(winner, True, (255, 255, 255))
            screen.blit(winner_text, (self.width // 2 - winner_text.get_width() // 2, self.height // 3))

            options_text = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, line in enumerate(options_text):
                text_surface = self.font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, self.height // 2 + i * 40))

            pygame.display.flip()

            # Wait for user choice
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return True
                        elif event.key in (pygame.K_3, pygame.K_5, pygame.K_7):
                            self.winning_score = int(event.unicode)
                            self.player_score = 0
                            self.ai_score = 0
                            self.ball.reset()
                            waiting = False
                            return False
            return True
        return False
