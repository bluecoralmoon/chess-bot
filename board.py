from dataclasses import dataclass, field
from collections import deque
import fen

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

        return fen.from_fen(self, fen_pos=fen_pos)
    
    def to_fen(self) -> str:
        '''Transforma la posición actual a formato FEN y la retorna.'''

        return fen.to_fen(self)
    
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
