class Card(object):
    def __init__(self, suite, number):
        self.suite = suite
        self.number = number

    def __str__(self):
        return self.suite + " " + str(self.number)