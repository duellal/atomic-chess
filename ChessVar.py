# Author: Alexandria Duell
# GitHub username: duellal
# Date:
# Description: Creates a ChessVar class with methods to play a game of atomic chess.

class Player:
    """
    Initializes a player for the atomic chess game. The player must pick a color between white and black. Both
    players cannot be the same color in order to play against each other.
    """

    def __init__(self, color):
        self._color = color

    def get_color(self):
        """
        Gets the player’s chess piece color.
        :return: string - color
        """
        return self._color


class ChessVar:
    def __init__(self):
        self._all_game_states = ['UNFINISHED', 'WHITE WON', 'BLACK WON']
        self._game_state = self._all_game_states[0]
        self._board = {
            1: {'a': 'w-r', 'b': 'w-kn', 'c': 'w-b', 'd': 'w-q', 'e': 'w-kg', 'f': 'w-b', 'g': 'w-kn', 'h': 'w-r'},
            2: {'a': 'w-p', 'b': 'w-p', 'c': 'w-p', 'd': 'w-p', 'e': 'w-p', 'f': 'w-p', 'g': 'w-p', 'h': 'w-p'},
            3: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': 'w-p', 'g': '', 'h': ''},
            4: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            5: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            6: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            7: {'a': 'b-p', 'b': 'b-p', 'c': 'b-p', 'd': 'b-p', 'e': 'b-p', 'f': 'b-p', 'g': 'b-p', 'h': 'b-p'},
            8: {'a': 'b-r', 'b': 'b-kn', 'c': 'b-b', 'd': 'b-kg', 'e': 'b-q', 'f': 'b-b', 'g': 'b-kn', 'h': 'b-r'}
        }
        self._turn = True
        self._alph_tuple = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        # Piece Moves dictionary:
        # self._piece_moves = {
        #     'kg': {
        #         'num_sq': [1],
        #         'dir': 'any'
        #     },
        #     'q': {
        #         'num_sq': [7],
        #         'dir': '+'
        #     },
        #     'b': {
        #         'num_sq': [7],
        #         'dir': 'x'
        #     },
        #     'kn': {
        #         # Total moves per turn
        #         #     2 moves in a + dir, then 1 move right angle
        #         'num_sq': [2, 1],
        #         'dir': ['+', 'r']
        #     },
        #     'r': {
        #         'num_sq': [7],
        #         'dir': '+'
        #     },
        #     'p': {
        #         # 1st move - up to 2 squares
        #         # 2nd move + onward - up to 1 square
        #         'num_sq': [2, 1],
        #         'dir': 'w'
        #     }
        # }

    def get_game_state(self):
        """
        [DONE]
        Gets the current game state from three options: UNFINISHED, WHITE_WON, or BLACK_WON.
        :return: string
        """
        return self._game_state

    def set_game_state(self, player_won):
        """
        [DONE]
        :param player_won:
        :return:
        """
        # White wins:
        if player_won == 'w':
            self._game_state = self._all_game_states[1]
            return

        # Black wins:
        elif player_won == 'b':
            self._game_state = self._all_game_states[2]
            return

        # If no player_won, set game state to UNFINISHED
        self._game_state = self._all_game_states[0]

    def make_move(self, init_sq, place_sq):
        """
        Makes indicated move for the chess piece as long as the game has not already been won, it's the player's
        chess piece whose turn it currently is, and the move is legal.
        :param init_sq: string - column and row acronym for the chess piece to move
            - ex: b2
        :param place_sq: string - column and row acronym for the placement of the chess piece.
            - ex: g5
        :return: boolean
        """
        move_piece = self.get_piece(init_sq)
        player_turn = self.get_turn()
        move_valid = None

        print('Player Turn:', player_turn)
        print('Move piece:', move_piece)
        print('Init Square:', init_sq)
        print('Place Square:', place_sq)


    # Cases to return false:
        # If the square is empty:
        if move_piece is None:
            return False
        # If the chess piece is not the current player's:
        elif player_turn not in move_piece:
            return False
        # If the game is not unfinished (someone has won):
        elif self.get_game_state() is not self._all_game_states[0]:
            return False

    # If no case for the piece return false, else continue to see if move is legal:
        match move_piece[-1]:
            case 'p':
                print('Pawn')
                move_valid = self.check_pawn_move(player_turn, init_sq, place_sq)
            case 'b':
                print('Bishop')
                pass
            case 'r':
                print('Rook')
                pass
            case 'n':
                print('Knight')
                pass
            case 'q':
                print('Queen')
                pass
            case 'g':
                print('King')
                pass
            case _:
                print('No Matching Piece')
                return False
        # If move is legal:
        #   Remove exploded + captured pieces
        #   Move the initial piece to the placement square
        #   Set the turn as the next player's
        #   Return Boolean
        if move_valid:
            self.remove_pieces_around_explosion(place_sq)
            self.move_piece(move_piece, init_sq, place_sq)
            self.set_turn()
            print('Turn Success Board:', self.print_board())
            return move_valid
        # Return false if move is not legal:
        print('Turn Fail Board:', self.print_board())
        return move_valid

    def print_board(self):
        """
        [DONE]
        Prints the current state of the board.
        :return: dictionary of dictionaries
        """
        board_rows = []
        for row in range(1, len(self._board) + 1):
            print(f'{row}: {self._board[row]}')

    def set_turn(self):
        """
        [DONE]
        Changes the turn after a player has made a legal move, if they can.
        :return: None
        """
        self._turn = not self._turn

    def get_turn(self):
        """
        [DONE]
        Gets the current player's turn by their color acronym.
        :return: boolean
        """
        if self._turn:
            return 'w'
        return 'b'

    def get_piece(self, pos):
        """
        [DONE]
        Gets the piece on the board if there is one at the given location.
        :param pos: string - denotes location on chess board; ex: "C4" or "c4"
        :return: None or string
            - None: if there is no piece in that location
            - String: the piece acronym at that location
        """
        p_row = int(pos[1])
        p_col = pos[0].lower()
        # Actual square at position:
        true_sq = self._board[p_row][p_col]
        if len(true_sq) >= 3:
            return true_sq
        # Catch all:
        return None

    def move_piece(self, move_piece, init_sq, place_sq):
        """
        [DONE]
        :param move_piece:
        :param init_sq:
        :param place_sq:
        :return:
        """
        init_col = init_sq[0].lower()
        init_row = int(init_sq[1])

        place_col = place_sq[0].lower()
        place_row = int(place_sq[1])

        self._board[init_row][init_col] = ''
        self._board[place_row][place_col] = move_piece
        return

    def get_col_num_helper(self, col):
        """
        [DONE]
        :param col:
        :return:
        """
        # Get the column number as its index (will need in below for loop):
        for index, letter in enumerate(self._alph_tuple):
            if letter == col:
                return index

    def remove_pieces_around_explosion(self, cap_pos):
        """
        [DONE]
        :param cap_pos:
        :return:
        """
        cap_col = cap_pos[0].lower()
        # Get the column number as its index (will need in below for loop):
        cap_col_num = self.get_col_num_helper(cap_col)
        cap_row = int(cap_pos[1])
        exploded_pieces = []
        count_kings = 0

        for row_num in self._board:
            # Check if rows are the explosion row, the row before or the row after:
            if row_num == cap_row or row_num == cap_row - 1 or row_num == cap_row + 1:
                for col_index, col in enumerate(self._board[row_num]):
                    # Check the columns of the explosion, and the columns before and after:
                    if col_index == cap_col_num - 1 or col_index == cap_col_num or col_index == cap_col_num + 1:
                        # Check if any piece is a pawn:
                        #   1) If the pawn is the captured pawn, add to list
                        #   2) Otherwise pass
                        if self._board[row_num][col].find('p') > 0:
                            if row_num == cap_row and col == cap_col:
                                exploded_pieces.append(f'{col}{row_num}')
                        # Check if there is a piece on the square:
                        elif len(self._board[row_num][col]) > 0:
                            # If piece is a king, add to the count:
                            if 'kg' in self._board[row_num][col]:
                                count_kings += 1
                            # Check if more than 1 king is being exploded:
                            if count_kings == 2:
                                return False
                            # Append the square to the list:
                            exploded_pieces.append(f'{col}{row_num}')

        for square in exploded_pieces:
            sq_col = square[0].lower()
            sq_row = int(square[1])

            # Check if any piece is a pawn:
            #   1) If the pawn is the captured pawn, remove
            #   2) Otherwise do not remove
            if 'p' in self._board[sq_row][sq_col]:
                if cap_pos.lower() == square:
                    self._board[cap_row][cap_col] = ''
            elif 'kg' in self._board[sq_row][sq_col]:
                # If white king is captured, black wins:
                if 'w' in self._board[sq_row][sq_col]:
                    return self.set_game_state('b')
                # If black king is captured, white wins:
                if 'b' in self._board[sq_row][sq_col]:
                    return self.set_game_state('w')
            # Remove all other pieces:
            self._board[sq_row][sq_col] = ''

        return True

    def check_pawn_move(self, player_turn, init_sq, place_sq):
        poss_moves = []
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.get_col_num_helper(init_col)
        col_lower = init_col_num - 2
        col_upper = init_col_num + 2
        # Makes sure that columns for the loops cannot go off or go to the other side of the board:
        if col_lower < -1:
            col_lower = -1
        if col_upper > 8:
            col_upper = 8

        # If pawn is in initial row, pawn can move 1 or 2 squares:
        if player_turn == 'w' and init_row == 2:
            for row in range(3, 5):
                for col in range(col_lower, col_upper + 1):
                    # First row, 3 consecutive cols (one on each side of init col):
                    if row == 3 and col in range(col_lower + 1, col_upper):
                        poss_moves.append(f'{self._alph_tuple[col]}{row}')
                        if f'{self._alph_tuple[col]}{row}' == place_sq:
                            return True
                    # Second row, only pass cols 2 squares over fom init col:
                    if row == 4 and ((0 < col_lower == col) or (8 > col_upper == col) or (col == init_col_num)):
                        poss_moves.append(f'{self._alph_tuple[col]}{row}')
                        if f'{self._alph_tuple[col]}{row}' == place_sq:
                            return True
            return False
        if player_turn == 'b' and init_row == 7:
            for row in range(5, 7):
                for col in range(col_lower, col_upper + 1):
                    # First row, 3 consecutive cols (one on each side of init col):
                    if row == 6 and col in range(col_lower + 1, col_upper):
                        poss_moves.append(f'{self._alph_tuple[col]}{row}')
                        if f'{self._alph_tuple[col]}{row}' == place_sq:
                            return True
                    # Second row, only pass cols 2 squares over fom init col:
                    if row == 5 and ((0 < col_lower == col) or (8 > col_upper == col) or (col == init_col_num)):
                        poss_moves.append(f'{self._alph_tuple[col]}{row}')
                        if f'{self._alph_tuple[col]}{row}' == place_sq:
                            return True
            return False
        # If pawn is not in initial row, pawn can move only 1 square
        else:
            if player_turn == 'w':
                for row in range(init_row + 1, init_row + 2):
                    for col in range(col_lower, col_upper + 1):
                        # First row, 3 consecutive cols (one on each side of init col):
                        if col in range(col_lower + 1, col_upper):
                            poss_moves.append(f'{self._alph_tuple[col]}{row}')
                            if f'{self._alph_tuple[col]}{row}' == place_sq:
                                return True
                return False
            if player_turn == 'b':
                for row in range(init_row - 1, init_row - 2):
                    for col in range(col_lower, col_upper + 1):
                        # First row, 3 consecutive cols (one on each side of init col):
                        if col in range(col_lower + 1, col_upper):
                            poss_moves.append(f'{self._alph_tuple[col]}{row}')
                            if f'{self._alph_tuple[col]}{row}' == place_sq:
                                return True
                return False
        return False


# board = ChessVar()
# # print(board.get_turn())
# print(board.set_turn())
# # print(board.get_game_state())
# # print(board.get_turn())
# board.print_board()
# # print('Get Piece on Board:', board.get_piece('C8'))
# print(board.make_move('b7', 'b5'))
# board.print_board()
