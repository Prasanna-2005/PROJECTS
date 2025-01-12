#include "includes.h"
// ****************************************    KnightPiece     **************************************************************

KnightPiece::KnightPiece(char PieceColor) : BasePiece(PieceColor) {}

KnightPiece::~KnightPiece() {}

char KnightPiece::GetPiece() {
    return 'N';
}

string KnightPiece::GetPieceName() {
    return "Knight";
}

bool KnightPiece::AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]) {
    try {
        
        // Check if the move is in an L-shape (Knight's move)
        if ((SrcCol == DestCol + 1 || SrcCol == DestCol - 1) && 
            (SrcRow == DestRow + 2 || SrcRow == DestRow - 2)) {
            return true;
        }
        if ((SrcCol == DestCol + 2 || SrcCol == DestCol - 2) && 
            (SrcRow == DestRow + 1 || SrcRow == DestRow - 1)) {
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