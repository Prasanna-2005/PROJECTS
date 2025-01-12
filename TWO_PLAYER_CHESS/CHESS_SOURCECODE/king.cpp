#include"includes.h"

// *****************************************        KingPiece       *********************************************************************
KingPiece::KingPiece(char PieceColor) : BasePiece(PieceColor) {}

KingPiece::~KingPiece() {}

char KingPiece::GetPiece() {
    return 'K';
}

string KingPiece::GetPieceName() {
    return "King";
}

bool KingPiece::AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]) {
    try {
      
        int rowDiff = DestRow - SrcRow;
        int colDiff = DestCol - SrcCol;

        // King can move one square in any direction
        if (((rowDiff >= -1) && (rowDiff <= 1)) && ((colDiff >= -1) && (colDiff <= 1))) {
            return true;
        }
        return false;
    } catch (const out_of_range& e) {
        cerr << "Error: " << e.what() << endl;
        return false; // Return false to indicate an illegal move
    } catch (const exception& e) {
        cerr << "An unexpected error occurred: " << e.what() << endl;
        return false; // Return false to indicate an illegal move
    } catch (...) {
        cerr << "An unknown error occurred." << endl;
        return false; // Return false to indicate an illegal move
    }
}