import enum
import sys
import os


class Colors(object):
    Free = 0
    White = 1
    Black = 2

class Piece(object):
    def __init__(self, color):
        self.color = color
        self.picture = None
        self.was_moved = False

    def get_picture(self):
        return self.picture

class Free_space(Piece):
    def __init__(self, color=Colors.Free):
        super().__init__(color)
        self.picture = ' '

class Pawn(Piece):
    __name__ = 'Pawn'
    
    def __init__(self, color):
        super().__init__(color)
        self.picture = '♙' if color == Colors.White else '♟'
        
    def is_possible(self, coords): #coords = [x1, y1, x2, y2]
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
    
    def __init__(self, color):
        super().__init__(color)
        self.picture = '♘' if color == Colors.White else '♞'
        
    def is_possible(self, coords): #coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) == 2 and abs(deltaY) == 1:
            return True
        if abs(deltaX) == 1 and abs(deltaY) == 2:
            return True
        return False

class Rook(Piece):
    __name__ = 'Rook'
    
    def __init__(self, color):
        super().__init__(color)
        self.picture = '♖' if color == Colors.White else '♜'
        
    def is_possible(self, coords): #coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) == 0 and abs(deltaY) != 0:
            return True
        if abs(deltaX) != 0 and abs(deltaY) == 0:
            return True
        return False

class Bishop(Piece):
    __name__ = 'Bishop'
    
    def __init__(self, color):
        super().__init__(color)
        self.picture = '♗' if color == Colors.White else '♝'
        
    def is_possible(self, coords): #coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) == abs(deltaY):
            if deltaX != 0:
                return True
        return False

class King(Piece):
    __name__ = 'King'
    
    def __init__(self, color):
        super().__init__(color)
        self.picture = '♔' if color == Colors.White else '♚'
        
    def is_possible(self, coords): #coords = [x1, y1, x2, y2]
        deltaX = coords[0] - coords[2]
        deltaY = coords[1] - coords[3]
        if abs(deltaX) < 2 and abs(deltaY) < 2:
            if abs(deltaX) + abs(deltaY) != 0:
                return True
        return False

class Queen(Piece):
    __name__ = 'Queen'
    
    def __init__(self, color):
        super().__init__(color)
        self.picture = '♕' if color == Colors.White else '♛'
        
    def is_possible(self, coords): #coords = [x1, y1, x2, y2]
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

class cell(object):
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.piece_type = Piece

