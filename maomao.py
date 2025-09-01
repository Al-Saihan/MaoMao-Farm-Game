from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import time

# ! --------------------------------------- :TODO: ---------------------------------------
# ! --------------------------------------- :TODO: ---------------------------------------
# ! --------------------------------------- :TODO: ---------------------------------------
# TODO: Make House Class --------------------------------------
# TODO: Make Fence Class --------------------------------------
# TODO: Make Road Class ---------------------------------------
# TODO: Make Car Class ----------------------------------------
# TODO: Make Pond Class ---------------------------------------
# TODO: Make Farmable Plot Class [With Crop Specifier] --------
# TODO: Make Cows Barn Class ---------------------------------- Nusayba
# TODO: Make Hens Barn Class ---------------------------------- Nusayba
# TODO: Make Cows Class ---------------------------------------
# TODO: Make Hens Class ---------------------------------------
# TODO: Make Crops Class [Wheat, Potato, Carrot, Sunflower] ---
# TODO: Make Player Class [A Cat Humanoid] -------------------- Saihan
# TODO: Design User Interface

# ! --------------------------------------- Global Variables ---------------------------------------
# ! --------------------------------------- Global Variables ---------------------------------------
# ! --------------------------------------- Global Variables ---------------------------------------

# ! Camera and Window Global Keys
W, H = 1280, 720
FOV = 30  # TODO:  DEFEAULT IS 100, PLEASE CHANGE IT BACK TO 100 IF CHANGED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! (God Bless You) [Saihan]
CAMERA_Z_REWORK = 0
CAMERA_EXTRA_TURN = 0
SELFIE = False

