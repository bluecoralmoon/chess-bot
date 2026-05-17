'''
En este módulo se implementan todas las funciones utilizadas
para la carga y descarga de información del tablero mediante
la notación FEN.

Contiene varias funciones auxiliares para este propósito.
'''

from collections import deque
import re

def to_fen(board) -> str:
    '''Transforma la posición actual a formato FEN y la retorna.'''

    fen = ""

    # Piezas
    contador = 0
    for sq in range(63, -1, -1):
        if not board.occupancy & (1 << sq):
            contador += 1
        else:
            if contador != 0:
                fen += str(contador)
            contador = 0
            if (board.white_pawns & (1 << sq)):
                fen += "P"
            elif (board.white_knights & (1 << sq)):
                fen += "N"
            elif (board.white_bishops & (1 << sq)):
                fen += "B"
            elif (board.white_rooks & (1 << sq)):
                fen += "R"
            elif (board.white_queens & (1 << sq)):
                fen += "Q"
            elif (board.white_king & (1 << sq)):
                fen += "K"
            elif (board.black_pawns & (1 << sq)):
                fen += "p"
            elif (board.black_knights & (1 << sq)):
                fen += "n"
            elif (board.black_bishops & (1 << sq)):
                fen += "b"
            elif (board.black_rooks & (1 << sq)):
                fen += "r"
            elif (board.black_queens & (1 << sq)):
                fen += "q"
            elif (board.black_king & (1 << sq)):
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
    fen += "b" if board.board_state & 1 else "w"
    fen += " "

    # Enroque
    K = board.board_state & 1 << 1
    Q = board.board_state & 1 << 2
    k = board.board_state & 1 << 3
    q = board.board_state & 1 << 4
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
    en_passant_sq = board.board_state >> 5 & ((1 << 6) - 1)
    if en_passant_sq == 0:
        fen += "-"
    else:
        fen += index_to_square(en_passant_sq)
    fen += " "

    # Halfmove clock
    halfmove_clock = board.board_state >> 11 & ((1 << 6) - 1)
    fen += str(halfmove_clock)
    fen += " "

    # Fullmove number
    fen += str(board.fullmove_number)

    return fen

def from_fen(board, fen_pos: str = '') -> bool:
    '''Carga la posición de `board.fen` o, si existe, `fen_pos`.\n
    `fen_pos` debe estar en formato FEN.\n
    Retorna `True` si fue exitoso y `False` en caso contrario.\n
    En caso de ser exitoso, guarda `fen_pos` en `board.fen`.'''

    fen = fen_pos if fen_pos else board.fen
    if not check_fen_format(fen): return False

    board.reset_bitboards()

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

    board.board_state_history = deque()
    board.fullmove_number = int(fullmove_number)
    turn = 0 if turn == "w" else 1
    en_passant_square = 0 if en_passant_square == "-" \
                            else square_to_index(en_passant_square)
    board.board_state = (turn |
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
                    board.white_pawns |= 1 << square
                else:
                    board.black_pawns |= 1 << square
            elif el in "nN":
                if el.isupper():
                    board.white_knights |= 1 << square
                else:
                    board.black_knights |= 1 << square
            elif el in "bB":
                if el.isupper():
                    board.white_bishops |= 1 << square
                else:
                    board.black_bishops |= 1 << square
            elif el in "rR":
                if el.isupper():
                    board.white_rooks |= 1 << square
                else:
                    board.black_rooks |= 1 << square
            elif el in "qQ":
                if el.isupper():
                    board.white_queens |= 1 << square
                else:
                    board.black_queens |= 1 << square
            elif el in "kK":
                if el.isupper():
                    board.white_king |= 1 << square
                else:
                    board.black_king |= 1 << square
            if el != "/":
                square -= 1

    board.update_occupancy()
    board.fen = fen

    return True

def square_to_index(square: str) -> int:
    '''Transforma el nombre de una casilla a su índice.
    
    Ej. `"e4"` -> `27`.
    Retorna `-1` en caso de error.'''

    if (len(square) != 2 or type(square) != str
        or square[0] not in "abcdefgh" or square[1] not in "12345678"):
        return -1
    
    return int(square[1]) * 8 - "abcdefgh".index(square[0]) - 1

def index_to_square(index: int) -> str | None:
    '''Transforma el índice de una casilla a su nombre.
    
    Ej. `27` -> `"e4"`.
    Retorna `None` en caso de error.'''

    if (type(index) != int or index < 0 or index > 63):
        return None
    
    return ("abcdefgh"[::-1])[index % 8] + str(index // 8 + 1)

def check_fen_format(fen: str) -> bool:
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