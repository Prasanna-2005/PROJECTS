
using namespace std;
// ***************************************      BasePiece     *********************************************************************
class BasePiece {
public:
    BasePiece(char PieceColor);
    virtual ~BasePiece();

    virtual char GetPiece() = 0;
    virtual string GetPieceName() =0;
    char GetColor();
    bool IsLegalMove(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]);
private:
    virtual bool AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]) = 0;
    char PieceColor;
};

// ***************************************      Pawn    *********************************************************************


class PawnPiece : public BasePiece {
public:
    PawnPiece(char PieceColor);
    ~PawnPiece();
      bool IsPromotion(int DestRow);
    bool CanEnPassant(int StartRow, int StartCol, int EndRow, int EndCol, pair<int, int> enPassantTarget);
        bool EnableEnPassant(int StartRow, int EndRow, int StartCol, pair<int, int>& enPassantTarget);
private:
    virtual char GetPiece();
    virtual string GetPieceName();
    bool AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]);
};


// ***************************************  Knight    *********************************************************************

class KnightPiece : public BasePiece {
public:
    KnightPiece(char PieceColor);
    ~KnightPiece();
private:
    virtual char GetPiece();
    virtual string GetPieceName();
    bool AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]);
};


// ***************************************   Bishop     *********************************************************************

class BishopPiece : public BasePiece {
public:
    BishopPiece(char PieceColor);
    ~BishopPiece();
private:
    virtual char GetPiece();
    virtual string GetPieceName();
    bool AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]);
};


// ***************************************   Rook   *********************************************************************

class RookPiece : public BasePiece {
public:
    RookPiece(char PieceColor);
    ~RookPiece();
private:
    virtual char GetPiece();
    virtual string GetPieceName();
    bool AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]);
};


// ***************************************     Queen     *********************************************************************

class QueenPiece : public BasePiece {
public:
    QueenPiece(char PieceColor);
    ~QueenPiece();
private:
    virtual char GetPiece();
    virtual string GetPieceName();
    bool AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]);
};


// ***************************************     King     *********************************************************************

class KingPiece : public BasePiece {
public:
    KingPiece(char PieceColor);
    ~KingPiece();
private:
    virtual char GetPiece();
    virtual string GetPieceName();
    bool AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]);
};


