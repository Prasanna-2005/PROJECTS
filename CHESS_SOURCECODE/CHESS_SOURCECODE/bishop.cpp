#include "includes.h"

// *******************************************      Bishop Piece    *****************************************************************

BishopPiece::BishopPiece(char PieceColor) : BasePiece(PieceColor) {}

BishopPiece::~BishopPiece() {}

char BishopPiece::GetPiece() {
    return 'B';
}

string BishopPiece::GetPieceName() {
    return "Bishop";
}

bool BishopPiece::AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]) {
    try {
        // Check if the move is diagonal
        if (abs(DestCol - SrcCol) == abs(DestRow - SrcRow)) {
            // Ensure all intervening squares are empty
            int rowDirectionSet = (DestRow - SrcRow > 0) ? 1 : -1;
            int colDirectionSet = (DestCol - SrcCol > 0) ? 1 : -1;
            int CheckRow = SrcRow + rowDirectionSet;
            int CheckCol = SrcCol + colDirectionSet;

            while (CheckRow != DestRow) {
                if (GameBoard[CheckRow][CheckCol] != nullptr) {
                    return false; // There is some piece in between src and dest.
                }
                CheckRow += rowDirectionSet;
                CheckCol += colDirectionSet;
            }
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