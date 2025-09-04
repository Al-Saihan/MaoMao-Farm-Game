from tkinter import font
from matplotlib import scale
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLUT import GLUT_STROKE_ROMAN
import math
import time

# ! --------------------------------------- :TODO: ---------------------------------------
# ! --------------------------------------- :TODO: ---------------------------------------
# ! --------------------------------------- :TODO: ---------------------------------------
# TODO: Make House Class -------------------------------------- Mao [Finished]
# TODO: Make Fence Class -------------------------------------- Saihan [Finished]
# TODO: Make Collision Class ---------------------------------- Saihan [Finished]
# TODO: Make Road --------------------------------------------- Saihan [Finished]
# TODO: Make Car/Shop(buy/sell point) Class ------------------- Mao
# TODO: Make Pond Class --------------------------------------- Mao [Finished]
# TODO: Make Farmable Plot Class [With Crop Specifier] --------
# TODO: Make Cows Barn Class ---------------------------------- Nusayba
# TODO: Make Cows Class --------------------------------------- Nusayba
# TODO: Make Hens Barn Class ---------------------------------- Mao
# TODO: Make Hens Class --------------------------------------- Mao
# TODO: Make Crops Class [Wheat, Potato, Carrot, Sunflower] ---
# TODO: Make Player Class [A Cat Humanoid] -------------------- Saihan [Finished]
# TODO: Water Mechanism ---------------------------------------
# TODO: Crops Grow Logic --------------------------------------
# TODO: Harvest Logic -----------------------------------------
# TODO: Inventory System --------------------------------------
# TODO: Buy/ Sell Logics --------------------------------------
# TODO: Cheat Modes -------------------------------------------
# TODO: Rain Logic --------------------------------------------
# TODO: Day-Night Cycle ---------------------------------------
# TODO: Design User Interface --------------------------------- Sauihan [WIP]


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
BALANCE = 0.0
TIME = {"hour": 6, "minute": 0}
WEATHER = "clear"  # ? Clear, Rainy
WATER = 10
MAX_WATER = 10
INVENTORY = {
    "wheat": 0,
    "potato": 0,
    "carrot": 0,
    "sunflower": 0,
    "chicken": 0,
    "egg": 0,
    "cow": 0,
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
        glVertex3f(50, 0, 0.1)  # ? pond left bottom point
        glColor3f(0.55, 0.75, 0.95)
        glVertex3f(300, 0, 0.1)  # ? pond right bottom point
        glColor3f(0.45, 0.70, 0.85)
        glVertex3f(300, -530, 0.1)  # ? pond right top point
        glColor3f(0.05, 0.15, 0.35)
        glVertex3f(50, -530, 0.1)  # ? pond left top point
        glEnd()
        glBegin(GL_QUADS)
        # ! Pond Area
        glColor3f(0.95, 0.75, 0.80)
        glVertex3f(80, -30, 0.5)  # ? pond left bottom point
        glColor3f(0.98, 0.70, 0.65)
        glVertex3f(270, -30, 0.5)  # ? pond right bottom point
        glColor3f(0.80, 0.70, 0.90)
        glVertex3f(270, -500, 0.5)  # ? pond right top point
        glColor3f(0.70, 0.50, 0.60)
        glVertex3f(80, -500, 0.5)  # ? pond left top point
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
        glColor3f(0.8, 0.5, 0.6)  # Brownish pink
        glutSolidCylinder(1, 1, 10, 10)
        glPopMatrix()
        
        #? Tree Head
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z + 80)
        glScalef(30, 30, 30)
        glColor3f(1.0, 0.7, 0.8)  # Sakura pink
        glutSolidSphere(1, 30, 30)
        glPopMatrix()
    

tree = Tree(600, 600, 0)    
    
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
        glTranslatef(self.position[0] - 70, self.position[1] - 30, self.position[2] + 60)
        glScalef(20, 1, 20)
        glColor3f(0.8, 0.9, 1.0)  # Blueish white color
        glutSolidCube(1)
        glPopMatrix()
        
        # ? Truck window right
        glPushMatrix()
        glTranslatef(558, 467, 30)
        glScalef(20, 1, 20)
        glColor3f(0.8, 0.9, 1.0)  # Blueish white color
        glutSolidCube(1)
        glPopMatrix()
        
        # ? Truck window front
        glPushMatrix()
        glTranslatef(self.position[0] - 70, self.position[1] - 75, self.position[2] + 30)
        glScalef(1, 40, 30)
        glColor3f(0.8, 0.9, 1.0)  # Blueish white color
        glutSolidCube(1)
        glPopMatrix()

        # ? Wheels (4 wheels)
        wheel_positions = [
            (75, 35, 10),
            (75, -35, 10),
            (180, 35, 10),
            (180, -35, 10),
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


class House:
    def __init__(self, position):
        self.position = position
        pass

    def draw_housearea(self):
        glBegin(GL_QUADS)
        # ! House Area
        glColor3f(0.95, 0.85, 0.4)  # ? Yellowish field color
        glVertex3f(-100, 380, 0.1)  # ? house area left bottom point
        glVertex3f(425, 380, 0.1)  # ? house area right bottom point
        glVertex3f(425, 725, 0.1)  # ? house area right top point
        glVertex3f(-100, 725, 0.1)  # ? house area left top point
        glEnd()
        # ! Garage
        glBegin(GL_QUADS)
        glColor3f(0.7, 0.7, 0.7)  # Light gray for the quad
        glVertex3f(425, 420, 0.11)
        glVertex3f(700, 420, 0.11)
        glVertex3f(700, 680, 0.11)
        glVertex3f(425, 680, 0.11)
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


class Coop:
    def name(self, position):
     pass

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
        scaleX = 250
        scaleY = 250
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
        height = 10
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z + height / 2)
        glScalef(150, 200, height)
        glutSolidCube(1)
        glPopMatrix()

