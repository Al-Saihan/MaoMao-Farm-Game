from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLUT import GLUT_STROKE_ROMAN
import math
import time
import os
import random
from random import randint

# ! IGNORE THIS, IT'S JUST FOR DEBUGGING PURPOSES
# Open config.txt if it exists, otherwise create it
config_path = "config.txt"
if not os.path.exists(config_path):
    with open(config_path, "w") as f:
        f.write("# Configuration file\n")
else:
    with open(config_path, "r") as f:
        pass  # File exists, just open it

# ! --------------------------------------- :TODO: ---------------------------------------
# ! --------------------------------------- :TODO: ---------------------------------------
# ! --------------------------------------- :TODO: ---------------------------------------
# TODO: Make House Class -------------------------------------- Mao [Finished]
# TODO: Make Fence Class -------------------------------------- Saihan [Finished]
# TODO: Make Collision Class ---------------------------------- Saihan [Finished]
# TODO: Make Road --------------------------------------------- Saihan [Finished]
# TODO: Make Car/Shop(buy/sell point) Class ------------------- Mao [Finished]
# TODO: Make Pond Class --------------------------------------- Mao [Finished]
# TODO: Make Farmable Plot Class [With Crop Specifier] -------- Nusayba [Finished]
# TODO: Make Cows Barn Class ---------------------------------- Nusayba [Finished]
# TODO: Make Cows Class --------------------------------------- Nusayba [Finished]
# TODO: Make Hens Barn Class ---------------------------------- Mao [Finished]
# TODO: Make Hens Class --------------------------------------- Mao [Finished]
# TODO: Make Crops Class [Wheat, Potato, Carrot, Sunflower] --- Nusayba [Finished]
# TODO: Make Player Class [A Cat Humanoid] -------------------- Saihan [Finished]
# TODO: Crop Planting Logic ----------------------------------- WIP ------------------------------------
# TODO: Water Mechanism --------------------------------------- Nusayba, Mao [Finished]
# TODO: Crops Grow Logic -------------------------------------- Nusayba [Finished]
# TODO: Harvest Logic ----------------------------------------- WIP ------------------------------------
# TODO: Inventory System -------------------------------------- Saihan [Finished]
# TODO: Buy/ Sell Logics -------------------------------------- Saihan [WIP]
# TODO: Cheat Modes ------------------------------------------- WIP ------------------------------------
# TODO: Rain Logic -------------------------------------------- WIP ------------------------------------
# TODO: Day-Night Cycle --------------------------------------- Amra Shobai Raja [Finished]
# TODO: Design User Interface --------------------------------- Saihan [Finished]


# ! --------------------------------------- Global Variables ---------------------------------------
# ! --------------------------------------- Global Variables ---------------------------------------
# ! --------------------------------------- Global Variables ---------------------------------------

# ! Camera and Window Global Keys
W, H = 1280, 720
FOV = 70  # TODO:  DEFEAULT IS 70, PLEASE CHANGE IT BACK TO 70 IF CHANGED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! (God Bless You) [Saihan]
CAMERA_Z_REWORK = 0
CAMERA_ROTATE = 0
TOPVIEW = False

# ! Buttons
BUTTONS = {"w": False, "s": False, "a": False, "d": False, "la": False, "ra": False}

# ! Player Control
P_SPEED = 1
P_ROTATE_ANGLE = 0.4


# ! GAME LOGIC VARIABLES
CHEAT = False
SHOP = False
LAST_TIME_UPDATE = time.time()
SHOP_OPEN = False
DAY = 0
BALANCE = 1000.0
TIME = {"hour": 6, "minute": 0}
WEATHER = "clear"  # ? Clear, Rainy
NIGHT = False
BUCKET_FLAG = False
POND_FLAG = False
WATER = 10
MAX_WATER = 10
INVENTORY = {
    "wheat": 0,
    "wheat seed": 0,
    "carrot": 0,
    "carrot seed": 0,
    "chickens": 5,
    "egg": 0,
    "cows": 0,
    "milk": 0,
}

# ! --------------------------------------- CLasses ---------------------------------------
# ! --------------------------------------- CLasses ---------------------------------------
# ! --------------------------------------- CLasses ---------------------------------------


# ! Player
class Player:
    def __init__(self, position, rotation=0):
        self.position = position
        self.rotation = rotation

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
        glRotatef(
            self.rotation, 0, 0, 1
        )  # ? Rotate around Z-axis (facing X+ initially)

        # ! Variables
        leg_width, leg_height, leg_depth = 1.8, 7, 1.8
        body_width, body_height, body_depth = 5, 8, 3
        head_radius = 3
        arm_width, arm_height, arm_depth = 1.5, 6, 1.5
        tail_length, tail_width = 1.25, 0.5
        leg_swing_angle = 0
        arm_swing_angle = 0

        if BUTTONS["w"] or BUTTONS["s"]:
            # ? Animate walking
            time = glutGet(GLUT_ELAPSED_TIME) / 50.0
            leg_swing_angle = 20 * math.sin(time)

            # ! +Pi Reverse Arm Swing Compared with Leg
            arm_swing_angle = 15 * math.sin(time + math.pi)

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
        glScalef(0.3, 1.0, 1.0)
        glutSolidCone(1.4, 2.5, 10, 10)
        glPopMatrix()

        # ? Right ear
        glPushMatrix()
        glTranslatef(0, head_radius * 0.5, head_radius * 0.8)
        glRotatef(-40, 1, 0, 0)
        glColor3f(0.5, 0.5, 0.5)  # ! Lighter dark gray
        glScalef(0.3, 1.0, 1.0)
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
        glPushMatrix()
        glRotatef(60, 1, 0, 0)
        for i in range(3):
            glPushMatrix()
            glTranslatef(head_radius * 0.7, 0, head_radius * 0.3)
            glRotatef(i * 30, 1, 0, 0)
            glColor3f(0.2, 0.2, 0.2)  # ? Dark gray
            quad = gluNewQuadric()
            gluCylinder(quad, 0.12, 0.12, 3, 10, 1)
            gluDeleteQuadric(quad)
            glPopMatrix()
        glPopMatrix()

        # ? Right Whisker
        glPushMatrix()
        glRotatef(-60, 1, 0, 0)
        for i in range(3):
            glPushMatrix()
            glTranslatef(head_radius * 0.7, 0, head_radius * 0.3)
            glRotatef(-i * 30, 1, 0, 0)
            glColor3f(0.2, 0.2, 0.2)  # ? Dark gray
            quad = gluNewQuadric()
            gluCylinder(quad, 0.12, 0.12, 3, 10, 1)
            gluDeleteQuadric(quad)
            glPopMatrix()
        glPopMatrix()

        # ? Mouth : W Text
        glPushMatrix()
        glTranslatef(head_radius, -0.7, head_radius - 4)
        glRotatef(90, 0, 1, 0)
        glRotatef(90, 0, 0, 1)
        glColor3f(0.2, 0.2, 0.2)
        glScalef(0.02, 0.02, 0.02)
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord("w"))
        glPopMatrix()

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

        # ? Tail v2
        glPushMatrix()
        glTranslatef(body_depth - 4.5, 0, leg_height + 2)
        glScalef(tail_width, tail_width, tail_length * 0.8)
        glRotatef(-90 - 30, 0, 1, 0)
        # glRotatef(90, 1, 0, 0) # Along It's Own Axis - Rotates On Its Own - X
        glColor3f(0.3, 0.3, 0.3)  # ! Light dark gray

        x = 0.0
        while x <= 5.0:
            glPointSize(4 * (70 / FOV))  # ? This controls the thickness of the tail
            glBegin(GL_POINTS)

            speed = 0.005 * glutGet(GLUT_ELAPSED_TIME)
            y = 0.5 * (math.sin(x - speed) + math.sin(speed))
            z = 0.0

            glVertex3f(x, y, z)
            glEnd()

            x += 0.05  # ? This controls the smoothness of the tail / Step Size

        glPopMatrix()

        glPopMatrix()


