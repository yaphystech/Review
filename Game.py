from Chess_board import Chess_board
from Colors import Colors
import sys


class Game(object):
    desk = Chess_board()
    move_from = []
    move_to = []

    def __init__(self):
        """Creates game"""
        self.desk = Chess_board()

        fst_move = input('First move (white/black): ')
        fst_move = Colors.White if fst_move.lower().startswith('w') else Colors.Black
        self.desk.change_move(fst_move)

        self.desk.print()

        self.move_from = []
        self.move_to = []

    def run(self):
        """"Starts the game"""
        while True:
            self.move_from = input('From: ')
            if self.move_from.lower().startswith('stop'):
                break
            elif self.move_from.lower().startswith('castling'):
                self.move_from = input('Try to do castling (left/right): ')
                if self.desk.current_move == Colors.White:
                    self.move_from = ['A'] if self.move_from.lower().startswith('l') else ['H']
                    self.move_from.append('1')
                    self.move_to = ['F' if self.move_from[0] == 'H' else 'C', '1']
                else:
                    self.move_from = ['H'] if self.move_from.lower().startswith('l') else ['A']
                    self.move_from.append('8')
                    self.move_to = ['F' if self.move_from[0] == 'H' else 'C', '8']
                self.desk.prepare_for_castling(self.move_from, self.move_to)
            else:
                self.move_from = list(self.move_from)
                self.move_to = list(input('To: '))
            coordinates = self.move_from + self.move_to
            sys.stdout.flush()
            try:
                self.desk.move(coordinates)
                self.desk.print()
            except Exception as e:
                print(e)
                pass
