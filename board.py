from dataclasses import dataclass, field
from collections import deque
import re

@dataclass(slots=True)
class Board:
    # Posición cargada en formato FEN
    fen: str = ''

    # Bitboards de piezas
    white_pawns: int = 0
    white_knights: int = 0
    white_bishops: int = 0
    white_rooks: int = 0
    white_queens: int = 0
    white_king: int = 0
    black_pawns: int = 0
    black_knights: int = 0
    black_bishops: int = 0
    black_rooks: int = 0
    black_queens: int = 0
    black_king: int = 0
    # Bitboards condensados
    all_white: int = 0
    all_black: int = 0
    occupancy: int = 0

    # Estado de la partida. Formato board_state:
    # Bit 0: Turno (0 = blancas, 1 = negras)
    # Bits 1-4: Derechos de enroque (KQkq, 1 = puede, 0 = no puede)
    # Bits 5-10: Casilla de en passant (0-63, 0 = ninguna)
    # Bits 11-16: Halfmove clock (0-50)
    board_state: int = 0
    fullmove_number: int = 0

    # Historial de estados (para make_move()/unmake_move())
    # **ES UN STACK**
    # En el mismo formato de board_state
    board_state_history: deque[int] = field(default_factory=deque)

    def __post_init__(self) -> None:
        '''Carga la posición FEN de `self.fen` luego de `__init__`.'''
        self.from_fen()

    def from_fen(self, fen_pos: str = '') -> bool:
        '''Carga la posición de `self.fen` o, si existe, `fen_pos`.\n
        `fen_pos` debe estar en formato FEN.\n
        Retorna `True` si fue exitoso y `False` en caso contrario.\n
        En caso de ser exitoso, guarda `fen_pos` en `self.fen`.'''

        fen = fen_pos if fen_pos else self.fen
        if not self.check_fen_format(fen): return False

        self.reset_bitboards()

        (pieces, turn, fen_castling_rights,
        en_passant_square, halfmove_clock,
        fullmove_number) = fen.strip().split()
        castling_rights = 0
        if "q" in fen_castling_rights:
            castling_rights |= 1
        if "k" in fen_castling_rights:
            castling_rights |= 1 << 1
        if "Q" in fen_castling_rights:
            castling_rights |= 1 << 2
        if "K" in fen_castling_rights:
            castling_rights |= 1 << 3

        self.board_state_history = deque()
        self.fullmove_number = int(fullmove_number)
        turn = 0 if turn == "w" else 1
        en_passant_square = 0 if en_passant_square == "-" \
                              else self.square_to_index(en_passant_square)
        self.board_state = (turn |
                            castling_rights << 1 |
                            en_passant_square << 5 |
                            int(halfmove_clock) << 11)

        square = 63
        for el in pieces:
            # Recorremos cada elemento del tablero del FEN
            # Si encontramos algo lo modificamos en el bitboard respectivo

            if el.isnumeric():
                square -= int(el)
            else:
                if el in "pP":
                    if el.isupper():
                        self.white_pawns |= 1 << square
                    else:
                        self.black_pawns |= 1 << square
                elif el in "nN":
                    if el.isupper():
                        self.white_knights |= 1 << square
                    else:
                        self.black_knights |= 1 << square
                elif el in "bB":
                    if el.isupper():
                        self.white_bishops |= 1 << square
                    else:
                        self.black_bishops |= 1 << square
                elif el in "rR":
                    if el.isupper():
                        self.white_rooks |= 1 << square
                    else:
                        self.black_rooks |= 1 << square
                elif el in "qQ":
                    if el.isupper():
                        self.white_queens |= 1 << square
                    else:
                        self.black_queens |= 1 << square
                elif el in "kK":
                    if el.isupper():
                        self.white_king |= 1 << square
                    else:
                        self.black_king |= 1 << square
                if el != "/":
                    square -= 1

        self.update_occupancy()
        self.fen = fen

        return True

    def square_to_index(self, square: str) -> int:
        '''Transforma el nombre de una casilla a su índice.
        
        Ej. `"e4"` -> `27`.
        Retorna `-1` en caso de error.'''

        if (len(square) != 2 or type(square) != str
            or square[0] not in "abcdefgh" or square[1] not in "12345678"):
            return -1
        
        return int(square[1]) * 8 - "abcdefgh".index(square[0]) - 1
    
    def index_to_square(self, index: int) -> str | None:
        '''Transforma el índice de una casilla a su nombre.
        
        Ej. `27` -> `"e4"`.
        Retorna `None` en caso de error.'''

        if (type(index) != int or index < 0 or index > 63):
            return None
        
        return ("abcdefgh"[::-1])[index % 8] + str(index // 8 + 1)

    def check_fen_format(self, fen: str) -> bool:
        '''Retorna `True` si el string el cumple formato FEN
           y `False` en caso contrario.'''
        fen_regex = r"^([pnbrqkPNBRQK1-8]{1,8}/){7}" \
                    r"[pnbrqkPNBRQK1-8]{1,8}" \
                    r"\s+(w|b)\s+(-|[KQkq]{1,4})" \
                    r"\s+(-|[a-h][1-8])\s+(\d+)\s+(\d+)$"

        if not re.match(fen_regex, fen):
            return False
        
        if ("p" in fen.split()[0].split("/")[0].lower() or
            "p" in fen.split()[0].split("/")[7].lower()):
            return False
        
        k = 0
        K = 0
        n_squares = 0
        for c in fen.split()[0]:
            if c in "pnbrqkPNBRQK":
                if c == "k":
                    k += 1
                if c == "K":
                    K += 1
                n_squares += 1
            if c.isnumeric():
                n_squares += int(c)
        
        if n_squares != 64 or k != 1 or K != 1:
            return False

        return True
    
    def reset_bitboards(self) -> None:
        '''Settea todos los bitboards del tablero a `0`.'''

        self.white_pawns = 0
        self.white_knights = 0
        self.white_bishops = 0
        self.white_rooks = 0
        self.white_queens = 0
        self.white_king = 0
        self.black_pawns = 0
        self.black_knights = 0
        self.black_bishops = 0
        self.black_rooks = 0
        self.black_queens = 0
        self.black_king = 0

        self.all_white = 0
        self.all_black = 0
        self.occupancy = 0
    
    def to_fen(self) -> str:
        '''Transforma la posición actual a formato FEN y la retorna.'''

        fen = ""

        # Piezas
        contador = 0
        for sq in range(63, -1, -1):
            if not self.occupancy & (1 << sq):
                contador += 1
            else:
                if contador != 0:
                    fen += str(contador)
                contador = 0
                if (self.white_pawns & (1 << sq)):
                    fen += "P"
                elif (self.white_knights & (1 << sq)):
                    fen += "N"
                elif (self.white_bishops & (1 << sq)):
                    fen += "B"
                elif (self.white_rooks & (1 << sq)):
                    fen += "R"
                elif (self.white_queens & (1 << sq)):
                    fen += "Q"
                elif (self.white_king & (1 << sq)):
                    fen += "K"
                elif (self.black_pawns & (1 << sq)):
                    fen += "p"
                elif (self.black_knights & (1 << sq)):
                    fen += "n"
                elif (self.black_bishops & (1 << sq)):
                    fen += "b"
                elif (self.black_rooks & (1 << sq)):
                    fen += "r"
                elif (self.black_queens & (1 << sq)):
                    fen += "q"
                elif (self.black_king & (1 << sq)):
                    fen += "k"
            
            if sq != 0 and sq % 8 == 0:
                if contador != 0:
                    fen += str(contador)
                contador = 0
                fen += "/"
            if sq == 0:
                if contador != 0:
                    fen += str(contador)
                contador = 0
                fen += " "
        
        # Turno
        fen += "b" if self.board_state & 1 else "w"
        fen += " "

        # Enroque
        K = self.board_state & 1 << 1
        Q = self.board_state & 1 << 2
        k = self.board_state & 1 << 3
        q = self.board_state & 1 << 4
        if not (K or Q or k or q):
            fen += "-"
        else:
            if K:
                fen += "K"
            if Q:
                fen += "Q"
            if k:
                fen += "k"
            if q:
                fen += "q"
        fen += " "

        # En passant
        en_passant_sq = self.board_state >> 5 & ((1 << 6) - 1)
        if en_passant_sq == 0:
            fen += "-"
        else:
            fen += self.index_to_square(en_passant_sq)
        fen += " "

        # Halfmove clock
        halfmove_clock = self.board_state >> 11 & ((1 << 6) - 1)
        fen += str(halfmove_clock)
        fen += " "

        # Fullmove number
        fen += str(self.fullmove_number)

        return fen
    
    def update_occupancy(self) -> None:
        '''Actualiza `all_white`, `all_black` y `occupancy`.'''

        self.all_white = (self.white_pawns   | self.white_knights
                        | self.white_bishops | self.white_rooks
                        | self.white_queens  | self.white_king)
        self.all_black = (self.black_pawns   | self.black_knights
                        | self.black_bishops | self.black_rooks
                        | self.black_queens  | self.black_king)
        self.occupancy = self.all_white | self.all_black

    def visualize_board(self) -> None:
        '''Imprime el estado de `Board` en un formato amigable.'''

        print('    A B C D E F G H')

        square = 63
        for rank in range(8):
            row = ""

            while square >= (8 - (rank + 1)) * 8:
                if self.white_pawns & (1 << square):
                    row += "♙"
                elif self.white_knights & (1 << square):
                    row += "♘"
                elif self.white_bishops & (1 << square):
                    row += "♗"
                elif self.white_rooks & (1 << square):
                    row += "♖"
                elif self.white_queens & (1 << square):
                    row += "♕"
                elif self.white_king & (1 << square):
                    row += "♔"
                elif self.black_pawns & (1 << square):
                    row += "♟"
                elif self.black_knights & (1 << square):
                    row += "♞"
                elif self.black_bishops & (1 << square):
                    row += "♝"
                elif self.black_rooks & (1 << square):
                    row += "♜"
                elif self.black_queens & (1 << square):
                    row += "♛"
                elif self.black_king & (1 << square):
                    row += "♚"
                else:
                    row += "-"
                
                square -= 1

            print(8 - rank, '|', ' '.join(row))      

def test_board():
    # Creé este test para probarlo usando "pytest"
    # Es bastante útil para debuggear
    b = Board()
    print(b)
    success = b.from_fen(fen_pos="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print(f"¿FUNCIONO LA IMPORTACION DE FEN rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1?: {success}")
    print(b)
    assert b.occupancy == 0xFFFF00000000FFFF
    assert b.all_white == 0x000000000000FFFF
    assert b.all_black == 0xFFFF000000000000
    assert b.white_pawns == 0x000000000000FF00
    assert b.black_pawns == 0x00FF000000000000
    assert b.white_knights == 0x0000000000000042
    assert b.black_knights == 0x4200000000000000
    assert b.white_bishops == 0x0000000000000024
    assert b.black_bishops == 0x2400000000000000
    assert b.white_rooks == 0x0000000000000081
    assert b.black_rooks == 0x8100000000000000
    assert b.white_queens == 0x0000000000000010
    assert b.black_queens == 0x1000000000000000
    assert b.white_king == 0x0000000000000008
    assert b.black_king == 0x0800000000000000
    assert b.board_state == 30

    from debug import print_board, print_board_state

    print_board(b.white_pawns)
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

    print(b.square_to_index("e4"))
    print(b.index_to_square(b.square_to_index("e4")))
