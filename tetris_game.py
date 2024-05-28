import random
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.label import Label

# Fullscreen mode
Window.fullscreen = 'auto'
ROWS = 23
COLS = 19
FPS = 24

# COLORS
BLACK = (0.082, 0.094, 0.114)
BLUE = (0.122, 0.098, 0.298)
RED = (0.988, 0.357, 0.478)
WHITE = (1, 1, 1)

# IMAGES
img_paths = [
    'sourses/figures/1.png',
    'sourses/figures/2.png',
    'sourses/figures/3.png',
    'sourses/figures/4.png',
    'sourses/figures/5.png',
    'sourses/figures/6.png'
]
Assets = {}

# FONT PATHS (Change the paths to your font files)
font_path = 'sourses/Alternity-8w7J.ttf'

for i, path in enumerate(img_paths):
    if os.path.exists(path):
        Assets[i + 1] = CoreImage(path).texture
    else:
        print(f"Image path not found: {path}")

class Tetramino:
    FIGURES = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }
    TYPES = list(FIGURES.keys())

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]
        self.color = random.randint(1, 6)
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

class TetrisGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = ROWS
        self.cols = COLS
        self.score = 0
        self.level = 1
        self.board = [[0 for j in range(COLS)] for i in range(ROWS)]
        self.next = None
        self.gameover = False
        self.new_figure()
        self.counter = 0
        self.move_down = False
        self.can_move = True
        Clock.schedule_interval(self.update, 1.0 / FPS)
        self.bind(size=self.update_canvas, pos=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Draw the background
            Color(*BLACK)
            Rectangle(pos=self.pos, size=self.size)

            # Draw the grid (Game field)
            Color(*WHITE)
            for i in range(self.rows):
                Line(points=[580, i*40+40, 1340, i*40+40], width=1/3)
            for j in range(self.cols + 1):
                Line(points=[j*40+580, 40, j*40+580, 920], width=1/3)

            # Draw the tetris board (Game field)
            for x in range(self.rows):
                for y in range(self.cols):
                    if self.board[x][y] > 0:
                        val = self.board[x][y]
                        img = Assets.get(val)
                        if img:
                            Rectangle(texture=img, pos=(y*40+580, 920 - x*40), size=(40, 40))
                        Line(rectangle=(y*40+580, 920 - x*40, 40, 40), width=0.3, color=Color(*WHITE))

            # Draw the current tetramino (Game field)
            if self.figure:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.figure.image():
                            img = Assets.get(self.figure.color)
                            if img:
                                x = 40 * (self.figure.x + j)
                                y = 40 * (self.figure.y + i)
                                Rectangle(texture=img, pos=(580 + x, 920 - y), size=(40, 40))
                                Line(rectangle=(580 + x, 920 - y, 40, 40), width=1, color=Color(*WHITE))

            # Draw the HUD
            Color(*BLUE)
            Rectangle(pos=(1, 920), size=(1920, 160))

            # Draw the score and level (HUD)
            self.add_widget(Label(text=str(self.score), font_size=100, color=WHITE, pos=(100, 950)))
            self.add_widget(Label(text=f'Level : {self.level}', font_size=80, color=WHITE, pos=(1660, 950)))

            # Draw the next figure (HUD)
            if self.next:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.next.image():
                            img = Assets.get(self.next.color)
                            if img:
                                x = 40 * (j + 1)
                                y = 40 * (3 - i)
                                Rectangle(texture=img, pos=(950 - 90 + x, 920 + y), size=(40, 40))
                                Line(rectangle=(950 - 90 + x, 920 + y, 40, 40), width=1, color=Color(*WHITE))

            # Draw game over screen (HUD)
            if self.gameover:
                Color(*BLACK)
                rect = (775, 425, 370, 230)
                Rectangle(pos=(rect[0], rect[1]), size=(rect[2], rect[3]))
                Line(rectangle=rect, width=2, color=Color(*RED))
                self.add_widget(Label(text='Game Over', font_size=50, color=WHITE, pos=(rect[0] + rect[2] // 2.6, rect[1] + rect[3] // 2)))
                self.add_widget(Label(text='Press r to restart', font_size=40, color=RED, pos=(rect[0] + rect[2] // 2.6, rect[1] + rect[3] // 9)))
                self.add_widget(Label(text='Press q to quit', font_size=40, color=RED, pos=(rect[0] + rect[2] // 2.6, rect[1] + rect[3] // 3.5)))

    def new_figure(self):
        if not self.next:
            self.next = Tetramino(5, 0)
        self.figure = self.next
        self.next = Tetramino(5, 0)
        if self.intersects():
            self.figure.y -= 3
            if self.intersects():
                self.gameover = True

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (i + self.figure.y >= self.rows or j + self.figure.x >= self.cols or j + self.figure.x < 0 or self.board[i + self.figure.y][j + self.figure.x] > 0):
                        intersection = True
        return intersection

    def remove_line(self):
        rerun = False
        for y in range(self.rows - 1, -1, -1):
            is_full = True
            for x in range(self.cols):
                if self.board[y][x] == 0:
                    is_full = False
            if is_full:
                del self.board[y]
                self.board.insert(0, [0 for _ in range(self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
                rerun = True

        if rerun:
            self.remove_line()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.remove_line()
        self.new_figure()
        if self.intersects():
            self.gameover = True

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        self.figure.x += dx
        if self.intersects():
            self.figure.x -= dx

    def rotate(self):
        rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = rotation

    def update(self, dt):
        self.counter += 1
        if self.counter >= 10000:
            self.counter = 0

        if self.can_move:
            if self.counter % (FPS // (self.level * 2)) == 0 or self.move_down:
                if not self.gameover:
                    self.go_down()
        self.update_canvas()

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if self.can_move and not self.gameover:
            if keycode[1] == 'left':
                self.go_side(-1)
            elif keycode[1] == 'right':
                self.go_side(1)
            elif keycode[1] == 'up':
                self.rotate()
            elif keycode[1] == 'down':
                self.move_down = True
            elif keycode[1] == 'spacebar':
                self.go_space()
        if keycode[1] == 'r':
            self.__init__()
        if keycode[1] == 'p':
            self.can_move = not self.can_move
        if keycode[1] == 'q' or keycode[1] == 'escape':
            App.get_running_app().stop()

    def on_key_up(self, keyboard, keycode):
        if keycode[1] == 'down':
            self.move_down = False

class TetrisApp(App):
    def build(self):
        game = TetrisGame()
        keyboard = Window.request_keyboard(game.on_key_up, game)
        keyboard.bind(on_key_down=game.on_key_down, on_key_up=game.on_key_up)
        return game

if __name__ == '__main__':
    TetrisApp().run()