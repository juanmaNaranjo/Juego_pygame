import pygame
import random

AZUL = [0,255,243]
VERDE = [0,255,0]
AMARILLO=[251,255,0]
BLANCO = [255, 255, 255]
NEGRO = [0,0,0]
ROJO=[232,60,84]
ROSADO=[255,0,247]
NARANJA=[255,87,51]
ANCHO = 800
ALTO = 600

def recortar(i_ancho,i_alto,m):
    info=m.get_rect()
    f_ancho=info[2]
    f_alto=info[3]
    mls=list()
    ls=list()
    filas=i_alto
    col=i_ancho
    corte_ancho=int(f_ancho/col)
    corte_alto=int(f_alto/filas)
    for i in range(filas):
        ls=[]
        for j in range(col):
            cuadrado =m.subsurface((corte_ancho*j),(corte_alto*i),corte_ancho,corte_alto)
            ls.append(cuadrado)
        mls.append(ls)

    return mls

class Jugador(pygame.sprite.Sprite):

    def __init__(self, m ,lim_p, lim_anim=[0,6], desp=0):

        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.anm_ini=lim_anim[0]
        self.anm_fin=lim_anim[1]

        self.col=self.anm_ini
        self.dir=0+desp

        self.image = self.m[self.dir][self.col]
        self.rect=self.image.get_rect()

        self.rect.x = 200
        self.rect.y = 200
        self.velx = 0
        self.vely = 0
        self.lim_px = lim_p[0]
        self.lim_py = lim_p[1]
        self.salud=100
        self.potencia = 10
        self.bloques = pygame.sprite.Group()


    def update(self):
        if self.velx != self.vely:
            self.image = self.m[self.dir][self.col]

            if self.col < self.anm_fin:
                self.col+=1
            else:
                self.col=self.anm_ini

        self.rect.x += self.velx

        col = pygame.sprite.spritecollide(self,self.bloques, False)
        for b in col:
           if self.velx > 0:
                if self.rect.right > b.rect.left:
                    self.rect.right = b.rect.left
           else:
                if self.rect.left < b.rect.right:
                    self.rect.left = b.rect.right
           self.velx = 0

        if self.rect.x < 0:
            self.rect.right = ANCHO

        if self.rect.x > ANCHO:
            self.rect.x = 0

        self.rect.y += self.vely

        col = pygame.sprite.spritecollide(self, self.bloques, False)
        for b in col:
            if self.vely > 0:
                if self.rect.bottom > b.rect.top:
                    self.rect.bottom = b.rect.top

            else:
                if self.rect.top < b.rect.bottom:
                    self.rect.top = b.rect.bottom
            self.vely = 0

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.y > ALTO-self.rect.height:
            self.rect.y = ALTO-self.rect.height

        if self.rect.x > self.lim_px - self.rect.width:
            self.rect.x = self.lim_px - self.rect.width

        '''if self.rect.x < self.rect.width -self.lim_px:
            self.rect.x = self.rect.width -self.lim_px


        if self.rect.y <  self.rect.height-self.lim_py :
            self.rect.y = self.rect.height-self.lim_py

        if self.rect.y > self.lim_py -self.rect.height :
            self.rect.y = self.lim_py -self.rect.height'''

class Jefe(pygame.sprite.Sprite):
    def __init__(self,pos, m ,lim_p, lim_anim=[0,3]):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.anm_ini=lim_anim[0]
        self.anm_fin=lim_anim[1]

        self.col=self.anm_ini
        self.dir=1+desp

        self.image = self.m[self.dir][self.col]
        self.rect=self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 8
        self.vely = 8
        self.temp = 100
        self.lim_px = lim_p[0]
        self.lim_py = lim_p[1]
        self.salud=200


    def update(self):
        if self.velx != self.vely:
            self.image = self.m[self.dir][self.col]

            if self.col < self.anm_fin:
                self.col+=1
            else:
                self.col=self.anm_ini

        if self.velx > 0:
            self.dir=2+desp
        else :
            self.dir=1+desp

        self.rect.x += self.velx

        if self.rect.x > (self.lim_px -500) - self.rect.width:
            self.velx = -5

        if self.rect.x < self.rect.width - (self.lim_px-500):
            self.velx = 5

        self.rect.y += self.vely

        if self.rect.y > self.rect.height - (self.lim_py ):
            self.vely = 5

        if self.rect.y < self.lim_py  - self.rect.height:
            self.vely = -5

        if self.rect.x < (self.lim_px-1300)- self.rect.width :
            self.velx = 5