class Pond:
    def __init__(self):
        # self.position = position
        pass

    def draw_pond(self):
        if NIGHT:
            glBegin(GL_QUADS)
            # ! Pond Area Border
            # Night Mode Gradient
            glColor3f(
                0.18, 0.18, 0.38
            )  # Slightly lighter blue-purple for the bottom-left
            glVertex3f(50, 0, 1)

            glColor3f(0.12, 0.12, 0.28)  # Lighter deep blue for the bottom-right
            glVertex3f(300, 0, 1)

            glColor3f(
                0.08, 0.08, 0.18
            )  # Still dark, but a bit lighter for the top-right
            glVertex3f(300, -530, 1)

            glColor3f(
                0.05, 0.05, 0.12
            )  # Almost black, but with a hint of blue for the top-left
            glVertex3f(50, -530, 1)

            glEnd()

            glBegin(GL_QUADS)
            # ! Pond Area
            # Night Mode: Slightly darker gradient for pond area
            glColor3f(0.55, 0.45, 0.55)
            glVertex3f(80, -30, 1.5)  # pond left bottom point
            glColor3f(0.60, 0.40, 0.50)
            glVertex3f(270, -30, 1.5)  # pond right bottom point
            glColor3f(0.45, 0.40, 0.60)
            glVertex3f(270, -500, 1.5)  # pond right top point
            glColor3f(0.40, 0.30, 0.40)
            glVertex3f(80, -500, 1.5)  # pond left top point
            glEnd()
        else:
            glBegin(GL_QUADS)
            # ! Pond Area Border
            glColor3f(0.65, 0.85, 1.0)
            glVertex3f(50, 0, 1)  # ? pond left bottom point
            glColor3f(0.55, 0.75, 0.95)
            glVertex3f(300, 0, 1)  # ? pond right bottom point
            glColor3f(0.45, 0.70, 0.85)
            glVertex3f(300, -530, 1)  # ? pond right top point
            glColor3f(0.05, 0.15, 0.35)
            glVertex3f(50, -530, 1)  # ? pond left top point
            glEnd()

            glBegin(GL_QUADS)
            # ! Pond Area
            glColor3f(0.95, 0.75, 0.80)
            glVertex3f(80, -30, 1.5)  # ? pond left bottom point
            glColor3f(0.98, 0.70, 0.65)
            glVertex3f(270, -30, 1.5)  # ? pond right bottom point
            glColor3f(0.80, 0.70, 0.90)
            glVertex3f(270, -500, 1.5)  # ? pond right top point
            glColor3f(0.70, 0.50, 0.60)
            glVertex3f(80, -500, 1.5)  # ? pond left top point
            glEnd()


pond = Pond()


class Tree:
    def __init__(self, x, y, z):
        global BOUND_BOXES
        self.x = x
        self.y = y
        self.z = z
        BOUND_BOXES.append(
            BorderLine(
                [self.x, self.y, self.z], [self.x, self.y, self.z + 20], strength=20
            )
        )

    def draw_tree(self):
        # ? Tree Trunk
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glScalef(10, 10, 80)
        if NIGHT:
            glColor3f(0.7, 0.4, 0.5)  # NIGHT Brownish pink
        else:
            glColor3f(0.8, 0.5, 0.6)  # Brownish pink

        glutSolidCylinder(1, 1, 10, 10)
        glPopMatrix()

        # ? Tree Head
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z + 80)
        glScalef(30, 30, 30)
        if NIGHT:
            glColor3f(0.9, 0.6, 0.7)  # NIGHT Sakura pink
        else:
            glColor3f(1.0, 0.7, 0.8)  # Sakura pink
        glutSolidSphere(1, 30, 30)
        glPopMatrix()


class Shop:
    def __init__(self, position):
        self.position = position
        pass

    def draw_truck_kun(self):

        # ? Initial Truck Position
        glPushMatrix()
        glTranslate(self.position[0], self.position[1], self.position[2] + 10)
        glRotate(90, 0, 0, 1)
        glScale(0.75, 0.75, 0.75)

        # ? Truck Driver Jekhane Thaake [Driver Seat]
        glPushMatrix()
        glTranslatef(0, 0, 36)
        glScalef(50, 50, 50)
        glColor3f(0.95, 0.6, 0.8)  # Pookie pink color
        glutSolidCube(1)
        glPopMatrix()

        # ? Truck Malamal Jekhane Thake [Container]
        glPushMatrix()
        glTranslatef(100, 0, 35)
        glScalef(150, 80, 70)
        glColor3f(0.33, 0.0, 0.13)  # Dark maroon
        glutSolidCube(1)
        glPopMatrix()

        # ? Truck window left
        glPushMatrix()
        glTranslatef(0, -20, 40)
        glScalef(30, 15, 20)
        glColor4f(0.6, 0.6, 0.65, 0.5)
        glutSolidCube(1)
        glPopMatrix()

        # ? Truck window right
        glPushMatrix()
        glTranslatef(0, 20, 40)
        glScalef(30, 15, 20)
        glColor4f(0.6, 0.6, 0.65, 0.5)
        glutSolidCube(1)
        glPopMatrix()

        # ? Truck window front
        glPushMatrix()
        glTranslatef(-25, 0, 40)
        glScalef(10, 40, 20)
        glColor4f(0.6, 0.6, 0.65, 0.5)
        glutSolidCube(1)
        glPopMatrix()

        # ? Wheels (4 wheels)
        wheel_positions = [
            (75, 35, 10),
            (75, -35, 10),
            (105, 35, 10),
            (105, -35, 10),
            (180, 35, 10),
            (180, -35, 10),
            (150, 35, 10),
            (150, -35, 10),
        ]

        xFix = -30
        for wx, wy, wz in wheel_positions:
            glPushMatrix()
            glTranslatef(wx + xFix, wy, wz)
            glRotatef(90, 0, 0, 1)
            glRotatef(90, 0, 1, 0)
            glColor3f(0.1, 0.1, 0.1)  # Black wheels
            glutSolidTorus(4, 12, 16, 32)
            glPopMatrix()

        glPopMatrix()


truck = Shop([550, 470, 0.1])


class Bucket:
    def __init__(self, position, rotation=0):
        self.position = position

    def draw_bucket(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotate(MAOMAO.rotation, 0, 0, 1)
        glPushMatrix()
        glTranslatef(0, 0, 5)
        glScalef(5, 5, 5)
        glColor3f(0.6, 0.6, 0.7)  # Light grayish blue
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, 7.5)
        glScalef(4, 4, 0.1)
        if WATER == 0:
            glColor3f(0.2, 0.2, 0.2)  # Dark grey for empty inside effect
        else:
            glColor3f(0.85, 0.7, 0.85)  # Mauve color water
        glutSolidCube(1)
        glPopMatrix()
        glPopMatrix()


class House:
    def __init__(self, position):
        self.position = position
        pass

    def draw_housearea(self):
        glBegin(GL_QUADS)
        # ! House Area
        if NIGHT:
            glColor3f(
                0.95 - 0.1, 0.85 - 0.1, 0.4 - 0.1
            )  # Yellowish field color (darker at night)
        else:
            glColor3f(0.95, 0.85, 0.4)  # Yellowish field color
        glVertex3f(-100, 380, 1)  # ? house area left bottom point
        glVertex3f(425, 380, 1)  # ? house area right bottom point
        glVertex3f(425, 725, 1)  # ? house area right top point
        glVertex3f(-100, 725, 1)  # ? house area left top point
        glEnd()
        # ! Garage
        glBegin(GL_QUADS)
        if NIGHT:
            glColor3f(
                0.7 - 0.1, 0.7 - 0.1, 0.7 - 0.1
            )  # Light gray for the quad (darker at night)
        else:
            glColor3f(0.7, 0.7, 0.7)  # Light gray for the quad
        glVertex3f(425, 420, 1)
        glVertex3f(700, 420, 1)
        glVertex3f(700, 680, 1)
        glVertex3f(425, 680, 1)
        glEnd()

    def draw_house(self):
        # ? House Base
        glPushMatrix()
        glTranslatef(*self.position)
        glScalef(300, 150, 100)
        glColor3f(0.80, 0.60, 0.70)
        # glColor3f(0.8, 0.5, 0.3)
        glutSolidCube(1)
        glPopMatrix()

        # ? Roof square base
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2] + 60)
        # glRotatef(45, 0, 1, 0)
        glScalef(350, 150, 20)
        glColor3f(0.5, 0.1, 0.1)
        glutSolidCube(1)

        glScalef(0.8, 0.8, 1)
        glTranslatef(0, 0, 1)
        glColor3f(0.45, 0.1, 0.1)
        glutSolidCube(1)

        glScalef(0.8, 0.8, 1)
        glTranslatef(0, 0, 1)
        glColor3f(0.35, 0.1, 0.1)
        glutSolidCube(1)

        glScalef(0.8, 0.8, 1)
        glTranslatef(0, 0, 1)
        glColor3f(0.30, 0.1, 0.1)
        glutSolidCube(1)
        glPopMatrix()

        # ? house door
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1] - 75, self.position[2] - 20)
        glScalef(50, 1, 110)
        glColor3f(0.2, 0.1, 0.05)
        glutSolidCube(1)
        glPopMatrix()

        # ? house window left
        glPushMatrix()
        glTranslatef(
            self.position[0] - 70, self.position[1] - 75, self.position[2] + 30
        )
        glScalef(40, 1, 30)
        glColor3f(0.8, 0.9, 1.0)  # Blueish white color
        glutSolidCube(1)
        glPopMatrix()

        # ? house window right
        glPushMatrix()
        glTranslatef(
            self.position[0] + 70, self.position[1] - 75, self.position[2] + 30
        )
        glScalef(40, 1, 30)
        glColor3f(0.8, 0.9, 1.0)  # Blueish white color
        glutSolidCube(1)
        glPopMatrix()


