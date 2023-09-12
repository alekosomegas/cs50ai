from minesweeper import Minesweeper, MinesweeperAI, Sentence
import pytest

class TestSentence:
    def test_known_mines(self):
        sentence = Sentence({(0,0)}, 1)
        assert sentence.known_mines() == {(0,0)}

    def test_known_safe(self):
        sentence = Sentence({(0,0)}, 0)
        assert sentence.known_safes() == {(0,0)}
