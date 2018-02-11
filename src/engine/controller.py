from pygame.locals import KEYUP, KEYDOWN


class Controller:
    def __init__(self):
        self.directions = []
        self.actions = []

    def get_direction(self):
        if self.directions:
            return self.directions[-1]

    def get_action(self):
        if self.actions:
            return self.actions[-1]

    def process(self, event):
        if event.type == KEYDOWN:
            return True
        elif event.type == KEYUP:
            return True
        return False


class KeyboardController(Controller):
    pass
