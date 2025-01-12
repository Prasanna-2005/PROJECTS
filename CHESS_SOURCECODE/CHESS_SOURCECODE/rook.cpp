#include "includes.h"

// *******************************************      RookPiece      ********************************************************

RookPiece::RookPiece(char PieceColor) : BasePiece(PieceColor) {}

RookPiece::~RookPiece() {}

char RookPiece::GetPiece() {
    return 'R';
}

string RookPiece::GetPieceName() {
    return "Rook";
}

bool RookPiece::AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]) {
    try {
        // Check for out-of-bounds indices
        if (SrcRow < 0 || SrcRow >= 8 || SrcCol < 0 || SrcCol >= 8 ||
            DestRow < 0 || DestRow >= 8 || DestCol < 0 || DestCol >= 8) {
            throw out_of_range("Source or destination coordinates are out of bounds.");
        }

        if (SrcRow == DestRow) {
            // Check all intervening squares in the same row
            int colDirectionSet = (DestCol - SrcCol > 0) ? 1 : -1;
            for (int CheckCol = SrcCol + colDirectionSet; CheckCol != DestCol; CheckCol += colDirectionSet) {
                if (GameBoard[SrcRow][CheckCol] != nullptr) {
                    return false; // There is a piece in between
                }
            }
            return true; // Valid move in the same row
        } else if (DestCol == SrcCol) {
            // Check all intervening squares in the same column
            int rowDirectionSet = (DestRow - SrcRow > 0) ? 1 : -1;
            for (int CheckRow = SrcRow + rowDirectionSet; CheckRow != DestRow; CheckRow += rowDirectionSet) {
                if (GameBoard[CheckRow][SrcCol] != nullptr) {
                    return false; // There is a piece in between
                }
            }
            return true; // Valid move in the same column
        }
        return false; // Not a valid move for a rook
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