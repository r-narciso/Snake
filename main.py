import pygame
import random

FRAME_RATE = 10
FRAME_WIDTH = 500
FRAME_HEIGHT = 500
WALL_WIDTH = 5
SNAKE_SIZE = 20
FOOD_RAD = 4

class Snake(object):
    def __init__(self):
        self.x = (FRAME_WIDTH - SNAKE_SIZE)/2 + WALL_WIDTH
        self.y = (FRAME_HEIGHT - SNAKE_SIZE)/2 + WALL_WIDTH
        self.length = 1
        self.x_vel = SNAKE_SIZE
        self.y_vel = 0

        self.body = [self.head()]

    def head(self):
        return pygame.Rect(self.x, self.y, SNAKE_SIZE, SNAKE_SIZE)

    def move_left(self):
        self.x_vel = - SNAKE_SIZE
        self.y_vel = 0

    def move_right(self):
        self.x_vel = SNAKE_SIZE
        self.y_vel = 0

    def move_up(self):
        self.x_vel = 0
        self.y_vel = -SNAKE_SIZE

    def move_down(self):
        self.x_vel = 0
        self.y_vel = SNAKE_SIZE

    def increase_size(self):
        self.body.insert(0, pygame.Rect(self.x, self.y, SNAKE_SIZE, SNAKE_SIZE))

    def draw(self, win):
        self.x = (self.x + self.x_vel)
        if self.x < WALL_WIDTH or self.x >= FRAME_WIDTH+WALL_WIDTH:
            return False
        self.y = (self.y + self.y_vel)
        if self.y < WALL_WIDTH or self.y >= FRAME_HEIGHT+WALL_WIDTH:
            return False
        for piece in self.body:
            if piece.colliderect(self.head()):
                return False
        self.body.insert(0, self.head())
        self.body.pop()
        drawn = []
        for piece in self.body:
            pygame.draw.rect(win, (0,255,0), piece)
            drawn.append(piece)

        return True

    def __del__(self):
        pass

class Food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.show = False

    @classmethod
    def random(cls):
        return Food(random.randint(0, FRAME_WIDTH) // SNAKE_SIZE * SNAKE_SIZE + SNAKE_SIZE//2 + WALL_WIDTH,
                    random.randint(0, FRAME_HEIGHT) // SNAKE_SIZE * SNAKE_SIZE + SNAKE_SIZE//2 + WALL_WIDTH)

    def check_eat(self, snake):
        return snake.head().collidepoint(self.x, self.y)

    def draw(self, win):
        pygame.draw.circle(win, (255,0,0), (self.x, self.y), FOOD_RAD)

def display_text(win, text, x, y, size, color):
    font = pygame.font.SysFont('comicsansms', size)
    rendering = font.render(text, True, color)
    win.blit(rendering, (x, y))

def text_size(text, size):
    font = pygame.font.SysFont('comicsansms', size)
    return font.size(text)

def main():
    # start the window
    win = pygame.display.set_mode((FRAME_WIDTH+WALL_WIDTH*2, FRAME_HEIGHT+WALL_WIDTH*2))

    #initial setup
    pygame.display.set_caption('Snakey Snake')
    clock = pygame.time.Clock()

    init = pygame.font.init()

    # init the snake
    snake = Snake()

    # init the current food item
    food = Food.random()

    # do the intro sequence
    pygame.draw.lines(win, (255,255,255), True, [(0,0),
                                                 (0,FRAME_HEIGHT+WALL_WIDTH*2),
                                                 (FRAME_WIDTH+WALL_WIDTH*2, FRAME_HEIGHT+WALL_WIDTH*2),
                                                 (FRAME_WIDTH+WALL_WIDTH*2, 0)], 5)
    pygame.draw.rect(win, (255,255,255), (FRAME_WIDTH//2 - 100 + WALL_WIDTH, FRAME_HEIGHT//2 - 50 + WALL_WIDTH,
                                          200, 100))
    text_width, text_height = text_size('START', 40)
    display_text(win, 'START', (FRAME_WIDTH-text_width)//2 + WALL_WIDTH, (FRAME_HEIGHT-text_height)//2 + WALL_WIDTH, 40, (0,0,0))
    pygame.display.update()
    wait = True
    while wait:
        clock.tick(FRAME_RATE)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    wait = False

    wait = True
    while wait:
        clock.tick(FRAME_RATE)
        if event.type == pygame.QUIT:
            wait = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.move_left()
                elif event.key == pygame.K_RIGHT:
                    snake.move_right()
                elif event.key == pygame.K_UP:
                    snake.move_up()
                elif event.key == pygame.K_DOWN:
                    snake.move_down()
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    wait = False

        if food.check_eat(snake):
            snake.increase_size()
            del food
            food = Food.random()

        win.fill((0,0,0))
        pygame.draw.lines(win, (255,255,255), True, [(0,0),
                                                 (0,FRAME_HEIGHT+WALL_WIDTH*2),
                                                 (FRAME_WIDTH+WALL_WIDTH*2, FRAME_HEIGHT+WALL_WIDTH*2),
                                                 (FRAME_WIDTH+WALL_WIDTH*2, 0)], 5)
        food.draw(win)
        wait = snake.draw(win)
        pygame.display.update()

    # do clean up stuff here
    pygame.draw.rect(win, (255,0,0), (FRAME_WIDTH//2 - 100 + WALL_WIDTH, FRAME_HEIGHT//2 - 50 + WALL_WIDTH,
                                          200, 100))
    text_width, text_height = text_size('DED', 40)
    display_text(win, 'DED', (FRAME_WIDTH-text_width)//2 + WALL_WIDTH, (FRAME_HEIGHT-text_height)//2 + WALL_WIDTH, 40, (0,0,0))
    pygame.display.update()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                wait = False
    return

main()