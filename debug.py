def print_board_state(board_state: int) -> None:
    '''Recibe un `int` con el formato de `board_state` y lo imprime
    para verificar que el formato esté correcto.
    
    El formato es:
    Bit 0: Turno (0 = blancas, 1 = negras);
    Bits 1-4: Derechos de enroque (KQkq, 1 = puede, 0 = no puede);
    Bits 5-10: Casilla de en passant (0-63, 0 = ninguna);
    Bits 11-16: Halfmove clock (0-50).'''

    print("Juegan las", "negras" if (board_state & 1) else "blancas")
    K = board_state & 1 << 1
    Q = board_state & 1 << 2
    k = board_state & 1 << 3
    q = board_state & 1 << 4
    print(
        "Las blancas" + (" pueden enroncar" if K | Q else "") +
        (" en el lado del rey" if K else "") +
        (" y" if K and Q else "") +
        (" en el lado de la reina" if Q else "") +
        (" no pueden enroncar" if not K and not Q else "")
    )
    print(
        "Las negras" + (" pueden enroncar" if k | q else "") +
        (" en el lado del rey" if k else "") +
        (" y" if k and q else "") +
        (" en el lado de la reina" if q else "") +
        (" no pueden enroncar" if not k and not q else "")
    )

    en_passant_sq = board_state >> 5 & ((1 << 6) - 1)
    print(f"Hay en passant en la casilla {en_passant_sq}"
          if en_passant_sq else "No hay en passant")
    
    halfmove_clock = board_state >> 11 & ((1 << 6) - 1)
    print(f"Ha habido {halfmove_clock} movimientos desde la última captura "
          "o avance de peón")
    
    print(f"Estado encriptado: {format(board_state, 'b')}")

if __name__ == "__main__":
    import random
    board_state = random.getrandbits(17)
    print_board_state(board_state)
