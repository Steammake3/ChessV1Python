from board import *
from helper import *
from globals import *

x="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RN2KBNR w - e5 23 203"

print("\n"+repr(ChessBoard(x))+"\n")
print("\n"+ChessBoard(x).show()+"\n")

assert repr(ChessBoard())=="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
assert repr(ChessBoard(x))==x

print("Yay")