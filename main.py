from __future__ import division
import pygame
import time
import os
import sys
import glob
import random
pygame.init()
screen=pygame.display.set_mode((1000,1000))
spikesound=pygame.mixer.Sound("sounds/spike.wav")
bombsound=pygame.mixer.Sound("sounds/bomb.wav")
explosionsound=pygame.mixer.Sound("sounds/explosion.wav")
electricitysound=pygame.mixer.Sound("sounds/electricity.wav")
lasersound=pygame.mixer.Sound("sounds/laser.wav")
powerupsound=pygame.mixer.Sound("sounds/powerup.wav")
boostsound=pygame.mixer.Sound("sounds/boost.wav")
rocksound=pygame.mixer.Sound("sounds/rock.wav")
wallsound=pygame.mixer.Sound("sounds/wall.wav")
teleportersound=pygame.mixer.Sound("sounds/teleporter.wav")
teleportationsound=pygame.mixer.Sound("sounds/teleportation.wav")
lavasound=pygame.mixer.Sound("sounds/lava.wav")
walksound=pygame.mixer.Sound("sounds/walk.wav")
jumpsound=pygame.mixer.Sound("sounds/jump.wav")
damagesound=pygame.mixer.Sound("sounds/damage.wav")
duckingsound=pygame.mixer.Sound("sounds/duck.wav")
scrollsound=pygame.mixer.Sound("sounds/scroll.wav")
clicksound=pygame.mixer.Sound("sounds/click.wav")
hitsound=pygame.mixer.Sound("sounds/hit.wav")
spikes=[]
bombs=[]
electricbarriers=[]
lasers=[]
lavablocks=[]
rocks=[]
walls=[]
teleporters=[]
powerups=[]
monsters=[]
modobjects=[]
moddict={}
maxpos=100
codetoexecute=[]
modfunctions={}
def addfunction(name,func) :
    modfunctions[name]=func
def execfuncs(name,funcdict) :
    for func in funcdict.keys() :
        if func == name :
            funcdict[func]()
def playerinrange(player) :
    for spike in spikes :
        if spike.pos in range (player.pos+1,player.pos+11) or spike.pos in range(player.pos-10,player.pos) :
            return True
    for bomb in bombs :
        if bomb.pos in range(player.pos+1,player.pos+11) or bomb.pos in range(player.pos-10,player.pos) :
            return True
    for electricbarrier in electricbarriers :
        if electricbarrier.pos in range(player.pos+1,player.pos+11) or electricbarrier in range(player.pos-10,player.pos) :
            return True
    for laser in lasers :
        if laser.pos in range(player.pos+1,player.pos+11) or laser.pos in range(player.pos-10,player.pos) :
            return True
    for lava in lavablocks :
        if lava.pos in range(player.pos+1,player.pos+11) or lava.pos in range(player.pos-10,player.pos) :
            return True
    for rock in rocks :
        if rock.pos in range(player.pos+1,player.pos+11) or rock.pos in range(player.pos-10,player.pos) :
            return True
    for wall in walls :
        if wall.pos in range(player.pos+1,player.pos+11) or wall.pos in range(player.pos-10,player.pos) :
            return True
    for teleporter in teleporters :
        if teleporter.pos in range(player.pos+1,player.pos+11) or teleporter.pos in range(player.pos-10,player.pos) :
            return True
    for powerup in powerups :
        if powerup.pos in range(player.pos+1,player.pos+11) or powerup.pos in range(player.pos-10,player.pos) :
            return True
    for monster in monsters :
        if monster.pos in range(player.pos+1,player.pos+11) or monster.pos in range(player.pos-10,player.pos) :
            return True
    for modobject in modobjects :
        if modobject.pos in range(player.pos+1,player.pos+11) or modobject.pos in range(player.pos-10,player.pos) :
            return True
    return False
def say(txt) :
    os.system("say \"{}\"".format(txt))
class Player() :
    def __init__(self) :
        self.pos=1
        self.maxtimer=60
        self.fighting=False
        self.jumping=False
        self.ducking=False
        self.health=10
        self.jumptimer=0
        self.monstertimer=0
        self.damage=2
    def attack(self,monster) :
        hitsound.play()
        monster.health-=self.damage
    def update(self) :
        if self.pos > maxpos :
            self.pos=maxpos
        if self.pos < 1 :
            self.pos=1
        if self.jumping :
            self.jumptimer-=1
        if self.jumping and self.jumptimer <= 0 :
            self.jumping=False
            self.jumptimer=0
            walksound.play()
        if playerinrange(self) :
            self.maxtimer=9
        else :
            self.maxtimer=60
        if self.health <= 0 :
            os.system("say \" you died\"")
            reset()
            currentscene.switchscene(Mainmenu())
        execfuncs("playerupdate",modfunctions)
