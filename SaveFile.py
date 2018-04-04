def SaveFile(enemyBullets, playerBullets, player):
    ostream = open('save.txt', 'w')
    for e in shared.enemy_list:
        ostream.write('e' + str(e.rect.x) + str(e.rect.y) + ',')
    for b in enemyBullets:
        ostream.write('b' + str(b.type) + str(b.rect.x) + str(b.rect.y) + str(b.angle) + ',')
    for b in playerBullets:
        ostream.write('b' + str(b.type) + str(b.rect.x) + str(b.rect.y) + str(b.angle) + ',')

    ostream.write('p' + str(player.rect.x) + str(player.rect.y) + '--')

def LoadFile():
    ostream = open('save.txt', 'r')
    
