class testobject() :
    args=1
    def __init__(self,pos) :
        self.pos=int(pos)
    def update(self) :
        if inrange(player.pos,self.pos,"right") :
            playsound(jumpsound,"right",.5,player.pos,self.pos) 
        if inrange(player.pos,self.pos,"left") :
            playsound(jumpsound,"left",.5,player.pos,self.pos)
        if self.pos == player.pos :
            playsound(jumpsound,"center",.5,player.pos,self.pos)
moddict["ghost"]=["testobject",testobject]
def hi() :
    if event.type == pygame.KEYDOWN and event.key == pygame.K_h :
        os.system("say \"hi\"")
addfunction("menuevents",hi)