# ! Buttons
BUTTONS = {"w": False, "s": False, "a": False, "d": False, "la": False, "ra": False}

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
        # ! Please don't ask how I did this, my head hurts from all the trial & errors + calculations I had to do on paper [Saihan]

        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation, 0, 0, 1)  # Rotate around Z-axis (facing X+ initially)

        # ! Variables
        leg_width, leg_height, leg_depth = 1.8, 7, 1.8
        body_width, body_height, body_depth = 5, 8, 3
        head_radius = 3
        arm_width, arm_height, arm_depth = 1.5, 6, 1.5
        tail_length, tail_width = 1, 0.5
        leg_swing_angle = 0
        arm_swing_angle = 0
        rotateVar = math.sin(glutGet(GLUT_ELAPSED_TIME) / 200.0) * 15
        if BUTTONS["w"] or BUTTONS["s"]:
            # ? Animate walking
            time = glutGet(GLUT_ELAPSED_TIME) / 50.0
            leg_swing_angle = 35 * math.sin(time)
            
            # ! +Pi Reverse Arm Swing Compared with Leg
            arm_swing_angle = 20 * math.sin(time + math.pi)

        # ? Left leg
        glPushMatrix()
        glTranslatef(0, -body_width / 3, leg_height / 2)
        glRotatef(leg_swing_angle, 0, 1, 0)  # ! Left Leg Swing
        glScalef(leg_depth, leg_width, leg_height)
        glColor3f(0.3, 0.3, 0.3)  # ! Light dark gray
        glutSolidCube(1)
        glPopMatrix()

        # ? Right leg
        glPushMatrix()
        glTranslatef(0, body_width / 3, leg_height / 2)
        glRotatef(-leg_swing_angle, 0, 1, 0)  # ! Right Leg Swing
        glScalef(leg_depth, leg_width, leg_height)
        glColor3f(0.3, 0.3, 0.3)  # ! Light dark gray
        glutSolidCube(1)
        glPopMatrix()

        # ? Body
        glPushMatrix()
        glTranslatef(0, 0, leg_height + body_height / 2)
        glScalef(body_depth, body_width, body_height)
        glColor3f(0.95, 0.6, 0.8)  # ! Pink
        glutSolidCube(1)
        glPopMatrix()

        # ! HEAD START
        glPushMatrix()
        glTranslatef(0, 0, leg_height + body_height + head_radius * 0.8)

        # ? Head
        glPushMatrix()
        glScalef(1.0, 1.0, 1.1)
        glColor3f(0.92, 0.82, 0.66)  # ! HUMAN SKIN COLOR, BEHOLD
        glutSolidSphere(head_radius, 30, 30)
        glPopMatrix()

        # ? Left ear
        glPushMatrix()
        glTranslatef(0, -head_radius * 0.5, head_radius * 0.8)
        glRotatef(40, 1, 0, 0)
        glColor3f(0.5, 0.5, 0.5)  # ! Lighter dark gray
        glScalef(0.7, 1.0, 1.0)
        glutSolidCone(1.4, 2.5, 10, 10)
        glPopMatrix()

        # ? Right ear
        glPushMatrix()
        glTranslatef(0, head_radius * 0.5, head_radius * 0.8)
        glRotatef(-40, 1, 0, 0)
        glColor3f(0.5, 0.5, 0.5)  # ! Lighter dark gray
        glScalef(0.7, 1.0, 1.0)
        glutSolidCone(1.4, 2.5, 10, 10)
        glPopMatrix()

        # ? Left eye
        glPushMatrix()
        glTranslatef(head_radius * 0.7, -head_radius * 0.4, head_radius * 0.6)
        glRotatef(10, 0, 0, 1)
        glScalef(0.8, 0.3, 0.4)
        glColor3f(0.1, 0.1, 0.1)  # ! Black
        glutSolidSphere(0.8, 10, 10)
        glPopMatrix()

        # ? Right eye
        glPushMatrix()
        glTranslatef(head_radius * 0.7, head_radius * 0.4, head_radius * 0.6)
        glRotatef(-10, 0, 0, 1)
        glScalef(0.8, 0.3, 0.4)
        glColor3f(0.1, 0.1, 0.1)  # ! Black
        glutSolidSphere(0.8, 10, 10)
        glPopMatrix()

        # ? Left Whisker
        # TODO: MATHA BETHA KORE, I ADD LATER

        # ? Right Whisker
        # TODO: MATHA BETHA KORE, I ADD LATER

        glPopMatrix()
        # ! END HEAD

        # ? Left arm
        glPushMatrix()
        glTranslatef(0, -body_width / 2 - arm_width / 2, leg_height + body_height * 0.7)
        glRotatef(arm_swing_angle, 0, 1, 0)  # ! Left Swing Arm
        glScalef(arm_depth, arm_width, arm_height)
        glColor3f(0.3, 0.3, 0.3)  # ! Light dark gray
        glutSolidCube(1)
        glPopMatrix()

        # ? Right arm
        glPushMatrix()
        glTranslatef(0, body_width / 2 + arm_width / 2, leg_height + body_height * 0.7)
        glRotatef(-arm_swing_angle, 0, 1, 0)  # ! Right Arm Swing
        glScalef(arm_depth, arm_width, arm_height)
        glColor3f(0.3, 0.3, 0.3)  # ! Light dark gray
        glutSolidCube(1)
        glPopMatrix()

        # # ? Tail
        # glPushMatrix()
        # glTranslatef(-body_depth / 2, 0, leg_height + 3)
        # glRotatef(-20, 0, 1, 0)
        # glRotatef(rotateVar, 1, 0, 0)  # ! Tail Move
        # glScalef(tail_width, tail_width, tail_length)
        # glColor3f(0.3, 0.3, 0.3)  # ! Light dark gray
        # glutSolidCube(1)
        # glPopMatrix()

        # ? Tail v2
        glPushMatrix()
        glTranslatef(-body_depth / 2 - 7, 0, leg_height + 6)
        glScalef(tail_width, tail_width, tail_length)
        glRotatef(270, 0, 1, 0)
        glColor3f(0.3, 0.3, 0.3)  # ! Light dark gray

        x = 0.0
        while x <= 5.0:
            glPointSize(5)
            glBegin(GL_POINTS)

            speed = 0.005 * glutGet(GLUT_ELAPSED_TIME)
            y = 0.5 * (math.sin(x - speed) + math.sin(speed))
            z = 0.0

            glVertex3f(x, y, z)
            glEnd()

            x += 0.05 # ? This controls the smoothness of the tail / Step Size

        glPopMatrix()
        
        glPopMatrix()


