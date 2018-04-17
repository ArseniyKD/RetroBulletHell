# Created by Arseniy Kouzmenkov 1542302 and Patrisha de Boon 1496979

import Bullets
import PlayerMovement
import shared
import EnemyCreation
import pygame

# convert all necessary imformation from all applicatble data structures into
# a text file.
def saveFile(enemyWaves, enemy_bullet_list, player_bullet_list, player, score):
    # open an output stream to the save file
    ostream = open('save.txt', 'w')
    # iterate through enemy waves and record the etype, the currentY, and the
    # intial x
    for e in enemyWaves:
        ostream.write('e' + ',' + str(e.Etype) + ',' + str(e.currentY) + ',' + str(e.initialX))
        # iterate though all active enemies and record their index and health
        for i in e.activeIndecies:
            ostream.write(',' + str(i) + ',' + str(e.IndexEnemyWave(i).health))
        ostream.write(' ')
    # iterate through all enemy bullets and record their type, location, and angle
    for b in enemy_bullet_list:
        ostream.write('be' + ',' + str(b.type) + ',' + str(b.rect.x) + ',' + str(b.rect.y) + ',' + str(b.angle) + ' ')
    # iterate through all player bullets and record their type, location, and angle
    for b in player_bullet_list:
        ostream.write('bp' + ',' + str(b.type) + ',' + str(b.rect.x) + ',' + str(b.rect.y) + ' ')
    # record the locationi and health of the player, and the score
    ostream.write('p' + ',' + str(player.rect.x) + ',' + str(player.rect.y) + ',' + str(player.health) + ' ')
    ostream.write('s' + ',' + str(score))

# convert information in a text file into data structures with which the game
# can run, allowing the player to continue from a previous save
def loadFile():
    # try opening a save file, and return an error if the file can't be opened
    try:
        istream = open('save.txt', 'r')
    except:
        print("A save file could not be found")
        return False
    # record the text in the istream and initialize the applicable data structures
    Input = istream.read().split()
    enemyWaves = []
    player_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()
    score = 0
    # iterate through each space seperated protion of Index
    for I in Input:
        # create a list of the comma seperated terms in I
        X = I.split(',')
        # create an enemy wave if the text portion starts with e
        if I[0] == 'e':
            # create the enemy wave and add it to the wave list and include
            # the Etype
            enemyWaves.append(EnemyCreation.EnemyWave(int(X[1])))
            # create enemies in the enemy wave, according to their Etype,
            # the initialX, and the current Y
            enemyWaves[-1].CreateEnemyWave(int(X[3]), int(X[2]))
            dictionary = {}
            j = 4
            while j < len(X)-1:
                dictionary[int(X[j])] = int(X[j+1])
                j += 2
            # remove the enemies that were not active in the save file, and
            # record the health of the remaining active enemies
            enemyWaves[-1].activeIndecies = list(dictionary.keys())
            for j in range(enemyWaves[-1].Size):
                if j not in dictionary.keys():
                    # remove inactive enemies from the list
                    shared.enemy_list.remove(enemyWaves[-1].IndexEnemyWave(j))
                else:
                    enemyWaves[-1].IndexEnemyWave(j).health = dictionary[j]
            # set the correct size of the wave
            enemyWaves[-1].Size = len(enemyWaves[-1].activeIndecies)

        # create a bullet if the text portion starts with b
        elif I[0] == 'b':
            # create an enemy bullet and record the type, location, and angle
            if I[1] == 'e':
                b = Bullets.Bullet(X[1], angle = int(X[4]), x = int(X[2]), y = int(X[3]))
                enemy_bullet_list.add(b)
            # create a player bullet and record the type and location
            elif I[1] == 'p':
                b = Bullets.Bullet(X[1], x = int(X[2]), y = int(X[3]))
                player_bullet_list.add(b)

        # create the player character if the text portion starts with p, record
        # the player's location and health
        elif I[0] == 'p':
            p = PlayerMovement.Player()
            p.rect.x = int(X[1])
            p.rect.y = int(X[2])
            p.health = int(X[3])

        # record the score if the text portion starts with s
        elif I[0] == 's':
            score = int(X[1])

    # return all of the information needed to run the game from the save point
    return (enemyWaves, enemy_bullet_list, player_bullet_list, p, score)
