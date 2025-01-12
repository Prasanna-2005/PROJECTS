#include "includes.h"

// ********************************************     BasePiece    ***************************************************************
BasePiece::BasePiece(char PieceColor) : PieceColor(PieceColor) {
    if (PieceColor != 'W' && PieceColor != 'B') { // Assuming 'W' for white and 'B' for black
        throw invalid_argument("Invalid piece color. Must be 'W' or 'B'.");
    }
}

BasePiece::~BasePiece() {}

// Returns the color of the piece
char BasePiece::GetColor() {
    return PieceColor;
}

// Checks if the move is legal
bool BasePiece::IsLegalMove(int SrcRow, int SrcCol, int DestRow, int DestCol, BasePiece* GameBoard[8][8]) {
    try {
        BasePiece* Dest = GameBoard[DestRow][DestCol];
        if ((Dest == nullptr) || (PieceColor != Dest->GetColor())) {
            return AreSquaresLegal(SrcRow, SrcCol, DestRow, DestCol, GameBoard);
        }
        return false;
    } catch (const out_of_range& e) {
        cerr << "Error: " << e.what() << endl;
        return false; // Return false to indicate an illegal move
    } catch (const invalid_argument& e) {
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

