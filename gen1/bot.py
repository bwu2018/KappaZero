import argparse
import chess.variant
import time
import chess.svg


def eval(board):
    #TODO: Definitely a better and more efficient eval function
    board_str = str(board)

    pawn_val = 10
    knight_val = 30
    bishop_val = 30
    rook_val = 50
    queen_val = 90
    king_val = 10

    white_pawn = board_str.count('P') * -pawn_val
    white_knight = board_str.count('N') * -knight_val
    white_bishop = board_str.count('B') * -bishop_val
    white_rook = board_str.count('R') * -rook_val
    white_queen = board_str.count('Q') * -queen_val
    white_king = board_str.count('K') * -king_val

    black_pawn = board_str.count('p') * pawn_val
    black_knight = board_str.count('n') * knight_val
    black_bishop = board_str.count('b') * bishop_val
    black_rook = board_str.count('r') * rook_val
    black_queen = board_str.count('q') * queen_val
    black_king = board_str.count('k') * king_val

    total = white_pawn + white_knight + white_bishop + white_rook + white_queen + white_king + black_pawn + black_knight + black_bishop + black_rook + black_queen + black_king
    # print(total)
    return total

def alpha_beta(board, depth, alpha, beta, maximizing_player = chess.WHITE):
    # print(alpha, beta)
    # print(board)
    if depth == 0 or board.is_variant_end():
        return [eval(board)]
    if board.turn == maximizing_player:
        value = float('-inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            eval_value = alpha_beta(board, depth - 1, alpha, beta, False)
            if eval_value[0] >= value:
                value = eval_value[0]
                best_move = move
            board.pop()
            if value >= beta:
                break
            alpha = max(alpha, value)
        return value, best_move
    else:
        value = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            eval_value = alpha_beta(board, depth - 1, alpha, beta, True)
            if eval_value[0] <= value:
                value = eval_value[0]
                best_move = move
            board.pop()
            if value <= alpha:
                break
            beta = min(beta, value)
        return value, best_move


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, help='depth of search')
    args = parser.parse_args()
    print('Depth:', args.depth)
    board = chess.variant.AntichessBoard()
    # current_move = input('Enter move:')
    current_move = ''
    while current_move != 'exit':
        if current_move == '':
            start_time = time.time()
            eval_value = alpha_beta(board, args.depth, float('-inf'), float('inf'), chess.WHITE)
            print('Time:', time.time() - start_time)
            print(eval_value)
            print(board.san(eval_value[1]))
            board.push(eval_value[1])
            print('Current board:', eval(board))
            print(board)
        else:
            board.push_san(current_move)
            print(board)
            print('-----------------')
        if board.outcome():
            print('Winner:', board.outcome())
            break
        # current_move = input('Enter move:')

            

if __name__ == '__main__':
    main()