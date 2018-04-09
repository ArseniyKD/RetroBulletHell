import pygame  # load pygame keywords
import sys     # let python use the file system
import os      # help python identify the OS
import shared
import time

xMax = shared.width  # allows us to place further restrictions later
yMax = shared.height  # allows us to place further restrictions later

# the following was created using the help of this tutorial:
# https://opensource.com/article/17/12/game-python-add-a-player
# And the sprites we used for the player came from here:
# https://arboris.deviantart.com/art/Spaceship-sprites-43030167

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
            image = pygame.image.load(path).convert_alpha()
            _image_library[path] = image
        return image

_mask_library = {}
def get_mask(image):
    global _mask_library
    mask = _mask_library.get(image)
    if mask == None:
        mask = pygame.mask.from_surface(image)
        _mask_library[image] = mask
    return mask

class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 5
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.images = []  # note: all images are 39 by 43
        self.masks = []
        self.type0 = 0
        self.type1 = 1
        for i in range(4):
            self.images.append([])
            if i < 3:
                self.masks.append([])
            for j in range(3):
                img = get_image(os.path.join('images','player' + str(i) + str(j) + '.png'))
                self.images[i].append(img)
                if i < 3:
                    # mask = pygame.mask.from_surface(self.images[i][j])
                    mask = get_mask(self.images[i][j])
                    self.masks[i].append(mask)

        self.mask = self.masks[self.type0][self.type1]
        self.image = self.images[self.type0][self.type1]
        self.rect  = self.image.get_rect()


    def changeHealth(self, change, screen, player_list):
        if change < 0:
            self.image = self.images[3][self.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            self.image = self.images[self.type0][self.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            self.image = self.images[3][self.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()
            time.sleep(0.25)
            self.image = self.images[self.type0][self.type1]
            player_list.draw(screen) # draw player
            pygame.display.update()


        self.health += change
        if self.health > 0:
            return False
        else:
            return True

    def move(self,x,y):
        '''
        change sprite's location
        '''
        self.movex += x
        self.movey += y

    def constrain(self):
        if self.movex > 0:
            if self.rect.x + shared.imgWidth > shared.width - 5:
                self.rect.x = shared.width - shared.imgWidth - 5
        elif self.movex < 0:
            if self.rect.x < 0 + 5:
                self.rect.x = 0 + 5
        if self.movey > 0:
            if self.rect.y + shared.imgHeight > shared.height - 5:
                self.rect.y = shared.height - shared.imgHeight - 2
        elif self.movey < 0:
            if self.rect.y < 0 + 5:
                self.rect.y = 0 + 5

    def update(self):
        '''
        Update sprite position
        '''
        # record movex and movey before constraining so the correct images can
        # be used
        Movex = self.movex
        Movey = self.movey

        # update the position of the images and constrain them to the screen
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        self.constrain()

        #change player image to match movement input

        # default positions
        i = 1
        j = 1

        # if moving down
        if Movey > 0:
            i = 0
        # if moving up
        elif Movey < 0:
            i = 2

        # if moving left
        if Movex < 0:
            j = 0
        # if moving right
        elif Movex > 0:
            j = 2

        self.type0 = i
        self.type1 = j
        self.constrain()
        self.image = self.images[i][j]
        self.mask = self.masks[self.type0][self.type1]

    def reset(self):
        self.health = 5
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.rect.x = shared.width/2 - shared.imgWidth/2
        self.rect.y = shared.height - shared.height/4 - shared.imgHeight/2



# pass a pygame event to the function to check if it is a keypress or release
# that affects mmovement. Returns true if the player moves, and false if it did
# not
# This allows for users to use wasd and arrow keys for movement
def Move(event, player):
    flag = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            player.move(-shared.step, 0)
            flag = True
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            player.move(shared.step, 0)
            flag = True
        if event.key == pygame.K_UP or event.key == ord('w'):
            player.move(0, -shared.step)
            flag = True
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            player.move(0, shared.step)
            flag = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            player.move(shared.step, 0)
            flag = True
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            player.move(-shared.step, 0)
            flag = True
        if event.key == pygame.K_UP or event.key == ord('w'):
            player.move(0, shared.step)
            flag = True
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            player.move(0, -shared.step)
            flag = True
    return flag
