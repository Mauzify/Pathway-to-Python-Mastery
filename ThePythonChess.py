import os
import time
import secrets
import random
import ctypes
import sys
sys.setrecursionlimit(6000)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if os.name == "nt":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    std_handle = kernel32.GetStdHandle(-11)
    mode = ctypes.c_uint()
    kernel32.GetConsoleMode(std_handle, ctypes.byref(mode))
    kernel32.SetConsoleMode(std_handle, mode.value | 0x0004)
############################################################################
GREEN = "\033[92m" 
BLUE = "\033[34m"
DARKBLUE = "\033[1;34m"
CYAN = "\033[96m" 
RED = "\033[91m" 
REDBACKGROUND = "\033[41m"
YELLOW = "\033[33m"
RESET = "\033[0m" 
BOLD = "\033[1m" 
############################################################################
WHITE_SQUARE = "\033[47m\033[30m"
BLACK_SQUARE = "\033[100m\033[97m"
############################################################################
PIECES = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙",
    ".": " "
}
############################################################################
PIECE_NAMES = {
    "p": "PAWN", "r": "ROOK", "n": "KNIGHT", "b": "BISHOP", "q": "QUEEN", "k": "KING",
    "P": "PAWN", "R": "ROOK", "N": "KNIGHT", "B": "BISHOP", "Q": "QUEEN", "K": "KING"
}
############################################################################
VALUES = {
    'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000,
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
    '.': 0
}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PST = {
    'P': [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ],
    'N': [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ],
    'K': [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [ 20, 20,  0,  0,  0,  0, 20, 20],
        [ 20, 30, 10,  0,  0, 10, 30, 20]
    ]
}
############################################################################
def create_board(): 
    return [
        ["r", "n", "b", "q", "k", "b", "n", "r"], 
        ["p", "p", "p", "p", "p", "p", "p", "p"], 
        [".", ".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", ".", "."], 
        ["P", "P", "P", "P", "P", "P", "P", "P"], 
        ["R", "N", "B", "Q", "K", "B", "N", "R"] 
    ]
############################################################################
def typewriter(text, color=RESET, speed=0.001, bold=False, end="\n"):
    style = color + (BOLD if bold else "")
    print(style, end="", flush=True)
    for char in text:
        print(char, end="", flush=True)
        delay = speed + random.uniform(0, 0.01)
        if char in ".!?": delay += 0.1
        time.sleep(delay)
    print(RESET, end=end, flush=True)
############################################################################
def get_coords(position): 
    column_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    try: 
        column = column_map[position[0].lower()]
        row = 8 - int(position[1])
        if 0 <= row <= 7 and 0 <= column <= 7:
            return row, column
        return None
    except:
        return None
############################################################################
def coord_to_alg(coords):
    column_map = ["A", "B", "C", "D", "E", "F", "G", "H"]
    return f"{column_map[coords[1]]}{8 - coords[0]}"
############################################################################
def draw_board_itself(board, last_log="NO SYSTEM LOGS"):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f" LOG > {CYAN}{last_log}{RESET}")
    print(f"{BOLD}        A      B      C      D      E      F      G      H{RESET}")
    for i, row in enumerate(board):
       for _ in range(3): 
        print(f"  {8-i} |", end="")
        for j, piece in enumerate(row):
            style = WHITE_SQUARE if (i + j) % 2 == 0 else BLACK_SQUARE
            if _ == 1:  
                print(f"{style}   {PIECES[piece]}   {RESET}", end="")
            else:
                print(f"{style}       {RESET}", end="")
        print(f"| {BOLD}{8-i}")
    print(f"{BOLD}        A      B      C      D      E      F      G      H{RESET}")
    print("\n")
