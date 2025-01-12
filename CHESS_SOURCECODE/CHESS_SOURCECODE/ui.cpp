#include"includes.h"
#include <fstream>
#include<sstream>

// Constructor to initialize the board
game::game() : PlayerTurn('W'),Player("White") {
    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; col++) {
            GameBoard[row][col] = nullptr;
        }
    }

    // Fill black pawns at 6th row and white pawns at 1st row
    for (int col = 0; col < 8; col++) { 
        GameBoard[6][col] = new PawnPiece('B');
        GameBoard[1][col] = new PawnPiece('W');
            
    }
    

    // Fill remaining pieces
    GameBoard[7][0] = new RookPiece('B');
    GameBoard[7][1] = new KnightPiece('B');
    GameBoard[7][2] = new BishopPiece('B'); 
    GameBoard[7][3] = new QueenPiece('B');
    GameBoard[7][4] = new KingPiece('B');
    GameBoard[7][5] = new BishopPiece('B');
    GameBoard[7][6] = new KnightPiece('B');
    GameBoard[7][7] = new RookPiece('B');

    GameBoard[0][0] = new RookPiece('W');
    GameBoard[0][1] = new KnightPiece('W');
    GameBoard[0][2] = new BishopPiece('W');
    GameBoard[0][3] = new QueenPiece('W');
    GameBoard[0][4] = new KingPiece('W');
    GameBoard[0][5] = new BishopPiece('W');
    GameBoard[0][6] = new KnightPiece('W');
    GameBoard[0][7] = new RookPiece('W');
}

// Destructor to clean up the board
game::~game() {
    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; col++) {
            delete GameBoard[row][col];
            GameBoard[row][col] = nullptr;
        }
    }
}

// Print function to display the board
void game::Print() {
    const int cellWidth = 6;
    const int cellHeight = 3;

    for (int row = 0; row < 8 * cellHeight; row++) {

        int row_num = row / cellHeight;   
        for (int col = 0; col < 8 * cellWidth; col++) {    

            int col_num = col / cellWidth;   // each cell colwise  [ 01((2-p_color)(3-piece))45 ]

            if ((row % 3 == 1) && ((col % 6 == 2) ||(col % 6 == 3)) && GameBoard[7 - row_num][col_num] != nullptr) {
               
                if (col % 6 == 2) {    //col :: 2
                    cout << GameBoard[7 - row_num][col_num]->GetColor();
                } else {    //col :: 3
                    cout << GameBoard[7 - row_num][col_num]->GetPiece();
                }
            } else {
                if ((row_num + col_num) % 2 == 1) {    //let (row_num + col_num = x )  all odd x -->black box  , even->white box 
                    cout << BS;     
                } else {
                    cout << WS;    //white 
                }
            }
        }
        if (row % 3 == 1) { // 0(1)2    3(4)5  ........   21(22)23      
            cout << ' ' << 8 - row_num << ' ';
        } else {
            cout << "   ";
        }
        cout << endl;
    }

    for (int row = 0; row < cellHeight; row++) {
        if (row % 3 == 1) {
           
            for (int col = 0; col < 8 * cellWidth; col++) {
                int col_num = col / cellWidth;
                if (col % 6 == 3) { 
                    cout << (char)(col_num + 'A');
                } else {
                    cout << ' ';
                }
            }
            cout << endl;
        } 
    }
}

void game::Start(int x) {
    if(x==1){
        AlternateTurn();
    }
    cout << "\n\n\t\tWelcome to Chess Game \n\n\n";
    while (!IsGameOver()) {
        makeMove();
        AlternateTurn();
    }
    Print();
}

