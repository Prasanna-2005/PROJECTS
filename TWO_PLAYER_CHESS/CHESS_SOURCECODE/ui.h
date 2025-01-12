#include<vector>
#define WHITE_SQUARE_WINDOWS "\xDB" // -->█ white color
#define BLACK_SQUARE_WINDOWS "\xFF" //--->█ black color 

#define WHITE_SQUARE_LINUX " "   //-->terminals background act as white
#define BLACK_SQUARE_LINUX "█"   // █ black color

#ifdef _WIN32
   #define WS WHITE_SQUARE_WINDOWS
   #define BS BLACK_SQUARE_WINDOWS
#else
   #define WS WHITE_SQUARE_LINUX
   #define BS BLACK_SQUARE_LINUX
#endif

using namespace std;
class game {   
public:
    game();                // Constructor
    ~game();               // Destructor

    bool whiteKingMoved = false;
    bool whiteRookKingsideMoved = false;
    bool whiteRookQueensideMoved = false;
    bool white_castling_possible = true;

    bool blackKingMoved = false;
    bool blackRookKingsideMoved = false;
    bool blackRookQueensideMoved = false;
    bool black_castling_possible = true;
   
   bool would_be_in_check(char PlayerTurn, int x, int y) ;


    void Start(int x);                // Initialize the game
    void Print();                // Print the board

    void makeMove();          // Get and process the next move
    void AlternateTurn();        // Switch player turn
    void resetBoard() ;
     
    bool IsInCheck(char PieceColor);  // Check if a player is in check
    bool CanMove(char PieceColor);    // Check if a player can make a legal move
    bool IsGameOver();                // Check if the game is over

    void operator++();  //moves tracker
    void operator++(int); //captures tracker

    int PromotePawn(int row, int col,char choice);

    bool enPassantPossible = false;
    pair<int, int> enPassantTarget;

    void loadFromFile(const string& filename);
    void saveToFile(const string& filename);
   void makeAutoMove(int startRow, int startCol, int endRow, int endCol, bool isEnPassant, bool isPromotion);
    string coordinateToNotation(int row, int col);



private:
    BasePiece* GameBoard[8][8];   // 8x8 chessboard
    char PlayerTurn;                  // Whose turn it is ('W' or 'B')
    string Player;  //  // Whose turn it is ('WHITE' or 'BLACK')

    vector<pair<pair<int, int>, pair<int, int>>> whiteMoves;    //redo + game retrival <stores coordinates<(2,3),(3,4)>>
    vector<pair<pair<int, int>, pair<int, int>>> blackMoves;

    vector<string> whiteNotation;   // Stores move names in string format eg:d5 ka5
    vector<string> blackNotation;   


    int w_moves = 0;
    int b_moves = 0;

    int w_captures = 0;
    int b_captures = 0;



    

};
