from dataclasses import dataclass, field
from collections import deque
import fen

PIECE_TO_EMOJI: dict = {
    'white_pawns': '♙',
    'white_knights': '♘',
    'white_bishops': '♗',
    'white_rooks': '♖',
    'white_queens': '♕',
    'white_king': '♔',
    'black_pawns': '♟',
    'black_knights': '♞',
    'black_bishops': '♝',
    'black_rooks': '♜',
    'black_queens': '♛',
    'black_king': '♚'
}

@dataclass(slots=True)
class Board:
    # Posición cargada en formato FEN
    fen: str = ''

    # Bitboards (se cargan en el __post_init__)
    bitboards: dict = field(default_factory=dict)

    # Estado de la partida. Formato board_state:
    # Bit 0: Turno (0 = blancas, 1 = negras)
    # Bits 1-4: Derechos de enroque (KQkq, 1 = puede, 0 = no puede)
    # Bits 5-10: Casilla de en passant (0-63, 0 = ninguna)
    # Bits 11-16: Halfmove clock (0-50)
    board_state: int = 30
    fullmove_number: int = 0

    # Historial de estados (para make_move()/unmake_move())
    # **ES UN STACK**
    # En el mismo formato de board_state
    board_state_history: deque[int] = field(default_factory=deque)

    def __post_init__(self) -> None:
        '''Carga los bitboards en el diccionario de bitboards
        (`self.bitboards`) después de `__init__`.

        Luego carga la posición FEN de `self.fen`.'''
        
        # Bitboards de piezas
        self.bitboards['white_pawns'] = 0x000000000000FF00
        self.bitboards['white_knights'] = 0x0000000000000042
        self.bitboards['white_bishops'] = 0x0000000000000024
        self.bitboards['white_rooks'] = 0x0000000000000081
        self.bitboards['white_queens'] = 0x0000000000000010
        self.bitboards['white_king'] = 0x0000000000000008
        self.bitboards['black_pawns'] = 0x00FF000000000000
        self.bitboards['black_knights'] = 0x4200000000000000
        self.bitboards['black_bishops'] = 0x2400000000000000
        self.bitboards['black_rooks'] = 0x8100000000000000
        self.bitboards['black_queens'] = 0x1000000000000000
        self.bitboards['black_king'] = 0x0800000000000000

        # Bitboards condensados
        self.bitboards['all_white'] = 0x000000000000FFFF
        self.bitboards['all_black'] = 0xFFFF000000000000
        self.bitboards['occupancy'] = 0xFFFF00000000FFFF

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

        for bitboard in self.bitboards.keys():
            self.bitboards[bitboard] = 0
    
    def update_occupancy(self) -> None:
        '''Actualiza `all_white`, `all_black` y `occupancy`.'''

        self.bitboards['all_white'] = (
            self.bitboards['white_pawns']   | self.bitboards['white_knights']
            | self.bitboards['white_bishops'] | self.bitboards['white_rooks']
            | self.bitboards['white_queens']  | self.bitboards['white_king'])
        self.bitboards['all_black'] = (
            self.bitboards['black_pawns']   | self.bitboards['black_knights']
            | self.bitboards['black_bishops'] | self.bitboards['black_rooks']
            | self.bitboards['black_queens']  | self.bitboards['black_king'])
        self.bitboards['occupancy'] = (
            self.bitboards['all_white'] | self.bitboards['all_black'])

    def visualize_board(self) -> None:
        '''Imprime el estado de `Board` en un formato amigable.'''

        print('    A B C D E F G H')

        square = 63
        for rank in range(8):
            row = ""

            while square >= (8 - (rank + 1)) * 8:
                piece = False

                for bitboard in fen.PIECE_BITBOARDS:
                    if self.bitboards[bitboard] & (1 << square):
                        row += PIECE_TO_EMOJI[bitboard]
                        piece = True
                
                if not piece:
                    row += "-"
                
                square -= 1

            print(8 - rank, '|', ' '.join(row))

    def unmake_move(self, move: str) -> None:
        '''
        Deshace un movimiento con el formato de **Move**:


        _Bits 0-5: casilla de origen (0-63);_\n
        _Bits 6-11: casilla de destino (0-63);_\n
        _Bits 12-15: tipo de pieza (0-11 según el índice del bitboard);_\n
        _Bits 16-19: pieza capturada (0-11, o 15 = ninguna);_\n
        _Bits 20-21: tipo de movimiento_
        _(0 = normal, 1 = enroque, 2 = en passant, 3 = promoción);_\n
        _Bits 22-23: promoción_
        _(0 = reina, 1 = torre, 2 = alfil, 3 = caballo)._\n


        Restaura un board_state del historial en el formato
        de **BoardState**:

        _Bit 0: Turno (0 = blancas, 1 = negras);_\n
        _Bits 1-4: Derechos de enroque (KQkq, 1 = puede, 0 = no puede);_\n
        _Bits 5-10: Casilla de en passant (0-63, 0 = ninguna);_\n
        _Bits 11-16: Halfmove clock (0-50)._
        '''



        return NotImplemented