class Bloque(pygame.sprite.Sprite):
    def __init__(self, pos, img_bloque):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_bloque
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.vely=0


    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

class Generador(pygame.sprite.Sprite):

    def __init__(self,img,pos, cl=BLANCO):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.temp = random.randrange(30)
        self.crear=False
        self.limite= 3
        self.velx = 0
        self.vely = 0

    def RetPos(self):
        px=self.rect.left -5
        py=self.rect.top +10
        return ([px,py])

    def update(self):
        self.rect.y += self.vely
        if self.rect.y < 100:
            self.vely = 5
        if self.rect.y > 600:
            self.vely = -5
        self.temp -= 1
        if self.temp <= 0:
            self.crear = True

        self.rect.x += self.velx
        '''if self.rect.x < 100:
            self.velx = 5
        if self.rect.x > 600:
            self.velx = -5'''


class Goma(pygame.sprite.Sprite):

    def __init__(self, pos,m,lim_p,lim_anim=[0,3], cl=AZUL):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.anm_ini=lim_anim[0]
        self.anm_fin=lim_anim[1]

        self.col=self.anm_ini
        self.dir=1+desp

        self.image = self.m[self.dir][self.col]
        self.rect=self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = 8
        self.velx = 8
        self.temp = 100
        self.lim_px=lim_p[0]
        self.lim_py = lim_p[1]

    def update(self):

        if self.velx != self.vely:
            self.image = self.m[self.dir][self.col]

            if self.col < self.anm_fin:
                self.col+=1
            else:
                self.col=self.anm_ini
        if self.velx > 0:
            self.dir=2+desp
        else :
            self.dir=1+desp



        self.rect.x += self.velx

        if self.rect.x > self.lim_px - self.rect.width:
            self.velx = -5

        if self.rect.x < self.rect.width -self.lim_px:
            self.velx = 5

        self.rect.y += self.vely

        if self.rect.y >  self.rect.height-self.lim_py :
            self.vely = 5

        if self.rect.y < self.lim_py -self.rect.height  :
            self.vely = -5

class Modificador(pygame.sprite.Sprite):

    def __init__(self, pos, img_bloque,cl=AMARILLO):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_bloque
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vely = 0
        self.velx = 0

    def update(self):
        self.rect.y += self.vely
        if self.rect.bottom > (ALTO-10):
            self.rect.bottom = ALTO-10
        self.rect.x += self.velx
        if self.rect.top > (ALTO - 10):
            self.rect.top = ALTO - 10