############################################################################
def is_legal_move(board, start, end, current_turn, ignore_check=False):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    target = board[er][ec]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if piece == ".": return False
    if current_turn == "white" and not piece.isupper(): return False
    if current_turn == "black" and not piece.islower(): return False
    if target != "." and piece.isupper() == target.isupper(): return False
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    p_type = piece.lower()
    dr, dc = abs(er - sr), abs(ec - sc)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    legal = False
    if p_type == "r":
        if (sr == er or sc == ec) and not is_path_blocked(board, start, end): legal = True
    elif p_type == "b":
        if dr == dc and not is_path_blocked(board, start, end): legal = True
    elif p_type == "q":
        if ((sr == er or sc == ec) or (dr == dc)) and not is_path_blocked(board, start, end): legal = True
    elif p_type == "n":
        if (dr == 2 and dc == 1) or (dr == 1 and dc == 2): legal = True
    elif p_type == "k":
        if dr <= 1 and dc <= 1: legal = True
    elif p_type == "p":
        direction = -1 if piece == "P" else 1
        if sc == ec and target == "." and er == sr + direction: legal = True
        elif sc == ec and target == "." and er == sr + (2 * direction):
            start_row = 6 if piece == "P" else 1
            if sr == start_row and board[sr + direction][sc] == ".": legal = True
        elif dc == 1 and target != "." and er == sr + direction: legal = True
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if not legal: return False
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if not ignore_check:
        tmp_target = board[er][ec]
        board[er][ec] = board[sr][sc]
        board[sr][sc] = "."
        in_check = is_in_check(board, current_turn)
        board[sr][sc] = board[er][ec]
        board[er][ec] = tmp_target
        if in_check: return False
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    return True
############################################################################
def is_path_blocked(board, start, end):
    sr, sc = start
    er, ec = end
    row_step = (er - sr) // max(1, abs(er - sr)) if er != sr else 0
    col_step = (ec - sc) // max(1, abs(ec - sc)) if ec != sc else 0
    curr_r, curr_c = sr + row_step, sc + col_step
    while (curr_r, curr_c) != (er, ec):
        if board[curr_r][curr_c] != ".": return True
        curr_r += row_step
        curr_c += col_step
    return False
############################################################################
def is_in_check(board, color):
    king_char = "K" if color == "white" else "k"
    king_pos = None
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_char:
                king_pos = (r, c)
                break
    if not king_pos: return True 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
    enemy_color = "black" if color == "white" else "white"
    for r in range(8):
        for c in range(8):
            if board[r][c] != "." and ((enemy_color == "white" and board[r][c].isupper()) or (enemy_color == "black" and board[r][c].islower())):
                if is_legal_move(board, (r, c), king_pos, enemy_color, ignore_check=True):
                    return True
    return False
############################################################################
def evaluate_board(board):
    score = 0
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p == ".": continue
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
            val = VALUES[p]
            p_upper = p.upper()
            if p_upper in PST:
                table = PST[p_upper]
                score_idx = (7-r) if p.islower() else r
                pos_val = table[score_idx][c]
                val += pos_val
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                
            if p.isupper(): score += val
            else: score -= val
    return score
############################################################################
def get_all_moves(board, color):
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == ".": continue
            if (color == "white" and board[r][c].isupper()) or (color == "black" and board[r][c].islower()):
                for tr in range(8):
                    for tc in range(8):
                        if is_legal_move(board, (r, c), (tr, tc), color):
                            moves.append(((r, c), (tr, tc)))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    moves.sort(key=lambda m: VALUES[board[m[1][0]][m[1][1]]], reverse=True)
    return moves
############################################################################
def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate_board(board), None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    best_move = None
    pieces = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p != "." and ((maximizing and p.isupper()) or (not maximizing and p.islower())):
                pieces.append((r, c))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if maximizing:
        max_ev = -10000
        for r, c in pieces:
            for tr in range(8):
                for tc in range(8):
                    if is_legal_move(board, (r, c), (tr, tc), "white"):
                        tmp = board[tr][tc]; board[tr][tc] = board[r][c]; board[r][c] = "."
                        ev = minimax(board, depth-1, alpha, beta, False)[0]
                        board[r][c] = board[tr][tc]; board[tr][tc] = tmp
                        if ev > max_ev:
                            max_ev = ev
                            best_move = ((r, c), (tr, tc))
                        alpha = max(alpha, ev)
                        if beta <= alpha: break
            if beta <= alpha: break
        return max_ev, best_move
    else:
        min_ev = 10000
        for r, c in pieces:
            for tr in range(8):
                for tc in range(8):
                    if is_legal_move(board, (r, c), (tr, tc), "black"):
                        tmp = board[tr][tc]; board[tr][tc] = board[r][c]; board[r][c] = "."
                        ev = minimax(board, depth-1, alpha, beta, True)[0]
                        board[r][c] = board[tr][tc]; board[tr][tc] = tmp
                        if ev < min_ev:
                            min_ev = ev
                            best_move = ((r, c), (tr, tc))
                        beta = min(beta, ev)
                        if beta <= alpha: break
            if beta <= alpha: break
        return min_ev, best_move