void game::makeMove() {
    bool ValidMove = false;

    while (!ValidMove) {
        Print();
        cout << "CAPTURES\nWHITE: " << w_captures << "  BLACK: " << b_captures << endl;
        cout << "WHITE.........BLACK\n";
        for (int i = 0; i < whiteNotation.size(); ++i) {
            cout << whiteNotation[i] << " ........ ";
            if (i < blackNotation.size()) {
                cout << blackNotation[i] << "\n";
            } else {
                cout << "\n";
            }
        }
        cout << endl;

        // Prompt user input for Move, Undo, Redo, or Load
        cout << "Options:\n";
        cout << "Press 'm' --> make a move,\n 's' --> save in file \n 'l' --> load \n";
        char choice;
        cin >> choice;

        choice = toupper(choice);
        if (choice == 'S') {
            saveToFile("c.txt"); 
        }
        else if (choice == 'L') { // Load from file
            // string filename;
            // cout << "Enter file name to load moves from: ";
            // cin >> filename;
            loadFromFile("c.txt");
            return;
        }
        else if (choice == 'M') {
            // Make a new move
            cout << PlayerTurn << "'s Move (e.g., E2 E4): ";
            string StartMove, EndMove;
            cin >> StartMove >> EndMove;

            if (StartMove.length() == 2 && EndMove.length() == 2) {
                char StartColChar = toupper(StartMove[0]);
                int StartCol = StartColChar - 'A';
                int StartRow = StartMove[1] - '1';

                char EndColChar = toupper(EndMove[0]);
                int EndCol = EndColChar - 'A';
                int EndRow = EndMove[1] - '1';

                if ((StartRow >= 0 && StartRow <= 7) && (StartCol >= 0 && StartCol <= 7) &&
                    (EndRow >= 0 && EndRow <= 7) && (EndCol >= 0 && EndCol <= 7)) {
                    
                    BasePiece* CurrPiece = GameBoard[StartRow][StartCol];
                    if (CurrPiece->GetPiece() == 'K' && abs(StartCol - EndCol) == 2) {
                            if (PlayerTurn == 'W' && !whiteKingMoved) {
                                if (EndCol == 6 && !whiteRookKingsideMoved && GameBoard[0][7] != nullptr && GameBoard[0][7]->GetPiece() == 'R') {
                                    // Kingside castling for white
                                    
                                    if (GameBoard[0][5] == nullptr && GameBoard[0][6] == nullptr) {
                                        if (!IsInCheck(PlayerTurn) && !would_be_in_check(PlayerTurn, 0, 5) && !would_be_in_check(PlayerTurn, 0, 6)) {
                                            GameBoard[0][6] = GameBoard[0][4];
                                            GameBoard[0][4] = nullptr;
                                            GameBoard[0][5] = GameBoard[0][7];
                                            GameBoard[0][7] = nullptr;
                                            whiteKingMoved = true;
                                            whiteRookKingsideMoved = true;
                                            ValidMove = true;
                                            white_castling_possible =false;
                                            whiteMoves.push_back({{StartRow, StartCol}, {EndRow, EndCol}});
                                            whiteNotation.push_back("O-O");
                                            ++(*this);
                                            return;
                                        }
                                    }
                                } else if (EndCol == 2 && !whiteRookQueensideMoved && GameBoard[0][0] != nullptr && GameBoard[0][0]->GetPiece() == 'R') {
                                    // Queenside castling for white
                                    if (GameBoard[0][1] == nullptr && GameBoard[0][2] == nullptr && GameBoard[0][3] == nullptr) {
                                        if (!IsInCheck(PlayerTurn) && !would_be_in_check(PlayerTurn, 0, 3) && !would_be_in_check(PlayerTurn, 0, 2)) {
                                            GameBoard[0][2] = GameBoard[0][4];
                                            GameBoard[0][4] = nullptr;
                                            GameBoard[0][3] = GameBoard[0][0];
                                            GameBoard[0][0] = nullptr;
                                            whiteKingMoved = true;
                                            whiteRookQueensideMoved = true;
                                            ValidMove = true;
                                            whiteMoves.push_back({{StartRow, StartCol}, {EndRow, EndCol}});
                                            whiteNotation.push_back("O-O-O");
                                            white_castling_possible = false;
                                            ++(*this);
                                            return;
                                        }
                                    }
                                }
                            } else if (PlayerTurn == 'B' && !blackKingMoved) {
                                if (EndCol == 6 && !blackRookKingsideMoved && GameBoard[7][7] != nullptr && GameBoard[7][7]->GetPiece() == 'R') {
                                    // Kingside castling for black
                                    if (GameBoard[7][5] == nullptr && GameBoard[7][6] == nullptr) {
                                        if (!IsInCheck(PlayerTurn) && !would_be_in_check(PlayerTurn, 7, 5) && !would_be_in_check(PlayerTurn, 7, 6)) {
                                            
                                            GameBoard[7][6] = GameBoard[7][4];
                                            GameBoard[7][4] = nullptr;
                                            GameBoard[7][5] = GameBoard[7][7];
                                            GameBoard[7][7] = nullptr;
                                            blackKingMoved = true;
                                            blackRookKingsideMoved = true;
                                            ValidMove = true;
                                            blackNotation.push_back("O-O");
                                            blackMoves.push_back({{StartRow, StartCol}, {EndRow, EndCol}});
                                            black_castling_possible =false;
                                            ++(*this);
                                            return;
                                        }
                                    }
                                } else if (EndCol == 2 && !blackRookQueensideMoved && GameBoard[7][0] != nullptr && GameBoard[7][0]->GetPiece() == 'R') {
                                    // Queenside castling for black
                                    if (GameBoard[7][1] == nullptr && GameBoard[7][2] == nullptr && GameBoard[7][3] == nullptr) {
                                        if (!IsInCheck(PlayerTurn) && !would_be_in_check(PlayerTurn, 7, 3) && !would_be_in_check(PlayerTurn, 7, 2)) {
                                            
                                            GameBoard[7][2] = GameBoard[7][4];
                                            GameBoard[7][4] = nullptr;
                                            GameBoard[7][3] = GameBoard[7][0];
                                            GameBoard[7][0] = nullptr;
                                            blackKingMoved = true;
                                            blackRookQueensideMoved = true;
                                            ValidMove = true;
                                            blackNotation.push_back("O-O-O");
                                            black_castling_possible =false;
                                            blackMoves.push_back({{StartRow, StartCol}, {EndRow, EndCol}});
                                            ++(*this);
                                            return;
                                        }
                                    }
                                }
                            }
                            continue;
                        }
                      

                    if (CurrPiece!=nullptr&&  enPassantPossible && dynamic_cast<PawnPiece*>(CurrPiece)) {
                                if (StartCol != EndCol && GameBoard[EndRow][EndCol] == nullptr && enPassantTarget == make_pair(EndRow, EndCol)) {
                                    int capturedRow = (CurrPiece->GetColor() == 'W') ? EndRow - 1 : EndRow + 1;
                                    BasePiece* temp = GameBoard[capturedRow][EndCol] ;
                                    BasePiece*temp2 = GameBoard[StartRow][StartCol];

                                    GameBoard[EndRow][EndCol] = GameBoard[StartRow][StartCol];
                                    GameBoard[StartRow][StartCol] = nullptr;
                                    GameBoard[capturedRow][EndCol] = nullptr;
                                        if (!IsInCheck(PlayerTurn)){
                                            (*this)++;  // Update capture tracker
                                            ++(*this);
                                            delete GameBoard[capturedRow][EndCol] ;

                                            string moveNotation = "Px" + EndMove;
                                            if (PlayerTurn == 'W') {
                                                    whiteMoves.push_back({{StartRow, StartCol}, {-1*EndRow, EndCol}});
                                                    whiteNotation.push_back(moveNotation);
                                            } else {
                                                    blackMoves.push_back({{StartRow, StartCol}, {EndRow, -1*EndCol}});
                                                    blackNotation.push_back(moveNotation);
                                                    return ;
                                            }
                                        }
                                        else{
                                             GameBoard[EndRow][EndCol] = nullptr; 
                                            GameBoard[StartRow][StartCol] = temp2;
                                            GameBoard[capturedRow][EndCol] = temp;
                                            cout<<" Moving current piece puts you in check.\n";
                                        }  
                                 }
                             }
                    if (CurrPiece == nullptr) {
                        cout << "Invalid Move: No piece at the starting position.\n";
                    } else if (CurrPiece->GetColor() != PlayerTurn) {
                        cout << "Invalid Move: You cannot move your opponent's piece.\n";
                    } else if (!CurrPiece->IsLegalMove(StartRow, StartCol, EndRow, EndCol, GameBoard)) {
                        cout << "Invalid Move: The move is not allowed for this piece.\n";
                    } else {
                                    
                        BasePiece* TargetPiece = GameBoard[EndRow][EndCol];
                        GameBoard[EndRow][EndCol] = CurrPiece;
                        GameBoard[StartRow][StartCol] = nullptr;
                        
                        if (!IsInCheck(PlayerTurn)) {

                                 if (RookPiece* rook = dynamic_cast<RookPiece*>(CurrPiece)) { 
                                        if(PlayerTurn=='W' && white_castling_possible){
                                            white_castling_possible = false;
                                        }
                                        else if(PlayerTurn=='B' && black_castling_possible){
                                            black_castling_possible = false;
                                        }
                                  }

                                  if (KingPiece* king = dynamic_cast<KingPiece*>(CurrPiece)) { 
                                        if(PlayerTurn=='W' && white_castling_possible){
                                            white_castling_possible = false;
                                        }
                                        else if(PlayerTurn=='B' && black_castling_possible){
                                            black_castling_possible = false;
                                        }
                                  }

                                enPassantPossible = false;
                                if (PawnPiece* pawn = dynamic_cast<PawnPiece*>(CurrPiece)) {
                                    if (pawn->EnableEnPassant(StartRow, EndRow, StartCol, enPassantTarget)) {
                                        enPassantPossible = true;
                                    }
                                }
                                // Handle pawn promotion
                                if (PawnPiece* pawn = dynamic_cast<PawnPiece*>(CurrPiece)) {
                                    if (pawn->IsPromotion(EndRow)) {
                                        cout << "Pawn Promotion! Choose a piece (Q - Queen, R - Rook, B - Bishop, N - Knight): ";
                                            char choice;
                                            cin >> choice;
                                            choice = toupper(choice);
                                       int val = PromotePawn(EndRow,EndCol,choice);  // Handle promotion based on user input
                                        EndRow*=10;
                                        EndRow+=val;
                                        EndRow *= -1;
                                        EndCol *= -1;
                                        
                                    }
                                }

                                // Log the move in the appropriate player vector
                                string moveNotation = string(1, CurrPiece->GetPiece()) + (TargetPiece ? "x" : "") + EndMove;
                                if (PlayerTurn == 'W') {
                                    whiteMoves.push_back({{StartRow, StartCol}, {EndRow, EndCol}});
                                    whiteNotation.push_back(moveNotation);
                                } else {
                                    blackMoves.push_back({{StartRow, StartCol}, {EndRow, EndCol}});
                                    blackNotation.push_back(moveNotation);
                                }
                                if (TargetPiece != nullptr) {
                                    (*this)++;  // piece-capture tracker
                                }
                                ++(*this);  // moves tracker

                                delete TargetPiece;  // capture opponent piece if present
                                ValidMove = true;
                        } else {
                               enPassantPossible = false;
                            // Revert move if check condition fails
                            GameBoard[StartRow][StartCol] = CurrPiece;
                            GameBoard[EndRow][EndCol] = TargetPiece;
                            cout << "Invalid Move: Moving current piece puts you in check.\n";
                        }
                    }
                } else {
                    cout << "Invalid Input.\n";
                }
            }
        }
    }
}

