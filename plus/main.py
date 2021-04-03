import pygame
from pygame import midi
from time import sleep
from sys import exit
from threading import Thread
from numpy.random import randint


class Piano:
    WHITE_KEY_WIDTH = 60
    WHITE_KEY_HEIGHT = 200
    BLACK_KEY_WIDTH = 40
    BLACK_KEY_HEIGHT = 140
    black_location = [40, 100, 220, 280, 340, 460, 520, 640, 700, 760, 880, 940, 1060, 1120, 1180]
    white_key_list = [36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71]
    black_key_list = [37, 39, 42, 44, 46, 49, 51, 54, 56, 58, 61, 63, 66, 68, 70]

    WHITE_DOWN = 0
    BLACK_DOWN = 1
    def __init__(self,screen):
        self.screen  = screen
        self.player = midi.Output(0, latency=0)
        self.player.set_instrument(0)
        self.black_range = [(i, i + Piano.BLACK_KEY_WIDTH) for i in Piano.black_location]
        self.image_size = (70, 70)
        self.image1 = pygame.transform.scale(pygame.image.load('image1.png'), self.image_size)
        self.image2 = pygame.transform.scale(pygame.image.load('image2.png'), self.image_size)

    def _play(self,key):
        self.player.note_on(key, velocity=127, channel=0)
        sleep(1)
        self.player.note_off(key)

    def play_note(self,key):
        Thread(target=self._play, args=(key,)).start()

    def draw_black(self):
        for i in self.black_location:
            pygame.draw.rect(self.screen, BLACK,((i, height - Piano.WHITE_KEY_HEIGHT), (Piano.BLACK_KEY_WIDTH, Piano.BLACK_KEY_HEIGHT)), 0)
    def draw_white(self):
        self.screen.fill(WHITE)
        for i in range(21):
            pygame.draw.rect(self.screen,BLACK,((i*Piano.WHITE_KEY_WIDTH,height-Piano.WHITE_KEY_HEIGHT),(Piano.WHITE_KEY_WIDTH,Piano.WHITE_KEY_HEIGHT)),1)

    def key_down(self,index,location,category):
        x,y = location
        if category == Piano.WHITE_DOWN:
            pygame.draw.rect(self.screen, SKYBLUE, ((index * Piano.WHITE_KEY_WIDTH, height - Piano.WHITE_KEY_HEIGHT),(Piano.WHITE_KEY_WIDTH, Piano.WHITE_KEY_HEIGHT)))
            self.draw_black()#由于绘图的顺序问题 这里要再画一遍黑的覆盖
            self.play_note(Piano.white_key_list[index])
            self.screen.blit(pygame.transform.rotate(self.image1, randint(-30, 31, 1)),(x - self.image_size[0] / 2, int(randint(20, height-Piano.WHITE_KEY_HEIGHT-self.image_size[0], 1))))

        else:
            pygame.draw.rect(self.screen, BLUE,((self.black_location[index], height - Piano.WHITE_KEY_HEIGHT), (Piano.BLACK_KEY_WIDTH, Piano.BLACK_KEY_HEIGHT)), 0)
            pygame.draw.rect(self.screen, BLACK, ((self.black_location[index], height - Piano.WHITE_KEY_HEIGHT),(Piano.BLACK_KEY_WIDTH, Piano.BLACK_KEY_HEIGHT)), 1)
            #再画一下轮廓
            self.play_note(Piano.black_key_list[index])
            self.screen.blit(pygame.transform.rotate(self.image2, randint(-30, 31, 1)), (x - self.image_size[0] / 2, int(randint(20, height-Piano.WHITE_KEY_HEIGHT-self.image_size[0], 1))))
            #点击两端的琴键时图片可能会出框

pygame.init()
midi.init()
pygame.mixer.music.fadeout(1)

WHITE = (255,255,255)
BLACK = (0,0,0)
SKYBLUE = (135,206,235)
BLUE = (0,0,255)
YELLOW = (255,255,0)
bgSize = width, height = 1260, 480
screen = pygame.display.set_mode(bgSize)
piano = Piano(screen)
piano.draw_white()
piano.draw_black()
pygame.display.set_caption('钢琴')


font = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 50)
message = font.render('电子琴',True, (255,0,0))
#screen.blit(message, (500, 100))
pygame.display.flip()

fps = 30
fclock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        x = -1
        y = -1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
                pygame.quit()
        elif event.type == pygame.QUIT:
            exit()
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
        elif event.type == pygame.FINGERDOWN:
            x, y = int(event.x * width), int(event.y * height)

        if x >= 0 and y >= 0:
            piano.draw_white()
            piano.draw_black()
            #screen.blit(message, (500, 100))

            if y > height - Piano.WHITE_KEY_HEIGHT:#键盘区
                if y < height-Piano.WHITE_KEY_HEIGHT+Piano.BLACK_KEY_HEIGHT:#可能黑键
                    flag = False
                    for i in range(len(piano.black_location)):
                        if piano.black_range[i][0] < x < piano.black_range[i][1]:#黑键
                            flag = True
                            piano.key_down(i,(x,y),Piano.BLACK_DOWN)
                            break
                    if not flag:#白键
                        piano.key_down(x//Piano.WHITE_KEY_WIDTH, (x, y), Piano.WHITE_DOWN)
                else:#白键
                    piano.key_down(x//Piano.WHITE_KEY_WIDTH, (x, y), Piano.WHITE_DOWN)
            pygame.display.flip()
            fclock.tick(fps)


'''
while True:
    play(int(input()))
'''
