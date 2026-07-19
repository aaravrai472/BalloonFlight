import random
import pygame

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
SPEED = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Flight")

bg = pygame.transform.scale(pygame.image.load("assets/bg.png"), (800, 600))


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/balloon.png").convert_alpha(),
            (331 // 2, 339 // 2 + 35),
        )
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.velocity = 0
        self.gravity = 0.04
        self.lift = 0.12
        self.sink = 0.1
        self.max_speed = 4

    def reset_game(self):
        global score
        self.rect.y = 250
        self.velocity = 0
        score = 0

    def physics(self, keys):
        global game_active

        self.velocity += self.gravity
        if keys[pygame.K_UP]:
            self.velocity -= self.lift
        if keys[pygame.K_DOWN]:
            self.velocity += self.sink

        velocity = max(-self.max_speed, min(self.max_speed, self.velocity))

        self.rect.y += velocity

        if self.rect.bottom > HEIGHT:
            game_active = False


class House(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        self.image = pygame.image.load("assets/house.png")
        self.image = pygame.transform.scale(self.image, (294 // 2 + 50, 238 // 2 + 50))
        self.x = x
        self.y = HEIGHT // 2 + 65
        self.rect = self.image.get_rect()

    def update(self):
        self.x -= SPEED
        self.rect.x = self.x

        if self.x < -500:
            self.x = WIDTH


class Tree(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        self.image = pygame.image.load("assets/tree.png")
        self.image = pygame.transform.scale(self.image, (294 // 2 + 50, 238 // 2 + 50))
        self.x = x
        self.y = HEIGHT // 2 + 65
        self.rect = self.image.get_rect()

    def update(self):
        self.x -= SPEED
        self.rect.x = self.x

        if self.x < -200:
            self.x = WIDTH


class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load("assets/ground.png"), (WIDTH, HEIGHT // 7)
        )
        self.x = x
        self.y = 515
        self.rect = self.image.get_rect()

    def update(self):
        self.x -= SPEED
        self.rect.x = self.x

        if self.x < -80:
            self.x = WIDTH


class Bird(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        self.image = pygame.image.load("assets/bird.png")
        self.image = pygame.transform.scale(self.image, (133 // 2, 73 // 2))
        self.x = x
        self.y = random.randint(0, 400)
        self.rect = self.image.get_rect()

    def update(self):
        self.x -= SPEED + 3
        self.rect.x = self.x

        if self.x < -500:
            self.x = WIDTH
            self.y = random.randint(0, 400)


player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

houses = [House(x) for x in range(WIDTH, WIDTH + 1000, 3799)]
trees = [Tree(x) for x in range(WIDTH, WIDTH + 1000, 564)]
grounds = [Ground(x) for x in range(WIDTH, WIDTH + 1000, 50)]
birds = [Bird(x) for x in range(WIDTH, WIDTH + 1000, 3799)]

# Game state
score = 0
game_active = False


def draw_text(text, x, y):
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, (x, y))


running = True
while running:
    screen.blit(bg, (0, 0))
    for ground in grounds:
        ground.update()
        screen.blit(ground.image, (ground.x, ground.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_active:
                game_active = True
                player.reset_game()

    all_sprites.update()

    for house in houses:
        house.update()
        screen.blit(house.image, (house.x, house.y))
    for tree in trees:
        tree.update()
        screen.blit(tree.image, (tree.x, tree.y))
    for bird in birds:
        bird.update()
        screen.blit(bird.image, (bird.x, bird.y))

    if game_active:
        keys = pygame.key.get_pressed()
        player.physics(keys)

        # Score
        score += 1

        # Draw player
        screen.blit(player.image, (player.rect.x, player.rect.y))

        draw_text(f"Score: {score}", 10, 10)

        all_sprites.draw(screen)

    else:
        draw_text("Use UP/DOWN arrows to fly", 200, 230)
        draw_text("Press any key to Start", 210, 270)
        draw_text(f"Score: {score}", 330, 310)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