bool game::would_be_in_check(char PlayerTurn, int x, int y) {
    // Temporarily move the king to the new position
    BasePiece* originalPiece = GameBoard[x][y];
    GameBoard[x][y] = new KingPiece(PlayerTurn);

    bool inCheck = IsInCheck(PlayerTurn);

    // Restore the original piece
    delete GameBoard[x][y];
    GameBoard[x][y] = originalPiece;

    return inCheck;
}

int game::PromotePawn(int row, int col ,char choice) {

    BasePiece* newPiece = nullptr;
    char color = GameBoard[row][col]->GetColor();
    
    switch (choice) {
        case 'Q':
            newPiece = new QueenPiece(color);
            return 1;
            break;
        case 'R':
            newPiece = new RookPiece(color);
            return 2;
            break;
        case 'B':
            newPiece = new BishopPiece(color);
            return 3;
            break;
        case 'N':
            newPiece = new KnightPiece(color);
            return 4;
            break;
        default:
            cout << "Invalid choice, defaulting to Queen." << endl;
            newPiece = new QueenPiece(color);
         return 1;
    }

    delete GameBoard[row][col]; // Remove pawn from the board
    GameBoard[row][col] = newPiece; // Replace pawn with the new piece
    cout << "Pawn promoted to " << newPiece->GetPieceName() << "!" << endl;
    
}

