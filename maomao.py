from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math

# ! --------------------------------------- :TODO: ---------------------------------------
# ! --------------------------------------- :TODO: ---------------------------------------
# ! --------------------------------------- :TODO: ---------------------------------------
# TODO: Make House Class
# TODO: Make Fence Class
# TODO: Make Road Class
# TODO: Make Car Class
# TODO: Make Pond Class
# TODO: Make Farmable Plot Class [With Crop Specifier]
# TODO: Make Cows Barn Class
# TODO: Make Hens Barn Class
# TODO: Make Cows Class
# TODO: Make Hens Class
# TODO: Make Crops Class [Wheat, Potato, Carrot, Sunflower]
# TODO: Make Player Class [A Cat Humanoid]
# TODO: Design User Interface

# ! --------------------------------------- Global Variables ---------------------------------------
# ! --------------------------------------- Global Variables ---------------------------------------
# ! --------------------------------------- Global Variables ---------------------------------------

# ! Camera and Window Global Keys
W, H = 1280, 720
FOV = 100
CAMERA_Z_REWORK = 0

# ! Player Movement
BUTTONS = {"w": False, "s": False, "a": False, "d": False}

STEP = 0.1
ROTATE_ANGLE = 0.1

# ! --------------------------------------- CLasses ---------------------------------------
# ! --------------------------------------- CLasses ---------------------------------------
# ! --------------------------------------- CLasses ---------------------------------------


# ! Player
class Player:
    def __init__(self, position):
        self.position = position
        self.rotation = 0

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def rotate(self, angle):
        self.rotation += angle
        self.rotation %= 360

    def draw(self):
        glPushMatrix()
        # Move to player position
        glTranslatef(self.position[0], self.position[1], self.position[2])
        # Rotate player
        glRotatef(self.rotation, 0, 0, 1)

        # Draw legs (2 cubes)
        leg_width, leg_height, leg_depth = 2, 6, 2
        body_width, body_height, body_depth = 6, 10, 4
        head_radius = 3

        # Left leg
        glPushMatrix()
        glTranslatef(0, -body_width / 4, leg_height / 2)
        glScalef(leg_depth, leg_width, leg_height)
        glColor3f(0.6, 0.4, 0.2)
        glutSolidCube(1)
        glPopMatrix()

        # Right leg
        glPushMatrix()
        glTranslatef(0, body_width / 4, leg_height / 2)
        glScalef(leg_depth, leg_width, leg_height)
        glColor3f(0.6, 0.4, 0.2)
        glutSolidCube(1)
        glPopMatrix()

        # Body (cube)
        glPushMatrix()
        glTranslatef(0, 0, leg_height + body_height / 2)
        glScalef(body_depth, body_width, body_height)
        glColor3f(1.0, 0.8, 0.6)
        glutSolidCube(1)
        glPopMatrix()

        # Head (sphere)
        glPushMatrix()
        glTranslatef(0, 0, leg_height + body_height + head_radius)
        glColor3f(1.0, 0.9, 0.7)
        glutSolidSphere(head_radius, 20, 20)
        glPopMatrix()

        # Left hand (facing forward)
        glPushMatrix()
        glTranslatef(0, -body_width / 2 - 1, leg_height + body_height * 0.8)
        glRotatef(90, 1, 0, 0)  # Rotate to face forward
        glScalef(2, 2, 6)
        glColor3f(0.8, 0.6, 0.4)
        glutSolidCube(1)
        glPopMatrix()

        # Right hand (facing forward)
        glPushMatrix()
        glTranslatef(0, body_width / 2 + 1, leg_height + body_height * 0.8)
        glRotatef(90, 1, 0, 0)  # Rotate to face forward
        glScalef(2, 2, 6)
        glColor3f(0.8, 0.6, 0.4)
        glutSolidCube(1)
        glPopMatrix()

        glPopMatrix()


MAOMAO = Player([0, 0, 0])


# ! --------------------------------------- Draw Functions ---------------------------------------
# ! --------------------------------------- Draw Functions ---------------------------------------
# ! --------------------------------------- Draw Functions ---------------------------------------