player=Player()
class Spike() :
    def __init__(self,pos) :
        self.pos=pos
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=spikesound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            spikesound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=spikesound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            spikesound.stop()
        if self.pos == player.pos and not player.jumping :
            c=spikesound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            spikesound.stop()
            player.health-=2
            player.pos-=1
            damagesound.play()
        if player.pos == self.pos and player.jumping :
            c=spikesound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            spikesound.stop()
        execfuncs("spikeupdate",modfunctions)
class Bomb() :
    def __init__(self,pos) :
        self.pos=pos
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=bombsound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            bombsound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=bombsound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            bombsound.stop()
        if self.pos == player.pos and not player.jumping :
            explosionsound.play()
            player.health-=5
            damagesound.play()
            bombs.remove(self)
        if self.pos == player.pos and player.jumping :
            c=bombsound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            bombsound.stop()
        execfuncs("bombupdate",modfunctions)
class Electricbarrier() :
    def __init__(self,pos) :
        self.pos=pos
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=electricitysound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            electricitysound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=electricitysound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            electricitysound.stop()
        if self.pos == player.pos and not player.jumping :
            c=electricitysound.play()
            c.set_volume(1.0,1.0)
            damagesound.play()
            player.health-=5
            player.pos-=1
        if player.pos == self.pos and player.jumping :
            c=electricitysound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            electricitysound.stop()
        execfuncs("electricbarrierupdate",modfunctions)
class Laser() :
    def __init__(self,pos) :
        self.pos=pos
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=lasersound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            lasersound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=lasersound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            lasersound.stop()
        if self.pos == player.pos and not player.ducking :
            c=lasersound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            lasersound.stop()
            damagesound.play()
            player.health-=5
            player.pos+=1
        if self.pos == player.pos and player.ducking :
            c=lasersound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            lasersound.stop()
        execfuncs("laserupdate",modfunctions)
class Lava() :
    def __init__(self,pos) :
        self.pos=pos
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=lavasound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.5)
            lavasound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=lavasound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.5)
            lavasound.stop()
        if self.pos == player.pos and not player.jumping :
            c=lavasound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.5)
            lavasound.stop()
            damagesound.play()
            player.health=0
        if self.pos == player.pos and player.jumping :
            c=lavasound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.5)
            lavasound.stop()
        execfuncs("lavaupdate",modfunctions)
class Rock() :
    def __init__(self,pos) :
        self.pos=pos
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=rocksound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            rocksound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=rocksound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            rocksound.stop()
        if self.pos == player.pos and not player.jumping :
            c=rocksound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            rocksound.stop()
            player.pos-=1
        if self.pos == player.pos and player.jumping :
            c=rocksound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            rocksound.stop()
        execfuncs("rockupdate",modfunctions)
class Wall() :
    def __init__(self,pos) :
        self.pos=pos
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=wallsound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            wallsound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=wallsound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            wallsound.stop()
        if self.pos == player.pos and not player.ducking :
            c=wallsound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            wallsound.stop()
            player.pos-=1
        if self.pos == player.pos and player.ducking :
            c=wallsound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            wallsound.stop()
        execfuncs("wallupdate",modfunctions)
class Powerup() :
    def __init__(self,pos,amount) :
        self.pos=pos
        self.amount=amount
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=powerupsound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            powerupsound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=powerupsound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            powerupsound.stop()
        if self.pos == player.pos and not player.jumping :
            boostsound.play()
            player.health+=self.amount
            powerups.remove(self)
        if self.pos == player.pos and player.jumping :
            c=powerupsound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            powerupsound.stop()
        execfuncs("powerupupdate",modfunctions)
class Teleporter() :
    def __init__(self,pos,tpos) :
        self.pos=pos
        self.tpos=tpos
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=teleportersound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            teleportersound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=teleportersound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            teleportersound.stop()
        if self.pos == player.pos and not player.jumping :
            teleportationsound.play()
            player.pos=self.tpos
        if self.pos == player.pos and player.jumping :
            c=teleportersound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            teleportersound.stop()
        execfuncs("teleporterupdate",modfunctions)
class Monster() :
    def __init__(self,pos,health,damage,sound) :
        self.pos=pos
        self.health=health
        self.damage=damage
        self.sound=pygame.mixer.Sound("sounds/{}".format(sound))
    def attack(self) :
        damagesound.play()
        player.health-=self.damage
    def update(self) :
        if self.pos in range(player.pos+1,player.pos+11) :
            c=self.sound.play()
            c.set_volume(0.0,calcrightvolume(player.pos,self.pos))
            time.sleep(.1)
            self.sound.stop()
        if self.pos in range(player.pos-10,player.pos) :
            c=self.sound.play()
            c.set_volume(calcleftvolume(player.pos,self.pos),0.0)
            time.sleep(.1)
            self.sound.stop()
        if self.pos == player.pos :
            c=self.sound.play()
            c.set_volume(1.0,1.0)
            time.sleep(.1)
            self.sound.stop()
        if self.pos == player.pos and player.monstertimer >= 2 :
            self.attack()
            player.monstertimer=0
        if self.pos == player.pos :
            player.fighting=True
        if self.health <= 0 :
            monsters.remove(self)
            player.fighting=False
        execfuncs("monsterupdate",modfunctions)