void game::AlternateTurn() {
     Player = (PlayerTurn == 'W') ? "Black" : "White";
    PlayerTurn = (PlayerTurn == 'W') ? 'B' : 'W';
   
}

bool game::IsGameOver() {
    bool canMove = CanMove(PlayerTurn);
    if (!canMove) {     //  gameover 
        if (IsInCheck(PlayerTurn)) {
            AlternateTurn();
            cout << "Checkmate, " << PlayerTurn << " Wins!" << endl;
        } else {
            cout << "Stalemate!" << endl;
        }
    }
    return false; // game not over
}

bool game::IsInCheck(char PieceColor) {

    int KingRow, KingCol;
    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; col++) {
            if (GameBoard[row][col] != nullptr && GameBoard[row][col]->GetColor() == PieceColor && GameBoard[row][col]->GetPiece() == 'K') {
                KingRow = row;
                KingCol = col;
                // cout<<row<<col;
            }
        }
    }
    int row;
    int col;
    for (row = 0; row < 8; row++) {
        for (col = 0; col < 8; col++) {
            if (GameBoard[row][col] != nullptr && GameBoard[row][col]->GetColor() != PieceColor && GameBoard[row][col]->IsLegalMove(row, col, KingRow, KingCol, GameBoard)) {
    
                return true;
            }
        }
    }
    return false;
}

