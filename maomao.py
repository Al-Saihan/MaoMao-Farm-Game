from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLUT import GLUT_STROKE_ROMAN
import math
import time
import os

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
# TODO: Make Farmable Plot Class [With Crop Specifier] --------
# TODO: Make Cows Barn Class ---------------------------------- Nusayba
# TODO: Make Cows Class --------------------------------------- Nusayba
# TODO: Make Hens Barn Class ---------------------------------- Mao [Finished]
# TODO: Make Hens Class --------------------------------------- Mao [Finished]
# TODO: Make Crops Class [Wheat, Potato, Carrot, Sunflower] ---
# TODO: Make Player Class [A Cat Humanoid] -------------------- Saihan [Finished]
# TODO: Water Mechanism ---------------------------------------
# TODO: Crops Grow Logic --------------------------------------
# TODO: Harvest Logic -----------------------------------------
# TODO: Inventory System --------------------------------------
# TODO: Buy/ Sell Logics -------------------------------------- Saihan [WIP]
# TODO: Cheat Modes -------------------------------------------
# TODO: Rain Logic --------------------------------------------
# TODO: Day-Night Cycle ---------------------------------------
# TODO: Design User Interface --------------------------------- Sauihan [Finished]


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
LAST_TIME_UPDATE = time.time()
DAY = 0
BALANCE = 0.0
TIME = {"hour": 6, "minute": 0}
WEATHER = "clear"  # ? Clear, Rainy
NIGHT = False
WATER = 10
MAX_WATER = 10
INVENTORY = {
    "wheat": 0,
    "potato": 0,
    "carrot": 0,
    "sunflower": 0,
    "chickens": 0,
    "egg": 0,
    "cows": 2,
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
        self.x = x
        self.y = y
        self.z = z

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
    def __init__(self, position):
        self.position = position
        pass

    def draw_bucket(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2] + 5)
        glScalef(5, 5, 5)
        glColor3f(0.8, 0.8, 0.9)  # Light grayish blue
        glutSolidCube(1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2] + 7.5)
        glScalef(4, 4, 0.1)
        glColor3f(0.2, 0.2, 0.2)  # Dark grey for empty inside effect
        glutSolidCube(1)
        glPopMatrix()

bucket = Bucket([200, 200, 0.1])

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

        glColor3f(0.9, 0.9, 0.9)  # ? Off-White Color
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

        if abs(distance) < self.strength:
            return True
        return False


