from Figures import Piece


class cell(object):
    def __init__(self, coordinate):
        """Takes coordinate and create a cell(creature)"""
        self.coordinate = coordinate
        self.piece_type = Piece