bool game::CanMove(char PieceColor) {
    //Trying all pieces of current player to move to all positions of board 
    //and check if there exists a move ,incase a move was found return true,
    //after trying all pieces if move was not found return false
    for (int row = 0; row < 8; row++) {
        for (int col = 0; col < 8; col++) {
            if (GameBoard[row][col] != nullptr && GameBoard[row][col]->GetColor() == PieceColor)
             {
                for (int toMoveRow = 0; toMoveRow < 8; toMoveRow++) {
                    for (int toMoveCol = 0; toMoveCol < 8; toMoveCol++)
                     {  
                        if (GameBoard[row][col]->IsLegalMove(row, col, toMoveRow, toMoveCol, GameBoard)) 
                        {
                            //momentarily moving a piece
                            BasePiece* Temp = GameBoard[toMoveRow][toMoveCol];
                            GameBoard[toMoveRow][toMoveCol] = GameBoard[row][col];
                            GameBoard[row][col] = nullptr;

                            bool canMove = !IsInCheck(PieceColor);

                            //revert to old stage
                            GameBoard[row][col] = GameBoard[toMoveRow][toMoveCol];
                            GameBoard[toMoveRow][toMoveCol] = Temp;
                            if (canMove) {  //move exist stop
                                return true;
                            }
                        }
                    }
                }
            }
        }
    }
    return false;
}

void game::operator++(){
    if(PlayerTurn=='W'){
        w_moves++;
    }
    else{
        b_moves++;
    }
}

void game::operator++(int){
    if(PlayerTurn=='W'){
        w_captures++;
    }
    else{
        b_captures++;
    }
}


