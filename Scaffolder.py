import pygame
import random
pygame.init()


visinaProzora=600;
sirinaProzora=500;

prozor= pygame.display.set_mode((sirinaProzora,visinaProzora))
pygame.display.set_caption("Scaffolder")


#animacija, treba popraviti, ovo je samo trenutno
hodajDesno=[pygame.image.load('w1.png'),pygame.image.load('w2.png'),pygame.image.load('w3.png'),pygame.image.load('w4.png'),pygame.image.load('w5.png'),pygame.image.load('w6.png'),pygame.image.load('w7.png'),pygame.image.load('w8.png')]
hodajLevo=[pygame.transform.flip(pygame.image.load('w1.png'),True,False),pygame.transform.flip(pygame.image.load('w2.png'),True,False),pygame.transform.flip(pygame.image.load('w3.png'),True,False),pygame.transform.flip(pygame.image.load('w4.png'),True,False),pygame.transform.flip(pygame.image.load('w5.png'),True,False),pygame.transform.flip(pygame.image.load('w6.png'),True,False),pygame.transform.flip(pygame.image.load('w7.png'),True,False),pygame.transform.flip(pygame.image.load('w8.png'),True,False)]
slikaIgraca=pygame.image.load('w1.png')
skok=[pygame.image.load('j1.png'),pygame.image.load('j2.png'),pygame.image.load('j3.png'),pygame.image.load('j4.png'),pygame.image.load('j5.png'),pygame.image.load('j6.png'),pygame.image.load('j7.png')]
pozadina=pygame.image.load('pozadina.jpg')
clock=pygame.time.Clock()
platformaSlika=pygame.image.load('platformaSlika.png')


#SCORE-------------
def score(skor):
    font = pygame.font.SysFont(None , 25)
    text = font.render("Skor: "+str(skor),True , (0,0,0))
    prozor.blit(text , (0,0))

############## START EKRAN ##################
def text_objects(poruka, boja,vel_font=25):
    font = pygame.font.SysFont(None , vel_font)
    textSurface = font.render(poruka, True, boja)
    return textSurface, textSurface.get_rect()
def ispisi_poruku(poruka , boja , y_pomeraj = 0, vel_font=25):
    #font = pygame.font.SysFont(None , vel_font)
    TextSurf, TextRect = text_objects(poruka, boja,vel_font)
    TextRect.center = (255,500/2 + y_pomeraj) 
    prozor.blit(TextSurf, TextRect)


#Pauza---------------------------------
def pauza():
    pauza_promenljiva = True

    while pauza_promenljiva:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pauza_promenljiva = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        ispisi_poruku("Pauza", (255,255,255) , -120, 75)
        ispisi_poruku("\"p\" - nastavak  \"q\" - izlaz iz igre" ,(255,255,255) , 0)
        pygame.display.update()
        clock.tick(5)


def start_igre():
    
    intro = True
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro = False
                    
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #prozor.fill((255,255,255))
        pozadina=pygame.image.load('start.jpg')
        prozor.blit(pozadina,(0,0))
        ispisi_poruku("Welcome to Scaffolder" , (0,155,0),-100,65)
        ispisi_poruku("Game by: " , (255,255,255),-70,25)
        ispisi_poruku("Alen||Bogosav||Danilo" , (255,255,255),-50,25)
        ispisi_poruku("Klikni \"s\" za start ili \"q\" za quit!"  , (255,255,255),100,25)
        ispisi_poruku("(u toku igre \"p\" za pauzu)"  , (255,255,255),120,25)
        
        pygame.display.update()
        #pygame.time.Clock().tick(15)

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
    score(skor)
    pygame.display.update()




munja = 5
indikator = False
skor = 0
run=True
GameOver = False
brojac=0
#GLAVNA UPDATE FUNKCIJA
while run:
    if brojac==0:
        brojac+=1
        start_igre()
        zemlja = platforma(0,visinaProzora-37,sirinaProzora)
        igrac  = player(150,visinaProzora-108,42,78,zemlja)
        igrac.y = 492
        brojacZaPadanje=0
        platforme = []
        platforme.append(zemlja)
    #milisekunde, FPS, koliko cesto se slika apdejta
    #for plat in platforme:
    #    if plat.collide(igrac.hitbox):
    #        igrac.y=plat.y+igrac.visObjekta
    pygame.time.delay(27) #3*3 

    #GameOver ekran--------------------------------------   
    while GameOver == True:
        pomocna_pozadina=pygame.image.load('start.jpg')
        prozor.blit(pomocna_pozadina,(0,0))
        #prozor.fill((0,0,0))
        ispisi_poruku("GameOver" , (255,25,25),0,50)
        ispisi_poruku("Vas skor je: " + str(skor) , (255,255,255), 25)
        ispisi_poruku("Ako hoces opet klikni \"s\", ako pak neces klikni \"q\"!" , (255,255,255), 100)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    skor = 0
                    GameOver = False
                    run = True
                    zemlja = platforma(0,visinaProzora-37,sirinaProzora)
                    igrac  = player(150,visinaProzora-108,42,78,zemlja)
                    brojacZaPadanje=0
                    platforme = []
                    platforme.append(zemlja)
                    
                if event.key == pygame.K_q:
                    GameOver = False
                    run = False
    if igrac.y >530:
        GameOver = True
        indikator = False


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pauza()

    #GENERACIJA PLATFORMI
    if len(platforme) < 500:
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
    else:
        del platforme[250:500]

    

    #KRETNJA I GRANICA KRETNJE
    if keys[pygame.K_LEFT] and igrac.x>0:
        igrac.x-=igrac.brzina
        igrac.levoOkrenut=True
        igrac.desnoOkrenut=False
        slikaIgraca=pygame.transform.flip(pygame.image.load('w1.png'),True,False)
        #if igrac.brzina < 20:
        #    igrac.brzina+=1
    elif keys[pygame.K_RIGHT] and igrac.x<(sirinaProzora-igrac.sirObjekta):
        igrac.x+=igrac.brzina
        igrac.levoOkrenut=False
        igrac.desnoOkrenut=True
        slikaIgraca=pygame.image.load('w1.png')
        #if igrac.brzina < 20:
        #    igrac.brzina+=1
    else:
        igrac.levoOkrenut=False
        igrac.desnoOkrenut=False
        igrac.hodanjeBrojac=0
        #igrac.brzina=5

    #SKAKANJE I PADANJE
    if not(igrac.isStoji): #KAD NE STOJI
        for plat in platforme:
            if igrac.y+72>plat.y and igrac.y+72< plat.y+8 and igrac.x + igrac.sirObjekta-5>=plat.x+2 and igrac.x<= plat.x+plat.sirObjekta:
                igrac.y=plat.y-igrac.visObjekta+11
                igrac.isStoji=True
                igrac.platformaa=plat
                brojacZaPadanje=0
                if plat != platforme[0]:
                    skor = skor + 1
                break
    else: #KAD STOJI
        if igrac.x + igrac.sirObjekta-10<igrac.platformaa.x+2 or igrac.x+15> igrac.platformaa.x+igrac.platformaa.sirObjekta:
            igrac.isStoji=False
    if not(igrac.isSkok): 
        if not(igrac.isStoji): #KAD PADA
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

    if igrac.y <=256:
        indikator = True
    if indikator == True:
        for p in platforme:
            p.y += munja
        igrac.y += munja
    osveziSliku()
pygame.quit()

