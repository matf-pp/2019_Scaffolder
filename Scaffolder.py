import pygame
import random
pygame.init()


visinaProzora=600;
sirinaProzora=500;

prozor= pygame.display.set_mode((sirinaProzora,visinaProzora))

pygame.display.set_caption("Scaffolder")

#animacija, treba popraviti, ovo je samo trenutno
hodajDesno=[pygame.image.load('1.jpg'),pygame.image.load('2.jpg'),pygame.image.load('3.jpg')]
hodajLevo=[pygame.transform.flip(pygame.image.load('1.jpg'),True,False),pygame.transform.flip(pygame.image.load('2.jpg'),True,False),pygame.transform.flip(pygame.image.load('3.jpg'),True,False)]
slikaIgraca=pygame.image.load('5.jpg')
pozadina=pygame.image.load('pozadina.jpg')
clock=pygame.time.Clock()
platformaSlika=pygame.image.load('platformaSlika.png')

#pozicija i opis objekta kao i brzina kretanja
class player(object):
    def __init__(self,x,y,sirObjekta,visObjekta,platformaa):
        self.x=x
        self.y=y
        self.sirObjekta=sirObjekta
        self.visObjekta=visObjekta
        self.brzina=5
        self.isSkok=False
        self.intenzitetSkoka=9
        self.skokBrojac= self.intenzitetSkoka
        self.levoOkrenut=False
        self.desnoOkrenut=False
        self.hodanjeBrojac=0 #sluzi ako nasa animacija hodanja ima vise slika-faza hodanja
        self.isStoji = True
        self.platformaa=platformaa


    def draw(self,prozor):
        self.hitbox=(self.x+4,self.y,self.sirObjekta-24,self.visObjekta-10)#AAA
        if self.hodanjeBrojac + 1 >=9:
        #(3*3)zelimo da nasa slika traje 3 frejma i imamo 3 razlicite slike hodanja
            self.hodanjeBrojac=0
        if self.levoOkrenut:
            prozor.blit(hodajLevo[self.hodanjeBrojac//3],(self.x,self.y))
            self.hodanjeBrojac+=1
        elif self.desnoOkrenut:
            prozor.blit(hodajDesno[self.hodanjeBrojac//3],(self.x,self.y))
            self.hodanjeBrojac+=1
        else:
            prozor.blit(slikaIgraca,(self.x,self.y))
        self.hitbox=(self.x+4,self.y+8,self.sirObjekta-13,self.visObjekta-13)#AAA
        pygame.draw.rect(prozor,(255,0,0),self.hitbox,2)

class platforma(object):
    #INICIJALIZACIJA SLIKE AKO JE U FOLDERU "slike"
    def __init__(self,x,y,sirObjekta):
        self.x=x
        self.y=y
        self.sirObjekta=sirObjekta
        self.visObjekta=20

    def draw(self, prozor):
        prozor.blit(pygame.transform.scale(platformaSlika,(self.sirObjekta,50)),(self.x,self.y))
        self.hitbox=(self.x+10,self.y+6,self.sirObjekta-20,30)
        pygame.draw.rect(prozor,(255,0,0),self.hitbox,2)
    def collide(self,rect):
        if rect[0]+rect[2]>self.hitbox and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1]+rect[3]> self.hitbox[1]:
                return True
            return False
            

    
def osveziSliku():
    # kad stavimo global to znaci da koristimo
    #vec postojecu promenljivu sa ovim imenom, deklarisanu van funkcije
    prozor.blit(pozadina,(0,0))
    zemlja.draw(prozor)
    
    for x in platforme:
        x.draw(prozor)
    igrac.draw(prozor)
    pygame.display.update()


zemlja = platforma(0,visinaProzora-37,sirinaProzora)
igrac  = player(150,visinaProzora-108,42,78,zemlja)

    
brojacZaPadanje=0
platforme = []
platforme.append(zemlja)
#GLAVNA UPDATE FUNKCIJA
run=True
while run:
    #milisekunde, FPS, koliko cesto se slika apdejta
    #for plat in platforme:
    #    if plat.collide(igrac.hitbox):
    #        igrac.y=plat.y+igrac.visObjekta

    pygame.time.delay(27) #3*3
    
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    #GENERACIJA PLATFORMI
    if len(platforme) <20:
        if len(platforme) == 1:
            platformaA = platforma(random.randint(20,sirinaProzora-170),zemlja.y-100, 200)
            platforme.append(platformaA)
        else:
            platformaB = platforme.pop()
            pomocnaProm=random.random()
            if pomocnaProm <0.5:
                platformaA = platforma(random.randint(platformaB.x-100,platformaB.x),platformaB.y-100, 200-random.randint(1,50))
            else:
                platformaA = platforma(random.randint(platformaB.x,platformaB.x+100),platformaB.y-100, 200-random.randint(1,50))                
            platforme.append(platformaB)
            platforme.append(platformaA)



    keys=pygame.key.get_pressed()
    #kretnja i granica kretnje
    if keys[pygame.K_LEFT] and igrac.x>0:
        igrac.x-=igrac.brzina
        igrac.levoOkrenut=True
        igrac.desnoOkrenut=False
        if igrac.brzina < 20:
            igrac.brzina+=1
    elif keys[pygame.K_RIGHT] and igrac.x<(sirinaProzora-igrac.sirObjekta):
        igrac.x+=igrac.brzina
        igrac.levoOkrenut=False
        igrac.desnoOkrenut=True
        if igrac.brzina < 20:
            igrac.brzina+=1
    else:
        igrac.levoOkrenut=False
        igrac.desnoOkrenut=False
        igrac.hodanjeBrojac=0
        igrac.brzina=5
    #Skakanje
    if not(igrac.isStoji):
        for plat in platforme:
            if igrac.y+72>plat.y and igrac.y+72< plat.y+8 and igrac.x + igrac.sirObjekta-5>=plat.x+2 and igrac.x<= plat.x+plat.sirObjekta:
                igrac.y=plat.y-igrac.visObjekta+7
                igrac.isStoji=True
                igrac.platformaa=plat
                brojacZaPadanje=0
                break
    else:
        if igrac.x + igrac.sirObjekta-5<igrac.platformaa.x+2 or igrac.x> igrac.platformaa.x+igrac.platformaa.sirObjekta:
            igrac.isStoji=False
            
    
    if not(igrac.isSkok):
        if not(igrac.isStoji):
            #if brojacZaPadanje<15:
            #    brojacZaPadanje+=1
            #igrac.y+=brojacZaPadanje*1.5
            igrac.y+=7
        if keys[pygame.K_SPACE] and igrac.isStoji:
            igrac.isSkok = True
            igrac.levoOkrenut=False
            igrac.desnoOkrenut=False
            igrac.hodanjeBrojac=0
            brojacZaPadanje=0
    else:
        #igrac.skokBrojac=igrac.brzina
        if igrac.skokBrojac >= 0:
            
            igrac.y-=(igrac.skokBrojac ** 2)*0.5
            igrac.skokBrojac -= 1
        else:
            igrac.isSkok=False
            igrac.isStoji=False
            igrac.skokBrojac=igrac.intenzitetSkoka
    osveziSliku()
pygame.quit()

