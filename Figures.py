from Colors import Colors


class Piece(object):
    __name__ = 'Piece'
    available_ways = {}

    def __init__(self, color):
        """Takes a color(int) and creates black or white figure(type of cell) in dependence of color"""
        self.color = color
        self.picture = None
        self.was_moved = False

    def get_picture(self):
        """Returns an image"""
        return self.picture

    def is_possible(self, coords):
        """Takes a list of coordinates, for ex, [A, 1, B, 2](but instead the letters are the corresponding numbers), and
                 checks, can this course be done or not"""

     def possible_ways(self, move_from):
        """Takes a list move_from and return all available ways for this figure from this position"""
        self.available_ways = {}
        c = move_from
        c[0] = ord(c[0].upper()) - 65
        c[1] = int(c[1]) - 1
        counter = 0
        for y in range(8):
            for x in range(8):
                if counter == 0:
                    c.append(x)
                    c.append(y)
                    counter = 1
                c.insert(2, x)
                c.insert(3, y)
                if self.is_possible(self, c):
                    self.available_ways[chr(x + 65) + chr((y + 1))] = 1
        return self.available_ways.keys()


class Free_space(Piece):
    def __init__(self, color=Colors.Free):
        super().__init__(color)
        self.picture = ' '


class Pawn(Piece):
    __name__ = 'Pawn'
    available_ways = {}

    def __init__(self, color):
        super().__init__(color)
        self.picture = '♙' if color == Colors.White else '♙'

    def is_possible(self, coords):  # coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        is_own_field = 0 <= coords[1] - 1 - (self.color - 1) * 4 <= 1
        its_color = self.color * 2 - 3
        is_it_ok = False
        if its_color * deltaY > 0:
            is_it_ok = True
        if not is_it_ok:
            return False


class Knight(Piece):
    __name__ = 'Knight'
    available_ways = {}

    def __init__(self, color):
        super().__init__(color)
        self.picture = '♘' if color == Colors.White else '♞'

    def is_possible(self, coords):  # coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) == 2 and abs(deltaY) == 1:
            return True
        if abs(deltaX) == 1 and abs(deltaY) == 2:
            return True
        return False


class Rook(Piece):
    __name__ = 'Rook'
    available_ways = {}

    def __init__(self, color):
        super().__init__(color)
        self.picture = '♖' if color == Colors.White else '♜'

    def is_possible(self, coords):  # coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) == 0 and abs(deltaY) != 0:
            return True
        if abs(deltaX) != 0 and abs(deltaY) == 0:
            return True
        return False


class Bishop(Piece):
    __name__ = 'Bishop'
    available_ways = {}

    def __init__(self, color):
        super().__init__(color)
        self.picture = '♗' if color == Colors.White else '♝'

    def is_possible(self, coords):  # coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) == abs(deltaY):
            if deltaX != 0:
                return True
        return False


class King(Piece):
    __name__ = 'King'
    available_ways = {}

    def __init__(self, color):
        super().__init__(color)
        self.picture = '♔' if color == Colors.White else '♚'

    def is_possible(self, coords):  # coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) < 2 and abs(deltaY) < 2:
            if abs(deltaX) + abs(deltaY) != 0:
                return True
        return False


class Queen(Piece):
    __name__ = 'Queen'
    available_ways = {}

    def __init__(self, color):
        super().__init__(color)
        self.picture = '♕' if color == Colors.White else '♛'

    def is_possible(self, coords):  # coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) == abs(deltaY):
            if deltaX != 0:
                return True
        if abs(deltaX) == 0 and abs(deltaY) != 0:
            return True
        if abs(deltaY) == 0 and abs(deltaX) != 0:
            return True
        return False
