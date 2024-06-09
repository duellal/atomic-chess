# Author: Alexandria Duell
# GitHub username: duellal
# Date: 6/8/24
# Description: Creates a ChessVar class with methods to play a game of atomic chess. The ChessVar class keeps track
# of the player whose turn it is and the game state.


class ChessVar:
    """
    Initiates the ChessVar class. The ChessVar class has the following methods:
        Public Methods:
            - get_game_state, get_piece, make_move, print_board, get_turn, reset_game
        Private Methods:
            - set_game_state, move_piece, remove_pieces_around_explosion, get_col_num_helper,
            check_pawn_move, check_knight_move, check_bishop_move, bishop_recursion_helper, check_king_move,
            check_rook_move, check_checkmate, and get_king_pos
        Methods for testing:
            - reset_knight_test, reset_rook_test, reset_bishop_test, reset_queen_test, reset_king_test, set_turn (is
            also used in the class as a private method)
    """

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
        self._white_king = 'e1'
        self._black_king = 'e8'

    def get_game_state(self):
        """
        Gets the current game state from three options: UNFINISHED, WHITE_WON, or BLACK_WON.
        :return: string
        """
        return self._game_state

    def __set_game_state(self, player_won):
        """
        Set the game state using one of the three options: UNFINISHED, WHITE_WON, or BLACK_WON. This is a private
        method.
        :param player_won: string - 'w' or 'b' denoting which player won the game
        :return: None
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
        Makes indicated move for the chess piece as long as the following conditions are met:
            - the game has not already been won
            - the initial chess piece to move is the player's chess piece whose turn it currently is
            - the move is legal for that particular piece
            - the move does not go off the board

        If a move can be made the following happens:
            - the chess piece is moved to the indicated square
            - if there is a captured piece, remove any other exploded pieces from the board
            - update the game state if a player has won
            - return True

        If a move cannot be made, the method returns False.

        :param init_sq: string - column and row acronym for the chess piece to move
            - ex: b2
        :param place_sq: string - column and row acronym for the placement of the chess piece.
            - ex: g5
        :return: boolean
        """
        init_col = init_sq[0].lower()
        init_col_num = self.__get_col_num_helper(init_col)
        init_row = int(init_sq[1])

        place_col = place_sq[0].lower()
        place_col_num = self.__get_col_num_helper(place_col)
        place_row = int(place_sq[1])

        # If the row number or column number is not an integer:
        if (isinstance(init_col_num, int) and
                isinstance(place_col_num, int) and
                isinstance(init_row, int) and
                isinstance(place_row, int)):
            pass
        else:
            return False

        # If the indicated move is off of the board:
        if 0 < init_col_num > 8 or 0 < place_col_num > 8:
            return False
        elif 0 < init_row > 8 or 0 < place_row > 8:
            return False

        move_piece = self.get_piece(init_sq)
        place_sq_piece = self.get_piece(place_sq)
        player_turn = self.get_turn()
        move_valid = False

        # Cases to return false:
        # If the square is empty:
        if move_piece == '':
            return False
        # If the chess piece is not the current player's:
        elif player_turn not in move_piece:
            return False
        # Can't capture your own piece:
        elif player_turn in place_sq_piece:
            return False
        # If the game is not unfinished (someone has won):
        elif self.get_game_state() is not self._all_game_states[0]:
            return False

        # If no case for the piece return false, else continue to see if move is legal:
        match move_piece[-1]:
            # Pawn
            case 'p':
                checkmate = self.__check_checkmate(self.__check_pawn_move, init_sq)
                if checkmate is False:
                    move_valid = self.__check_pawn_move(init_sq, place_sq)
                else:
                    return False
            # Bishop
            case 'b':
                checkmate = self.__check_checkmate(self.__check_bishop_move, init_sq)
                if checkmate is False:
                    move_valid = self.__check_bishop_move(init_sq, place_sq)
                else:
                    return False
            # Rook
            case 'r':
                checkmate = self.__check_checkmate(self.__check_rook_move, init_sq)
                if checkmate is False:
                    move_valid = self.__check_rook_move(init_sq, place_sq)
                else:
                    return False
                pass
            # Knight
            case 'n':
                checkmate = self.__check_checkmate(self.__check_knight_move, init_sq)
                if checkmate is False:
                    move_valid = self.__check_knight_move(init_sq, place_sq)
                else:
                    return False
            # Queen
            # Uses bishop + rook movements
            case 'q':
                checkmate_bishop = self.__check_checkmate(self.__check_bishop_move, init_sq)
                checkmate_rook = self.__check_checkmate(self.__check_rook_move, init_sq)

                if checkmate_bishop is False and checkmate_rook is False:
                    bishop_pass = self.__check_bishop_move(init_sq, place_sq)
                    rook_pass = self.__check_rook_move(init_sq, place_sq)

                    if bishop_pass or rook_pass:
                        move_valid = True
                else:
                    return False
            # King
            case 'g':
                move_valid = self.__check_king_move(init_sq, place_sq)
            # No matching pieces to the indicated piece/square is an empty string
            case _:
                return False

        # If move is legal:
        # Remove exploded + captured pieces
        # Move the initial piece to the placement square
        # Set the turn as the next player's
        # Return Boolean (move_valid)
        if move_valid:
            explosion = None
            if move_valid and place_sq_piece:
                explosion = self.__remove_pieces_around_explosion(place_sq)

            self.__move_piece(move_piece, explosion, init_sq, place_sq)
            self.set_turn()
            return move_valid
        # Return false if move is not legal:
        return move_valid

    def print_board(self):
        """
        Prints the current state of the board changing out the acronyms for unicode chess pieces.
        :return: printed rows of lists that are numbered from 9 to 1 (as per the README.md board looks; 9 being the
        columns)
        """
        board_rows = []
        # Adding the unicode chess pieces to the board_rows list to print out a board with chess piece images instead
        # of acronyms
        for row in range(1, len(self._board) + 1):
            row_arr = []
            for col in self._board[row]:
                match self._board[row][col]:
                    case "w-p":
                        row_arr.append('\u2659')
                    case "w-r":
                        row_arr.append('\u2656')
                    case "w-b":
                        row_arr.append('\u2657')
                    case "w-kn":
                        row_arr.append('\u2658')
                    case "w-q":
                        row_arr.append('\u2655')
                    case "w-kg":
                        row_arr.append('\u2654')
                    case "b-p":
                        row_arr.append('\u265F')
                    case "b-r":
                        row_arr.append('\u265C')
                    case "b-b":
                        row_arr.append('\u265D')
                    case "b-kn":
                        row_arr.append('\u265E')
                    case "b-q":
                        row_arr.append('\u265B')
                    case "b-kg":
                        row_arr.append('\u265A')
                    case _:
                        row_arr.append(' ')
            board_rows.append(row_arr)

        col_alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        board_row = 9
        for row in reversed(range(0, len(board_rows) + 1)):
            if board_row == 9:
                print(f'{board_row}: {col_alph}')
            else:
                print(f'{board_row}: {board_rows[row]}')
            board_row -= 1

    def set_turn(self):
        """
        If a player makes a legal move, the method changes the turn. If the move is not legal, the turn stays the
        same. This method is private.
        :return: None
        """
        self._turn = not self._turn

    def get_turn(self):
        """
        Gets the current player's turn by their color acronym ('w' or 'b').
        :return: string
        """
        if self._turn:
            return 'w'
        return 'b'

    def get_piece(self, pos):
        """
        Gets the piece on the board if there is one at the given location. This is not a private method in order to
        test, otherwise it would be.
        :param pos: string - denotes the algebraic notation of the chess board square
            - ex: "C4" or "c4"
        :return: None or string
            - String: the piece acronym at that location or an empty string
                - ex: 'w-p' or ''
        """
        p_row = int(pos[1])
        p_col = pos[0].lower()
        # Actual square at position:
        return self._board[p_row][p_col]

    def __move_piece(self, move_piece, explosion, init_sq, place_sq):
        """
        Changes the location of a chess piece and updates the board accordingly. If a pawn causes the explosion,
        this method makes sure the pawn causing the explosion + the captured pawn are both taken off the board (unlike
        other pawns around the explosion). It updates the kings' location (used in get_king_pos for keeping track of
        the kings for other methods).

        This is a private method.

        :param move_piece:
        :param explosion:
        :param init_sq: string - algebraic notation of the initial square a piece should be at
        :param place_sq: string - algebraic notation of the placement square a piece should move to
        :return: None
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

        # Update king position:
        if 'w-kg' == move_piece:
            self._white_king = f'{place_col}{place_row}'
        elif 'b-kg' == move_piece:
            self._black_king = f'{place_col}{place_row}'

        # Move the piece:
        self._board[init_row][init_col] = ''
        self._board[place_row][place_col] = move_piece

    def __get_col_num_helper(self, col):
        """
        Helper function to get the index number of the column letter.
        :param col: string - column letter
        :return: integer - column index
        """
        # Get the column number as its index (will need in below methods):
        for index, letter in enumerate(self._alph_tuple):
            if letter == col:
                return index

    def __remove_pieces_around_explosion(self, cap_pos):
        """
        Once the make_move method has gone past checking if a piece can make a valid move, it will call this method
        if there is another piece on the placement square, and will execute the explosion.

        This explosion method checks to see if any piece around the capture is a pawn; if the piece is not a pawn,
        it adds it to the explosion pieces and if it is, it does not add it. This method checks if both kings
        are removed from the board, and returns False if true. If the other player's king is captured or exploded in
        the move, this method sets the game state to the player who has won.

        This method is private.

        :param cap_pos: string - algebraic notation of the captured piece's position
        :return: False or an array of exploded pieces around the capture
        """
        cap_col = cap_pos[0].lower()
        # Get the column number as its index (will need in below for loop):
        cap_col_num = self.__get_col_num_helper(cap_col)
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
                    self.__set_game_state('b')
                # If black king is captured, white wins:
                if 'b' in self._board[sq_row][sq_col]:
                    self.__set_game_state('w')
            # Remove all other pieces:
            self._board[sq_row][sq_col] = ''

        return exploded_pieces

    def __check_pawn_move(self, init_sq, place_sq):
        """
        This method checks if the pawn can make a legal move or not.

        It checks if the pawn is in the first position for the players whose piece it is, and allows the pawn to move
        forward 1 or 2 squares on that initial starting square. If the piece is not on the starting square,
        it allows the pawn to move only 1 square forward. If the pawn is capturing another piece, the method checks
        that the capture is diagonally by 1 square.

        This method is private and returns a boolean if the pawn can make the indicated move.

        :param init_sq: string - algebraic notation of the initial square a piece should be at
        :param place_sq: string - algebraic notation of the placement square a piece should move to
        :return: Boolean
        """
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.__get_col_num_helper(init_col)
        col_lower = init_col_num - 2
        col_upper = init_col_num + 2

        # Makes sure that columns for the loops cannot go off or go to the other side of the board:
        if col_lower < -1:
            col_lower = -1
        if col_upper > 8:
            col_upper = 8

        # If pawn is in initial row, pawn can move 1 or 2 squares:
        if init_row == 2:
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
        if init_row == 7:
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
            if self.get_turn() == 'w':
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
            if self.get_turn() == 'b':
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

    def __check_rook_move(self, init_sq, place_sq):
        """
        This method checks if the rook can make a legal move or not.

        It checks if the direction the rook is being placed at is either forward, backward, or side to side and if
        there is an obstruction to the placement square, as the rook cannot move with pieces in the way.

        This method is private and returns a boolean if the rook can make the indicated move.

        :param init_sq: string - algebraic notation of the initial square a piece should be at
        :param place_sq: string - algebraic notation of the placement square a piece should move to
        :return: Boolean
        """
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.__get_col_num_helper(init_col)

        place_row = int(place_sq[1])
        place_col = place_sq[0].lower()
        place_col_num = self.__get_col_num_helper(place_col)

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

    def __check_king_move(self, init_sq, place_sq):
        """
        This method checks if the king can make a legal move or not.

        It checks if the direction the king is being placed is 1 square in any direction around it and if
        there is an obstruction to the placement square, as the king cannot move with pieces in the way.

        This method is private and returns a boolean if the king can make the indicated move.

        :param init_sq: string - algebraic notation of the initial square a piece should be at
        :param place_sq: string - algebraic notation of the placement square a piece should move to
        :return: Boolean
        """
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.__get_col_num_helper(init_col)

        place_row = int(place_sq[1])
        place_col = place_sq[0].lower()

        # King cannot capture other pieces
        if self._board[place_row][place_col] != '':
            return False

        # If placement square is within 1 square reach of the king:
        for row in range(init_row - 1, init_row + 2):
            for col in range(init_col_num - 1, init_col_num + 2):
                if place_sq == f'{self._alph_tuple[col]}{row}':
                    return True
        # Else return False (catch all)
        return False

    def __check_knight_move(self, init_sq, place_sq):
        """
        This method checks if the knight can make a legal move or not.

        It checks if the direction the knight is being placed at is in a "L" shape from it's starting square. The
        knight can move past other pieces on the board, and it is not checked in this method.

        This method is private and returns a boolean if the knight can make the indicated move.

        :param init_sq: string - algebraic notation of the initial square a piece should be at
        :param place_sq: string - algebraic notation of the placement square a piece should move to
        :return: Boolean
        """
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.__get_col_num_helper(init_col)

        place_row = int(place_sq[1])
        place_col = place_sq[0].lower()
        place_col_num = self.__get_col_num_helper(place_col)

        # Top + Bottom: col +- 1 and row either + 2 or -2
        # Top + Bottom Row:
        if abs(init_row - place_row) == 2:
            # Left + Right Col:
            if abs(init_col_num - place_col_num) == 1:
                return True
            else:
                return False

        # Left + Right: col either + 2 or -2 and row +- 1
        # Left + Right Col:
        elif abs(init_col_num - place_col_num) == 2:
            # Top + Bottom Row
            if abs(init_row - place_row) == 1:
                return True
            else:
                return False
        else:
            return False

    def __check_bishop_move(self, init_sq, place_sq):
        """
        This method checks if the bishop can make a legal move or not.

        It checks if the direction the bishop is being placed at is in a diagonal and if
        there is an obstruction to the placement square, as the bishop cannot move with pieces in the way.

        This method is private and returns a boolean if the bishop can make the indicated move.

        :param init_sq: string - algebraic notation of the initial square a piece should be at
        :param place_sq: string - algebraic notation of the placement square a piece should move to
        :return: Boolean
        """
        init_row = int(init_sq[1])
        init_col = init_sq[0].lower()
        init_col_num = self.__get_col_num_helper(init_col)

        place_row = int(place_sq[1])
        place_col = place_sq[0].lower()
        place_col_num = self.__get_col_num_helper(place_col)

        # Diagonal Up - Increase Row, Increase Col (Left Up):
        if init_row < place_row:
            if init_col_num < place_col_num:
                return self.__bishop_recursion_helper(init_col_num, init_row, init_col_num + 1, init_row + 1, place_sq)
            # Increase Row, Decrease Col (Right Up):
            elif init_col_num > place_col_num:
                return self.__bishop_recursion_helper(init_col_num, init_row, init_col_num - 1, init_row + 1, place_sq)
            # Col is the same:
            else:
                return False

        # Diagonal Down - Decrease row, Decrease Col (Left Down):
        elif init_row > place_row:
            if init_col_num < place_col_num:
                return self.__bishop_recursion_helper(init_col_num, init_row, init_col_num + 1, init_row - 1, place_sq)
            # Decrease Row, Increase Col (Right Down):
            elif init_col_num > place_col_num:
                return self.__bishop_recursion_helper(init_col_num, init_row, init_col_num - 1, init_row - 1, place_sq)
            # Col is the same:
            else:
                return False
        # Row is the same as the initial square:
        return False

    def __bishop_recursion_helper(self, init_sq_col_num, init_sq_row, next_sq_col_num, next_sq_row, place_sq):
        """
        This method is a helper function to check if the bishop can go to the placement square or not.

        :param init_sq_col_num: integer - the index integer associated with the column letter of the initial square
        :param init_sq_row: integer - the index integer associated with the initial square's row :param
        next_sq_col_num:integer - the index integer associated with the column letter of the next square being
        evaluated
        :param next_sq_row: integer - the index integer associated with the next square's row that is being
        evaluated
        :param place_sq: string - algebraic notation associated with the placement square of the move
        :return: boolean or recurs the method
        """
        # Going back in columns + rows:
        if next_sq_col_num + 1 == init_sq_col_num:
            if next_sq_row + 1 == init_sq_row:
                # If there is a piece in the way of the placement square:
                if (self._board[next_sq_row][self._alph_tuple[next_sq_col_num]] != ''
                        and f'{self._alph_tuple[next_sq_col_num]}{next_sq_row}' != place_sq):
                    return False
                # If at the placement square, return True:
                elif f'{self._alph_tuple[next_sq_col_num]}{next_sq_row}' == place_sq:
                    return True
                elif next_sq_col_num - 1 < 0 or next_sq_row - 1 < 0:
                    return False
                # If not at the placement square continue:
                return self.__bishop_recursion_helper(next_sq_col_num, next_sq_row, next_sq_col_num - 1,
                                                      next_sq_row - 1,
                                                      place_sq)

            # Going back in columns, going forward in rows:
            elif init_sq_row == next_sq_row - 1:
                # If there is a piece in the way of the placement square:
                if (self._board[next_sq_row][self._alph_tuple[next_sq_col_num]] != ''
                        and f'{self._alph_tuple[next_sq_col_num]}{next_sq_row}' != place_sq):
                    return False
                # If at the placement square, return True:
                elif f'{self._alph_tuple[next_sq_col_num]}{next_sq_row}' == place_sq:
                    return True
                elif next_sq_col_num - 1 < 0 or next_sq_row + 1 > 8:
                    return False
                # If not at the placement square continue:
                return self.__bishop_recursion_helper(next_sq_col_num, next_sq_row, next_sq_col_num - 1,
                                                      next_sq_row + 1,
                                                      place_sq)

        # Going forward in columns, going backward in rows:
        if init_sq_col_num == next_sq_col_num - 1:
            if next_sq_row + 1 == init_sq_row:
                # If there is a piece in the way of the placement square:
                if (self._board[next_sq_row][self._alph_tuple[next_sq_col_num]] != ''
                        and f'{self._alph_tuple[next_sq_col_num]}{next_sq_row}' != place_sq
                ):
                    return False
                # If at the placement square, return True:
                elif f'{self._alph_tuple[next_sq_col_num]}{next_sq_row}' == place_sq:
                    return True
                elif next_sq_row - 1 < 0 or next_sq_col_num + 1 > 7:
                    return False
                # If not at the placement square continue:
                return self.__bishop_recursion_helper(next_sq_col_num, next_sq_row, next_sq_col_num + 1,
                                                      next_sq_row - 1,
                                                      place_sq)

            # Going forward in both columns and rows:
            elif init_sq_row == next_sq_row - 1:
                # If there is a piece in the way of the placement square:
                if (self._board[next_sq_row][self._alph_tuple[next_sq_col_num]] != ''
                        and f'{self._alph_tuple[next_sq_col_num]}{next_sq_row}' != place_sq
                ):
                    return False
                # If at the placement square, return True:
                elif f'{self._alph_tuple[next_sq_col_num]}{next_sq_row}' == place_sq:
                    return True
                elif next_sq_col_num + 1 > 7 or 8 < next_sq_row + 1:
                    return False
                # If not at the placement square continue:
                return self.__bishop_recursion_helper(next_sq_col_num, next_sq_row, next_sq_col_num + 1,
                                                      next_sq_row + 1,
                                                      place_sq)

    def __check_checkmate(self, check_next_piece_move, piece_pos):
        """
        Checks if the piece's next move will capture the king.

        This is a private method.

        :param check_next_piece_move: private method for the piece being checked
        :param piece_pos: string - algebraic notation for the position of the piece being checked
        :return: Boolean
        """
        no_checkmate = False
        checkmate = True

        if self.get_turn() == 'w':
            king_pos = self._black_king

            if check_next_piece_move(piece_pos, king_pos) is True:
                return checkmate
            else:
                return no_checkmate
        else:
            king_pos = self._white_king
            if check_next_piece_move(piece_pos, king_pos) is True:
                return checkmate
            else:
                return no_checkmate

    def __get_king_pos(self, player_turn):
        """
        Gets the current king's position for the current player.

        This is a private method.

        :param player_turn: string - 'w' or 'b'
        :return: string - algebraic notation of the current player's king.
        """
        if player_turn == 'w':
            return self._white_king
        else:
            return self._black_king

    def reset_game(self):
        """
        Resets the game when called. Game state, player turn, and game board are all reset to initial instances.
        :return: None
        """
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
        self._white_king = 'e1'
        self._black_king = 'e8'

    def reset_knight_test(self):
        """
        Resets the game to put the black knight to be in the middle of the board. Every other instance is reset to
        initial instances. For testing purposes only.
        :return: None
        """
        self._game_state = self._all_game_states[0]
        self._board = {
            1: {'a': 'w-r', 'b': 'w-kn', 'c': 'w-b', 'd': 'w-q', 'e': 'w-kg', 'f': 'w-b', 'g': 'w-kn', 'h': 'w-r'},
            2: {'a': 'w-p', 'b': 'w-p', 'c': 'w-p', 'd': 'w-p', 'e': 'w-p', 'f': 'w-p', 'g': 'w-p', 'h': 'w-p'},
            3: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            4: {'a': '', 'b': '', 'c': '', 'd': '', 'e': 'b-kn', 'f': '', 'g': '', 'h': ''},
            5: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            6: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            7: {'a': 'b-p', 'b': 'b-p', 'c': 'b-p', 'd': 'b-p', 'e': 'b-p', 'f': 'b-p', 'g': 'b-p', 'h': 'b-p'},
            8: {'a': 'b-r', 'b': '', 'c': 'b-b', 'd': 'b-q', 'e': 'b-kg', 'f': 'b-b', 'g': 'b-kn', 'h': 'b-r'}
            }
        self._turn = True
        self._white_king = 'e1'
        self._black_king = 'e8'

    def reset_rook_test(self):
        """
        Resets the game to put the black rook to be in the middle of the board. Every other instance is reset to
        initial instances. For testing purposes only.
        :return: None
        """
        self._game_state = self._all_game_states[0]
        self._board = {
            1: {'a': 'w-r', 'b': 'w-kn', 'c': 'w-b', 'd': 'w-q', 'e': 'w-kg', 'f': 'w-b', 'g': 'w-kn', 'h': 'w-r'},
            2: {'a': 'w-p', 'b': 'w-p', 'c': 'w-p', 'd': 'w-p', 'e': 'w-p', 'f': 'w-p', 'g': 'w-p', 'h': 'w-p'},
            3: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            4: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            5: {'a': '', 'b': '', 'c': '', 'd': 'b-r', 'e': '', 'f': '', 'g': '', 'h': ''},
            6: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            7: {'a': 'b-p', 'b': 'b-p', 'c': 'b-p', 'd': 'b-p', 'e': 'b-p', 'f': 'b-p', 'g': 'b-p', 'h': 'b-p'},
            8: {'a': '', 'b': 'b-kn', 'c': 'b-b', 'd': 'b-q', 'e': 'b-kg', 'f': 'b-b', 'g': 'b-kn', 'h': 'b-r'}
            }
        self._turn = True
        self._white_king = 'e1'
        self._black_king = 'e8'

    def reset_bishop_test(self):
        """
        Resets the game to put the black bishop to be in the middle of the board. Every other instance is reset to
        initial instances. For testing purposes only.
        :return: None
        """
        self._game_state = self._all_game_states[0]
        self._board = {
            1: {'a': 'w-r', 'b': 'w-kn', 'c': 'w-b', 'd': 'w-q', 'e': 'w-kg', 'f': 'w-b', 'g': 'w-kn', 'h': 'w-r'},
            2: {'a': 'w-p', 'b': 'w-p', 'c': 'w-p', 'd': 'w-p', 'e': 'w-p', 'f': 'w-p', 'g': 'w-p', 'h': 'w-p'},
            3: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            4: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            5: {'a': '', 'b': '', 'c': '', 'd': 'b-b', 'e': '', 'f': '', 'g': '', 'h': ''},
            6: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            7: {'a': 'b-p', 'b': 'b-p', 'c': 'b-p', 'd': 'b-p', 'e': 'b-p', 'f': 'b-p', 'g': 'b-p', 'h': 'b-p'},
            8: {'a': 'b-r', 'b': 'b-kn', 'c': '', 'd': 'b-q', 'e': 'b-kg', 'f': 'b-b', 'g': 'b-kn', 'h': 'b-r'}
            }
        self._turn = True
        self._white_king = 'e1'
        self._black_king = 'e8'

    def reset_queen_test(self):
        """
        Resets the game to put the black queen to be in the middle of the board. Every other instance is reset to
        initial instances. For testing purposes only.
        :return: None
        """
        self._game_state = self._all_game_states[0]
        self._board = {
            1: {'a': 'w-r', 'b': 'w-kn', 'c': 'w-b', 'd': 'w-q', 'e': 'w-kg', 'f': 'w-b', 'g': 'w-kn', 'h': 'w-r'},
            2: {'a': 'w-p', 'b': 'w-p', 'c': 'w-p', 'd': 'w-p', 'e': 'w-p', 'f': 'w-p', 'g': 'w-p', 'h': 'w-p'},
            3: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            4: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            5: {'a': '', 'b': '', 'c': '', 'd': 'b-q', 'e': '', 'f': '', 'g': '', 'h': ''},
            6: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            7: {'a': 'b-p', 'b': 'b-p', 'c': 'b-p', 'd': 'b-p', 'e': 'b-p', 'f': 'b-p', 'g': 'b-p', 'h': 'b-p'},
            8: {'a': 'b-r', 'b': 'b-kn', 'c': 'b-b', 'd': '', 'e': 'b-kg', 'f': 'b-b', 'g': 'b-kn', 'h': 'b-r'}
            }
        self._turn = True
        self._white_king = 'e1'
        self._black_king = 'e8'

    def reset_king_test(self):
        """
        Resets the game to put the black king to be in the middle of the board. Every other instance is reset to
        initial instances. For testing purposes only.
        :return: None
        """
        self._game_state = self._all_game_states[0]
        self._board = {
            1: {'a': 'w-r', 'b': 'w-kn', 'c': 'w-b', 'd': 'w-q', 'e': 'w-kg', 'f': 'w-b', 'g': 'w-kn', 'h': 'w-r'},
            2: {'a': 'w-p', 'b': 'w-p', 'c': 'w-p', 'd': 'w-p', 'e': 'w-p', 'f': 'w-p', 'g': 'w-p', 'h': 'w-p'},
            3: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            4: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            5: {'a': '', 'b': '', 'c': '', 'd': 'b-kg', 'e': '', 'f': '', 'g': '', 'h': ''},
            6: {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''},
            7: {'a': 'b-p', 'b': 'b-p', 'c': 'b-p', 'd': 'b-p', 'e': 'b-p', 'f': 'b-p', 'g': 'b-p', 'h': 'b-p'},
            8: {'a': 'b-r', 'b': 'b-kn', 'c': 'b-b', 'd': 'b-q', 'e': '', 'f': 'b-b', 'g': 'b-kn', 'h': 'b-r'}
            }
        self._turn = True
        self._white_king = 'e1'
        self._black_king = 'e8'
