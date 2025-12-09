#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>

#include "Minesweeper.h"

using namespace std;

int main()
{
    srand(time(NULL));

    board bdCon;
    coord g;
    endVars e;

    e.win = false;
    e.end = false;

    init(bdCon);
    bombGen(bdCon);

    vector<vector<int>> bd(bdCon.y, vector<int>(bdCon.x, 0));
    vector<vector<char>> bdDisp(bdCon.y, vector<char>(bdCon.x, blank));

    boardGen(bdCon, bd, bdDisp);
    disp(bdCon, bdDisp);

    while (true) {
        guess(g, bdCon);
        action(g, bd, bdDisp, bdCon, e);
        if (e.end) {
            if (gameover(e.win)) {          //reset game
                init(bdCon);
                bombGen(bdCon);
                reset(bd, bdDisp, bdCon);
                boardGen(bdCon, bd, bdDisp);
                disp(bdCon, bdDisp);
                e.end = false;
            } else {
                cout<<"\n\n\n               Thanks for playing!      "<<endl<<endl<<endl<<endl;
                break;
            }
        } else {
            disp(bdCon, bdDisp);
        }
    }

    return 0;
}
