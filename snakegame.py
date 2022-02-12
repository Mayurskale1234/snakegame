import pygame
from pygame.locals import *
import time
import random


SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = 160
        self.y = 160

    def Draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def Move(self):
        self.x = random.randrange(0,25,1) * SIZE
        self.y = random.randrange(0,15,1) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def Draw(self):
        self.parent_screen.fill((10, 66, 22))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "up":
            self.y[0] -=  SIZE

        if self.direction == "down":
            self.y[0] += SIZE

        if self.direction == "left":
            self.x[0] -= SIZE

        if self.direction == "right":
            self.x[0] += SIZE

        self.Draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 600))
        self.surface.fill((139, 0, 0))
        self.Snake = Snake(self.surface, 1)
        self.Snake.Draw()
        self.Apple = Apple(self.surface)
        self.Apple.Draw()


    def is_collision(self, x1,y1,x2,y2):
        if x2 >= x1 and x2 < x1 + SIZE:
            if y2 >= y1 and y2 < y1 + SIZE:
                return True

        return False

    #def render_bg(self):
        #bg = pygame.image.load("img3.jpg")
        #self.surface.blit(bg,(0,0))


    def play(self):
        #self.render_bg()
        self.Snake.walk()
        self.Apple.Draw()
        self.display_score()
        pygame.display.flip()

        # collision with apple
        if self.is_collision(self.Snake.x[0], self.Snake.y[0], self.Apple.x, self.Apple.y):
            sound = pygame.mixer.Sound("snakeaudio2.mp3")
            pygame.mixer.Sound.play(sound)
            self.Snake.increase_length()
            self.Apple.Move()

        # collision with itself
        for i in range(3, self.Snake.length):
            if self.is_collision(self.Snake.x[0], self.Snake.y[0], self.Snake.x[i], self.Snake.y[i]):
                sound = pygame.mixer.Sound("gameover.wav")
                pygame.mixer.Sound.play(sound)
                raise "Game over"



    def display_score(self):
        #self.render_bg()
        pygame.font.init()
        font = pygame.font.SysFont('arail', 30)
        score = font.render(f"score: {self.Snake.length}" ,True, (255,255,255))
        self.surface.blit(score,(800,20))

    def show_game_over(self):
        #self.render_bg()
        pygame.font.init()
        font = pygame.font.SysFont('arail', 30)
        line1 = font.render(f"Game is over..... Your final score is: {self.Snake.length}", True, (255, 255, 255))
        self.surface.blit(line1,(300, 300))
        line2 = font.render("To play again press ENTER, To quit press ESC.", True, (255, 255, 255))
        self.surface.blit(line2, (300, 350))
        pygame.display.flip()

    def reset(self):
        self.Snake = Snake(self.surface, 1)
        self.Apple = Apple(self.surface)


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if event.key == K_UP:
                        self.Snake.move_up()

                    if event.key == K_DOWN:
                        self.Snake.move_down()

                    if event.key == K_LEFT:
                        self.Snake.move_left()

                    if event.key == K_RIGHT:
                        self.Snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.run()