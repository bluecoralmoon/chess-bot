from dataclasses import dataclass
from collections import deque

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
    board_state_history: deque[int] = deque()

    def __post_init__(self) -> None:
        '''Carga la posición FEN de `self.fen` luego de `__init__`.'''
        self.from_fen()

    def from_fen(self, fen_pos: str = None) -> None:
        '''Carga la posición de `self.fen` a menos que haya `fen_pos`.
        \n`fen_pos` debe estar en formato FEN.'''

        return NotImplemented
    
    def to_fen(self) -> str:
        '''Transforma la posición actual a formato FEN y la retorna.'''

        return NotImplemented
    
    def update_occupancy(self) -> None:
        '''Actualiza `all_white`, `all_black` y `occupancy`.'''

        self.all_white = (self.white_pawns   | self.white_knights
                        | self.white_bishops | self.white_rooks
                        | self.white_queens  | self.white_king)
        self.all_black = (self.black_pawns   | self.black_knights
                        | self.black_bishops | self.black_rooks
                        | self.black_queens  | self.black_king)
        self.occupancy = self.all_white | self.all_black