House1 = House([162, 600, 0.1])


class Fence:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self):
        x1, y1, z1 = self.start
        x2, y2, z2 = self.end

        # ! Horizontal Connector - Variables
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        mid_z = (z1 + z2) / 2

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1

        connectorLength = math.sqrt(dx**2 + dy**2 + dz**2)
        connectorWidth = 2
        connectorHeight = 2.5

        # ! Connector - Draw
        glPushMatrix()
        glTranslatef(mid_x, mid_y, mid_z)

        if dx > dy:
            glScalef(connectorLength, connectorWidth, connectorHeight)
        else:
            glScalef(connectorWidth, connectorLength, connectorHeight)

        glColor3f(0.3, 0.3, 0.3)  # Light dark black
        glutSolidCube(1)
        glPopMatrix()

        # ! Vertical Connector Nodes (4 Nodes, Equally Spaced)
        connection_nodes = [
            [x1, y1, z1],
            [x1 + dx * 0.33, y1 + dy * 0.33, z1 + dz * 0.33],
            [x1 + dx * 0.66, y1 + dy * 0.66, z1 + dz * 0.66],
            [x2, y2, z2],
        ]

        # ! Node Draw
        for nodes in connection_nodes:
            glPushMatrix()
            glTranslatef(nodes[0], nodes[1], nodes[2] / 2)

            if dx > dy:
                glScalef(5, connectorWidth * 1.1, 20)
            else:
                glScalef(connectorWidth * 1.1, 5, 20)

            glColor3f(0.7, 0.5, 0.3)  # ? Brownish color for posts
            glutSolidCube(1)
            glPopMatrix()


class BorderLine:
    def __init__(self, A, B, strength=15):
        self.A = A
        self.B = B
        self.strength = strength

    def __call__(self, C=[0, 0, 0]):
        # ! PEAK CROSS PRODUCT SHENANIGANS

        # ? Distance of the Point C, on the line AB
        AB = [self.B[i] - self.A[i] for i in range(3)]
        AC = [C[i] - self.A[i] for i in range(3)]

        cross = [
            AB[1] * AC[2] - AB[2] * AC[1],
            AB[2] * AC[0] - AB[0] * AC[2],
            AB[0] * AC[1] - AB[1] * AC[0],
        ]

        # ? Magnetudes
        cross_mag = math.sqrt(sum([x**2 for x in cross]))
        AB_mag = math.sqrt(sum([x**2 for x in AB]))

        distance = cross_mag / AB_mag if AB_mag != 0 else 0

        # ? Limit check: projection must be between A and B
        BC = [C[i] - self.B[i] for i in range(3)]
        dot1 = sum([AB[i] * AC[i] for i in range(3)])
        dot2 = sum([(-AB[i]) * BC[i] for i in range(3)])
        is_between = dot1 >= 0 and dot2 >= 0

        if is_between and abs(distance) < self.strength:
            return True
        return False


class Plot:
    def __init__(self, position):
        self.position = position
        self.slots = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 0=empty,1=wheat,2=carrot
        self.slot_colors = []
        self.watered = []
        for i in range(3):
            row_colors = []
            row_watered = []
            for j in range(3):
                row_colors.append([0, 1, 0])  # default green
                row_watered.append(False)
            self.slot_colors.append(row_colors)
            self.watered.append(row_watered)
        self.scaleX = 150
        self.scaleY = 150

    def set_slot_color(self, i, j, color):
        self.slot_colors[i][j] = color

    def water_slot(self, i, j):
        self.watered[i][j] = True

    def get_slot_at(self, x, y):
        scaleX, scaleY = self.scaleX, self.scaleY
        slot_width = scaleX / 3
        slot_height = scaleY / 3
        min_x = self.position[0] - scaleX / 2
        min_y = self.position[1] - scaleY / 2
        if min_x <= x <= min_x + scaleX and min_y <= y <= min_y + scaleY:
            i = int((x - min_x) // slot_width)
            j = int((y - min_y) // slot_height)
            return i, j
        return None

    def draw(self):
        scaleX = self.scaleX
        scaleY = self.scaleY
        slot_width = scaleX / 3
        slot_height = scaleY / 3

        for i in range(3):
            for j in range(3):
                glPushMatrix()
                x = self.position[0] - scaleX / 2 + slot_width / 2 + i * slot_width
                y = self.position[1] - scaleY / 2 + slot_height / 2 + j * slot_height
                glTranslatef(x, y, 1)
                glScalef(slot_width, slot_height, 2)

                if self.watered[i][j]:
                    glColor3f(0.36, 0.25, 0.2)
                else:
                    glColor3f(244 / 255, 223 / 255, 144 / 255)

                glutSolidCube(1)
                glPopMatrix()

                if self.slots[i][j] == 1:
                    self.draw_wheat(
                        i, j, slot_width, slot_height, self.slot_colors[i][j]
                    )
                elif self.slots[i][j] == 2:
                    self.draw_carrot(
                        i, j, slot_width, slot_height, self.slot_colors[i][j]
                    )

        glColor3f(180 / 255, 150 / 255, 80 / 255)

        glPushMatrix()
        glTranslatef(self.position[0], self.position[1] - slot_height / 2, 3)
        glScalef(scaleX, 1, 3)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.position[0], self.position[1] + slot_height / 2, 3)
        glScalef(scaleX, 1, 3)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.position[0] - slot_width / 2, self.position[1], 3)
        glScalef(1, scaleY, 3)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.position[0] + slot_width / 2, self.position[1], 3)
        glScalef(1, scaleY, 3)
        glutSolidCube(1)
        glPopMatrix()

    def draw_wheat(self, i, j, slot_width, slot_height, color):
        glColor3f(*color)
        # 2 rows × 4 columns = 8 sticks
        for row in range(2):
            for col in range(4):
                glPushMatrix()
                x = (
                    self.position[0]
                    - self.scaleX / 2
                    + i * slot_width
                    + (col + 0.5) * slot_width / 4
                )
                y = (
                    self.position[1]
                    - self.scaleY / 2
                    + j * slot_height
                    + (row + 0.5) * slot_height / 2
                )
                glTranslatef(x, y, 2)
                glScalef(2, 2, 10)
                glutSolidCube(1)
                glPopMatrix()

    def draw_carrot(self, i, j, slot_width, slot_height, color):
        glColor3f(*color)
        for row in range(2):
            for col in range(4):
                glPushMatrix()
                x = (
                    self.position[0]
                    - self.scaleX / 2
                    + i * slot_width
                    + (col + 0.5) * slot_width / 4
                )
                y = (
                    self.position[1]
                    - self.scaleY / 2
                    + j * slot_height
                    + (row + 0.5) * slot_height / 2
                )
                glTranslatef(x, y, 2)
                glScalef(2, 2, 10)
                glutSolidCube(1)
                glPopMatrix()


