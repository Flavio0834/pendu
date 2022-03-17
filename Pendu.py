from tkinter import *
from random import randint
from formes import *
from tkinter.colorchooser import askcolor

class monBoutonLettre(Button):
    def __init__(self,parent,texte,traitement):
        super().__init__(parent,text=texte)
        self.__lettre=texte
        self.traitement=traitement
        self.config(command=self.cliquer,state="disabled")
    
    def cliquer(self):
        self.config(state="disabled")
        self.traitement(self.__lettre)

class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur, couleur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur, bg=couleur)
        self.__listeFormes=[]

        # Base, Poteau, Traverse, Corde
        self.__listeFormes.append(Rectangle(self, 50,  270, 200,  26, "brown", "hidden"))
        self.__listeFormes.append(Rectangle(self, 87,   83,  26, 200, "brown", "hidden"))
        self.__listeFormes.append(Rectangle(self, 87,   70, 150,  26, "brown", "hidden"))
        self.__listeFormes.append(Rectangle(self, 183,  67,  10,  40, "brown", "hidden"))
        # Tete, Tronc
        self.__listeFormes.append(Rectangle(self, 188, 120,  20,  20, "black", "hidden"))
        self.__listeFormes.append(Rectangle(self, 175, 143,  26,  60, "black", "hidden"))
        # Bras gauche et droit
        self.__listeFormes.append(Rectangle(self, 133, 150,  40,  10, "black", "hidden"))
        self.__listeFormes.append(Rectangle(self, 203, 150,  40,  10, "black", "hidden"))
        # Jambes gauche et droite
        self.__listeFormes.append(Rectangle(self, 175, 205,  10,  40, "black", "hidden"))
        self.__listeFormes.append(Rectangle(self, 191, 205,  10,  40, "black", "hidden"))



    def etatForme(self,i,state):
        self.__listeFormes[i-1].setState(state)

    def changerFondCanva(self):
        self.config(bg=askcolor()[1])



