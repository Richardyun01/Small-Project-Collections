#include <iostream>
#include <conio.h>
#include <stdlib.h>

#include "Common.h"
#include "Board.h"

using namespace std;

int x, y;
int main_board[HEIGHT][WIDTH]; //x, y
int main_cpy[HEIGHT][WIDTH];
int mblock[4][4];

int main()
{
    Board m;

    x = 4, y = 0;           //init coordinates

    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            mblock[i][j] = m.POS_FREE;
        }
    }

    std::cout << "===============\nPress 1: Start Game\n===============\n";

    int select = 0;
    std::cin >> select;     //get input

    switch (select) {
    case 1:
        m.clear_screen();   //clear screen
        m.init_draw_main(); //initialize board

        m.start();          //start game;
        break;
    default:
        exit(0);
        break;
    }
}