class Coop:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def draw(self):
        height = 1
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z + height / 2)
        glScalef(150, 200, height)
        glColor3f(0.95, 0.85, 0.4)  # Yellowish field color
        glutSolidCube(1)
        glPopMatrix()

    def draw_coop(self):
        # ? Base
        glPushMatrix()
        glTranslatef(self.x - 20, self.y - 70, self.z + 20)
        # glRotatef(45, 0, 1, 0)
        glScalef(50, 30, 20)
        glColor3f(0.8, 0.5, 0.6)  # Pinkish brown
        glutSolidCube(1)
        glPopMatrix()

        # ? Roof 1st layer
        glPushMatrix()
        glTranslatef(self.x - 20, self.y - 70, self.z + 31)
        # glRotatef(45, 0, 1, 0)
        glScalef(60, 40, 5)
        glColor3f(0.33, 0.0, 0.13)  # Dark maroon pink
        glutSolidCube(1)
        glPopMatrix()

        # ? Roof 2nd layer
        glPushMatrix()
        glTranslatef(self.x - 20, self.y - 70, self.z + 36)
        # glRotatef(45, 0, 1, 0)
        glScalef(50, 30, 5)
        glColor3f(0.40, 0.0, 0.20)  # Dark maroon pink
        glutSolidCube(1)
        glPopMatrix()

        # ? Roof 3rd layer
        glPushMatrix()
        glTranslatef(self.x - 20, self.y - 70, self.z + 41)
        # glRotatef(45, 0, 1, 0)
        glScalef(40, 20, 5)
        glColor3f(0.5, 0.0, 0.13)  # Maroon color
        glutSolidCube(1)
        glPopMatrix()

        # ? windows
        glPushMatrix()
        glTranslatef(self.x - 20, self.y - 54, self.z + 20)
        glScalef(15, 2, 10)
        glColor3f(0.33, 0.0, 0.13)  # Dark maroon color
        glutSolidCube(1)
        glPopMatrix()

        # ? designs
        glPushMatrix()
        glTranslatef(self.x - 40, self.y - 54, self.z + 20)
        glScalef(10, 2, 20)
        glColor3f(0.5, 0.0, 0.13)  # Maroon color
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.x, self.y - 54, self.z + 20)
        glScalef(10, 2, 20)
        glColor3f(0.5, 0.0, 0.13)  # Maroon color
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()

        # Move cube so its pivot (bottom edge) starts at the origin
        glTranslatef(self.x - 20, self.y - 45, self.z + 15)

        # Shift pivot down by half the height (after scaling Y=20 → half=10)
        glTranslatef(0, -10, 0)

        # Rotate downward around the X-axis so one end touches the ground
        glRotatef(-45, 1, 0, 0)

        # Move pivot back up to its proper position
        glTranslatef(0, 10, 0)

        # Scale cube to desired slide dimensions
        glScalef(15, 20, 2)

        # Set slide color (maroon)
        glColor3f(0.5, 0.0, 0.13)

        # Draw the cube
        glutSolidCube(1)

        glPopMatrix()


class Chicken:
    def __init__(self, x, y, z, rotation=0):
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation

    def draw_chicken(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rotation, 0, 0, 1)

        # ? Chicken Body
        glColor3f(1.0, 0.8, 0.9)  # Light pink
        glPushMatrix()
        glTranslatef(0, 0, 10)
        glScalef(10, 5, 7)
        glutSolidCube(1)
        glPopMatrix()

        # ? Chicken Head
        glPushMatrix()
        glTranslatef(5, 0, 15)
        glScalef(5, 5, 5)
        glutSolidCube(1)
        glPopMatrix()

        # ? beck
        glPushMatrix()
        glTranslatef(9, 0, 15)
        glScalef(3, 4, 1)
        glColor3f(1.0, 0.5, 0.0)  # Orange color for beck
        glutSolidCube(1)
        glPopMatrix()

        # ? red comb
        glPushMatrix()
        glTranslatef(7, 0, 14)
        glScalef(2, 2, 2)
        glColor3f(1.0, 0.0, 0.0)  # Red color for comb
        glutSolidCube(1)
        glPopMatrix()

        # ? Chicken Legs -- left
        glPushMatrix()
        glTranslatef(0, 1, 5)
        glScalef(1, 1, 3)
        glColor3f(1.0, 0.5, 0.0)  # Orange color for legs
        glutSolidCube(1)
        glPopMatrix()

        # ? Chicken Legs -- right
        glPushMatrix()
        glTranslatef(0, -1, 5)
        glScalef(1, 1, 3)
        glColor3f(1.0, 0.5, 0.0)  # Orange color for legs
        glutSolidCube(1)
        glPopMatrix()

        # ? Chicken Eyes
        glBegin(GL_POINTS)
        glColor3f(0.0, 0.0, 0.0)  # Black color for eyes
        glVertex3f(7.8, -1, 17)
        glVertex3f(7.8, 1, 17)
        glEnd()

        # ? chicken wings
        glPushMatrix()
        glTranslatef(0, -2.8, 10)
        glScalef(6, 1, 4)
        glColor3f(0.9, 0.5, 0.7)  # Lighter pink
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 2.8, 10)
        glScalef(6, 1, 4)
        glColor3f(0.9, 0.5, 0.7)  # Lighter pink
        glutSolidCube(1)
        glPopMatrix()
        glPopMatrix()


class Pillar:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def draw(self):
        # ? pillar
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glScalef(5, 5, 40)
        glColor3f(0.33, 0.0, 0.13)  # Dark maroon pink
        glutSolidCylinder(0.5, 0.3, 10, 10)
        glPopMatrix()


class Barn:
    def __init__(self, position):
        self.position = position

    def draw_barn(self):

        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2] + 25)
        glScalef(180, 120, 50)
        glColor3f(0.8, 0.1, 0.1)
        glutSolidCube(1)
        glPopMatrix()

        # roof
        glColor3f(0.5, 0.25, 0.1)  # brown
        glBegin(GL_TRIANGLES)
        # front
        glVertex3f(self.position[0] - 90, self.position[1] - 60, self.position[2] + 50)
        glVertex3f(self.position[0] + 90, self.position[1] - 60, self.position[2] + 50)
        glVertex3f(self.position[0], self.position[1], self.position[2] + 100)

        # Back
        glVertex3f(self.position[0] - 90, self.position[1] + 60, self.position[2] + 50)
        glVertex3f(self.position[0] + 90, self.position[1] + 60, self.position[2] + 50)
        glVertex3f(self.position[0], self.position[1], self.position[2] + 100)

        # Left
        glVertex3f(self.position[0] - 90, self.position[1] - 60, self.position[2] + 50)
        glVertex3f(self.position[0] - 90, self.position[1] + 60, self.position[2] + 50)
        glVertex3f(self.position[0], self.position[1], self.position[2] + 100)

        # Right
        glVertex3f(self.position[0] + 90, self.position[1] - 60, self.position[2] + 50)
        glVertex3f(self.position[0] + 90, self.position[1] + 60, self.position[2] + 50)
        glVertex3f(self.position[0], self.position[1], self.position[2] + 100)
        glEnd()

        # door
        glPushMatrix()
        glTranslatef(
            self.position[0] - 40, self.position[1] - 60.1, self.position[2] + 15
        )
        glScalef(20, 1, 30)
        glColor3f(0.3, 0.15, 0.05)  # dark brown
        glutSolidCube(1)
        glPopMatrix()

        # big foor
        glPushMatrix()
        glTranslatef(
            self.position[0] + 30, self.position[1] - 60.2, self.position[2] + 20
        )
        glScalef(60, 1, 40)
        glColor3f(0.35, 0.2, 0.1)
        glutSolidCube(1)
        glPopMatrix()

        # handle??
        glPushMatrix()
        glTranslatef(self.position[0] + 30, self.position[1] - 61, self.position[2] + 5)
        glScalef(5, 1, 5)
        glColor3f(0.9, 0.9, 0.9)
        glutSolidCube(1)
        glPopMatrix()


