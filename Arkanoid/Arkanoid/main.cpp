#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include "object.h"

//GLdouble rotMatrix[4][16];
const int MAX_LIVES = 5;
const int NO_SPHERE=52;

class Arkanoid {
public:
    Arkanoid() { init(); }

    void init() {
        const float coord[NO_SPHERE][2] = {
            {-2.8, -8.0}, {2.8, -8.0},
            {-2.0, -8.0}, {2.0, -8.0},
            {-1.2, -8.0}, {1.2, -8.0},
            {-0.4, -8.0}, {0.4, -8.0},
            {-3.4, -7.4}, {3.4, -7.4},
            {-4.0, -6.8}, {4.0, -6.8},
            {-4.0, -6.0}, {4.0, -6.0},
            {-4.0, -5.2}, {4.0, -5.2},
            {-4.0, -4.4}, {4.0, -4.4},
            {-4.0, -3.6}, {4.0, -3.6},
            {-4.0, -2.8}, {4.0, -2.8},
            {-4.0, -2.0}, {4.0, -2.0},
            {-4.0, -1.2}, {4.0, -1.2},
            {-4.0, -0.4}, {4.0, -0.4},
            {-3.4,  0.2}, {3.4,  0.2},
            {-2.8,  0.8}, {2.8,  0.8},
            {-2.0,  0.8}, {2.0,  0.8},
            {-1.2,  0.8}, {1.2,  0.8},
            {-0.4,  0.8}, {0.4,  0.8},
            {-2.0, -6.2}, {2.0, -6.2},
            {-2.0, -5.4}, {2.0, -5.4},
            { 0.0, -3.6}, {0.0, -2.8},
            {-2.8, -2.0}, {2.8, -2.0},
            {-2.0, -1.4}, {2.0, -1.4},
            {-1.2, -0.8}, {1.2, -0.8},
            {-0.4, -0.8}, {0.4, -0.8},
        };
        for (int i = 0; i < NO_SPHERE; i++) {
            _exist[i] = true;
            _sphere[i].setColor(0.8, 0.8, 0);
            _sphere[i].setCenter(coord[i][0], 0, coord[i][1]);
        }
        _numExist = NO_SPHERE;

        _ground.setSize(10., 0.1, 15);
        _ground.setColor(0., 0.6, 0.); _ground.setCenter(0., -0.6, -3);

        _wall[0].setSize(0.2, 1., 15);
        _wall[0].setColor(0.2, 0.2, 0.2); _wall[0].setCenter(-5.1, -0.1, -3);

        _wall[1].setSize(0.2, 1., 15);
        _wall[1].setColor(0.2, 0.2, 0.2); _wall[1].setCenter(5.1, -0.1, -3);

        _wall[2].setSize(10.4, 1., 0.2);
        _wall[2].setColor(0.2, 0.2, 0.2); _wall[2].setCenter(0., -0.1, -10.6);

        waitStart();
    }

    void display() {
        for (int i = 0; i < NO_SPHERE; i++)
            if (_exist[i]) _sphere[i].draw();
        for (int i = 0; i < 3; i++) _wall[i].draw();
        _ball.draw();
        _bar.draw();
        _ground.draw();
        drawText();
    }

    void rotate(int rx, int ry) {
        for (int i = 0; i < NO_SPHERE; i++)
            if (_exist[i]) _sphere[i].rotate(rx, ry);
        for (int i = 0; i < 3; i++) _wall[i].rotate(rx, ry);
        _ball.rotate(rx, ry);
        _bar.rotate(rx, ry);
        _ground.rotate(rx, ry);
    }

    void moveBar(float x) {
        _bar.setCenter(x*10, 0, _bar.center_z);
        if (_waitStart)
            _ball.setCenter(x*10, 0, _ball.center_z);
    }

    void moveBarDelta(float delta) {
        _bar.setCenter(_bar.center_x+delta, 0, _bar.center_z);
        if (_waitStart)
            _ball.setCenter(_ball.center_x+delta, 0, _ball.center_z);
    }

    void moveBall(int delta) {
        if (_waitStart) return;
        _ball.setCenter(_ball.center_x+delta*0.005*_ball.dir_x, 0,
                        _ball.center_z+delta*0.005*_ball.dir_z);

        for (int i = 0; i < NO_SPHERE; i++) {
            if (_exist[i] && _sphere[i].hasIntersected(_ball)) {
                _sphere[i].hitBy(_ball);
                _exist[i] = false;
                _numExist--;
                _score += 100;
                break;
            }
        }
        for (int i = 0; i < 3; i++) {
            if (_wall[i].hasIntersected(_ball)) {
                _wall[i].hitBy(_ball);
                break;
            }
        }
        if (_bar.hasIntersected(_ball)) {
            _bar.hitBy(_ball);
        } else if (!_ground.hasIntersected(_ball)) {
            _lives--;
            waitStart();
        }

        if (_numExist == 0 || _lives == 0) {
            _gameOver = true;
            init();
        }
    }

    void start() {
        if (!_waitStart) return;
        _waitStart = false;
        _ball.dir_x = _ball.dir_y = 0;
        _ball.dir_z = -0.7;
    }

