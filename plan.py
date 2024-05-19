# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS

# 1) Initializing the ChessVar class
#       - Data members:
#           1) game_state - string
#               - state of the game: UNFINISHED, WHITE WON, or BLACK WON

#           2) board - list of dictionaries
#               - each dictionary is a row
#                   - ex: board[0] = {...}
#               - each dictionary will contain the alphabetical columns with their values being either an empty
#               string, or a denoted player and chess piece acronym
#                   - Player + Chess Piece Acronyms:
#                       - White: w
#                       - Black: b
#                       - King: kg
#                       - Queen: q
#                       - Bishop: b
#                       - Knight: kn
#                       - Rook: r
#                       - Pawn: p
#                   - ex: board[3] = {'a': '', 'b': '', 'c': 'w-kn', 'd': '', 'e': 'b-p', 'f': 'w-p', 'g': '',
#                   'h': 'b-b'}

#               3) turn:
#                   - Boolean - True = white turn
# #                           - False = black turn


# 2) Keeping track of turn order
#       - Turn order will be kept track of by a method called set_turn
#           - It will set the turn data member to the opposite boolean
#           - Will be used at the end of the make_move method


# 3) Keeping track of the current board position
#       - In the make_move method, the board will be updated using the 'algebraic notation' for the locations of the
#       chess pieces


# 4) Determining if a regular move is valid
#       - check_playable_move method:
#           1) Check to see if the initial location is part of the current player's chess pieces
#               - True? Cont.
#               - False? return False
#           2) Make the move
#               - Current position = ''
#               - New position = location
#           3) Check to see if explosion occurs
#               - If new location = '' - false
#               - If new location = opposite player's piece - true
#           4) If explosion occurs, check to see if any pieces can be removed
#               - If piece is pawn (player-p): false
#               - Otherwise true
#           5) Remove any pieces that can be removed from explosion
#           6) Update game state
#               - If other player's king is captured, current player wins
#               - Otherwise UNFINISHED
#           7) Update which player's turn it is via set_turn method
#           8) return True


# 5) Determining if a fair piece entering move is valid
#       - method to determine if piece can move to that square
#           - Need to determine what piece is being moved
#           - What moves could be possible
#           - Is the second param in the make_move, one of the possible moves?
#               - True - cont. making_move
#               - False - making_move returns false


# 6) Determining the current state of the game
#       - game_state data member
#       - Updates during make_move method