def reset() :
    global player
    global spikes
    global bombs
    global electricbarriers
    global lasers
    global lavablocks
    global rocks
    global walls
    global powerups
    global teleporters
    global monsters
    player=Player()
    spikes=[]
    bombs=[]
    electricbarriers=[]
    lasers=[]
    lavablocks=[]
    rocks=[]
    walls=[]
    teleporters=[]
    powerups=[]
    monsters=[]
def calcrightvolume(playerpos,objpos) :
    voldict={10:1,9:2,8:3,7:4,6:5,5:6,4:7,3:8,2:9,1:10}
    num=objpos-playerpos
    return voldict[num]/10
def calcleftvolume(playerpos,objpos) :
    voldict={1:10,2:9,3:8,4:7,5:6,6:5,7:4,8:3,9:2,10:1}
    num=playerpos-objpos
    return voldict[num]/10
def testspeakers() :
    pygame.mixer.music.pause()
    c=spikesound.play()
    c.set_volume(1.0,0.0)
    time.sleep(.5)
    spikesound.stop()
    say("left")
    time.sleep(.5)
    c=spikesound.play()
    c.set_volume(1.0,1.0)
    time.sleep(.5)
    spikesound.stop()
    say("centre")
    time.sleep(.5)
    c=spikesound.play()
    c.set_volume(0.0,1.0)
    time.sleep(.5)
    spikesound.stop()
    say("right")
    pygame.mixer.music.play()
def findmonster() :
    for monster in monsters :
        if monster.pos == player.pos :
            return monster
    return None
def loadlevel(levelfile) :
    global maxpos
    f=open(str(levelfile),"r+")
    data=f.read()
    f.close()
    for line in data.split("\n") :
        if line.split(":")[0] == "music" :
            pygame.mixer.music.load("sounds/{}".format(line.split(":")[1]))
            pygame.mixer.music.play(-1)
        if line.split(":")[0] == "maxpos" :
            maxpos=int(line.split(":")[1])
        if line.split(":")[0] == "startpos" :
            player.pos=int(line.split(":")[1])
        if line.split(":")[0] == "spike" :
            spikes.append(Spike(int(line.split(":")[1])))
        if line.split(":")[0] == "bomb" :
            bombs.append(Bomb(int(line.split(":")[1])))
        if line.split(":")[0] == "electricbarrier" :
            electricbarriers.append(Electricbarrier(int(line.split(":")[1])))
        if line.split(":")[0] == "laser" :
            lasers.append(Laser(int(line.split(":")[1])))
        if line.split(":")[0] == "lava" :
            lavablocks.append(Lava(int(line.split(":")[1])))
        if line.split(":")[0] == "rock" :
            rocks.append(Rock(int(line.split(":")[1])))
        if line.split(":")[0] == "wall" :
            walls.append(Wall(int(line.split(":")[1])))
        if line.split(":")[0] == "teleporter" :
            teleporters.append(Teleporter(int(line.split(":")[1].split("|")[0]),int(line.split(":")[1].split("|")[1])))
        if line.split(":")[0] == "powerup" :
            powerups.append(Powerup(int(line.split(":")[1].split("|")[0]),int(line.split(":")[1].split("|")[1])))
        if line.split(":")[0] =="monster" :
            monsters.append(Monster(int(line.split(":")[1].split("|")[0]),int(line.split(":")[1].split("|")[1]),int(line.split(":")[1].split("|")[2]),line.split(":")[1].split("|")[3]))
        for key in moddict.keys() :
            if line.split(":")[0] == key :
                cstring="modobjects.append({}(".format(moddict[key][0])
                for arg in range(moddict[key][1].args) :
                    cstring=cstring+"{},".format(line.split(":")[1].split("|")[arg])
                cstring=cstring[0:len(cstring)-1]
                cstring=cstring+"))"
                codetoexecute.append(cstring)
def playsound(sound,dir,delay,playerpos,objpos) :
    c=sound.play()
    if dir == "left" :
        c.set_volume(calcleftvolume(playerpos,objpos),0.0)
    elif dir == "center" :
        c.set_volume(1.0,1.0)
    elif dir == "right" :
        c.set_volume(0.0,calcrightvolume(playerpos,objpos))
    time.sleep(delay)
    sound.stop()
