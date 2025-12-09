#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>

#include "Minesweeper.h"

using namespace std;

//division of x / y without remainder
int mod(int x, int y) {
    return (x / y) - x % y;
}

//ask for the board dimensions and resize the mines vector
void init(board& bd) {
    cout << "Enter board width: ";
    while (true) {  //enter width
        cin >> bd.x;
        if (bd.x >= 5 && bd.x <= 100) break;
        else cout << "Error - enter a number between 5 and 100:";
    }

    cout << "Enter board height: ";
    while (true) {  //enter height
        cin >> bd.y;
        if (bd.y >= 5 && bd.y <= 100) break;
        else cout << "Error - enter a number between 5 and 100:";
    }

    bd.mines.resize(bd.x * bd.y / rationBomb + 1);
}

//generate the coords for the bombs
void bombGen(board& bd) {
    for (int i = 0; i < bd.mines.size() - 1; i++) { //create x mines
        coord temp;
        bool cont = true;
        while (cont == true) {
            //create rand x and y
            temp.x = rand() % bd.x;
            temp.y = rand() % bd.y;
            for (int j = 0; j < bd.mines.size() - 1; j++) { //check for existing mines
                if (bd.mines.at(j).x == temp.x && bd.mines.at(j).y == temp.y) {
                    cont = true;
                    break;                          //stop if there is already a bomb there
                } else {
                    cont = false;                   //set cont to false to break the while loop
                }
            }
        }
        bd.mines.at(i) = temp;
    }
}

//determine the ranges for finding the mines
void checkR(int rx[], int ry[], const coord& s, const board& bdCon) {
    //reset ranges
    rx[0] = -1; rx[1] = 2; ry[0] = -1; ry[1] = 2;

    //deside to change ranges
    if (s.x == 0) {
        rx[0] = 0;
    } else if (s.x == bdCon.x - 1) {
        rx[1] = 1;
    } else {
        rx[0] = -1;
        rx[1] = 2;
    }

    if (s.y == 0) {
        ry[0] = 0;
    } else if (s.y == bdCon.y) {
        ry[1] = 1;
    } else {
        ry[0] = -1;
        ry[1] = 2;
    }
}

/*
    0 means empty space
    9 means bomb
    nums 1-8 mean the num of bombs in the proximity
*/
void boardGen(const board& bdCon, std::vector<std::vector<int>>& bd, std::vector<std::vector<char>>& bdDisp) {
    for (int i = 0; i < bdCon.y - 1; i++) {
        for (int j = 0; j < bdCon.x - 1; j++) {
            for (int k = 0; k < bdCon.mines.size() - 1; k++) {
                if (bdCon.mines.at(k).x == j && bdCon.mines.at(k).y == i)
                    bd[j][i] = 9;
            }
        }
    }

    //Create the numbers on the board
    for (int i = 0; i < bdCon.y; i++) {     //position y
        for (int j = 0; j < bdCon.x; j++) { //position x
            int asNum = 0, rx[2], ry[2];
            coord s;
            s.x = j; s.y = i;
            checkR(rx, ry, s, bdCon);       //set search ranges

            //check surrounding area
            if (bd[j][i] != 9) {
                for (int k = ry[0]; k < ry[1]; k++) {
                    for (int l = rx[0]; l < rx[1]; l++) {
                        if (bd[j + l][i + k] == 9) asNum++;
                    }
                }
                bd[j][i] = asNum;
            }
        }
    }

    for (int i = 0; i < bdCon.y; i++) {     //sets all spaces of display board to the blank char
        for (int j = 0; j < bdCon.x; j++) {
            bdDisp[j][i] = blank;
        }
        cout << endl;
    }
}

//displays the gameBoard
void disp(const board& bdCon, std::vector<std::vector<char>>& bdDisp) {
    cout << " ";
    for (int i = 0; i < bdCon.y + 2; i++) {     //loop through y vals
        for (int j = 0; j < bdCon.x + 1; j++) { //loop through x vals
            if (i == 0) {
                cout << j << " ";
            } else if (i == 1) {
                cout << "__";                   //top of board > add line
            } else {
                if (j == 0) {                   //edge of board > add line
                    if (i > 10) cout << i - 1 << "|";
                    else cout << i - 1 << " |";
                } else {
                    cout << " " << bdDisp[j-1][i-2];
                }
            }
        }
        cout << endl;
    }
}

bool gameover(bool win) {
    char ag;
    bool again;
    if (win){
        cout << "\n\n---------------------------You won!---------------------------"<< endl << endl;
    } else {
        cout << "\n\n---------------------------You lost!---------------------------"<< endl << endl;
    }

    cout << "Do you want to play again(y/n): ";
    while (true) {
        cin >> ag;
        if (ag == 'y') {
            again = true;
            break;
        } else if (ag == 'n') {
            again = false;
            break;
        } else {
            cout << "Error - please enter y or n: ";
        }
    }

    return again;
}

