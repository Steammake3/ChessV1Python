from globals import Pieces

def pgn_to_index(coord = "a1"):
    tis = "abcdefgh"
    return (int(coord[1])-1)*8 + tis.find(coord[0].lower())

def index_to_pgn(index=8):
    tis = "abcdefgh"
    return tis[index%8] + str(index//8+1)

def is_empty(piece):
    return not (piece&7)

def is_piece(piece):
    return bool(piece&7)