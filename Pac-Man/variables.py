'''
Contains the Variable class which stored the lives and the current score
'''

class Variables():
    '''
    A class to store the score and lives

    Methods
    -------
    get_lives()
        Returns current amount of lives
    set_lives(lives)
        Sets the lives to a specific value
    live_lost()
        Takes a life and returns current lives to detect potential Game Over
    raise_score(increase)
        Raises the score by a certain amount
    get_score()
        Returns the current score
    '''
 



    def raise_score(self, increase):
        '''
        Increases current score by certain amount

        Parameters
        ----------
        increase : int
            The amount by which the score increases
        '''
        self.score += increase

    def get_score(self):
        '''
        Returns the current score

        Returns
        -------
        int
            Current score
        '''
        return self.score
