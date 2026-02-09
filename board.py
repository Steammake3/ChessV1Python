from helper import *
from globals import Pieces

class ChessBoard:

    FENMAPPINGS = {"r" : Pieces.Black | Pieces.Rook,
                "n" : Pieces.Black | Pieces.Knight,
                "b" : Pieces.Black | Pieces.Bishop,
                "q" : Pieces.Black | Pieces.Queen,
                "k" : Pieces.Black | Pieces.King,
                "p" : Pieces.Black | Pieces.Pawn,
                "R" : Pieces.White | Pieces.Rook,
                "N" : Pieces.White | Pieces.Knight,
                "B" : Pieces.White | Pieces.Bishop,
                "Q" : Pieces.White | Pieces.Queen,
                "K" : Pieces.White | Pieces.King,
                "P" : Pieces.White | Pieces.Pawn}

    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        """
        Creates a new ChessBoard with the given FEN

        Attributes - board (pieces),
            current_move (uses same schemes as Pieces),
            castling_rights (Bitflag 0bABCD, AB are white king & queen, CD is black)
            en_passant (-1 when N/A, otherwise an index)
            halfmove,
            fullmove,
            pindeces (list of indeces where pieces may be found)

        :param fen: FEN string (optional - will use starting position FEN if not provided)

        """
        fields = fen.strip().split(" ")

        #Decipher FEN boardstate
        ranks = fields[0].split("/")
        self.board = []

        for rank in ranks:
            final = []
            for char in rank:
                if char in "12345678":
                    final += [Pieces.Empty]*int(char)
                else: final.append(self.FENMAPPINGS[char])
            self.board = final + self.board
        
        #Get whose move it is
        self.current_move = Pieces.Black if fields[1]=="b" else Pieces.White

        #Determine castling rights (Bitflags White then Black, King then Queen)
        self.castling_rights = 0
        self.castling_rights |= int("K" in fields[2]) << 3
        self.castling_rights |= int("Q" in fields[2]) << 2
        self.castling_rights |= int("k" in fields[2]) << 1
        self.castling_rights |= int("q" in fields[2])

        #En Passant Square (-1 for null)
        self.en_passant = -1 if fields[3]=="-" else pgn_to_index(fields[3])

        #Halfmove - ++ each turn, unless move was a capture or pawn push
        self.halfmove = int(fields[4])

        #Fullmove - ++ Every time Black plays a move
        self.fullmove = int(fields[5])

        self.pindeces = []
        self.update_pindeces()
    
    def update_pindeces(self):
        retval = []
        for i in range(64):
            if is_piece(self.board[i]): retval.append(i)
        self.pindeces = retval
    
    def __repr__(self):
        """
        Returns a FEN
        """
        retfen = ""

        #Boardstate
        INVFEN = {v: k for k, v in self.FENMAPPINGS.items()}
        FENranks = []
        boardranks = [self.board[i:i+8] for i in range(0, 64, 8)]
        for boardrank in boardranks:
            FENrank = ""
            emptc = 0 #Counter for empty cells
            for square in boardrank:
                if is_empty(square): emptc+=1
                else:
                    FENrank += f"{emptc if emptc else ''}{INVFEN[square]}"
                    emptc = 0
            FENranks.append(FENrank if FENrank else "8")
        
        retfen += "/".join(reversed(FENranks)) + " "

        #Current Move
        retfen += "w " if self.current_move==Pieces.White else "b "

        #Castling (dash means none)
        RIGHTS = ("-", "q", "k", "kq", "Q", "Qq", "Qk", "Qkq", "K", "Kq", "Kk", "Kkq", "KQ", "KQq", "KQk", "KQkq")
        retfen += RIGHTS[self.castling_rights] + " "

        #En Passant (-1 means dash)
        retfen += ("-" if self.en_passant==-1 else index_to_pgn(self.en_passant)) + " "

        #Halfmove + Fullmove combo
        retfen += f"{self.halfmove} {self.fullmove}"

        return retfen
    
    def show(self):
        """×"""
        VMAP = {Pieces.Black | Pieces.Rook : "♜",
                Pieces.Black | Pieces.Knight : "♞",
                Pieces.Black | Pieces.Bishop : "♝",
                Pieces.Black | Pieces.Queen : "♛",
                Pieces.Black | Pieces.King : "♚",
                Pieces.Black | Pieces.Pawn : "♟",
                Pieces.White | Pieces.Rook : "♖",
                Pieces.White | Pieces.Knight : "♘",
                Pieces.White | Pieces.Bishop : "♗",
                Pieces.White | Pieces.Queen : "♕",
                Pieces.White | Pieces.King : "♔",
                Pieces.White | Pieces.Pawn : "♙"}
        
        retval = ""
        for rank in reversed([self.board[i:i+8] for i in range(0, 64, 8)]):
            for piece in rank:
                if piece==Pieces.Empty: retval += "  |"
                else: retval += f"{VMAP[piece]} |"
            retval += "\n"+"==+"*8+"\n"
        
        return retval