print(BorderLine([0, 0, 0], [1, 0, 0]))

MAOMAO = Player([570, 617, 0], -90)

a1 = Fence([-740, -590, 10], [740, -590, 10])
a2 = Fence([-740, 740, 10], [740, 740, 10])
a3 = Fence([-740, -590, 10], [-740, 740, 10])
a4 = Fence([740, -590, 10], [740, 740, 10])

FENCES = [a1, a2, a3, a4]

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

t1 = Tree(100, 400, 0)
t2 = Tree(650, 550, 0)
t3 = Tree(-100, 550, 0)
TREES = [t1, t2, t3]


COOP = Coop(-200, -200, 0)

# ! --------------------------------------- Draw Functions ---------------------------------------
# ! --------------------------------------- Draw Functions ---------------------------------------
# ! --------------------------------------- Draw Functions ---------------------------------------


def farmLand():
    glBegin(GL_QUADS)
    # ! Grass Land
    glColor3f(0.0, 0.8, 0.0)  # ? Grass green color
    glVertex3f(-750, -600, 0)
    glVertex3f(750, -600, 0)
    glVertex3f(750, 750, 0)
    glVertex3f(-750, 750, 0)
    glEnd()

    # ! Road
    glBegin(GL_QUADS)
    glColor3f(0.95, 0.95, 0.5)  # ? Road brown color
    # ! 1
    glVertex3f(150, 250, 0.1)
    glVertex3f(750, 250, 0.1)
    glVertex3f(750, 150, 0.1)
    glVertex3f(150, 150, 0.1)

    # ! 2
    glVertex3f(-50, 230, 0.1)
    glVertex3f(150, 150, 0.1)
    glVertex3f(150, 250, 0.1)
    glVertex3f(-50, 330, 0.1)

    # ! 3
    glVertex3f(-750, 230, 0.1)
    glVertex3f(-50, 230, 0.1)
    glVertex3f(-50, 330, 0.1)
    glVertex3f(-750, 330, 0.1)

    # ! 4
    glVertex3f(-100, 50, 0.1)
    glVertex3f(0, 25, 0.1)
    glVertex3f(160, 160, 0.1)
    glVertex3f(120, 250, 0.1)

    # ! 5
    glVertex3f(-100, -600, 0.1)
    glVertex3f(0, -600, 0.1)
    glVertex3f(0, 50, 0.1)
    glVertex3f(-100, 50, 0.1)

    # ! 6
    glVertex3f(330, -300, 0.1)
    glVertex3f(400, -300, 0.1)
    glVertex3f(400, 150, 0.1)
    glVertex3f(330, 150, 0.1)

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
    draw_text(105, H - 30, "MaoMao Farming Simulator", (0, 0, 0))
    draw_text(105, H - 60, f"Balance: {BALANCE:.2f}$", (0, 0, 0))
    draw_text(105, H - 90, f"Time: {TIME['hour']:02}:{TIME['minute']:02}", (0, 0, 0))
    draw_text(W - 200, H - 30, f"Weather: {WEATHER}", (0, 0, 0))

    # ? TEXTS Background - (Bottom Left)
    draw_text(15, H - 500, "Inventory:", (0, 0, 0))
    glColor3f(0.85, 0.7, 0.85)  # Lighter mauve color
    glBegin(GL_QUADS)
    glVertex2f(12, H - 510)
    glVertex2f(150, H - 510)
    glVertex2f(150, H - 510 - 30 * len(INVENTORY) + 33)
    glVertex2f(12, H - 510 - 30 * len(INVENTORY) + 33)
    glEnd()

    # ? Inventory Border
    glLineWidth(1)
    glBegin(GL_LINE_STRIP)
    glColor3f(0, 0, 0)
    glVertex2f(12, H - 510)
    glVertex2f(150, H - 510)
    glVertex2f(150, H - 510 - 30 * len(INVENTORY) + 33)
    glVertex2f(12, H - 510 - 30 * len(INVENTORY) + 33)
    glVertex2f(12, H - 510)
    glEnd()

    # ? Inventory Items (Write and Underline)
    for k, v in INVENTORY.items():
        index = list(INVENTORY.keys()).index(k) + 1
        draw_text(15, H - 500 - 30 * index, f"{k.capitalize()}: {v}", (0, 0, 0))
        glColor3f(0.6, 0.4, 0.6)
        glBegin(GL_LINES)
        glVertex2f(15, H - 500 - 30 * index - 5)
        glVertex2f(140, H - 500 - 30 * index - 5)
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
    glClearColor(0.53, 0.81, 0.92, 1)  # Sky blue color
    setupCamera()

    MAOMAO.draw()
    House1.draw_housearea()
    House1.draw_house()
    pond.draw_pond()
    truck.draw_truck_kun()
    for tree in TREES:
        tree.draw_tree()

    farmLand()
    drawFences()
    drawPlots()
    COOP.draw()

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
