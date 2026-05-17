from board import Board

def test_board():
    # Creé este test para probarlo usando "pytest"
    # Es bastante útil para debuggear
    b = Board()
    print(b)
    success = b.from_fen(fen_pos="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print(f"¿FUNCIONO LA IMPORTACION DE FEN rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1?: {success}")
    print(b)
    assert b.bitboards['occupancy'] == 0xFFFF00000000FFFF
    assert b.bitboards['all_white'] == 0x000000000000FFFF
    assert b.bitboards['all_black'] == 0xFFFF000000000000
    assert b.bitboards['white_pawns'] == 0x000000000000FF00
    assert b.bitboards['black_pawns'] == 0x00FF000000000000
    assert b.bitboards['white_knights'] == 0x0000000000000042
    assert b.bitboards['black_knights'] == 0x4200000000000000
    assert b.bitboards['white_bishops'] == 0x0000000000000024
    assert b.bitboards['black_bishops'] == 0x2400000000000000
    assert b.bitboards['white_rooks'] == 0x0000000000000081
    assert b.bitboards['black_rooks'] == 0x8100000000000000
    assert b.bitboards['white_queens'] == 0x0000000000000010
    assert b.bitboards['black_queens'] == 0x1000000000000000
    assert b.bitboards['white_king'] == 0x0000000000000008
    assert b.bitboards['black_king'] == 0x0800000000000000
    assert b.board_state == 30

    from debug import print_board, print_board_state

    print_board(b.bitboards['white_pawns'])
    print()

    b.visualize_board()
    print()

    success = b.from_fen(fen_pos="8/1kB1Rq2/N2r2Q1/b5n1/1p3Q2/2P1q3/3K4/8 b - - 31 121")
    print(f"¿FUNCIONO LA IMPORTACION DE FEN? 8/1kB1Rq2/N2r2Q1/b5n1/1p3Q2/2P1q3/3K4/8 b - - 31 121: {success}")
    b.visualize_board()
    print_board_state(b.board_state)
    print(b)
    print()

    print(b.to_fen())
    assert b.to_fen() == "8/1kB1Rq2/N2r2Q1/b5n1/1p3Q2/2P1q3/3K4/8 b - - 31 121"

    success = b.from_fen(fen_pos="3Pp3/8/8/1K3k2/8/8/8/3P2p1 w - - 0 1")
    print(f"¿FUNCIONO LA IMPORTACION DE FEN 3Pp3/8/8/1K3k2/8/8/8/3P2p1 w - - 0 1?: {success}")
    b.visualize_board()
    print_board_state(b.board_state)
    print()

    print(b.to_fen())