class Cow:
    def __init__(
        self,
        position,
        scale=6.0,
        body_color=(0.85, 0.85, 0.85),
        nose_color=(0.7, 0.7, 0.7),
        ear_color=(0.7, 0.5, 0.4),
        rotation=0,
    ):
        self.position = [position[0], position[1], position[2]]
        self.rotation = rotation
        self.scale = scale
        self.body_color = body_color
        self.nose_color = nose_color
        self.ear_color = ear_color

    def draw(self):
        s = self.scale
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 0, 1)

        # body
        glPushMatrix()
        glTranslatef(0, 0, 1.5 * s)
        glScalef(4 * s, 2 * s, 2 * s)
        glColor3f(*self.body_color)
        glutSolidCube(1)
        glPopMatrix()

        # head
        glPushMatrix()
        glTranslatef(2.5 * s, 0, 2.5 * s)
        glScalef(1.5 * s, 1.5 * s, 1.5 * s)
        glColor3f(*self.body_color)
        glutSolidCube(1)
        glPopMatrix()

        # nose
        glPushMatrix()
        glTranslatef(3.25 * s, 0, 2.0 * s)
        glScalef(0.25 * s, 1.2 * s, 0.4 * s)
        glColor3f(*self.nose_color)
        glutSolidCube(1)
        glPopMatrix()

        # eyes
        eye_positions = [
            (3.2 * s, 0.35 * s, 2.5 * s, 0.15 * s),
            (3.2 * s, -0.35 * s, 2.5 * s, 0.15 * s),
        ]
        glColor3f(0, 0, 0)
        for x, y, z, size in eye_positions:
            glPushMatrix()
            glTranslatef(x, y, z)
            glScalef(size, size, size)
            glutSolidCube(1)
            glPopMatrix()

        # ears/horns? idk
        ear_positions = [
            (2.8 * s, 0.75 * s, 3.0 * s, 0.4 * s, 45),
            (2.8 * s, -0.75 * s, 3.0 * s, 0.4 * s, -45),
        ]
        glColor3f(*self.ear_color)
        for x, y, z, size, rot in ear_positions:
            glPushMatrix()
            glTranslatef(x, y, z)
            glRotatef(rot, 0, 0, 1)
            glScalef(size, size, size)
            glutSolidCube(1)
            glPopMatrix()

        # tail
        glPushMatrix()
        glTranslatef(-2 * s, 0, 1.5 * s)
        glRotatef(45, 0, 1, 0)
        glScalef(0.3 * s, 0.3 * s, 1.2 * s)
        glColor3f(*self.ear_color)
        glutSolidCube(1)
        glPopMatrix()

        # leg
        leg_z = 0.75 * s
        leg_positions = [
            (1.5 * s, -0.8 * s, leg_z),
            (1.5 * s, 0.8 * s, leg_z),
            (-1.5 * s, -0.8 * s, leg_z),
            (-1.5 * s, 0.8 * s, leg_z),
        ]
        for pos in leg_positions:
            glPushMatrix()
            glTranslatef(*pos)
            glScalef(0.8 * s, 0.8 * s, 1.5 * s)
            glColor3f(*self.body_color)
            glutSolidCube(1)
            glPopMatrix()

        glPopMatrix()


COOP = Coop(-200, -200, 0)
BARN = Barn([-400, 400, 0])
MAOMAO = Player([-161, 299, 0], 110)
BUCKET = Bucket([MAOMAO.position[0] + 10, MAOMAO.position[1] - 10, 10])

a1 = Fence([-740, -590, 10], [740, -590, 10])
a2 = Fence([-740, 740, 10], [740, 740, 10])
a3 = Fence([-740, -590, 10], [-740, 740, 10])
a4 = Fence([740, -590, 10], [740, 740, 10])
# Chicken Fences
a5 = Fence([-130, -290, 10], [-130, -110, 10])
a6 = Fence([-265, -290, 10], [-130, -290, 10])
a7 = Fence([-265, -110, 10], [-130, -110, 10])
a8 = Fence([-265, -290, 10], [-265, -110, 10])
# cow fences
a9 = Fence([-310, 350, 10], [-126, 350, 10])
a10 = Fence([-310, 455, 10], [-126, 455, 10])
a11 = Fence([-126, 350, 10], [-126, 455, 10])
# Garage Fence
a12 = Fence([693, 433, 0], [692, 667, 10])
a13 = Fence([439, 667, 0], [692, 667, 10])
a14 = Fence([439, 433, 0], [439, 667, 10])


FENCES = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14]

b1 = BorderLine([-740, -590, 10], [740, -590, 10])
b2 = BorderLine([-740, 740, 10], [740, 740, 10])
b3 = BorderLine([-740, -590, 10], [-740, 740, 10])
b4 = BorderLine([740, -590, 10], [740, 740, 10])
# Chicken Fences
b5 = BorderLine([-130, -290, 10], [-130, -110, 10], strength=11)
b6 = BorderLine([-265, -290, 10], [-130, -290, 10], strength=11)
b7 = BorderLine([-265, -110, 10], [-130, -110, 10], strength=11)
b8 = BorderLine([-265, -290, 10], [-265, -110, 10], strength=11)
# cow fences
b9 = BorderLine([-310, 350, 10], [-126, 350, 10], strength=11)
b10 = BorderLine([-310, 455, 10], [-126, 455, 10], strength=11)
b11 = BorderLine([-126, 350, 10], [-126, 455, 10], strength=11)
# Garage Fence
b12 = BorderLine([693, 433, 0], [692, 667, 10])
b13 = BorderLine([439, 667, 0], [692, 667, 10])
b14 = BorderLine([439, 433, 0], [439, 667, 10])
# Pool Border
b15 = BorderLine([86, -36, 0], [86, -495, 0])
b16 = BorderLine([86, -495, 0], [265, -495, 0])
b17 = BorderLine([265, -495, 0], [265, -36, 0])
b18 = BorderLine([265, -36, 0], [86, -36, 0])


BOUND_BOXES = []
BOUND_BOXES.append(b1)
BOUND_BOXES.append(b2)
BOUND_BOXES.append(b3)
BOUND_BOXES.append(b4)
BOUND_BOXES.append(b5)
BOUND_BOXES.append(b6)
BOUND_BOXES.append(b7)
BOUND_BOXES.append(b8)
BOUND_BOXES.append(b9)
BOUND_BOXES.append(b10)
BOUND_BOXES.append(b11)
BOUND_BOXES.append(b12)
BOUND_BOXES.append(b13)
BOUND_BOXES.append(b14)
BOUND_BOXES.append(b15)
BOUND_BOXES.append(b16)
BOUND_BOXES.append(b17)
BOUND_BOXES.append(b18)

PLOT1 = Plot([570, -20, 1])
PLOT2 = Plot([570, -350, 1])

PLOT1.slots[0][0] = 1  # wheat
PLOT1.slots[1][1] = 2  # carrot
PLOT2.slots[2][2] = 1  # wheat


PLOT1.set_slot_color(0, 0, [1, 1, 0])  # yellow wheat
PLOT1.set_slot_color(1, 1, [1, 0.5, 0])  # orange carrot


PLOT2.water_slot(2, 2)

PLOTS = [PLOT1, PLOT2]

t1 = Tree(203.79, 58.59, 0)
t2 = Tree(396.99, 343.36, 0)
t3 = Tree(-184, -499, 0)
t4 = Tree(-290, -430, 0)
t5 = Tree(-518, -502, 0)
t6 = Tree(-696, -456, 0)
t7 = Tree(-552, -295, 0)
t8 = Tree(-611, -90, 0)
t9 = Tree(-611, -90, 0)
t10 = Tree(-340, -112, 0)
t11 = Tree(-546, 121, 0)
t12 = Tree(-275, 108, 0)
t13 = Tree(-216, 527, 0)
t14 = Tree(-427, 628, 0)
t15 = Tree(-601, 427, 0)
t16 = Tree(-653, 648, 0)
t17 = Tree(374, -461, 0)
TREES = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17]

pl1 = Pillar(-200, -260, 0)
pl2 = Pillar(-240, -260, 0)
pl3 = Pillar(-240, -280, 0)
pl4 = Pillar(-200, -280, 0)
PILLARS = [pl1, pl2, pl3, pl4]

chicken1 = Chicken(-150, -150, 0, rotation=30)
chicken2 = Chicken(-200, -130, 0, rotation=-20)
chicken3 = Chicken(-170, -180, 0, rotation=90)
chicken4 = Chicken(-250, -150, 0)
chicken5 = Chicken(-230, -180, 0, rotation=-90)
CHICKENS = [chicken1, chicken2, chicken3, chicken4, chicken5]

