#ifndef HEADER_3D3C3E96A5E1CC65
#define HEADER_3D3C3E96A5E1CC65

#include <vector>

//Custom variables (structs)
struct coord {                  //struct for storing coords
    short int x;
    short int y;
};

struct board {                  //stores setup data for board
    int x;                      //height
    int y;                      //width
    std::vector<coord> mines;   //vector for storing mine coords
};

struct endVars {
    bool win;
    bool end;                   //saves from adding another var to 3 functions
};

//constant variables
const char bomb = '*';
const char blank = '-';
const int rationBomb = 5;       //ratio for num of bombs, smaller number->more bombs

int mod(int x, int y);          //division of x / y without remainder

// Game start functions
void init(board& bd);
void bombGen(board& bd);
void checkR(int rx[], int ry[], const coord& s, const board& bdCon);
void boardGen(const board& bdCon, std::vector<std::vector<int>>& bd, std::vector<std::vector<char>>& bdDisp);

// Display functions
void disp(const board& bdCon, std::vector<std::vector<char>>& bdDisp);

// End game functions
bool gameover(bool win);
void dispBombs(std::vector<std::vector<char>>& bdDisp, std::vector<std::vector<int>>& bd, const board& bdCon);
void reset(std::vector<std::vector<int>>& bd, std::vector<std::vector<char>>& bdDisp, board& bdCon);

// Action functions
void guess(coord& g, const board& bdCon);
void zero(coord g, std::vector<std::vector<int>>& bd, std::vector<std::vector<char>>& bdDisp, const board& bdCon);
bool checkWin(std::vector<std::vector<char>>& bdDisp, const board& bdCon);
void action(coord g, std::vector<std::vector<int>>& bd, std::vector<std::vector<char>>& bdDisp, board& bdCon, endVars& e);

#endif // header guard

