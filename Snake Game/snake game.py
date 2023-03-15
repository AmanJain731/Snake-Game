import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Colors
white = (255, 255, 255)
blue = (155, 240, 240)
red = (255, 0, 0)
black = (0, 0, 0)
green = (74, 168, 50)

# Creating Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snake")
pygame.display.update()
font = pygame.font.SysFont(None, 55)

bgimg = pygame.image.load("snake game.jfif")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


clock = pygame.time.Clock()


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(green)
        text_screen("Welcome to Snakes", red, 250, 250)
        text_screen("Press Enter to Play", red, 250, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load("background.mp3")
                    pygame.mixer.music.play(loops=100)
                    game_loop()

        pygame.display.update()
        clock.tick(120)


# Game loop
def game_loop():
    # Game specific Variables
    exit_game = False
    game_over = False
    snake_x = 100
    snake_y = 200
    velocity_x = 0
    velocity_y = 0
    snake_size = 10
    fps = 120
    init_velocity = 2
    food_x = random.randint(0, screen_width)
    food_y = random.randint(0, screen_height)
    score = 0
    snake_list = []
    snake_length = 1
    
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.fill(blue)
            text_screen("Game over! Press Enter to continue...", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load("background.mp3")
                        pygame.mixer.music.play(loops=100)
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 10
                food_x = random.randint(0, screen_width - 100)
                food_y = random.randint(0, screen_height - 100)
                snake_length += 5
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(blue)
            gameWindow.blit(bgimg, (0, 0))
            # showing score
            text_screen("Score : " + str(score) + "  Highscore : " + str(highscore), red, 5, 5)
            head = [snake_x, snake_y]
            snake_list.append(head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                pygame.mixer.music.load("Wood Rattle.mp3")
                pygame.mixer.music.play()
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                pygame.mixer.music.load("Wood Rattle.mp3")
                pygame.mixer.music.play()
                game_over = True
            # snake position
            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, black, snake_list, snake_size)
            # food position
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