void game::saveToFile(const string& filename) {
    ofstream outFile(filename);

    if (!outFile) {
        cout << "Error: Could not open file for saving.\n";
        return;
    }
    int numMoves = max(whiteMoves.size(), blackMoves.size());
    for (int i = 0; i < numMoves; ++i) {
        // Write white move if it exists
        if (i < whiteMoves.size()) {
            outFile << whiteMoves[i].first.first << " " << whiteMoves[i].first.second << " "
                    << whiteMoves[i].second.first << " " << whiteMoves[i].second.second;
        } else {
            // Placeholder for missing move
            outFile << "-1 -1 -1 -1";
        }

        outFile << " "; // Space separator between white and black moves

        // Write black move if it exists
        if (i < blackMoves.size()) {
            outFile << blackMoves[i].first.first << " " << blackMoves[i].first.second << " "
                    << blackMoves[i].second.first << " " << blackMoves[i].second.second;
        } else {
            // Placeholder for missing move
            outFile << "-1 -1 -1 -1";
        }
        outFile << "\n"; // Newline to separate each move pair
    }

    outFile.close();
    cout << "Game saved to " << filename << "\n";
}


void game::loadFromFile(const string& filename) {
     int x;
    ifstream inFile(filename);
    if (!inFile) {
        cout << "Error: Could not open file for loading.\n";
        return;
    }

    resetBoard();  // Reset the game state before loading moves
    string line;
    bool isPromotion, isEnPassant;

    while (getline(inFile, line)) {

        stringstream ss(line);
        int whiteStartRow, whiteStartCol, whiteEndRow, whiteEndCol;
        int blackStartRow, blackStartCol, blackEndRow, blackEndCol;
        x = blackStartRow;
        // Read white's move


       ss >> whiteStartRow >> whiteStartCol >> whiteEndRow >> whiteEndCol>> blackStartRow >> blackStartCol >> blackEndRow >> blackEndCol;
         
        isPromotion = false;
        isEnPassant = false;
         whiteMoves.push_back({{whiteStartRow, whiteStartCol}, {whiteEndRow, whiteEndCol}});

        // Determine special cases for notation if needed
        if (whiteEndRow<0 && whiteEndCol<0 && whiteEndRow >= 10) {
            isPromotion = true;
        } else if (whiteEndRow <0 || whiteEndCol < 0) {
            isEnPassant = true;
            whiteEndRow = abs(whiteEndRow);
            whiteEndCol = abs(whiteEndCol);
        }

        if (whiteStartRow != -1) {  // Valid white move
            makeAutoMove(whiteStartRow, whiteStartCol, whiteEndRow, whiteEndCol, isEnPassant, isPromotion);
            
            if(isPromotion){
                 whiteEndRow /= 10;
            }
            // Construct notation
             string notation = "";
                     
            notation += coordinateToNotation(whiteEndRow, whiteEndCol);
            whiteNotation.push_back(notation);
        }
        
       

        isPromotion = false;
        isEnPassant = false;
        blackMoves.push_back({{blackStartRow, blackStartCol}, {blackEndRow, blackEndCol}});
   
        if (blackEndRow<0 && blackEndCol<0) {
                isPromotion = true;
                blackEndRow /= 10;
            } else if (blackEndRow < 0 || blackEndCol < 0) {
                isEnPassant = true;
                blackEndRow = abs(blackEndRow);
                blackEndCol = abs(blackEndCol);
            }

        if (blackStartRow != -1) {  // Valid black move
            // Construct notation
            makeAutoMove(blackStartRow, blackStartCol, blackEndRow, blackEndCol, isEnPassant, isPromotion);
              if(isPromotion){
                 blackEndRow /= 10;
            }
            
           string notation = "";       
            notation += coordinateToNotation(blackEndRow, blackEndCol);
            blackNotation.push_back(notation);

            
        }
    }
    
    inFile.close();
    cout << "Game loaded from " << filename << ". Continuing from last saved move.\n";

    Print();  // Display the current board state after loading moves
    if(x==-1)
        Start(1);  // Resume the game
    else{
        Start(0);
    }
}