class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.configure(bg="blue")
        # L'initialisation de l'arbre de scène se fait ici
        self.title('Jeu du pendu')
        #self.geometry('300x100+400+400')
        self.geometry("600x600")

        # Frame 1 : Boutons
        self.__barreOutils=Frame(self)
        self.__barreOutils.pack(side=TOP)

        boutonNouvellePartie = Button(self.__barreOutils, text='Nouvelle partie')
        boutonQuitter = Button(self.__barreOutils, text='Quitter')
        boutonNouvellePartie.pack(side=LEFT, padx=5, pady=5)
        boutonQuitter.pack(side=LEFT, padx=5, pady=5)

        boutonQuitter.config(command=self.destroy)
        boutonNouvellePartie.config(command=self.nouvellePartie)

        # Canevas
        self.__canva=ZoneAffichage(self,400,300,"red")
        self.__canva.pack(side=TOP,padx=5,pady=5)



        # Label : mot
        self.__mot=StringVar()
        self.__mot.set("Lancez une partie !")
        self.__motSecret=''
        self.__texte=Label(self,textvariable=self.__mot)
        self.__texte.pack(side=TOP,padx=8,pady=6,ipadx=5,ipady=2)

        # Frame 2 : clavier
        self.__clavier=Frame(self)
        self.__clavier.pack(side=TOP,padx=5,pady=5)

        self.__clavierListe=[]
        for i in range(26):
            boutonLettre=monBoutonLettre(self.__clavier,chr(ord('A')+i),self.traitement)
            self.__clavierListe.append(boutonLettre)
            if (i//7)+1==4:
                boutonLettre.grid(row=(i//7)+1,column=(i%7)+2,ipadx=8,padx=5,pady=3)
            else:
                boutonLettre.grid(row=(i//7)+1,column=(i%7)+1,ipadx=8,padx=5,pady=3)

        # Barre Menu
        self.__menu=Menu(self)

        # Menu Personnalisation
        self.__ongletPerso=Menu(self.__menu,tearoff=0)
        self.__ongletPerso.add_command(label="Modifier la couleur de fond",command=self.changerFond)
        self.__ongletPerso.add_command(label="Modifier la couleur du canevas",command=self.__canva.changerFondCanva)
        self.__menu.add_cascade(label="Personnalisation",menu=self.__ongletPerso)

        #Bouton Undo
        self.__menu.add_cascade(label="Retour",command=self.triche)


        self.config(menu=self.__menu)


    # On récupère la liste des mots pour la nouvelle partie
    def chargeMots(self):
        f = open('mots.txt', 'r')
        s = f.read()
        self.__mots = s.split('\n')
        f.close()

    def nouvellePartie(self):
        for i in range(10):
            self.__canva.etatForme(i+1,'hidden')
        # On dégrise toutes les lettres
        for k in self.__clavierListe:
            k.config(state='normal')
        # On charge les mots et on en affiche un au hasard
        self.chargeMots()
        self.__motSecret=self.__mots[randint(0,len(self.__mots)-1)]
        self.__mot.set("Mot : "+'*'*len(self.__motSecret))
        self.__rates=0
        self.__coups=[]
        self.__perdu=''
        self.__fini=False
        self.__boutonsAllumes=[]

    def traitement(self,lettre):
        if lettre in self.__motSecret:
            mottemp=self.__mot.get()
            for i in range(len(self.__motSecret)):
                if lettre==self.__motSecret[i]:
                    mottemp=mottemp[:i+6]+lettre+mottemp[i+7:]
            self.__mot.set(mottemp)
            if '*' not in self.__mot.get():
                self.gagne()
        else:
            self.rate()
        self.__coups.append(lettre)

    def gagne(self):
        self.__fini=True
        for k in self.__clavierListe:
            if k['state']=='normal':
                self.__boutonsAllumes.append(k)
            k.config(state='disabled')
        mottemp=self.__mot.get()
        self.__mot.set("C'est gagné ! :) "+mottemp)

    def rate(self):
        self.__rates+=1
        if self.__rates>=10:
            self.perdu()
        self.__canva.etatForme(self.__rates,'normal')

    def perdu(self):
        self.__fini=True
        self.__perdu=self.__mot.get()
        self.__boutonsAllumes=[]
        for k in self.__clavierListe:
            if k['state']=='normal':
                self.__boutonsAllumes.append(k)
            k.config(state='disabled')
        self.__mot.set("C'est perdu ! :( Mot : "+self.__motSecret)

    def changerFond(self):
        self.configure(bg=askcolor()[1])
    
    def triche(self):
        lettre=self.__coups.pop()
        for k in self.__clavierListe:# On dégrise la dernière case
            if k['text']==lettre:
                k.config(state='normal')
        if lettre in self.__motSecret:# Si le dernier coup était un bon coup, on remet les *
            mottemp=self.__mot.get()
            actuel=mottemp[::-1][:len(self.__motSecret)][::-1]
            for i in range(len(self.__motSecret)):
                if self.__motSecret[i]==lettre:
                    actuel=actuel[:i]+'*'+actuel[i+1:]
            self.__mot.set("Mot : "+actuel)
        else:# Si c'était un mauvais coup
            if self.__fini:# Et que c'était fini, on remet le message tel quel
                self.__mot.set(self.__perdu)
            # Ensuite dans tous les cas, il faut retirer le dernier dessin et une erreur comptabilisée.
            self.__canva.etatForme(self.__rates,'hidden')
            self.__rates-=1

        if self.__boutonsAllumes!=[]:# Si la partie était finie (gagnée/perdue), on remet les cases telles qu'elles étaient
            for k in self.__boutonsAllumes:
                k.config(state='normal')
            self.__boutonsAllumes=[]


if __name__=="__main__":
    fen = FenPrincipale()
    fen.mainloop()