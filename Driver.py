from       directKey    import  PressKey, ReleaseKey, W, A, S, D

class Driver:

    def __init__(self, layout = "SCOOTER", speedLimit = 50):
        self.layout = layout
        self.speedLimit = 50

    def straight(self):
        PressKey(W)
        ReleaseKey(A)
        ReleaseKey(D)
        ReleaseKey(S)

    def left(self):
        PressKey(A)
        ReleaseKey(W)
        ReleaseKey(D)
        ReleaseKey(S)
        ReleaseKey(A)

    def right(self):
        PressKey(D)
        ReleaseKey(W)
        ReleaseKey(A)
        ReleaseKey(S)
        ReleaseKey(D)

    def slow_down(self):
        ReleaseKey(W)
        ReleaseKey(A)
        ReleaseKey(D)
        ReleaseKey(S)

    def press_break(self):
        PressKey(S)
        ReleaseKey(W)
        ReleaseKey(A)
        ReleaseKey(S)
        ReleaseKey(D)

    