MAOMAO = Player([0, 0, 0])


# ! --------------------------------------- Draw Functions ---------------------------------------
# ! --------------------------------------- Draw Functions ---------------------------------------
# ! --------------------------------------- Draw Functions ---------------------------------------


def farmLand():
    glColor3f(0.0, 0.8, 0.0)  # Grass green color
    glBegin(GL_QUADS)
    glVertex3f(-750, -600, 0)
    glVertex3f(750, -600, 0)
    glVertex3f(750, 750, 0)
    glVertex3f(-750, 750, 0)
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
    global BUTTONS, SELFIE

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

    # ! Selfie Mode (V Key)
    if key == b"v":
        SELFIE = not SELFIE


def specialKeyListener(key, x, y):
    if key == GLUT_KEY_LEFT:
        BUTTONS["la"] = True
    elif key == GLUT_KEY_RIGHT:
        BUTTONS["ra"] = True

def specialKeyUpListener(key, x, y):
    if key == GLUT_KEY_LEFT:
        BUTTONS["la"] = False
    elif key == GLUT_KEY_RIGHT:
        BUTTONS["ra"] = False



def mouseListener(button, state, x, y):
    global FOV, CAMERA_Z_REWORK, SELFIE

    zoomUpStep = 6
    zoomDownStep = 2

    # ? Scroll Up:
    if button == 3 and state == GLUT_DOWN:
        FOV = max(FOV - zoomUpStep, 90)
        CAMERA_Z_REWORK = max(CAMERA_Z_REWORK - zoomUpStep, -(4 * zoomUpStep))

    # ? Scroll Down:
    if button == 4 and state == GLUT_DOWN:
        FOV = min(FOV + zoomDownStep, 110)
        CAMERA_Z_REWORK = min(CAMERA_Z_REWORK + zoomDownStep, (2 * zoomDownStep))

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
    angle_rad = math.radians(MAOMAO.rotation + CAMERA_EXTRA_TURN) 

    if SELFIE:
        cam_x = px + distance * math.cos(angle_rad)
        cam_y = py + distance * math.sin(angle_rad)
    else:
        cam_x = px - distance * math.cos(angle_rad)
        cam_y = py - distance * math.sin(angle_rad)

    cam_z = pz + height + CAMERA_Z_REWORK

    gluLookAt(cam_x, cam_y, cam_z, px, py, pz, 0, 0, 1)


def showScreen():
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, W, H)
    glClearColor(0.53, 0.81, 0.92, 1)  # Sky blue color
    setupCamera()

    MAOMAO.draw()

    farmLand()

    # ? Double Buffering - Smoothness
    glutSwapBuffers()


def devDebug():
    if not hasattr(devDebug, "last_print_time"):
        devDebug.last_print_time = time.time()

    current_time = time.time()
    if current_time - devDebug.last_print_time >= 1.0:
        x, y, z = MAOMAO.position
        print(
            f"{glutGet(GLUT_ELAPSED_TIME)} : Player Currently At - X={x:.2f} Y={y:.2f} Z={z:.2f}"
        )
        print("Camera Extra Angle", CAMERA_EXTRA_TURN)
        devDebug.last_print_time = current_time

    


def idle():
    global CAMERA_EXTRA_TURN

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

    if BUTTONS["la"]:
        CAMERA_EXTRA_TURN = max(-26, CAMERA_EXTRA_TURN - 0.2)
    if BUTTONS["ra"]:
        CAMERA_EXTRA_TURN = min(26, CAMERA_EXTRA_TURN + 0.2)

    devDebug()
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
    glutSpecialUpFunc(specialKeyUpListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()
