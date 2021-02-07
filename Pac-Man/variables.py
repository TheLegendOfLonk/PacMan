class Variables():
    def __init__(self):
        self.lives = 2
        self.score = 0
    def get_lives(self):
        return self.lives
    def set_lives(self, lives):
        self.lives = lives
