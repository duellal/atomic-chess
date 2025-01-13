import unittest
from ChessVar import ChessVar


def chess_notation_to_index(notation):
    column = ord(notation[0]) - ord('a')
    row = 8 - int(notation[1])
    return (row, column)


def index_to_chess_notation(index):
    column = chr(index[1] + ord('a'))
    row = 8 - index[0]
    return f"{column}{row}"


class TestAtomicChess(unittest.TestCase):
    def setUp(self):
        self.chess = ChessVar()
        # Reset board method is assumed to be part of initialization

    def test_initial_setup(self):
        self.assertEqual(self.chess.get_piece('a8'), 'b-r')
        self.assertEqual(self.chess.get_piece('b8'), 'b-kn')
        self.assertEqual(self.chess.get_piece('c8'), 'b-b')
        self.assertEqual(self.chess.get_piece('d8'), 'b-q')
        self.assertEqual(self.chess.get_piece('e8'), 'b-kg')
        self.assertEqual(self.chess.get_piece('f8'), 'b-b')
        self.assertEqual(self.chess.get_piece('g8'), 'b-kn')
        self.assertEqual(self.chess.get_piece('h8'), 'b-r')
        for i in range(8):
            self.assertEqual(self.chess.get_piece(f'{chr(ord("a") + i)}7'), 'b-p')
            self.assertEqual(self.chess.get_piece(f'{chr(ord("a") + i)}2'), 'w-p')
        self.assertEqual(self.chess.get_piece('a1'), 'w-r')
        self.assertEqual(self.chess.get_piece('b1'), 'w-kn')
        self.assertEqual(self.chess.get_piece('c1'), 'w-b')
        self.assertEqual(self.chess.get_piece('d1'), 'w-q')
        self.assertEqual(self.chess.get_piece('e1'), 'w-kg')
        self.assertEqual(self.chess.get_piece('f1'), 'w-b')
        self.assertEqual(self.chess.get_piece('g1'), 'w-kn')
        self.assertEqual(self.chess.get_piece('h1'), 'w-r')

    def test_pawn_moves(self):
        # White pawn moves
        self.assertEqual(self.chess.get_turn(), 'w')
        self.assertTrue(self.chess.make_move("e2", "e3"))  # Single move from starting position
        self.assertEqual(self.chess.get_piece('e3'), 'w-p')
        self.assertEqual(self.chess.get_piece('e2'), '')
        self.assertEqual(self.chess.get_turn(), 'b')

        self.assertTrue(self.chess.make_move("d7", "d6"))  # Clearing the path for double move
        self.assertTrue(self.chess.make_move("e4", "e6"))  # Double move from starting position
        self.assertEqual(self.chess.get_piece('e6'), 'w-p')
        self.assertEqual(self.chess.get_piece('e4'), '')
        self.assertEqual(self.chess.get_turn(), 'b')

        self.assertTrue(self.chess.make_move("e3", "e4"))  # Another single move
        self.assertEqual(self.chess.get_piece('e4'), 'w-p')
        self.assertEqual(self.chess.get_piece('e3'), '')
        self.assertEqual(self.chess.get_turn(), 'b')


        # Black pawn moves
        self.assertEqual(self.chess.get_turn(), 'w')
        self.assertTrue(self.chess.make_move("a7", "a5"))  # Single move from starting position
        self.assertEqual(self.chess.get_piece('a5'), 'b-p')
        self.assertEqual(self.chess.get_piece('a7'), '')
        self.assertEqual(self.chess.get_turn(), 'w')  # Ensure turn didn't change if the previous move was invalid
        self.assertFalse(self.chess.make_move("a5", "a4"))  # Attempting to move out of turn
        self.assertEqual(self.chess.get_piece('a5'), 'b-p')
        self.assertEqual(self.chess.get_piece('a4'), '')
        self.assertEqual(self.chess.get_turn(), 'w')  # Ensure turn didn't change if the previous move was invalid

        self.assertTrue(self.chess.make_move("b2", "b3"))  # Clearing the path for double move
        self.assertTrue(self.chess.make_move("a5", "a4"))  # Single move from starting position
        self.assertEqual(self.chess.get_piece('a4'), 'b-p')
        self.assertEqual(self.chess.get_piece('a5'), '')
        self.assertEqual(self.chess.get_turn(), 'w')

    def test_knight_moves(self):
        # White knight moves
        self.chess.make_move("g1", "f3")  # Knight to f3
        self.assertEqual(self.chess.get_piece('f3'), 'w-kn')
        self.assertEqual(self.chess.get_piece('g1'), '')

        self.chess.make_move("f3", "d4")  # Knight to d4
        self.assertEqual(self.chess.get_piece('d4'), 'w-kn')
        self.assertEqual(self.chess.get_piece('f3'), '')

        # Black knight moves
        self.chess.make_move("b8", "c6")  # Knight to c6
        self.assertEqual(self.chess.get_piece('c6'), 'b-kn')
        self.assertEqual(self.chess.get_piece('b8'), '')

        self.chess.make_move("c6", "e5")  # Knight to e5
        self.assertEqual(self.chess.get_piece('e5'), 'b-kn')
        self.assertEqual(self.chess.get_piece('c6'), '')

    def test_bishop_moves(self):
        # White bishop moves
        self.chess.make_move("f1", "c4")  # Bishop to c4
        self.assertEqual(self.chess.get_piece('c4'), 'w-b')
        self.assertEqual(self.chess.get_piece('f1'), '')

        self.chess.make_move("c4", "d5")  # Bishop to d5
        self.assertEqual(self.chess.get_piece('d5'), 'w-b')
        self.assertEqual(self.chess.get_piece('c4'), '')

        # Black bishop moves
        self.chess.make_move("c8", "h3")  # Bishop to h3
        self.assertEqual(self.chess.get_piece('h3'), 'b-b')
        self.assertEqual(self.chess.get_piece('c8'), '')

        self.chess.make_move("h3", "f1")  # Bishop to f1
        self.assertEqual(self.chess.get_piece('f1'), 'b-b')
        self.assertEqual(self.chess.get_piece('h3'), '')

    def test_rook_moves(self):
        # White rook moves
        self.chess.make_move("h1", "h3")  # Rook to h3
        self.assertEqual(self.chess.get_piece('h3'), 'w-r')
        self.assertEqual(self.chess.get_piece('h1'), '')

        self.chess.make_move("h3", "a3")  # Rook to a3
        self.assertEqual(self.chess.get_piece('a3'), 'w-r')
        self.assertEqual(self.chess.get_piece('h3'), '')

        # Black rook moves
        self.chess.make_move("a8", "a6")  # Rook to a6
        self.assertEqual(self.chess.get_piece('a6'), 'b-r')
        self.assertEqual(self.chess.get_piece('a8'), '')

        self.chess.make_move("a6", "h6")  # Rook to h6
        self.assertEqual(self.chess.get_piece('h6'), 'b-r')
        self.assertEqual(self.chess.get_piece('a6'), '')

    def test_queen_moves(self):
        # White queen moves
        self.chess.make_move("d1", "d3")  # Queen to d3
        self.assertEqual(self.chess.get_piece('d3'), 'w-q')
        self.assertEqual(self.chess.get_piece('d1'), '')

        self.chess.make_move("d3", "a3")  # Queen to a3
        self.assertEqual(self.chess.get_piece('a3'), 'w-q')
        self.assertEqual(self.chess.get_piece('d3'), '')

        # Black queen moves
        self.chess.make_move("d8", "d6")  # Queen to d6
        self.assertEqual(self.chess.get_piece('d6'), 'b-q')
        self.assertEqual(self.chess.get_piece('d8'), '')

        self.chess.make_move("d6", "h6")  # Queen to h6
        self.assertEqual(self.chess.get_piece('h6'), 'b-q')
        self.assertEqual(self.chess.get_piece('d6'), '')

    def test_king_moves(self):
        # White king moves
        self.chess.make_move("e1", "e2")  # King to e2
        self.assertEqual(self.chess.get_piece('e2'), 'w-kg')
        self.assertEqual(self.chess.get_piece('e1'), '')

        self.chess.make_move("e2", "d3")  # King to d3
        self.assertEqual(self.chess.get_piece('d3'), 'w-kg')
        self.assertEqual(self.chess.get_piece('e2'), '')

        # Black king moves
        self.chess.make_move("e8", "f7")  # King to f7
        self.assertEqual(self.chess.get_piece('f7'), 'b-kg')
        self.assertEqual(self.chess.get_piece('e8'), '')

        self.chess.make_move("f7", "g6")  # King to g6
        self.assertEqual(self.chess.get_piece('g6'), 'b-kg')
        self.assertEqual(self.chess.get_piece('f7'), '')

    def test_atomic_explosion(self):
        self.chess.make_move("e2", "e4")
        self.chess.make_move("d7", "d5")
        self.chess.make_move("e4", "d5")
        self.assertEqual(self.chess.get_piece('d5'), '')  # Capturing piece is removed
        # Additional logic needed to handle explosion correctly
        self.assertEqual(self.chess.get_piece('c5'), '')  # Piece to the left is removed
        self.assertEqual(self.chess.get_piece('e5'), '')  # Piece to the right is removed
        self.assertEqual(self.chess.get_piece('d6'), '')  # Piece above is removed

    def test_king_cannot_move_into_check(self):
        self.chess.make_move("f2", "f3")
        self.chess.make_move("e7", "e5")
        self.chess.print_board()
        self.chess.make_move("g1", "f3")
        self.chess.make_move("d8", "h4")
        self.chess.print_board()
        self.assertFalse(self.chess.make_move("e1", "e2"))  # King cannot move to e2 into check

    def test_checkmate(self):
        self.chess.make_move("f2", "f3")
        self.chess.make_move("e7", "e5")
        self.chess.make_move("g1", "f3")
        self.chess.make_move("d8", "h4")
        self.assertFalse(self.chess.make_move("e1", "e2"))

    def test_turn_alternation(self):
        self.assertEqual(self.chess.get_turn(), 'w')
        self.chess.make_move("e2", "e4")
        self.assertEqual(self.chess.get_turn(), 'b')
        self.chess.make_move("e7", "e5")
        self.assertEqual(self.chess.get_turn(), 'w')


if __name__ == '__main__':
    unittest.main()
