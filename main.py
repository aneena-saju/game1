import pygame as py
from pygame.locals import *
import random
import math
import time
import numpy as np

py.init()
# Set up the drawing window
width, height = 700, 1000
screen = py.display.set_mode((width, height), py.HWSURFACE)
clock = py.time.Clock()

background = py.image.load("./assets/Grid3.png")
background = py.transform.scale(background, (width, height))
background_position = 0
scroll_speed = 0
# sleep_time = 0.00008

###################################################Globals##############################################################

space = []  # List to store the random rectangles

LASER_X = 0
LASER_Y = 0
LASER_COLOR = (255, 0, 0)
INERTIA_FACTOR = 0.95
MAX_OBJECTS = 25
MAX_SCROLL = 20
CLOCK_RATE = 30

######################################################++++ASSETS++++####################################################

tief1 = py.image.load("assets/tie.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
tief1 = py.transform.scale(tief1, (25, 25))  # Scale the image to the desired size
tief2 = py.image.load("assets/tie2.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
tief2 = py.transform.scale(tief2, (25, 25))


class TieFighter:
    def __init__(self, x, y, var):
        self.speed = 0
        self.x = x
        self.y = y
        if var == 1:
            self.image = tief1
        elif var == 2:
            self.image = tief2
        else:
            self.image = tief1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect()


spaceship_image = py.image.load("./assets/flcn.png")  # Replace "spaceship.png" with the actual file path of your spaceship image
spaceship_image = py.transform.scale(spaceship_image, (80, 100))  # Scale the image to the desired size
spaceship_x = width // 2 - 50
spaceship_y = height - 100


class SpaceShip:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y
        self.max_speed: int = 8
        self.min_speed: int = -8
        self.spaceship_x_vel: int = 0
        self.spaceship_y_vel: int = 0
        self.spaceship_speed: int = 1

    def set_x_vel(self, vel):
        self.spaceship_x_vel += self.spaceship_speed * vel
        # print(self.spaceship_x_vel)

    def set_y_vel(self, vel):
        self.spaceship_y_vel += self.spaceship_speed * vel

    def draw(self):
        screen.blit(spaceship_image, (self.x, self.y))

    @staticmethod
    def get_rect():
        return spaceship_image.get_rect()


class Laser:
    def __init__(self, x, y):
        self.laser_width = 2
        self.laser_height = 10
        self.laser_color = (255, 0, 0)
        self.laser_speed = 1
        self.max_laser_speed = 20
        self.laser_vel = 0
        self.laser_x = x
        self.laser_y = y
        self.laser_state = True

    def draw(self, laser_color):
        self.laser_color = laser_color
        # self.laser_x = laser_x
        # self.laser_y = laser_y
        # self.laser_width = laser_width
        # self.laser_height = laser_height
        py.draw.rect(screen, self.laser_color, (self.laser_x, self.laser_y, self.laser_width, self.laser_height))

    def get_rect(self):
        return py.Rect(self.laser_x, self.laser_y, self.laser_width, self.laser_height)


astr1 = py.image.load("assets/asteroid1.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
astr1 = py.transform.scale(astr1, (40, 40))  # Scale the image to the desired size
astr2 = py.image.load("assets/asteroid2.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
astr2 = py.transform.scale(astr2, (35, 35))


class Asteroid:
    def __init__(self, x, y, var):
        self.x = x
        self.y = y
        self.speed = 0
        if var == 1:
            self.image = astr1
        elif var == 2:
            self.image = astr2
        else:
            self.image = astr2

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect()


health = py.image.load("assets/health.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
health = py.transform.scale(health, (20, 20))


class HealthIcon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = astr1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect()


explosion = py.image.load("./assets/sexp_sprite.png")
# print(explosion.get_height())
# explosion = py.transform.scale(explosion, (100, 800))
# print(explosion.get_width())

class Explotion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = explosion
        self.sprite_width = 50
        self.sprite_height = 50
        # Define the number of columns and rows in the sprite sheet
        self.columns = 5
        self.rows = 1

        # List to store individual sprites
        self.sprites = []
        # self.sx,self.sy = 0
        # print(sy)
        for row in range(self.rows):
            for col in range(self.columns):
                # nx = self.sx + (col * self.sprite_width)
                # ny = self.sy + (row * self.sprite_height)
                sx = col * self.sprite_width
                sy = row * self.sprite_height
                self.sprite = self.image.subsurface((sx, sy, self.sprite_width, self.sprite_height))
                self.sprites.append(self.sprite)

    def draw(self):
        # screen.blit(self.sprites[0], (self.x, self.y))
        # py.display.flip()
        # # time.sleep(0.2)
        # py.time.delay(200)
        # screen.blit(self.sprites[1], (self.x, self.y))
        # py.display.flip()
        # time.sleep(0.2)
        for sprite in self.sprites:
            # x = (index % self.columns) * self.sprite_width
            # y = (index // self.columns) * self.sprite_height
            # print(self.sprite)
            screen.blit(sprite, (self.x, self.y))
            py.display.flip()
            py.time.delay(10)
    def get_rect(self):
        return self.image.get_rect()


########################################################################################################################

millenium_falcon = SpaceShip(spaceship_x, spaceship_y)
laserx = Laser(LASER_X, LASER_Y)


#######################################################################################################################3

def check_collision():
    for rectx in space:
        # py.draw.rect(screen, (255, 0, 0), millenium_falcon.get_rect().move(millenium_falcon.x, millenium_falcon.y))
        # py.draw.rect(screen, (255, 255, 0), laserx.get_rect())
        rect_pos = rectx.get_rect().move(rectx.x, rectx.y)
        if millenium_falcon.get_rect().move(millenium_falcon.x, millenium_falcon.y).colliderect(rect_pos):
            # print(millenium_falcon.get_rect(), rectx.get_rect())
            # Handle collision response here
            print("Collision occurred MF")
            # break
        if laserx.get_rect().colliderect(rect_pos) and not laserx.laser_state:
            print("Coll laser")
            py.draw.rect(screen, (255, 255, 0), (rect_pos.x, rect_pos.y, 10, 10))
            laserx.laser_state = True
            # laserx.draw(LASER_COLOR)
            new_explosion = Explotion(rect_pos.x - 10, rect_pos.y - 10)
            new_explosion.draw()


def render_space(space):
    # Update and draw the rectangles
    i = 0  # print(rectangles)
    while i < len(space):
        spaceObject = space[i]
        spaceObject.y += math.ceil(scroll_speed) + spaceObject.speed
        # print(sleep_time)
        # time.sleep(sleep_time)
        spaceObject.draw()
        # Check if the rectangle has left the screen
        if spaceObject.y > height:
            # Remove the rectangle from the list
            space.pop(i)
        else:
            i += 1


def fire_laser():
    if laserx.laser_state:
        laserx.laser_state = False
        laserx.laser_x = millenium_falcon.x + 40
        laserx.laser_y = millenium_falcon.y


################################################ Main  Function ########################################################

def main(Running):
    global background_position, scroll_speed
    health_flag = 0

    while Running:
        # Did the user click the window close button?
        for event in py.event.get():
            if event.type == py.QUIT:
                Running = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    fire_laser()

        keys = py.key.get_pressed()
        # Update spaceship position based on pressed keys
        if keys[py.K_w]:
            # spaceship_y_vel -= spaceship_speed
            millenium_falcon.set_y_vel(-1)
        if keys[py.K_s]:
            millenium_falcon.set_y_vel(1)
        if keys[py.K_a]:
            millenium_falcon.set_x_vel(-1)
        if keys[py.K_d]:
            millenium_falcon.set_x_vel(1)

        ################################################################################################################
        clock.tick(CLOCK_RATE)
        ################################################################################################################

        millenium_falcon.spaceship_x_vel *= INERTIA_FACTOR
        millenium_falcon.spaceship_y_vel *= INERTIA_FACTOR

        # Limit the maximum speed
        spaceship_velocity_x = np.clip(millenium_falcon.spaceship_x_vel, millenium_falcon.min_speed, millenium_falcon.max_speed)
        spaceship_velocity_y = np.clip(millenium_falcon.spaceship_y_vel, millenium_falcon.min_speed, millenium_falcon.max_speed)

        # Update spaceship position based on velocity
        millenium_falcon.x = np.clip(millenium_falcon.x + spaceship_velocity_x, 0, width - 80)
        millenium_falcon.y = np.clip(millenium_falcon.y + spaceship_velocity_y, 0, height - 100)
        # print(millenium_falcon.spaceship_x_vel,spaceship_velocity_x)

        if not laserx.laser_state:
            laserx.laser_vel += laserx.laser_speed
            laserx.laser_vel *= INERTIA_FACTOR
            laserx.laser_vel = min(laserx.laser_vel, laserx.max_laser_speed)
            # print(laserx.laser_vel)
            laserx.laser_y -= laserx.laser_vel
            if laserx.laser_y < 0:
                laserx.laser_state = True

        ############################################################++++++++ Background ++++++++++++####################

        background_position += scroll_speed
        # Wrap the background around when it goes beyond the window height
        if background_position >= height:
            background_position = 0

        ############################################################++++++++ Generator ++++++++++++#####################
        # Generate a new random rectangle and add it to the list
        SPACE_LENGTH = len(space)
        if SPACE_LENGTH <= MAX_OBJECTS:  # Limit to 5 rectangles
            # rect_width = 20
            # rect_height = 20
            # Generate rect_x at least 50 pixels away from the last drawn rectangle
            if SPACE_LENGTH == 0:
                rect_x = width / 2
                rect_y = height - 20
            else:
                last_rect = space[-1]
                # print(last_rect)
                # min_x = min(random.choice([last_rect.x - 50, last_rect.x + last_rect.width + 50]), width)
                min_x = np.clip(last_rect.x - 400, 0, last_rect.x + 250)
                # print(min_x)
                max_x = width
                rect_x = random.randint(max(min_x, 0), min(max_x, width - 30))
                rect_y = random.randint(-height // 2, 0)  # Start rectangles above the screen

            # rect_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # rect = py.Rect(rect_x, rect_y, rect_width, rect_height)
            # print(rect)
            var = random.randint(1, 2)
            speed_modifer = random.randint(0, 2)
            random_draw = random.randint(1, 2)

            if random_draw == 1:
                new_tie = TieFighter(rect_x, rect_y, var)
                new_tie.speed = speed_modifer
                space.append(new_tie)
            elif random_draw == 2:
                new_asteroid = Asteroid(rect_x, rect_y, var)
                new_asteroid.speed = speed_modifer
                space.append(new_asteroid)
            else:
                pass

            if SPACE_LENGTH == MAX_OBJECTS:
                if health_flag == 30:
                    new_health = HealthIcon(rect_x, rect_y)
                    space.append(new_health)
                    health_flag = 0
                else:
                    health_flag += SPACE_LENGTH

        # Draw the background image
        screen.blit(background, (0, background_position))
        screen.blit(background, (0, background_position - height))

        #################################### Draw #####################################################################

        render_space(space)
        millenium_falcon.draw()
        if not laserx.laser_state:
            laserx.draw(LASER_COLOR)

        ################################### Events #####################################################################

        if SPACE_LENGTH > 5:
            check_collision()

        ###########################################Screen###############################################################

        py.display.flip()
        if scroll_speed <= MAX_SCROLL:
            scroll_speed += 0.001
        # scroll_speed += 0.01
        # print(scroll_speed)

    # Done
    py.quit()


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    main(True)
