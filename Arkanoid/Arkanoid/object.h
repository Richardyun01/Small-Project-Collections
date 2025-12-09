#ifndef __OBJECTS_H_
#define __OBJECTS_H_

#include <math.h>
#include <GL/glut.h>

const float sdepth = 10;

const GLfloat BoxVerts[][3] = {
    {-1., -1., -1.},
    {-1., -1.,  1.},
    {-1.,  1., -1.},
    {-1.,  1.,  1.},
    { 1., -1., -1.},
    { 1., -1.,  1.},
    { 1.,  1., -1.},
    { 1.,  1.,  1.}
};

const GLfloat bNorms[][3] = {
    {-1.,  0.,  0.},
    { 1.,  0.,  0.},
    { 0.,  1.,  0.},
    { 0., -1.,  0.},
    { 0.,  0., -1.},
    { 0.,  0.,  1.}
};

const int cubeIndices[][4] = {
    {0, 1, 3, 2},
    {4, 6, 7, 5},
    {2, 3, 7, 6},
    {0, 4, 5, 1},
    {0, 2, 6, 4},
    {1, 5, 7, 3}
};

class CSphere;

class CObject {
public:
    float center_x, center_y, center_z;
    float color_r, color_g, color_b;

public:
    CObject() {
        center_x = center_y = center_z = 0.;
    }

    virtual ~CObject() {}

    virtual void setCenter(float x, float y, float z) {
        center_x = x; center_y = y; center_z = z;
    }

    virtual void setColor(float r, float g, float b) {
        _color_r = r; _color_g = g; _color_b = b;
    }

    virtual void draw() {
        glLoadIdentity();
        glTranslatef(0., 0., -sdepth);
        glMultMatrixd(_mRotate);
        glTranslated(center_x, center_y, center_z);
        glColor3f(_color_r, _color_g, _color_b);
    }

    virtual void rotate(int rotate_x, int rotate_y) {
        glMatrixMode(GL_MODELVIEW);
        glPushMatrix();
        glLoadIdentity();
        glRotated(((double)rotate_y), 1., 0., 0.);
        glRotated(((double)rotate_x), 0., 1., 0.);
        glGetDoublev(GL_MODELVIEW_MATRIX, _mRotate);
        glPopMatrix();
    }

    virtual bool hasIntersected(CSphere& ball) = 0;
    virtual void hitBy(CSphere& ball) = 0;

private:
    GLdouble _mRotate[16];
    float _color_r, _color_g, _color_b;
};

class CSphere : public CObject {
public:
    const float radius = 0.35;
    float dir_x, dir_y, dir_z;
    float speed;

public:
    CSphere() {}
    virtual ~CSphere() {}

    void draw()
    {
        CObject::draw();
        glutSolidSphere(radius, 20, 16);
    }

    bool hasIntersected(CSphere& ball) {
        float dist = (center_x - ball.center_x) * (center_x - ball.center_x) +
                     (center_z - ball.center_z) * (center_z - ball.center_z);
        return sqrt(dist) < radius*2;
    }

    void hitBy(CSphere& ball) {
        ball.dir_x = ball.center_x - center_x;
        ball.dir_z = -ball.dir_z;
    }
};

class CWall : public CObject {
public:
    CWall() {}
    virtual ~CWall() {}

    void setSize(float w, float h, float d)
    {
        width = w; height = h; depth = d;
        for (int i = 0; i < 8; i++) {
            Verts[i][0] = w/2. * BoxVerts[i][0];
            Verts[i][1] = h/2. * BoxVerts[i][1];
            Verts[i][2] = d/2. * BoxVerts[i][2];
        }
    }

    void draw()
    {
        CObject::draw();

        for (int i = 0 ; i < 6 ; i++) {
            int v1 = cubeIndices[i][0];
            int v2 = cubeIndices[i][1];
            int v3 = cubeIndices[i][2];
            int v4 = cubeIndices[i][3];

            glBegin(GL_QUADS) ;
            glNormal3f(bNorms[i][0], bNorms[i][1], bNorms[i][2]);
            glVertex3f(Verts[v1][0], Verts[v1][1], Verts[v1][2]);
            glNormal3f(bNorms[i][0], bNorms[i][1], bNorms[i][2]);
            glVertex3f(Verts[v2][0], Verts[v2][1], Verts[v2][2]);
            glNormal3f(bNorms[i][0], bNorms[i][1], bNorms[i][2]);
            glVertex3f(Verts[v3][0], Verts[v3][1], Verts[v3][2]);
            glNormal3f(bNorms[i][0], bNorms[i][1], bNorms[i][2]);
            glVertex3f(Verts[v4][0], Verts[v4][1], Verts[v4][2]);
            glEnd () ;
        }
    }

    bool hasIntersected(CSphere& ball) {
        float x1 = center_x - width*0.5 - ball.radius;
        float x2 = center_x + width*0.5 + ball.radius;
        float z1 = center_z - depth*0.5 - ball.radius;
        float z2 = center_z + depth*0.5 + ball.radius;
        return x1 < ball.center_x && ball.center_x < x2 &&
               z1 < ball.center_z && ball.center_z < z2;
    }

    void hitBy(CSphere& ball) {
        if (width < depth) ball.dir_x = -ball.dir_x;
        else ball.dir_z = -ball.dir_z;
    }

private:
    float width, height, depth;
    GLfloat Verts[8][3];
};

#endif // __OBJECTS_H_