def loadsound(sound) :
    return pygame.mixer.Sound("sounds/{}".format(sound))
def inrange(playerpos,objpos,dir) :
    if dir == "right" :
        if objpos in range(playerpos+1,playerpos+11) :
            return True
    elif dir == "left" :
        if objpos in range(playerpos-10,playerpos) :
            return True
    return False
class Levelitem() :
    def __init__(self,levelfile,name) :
        self.file=levelfile
        self.name=name
        self.scenetoswitchto=Game()
    def onclick(self) :
        pygame.mixer.music.stop()
        loadlevel(self.file)
        execfuncs("loadlevelonclick",modfunctions)
class Quititem() :
    def __init__(self,name) :
        self.name=name
        self.scenetoswitchto=None
    def onclick(self) :
        execfuncs("quitonclick",modfunctions)
        time.sleep(.5)
        pygame.quit()
        sys.exit()
class Testspeakersitem() :
    def __init__(self,name) :
        self.name=name
        self.scenetoswitchto=None
    def onclick(self) :
        testspeakers()
        execfuncs("testspeakersonclick",modfunctions)
class Mainmenu() :
    def __init__(self) :
        say("main menu")
        pygame.mixer.music.load("sounds/menu.wav")
        pygame.mixer.music.play(-1)
        self.pos=1
        self.menuitems=[]
        self.next=self
        self.menuitems.append(Quititem("quit"))
        self.menuitems.append(Testspeakersitem("test speakers"))
        for file in glob.glob("levels/*.lvl") :
            self.menuitems.append(Levelitem(file,file.split("/")[1].split(".")[0]))
        say(self.menuitems[self.pos-1].name)
    def switchscene(self,scene) :
        if scene != None :
            self.next=scene
    def handle_events(self) :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_DOWN and self.pos < len(self.menuitems) :
                self.pos+=1
                scrollsound.play()
                say(self.menuitems[self.pos-1].name)
            if event.key == pygame.K_UP and self.pos > 1 :
                scrollsound.play()
                self.pos-=1
                say(self.menuitems[self.pos-1].name)
            if event.key == pygame.K_RETURN :
                clicksound.play()
                self.menuitems[self.pos-1].onclick()
                self.switchscene(self.menuitems[self.pos-1].scenetoswitchto)
        execfuncs("menuevents",modfunctions)
    def update(self) :
        execfuncs("menuupdate",modfunctions)
class Game() :
    def __init__(self) :
        self.next=self
        self.monstertimer=0
    def switchscene(self,scene) :
        self.next=scene
    def handle_events(self) :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_b :
                reset()
                self.switchscene(Mainmenu())
            if event.key == pygame.K_h :
                say(player.health)
            if event.key == pygame.K_RIGHT and player.pos < maxpos :
                if not player.jumping :
                    walksound.play()
                player.pos+=1
            if event.key == pygame.K_LEFT and player.pos > 1:
                if not player.jumping :
                    walksound.play()
                player.pos-=1
            if event.key == pygame.K_UP :
                jumpsound.play()
                player.jumping=True
                player.jumptimer=player.maxtimer
            if event.key == pygame.K_DOWN :
                player.ducking=True
                duckingsound.play()
            if event.key == pygame.K_SPACE :
                foundmonster=findmonster()
                if foundmonster != None :
                    player.attack(foundmonster)
                    player.monstertimer=0
            if event.key == pygame.K_c :
                say(player.pos)
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN :
            player.ducking=False
        execfuncs("gameevents",modfunctions)
    def update(self) :
        if player.fighting :
            player.monstertimer+=1
        player.update()
        for spike in spikes :
            spike.update()
        for bomb in bombs :
            bomb.update()
        for electricbarrier in electricbarriers :
            electricbarrier.update()
        for laser in lasers :
            laser.update()
        for lavablock in lavablocks :
            lavablock.update()
        for rock in rocks :
            rock.update()
        for wall in walls :
            wall.update()
        for teleporter in teleporters :
            teleporter.update()
        for powerup in powerups :
            powerup.update()
        for monster in monsters :
            monster.update()
        for modobject in modobjects :
            modobject.update()
        execfuncs("gameupdate",modfunctions)
clock=pygame.time.Clock()
currentscene=Mainmenu()
for modfile in glob.glob("mods/*.mod") :
    f=open(modfile,"r+")
    code=f.read()
    f.close()
    codeobject=compile(code,"modfile","exec")
    exec(codeobject)
while True :
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q :
            pygame.quit()
            sys.exit()
        currentscene.handle_events()
    currentscene.update()
    for code in codetoexecute :
        exec(code)
        codetoexecute.remove(code)
    screen.fill((0,0,0))
    currentscene=currentscene.next
    pygame.display.update()
    clock.tick(60)