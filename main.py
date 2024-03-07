import pygame
import random

pygame.init()
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('First Pygame')
clock = pygame.time.Clock()
running = True

dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


class Game():
    def __init__(self, puppy_group, food_group):
        self.puppy_group = puppy_group
        self.food_group = food_group
        self.score = 0
        self.lives = 5

        self.small_font = pygame.font.SysFont('impact', 24)
        self.big_font = pygame.font.SysFont('impact', 60)

        self.blue_food = pygame.image.load('images/food2.png')
        self.red_food = pygame.image.load('images/food.png')

        self.food_group.add(Food((random.randint(0, 800)), (random.randint(100, 200)), self.red_food, 1))
        for i in range(7):
            self.food_group.add(Food(i * 100, 200, self.blue_food, 0))

        self.score_sound = pygame.mixer.Sound('sounds/dog.mp3')
        self.die_sound = pygame.mixer.Sound('sounds/aww.mp3')
        self.game_over_sound = pygame.mixer.Sound('sounds/game_over.mp3')


    def update(self):
        self.check_collisions()
        self.draw()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_p]:
            self.pause_game()

    def draw(self):
        pygame.draw.rect(screen, 'blue', (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200), 4)

        title_text = self.big_font.render('Feed Puppy', True, 'blue')
        title_rect = title_text.get_rect()
        title_rect.centerx = WINDOW_WIDTH / 2
        title_rect.top = 5

        win_text = self.big_font.render('You Won!', True, 'red')
        win_rect = win_text.get_rect()
        win_rect.centerx = WINDOW_WIDTH / 2
        win_rect.centery = WINDOW_HEIGHT / 2 - 100

        lose_text = self.big_font.render('You Lost :(', True, 'red')
        lose_rect = lose_text.get_rect()
        lose_rect.centerx = WINDOW_WIDTH / 2
        lose_rect.centery = WINDOW_HEIGHT / 2 - 100

        restart_text = self.big_font.render('Press Enter to play again. :(', True, 'red')
        restart_rect = restart_text.get_rect()
        restart_rect.centerx = WINDOW_WIDTH / 2
        restart_rect.centery = WINDOW_HEIGHT / 2

        score_text = self.small_font.render(f'Score: {self.score}', True, 'blue')
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.small_font.render(f'Lives: {self.lives}', True, 'blue')
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 5, 5)

        screen.blit(title_text, title_rect)
        screen.blit(score_text, score_rect)
        screen.blit(lives_text, lives_rect)

        if self.score == 7:
            screen.blit(win_text, win_rect)
            screen.blit(restart_text, restart_rect)
            self.game_over()

        if self.lives == 0:
            screen.blit(lose_text, lose_rect)
            screen.blit(restart_text, restart_rect)
            self.food_group.remove(food_group)
            self.game_over()

    def game_over(self):
        self.puppy_group.reset()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.score = 0
            self.lives = 5

            self.food_group.add(Food((random.randint(0, 800)), (random.randint(100, 200)), self.red_food, 1))
            for i in range(7):
                self.food_group.add(Food(i * 100, 200, self.blue_food, 0))

    def pause_game(self):
        is_paused = True

        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False

                if event.type == pygame.QUIT:
                    is_paused = False
                    pygame.quit()

    def check_collisions(self):
        caught_food = pygame.sprite.spritecollideany(self.puppy_group, self.food_group)
        if caught_food:
            if caught_food.food_type == 0:
                self.lives -= 1
                self.puppy_group.reset()
                self.die_sound.play()

                if self.lives == 0:
                    self.game_over_sound.play()
            else:
                self.score_sound.play()
                caught_food.remove(self.food_group)
                self.score += 1

                if len(self.food_group) > 0:
                    random.choice(self.food_group.sprites()).kill()
                    if len(self.food_group) >= 1:
                        self.food_group.add(Food((random.randint(0, 800)), (random.randint(100, 200)), self.red_food, 1))

                    else:
                        self.puppy_group.reset()
                        self.game_over_sound.play()




class Puppy(pygame.sprite.Sprite):
    def __init__(self, x, y, bone_group):
        super().__init__()
        self.image = pygame.image.load('images/aspen2.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = 5

        self.bone_group = bone_group

    def update(self):
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x >= 4 :
            self.rect.x -= self.velocity

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x <= WINDOW_WIDTH - 95:
            self.rect.x += self.velocity

        '''
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y >= 104:
            self.rect.y -= self.velocity

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y <= WINDOW_HEIGHT - 95:
            self.rect.y += self.velocity
        '''

    def reset(self):
        self.rect.topleft = (200, 510)

    def fire(self):
        Bone(self.rect.centerx, self.rect.top, self.bone_group)


class Bone(pygame.sprite.Sprite):
    def __init__(self, x, y, bone_group):
        super().__init__()
        self.image = pygame.image.load('images/bone.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 10

        bone_group.add(self)


    def update(self):
        self.rect.y -= self.velocity



class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, image, food_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = random.randint(1, 5)

        self.food_type = food_type

        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def update(self):
        # self.rect.y += self.velocity
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity

        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1 * self.dx

        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
            self.dy = -1 * self.dy


food_group = pygame.sprite.Group()
# for i in range(8):
#     food = Food(i * 100, 200)
#     food_group.add(food)

bone_group = pygame.sprite.Group()

puppy_group = pygame.sprite.Group()
puppy = Puppy(200, 500, bone_group)
puppy_group.add(puppy)

game = Game(puppy, food_group)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                puppy.fire()

    # screen color
    screen.fill('silver')

    food_group.update()
    food_group.draw(screen)
    puppy_group.update()
    puppy_group.draw(screen)

    bone_group.update()
    bone_group.draw(screen)

    game.update()

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