class Plot:
    def __init__(self, position):
        self.position = position

    def draw(self):
        scaleX = 150
        scaleY = 150
        glColor3f(244 / 255, 223 / 255, 144 / 255)  # ? Lighter brown color for soil
        glPushMatrix()
        glTranslatef(*self.position)
        glScale(scaleX, scaleY, 2)
        glutSolidCube(1)
        glPopMatrix()

        glColor3f(180 / 255, 150 / 255, 80 / 255)
        glPushMatrix()
        glTranslatef(*self.position)
        glTranslatef(0, 50, 0)
        glScale(scaleX, 1, 3)
        glutSolidCube(1)
        glTranslatef(0, -100, 0)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(*self.position)
        glTranslatef(50, 0, 0)
        glScale(1, scaleY, 3)
        glutSolidCube(1)
        glTranslatef(-100, 0, 0)
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
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def draw_chicken(self):
        # ? Chicken Body
        glColor3f(1.0, 0.8, 0.9)  # Light pink
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z + 10)
        glScalef(10, 5, 7)
        glutSolidCube(1)
        glPopMatrix()

        # ? Chicken Head
        glPushMatrix()
        glTranslatef(self.x + 5, self.y, self.z + 15)
        glScalef(5, 5, 5)
        glutSolidCube(1)
        glPopMatrix()

        # ? beck
        glPushMatrix()
        glTranslatef(self.x + 9, self.y, self.z + 15)
        glScalef(3, 4, 1)
        glColor3f(1.0, 0.5, 0.0)  # Orange color for beck
        glutSolidCube(1)
        glPopMatrix()

        # ? red comb
        glPushMatrix()
        glTranslatef(self.x + 7, self.y, self.z + 14)
        glScalef(2, 2, 2)
        glColor3f(1.0, 0.0, 0.0)  # Red color for comb
        glutSolidCube(1)
        glPopMatrix()

        # ? Chicken Legs -- left
        glPushMatrix()
        glTranslatef(self.x, self.y + 1, self.z + 5)
        glScalef(1, 1, 3)
        glColor3f(1.0, 0.5, 0.0)  # Orange color for legs
        glutSolidCube(1)
        glPopMatrix()

        # ? Chicken Legs -- right
        glPushMatrix()
        glTranslatef(self.x, self.y - 1, self.z + 5)
        glScalef(1, 1, 3)
        glColor3f(1.0, 0.5, 0.0)  # Orange color for legs
        glutSolidCube(1)
        glPopMatrix()

        # ? Chicken Eyes
        glBegin(GL_POINTS)
        glColor3f(0.0, 0.0, 0.0)  # Black color for eyes
        glVertex3f(self.x + 7.8, self.y - 1, self.z + 17)
        glVertex3f(self.x + 7.8, self.y + 1, self.z + 17)
        glEnd()

        # ? chicken wings
        glPushMatrix()
        glTranslatef(self.x, self.y - 2.8, self.z + 10)
        glScalef(6, 1, 4)
        glColor3f(0.9, 0.5, 0.7)  # Lighter pink
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(self.x, self.y + 2.8, self.z + 10)
        glScalef(6, 1, 4)
        glColor3f(0.9, 0.5, 0.7)  # Lighter pink
        glutSolidCube(1)
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

print(BorderLine([0, 0, 0], [1, 0, 0]))

MAOMAO = Player([-161, 299, 0], 110)

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

BOUND_BOXES = [b1, b2, b3, b4]

p1 = Plot([570, -20, 1])
p2 = Plot([570, -350, 1])
# p3 = Plot([-200, 200, 1])
# p4 = Plot([200, -200, 1])

PLOTS = [p1, p2]

t1 = Tree(203.79333586600404, 58.59383956134186, 0)
t2 = Tree(396.9853972831635, 343.36338720735466, 0)
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

chicken1 = Chicken(-150, -150, 0)
chicken2 = Chicken(-200, -130, 0)
chicken3 = Chicken(-170, -180, 0)
CHICKENS = [chicken1, chicken2, chicken3]

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

    # ? Inventory Items (Write and Underline)
    for k, v in INVENTORY.items():
        index = list(INVENTORY.keys()).index(k) + 1
        draw_text(15, H - 470 - 30 * index, f"{k.capitalize()}: {v}", (0, 0, 0))
        glColor3f(0.6, 0.4, 0.6)
        glBegin(GL_LINES)
        glVertex2f(15, H - 470 - 30 * index - 5)
        glVertex2f(140, H - 470 - 30 * index - 5)
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

    # ! CHEAT: Night On/Off (R key)
    if key.lower() == b"r":
        global NIGHT
        NIGHT = not NIGHT

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
    if key == b"v":
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


def mouseListener(button, state, x, y):
    global FOV, CAMERA_Z_REWORK, TOPVIEW

    zoomUpStep = 4
    zoomDownStep = 6

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        with open(config_path, "a") as f:
            print("Writing to config.txt")
            f.write(
                f"a = Fence({MAOMAO.position[0]}, {MAOMAO.position[1]}, {MAOMAO.position[2]})\n"
            )

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

    glutPostRedisplay()

def updateTime():
    global TIME, LAST_TIME_UPDATE, NIGHT

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
        glClearColor(0.1, 0.1, 0.2, 1)  # Dark night color
    else:
        glClearColor(0.53, 0.81, 0.92, 1)  # Sky blue color

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

    for chimken in CHICKENS:
        chimken.draw_chicken()

    for i in range(INVENTORY["cows"]):
        COWS[i].draw()

    bucket.draw_bucket()
    
    
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
