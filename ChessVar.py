# Author: Alexandria Duell
# GitHub username: duellal
# Date:
# Description: Creates a ChessVar class with methods to play a game of atomic chess.


class ChessVar():
    def __init__(self):
        self._all_game_states = ['UNFINISHED', 'WHITE WON', 'BLACK WON']
        self._game_state = 'UNFINISHED'
        self._board = [
            {'a': 'w-r', 'b': 'w-kn', 'c': 'w-b', 'd': 'w-q', 'e': 'w-kg', 'f': 'w-b', 'g': 'w-kn', 'h': 'w-r'},
            {'a': 'w-p', 'b': 'w-p', 'c': 'w-p', 'd': 'w-p', 'e': 'w-p', 'f': 'w-p', 'g': 'w-p', 'h': 'w-p'},
            {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            {'a': 'b-p', 'b': 'b-p', 'c': 'b-p', 'd': 'b-p', 'e': 'b-p', 'f': 'b-p', 'g': 'b-p', 'h': 'b-p'},
            {'a': 'b-r', 'b': 'b-kn', 'c': 'b-b', 'd': 'b-q', 'e': 'b-kg', 'f': 'b-b', 'b-g': 'b-kn', 'h': 'b-r'}
        ]
        self._turn = True
        self._piece_moves = {
            'kg': {
                'num_sq': [1],
                'dir': 'any'
            },
            'q': {
                'num_sq': [7],
                'dir': '+'
            },
            'b': {
                'num_sq': [7],
                'dir': 'x'
            },
            'kn': {
                # Total moves per turn
                #     2 moves in a + dir, then 1 move right angle
                'num_sq': [2, 1],
                'dir': ['+', 'r']
            },
            'r': {
                'num_sq': [7],
                'dir': '+'
            },
            'p': {
                # 1st move - up to 2 squares
                # 2nd move + onward - up to 1 square
                'num_sq': [2, 1],
                'dir': 'w'
            }
        }

    def get_game_state(self):
        return self._game_state

    def make_move(self, init_sq, place_sq):
        return

    def print_board(self):
        return self._board

    def set_turn(self):
        self._turn = not self._turn

    def get_turn(self):
        return self._turn

    def get_piece(self, pos):
        """
        Gets the piece on the board if there is one at the given location.
        :param pos: string - denotes location on chess board; ex: "C4" or "c4"
        :return: None or string
            - None: if there is no piece in that location
            - String: the piece acronym at that location
        """
        p_row = int(pos[1]) - 1
        p_col = pos[0].lower()
        for index, row in enumerate(self._board):
            if index == p_row:
                if row[p_col] == '':
                    return None
                else:
                    return row[p_col]
        # Catch all:
        return None

    def check_playable_move(self, pos1, pos2):
        return


board = ChessVar()
print(board.get_turn())
print(board.set_turn())
print(board.get_game_state())
print(board.get_turn())
print(board.print_board())
print('Get Piece on Board:', board.get_piece('c5'))