cow1 = Cow([-276, 418, 0], scale=6, rotation=-30, body_color=(0.85, 0.85, 0.85))
cow2 = Cow(
    [-170, 408, 0],
    scale=6,
    rotation=-90,
    body_color=(1.0, 0.6, 0.6),
    nose_color=(0.8, 0.5, 0.5),
    ear_color=(0.6, 0.3, 0.2),
)
cow3 = Cow(
    [-200, 390, 0],
    scale=6,
    rotation=-110,
    body_color=(0.6, 0.9, 0.6),
    nose_color=(0.5, 0.7, 0.5),
)
COWS = [cow1, cow2, cow3]


# ! --------------------------------------- Draw Functions ---------------------------------------
# ! --------------------------------------- Draw Functions ---------------------------------------
# ! --------------------------------------- Draw Functions ---------------------------------------


def farmLand():
    glBegin(GL_QUADS)
    # ! Grass Land
    # Grass Land (darker at night)
    if NIGHT:
        glColor3f(0.05 - 0.1, 0.35 - 0.1, 0.05 - 0.1)
        glVertex3f(-750, -600, 0)
        glColor3f(0.10 - 0.1, 0.55 - 0.1, 0.10 - 0.1)
        glVertex3f(750, -600, 0)
        glColor3f(0.30 - 0.1, 0.70 - 0.1, 0.20 - 0.1)
        glVertex3f(750, 750, 0)
        glColor3f(0.55 - 0.1, 0.85 - 0.1, 0.40 - 0.1)
        glVertex3f(-750, 750, 0)
    else:
        glColor3f(0.05, 0.35, 0.05)
        glVertex3f(-750, -600, 0)
        glColor3f(0.10, 0.55, 0.10)
        glVertex3f(750, -600, 0)
        glColor3f(0.30, 0.70, 0.20)
        glVertex3f(750, 750, 0)
        glColor3f(0.55, 0.85, 0.40)
        glVertex3f(-750, 750, 0)
    glEnd()

    # ! Road
    glBegin(GL_QUADS)
    if NIGHT:
        glColor3f(0.95 - 0.1, 0.95 - 0.1, 0.5 - 0.1)  # Road brown color
    else:
        glColor3f(0.95, 0.95, 0.5)  # Road brown color
    # ! 1
    glVertex3f(150, 250, 1)
    glVertex3f(750, 250, 1)
    glVertex3f(750, 150, 1)
    glVertex3f(150, 150, 1)

    # ! 2
    glVertex3f(-50, 230, 1)
    glVertex3f(150, 150, 1)
    glVertex3f(150, 250, 1)
    glVertex3f(-50, 330, 1)

    # ! 3
    glVertex3f(-750, 230, 1)
    glVertex3f(-50, 230, 1)
    glVertex3f(-50, 330, 1)
    glVertex3f(-750, 330, 1)

    # ! 4
    glVertex3f(-100, 50, 1)
    glVertex3f(0, 25, 1)
    glVertex3f(160, 160, 1)
    glVertex3f(120, 250, 1)

    # ! 5
    glVertex3f(-100, -600, 1)
    glVertex3f(0, -600, 1)
    glVertex3f(0, 50, 1)
    glVertex3f(-100, 50, 1)

    # ! 6
    glVertex3f(330, -300, 1)
    glVertex3f(400, -300, 1)
    glVertex3f(400, 150, 1)
    glVertex3f(330, 150, 1)

    glEnd()


def drawFences():
    for lathi in FENCES:
        lathi.draw()


def drawPlots():
    for plot in PLOTS:
        plot.draw()


def draw_text(x, y, text, color, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(*color)

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))