void dispBombs(std::vector<std::vector<char>>& bdDisp, std::vector<std::vector<int>>& bd, const board& bdCon) {
    for (int i = 0; i < bdCon.y; i++) { //go through all the mine locations and set the display for each coord
        for (int j = 0; j < bdCon.x; j++) {
            if (bd[j][i] == 9) {
                bdDisp[j][i] = bomb;
            }
        }
    }
}

void reset(std::vector<std::vector<int>>& bd, std::vector<std::vector<char>>& bdDisp, board& bdCon) {
    for (int i = 0; i < bdCon.y; i++) { //reset all coord
        for (int j = 0; j < bdCon.x; j++) {
            bdDisp[j][i] = blank;
        }
    }

    for (int i = 0; i < bdCon.y; i++) { //reset all coord
        for (int j = 0; j < bdCon.x; j++) {
            bd[j][i] = 0;
        }
    }
}

//enter your guess coords
void guess(coord& g, const board& bdCon) {
    cout << endl << "Enter the x of your guess: ";
    while (true) {  //enter x
        cin >> g.x;
        if (g.x > 0 && g.x < bdCon.x + 1) {
            g.x--;
            break;
        } else {
            cout << endl << "Error, enter a number between 1 and " << bdCon.x << ": ";
        }
    }

    cout << endl << "Enter the y of your guess: ";
    while (true) {  //enter y
        cin >> g.y;
        if (g.y > 0 && g.y < bdCon.y + 1) {
            g.y--;
            break;
        } else {
            cout << endl << "Error, enter a number between 1 and " << bdCon.y << ": ";
        }
    }

    cout << endl << endl << endl;
}

void zero(coord g, std::vector<std::vector<int>>& bd, std::vector<std::vector<char>>& bdDisp, const board& bdCon) {
    vector<coord> found(100000000);             //it just has to be huge

    int rx[2], ry[2];                           //range of search(x), (y)
    int i = 0;
    vector<vector<int>> used(bdCon.x, vector<int>(bdCon.y, 0)); //0=not used, 1 is used
    found.at(0) = g;                            //set first 0 point to be the guess since the guess has been determined to be zero
    int run = 1;

    do {
        coord inter;                            //temp holder
        inter = found.at(i);
        checkR(rx, ry, inter, bdCon);
        used[inter.x][inter.y] = 1;             //add current zero to used list
        for (int j = ry[0]; j < ry[1]; j++) {   //search around poi
            for (int k = rx[0]; k < rx[1]; k++) {
                bdDisp[inter.x + k][inter.y + j] = char(bd[inter.x + k][inter.y + j] + 48);
                if (j == 0 && k == 0) {         //dont want to count the poi again

                } else {
                    if (bd[inter.x + k][inter.y + j] == 0 && used[inter.x + k][inter.y + j] == 0) {
                        found.at(run).x = inter.x + k;  //add new zero to list
                        found.at(run).y = inter.y + j;
                        run++;                          //adds to the total runs
                    }
                }
            }
        }
        i++;
    } while (i < run);
}

//If the number of blanks is equal to the number of bombs generated then the user wins
bool checkWin(std::vector<std::vector<char>>& bdDisp, const board& bdCon) {
    int i = 0;
    bool w = false;
    for (int j = 0; j < bdCon.y; j++) {     //counts the num of blanks
        for (int k = 0; k < bdCon.x; k++) {
            if (bdDisp[k][j] == blank) {
                i++;
            }
        }
    }

    if (i <= bdCon.mines.size()) w = true;  //compares to num of mines
    else w = false;

    return w;
}

//hub for controling all the actions depending on what the user guesses
void action(coord g, std::vector<std::vector<int>>& bd, std::vector<std::vector<char>>& bdDisp, board& bdCon, endVars& e) {
    if (bd[g.x][g.y] == 9) {                        //user guessed a mine location
        dispBombs(bdDisp, bd, bdCon);
        disp(bdCon, bdDisp);
        e.end = true;
        e.win = false;
    } else if (bd[g.x][g.y] == 0) {                 //user guessed a zero location
        zero(g, bd, bdDisp, bdCon);
    } else if (checkWin(bdDisp, bdCon)) {           //Check to see if the user has won
        e.end = true;
        e.win = true;
    } else {
        bdDisp[g.x][g.y] = char(bd[g.x][g.y] + 48); //other wise just display the number
    }
}