    void waitStart() {
        _waitStart = true;
        _ball.setColor(0.8, 0, 0); _ball.setCenter(0, 0, 3.3);
        _bar.setColor(0.4, 0.4, 0.4); _bar.setCenter(0, 0, 4);
    }

public:
    int _score = 0, _lives = MAX_LIVES, _numExist = NO_SPHERE;
    bool _waitStart = true, _gameOver = false;
    bool _exist[NO_SPHERE];
    CSphere _sphere[NO_SPHERE], _bar, _ball;
    CWall _ground, _wall[3];

    void renderString(float x, float y, float z, const char *str) {
        glRasterPos3f(x, y, z);
        for (const char *c = str; *c; c++)
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, *c);
    }

    void drawText() {
        char str[128];

        glColor3f(0.8, 0, 0);
        sprintf(str, "Lives: %d", _lives);
        renderString(-12, 0, -11, str);

        glColor3f(0, 0, 0);
        sprintf(str, "Score: %d", _score);
        renderString(8, 0, -11, str);

        if (_waitStart)
            renderString(-1, 0, 8, "Press Space to START");

        if (_gameOver) {
            glColor3f(0, 0, 1);
            renderString(-0.8, 1, 0, "Game Over");
        }
    }

};

Arkanoid app;

/////////////////////////////////////////////////////////////

const float zNear=1.0, zFar=100.0;
int rotate_x=0, rotate_y=55;
int downX, downY;
bool leftButton = false, middleButton = false, rightButton = false;

void MyIdleFunc(void) { glutPostRedisplay(); } /* things to do while idle */
void RunIdleFunc(void) { glutIdleFunc(MyIdleFunc); }
void PauseIdleFunc(void) { glutIdleFunc(NULL); }

void ReshapeCallback(int width, int height)
{
    float aspect = (float)width / (float)height;
    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(75.0, aspect, zNear, zFar);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glutPostRedisplay();
}

void DisplayCallback(void)
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);

    app.display();

    glutSwapBuffers();
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
}

int space_flag=0;

void KeyboardCallback(unsigned char ch, int x, int y) {
    switch (ch) {
    case 32 :
        app.start();
        break; // SPACE_KEY
    case 27:
        exit(0);
        break;
    }
    glutPostRedisplay();
}

void SpecialCallback(int key, int x, int y) {
    switch (key) {
    case GLUT_KEY_LEFT:
        app.moveBarDelta(-0.2);
        break;
    case GLUT_KEY_RIGHT:
        app.moveBarDelta(0.2);
        break;
    }
}

void MouseCallback(int button, int state, int x, int y)
{
    downX = x; downY = y;
    leftButton = ((button == GLUT_LEFT_BUTTON) && (state == GLUT_DOWN));
    middleButton = ((button == GLUT_MIDDLE_BUTTON) &&  (state == GLUT_DOWN));
    rightButton = ((button == GLUT_RIGHT_BUTTON) &&  (state == GLUT_DOWN));
    glutPostRedisplay();
}

void MotionCallback(int x, int y) {
    if (leftButton) {
        rotate_x += x - downX;
        rotate_y += y - downY;
        app.rotate(rotate_x, rotate_y);
    } else if (rightButton) {
        //int tdx=x-downX,tdy=0,tdz=y-downY,id=choice-1;
        //if (id<NO_SPHERE) g_sphere[id].setCenter(g_sphere[id].center_x+tdx/100.0,g_sphere[id].center_y+tdy/100.0,g_sphere[id].center_z+tdz/100.0);
    }
    downX = x;   downY = y;
    glutPostRedisplay();
}

void MoveCallback(int x, int y){
    float fx = (float) x / glutGet(GLUT_WINDOW_WIDTH) - 0.5;
    app.moveBar(fx);
    glutPostRedisplay();
}

int currentTime, previousTime=-1;
void renderScene()
{
    int timeDelta;
    currentTime = glutGet(GLUT_ELAPSED_TIME);
    if (previousTime == -1) timeDelta = 0;
    else timeDelta = currentTime - previousTime;
    app.moveBall(timeDelta);
    glutPostRedisplay();
    previousTime = currentTime;

}

int main(int argc, char **argv)
{
    GLfloat light0Position[] = {0, 1, 0, 1.};

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(1024, 1024);
    glutCreateWindow("OpenGL Applications");
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);
    glClearColor(0.7, 0.7, 0.7, 0.0);
    glPolygonOffset(1.0, 1.0);
    glDisable(GL_CULL_FACE);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST);
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
    glEnable(GL_COLOR_MATERIAL);
    glColorMaterial(GL_FRONT, GL_DIFFUSE);
    glLightfv (GL_LIGHT0, GL_POSITION, light0Position);
    glEnable(GL_LIGHT0);
    app.rotate(rotate_x, rotate_y);

    glShadeModel(GL_SMOOTH);
    glEnable(GL_LIGHTING);

    glutIdleFunc(renderScene);
    glutReshapeFunc(ReshapeCallback);
    glutDisplayFunc(DisplayCallback);
    glutKeyboardFunc(KeyboardCallback);
    glutSpecialFunc(SpecialCallback);
    glutMouseFunc(MouseCallback);
    glutMotionFunc(MotionCallback);
    glutPassiveMotionFunc(MoveCallback);

    glutMainLoop();
    return 0;
}
