import pygame as pg 

class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.level = 0
        self.high_score = 0
        
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (200, 200, 200)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None 
        self.score_rect = None
        self.prep_score()

    def increment_score(self): 
        self.score += self.settings.alien_points
        self.prep_score()

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def reset(self):
        f = open("highscores.txt", "r+")
        high_score = int(f.readline())
        f.close()
        if high_score < self.score: 
            f = open("highscores.txt", "w")
            f.write(str(self.score))
            f.close()
        self.score = 0
        self.update()

    def update(self): 
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)