if __name__ == "__main__":
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    #fondo pantalla
    fuente = pygame.font.Font(None, 32)
    fondo = pygame.image.load("fondo.png")
    info=fondo.get_rect()
    print("propiedades imagen: ", info)
    f_ancho=info[2]
    f_alto=info[3]
    f_x=0
    f_y=0
    f_x1 = 0
    f_y1 = 0
    f_vx=-8
    f_vy=-8
    f_limx = ANCHO - f_ancho
    f_limy = ALTO - f_alto
    f_limx1 = f_ancho - ANCHO
    f_limy1 =  f_alto - ALTO

    lim_d = 750
    lim_i = 500
    lim_s = 50
    lim_z = 50


    #jugagores
    jugadores=pygame.sprite.Group()
    jefes = pygame.sprite.Group()
    bloques = pygame.sprite.Group()
    balas = pygame.sprite.Group()
    gomas = pygame.sprite.Group()
    gomas1 = pygame.sprite.Group()
    generadores = pygame.sprite.Group()
    generadores1 = pygame.sprite.Group()
    modifs = pygame.sprite.Group()
    modifs1 = pygame.sprite.Group()
    modifs2 = pygame.sprite.Group()

    sp_ancho1 = 6
    sp_alto1 = 4
    #imagen1 = pygame.image.load('arboles2.png')
    #objetos colisionables
    imagen = pygame.image.load('casa.png')
    b = Bloque([130,350],imagen)
    bloques.add(b)

    b = Bloque([1160, 1200], imagen)
    bloques.add(b)

    b = Bloque([2100, 1200], imagen)
    bloques.add(b)

    b = Bloque([1800, 150], imagen)
    bloques.add(b)


    imagen1 = pygame.image.load('casa1.png')
    b = Bloque([500, 350], imagen1)
    bloques.add(b)

    b = Bloque([1160, 900], imagen1)
    bloques.add(b)

    b = Bloque([600, 1250], imagen1)
    bloques.add(b)

    b = Bloque([1160, 300], imagen1)
    bloques.add(b)

    imagen2 = pygame.image.load('casa2.png')
    b = Bloque([900, 330], imagen2)
    bloques.add(b)

    b = Bloque([2100, 750], imagen2)
    bloques.add(b)

    b = Bloque([130, 1200], imagen2)
    bloques.add(b)

    b = Bloque([1600, 1200], imagen2)
    bloques.add(b)

    b = Bloque([450, 100], imagen2)
    bloques.add(b)



    imagen3 = pygame.image.load('casa3.png')
    b = Bloque([1500, 350], imagen3)
    bloques.add(b)

    b = Bloque([130, 750], imagen3)
    bloques.add(b)

    b = Bloque([900, 750], imagen3)
    bloques.add(b)

    imagen4 = pygame.image.load('casa4.png')
    b = Bloque([1600, 750], imagen4)
    bloques.add(b)

    b = Bloque([500, 750], imagen4)
    bloques.add(b)

    b = Bloque([2100, 350], imagen4)
    bloques.add(b)



    sp_ancho=7
    sp_alto=8
    origen=pygame.image.load('skeleto3.png')
    m = recortar(sp_ancho, sp_alto, origen)

    imagen2 = pygame.image.load('ryuk.png')
    ryuk = recortar(4,4, imagen2)
    limite = 20

    jefe = pygame.image.load('arbol.png')
    je = recortar(4, 4, jefe)


    desp = 0
    j=Jugador(m,[f_ancho,f_alto],[0,6], desp)

    j.bloques=bloques
    jugadores.add(j)

    gn=pygame.image.load('portal.png')

    g = Generador(gn,[30, 300])
    g.limite = limite
    generadores.add(g)

    g = Generador(gn,[30, 700])
    g.limite = limite
    generadores.add(g)

    g = Generador(gn,[30, 1100])
    g.limite = limite
    generadores.add(g)

    g = Generador(gn,[30, 1500])
    g.limite = limite
    generadores.add(g)

    J=1
    jef = Generador(gn,[-45, 1550])
    jef.J = J
    generadores1.add(jef)

    imagen = pygame.image.load('pera.png')
    imagen1 = pygame.image.load('zanahoria.png')
    imagen2 = pygame.image.load('mora.png')

    n=5
    for i in range(n):
        px = random.randrange(500-f_limx)
        py = random.randrange(500-f_limy)
        g = Modificador([px, py], imagen1)
        g.temp = 100
        modifs.add(g)

    n = 5
    for i in range(n):
        px = random.randrange(500 - f_limx)
        py = random.randrange(500 - f_limy)
        g = Modificador([px, py], imagen)
        g.temp = 100
        modifs1.add(g)

    n = 3
    for i in range(n):
        px = random.randrange(500 - f_limx)
        py = random.randrange(500 - f_limy)
        g = Modificador([px, py],imagen2)
        g.temp = 100
        modifs2.add(g)


    col=0
    con = 0
    print("Salud ", j.salud)
    print("Potencia ", j.potencia)
    reloj=pygame.time.Clock()

    fin_juego = False
    fin=False
    seguir = False

    #ciclo inicial
    while (not fin) and (not seguir):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    seguir = True
        fuente = pygame.font.Font(None, 50)
        ini = pygame.font.Font(None, 100)
        text = pygame.font.Font(None, 40)
        info = "INICIO"
        objetivo= "OBJETIVO:"
        tx="MATAR AL JEFE UBICADO EN LA PARTE INFERIOR"
        continuar = "precione espacio para continuar"
        texto = ini.render(info, False,ROSADO)
        obj= fuente.render(objetivo, False,NARANJA)
        t= text.render(tx, False,NEGRO)
        con = text.render(continuar, False,ROJO)
        # pantalla.fill(NEGRO)
        pantalla.blit(fondo, [0, 0])
        pantalla.blit(texto, [300, 100])
        pantalla.blit(obj, [300, 250])
        pantalla.blit(t, [80, 300])
        pantalla.blit(con, [200, 500])

        pygame.display.flip()


    while (not fin) and (not fin_juego):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    j.velx=5
                    j.vely=0
                    j.dir=6+desp
                if event.key == pygame.K_LEFT:
                    j.velx=-5
                    j.vely=0
                    j.dir=2+desp
                if event.key == pygame.K_UP:
                    j.velx=0
                    j.vely=-5
                    j.dir=4+desp
                if event.key == pygame.K_DOWN:
                    j.velx=0
                    j.vely=5
                    j.dir=0+desp
                if event.key == pygame.K_a:
                    # golpe izquierda
                    j.velx = 0.1
                    j.vely = 0
                    j.dir = 3
                    for g in gomas:
                        if g.rect.y < -10:
                            lsj_col = pygame.sprite.spritecollide(j, jefes, False)
                            for je in jefes:
                                je.salud -=j.potencia
                                print("salud jefe: "+aaje.salud)

                            ls_col = pygame.sprite.spritecollide(j, gomas, False)
                            if j.salud < 100:
                                j.salud += 20
                                gomas.remove(g)
                    pygame.sprite.spritecollide(j, gomas, True)

                if event.key == pygame.K_s:
                    # Golpe Abajo
                    j.velx = 0
                    j.vely = 0.1
                    j.dir = 1
                    for g in gomas:
                        if g.rect.y < -10:
                            ls_col = pygame.sprite.spritecollide(j, gomas, False)
                            if j.salud < 100:
                                j.salud += 20
                                gomas.remove(g)

                    pygame.sprite.spritecollide(j, gomas, True)

                if event.key == pygame.K_d:
                    # Golpe Derecha
                    j.velx = 0.1
                    j.vely = 0
                    j.dir = 7
                    for g in gomas:
                        if g.rect.y < -10:
                            ls_col = pygame.sprite.spritecollide(j, gomas, False)
                            if j.salud < 100:
                                j.salud += 20
                                gomas.remove(g)

                    pygame.sprite.spritecollide(j, gomas, True)

                if event.key == pygame.K_w:
                    # Golpe arriba
                    j.velx = 0
                    j.vely = 0.1
                    j.dir = 5
                    for g in gomas:
                        if g.rect.y < -10:
                            ls_col = pygame.sprite.spritecollide(j, gomas, False)
                            if j.salud < 100:
                                j.salud += 20
                                gomas.remove(g)

                    pygame.sprite.spritecollide(j, gomas, True)

            if event.type == pygame.KEYUP:
                j.velx=0
                j.vely=0

        if j.rect.right > lim_d:
            j.rect.right=lim_d
            f_vx=-4
        else:
            f_vx=0

        if j.rect.bottom> lim_i:
            j.rect.bottom=lim_i
            f_vy=-4
        else:
            f_vy=0


        if j.rect.top< lim_s:
            j.rect.top=lim_s
            f_vy=4



        if j.rect.left < lim_z:
            j.rect.left= lim_z
            f_vx=4

        if f_x > 0:
            f_x = 0

        if f_y > 0:
            f_y = 0



        for b in bloques:
            b.velx = f_vx/2
            b.vely=f_vy/2

        for g in generadores:
            g.velx = f_vx
            g.vely = f_vy

        for o in gomas:
            o.vely = f_vy

        for m in modifs:
            m.velx = f_vx
            m.vely = f_vy

        for m in modifs1:
            m.velx = f_vx
            m.vely = f_vy


        for m in modifs2:
            m.velx = f_vx
            m.vely = f_vy

        for k in jefes:
            k.vely = f_vy


        '''for je in jefes:
            je.velx = f_vx
            je.vely = f_vy
            if je.velx != 0 and je.vely != 0:
                je.velx = f_vx
                je.vely = f_vy
            else:
                je.velx = 0
                je.vely = 0'''



        ls_col = pygame.sprite.spritecollide(j, gomas, False)

        for g in ls_col:
            j.salud -= 1


        ls_col1 = pygame.sprite.spritecollide(j, modifs, False)

        for g1 in ls_col1:
            if j.salud < 100:
                j.salud += 5

        ls_col2 = pygame.sprite.spritecollide(j, modifs1, False)
        for p1 in ls_col2:
            if j.potencia < 100:
                j.potencia += 5

        for g1 in modifs:
            if g1.rect.y < -1:
                modifs.remove(g1)

        pygame.sprite.spritecollide(j, modifs, True)

        for p2 in modifs1:
            if g1.rect.y < -1:
                modifs1.remove(g1)

        pygame.sprite.spritecollide(j, modifs1, True)

        ls_col3 = pygame.sprite.spritecollide(j, modifs2, False)
        for p1 in ls_col3:
            if j.potencia < 100:
                j.potencia += 4
            if j.salud < 100:
                j.salud+= 4

        for g1 in modifs2:
            if g1.rect.y < -1:
                modifs.remove(g1)
        pygame.sprite.spritecollide(j, modifs2, True)

        for g in generadores:
            n_generadores = len(generadores)
            # seleccion aleatoria del generadpr
            if g.crear and (g.limite > len(gomas)):
                gm = Goma(g.RetPos(),ryuk, [f_ancho, f_alto])
                gomas.add(gm)
                g.crear=False
                g.temp=100

        ls_col = pygame.sprite.spritecollide(j, gomas, False)

        for g in ls_col:
            j.salud -= 1


        ls_col1 = pygame.sprite.spritecollide(j, modifs, False)

        for g1 in ls_col1:
            if j.salud < 100:
                j.salud += 5

        ls_col2 = pygame.sprite.spritecollide(j, modifs1, False)
        for p1 in ls_col2:
            if j.potencia < 100:
                j.potencia += 5

        for g1 in modifs:
            if g1.rect.y < -1:
                modifs.remove(g1)

        pygame.sprite.spritecollide(j, modifs, True)

        for p2 in modifs1:
            if g1.rect.y < -1:
                modifs1.remove(g1)

        pygame.sprite.spritecollide(j, modifs1, True)

        for g in generadores:
            n_generadores = len(generadores)
            # seleccion aleatoria del generadpr
            if g.crear and (g.limite > len(gomas)):
                gm = Goma(g.RetPos(),ryuk, [f_ancho, f_alto])
                gomas.add(gm)
                g.crear = False
                g.temp = 150

        for J in generadores1:
            n_generadores1 = len(generadores1)
            # seleccion aleatoria del generadpr
            if J.crear and (J.J > len(jefes)):
                ge = Jefe(J.RetPos(),je,[f_ancho-1000, f_alto])
                jefes.add(ge)
                J.crear = False
                J.temp = 150


        if j.salud <= 0:
            fin_juego = True

        #pantalla.fill(NEGRO)

        info = "Salud: " + str(j.salud)
        info1 = "Potencia: " + str(j.potencia)
        texto = fuente.render(info, False, BLANCO)
        texto1 = fuente.render(info1, False, BLANCO)
        jugadores.update()
        jefes.update()
        gomas.update()
        gomas1.update()
        bloques.update()
        balas.update()
        bloques.update()
        generadores.update()
        generadores1.update()
        modifs.update()
        modifs1.update()
        modifs2.update()



        pantalla.blit(fondo,[f_x, f_y])
        pantalla.blit(texto, [20, 20])
        pantalla.blit(texto1, [20, 40])

        generadores.draw(pantalla)
        jugadores.draw(pantalla)
        jefes.draw(pantalla)
        gomas.draw(pantalla)
        gomas1.draw(pantalla)
        bloques.draw(pantalla)
        balas.draw(pantalla)
        modifs.draw(pantalla)
        modifs1.draw(pantalla)
        modifs2.draw(pantalla)


        pygame.display.flip()
        reloj.tick(100)

        if f_x > f_limx :
            f_x+=f_vx

        if f_y > f_limy:
            f_y += f_vy

        if  f_limy1 >= f_y1 :
             f_y1 -=f_vy

        if  f_limx1 >= f_x1 :
            f_x1 -= f_vx


    # Ciclo fin de Juego
    fuente = pygame.font.Font(None, 50)
    info = "FIN DE JUEGO "
    texto = fuente.render(info, False, ROJO)
    # pantalla.fill(NEGRO)
    pantalla.blit(fondo, [0, 0])
    pantalla.blit(texto, [250, 200])
    pygame.display.flip()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
