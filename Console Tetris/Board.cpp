#include <iostream>
#include <conio.h>
#include <stdio.h>
#include <stdlib.h>

#include "Common.h"
#include "Board.h"

void Board::control_user_input() {
    char key = getch();

    switch (key) {
    case 'd':
        if (!is_collide(x+1, y)) {
            move_block(x+1, y);
        }
        break;
    case 'a':
        if (!is_collide(x-1, y)) {
            move_block(x-1, y);
        }
        break;
    case 's':
        if (!is_collide(x, y+1)) {
            move_block(x, y+1);
        }
        break;
    case 'w':
        rotate_block();
    }
}

void Board::save_present_board_to_cpy() {
    for (size_t i = 0; i < HEIGHT - 1; i++) {
        for (size_t j = 0; j < WIDTH - 1; j++) {
            main_cpy[i][j] = main_board[i][j];
        }
    }
}

void Board::start() {
    size_t time_cnt = 0;
    size_t MAX = 20000;

    while (is_game_over() == false) {
        if (kbhit()) control_user_input();

        if (time_cnt < MAX) {
            time_cnt++;
        } else {
            processing_block();
            time_cnt = 0;
        }
    }

    std::cout << "===============\nGame Over\n===============\n";

    exit(0);
}

void Board::clear_screen() {
    system("cls");
}

void Board::init_draw_main() {
    for (size_t i = 0; i < HEIGHT - 1; i++) {
        for (size_t j = 0; j < WIDTH - 2; j++) {
            if ((j == 0) || (j == WIDTH - 2) || (i == HEIGHT - 2)) {
                main_board[i][j] = POS_BORDER;
                main_cpy[i][j] = POS_BORDER;
            } else {
                main_board[i][j] = POS_FREE;
                main_cpy[i][j] = POS_FREE;
            }
        }
    }

    clear_line();
    new_block();
    re_draw_main();
}
void Board::re_draw_main() {
    clear_screen();

    for (size_t i = 0; i < HEIGHT - 1; i++) {
        for (size_t j = 0; j < WIDTH - 1; j++) {
            switch (main_board[i][j]) {
            case POS_FREE:
                std::cout << " " << std::flush;
                break;
            case POS_FILLED:
                std::cout << "@" << std::flush;
                break;
            case POS_BORDER:
                std::cout << "$" << std::flush;
                break;
            }
        }
        std::cout << std::endl;
    }
}

int Board::getRandom(int min, int max) {
    return rand() % (max - min + 1) + min;
}

void Board::new_block() {
    x = 4, y = 0;

    Block m;
    int blockType = getRandom(0, 6);
    int rotation = getRandom(0, 3);

    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            mblock[i][j] = POS_FREE;
            mblock[i][j] = m.GetBlockType(blockType, rotation, i, j);
        }
    }

    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            main_board[i][x + j] = main_cpy[i][x + j] + mblock[i][j];

            if (main_board[i][x + j] > 1) {
                isGameOver = true;
            }
        }
    }
}

void Board::move_block(int x2, int y2) {
    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            main_board[y + i][x + j] -= mblock[i][j];
        }
    }

    x = x2, y = y2;

    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            main_board[y + i][x + j] += mblock[i][j];
        }
    }

    re_draw_main();
}

void Board::rotate_block() {
    int tmp[4][4];

    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            tmp[i][j] = mblock[i][j];
        }
    }

    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            mblock[i][j] = tmp[3 - i][j];
        }
    }

    if (is_collide(x, y)) {
        for (size_t i = 0; i < 4; i++) {
            for (size_t j = 0; j < 4; j++) {
                mblock[i][j] = tmp[i][j];
            }
        }
    }

    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            main_board[y + i][x + j] -= tmp[i][j];
            main_board[y + i][x + j] += mblock[i][j];
        }
    }

    re_draw_main();
}

void Board::clear_line() {
    for (int j = 0; j <= HEIGHT - 3; j++) {
        int i = 1;
        while (i <= WIDTH - 3) {
            if (main_board[j][i] == POS_FREE) {
                break;
            }
            i++;
        }

        if (i == WIDTH - 2) {
            for (int k = j; k > 0; k--) {
                for (int l = 1; l <= WIDTH - 3; l++) {
                    main_board[k][l] = main_board[k - 1][l];
                }
            }
        }
    }
}

bool Board::is_collide(int x2, int y2) {
    for (size_t i = 0; i < 4; i++) {
        for (size_t j = 0; j < 4; j++) {
            if (mblock[i][j] && main_cpy[y2 + i][x2 + j] != 0) {
                return true;
            }
        }
    }

    return false;
}

bool Board::is_game_over() {
    return isGameOver;
}

void Board::processing_block() {
    if (!is_collide(x, y+1)) {
        move_block(x, y+1);
    } else {
        clear_line();
        save_present_board_to_cpy();
        new_block();
        re_draw_main();
    }
}
