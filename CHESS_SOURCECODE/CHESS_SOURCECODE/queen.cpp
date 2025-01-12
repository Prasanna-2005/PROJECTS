#include "includes.h"
// *********************************************   QueenPiece   ***************************************************************

QueenPiece::QueenPiece(char PieceColor) : BasePiece(PieceColor) {}

QueenPiece::~QueenPiece() {}

char QueenPiece::GetPiece() {
    return 'Q';
}

string QueenPiece::GetPieceName() {
    return "Queen";
}

bool QueenPiece::AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]) {
    try {
              if (SrcRow == DestRow) {
            // Check all intervening squares in the same row
            int ColDirection = (DestCol - SrcCol > 0) ? 1 : -1;
            for (int CheckCol = SrcCol + ColDirection; CheckCol != DestCol; CheckCol += ColDirection) {
                if (GameBoard[SrcRow][CheckCol] != nullptr) {
                    return false; // There is a piece in between
                }
            }
            return true;
        } else if (DestCol == SrcCol) {
            // Check all intervening squares in the same column
            int RowDirection = (DestRow - SrcRow > 0) ? 1 : -1;
            for (int CheckRow = SrcRow + RowDirection; CheckRow != DestRow; CheckRow += RowDirection) {
                if (GameBoard[CheckRow][SrcCol] != nullptr) {
                    return false; // There is a piece in between
                }
            }
            return true;
        } else if (abs(DestCol - SrcCol) == abs(DestRow - SrcRow)) {
            // Check all intervening squares on the diagonal
            int RowDirection = (DestRow - SrcRow > 0) ? 1 : -1;
            int ColDirection = (DestCol - SrcCol > 0) ? 1 : -1;
            for (int CheckRow = SrcRow + RowDirection, CheckCol = SrcCol + ColDirection;
                 CheckRow != DestRow;
                 CheckRow += RowDirection, CheckCol += ColDirection) {
                if (GameBoard[CheckRow][CheckCol] != nullptr) {
                    return false; // There is a piece in between
                }
            }
            return true;
        }
        return false; // Not a valid move for a queen
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