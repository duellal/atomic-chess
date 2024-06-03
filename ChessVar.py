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
        self._all_game_states = ['UNFINISHED', 'WHITE_WON', 'BLACK_WON']
        self._game_state = self._all_game_states[0]
        self._board = {
            1: {'a': 'w-r', 'b': 'w-kn', 'c': 'w-b', 'd': 'w-q', 'e': 'w-kg', 'f': 'w-b', 'g': 'w-kn', 'h': 'w-r'},
            2: {'a': 'w-p', 'b': 'w-p', 'c': 'w-p', 'd': 'w-p', 'e': 'w-p', 'f': 'w-p', 'g': 'w-p', 'h': 'w-p'},
            3: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            4: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            5: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            6: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            7: {'a': 'b-p', 'b': 'b-p', 'c': 'b-p', 'd': 'b-p', 'e': 'b-p', 'f': 'b-p', 'g': 'b-p', 'h': 'b-p'},
            8: {'a': 'b-r', 'b': 'b-kn', 'c': 'b-b', 'd': 'b-q', 'e': 'b-kg', 'f': 'b-b', 'g': 'b-kn', 'h': 'b-r'}
        }
        self._turn = True
        self._alph_tuple = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')

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
        place_sq_piece = self.get_piece(place_sq)
        player_turn = self.get_turn()
        move_valid = False

        print('Player Turn:', player_turn)
        print('Move piece:', move_piece)
        print('Init Square:', init_sq)
        print('Place Square:', place_sq)
        print('Place Piece:', place_sq_piece)

        # Cases to return false:
        # If the square is empty:
        if move_piece == '':
            return False
        # If the chess piece is not the current player's:
        elif player_turn not in move_piece:
            print('HERE')
            return False
        # Can't capture your own piece:
        elif player_turn in place_sq_piece:
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
                move_valid = self.check_bishop_move(init_sq, place_sq)
                pass
            case 'r':
                print('Rook')
                move_valid = self.check_rook_move(init_sq, place_sq)
                pass
            case 'n':
                print('Knight')
                pass
            case 'q':
                print('Queen')
                bishop_pass = self.check_bishop_move(init_sq, place_sq)
                rook_pass = self.check_rook_move(init_sq, place_sq)

                if bishop_pass or rook_pass:
                    move_valid = True
            case 'g':
                print('King')
                move_valid = self.check_king_move(init_sq, place_sq)
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
            explosion = None
            if move_valid and place_sq_piece:
                explosion = self.remove_pieces_around_explosion(place_sq)

            self.move_piece(move_piece, explosion, init_sq, place_sq)
            self.set_turn()
            print('Turn Success Board:')
            self.print_board()
            return move_valid
        # Return false if move is not legal:
        print('Turn Fail Board:')
        self.print_board()
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
            - String: the piece acronym at that location or ''
        """
        p_row = int(pos[1])
        p_col = pos[0].lower()
        # Actual square at position:
        return self._board[p_row][p_col]

    def move_piece(self, move_piece, explosion, init_sq, place_sq):
        """
        [DONE]
        :param explosion:
        :param move_piece:
        :param init_sq:
        :param place_sq:
        :return:
        """
        init_col = init_sq[0].lower()
        init_row = int(init_sq[1])

        place_col = place_sq[0].lower()
        place_row = int(place_sq[1])

        # If a pawn causes an explosion, remove the pawn
        if explosion and 'p' in move_piece:
            self._board[init_row][init_col] = ''
            self._board[place_row][place_col] = ''
            return

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

        return exploded_pieces

    def check_pawn_move(self, player_turn, init_sq, place_sq):
        """
        [DONE] - Need to add description
        Pawn moves forward 1, unless 1st move, then can move forward 1 or 2 squares.
        Pawn captures forward 1 diagonally
        :param player_turn:
        :param init_sq:
        :param place_sq:
        :return:
        """
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
                        # Pawn moves straight with no captures:
                        if (f'{self._alph_tuple[col]}{row}' == place_sq
                                and col == init_col_num
                                and self._board[row][self._alph_tuple[col]] == ''):
                            return True
                        # Pawn moves diagonal with capture:
                        #   Pawn cannot move diagonally normally
                        elif (f'{self._alph_tuple[col]}{row}' == place_sq
                              and self._board[row][self._alph_tuple[col]] != ''
                              and self._alph_tuple[col] != init_col):
                            return True
                    # Second row, only pass cols 2 squares over fom init col:
                    if (row == 4
                            and ((0 < col_lower == col)
                                 or (8 > col_upper == col)
                                 or (col == init_col_num))):
                        # Pawn moves straight with no captures:
                        if (f'{self._alph_tuple[col]}{row}' == place_sq
                                and col == init_col_num
                                and self._board[row][self._alph_tuple[col]] == ''):
                            return True
                        # Pawn moves diagonal with capture:
                        #   Pawn cannot move diagonally normally
                        elif (f'{self._alph_tuple[col]}{row}' == place_sq
                              and self._board[row][self._alph_tuple[col]] != ''
                              and self._alph_tuple[col] != init_col):
                            return True
            return False
        if player_turn == 'b' and init_row == 7:
            for row in range(5, 7):
                for col in range(col_lower, col_upper + 1):
                    # First row, 3 consecutive cols (one on each side of init col):
                    if row == 6 and col in range(col_lower + 1, col_upper):
                        # Pawn moves straight with no captures:
                        if (f'{self._alph_tuple[col]}{row}' == place_sq
                                and col == init_col_num
                                and self._board[row][self._alph_tuple[col]] == ''):
                            return True
                        # Pawn moves diagonal with capture:
                        #   Pawn cannot move diagonally normally
                        elif (f'{self._alph_tuple[col]}{row}' == place_sq
                              and self._board[row][self._alph_tuple[col]] != ''
                              and self._alph_tuple[col] != init_col):
                            return True
                    # Second row, only pass cols 2 squares over fom init col:
                    if (row == 5
                            and ((0 < col_lower == col)
                                 or (8 > col_upper == col)
                                 or (col == init_col_num))):
                        # Pawn moves straight with no captures:
                        if (f'{self._alph_tuple[col]}{row}' == place_sq
                                and col == init_col_num
                                and self._board[row][self._alph_tuple[col]] == ''):
                            return True
                        # Pawn moves diagonal with capture:
                        #   Pawn cannot move diagonally normally
                        elif (f'{self._alph_tuple[col]}{row}' == place_sq
                              and self._board[row][self._alph_tuple[col]] != ''
                              and self._alph_tuple[col] != init_col):
                            return True
            return False
        # If pawn is not in initial row, pawn can move only 1 square
        else:
            if player_turn == 'w':
                for row in range(init_row + 1, init_row + 2):
                    for col in range(col_lower, col_upper + 1):
                        # First row, 3 consecutive cols (one on each side of init col):
                        if col in range(col_lower + 1, col_upper):
                            # Pawn moves straight with no captures:
                            if (f'{self._alph_tuple[col]}{row}' == place_sq
                                    and col == init_col_num
                                    and self._board[row][self._alph_tuple[col]] == ''):
                                return True
                            # Pawn moves diagonal with capture:
                            #   Pawn cannot move diagonally normally
                            elif (f'{self._alph_tuple[col]}{row}' == place_sq
                                  and self._board[row][self._alph_tuple[col]] != ''
                                  and self._alph_tuple[col] != init_col):
                                return True
                return False
            if player_turn == 'b':
                for row in range(init_row - 1, init_row):
                    for col in range(col_lower, col_upper + 1):
                        # First row, 3 consecutive cols (one on each side of init col):
                        if col in range(col_lower + 1, col_upper):
                            # Pawn moves straight with no captures:
                            if (f'{self._alph_tuple[col]}{row}' == place_sq
                                    and col == init_col_num
                                    and self._board[row][self._alph_tuple[col]] == ''):
                                return True
                            # Pawn moves diagonal with capture:
                            #   Pawn cannot move diagonally normally
                            elif (f'{self._alph_tuple[col]}{row}' == place_sq
                                  and self._board[row][self._alph_tuple[col]] != ''
                                  and self._alph_tuple[col] != init_col):
                                return True
                return False
        return False

    def check_rook_move(self, init_sq, place_sq):
        """
        Rook moves forward or back in any direction any number of squares.
        Cannot jump pieces - has to stop at end of board or at another piece
        :param init_sq:
        :param place_sq:
        :return:
        """
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.get_col_num_helper(init_col)

        place_row = int(place_sq[1])
        place_col = place_sq[0].lower()
        place_col_num = self.get_col_num_helper(place_col)

        # Going horizontally (columns):
        if init_row == place_row:
            if init_col_num < place_col_num:
                for col in range(init_col_num + 1, place_col_num + 1):
                    # If there is a piece in the way of the placement square:
                    if (self._board[init_row][self._alph_tuple[col]] != ''
                            and f'{self._alph_tuple[col]}{init_row}' != place_sq):
                        return False
                return True

            if init_col_num > place_col_num:
                for col in range(place_col_num, init_col_num):
                    print('Col:', col)
                    # If there is a piece in the way of the placement square:
                    if (self._board[init_row][self._alph_tuple[col]] != ''
                            and f'{self._alph_tuple[col]}{init_row}' != place_sq):
                        return False
                return True

            # If not in bounds:
            return False
        # Going vertically (rows):
        elif init_col == place_col:
            if init_row < place_row:
                for row in range(init_row + 1, place_row + 1):
                    # If there is a piece in the way of the placement square:
                    if (self._board[row][init_col] != ''
                            and f'{self._alph_tuple[init_col_num]}{row}' != place_sq):
                        return False
                return True
            elif init_row > place_row:
                for row in range(place_row, init_row):
                    # If there is a piece in the way of the placement square:
                    if (self._board[row][self._alph_tuple[init_col_num]] != ''
                            and f'{self._alph_tuple[init_col_num]}{row}' != place_sq):
                        return False
                return True

            # If not in bounds:
            return False
        # If going diagonally or any other square outside the "t":
        else:
            return False

    def check_king_move(self, init_sq, place_sq):
        """
        [DONE]
        :param init_sq:
        :param place_sq:
        :return:
        """
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.get_col_num_helper(init_col)

        for row in range(init_row - 1, init_row + 2):
            for col in range(init_col_num - 1, init_col_num + 2):
                if place_sq == f'{self._alph_tuple[col]}{row}':
                    return True
        return False

    def check_bishop_move(self, init_sq, place_sq):
        """
        [DONE]
        :param init_sq:
        :param place_sq:
        :return:
        """
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.get_col_num_helper(init_col)

        place_row = int(place_sq[1])
        place_col = place_sq[0].lower()
        place_col_num = self.get_col_num_helper(place_col)

        # Diagonal Up - Increase Row, Increase Col (Left Up):
        if init_row < place_row:
            if init_col_num < place_col_num:
                return self.bishop_recursion_helper(init_col_num, init_row, init_col_num + 1, init_row + 1, place_sq)
            # Increase Row, Decrease Col (Right Up):
            elif init_col_num > place_col_num:
                return self.bishop_recursion_helper(init_col_num, init_row, init_col_num - 1, init_row + 1, place_sq)
            # Col is the same:
            else:
                return False

        # Diagonal Down - Decrease row, Decrease Col (Left Down):
        elif init_row > place_row:
            if init_col_num < place_col_num:
                return self.bishop_recursion_helper(init_col_num, init_row, init_col_num + 1, init_row - 1, place_sq)
            # Decrease Row, Increase Col (Right Down):
            elif init_col_num > place_col_num:
                return self.bishop_recursion_helper(init_col_num, init_row, init_col_num - 1, init_row - 1, place_sq)
            # Col is the same:
            else:
                return False
        # Row is the same as the initial square:
        return False

    def bishop_recursion_helper(self, init_sq_col, init_sq_row, next_sq_col, next_sq_row, place_sq):
        """
        [DONE]
        :param init_sq_col:
        :param init_sq_row:
        :param next_sq_col:
        :param next_sq_row:
        :param place_sq:
        :return:
        """
        # Going back in columns + rows:
        if next_sq_col + 1 == init_sq_col:
            if next_sq_row + 1 == init_sq_row:
                # If there is a piece in the way of the placement square:
                if (self._board[next_sq_row][self._alph_tuple[next_sq_col]] != ''
                        and f'{self._alph_tuple[next_sq_col]}{next_sq_row}' != place_sq):
                    return False
                # If at the placement square, return True:
                elif f'{self._alph_tuple[next_sq_col]}{next_sq_row}' == place_sq:
                    return True
                # If not at the placement square continue:
                return self.bishop_recursion_helper(next_sq_col, next_sq_row, next_sq_col - 1, next_sq_row - 1, place_sq)

        # Going back in columns, going forward in rows:
            elif init_sq_row == next_sq_row - 1:
                # If there is a piece in the way of the placement square:
                if (self._board[next_sq_row][self._alph_tuple[next_sq_col]] != ''
                        and f'{self._alph_tuple[next_sq_col]}{next_sq_row}' != place_sq):
                    return False
                # If at the placement square, return True:
                elif f'{self._alph_tuple[next_sq_col]}{next_sq_row}' == place_sq:
                    return True
                # If not at the placement square continue:
                return self.bishop_recursion_helper(next_sq_col, next_sq_row, next_sq_col - 1, next_sq_row + 1, place_sq)

        # Going forward in columns, going backward in rows:
        if init_sq_col == next_sq_col - 1:
            if next_sq_row + 1 == init_sq_row:
                # If there is a piece in the way of the placement square:
                if (self._board[next_sq_row][self._alph_tuple[next_sq_col]] != ''
                        and f'{self._alph_tuple[next_sq_col]}{next_sq_row}' != place_sq
                ):
                    return False
                # If at the placement square, return True:
                elif f'{self._alph_tuple[next_sq_col]}{next_sq_row}' == place_sq:
                    return True
                # If not at the placement square continue:
                return self.bishop_recursion_helper(next_sq_col, next_sq_row, next_sq_col + 1, next_sq_row - 1, place_sq)

        # Going forward in both columns and rows:
            elif init_sq_row == next_sq_row - 1:
                # If there is a piece in the way of the placement square:
                if (self._board[next_sq_row][self._alph_tuple[next_sq_col]] != ''
                        and f'{self._alph_tuple[next_sq_col]}{next_sq_row}' != place_sq
                ):
                    return False
                # If at the placement square, return True:
                elif f'{self._alph_tuple[next_sq_col]}{next_sq_row}' == place_sq:
                    return True
                # If not at the placement square continue:
                return self.bishop_recursion_helper(next_sq_col, next_sq_row, next_sq_col + 1, next_sq_row + 1, place_sq)


board = ChessVar()
# print(board.get_turn())
# print(board.set_turn())
# print(board.get_game_state())
# print(board.get_turn())
# board.print_board()
# print('Get Piece on Board:', board.get_piece('C8'))

# board.print_board()

# # [PASS] Submission Test #1 - Create game, test pawn moves, game state + turns
#
# # [PASS] Submission Test #2 - Pawn Moves Without Capture
# print('SUB TEST 2 - Pawn Moves Without Capture')
# print('---------------------------------------')
# print(board.make_move('a2', 'a4'))
# print(board.make_move('a7', 'a6'))
# print(board.make_move('a4', 'a5'))
# print(board.make_move('a6', 'a5'))
# print(board.make_move('a6', 'b5'))
# print(board.make_move('a6', 'a6'))
# print(board.make_move('a6', 'a7'))
# print(board.make_move('b7', 'b6'))
#
# # [PASS] Submission Test #3 - Pawn Captures Pawn, No Other Pieces Affected By Explosion
# print('SUB TEST 3 - Pawn Captures Pawn, No Other Pieces Affected By Explosion')
# print('----------------------------------------------------------------------')
# print(board.make_move('a2', 'a4'))
# print(board.make_move('a7', 'a6'))
# print(board.make_move('a4', 'a5'))
# print(board.make_move('b7', 'b6'))
# print(board.make_move('a5', 'b6'))
#
# # [PASS] Submission Test #4 - Pawn captures pawn with explosion removing proper pieces
# print('SUB TEST 4 - Pawn captures pawn with explosion removing proper pieces')
# print('---------------------------------------------------------------------')
# # print(board.make_move('a2', 'a4'))
# # print(board.make_move('g7', 'g5'))
# # print(board.make_move('a4', 'a5'))
# # print(board.make_move('g5', 'g4'))
# # print(board.make_move('a5', 'a6'))
# # print(board.make_move('g4', 'g3'))
# # print(board.make_move('a6', 'b7'))
# #
# # [PASS] Submission Test #5 - Pawn Capture Pawn and Kills King, Game End
# print('SUB TEST 5 - Pawn Capture Pawn and Kills King, Game End')
# print('-------------------------------------------------------')
# print('[1] Game State:', board.get_game_state())
# print(board.make_move('a2', 'a4'))
# print(board.make_move('g7', 'g5'))
# print(board.make_move('a4', 'a5'))
# print(board.make_move('g5', 'g4'))
# print(board.make_move('a5', 'a6'))
# print('[2] Game State:', board.get_game_state())
# print(board.make_move('g4', 'g3'))
# print('[3] Game State:', board.get_game_state())
# print(board.make_move('a6', 'b7'))
# print('[4] Game State:', board.get_game_state())
# print(board.make_move('g3', 'f2'))
# print('[5] Game State:', board.get_game_state())
#
# # [PASS] My Test for Rook:
# print('MY TEST ROOK')
# print('------------')
# print(board.make_move('a2', 'a4'))
# print(board.make_move('h7', 'h5'))
# print(board.make_move('a1', 'a3'))
# print(board.make_move('f7', 'f6'))
# print('PLayer turn:', board.get_turn())
# print(board.make_move('a3', 'e3'))
# print(board.make_move('f6', 'f5'))
# print(board.make_move('e3', 'e5'))
# print(board.make_move('f5', 'f4'))
# print(board.make_move('e5', 'c5'))
# print(board.make_move('g7', 'g5'))
# print(board.make_move('c5', 'c3'))
#
# # [FAIL] Submission Test #6 - Rook + Pawn Movements with Rook Capture
# print('SUB TEST 6 - Rook + Pawn Movements with Rook Capture')
# print('----------------------------------------------------')
# print(board.make_move('a2', 'a4'))
# print(board.make_move('h7', 'h5'))
# # White Move
# print(board.make_move('a1', 'a5'))
# print(board.make_move('a1', 'a3'))
# # Black Move
# print(board.make_move('h8', 'f6'))
# print(board.make_move('h8', 'g6'))
#
# # [] Submission Test #7 - Knight Movement
# print('SUB TEST 7 - Knight Movement')
# print('----------------------------')
# print(board.make_move('b1', 'c3))
# print(board.make_move())
# print(board.make_move())
# print(board.make_move())
# print(board.make_move())
# print(board.make_move())
#
# # [] Submission Test #8 - Bishop Movement with Captures
# print('SUB TEST 8 - Bishop Movement with Captures')
# print('------------------------------------------')
# print(board.make_move('d2', 'd4'))
# print(board.make_move('e7', 'e5'))
# print(board.make_move('c1', 'a3'))
# print(board.make_move('c1', 'h6'))  # RU
# print(board.make_move('f8', 'c5'))  # LD
# print(board.make_move('h6', 'g7'))  # LU
# print(board.make_move('c5', 'd4'))  # RD

#
# # [] Submission Test #9 - Queen Movement with Captures + End of Game
print('SUB TEST 9 - Queen Movement with Captures + End of Game')
print('-------------------------------------------------------')
print(board.make_move('e2', 'e4'))
print(board.make_move('d7', 'd5'))
print(board.make_move('d1', 'd4'))
# print(board.make_move())
# print(board.make_move())
# print(board.make_move())

# # [PASS] Submission Test #10 - King Movement
# print('SUB TEST 10 - King Movement')
# print('---------------------------')
# print(board.make_move('e2', 'e4'))
# print(board.make_move('e7', 'e5'))
# print(board.make_move('e1', 'e3'))
# print(board.make_move('e1', 'f1'))
# print(board.make_move('e1', 'e2'))
# print(board.make_move('e8', 'd7'))
# print(board.make_move('e8', 'e7'))
# print(board.make_move('e2', 'f3'))
# # End their test, start of my test for backwards motion
# print(board.make_move('c7', 'c6'))
# print(board.make_move('f3', 'e1'))