void game::makeAutoMove(int startRow, int startCol, int endRow, int endCol, bool isEnPassant, bool isPromotion) {
    BasePiece* currPiece = GameBoard[startRow][startCol];

    // Handle castling
    if (currPiece->GetPiece() == 'K' && abs(startCol - endCol) == 2) {
        if (currPiece->GetColor() == 'W') {
            if (endCol == 6) { // Kingside castling for white
               
                GameBoard[0][6] = currPiece;
                GameBoard[0][4] = nullptr;
                GameBoard[0][5] = GameBoard[0][7];
                GameBoard[0][7] = nullptr;
                whiteKingMoved = true;
                whiteRookKingsideMoved = true;
            } else if (endCol == 2) { // Queenside castling for white
               
                GameBoard[0][2] = currPiece;
                GameBoard[0][4] = nullptr;
                GameBoard[0][3] = GameBoard[0][0];
                GameBoard[0][0] = nullptr;
                whiteKingMoved = true;
                whiteRookQueensideMoved = true;
            }
        } else if (currPiece->GetColor() == 'B') {
            if (endCol == 6) { // Kingside castling for black
                 GameBoard[7][6] = currPiece;
                GameBoard[7][4] = nullptr;
                GameBoard[7][5] = GameBoard[7][7];
                GameBoard[7][7] = nullptr;
                blackKingMoved = true;
                blackRookKingsideMoved = true;
            } else if (endCol == 2) { // Queenside castling for black
                 GameBoard[7][2] = currPiece;
                GameBoard[7][4] = nullptr;
                GameBoard[7][3] = GameBoard[7][0];
                GameBoard[7][0] = nullptr;
                blackKingMoved = true;
                blackRookQueensideMoved = true;
            }
        }
    } 
    else{
        GameBoard[endRow][endCol] = currPiece;
        GameBoard[startRow][startCol] = nullptr;
    }


     if (isEnPassant) {
        int capturedRow = (currPiece->GetColor() == 'W') ? endRow - 1 : endRow + 1;
        GameBoard[capturedRow][endCol] = nullptr;

        GameBoard[endRow][endCol] = currPiece;
        GameBoard[startRow][startCol] = nullptr;
    }

    if (isPromotion) {
        GameBoard[endRow][endCol] = currPiece;
        GameBoard[startRow][startCol] = nullptr;
        int promotionChoice = endRow % 10;  // Assume endRow is encoded with promotion piece
        endRow /= 10;
        PromotePawn(endRow, endCol, promotionChoice);
    }
}


string game::coordinateToNotation(int row, int col) {
    char colChar = 'A' + col;
    char rowChar = '1' + row;
    return string(1, colChar) + string(1, rowChar);
}


void game::resetBoard() {
    // Clear board and move data
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < 8; ++j) {
            delete GameBoard[i][j];
            GameBoard[i][j] = nullptr;
        }
    }
    whiteMoves.clear();
    blackMoves.clear();
    whiteNotation.clear();
    blackNotation.clear();

    // Reinitialize pieces on board (assume initBoard is the method that sets up pieces)
      for (int col = 0; col < 8; col++) { 
        GameBoard[6][col] = new PawnPiece('B');
        GameBoard[1][col] = new PawnPiece('W');
        
    }
    GameBoard[7][0] = new RookPiece('B');
    GameBoard[7][1] = new KnightPiece('B');
    GameBoard[7][2] = new BishopPiece('B'); 
    GameBoard[7][3] = new QueenPiece('B');
    GameBoard[7][4] = new KingPiece('B');
    GameBoard[7][5] = new BishopPiece('B');
    GameBoard[7][6] = new KnightPiece('B');
    GameBoard[7][7] = new RookPiece('B');

    GameBoard[0][0] = new RookPiece('W');
    GameBoard[0][1] = new KnightPiece('W');
    GameBoard[0][2] = new BishopPiece('W');
    GameBoard[0][3] = new QueenPiece('W');
    GameBoard[0][4] = new KingPiece('W');
    GameBoard[0][5] = new BishopPiece('W');
    GameBoard[0][6] = new KnightPiece('W');
    GameBoard[0][7] = new RookPiece('W');
   
}