def user_interface():
    global SHOP_OPEN
    glDisable(GL_DEPTH_TEST)
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # ! Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, W, 0, H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # ! UI Elements

    # ? MaoMao Profile Box
    glBegin(GL_QUADS)
    glColor3f(0.85, 0.7, 0.85)
    glVertex2f(15, H - 10)
    glVertex2f(100, H - 10)
    glVertex2f(100, H - 100)
    glVertex2f(15, H - 100)
    glEnd()

    # ? MaoMao Eyes
    glPointSize(10)
    glBegin(GL_POINTS)
    glColor3f(0, 0, 0)
    glVertex2f(35, H - 30)
    glVertex2f(80, H - 30)
    glEnd()

    # --------------------

    glPointSize(6)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)
    glVertex2f(35, H - 30)
    glVertex2f(80, H - 30)
    glEnd()

    # ? MaoMao Mouth
    stepX = 12.5
    stepY = -8

    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 0)
    glVertex2f(stepX + 35, H - 40 + stepY)
    glVertex2f(stepX + 40, H - 60 + stepY)
    glVertex2f(stepX + 45, H - 40 + stepY)
    glVertex2f(stepX + 50, H - 60 + stepY)
    glVertex2f(stepX + 55, H - 40 + stepY)
    glEnd()

    # ? Profile Border
    glLineWidth(1)
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 0)
    glVertex2f(15, H - 10)
    glVertex2f(100, H - 10)
    glVertex2f(100, H - 100)
    glVertex2f(15, H - 100)
    glVertex2f(15, H - 10)
    glEnd()

    # ? TEXTS - (Top Right)
    if NIGHT:
        textColor = (1, 1, 1)
    else:
        textColor = (0, 0, 0)

    draw_text(105, H - 30, "MaoMao Farming Simulator", textColor)
    draw_text(105, H - 60, f"Balance: {BALANCE:.2f}$", textColor)
    draw_text(105, H - 90, f"Time: {TIME['hour']:02}:{TIME['minute']:02}", textColor)
    draw_text(W - 200, H - 30, f"Weather: {WEATHER}", textColor)
    draw_text(W - 165, H - 60, f"Day: {DAY}", textColor)

    draw_text(13, H - 473, "Inventory:", (0, 0, 0))
    # ? TEXTS Background - (Bottom Left)
    glColor3f(0.85, 0.7, 0.85)  # Lighter mauve color
    glBegin(GL_QUADS)
    glVertex2f(12, H - 480)
    glVertex2f(150, H - 480)
    glVertex2f(150, H - 510 - 30 * len(INVENTORY) + 33)
    glVertex2f(12, H - 510 - 30 * len(INVENTORY) + 33)
    glEnd()

    # ? Inventory Border
    glLineWidth(1)
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 0)
    glVertex2f(12, H - 480)
    glVertex2f(150, H - 480)
    glVertex2f(150, H - 510 - 30 * len(INVENTORY) + 33)
    glVertex2f(12, H - 510 - 30 * len(INVENTORY) + 33)
    glVertex2f(12, H - 480)
    glEnd()

    # Show "Press F to open Shop" if player is near the car/shop
    car_pos = truck.position
    player_pos = MAOMAO.position
    dist = math.sqrt(
        (player_pos[0] - car_pos[0]) ** 2 + (player_pos[1] - car_pos[1]) ** 2
    )
    if dist >= 80:
        SHOP_OPEN = False
    elif dist < 80 and SHOP_OPEN == False:
        draw_text(W // 2 - 100, 80, "Press F to open Shop", (0.2, 0.1, 0.1))

    elif dist < 80 and SHOP_OPEN:
        draw_text(W // 2 - 100, 80, "Press F to close Shop", (0.2, 0.1, 0.1))

        # ? Draw shop menu background
        glColor3f(0.95, 0.9, 0.98)
        glBegin(GL_QUADS)
        glVertex2f(W // 2 - 220, H // 2 + 180)
        glVertex2f(W // 2 + 220, H // 2 + 180)
        glVertex2f(W // 2 + 220, H // 2 - 180)
        glVertex2f(W // 2 - 220, H // 2 - 180)
        glEnd()

        # ? Border
        glColor3f(0.3, 0.1, 0.3)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(W // 2 - 220, H // 2 + 180)
        glVertex2f(W // 2 + 220, H // 2 + 180)
        glVertex2f(W // 2 + 220, H // 2 - 180)
        glVertex2f(W // 2 - 220, H // 2 - 180)
        glEnd()

        draw_text(W // 2 - 60, H // 2 + 150, "SHOP MENU", (0.2, 0.1, 0.2))

        shop_items = [
            ("Wheat Seed", 10.0, "Buy"),
            ("Carrot Seed", 20.0, "Buy"),
            ("Chicken", 50.0, "Buy"),
            ("Cow", 100.0, "Buy"),
            ("Water Capacity", 500.0, "Buy"),
            ("Wheat", 15.0, "Sell"),
            ("Carrot", 25.0, "Sell"),
            ("Egg", 30.0, "Sell"),
            ("Milk", 60.0, "Sell"),
        ]

        for idx, (item, price, action) in enumerate(shop_items):
            y = H // 2 + 110 - idx * 28
            draw_text(W // 2 - 180, y, f"{item}", (0, 0, 0))
            draw_text(W // 2 + 20, y, f"{action} -- ${price:.2f}", (0.1, 0.1, 0.1))

    # ? Inventory Items (Write and Underline)
    for k, v in INVENTORY.items():
        index = list(INVENTORY.keys()).index(k) + 1
        draw_text(15, H - 470 - 30 * index, f"{k.capitalize()}: {v}", (0, 0, 0))
        glColor3f(0.6, 0.4, 0.6)
        glBegin(GL_LINES)
        glVertex2f(15, H - 470 - 30 * index - 5)
        glVertex2f(140, H - 470 - 30 * index - 5)
        glEnd()

    text = ["W", " A", " T", " E", " R"]
    for i in range(len(text)):
        draw_text(W - 60, 130 - i * 20, text[i], (0, 0, 0))

    # ? Water Bucket (Bottom Right)
    if WATER:
        glBegin(GL_QUADS)
        glColor3f(0.2, 0.5, 1)  # Lighter mauve color
        glVertex2f(W - 30, 10)
        glVertex2f(W - 10, 10)
        glVertex2f(W - 10, 20 * WATER)
        glVertex2f(W - 30, 20 * WATER)
        glEnd()

    # ! Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)


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

    # ! Water Mode (R key)
    if key.lower() == b"r":
        global BUCKET_FLAG
        BUCKET_FLAG = not BUCKET_FLAG
    
    # ! Cheat Mode (C Key)
    if key.lower() == b"c":
        global CHEAT
        CHEAT = not CHEAT
        cheat_mode(CHEAT)    

    # ! Shop Mode (F key)
    car_pos = truck.position
    player_pos = MAOMAO.position
    dist = math.sqrt(
        (player_pos[0] - car_pos[0]) ** 2 + (player_pos[1] - car_pos[1]) ** 2
    )
    if key.lower() == b"f" and dist < 80:
        global SHOP_OPEN
        SHOP_OPEN = not SHOP_OPEN

    # ! Escape key to exit game
    if key == b"\x1b":
        glutLeaveMainLoop()


def keyboardUpListener(key, x, y):
    global BUTTONS, TOPVIEW

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
    if key.lower() == b"v":
        TOPVIEW = not TOPVIEW


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


plot_coordinates = [(570, -20), (570, -350)]  # Add more plot coordinates as needed
pond_coordinates = [(0, 0)]  # Placeholder for pond coordinates


def mouseListener(button, state, x, y):
    global FOV, CAMERA_Z_REWORK, TOPVIEW, BUCKET_FLAG, POND_FLAG, SHOP_OPEN, BALANCE, INVENTORY, WATER, MAX_WATER

    zoomUpStep = 4
    zoomDownStep = 6

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        with open(config_path, "a") as f:
            print("Writing to config.txt")
            f.write(
                f"a = Fence({MAOMAO.position[0]}, {MAOMAO.position[1]}, {MAOMAO.position[2]})\n"
            )
        global WATER

        px, py, pz = MAOMAO.position

        for plot in PLOTS:
            slot = plot.get_slot_at(px, py)
            if slot:
                if WATER > 0:
                    i, j = slot
                    plot.water_slot(i, j)
                    print(f"Watered slot ({i},{j}) in plot at {plot.position}")
                    WATER -= 1
                    break

        if BUCKET_FLAG and WATER > 0:
            WATER -= 1
            print("Watering! Remaining:", WATER)

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        if SHOP_OPEN:
            if 456 < x < 785 and 235 < y < 252:
                print("Clicked on Wheat Seed")
                if BALANCE >= 10.0:
                    if INVENTORY["wheat seed"] < 20:
                        BALANCE -= 10.0
                        INVENTORY["wheat seed"] += 1
                        print("Bought 1 Wheat Seed")
                    else:
                        print("Max limit reached for Wheat Seed")
                else:
                    print("Not enough balance to buy Wheat Seed")

            elif 456 < x < 785 and 263 < y < 280:
                print("Clicked on Carrot Seed")
                if BALANCE >= 20.0:
                    if INVENTORY["carrot seed"] < 20:
                        BALANCE -= 20.0
                        INVENTORY["carrot seed"] += 1
                        print("Bought 1 Carrot Seed")
                    else:
                        print("Max limit reached for Carrot Seed")
                else:
                    print("Not enough balance to buy Carrot Seed")

            elif 456 < x < 785 and 291 < y < 308:
                print("Clicked on Chicken")
                if BALANCE >= 50.0:
                    if INVENTORY["chickens"] < 5:
                        BALANCE -= 50.0
                        INVENTORY["chickens"] += 1
                        print("Bought 1 Chicken")
                    else:
                        print("Max limit reached for Chickens")
                else:
                    print("Not enough balance to buy Chicken")

            elif 456 < x < 785 and 319 < y < 336:
                print("Clicked on Cow")
                if BALANCE >= 100.0:
                    if INVENTORY["cows"] < 3:
                        BALANCE -= 100.0
                        INVENTORY["cows"] += 1
                        print("Bought 1 Cow")
                    else:
                        print("Max limit reached for Cows")
                else:
                    print("Not enough balance to buy Cow")

            elif 456 < x < 785 and 347 < y < 364:
                print("Clicked on Water Capacity")
                if BALANCE >= 500.0:
                    BALANCE -= 500.0
                    MAX_WATER += 5
                    print("Increased max water capacity by 5")
                else:
                    print("Not enough balance to increase water capacity")

            elif 456 < x < 785 and 375 < y < 392:
                print("Clicked on Wheat")
                if INVENTORY["wheat"] > 0:
                    BALANCE += 15.0 * INVENTORY["wheat"]
                    print(
                        f"Sold {INVENTORY['wheat']} Wheat for ${15.0 * INVENTORY['wheat']:.2f}"
                    )
                    INVENTORY["wheat"] = 0
                else:
                    print("No Wheat to sell")

            elif 456 < x < 785 and 403 < y < 420:
                print("Clicked on Carrot")
                if INVENTORY["carrot"] > 0:
                    BALANCE += 25.0 * INVENTORY["carrot"]
                    print(
                        f"Sold {INVENTORY['carrot']} Carrot for ${25.0 * INVENTORY['carrot']:.2f}"
                    )
                    INVENTORY["carrot"] = 0
                else:
                    print("No Carrot to sell")

            elif 456 < x < 785 and 431 < y < 448:
                print("Clicked on Egg")
                if INVENTORY["egg"] > 0:
                    BALANCE += 30.0 * INVENTORY["egg"]
                    print(
                        f"Sold {INVENTORY['egg']} Egg for ${30.0 * INVENTORY['egg']:.2f}"
                    )
                    INVENTORY["egg"] = 0
                else:
                    print("No Egg to sell")

            elif 456 < x < 785 and 459 < y < 476:
                print("Clicked on Milk")
                if INVENTORY["milk"] > 0:
                    BALANCE += 60.0 * INVENTORY["milk"]
                    print(
                        f"Sold {INVENTORY['milk']} Milk for ${60.0 * INVENTORY['milk']:.2f}"
                    )
                    INVENTORY["milk"] = 0
                else:
                    print("No Milk to sell")

        else:
            if 50 < MAOMAO.position[0] < 300 and -515 < MAOMAO.position[1] < -10:
                print("Pond Clicked")
                if WATER < MAX_WATER:
                    WATER += 1
                    print(f"Collected water. Total water buckets: {WATER}")
                else:
                    print("Water buckets full.")

    # ? Scroll Up:
    if button == 3 and state == GLUT_DOWN:
        print("Scroll Up")
        FOV = max(FOV - zoomUpStep, 60)
        CAMERA_Z_REWORK = max(CAMERA_Z_REWORK - zoomUpStep, -(4 * zoomUpStep))

    # ? Scroll Down:
    if button == 4 and state == GLUT_DOWN:
        print("Scroll Down")
        FOV = min(FOV + zoomDownStep, 80)
        CAMERA_Z_REWORK = min(CAMERA_Z_REWORK + zoomDownStep, (2 * zoomDownStep))

# Put this at the top of your file
CHEAT_BACKUP = {}

def cheat_mode(CHEAT):
    global BALANCE, INVENTORY, WATER, MAX_WATER, CHEAT_BACKUP

    if CHEAT:
        # Save current state before overwriting
        CHEAT_BACKUP = {
            "BALANCE": BALANCE,
            "wheat": INVENTORY["wheat"],
            "carrot": INVENTORY["carrot"],
            "wheat seed": INVENTORY["wheat seed"],
            "carrot seed": INVENTORY["carrot seed"],
            "egg": INVENTORY["egg"],
            "milk": INVENTORY["milk"],
            "WATER": WATER,
            "MAX_WATER": MAX_WATER,
        }

        # Apply cheat values
        BALANCE = 999999999999.99
        INVENTORY["wheat"] = 99999999
        INVENTORY["carrot"] = 99999999
        INVENTORY["wheat seed"] = 99999999
        INVENTORY["carrot seed"] = 99999999
        INVENTORY["egg"] = 99999999
        INVENTORY["milk"] = 99999999
        WATER = 9999999
        MAX_WATER = 9999999999
        print("Cheat mode activated!")

    else:
        if CHEAT_BACKUP:  # Restore only if backup exists
            BALANCE = CHEAT_BACKUP["BALANCE"]
            INVENTORY["wheat"] = CHEAT_BACKUP["wheat"]
            INVENTORY["carrot"] = CHEAT_BACKUP["carrot"]
            INVENTORY["wheat seed"] = CHEAT_BACKUP["wheat seed"]
            INVENTORY["carrot seed"] = CHEAT_BACKUP["carrot seed"]
            INVENTORY["egg"] = CHEAT_BACKUP["egg"]
            INVENTORY["milk"] = CHEAT_BACKUP["milk"]
            WATER = CHEAT_BACKUP["WATER"]
            MAX_WATER = CHEAT_BACKUP["MAX_WATER"]
            print("Cheat mode deactivated!")
        else:
            print("Cheat mode was never activated, nothing to restore.")


def updateTime():
    global TIME, LAST_TIME_UPDATE, NIGHT, BALANCE

    if time.time() - LAST_TIME_UPDATE >= 0.5:  # Update every 1 second
        LAST_TIME_UPDATE = time.time()
        TIME["minute"] += 30
        if TIME["minute"] >= 60:
            TIME["minute"] = 0
            TIME["hour"] += 1
            if TIME["hour"] >= 24:
                TIME["hour"] = 0
                global DAY
                DAY += 1
                if INVENTORY["chickens"] > 0:
                    INVENTORY["egg"] += randint(0, INVENTORY["chickens"])
                if INVENTORY["cows"] > 0:
                    INVENTORY["milk"] += randint(0, INVENTORY["cows"])
                BALANCE += 50  # Daily allowance  
                        

            if 18 > TIME["hour"] > 6:
                NIGHT = False
            else:
                NIGHT = True


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
    angle_rad = math.radians(MAOMAO.rotation + CAMERA_ROTATE)

    cam_x = px - distance * math.cos(angle_rad)
    cam_y = py - distance * math.sin(angle_rad)

    cam_z = pz + height + CAMERA_Z_REWORK

    if TOPVIEW:
        angle_rad = math.radians(MAOMAO.rotation + CAMERA_ROTATE)
        cam_x = px - 200 * math.cos(angle_rad)
        cam_y = py - 200 * math.sin(angle_rad)
        cam_z = pz + 300
        gluLookAt(cam_x, cam_y, cam_z, px, py, pz, 0, 0, 1)
    else:
        gluLookAt(cam_x, cam_y, cam_z, px, py, pz, 0, 0, 1)


def showScreen():
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glEnable(GL_BLEND)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, W, H)

    if NIGHT:
        glClearColor(0.25, 0.15, 0.25, 1)  # Dark mauve color for night
    else:
        glClearColor(0.85, 0.85, 0.95, 1)  # Lighter pink color

    setupCamera()
    MAOMAO.draw()
    House1.draw_housearea()
    House1.draw_house()
    pond.draw_pond()
    truck.draw_truck_kun()
    for tree in TREES:
        tree.draw_tree()

    for pillar in PILLARS:
        pillar.draw()

    for i in range(INVENTORY["chickens"]):
        CHICKENS[i].draw_chicken()

    for i in range(INVENTORY["cows"]):
        COWS[i].draw()

    BUCKET.position = [MAOMAO.position[0], MAOMAO.position[1], 20]
    if BUCKET_FLAG:
        BUCKET.draw_bucket()

    COOP.draw()
    COOP.draw_coop()
    farmLand()
    drawFences()
    drawPlots()
    BARN.draw_barn()

    # ! User Interface
    user_interface()

    # ? Double Buffering - Smoothness
    glutSwapBuffers()


def devDebug():  # ! Clearly AI Written, Remove After Finishing. Thank You.
    # Initialize timing variables on first call
    if not hasattr(devDebug, "last_print_time"):
        devDebug.last_print_time = time.time()
        devDebug.frame_count = 0
        devDebug.fps = 0

    current_time = time.time()
    devDebug.frame_count += 1
    elapsed_time = current_time - devDebug.last_print_time

    # Only print if at least 1 second has passed
    if elapsed_time < 1.0:
        return

    # Get player position
    x, y, z = MAOMAO.position

    # Calculate FPS based on actual elapsed time and frame count
    devDebug.fps = devDebug.frame_count / elapsed_time

    # Format and print debug information
    print(
        f"{glutGet(GLUT_ELAPSED_TIME)} : Player Position - X={x:.2f} Y={y:.2f} Z={z:.2f}"
    )
    print(f"FPS: {devDebug.fps:.2f}")
    print(f"Camera Extra Angle: {CAMERA_ROTATE}")

    # Reset counters for next interval
    devDebug.last_print_time = current_time
    devDebug.frame_count = 0

    # print(b1(MAOMAO.position))


def idle():
    global CAMERA_ROTATE

    if BUTTONS["a"]:
        MAOMAO.rotate(P_ROTATE_ANGLE)  # ? Rotate left
    if BUTTONS["d"]:
        MAOMAO.rotate(-P_ROTATE_ANGLE)  # ? Rotate right

    angle_rad = math.radians(MAOMAO.rotation)

    # ! Move Forward
    if BUTTONS["w"]:
        dx = P_SPEED * math.cos(angle_rad)
        dy = P_SPEED * math.sin(angle_rad)
        move = True

        # ? Position after movement
        moveX = MAOMAO.position[0] + dx
        moveY = MAOMAO.position[1] + dy
        moveZ = MAOMAO.position[2]

        # ? Check for collisions
        for collisions in BOUND_BOXES:
            if collisions([moveX, moveY, moveZ]):
                move = False
                break

        # ? If No Collision - Move
        if move:
            MAOMAO.move(dx, dy)

    # ! Move Backward
    if BUTTONS["s"]:
        dx = -P_SPEED * math.cos(angle_rad)
        dy = -P_SPEED * math.sin(angle_rad)
        move = True

        # ? Position after movement
        moveX = MAOMAO.position[0] + dx
        moveY = MAOMAO.position[1] + dy
        moveZ = MAOMAO.position[2]

        # ? Check for collisions
        for collisions in BOUND_BOXES:
            if collisions([moveX, moveY, moveZ]):
                move = False
                break

        # ? If No Collision - Move
        if move:
            MAOMAO.move(dx, dy)

    updateTime()

    # # ! Camera Movement With Limit
    # if BUTTONS["la"]:
    #     CAMERA_EXTRA_TURN = max(-26, CAMERA_EXTRA_TURN - 0.2)
    # if BUTTONS["ra"]:
    #     CAMERA_EXTRA_TURN = min(26, CAMERA_EXTRA_TURN + 0.2)

    # ! Camera Movement WithOut Limit
    if BUTTONS["la"]:
        CAMERA_ROTATE -= 0.2
    if BUTTONS["ra"]:
        CAMERA_ROTATE += 0.2

    devDebug()
    glutPostRedisplay()


# ! --------------------------------------- MAIN ---------------------------------------
# ! --------------------------------------- MAIN ---------------------------------------
# ! --------------------------------------- MAIN ---------------------------------------


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
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