class Chess_board(object):
    
    def change_move(self, color = Colors.Free):
        if color != Colors.Free:
            self.current_move = color
        elif self.current_move == Colors.White:
            self.current_move = Colors.Black
        else:
            self.current_move = Colors.White
            
    def current_king_finder(self):
        for y in range(8):
            for x in range(8):
                if isinstance(self.board[y][x].piece_type, King):
                    if self.board[y][x].piece_type.color == self.current_move:
                        return (x, y)
        
    def current_shah_checker(self):
        if self.is_under_hit(self.current_king_finder()):
            self.shah = True
        else:
            self.shah = False
            
    def prepare_for_castling(self, move_from, move_to): 
        c = move_from + move_to
        c[0] = ord(c[0].upper()) - 65
        c[1] = int(c[1]) - 1
        c[2] = ord(c[2].upper()) - 65
        c[3] = int(c[3]) - 1
        #c = [x1, y1, x2, y2]
        if self.board[c[1]][4].piece_type.was_moved:
            self.ready_for_castling = False
            return
        elif self.board[c[1]][c[0]].piece_type.was_moved:
            self.ready_for_castling = False
            return
        else:
            rangeX = [3, 2, 1] if c[3] == 2 else [3, 4, 5, 6]
            for X in rangeX:
                if X != 3 and not isinstance(self.board[c[0]][X].piece_type, Free_space):
                    self.ready_for_castling = False
                    return
                if X != 6:
                    if self.is_under_hit([X, c[1]]):
                        self.ready_for_castling = False
                        return
        self.ready_for_castling = True
        return
    
    def is_under_hit(self, coordinates): #coordinates = [x2, y2]
        for y in range(8):
            for x in range(8):
                if not isinstance(self.board[y][x].piece_type, Free_space):
                    if self.board[y][x].piece_type.color != self.current_move:
                        is_possible = False
                        try:
                            self.trace_check([x, y] + coordinates)
                            is_possible = self.board[y][x].piece_type.is_possible([x, y] + coordinates)
                        except:
                            pass
                        if is_possible:
                            return True
        return False
                        
    
    def __init__(self):
        self.current_move = Colors.Free
        self.ready_for_castling = False
        self.shah = False
        self.board = [[cell((i, j)) for i in range(8)] for j in range(8)]
        for i in (1, 6):
            for j in range(8):
                self.board[i][j].piece_type = Pawn(Colors.White if i == 1 else Colors.Black)

        for i in (0, 7):
            self.board[i][0].piece_type = Rook(Colors.White if i == 0 else Colors.Black)
            self.board[i][7].piece_type = Rook(Colors.White if i == 0 else Colors.Black)
            self.board[i][1].piece_type = Knight(Colors.White if i == 0 else Colors.Black)
            self.board[i][6].piece_type = Knight(Colors.White if i == 0 else Colors.Black)
            self.board[i][2].piece_type = Bishop(Colors.White if i == 0 else Colors.Black)
            self.board[i][5].piece_type = Bishop(Colors.White if i == 0 else Colors.Black)
            self.board[i][4].piece_type = King(Colors.White if i == 0 else Colors.Black)
            self.board[i][3].piece_type = Queen(Colors.White if i == 0 else Colors.Black)
        for i in range(2, 6):
            for j in range(8):
                self.board[i][j].piece_type = Free_space()

    def print(self):
        output = '  A B C D E F G H\n' if self.current_move == Colors.White else '  H G F E D C B A\n'
        for i in range(8) if self.current_move == Colors.Black else range(7, -1, -1):
            output += str(i + 1) + ' '
            for j in range(8) if self.current_move == Colors.White else range(7, -1, -1):
                output += '\x1b[0m'
                if isinstance(self.board[i][j].piece_type, cell):
                    self.board[i][j].piece_type = Free_space()
                output += '\x1b[44m' if (i + j) % 2 == 0 else '\x1b[43m'
                output += self.board[i][j].piece_type.get_picture() + ' '
            output += '\x1b[0m\n'
        print(output, end = '')
        print('Current Move: {}'.format('White' if self.current_move == Colors.White else 'Black'))
        if self.shah:
            print('You\'re under shah!')
        
    def move(self, coords): #coords = ['<letter>', '<int>', '<letter>', '<int>']
        if len(coords) != 4:
            raise NotImplementedError('Wrong coordinates, try again!')
        c = coords
        c[0] = ord(c[0].upper()) - 65
        c[1] = int(c[1]) - 1
        c[2] = ord(c[2].upper()) - 65
        c[3] = int(c[3]) - 1
        #c = [x1, y1, x2, y2]
        if -1 >= c[0] or c[0] >= 8:
            raise NotImplementedError('Out of board! <Row \'From\'>')
        if -1 >= c[1] or c[1] >= 8:
            raise NotImplementedError('Out of board! <Line \'From\'>')
        if -1 >= c[2] or c[2] >= 8:
            raise NotImplementedError('Out of board! <Row \'To\'>')
        if -1 >= c[3] or c[3] >= 8:
            raise NotImplementedError('Out of board! <Line \'To\'>')
        if isinstance(self.board[c[1]][c[0]].piece_type, Free_space):
            raise NotImplementedError('Stop trying to move this empty space!')
        if self.board[c[1]][c[0]].piece_type.color != self.current_move:
            raise NotImplementedError('This piece is not yours!')
        if self.ready_for_castling:
            self.make_move(c)
            self.change_move()
            self.make_move(3, c[0], 3, 1 if c[1] == 2 else 5)
            self.ready_for_castling = False
            return
        is_possible = False
        if not isinstance(self.board[c[1]][c[0]].piece_type, Knight):
            self.trace_check(c)
        is_possible = self.board[c[1]][c[0]].piece_type.is_possible(c)
        if isinstance(self.board[c[1]][c[0]].piece_type, Pawn):
            if self.pawn_checker(c):
                self.make_move(c)
                self.current_shah_checker()
                return
        if not is_possible:
            raise NotImplementedError('This movement is prohibited by {}!'.format(self.board[c[1]][c[0]].piece_type.__name__))
        if self.board[c[3]][c[2]].piece_type.color == self.current_move:
            raise NotImplementedError('Trying to hit yourself with a {}!'.format(self.board[c[1]][c[0]].piece_type.__name__))
        self.make_move(c)
        self.current_shah_checker()
        
    def trace_check(self, c): #c = [x1, y1, x2, y2]
        deltaX = c[2] - c[0]
        deltaY = c[3] - c[1]
        if deltaX == 0 and deltaY == 0:
            raise NotImplementedError('You didn\'t move the piece!')
        elif deltaX == 0:
            stepY = int(deltaY / abs(deltaY))
            rangeY = range(c[1] + stepY, c[3], stepY)
            for Y in rangeY:
                if not isinstance(self.board[Y][c[0]].piece_type, Free_space):
                    raise NotImplementedError('Trying to get over the piece with a {}!'.format(self.board[c[1]][c[0]].piece_type.__name__))
            if self.board[c[3]][c[2]].piece_type.color == self.current_move:
                raise NotImplementedError('Trying to hit yourself with a {}!'.format(self.board[c[1]][c[0]].piece_type.__name__))
            return
        elif deltaY == 0:
            stepX = int(deltaX / abs(deltaX))
            rangeX = range(c[0] + stepX, c[2], stepX)
            for X in rangeX:
                if not isinstance(self.board[1][c[X]].piece_type, Free_space):
                    raise NotImplementedError('Trying to get over the piece with a {}!'.format(self.board[c[1]][c[0]].piece_type.__name__))
            if self.board[c[3]][c[2]].piece_type.color == self.current_move:
                raise NotImplementedError('Trying to hit yourself with a {}!'.format(self.board[c[1]][c[0]].piece_type.__name__))
        elif abs(deltaX) != abs(deltaY):
            raise NotImplementedError('Unable to do this move!')
        else:
            stepY = int(deltaY / abs(deltaY))
            stepX = int(deltaX / abs(deltaX))
            rangeY = [c[1] + stepY * i for i in range(1, abs(deltaY))]
            rangeX = [c[0] + stepX * j for j in range(1, abs(deltaX))]
            for i in range(len(rangeY)):
                if not isinstance(self.board[rangeY[i]][rangeX[i]].piece_type, Free_space):
                    raise NotImplementedError('Trying to get over the piece with a {}!'.format(self.board[c[1]][c[0]].piece_type.__name__))
            if self.board[c[3]][c[2]].piece_type.color == self.current_move:
                raise NotImplementedError('Trying to hit yourself with a {}!'.format(self.board[c[1]][c[0]].piece_type.__name__))
        
    def make_move(self, c):
        self.board[c[3]][c[2]].piece_type = self.board[c[1]][c[0]].piece_type
        try:
            self.board[c[3]][c[2]].piece_type.was_moved = True
        except AttributeError:
            pass
        self.board[c[1]][c[0]].piece_type = Free_space()
        self.shah = False
        self.change_move()
        
    def pawn_checker(self, c):
        deltaX = c[2] - c[0]
        deltaY = c[3] - c[1]
        if abs(deltaX) > 1 or abs(deltaY) > 2:
            raise NotImplementedError('This move is prohibited by Pawn!')
        if abs(deltaX) == 1:
            if abs(deltaY) != 1:
                raise NotImplementedError('This move is prohibited by Pawn!')
            else:
                if isinstance(self.board[c[3]][c[2]].piece_type, Free_space):
                    raise NotImplementedError('Trying to hit a free space with a Pawn!')
                elif self.board[c[3]][c[2]].piece_type.color == self.current_move:
                    raise NotImplementedError('Trying to hit yourself with a Pawn!')
                else:
                    return True
        else:
            if abs(deltaY) == 0:
                raise NotImplementedError('You didn\'t move the piece!')
            elif abs(deltaY) == 1:
                return True
            elif self.board[c[1]][c[0]].piece_type.was_moved:
                raise NotImplementedError('Unable to do a long move: Pawn was moved')
            else:
                return True


desk = Chess_board()

fst_move = input('First move (white/black): ')
fst_move = Colors.White if fst_move.lower().startswith('w') else Colors.Black
desk.change_move(fst_move)

desk.print()

move_from = []
move_to = []
while True:
    move_from = input('From: ')
    if move_from.lower().startswith('stop'):
        break
    elif move_from.lower().startswith('castling'):
        move_from = input('Try to do castling (left/right): ')
        if desk.current_move == Colors.White:
            move_from = ['A'] if move_from.lower().startswith('l') else ['H']
            move_from.append('1')
            move_to = ['F' if move_from[0] == 'H' else 'C', '1']
        else:
            move_from = ['H'] if move_from.lower().startswith('l') else ['A']
            move_from.append('8')
            move_to = ['F' if move_from[0] == 'H' else 'C', '8']
        desk.prepare_for_castling(move_from, move_to)
    else:
        move_from = list(move_from)
        move_to = list(input('To: '))
    coordinates = move_from + move_to
    sys.stdout.flush()
    try:
        desk.move(coordinates)
        desk.print()
    except Exception as e:
        print(e)
        pass

print('Thanks for playing!')
