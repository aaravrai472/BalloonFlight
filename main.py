import pygame

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Flight")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Player
player = pygame.Rect(100, 250, 40, 40)
velocity = 0
gravity = 0.045
boost = -1

# Game state
score = 0
game_active = False


def draw_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))


def reset_game():
    global player, velocity, score
    player.y = 250
    velocity = 0
    score = 0


running = True
while running:
    screen.fill((30, 30, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_active:
                game_active = True
                reset_game()
            elif event.key == pygame.K_SPACE:
                velocity = boost

    if game_active:
        # Player physics
        velocity += gravity
        player.y += velocity

        if player.top < 0 or player.bottom > HEIGHT:
            game_active = False

        # Score
        score += 1

        # Draw player
        pygame.draw.rect(screen, (255, 200, 0), player)

        draw_text(f"Score: {score}", 10, 10)

    else:
        draw_text("Press SPACE to Start", 250, 250)
        draw_text(f"Score: {score}", 330, 300)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