def farmLand():
    glColor3f(0.0, 0.8, 0.0)  # Grass green color
    glBegin(GL_QUADS)
    glVertex3f(-500, -500, 0)
    glVertex3f(500, -500, 0)
    glVertex3f(500, 500, 0)
    glVertex3f(-500, 500, 0)
    glEnd()


# ! --------------------------------------- Input Functions ---------------------------------------
# ! --------------------------------------- Input Functions ---------------------------------------
# ! --------------------------------------- Input Functions ---------------------------------------


def keyboardListener(key, x, y):
    global BUTTONS

    # ! Move forward (W key)
    if key.lower() == b"w":
        BUTTONS["w"] = True

    # ! Move backward (S key)
    if key.lower() == b"s":
        BUTTONS["s"] = True

    # ! Move left (A key)
    if key.lower() == b"a":
        BUTTONS["a"] = True

    # ! Move right (D key)
    if key.lower() == b"d":
        BUTTONS["d"] = True

    # ! Escape key to exit game
    if key == b"\x1b":
        glutLeaveMainLoop()


def keyboardUpListener(key, x, y):
    global BUTTONS

    # ! Move forward (W key)
    if key.lower() == b"w":
        BUTTONS["w"] = False

    # ! Move backward (S key)
    if key.lower() == b"s":
        BUTTONS["s"] = False

    # ! Move left (A key)
    if key.lower() == b"a":
        BUTTONS["a"] = False

    # ! Move right (D key)
    if key.lower() == b"d":
        BUTTONS["d"] = False


def specialKeyListener(key, x, y):
    pass


def mouseListener(button, state, x, y):
    global FOV, CAMERA_Z_REWORK

    # ? Scroll Up:
    if button == 3 and state == GLUT_DOWN:
        FOV = max(FOV - 5, 90)
        CAMERA_Z_REWORK = max(CAMERA_Z_REWORK - 5, -20)

    # ? Scroll Down:
    elif button == 4 and state == GLUT_DOWN:
        FOV = min(FOV + 5, 110)
        CAMERA_Z_REWORK = min(CAMERA_Z_REWORK + 5, 10)

    glutPostRedisplay()


# ! --------------------------------------- Camera Function ---------------------------------------
# ! ------------------------------------- ShowScreen Function -------------------------------------
# ! ---------------------------------------- Idle Function ----------------------------------------


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV, W / H, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    px, py, pz = MAOMAO.position

    distance = 60
    height = 50
    angle_rad = math.radians(MAOMAO.rotation)
    cam_x = px - distance * math.cos(angle_rad)
    cam_y = py - distance * math.sin(angle_rad)
    cam_z = pz + height + CAMERA_Z_REWORK
    gluLookAt(cam_x, cam_y, cam_z, px, py, pz, 0, 0, 1)


def showScreen():
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, W, H)
    glClearColor(0.2, 0.2, 0.2, 1)
    setupCamera()

    MAOMAO.draw()

    farmLand()

    # ? Double Buffering - Smoothness
    glutSwapBuffers()


def idle():
    if BUTTONS["a"]:
        MAOMAO.rotate(ROTATE_ANGLE)  # Rotate left
    if BUTTONS["d"]:
        MAOMAO.rotate(-ROTATE_ANGLE)  # Rotate right

    angle_rad = math.radians(MAOMAO.rotation)
    if BUTTONS["w"]:
        dx = STEP * math.cos(angle_rad)
        dy = STEP * math.sin(angle_rad)
        MAOMAO.move(dx, dy)
    if BUTTONS["s"]:
        dx = -STEP * math.cos(angle_rad)
        dy = -STEP * math.sin(angle_rad)
        MAOMAO.move(dx, dy)

    glutPostRedisplay()


# ! --------------------------------------- MAIN ---------------------------------------
# ! --------------------------------------- MAIN ---------------------------------------
# ! --------------------------------------- MAIN ---------------------------------------


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(W, H)
    glutInitWindowPosition(200, 100)
    glutCreateWindow(b"MaoMao's Farm - The Game")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()