############################################################################
if __name__ == "__main__":
    board = create_board()
    current_turn = "white"
    last_action = "SYSTEM INITIALIZED"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    os.system('cls' if os.name == 'nt' else 'clear')
    typewriter(f"    --->> {GREEN}{BOLD}Game of Chess{RESET} | Written in {YELLOW}Python{RESET} 3.11.8 | 3.11 (64-Bit) <<---", bold=True) 
    typewriter(f"             --> OPPONENT: {CYAN}C{RESET}{DARKBLUE}E{RESET}{CYAN}N{RESET}{DARKBLUE}T{RESET}{CYAN}R{RESET}{DARKBLUE}A{RESET}{CYAN}L{RESET} {DARKBLUE}P{RESET}{CYAN}R{RESET}{DARKBLUE}O{RESET}{CYAN}C{RESET}{DARKBLUE}E{RESET}{CYAN}S{RESET}{DARKBLUE}S{RESET}{CYAN}I{RESET}{DARKBLUE}N{RESET}{CYAN}G{RESET} {DARKBLUE}U{RESET}{CYAN}N{RESET}{DARKBLUE}I{RESET}{CYAN}T{RESET} ({RED}>{RESET}>{RED}{BOLD} | CPU | {RESET}<{RED}<{RESET}) <--", bold=True)
    typewriter(f"            DEVELOPED BY: {RED}MAUZIFY{RESET} >= https://github.com/Mauzify", bold=True)
    typewriter(f"=" * 80 + "\n\n")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    typewriter(f" >> {RED}S{RESET}{YELLOW}E{RESET}{GREEN}L{RESET}{CYAN}E{RESET}{BLUE}C{RESET}{DARKBLUE}T{RESET} {RED}D{RESET}{YELLOW}I{RESET}{GREEN}F{RESET}{CYAN}F{RESET}{BLUE}I{RESET}{DARKBLUE}C{RESET}{RED}U{RESET}{YELLOW}L{RESET}{GREEN}T{RESET}{CYAN}Y{RESET} [1: {GREEN}Casual{RESET}/{GREEN}Confident{RESET} | 2: {YELLOW}Intermediate{RESET} | 3: {RED}{BOLD}Magnus Carlsen Mode{RESET} 💀]", speed=0.01)
    diff = input(" > ")
    minimax_depth = 2 if diff == "1" else (3 if diff == "2" else 4)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[H", end="") 
    print("\n" * 27)       
############################################################################
    while True:
        for c in range(8):
            if board[0][c] == "P": board[0][c] = "Q"
            if board[7][c] == "p": board[7][c] = "q"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
        draw_board_itself(board, last_action)
        score = evaluate_board(board)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~          
        try:
            if current_turn == "white":
                check_status = f"{RED}[CHECK!]{RESET} " if is_in_check(board, "white") else ""
                typewriter(f"{check_status}{GREEN}{BOLD}SCORE: {RESET}{score} | {CYAN}{BOLD}TURN{RESET}: {BOLD}WHITE{RESET} | INPUT > ", end="", speed=0.005)
                raw = input().split()
                print("\033[1A\033[K", end="") 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
                if len(raw) == 2:
                    start = get_coords(raw[0])
                    end = get_coords(raw[1])
                    if start and end and is_legal_move(board, start, end, "white"):
                        p_name = PIECE_NAMES[board[start[0]][start[1]]]
                        last_action = f"WHITE {p_name}: {raw[0].upper()} > {raw[1].upper()}"
                        board[end[0]][end[1]] = board[start[0]][start[1]]
                        board[start[0]][start[1]] = "."
                        current_turn = "black"
                    else:
                        last_action = f"{RED}ILLEGAL MOVE/IN CHECK - RETRY{RESET}"
                else:
                    last_action = f"{RED}FORMAT ERROR: USE 'E2 E4'{RESET}"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~               
            else:
                typewriter("CPU IS THINKING...", color=CYAN, end="", speed=0.005)
                _, cpu_move = minimax(board, minimax_depth, -100000, 100000, False)
                print("\033[K", end="\r") 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                  
                if cpu_move:
                    p_name = PIECE_NAMES[board[cpu_move[0][0]][cpu_move[0][1]]]
                    m_start = coord_to_alg(cpu_move[0])
                    m_end = coord_to_alg(cpu_move[1])
                    last_action = f"CPU {p_name}: {m_start} > {m_end}"
                    board[cpu_move[1][0]][cpu_move[1][1]] = board[cpu_move[0][0]][cpu_move[0][1]]
                    board[cpu_move[0][0]][cpu_move[0][1]] = "."
                current_turn = "white"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
        except KeyboardInterrupt:
            break
############################################################################