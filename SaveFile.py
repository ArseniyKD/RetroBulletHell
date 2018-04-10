import Bullets
import PlayerMovement
import shared
import EnemyCreation
import pygame

def saveFile(enemyWaves, enemy_bullet_list, player_bullet_list, player, score):
    ostream = open('save.txt', 'w')
    for e in enemyWaves:
        ostream.write('e' + ',' + str(e.Etype) + ',' + str(e.currentY) + ',' + str(e.initialX))
        for i in e.activeIndecies:
            ostream.write(',' + str(i) + ',' + str(e.IndexEnemyWave(i).health))
        ostream.write(' ')
    for b in enemy_bullet_list:
        ostream.write('be' + ',' + str(b.type) + ',' + str(b.rect.x) + ',' + str(b.rect.y) + ',' + str(b.angle) + ' ')
    for b in player_bullet_list:
        ostream.write('bp' + ',' + str(b.type) + ',' + str(b.rect.x) + ',' + str(b.rect.y) + ' ')
    ostream.write('p' + ',' + str(player.rect.x) + ',' + str(player.rect.y) + ',' + str(player.health) + ' ')
    ostream.write('s' + ',' + str(score))


def loadFile():
    try:
        istream = open('save.txt', 'r')
    except:
        print("A save file could not be found")
        return False
    Input = istream.read().split()
    enemyWaves = []
    player_bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()
    score = 0
    for I in Input:
        X = I.split(',')
        # create an enemy wave
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

            enemyWaves[-1].activeIndecies = list(dictionary.keys())
            for j in range(enemyWaves[-1].Size):
                if j not in dictionary.keys():
                    # remove inactive enemies from the list
                    shared.enemy_list.remove(enemyWaves[-1].IndexEnemyWave(j))
                else:
                    #
                    enemyWaves[-1].IndexEnemyWave(j).health = dictionary[j]
            # set the correct size of the wave
            enemyWaves[-1].Size = len(enemyWaves[-1].activeIndecies)

        # create a bullet
        elif I[0] == 'b':
            if I[1] == 'e':
                b = Bullets.Bullet(X[1], angle = int(X[4]), x = int(X[2]), y = int(X[3]))
                enemy_bullet_list.add(b)
            elif I[1] == 'p':
                b = Bullets.Bullet(X[1], x = int(X[2]), y = int(X[3]))
                player_bullet_list.add(b)

        # create the player character
        elif I[0] == 'p':
            p = PlayerMovement.Player()
            p.rect.x = int(X[1])
            p.rect.y = int(X[2])
            p.health = int(X[3])

        elif I[0] == 's':
            score = int(X[1])

    return (enemyWaves, enemy_bullet_list, player_bullet_list, p, score)
