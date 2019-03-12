import pygame
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

#pozicija i opis objekta kao i brzina kretanja
class player(object):
    def __init__(self,x,y,sirObjekta,visObjekta):
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
    def draw(self,prozor):
        
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
                
def osveziSliku():
    #nakon kretnje objekta da se pozadina apdejta
    # kad stavimo global to znaci da koristimo
    #vec postojecu promenljivu sa ovim imenom, deklarisanu van funkcije
    #i ne zelimo neku novu unutar funkcije sa istim tim imenom
    #nas objekat,trenutni objekat pre implementacije sprite
    #prozor.fill((0,0,0))
    #pygame.draw.rect(prozor, (255,0,0), (x,y,sirObjekta,visObjekta))
    #pygame.display.update()
    prozor.blit(pozadina,(0,0))
    igrac.draw(prozor)
    pygame.display.update()

igrac = player(300,visinaProzora-108,42,78)
#GLAVNA UPDATE FUNKCIJA
run=True
while run:
    #milisekunde, FPS, koliko cesto se slika apdejta
    pygame.time.delay(27) #3*3

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
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
    if not(igrac.isSkok):
    #    pomeranje gore dole
    #    if keys[pygame.K_DOWN]:
    #        if y<(visinaProzora-visObjekta):
    #            y+=Brzina
    #    if keys[pygame.K_UP]:
    #        if y>0:
    #            y-=Brzina
        if keys[pygame.K_SPACE]:
            igrac.isSkok = True
            igrac.levoOkrenut=False
            igrac.desnoOkrenut=False
            igrac.hodanjeBrojac=0
    else:
        #igrac.skokBrojac=igrac.brzina
        if igrac.skokBrojac >= (igrac.intenzitetSkoka*(-1)):
            neg =1
            if igrac.skokBrojac< 0:
                neg=-1
            igrac.y-=(igrac.skokBrojac ** 2)*0.5 *neg
            igrac.skokBrojac -= 1
        else:
            igrac.isSkok=False
            igrac.skokBrojac=igrac.intenzitetSkoka
    osveziSliku()
pygame.quit()

