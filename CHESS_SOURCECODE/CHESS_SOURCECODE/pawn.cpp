#include "includes.h"
#include <stdexcept>

// ***************************************      PawnPiece     *********************************************************************

PawnPiece::PawnPiece(char PieceColor) : BasePiece(PieceColor) {}

PawnPiece::~PawnPiece() {}

char PawnPiece::GetPiece() {
    return 'P';
}

string PawnPiece::GetPieceName() {
    return "Pawn";
}

bool PawnPiece::AreSquaresLegal(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]) {
    try {
        BasePiece* Dest = GameBoard[DestRow][DestCol];
        if (Dest == nullptr) {
            // Destination square is unoccupied
            if (SrcCol == DestCol && abs(SrcRow - DestRow) == 1) {
                if (GetColor() == 'W') {
                    return DestRow > SrcRow; // Move forward for white
                } else {
                    return DestRow < SrcRow; // Move forward for black
                }
            } else if ((SrcCol == DestCol) && (SrcRow == 1 || SrcRow == 6) && abs(SrcRow - DestRow) == 2) {
                // Move 2 steps case
                if (GetColor() == 'W') {
                    return GameBoard[SrcRow + 1][DestCol] == nullptr; // Check if the square in between is empty
                } else {
                    return GameBoard[SrcRow - 1][DestCol] == nullptr; // Check if the square in between is empty
                }
            }
        } else {
            // Destination holds piece of opposite color --> piece strike
            if ((SrcCol == DestCol + 1) || (SrcCol == DestCol - 1)) {
                if (GetColor() == 'W') {
                    return DestRow == SrcRow + 1; // White pawn strike
                } else {
                    return DestRow == SrcRow - 1; // Black pawn strike
                }
            }
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

bool PawnPiece::IsPromotion(int DestRow) {
    try {
        if (GetColor() == 'W' && DestRow == 7) {
            return true; // White pawn reached the last rank
        } else if (GetColor() == 'B' && DestRow == 0) {
            return true; // Black pawn reached the last rank
        }
        return false;
    } catch (const exception& e) {
        cerr << "An unexpected error occurred: " << e.what() << endl;
        return false; // Return false to indicate an illegal move
    } catch (...) {
        cerr << "An unknown error occurred." << endl;
        return false; // Return false to indicate an illegal move
    }
}

// Checks if en passant is possible for the pawn at the specified position
bool PawnPiece::CanEnPassant(int startRow, int startCol, int endRow, int endCol, pair<int, int> enPassantTarget) {
    try {
        // Check if moving diagonally to en passant target
        return (endRow == enPassantTarget.first && endCol == enPassantTarget.second &&
                abs(endRow - startRow) == 1 && abs(endCol - startCol) == 1);
    } catch (const exception& e) {
        cerr << "An unexpected error occurred: " << e.what() << endl;
        return false; // Return false to indicate an illegal move
    } catch (...) {
        cerr << "An unknown error occurred." << endl;
        return false; // Return false to indicate an illegal move
    }
}


// Enables en passant if a pawn moves two squares forward
bool PawnPiece::EnableEnPassant(int startRow, int endRow, int col, std::pair<int, int>& enPassantTarget) {
    // If moving two squares forward, set enPassantTarget
    if (abs(startRow - endRow) == 2) {
        enPassantTarget = std::make_pair((startRow + endRow) / 2, col);
        return true;
    }
    return false;
}