import tictactoe as ttt
import pytest

empty_board = ttt.initial_state()

class TestPlayer: 
    def test_empty_board(self):
        assert ttt.player(empty_board) is ttt.X

    def test_Os_turn(self):
        board = ttt.initial_state()
        board[0][0] = ttt.X
        assert ttt.player(board) is ttt.O

    def test_Xs_turn(self): 
        board = ttt.initial_state()
        board[0][0] = ttt.X
        board[0][1] = ttt.O
        assert ttt.player(board) is ttt.X


class TestActions: 
    def test_empty_board(self):
        empty_board = ttt.initial_state()
        all_actions = set([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)])
        assert ttt.actions(empty_board) == all_actions

    def test_2_mover(self):
        board = ttt.initial_state()
        board[0][0] = ttt.X
        board[0][1] = ttt.O
        all_actions = set([(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)])
        assert ttt.actions(board) == all_actions

class TestResult:
    def test_out_of_bounds_action(self):
        action = (3,3)
        with pytest.raises(ttt.InvalidActionError):
            ttt.result(empty_board, action)

    def test_used_square_action(self):
        board = ttt.initial_state()
        board[1][1] = ttt.X
        action = (1,1)
        with pytest.raises(ttt.InvalidActionError):
            ttt.result(board, action)

    def test_empty_board(self):
        result_board = ttt.result(empty_board, (1,1))
        
        assert result_board is not empty_board

        for y in range(3):
            for x in range(3):
                if x == 1 and y == 1:
                    assert result_board[y][x] == ttt.X
                else:
                    assert result_board[y][x] == ttt.EMPTY

    def test_2_moves(self):
        board = ttt.initial_state()
        board[0][0] = ttt.X
        board[0][1] = ttt.O
        result_board = ttt.result(board, (0,2))

        assert result_board[0][0] == ttt.X
        assert result_board[0][1] == ttt.O
        assert result_board[0][2] == ttt.X

        for y in range(2):
            for x in range(3):
                assert result_board[y+1][x] == ttt.EMPTY

class TestWinner:
    def test_empty_board(self):
        assert ttt.winner(empty_board) == None
    
    def test_game_in_progress(self):
        board = ttt.initial_state()
        board[0][1] = ttt.X
        board[1][1] = ttt.O
        assert ttt.winner(board) == None

    def test_wins_vertically(self):
        board = [[ttt.X, ttt.O, ttt.O],
                 [ttt.X, ttt.X, ttt.O],
                 [ttt.X, ttt.EMPTY, ttt.EMPTY]]
        assert ttt.winner(board) == ttt.X

    def test_wins_horizontally(self): 
        board = [[ttt.X, ttt.X, ttt.X],
                 [ttt.O, ttt.X, ttt.O],
                 [ttt.O, ttt.EMPTY, ttt.EMPTY]]
        assert ttt.winner(board) == ttt.X

    def test_wins_diagonally(self):
        board1 = [[ttt.X, ttt.X, ttt.EMPTY],
                 [ttt.O, ttt.X, ttt.O],
                 [ttt.O, ttt.EMPTY, ttt.X]] 
        board2 = [[ttt.EMPTY, ttt.X, ttt.O],
                  [ttt.X,     ttt.O, ttt.X],
                  [ttt.O, ttt.EMPTY, ttt.EMPTY]]
        
        assert ttt.winner(board1) == ttt.X
        assert ttt.winner(board2) == ttt.O

    def test_tie(self):
        board = [[ttt.X, ttt.O, ttt.X],
                 [ttt.O, ttt.O, ttt.X],
                 [ttt.X, ttt.X, ttt.O]]
        assert ttt.winner(board) == None

class TestTerminal:
    def test_empty_board(self):
        assert ttt.terminal(empty_board) == False

    def test_game_in_progress(self):
        board = ttt.initial_state()
        board[0][1] = ttt.X
        board[1][1] = ttt.O
        assert ttt.terminal(board) == False

    def test_tie(self):
        board = [[ttt.X, ttt.O, ttt.X],
                 [ttt.O, ttt.O, ttt.X],
                 [ttt.X, ttt.X, ttt.O]]
        assert ttt.terminal(board) == True

    def test_winner(self):
        board = [[ttt.X, ttt.X, ttt.X],
                 [ttt.O, ttt.X, ttt.O],
                 [ttt.O, ttt.EMPTY, ttt.EMPTY]]
        assert ttt.terminal(board) == True

class TestUtility:
    def test_X_wins(self):
        board = [[ttt.X, ttt.X, ttt.X],
            [ttt.O, ttt.X, ttt.O],
            [ttt.O, ttt.EMPTY, ttt.EMPTY]]
        assert ttt.utility(board) == 1


    def test_O_wins(self):
        board = [[ttt.EMPTY, ttt.X, ttt.O],
            [ttt.X,     ttt.O, ttt.X],
            [ttt.O, ttt.EMPTY, ttt.EMPTY]]
        assert ttt.utility(board) == -1


    def test_tie(self):
        board = [[ttt.X, ttt.O, ttt.X],
                 [ttt.O, ttt.O, ttt.X],
                 [ttt.X, ttt.X, ttt.O]]
        assert ttt.utility(board) == 0
