import pygame
import random
from pygame.locals import *


class App:
    screen_width = 1000
    screen_height = 800
    snakePos = [[25, 20], [26, 20], [27, 20]]
    gameSize = [50, 40]
    dotPos = [random.randint(0,gameSize[0]),random.randint(0,gameSize[1])]
    score = 0
    blockSize = [screen_width / gameSize[0], screen_height/gameSize[1]]  # 2,2
    secTimer = USEREVENT
    speed = 500
    direction = 2
    game_over = False

    def draw_score(self):
        text = "Score: " + str(self.score)
        if self.game_over:
            text = text + "   GAME OVER!"
        myfont = pygame.font.SysFont('Arial', 30)
        text_surface = myfont.render(text, False, (0, 200, 0))
        self._display_surf.blit(text_surface, (0, 0))

    def eat_dot(self):
        self.dotPos = [random.randint(0, self.gameSize[0]-1), random.randint(0, self.gameSize[1]-1)]
        self.score += 1
        self.add_tail()

    def draw_dot(self):
        drawRect = pygame.Rect(self.dotPos[0]*self.blockSize[0],self.dotPos[1]*self.blockSize[0], self.blockSize[0], self.blockSize[1])
        pygame.draw.rect(self._display_surf,Color(50,50,200),drawRect)

    def add_tail(self):
        new_head = [self.snakePos[0][0], self.snakePos[0][1]]
        if self.direction == 0:
            new_head[1] -= 1
        if self.direction == 1:
            new_head[0] += 1
        if self.direction == 2:
            new_head[1] += 1
        if self.direction == 3:
            new_head[0] -= 1
        self.snakePos.insert(0, new_head)

    def update_snake(self):

        last_pos = False
        for position in self.snakePos:
            temp_pos = last_pos
            last_pos = [position[0], position[1]]
            if temp_pos == False:
                if self.direction == 0:
                    position[1] -= 1
                if self.direction == 1:
                    position[0] += 1
                if self.direction == 2:
                    position[1] += 1
                if self.direction == 3:
                    position[0] -= 1
            else:
                position[0] = temp_pos[0]
                position[1] = temp_pos[1]


    def draw_snake(self):
        for position in self.snakePos:
            drawx = position[0] * self.blockSize[0]
            drawy = position[1] * self.blockSize[1]
            drawrec = pygame.Rect((drawx, drawy), (self.blockSize[0],
                                  self.blockSize[1]))
            pygame.draw.rect(self._display_surf, Color(255, 0, 0), drawrec)

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.HWSURFACE)
        pygame.time.set_timer(self.secTimer, self.speed)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        if self.game_over == False:
            if event.type == self.secTimer:
                self.update_snake()
                if self.speed > 100:
                    self.speed -= 10
                pygame.time.set_timer(self.secTimer, self.speed)


    def on_loop(self):
        cur_pos = self.snakePos[0]
        last_pos = self.snakePos[1]
        if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP] and last_pos[1] != cur_pos[1]-1:
            self.direction = 0
        if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT] and last_pos[0] != cur_pos[0]+1:
            self.direction = 1
        if pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_DOWN] and last_pos[1] != cur_pos[1]+1:
            self.direction = 2
        if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT] and last_pos[0] != cur_pos[0]-1:
            self.direction = 3
        if self.snakePos[0] == self.dotPos:
            self.eat_dot()
        snake_head = self.snakePos[0]

        if snake_head in self.snakePos[1:]:
            self.game_over = True
        if snake_head[0] < 0 or snake_head[0] > self.gameSize[0] or snake_head[1] < 0 or snake_head[1] > self.gameSize[1]-1:
            self.game_over = True

    def on_render(self):
        self._display_surf.fill(Color(0, 0, 0))

        self.draw_snake()
        self.draw_dot()
        self.draw_score()

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
