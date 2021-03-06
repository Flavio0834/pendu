from tkinter import *
from tkinter import ttk
from random import randint
from tkinter import messagebox
from formes import *
from tkinter.colorchooser import askcolor
import sqlite3
from tkinter import simpledialog
from recupskin import *
from PIL import Image,ImageTk

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
		self.__listeFormes.append(Rectangle(self, 50,  320, 275,  26, "#8000ff", "hidden"))
		self.__listeFormes.append(Rectangle(self, 87,   83,  26, 250, "#8000ff", "hidden"))
		self.__listeFormes.append(Rectangle(self, 87,   70, 220,  26, "#8000ff", "hidden"))
		self.__listeFormes.append(Rectangle(self, 233,  67,  10,  40, "#8000ff", "hidden"))
		
		# Skin
		self.__tailles={
			'tete':((44,44),(216,120)),
			'bg':((17,66),(196,166)),
			'buste':((46,66),(215,166)),
			'bd':((17,66),(263,166)),
			'jg':((23,66),(214,234)),
			'jd':((23,66),(239,234))}
		self.changerSkin("FlavCraft0834")

		for i in range(10):
			self.etatForme(i+1,'normal')

	def etatForme(self,i,etat):
		self.itemconfig(i,state=etat)

	def changerFondCanva(self):
		self.config(bg=askcolor()[1])

	def changerCouleurPotence(self):
		couleur=askcolor()[1]
		print(couleur)
		for i in range(4):
			self.itemconfig(i+1,fill=couleur)

	def changerSkin(self,pseudo):
		self.__skin=recupskin(pseudo)
		if len(self.__listeFormes)==4:
			self.__listeFormes=self.__listeFormes[:4].copy()

			self.__teteTk=ImageTk.PhotoImage(Image.open(f"skin/part0.png").resize(self.__tailles['tete'][0]),master=self)
			self.__tete=self.create_image(self.__tailles['tete'][1],anchor=NW,image=self.__teteTk, state="hidden")
			self.__listeFormes.append(self.__tete)

			self.__bgTk=ImageTk.PhotoImage(Image.open(f"skin/part1.png").resize(self.__tailles['bg'][0]),master=self)
			self.__bg=self.create_image(self.__tailles['bg'][1],anchor=NW,image=self.__bgTk, state="hidden")
			self.__listeFormes.append(self.__bg)

			self.__busteTk=ImageTk.PhotoImage(Image.open(f"skin/part2.png").resize(self.__tailles['buste'][0]),master=self)
			self.__buste=self.create_image(self.__tailles['buste'][1],anchor=NW,image=self.__busteTk, state="hidden")
			self.__listeFormes.append(self.__buste)

			self.__bdTk=ImageTk.PhotoImage(Image.open(f"skin/part3.png").resize(self.__tailles['bd'][0]),master=self)
			self.__bd=self.create_image(self.__tailles['bd'][1],anchor=NW,image=self.__bdTk, state="hidden")
			self.__listeFormes.append(self.__bd)

			self.__jgTk=ImageTk.PhotoImage(Image.open(f"skin/part4.png").resize(self.__tailles['jg'][0]),master=self)
			self.__jg=self.create_image(self.__tailles['jg'][1],anchor=NW,image=self.__jgTk, state="hidden")
			self.__listeFormes.append(self.__jg)

			self.__jdTk=ImageTk.PhotoImage(Image.open(f"skin/part5.png").resize(self.__tailles['jd'][0]),master=self)
			self.__jd=self.create_image(self.__tailles['jd'][1],anchor=NW,image=self.__jdTk, state="hidden")
			self.__listeFormes.append(self.__jd)

		elif self.__skin:
			self.__teteTk=ImageTk.PhotoImage(Image.open(f"skin/part0.png").resize(self.__tailles['tete'][0]),master=self)
			self.itemconfig(self.__tete,image=self.__teteTk)

			self.__bgTk=ImageTk.PhotoImage(Image.open(f"skin/part1.png").resize(self.__tailles['bg'][0]),master=self)
			self.itemconfig(self.__bg,image=self.__bgTk)

			self.__busteTk=ImageTk.PhotoImage(Image.open(f"skin/part2.png").resize(self.__tailles['buste'][0]),master=self)
			self.itemconfig(self.__buste,image=self.__busteTk)

			self.__bdTk=ImageTk.PhotoImage(Image.open(f"skin/part3.png").resize(self.__tailles['bd'][0]),master=self)
			self.itemconfig(self.__bd,image=self.__bdTk)

			self.__jgTk=ImageTk.PhotoImage(Image.open(f"skin/part4.png").resize(self.__tailles['jg'][0]),master=self)
			self.itemconfig(self.__jg,image=self.__jgTk)

			self.__jdTk=ImageTk.PhotoImage(Image.open(f"skin/part5.png").resize(self.__tailles['jd'][0]),master=self)
			self.itemconfig(self.__jd,image=self.__jdTk)

		else:
			messagebox.showinfo(title="Information",message="Le pseudo indiqu?? n'est pas un pseudo associ?? ?? un compte Minecraft premium. Ainsi, le skin affich?? restera inchang??.")

class FenPrincipale(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.configure(bg="#808080")
		self.title('Jeu du pendu')
		self.geometry("600x600")
		self.__joueur=None # Pour plus tard

		# Frame 1 : Boutons
		self.__barreOutils=Frame(self)
		self.__barreOutils.pack(side=TOP)

		self.__boutonNouvellePartie = Button(self.__barreOutils, text='Nouvelle partie')
		self.__boutonQuitter = Button(self.__barreOutils, text='Quitter')
		self.__boutonNouvellePartie.pack(side=LEFT, padx=5, pady=5)
		self.__boutonQuitter.pack(side=LEFT, padx=5, pady=5)

		self.__boutonQuitter.config(command=self.destroy)
		self.__boutonNouvellePartie.config(command=self.nouvellePartie)

		# Canevas
		self.__canva=ZoneAffichage(self,450,350,"#808040")
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

		# Bouton connexion
		self.__menu.add_cascade(label="Choix joueur",command=self.authentification)

		# Menu Personnalisation
		self.__ongletPerso=Menu(self.__menu,tearoff=0)
		self.__ongletPerso.add_command(label="Modifier la couleur du fond",command=self.changerFond)
		self.__ongletPerso.add_separator()
		self.__ongletPerso.add_command(label="Modifier la couleur du fond de la barre d'outils",command=self.changerFondBarre)
		self.__ongletPerso.add_command(label="Modifier la couleur des boutons de la barre d'outils",command=self.changerCouleurBoutonsBarre)
		self.__ongletPerso.add_separator()
		self.__ongletPerso.add_command(label="Modifier la couleur du canevas",command=self.__canva.changerFondCanva)
		self.__ongletPerso.add_command(label="Modifier la couleur de la potence",command=self.__canva.changerCouleurPotence)
		self.__ongletPerso.add_separator()
		self.__ongletPerso.add_command(label="Modifier la couleur du fond du texte",command=self.changerCouleurFondTexte)
		self.__ongletPerso.add_separator()
		self.__ongletPerso.add_command(label="Modifier la couleur des boutons du clavier",command=self.changerCouleurBoutonsClavier)
		self.__ongletPerso.add_command(label="Modifier la couleur du fond du clavier",command=self.changerFondClavier)
		self.__menu.add_cascade(label="Personnalisation",menu=self.__ongletPerso)

		#Bouton Classement
		self.__menu.add_cascade(label="Classement",command=self.classement)

		#Bouton Undo
		self.__menu.add_cascade(label="Retour",command=self.triche)
		self.bind_all("<Control-z>",self.tricheClavier)
		self.bind_all("<Control-Z>",self.tricheClavier)

		self.config(menu=self.__menu)

		# Connexion BDD
		self.__bdd=JoueurDB('pendu.db')

	# On r??cup??re la liste des mots pour la nouvelle partie
	def chargeMots(self):
		f = open('mots.txt', 'r')
		s = f.read()
		self.__mots = s.split('\n')
		f.close()

	def nouvellePartie(self):
		# Choix du joueur
		if self.__joueur==None:
			self.authentification()

		# On clear le canevas
		for i in range(10):
			self.__canva.etatForme(i+1,'hidden')
		# On d??grise toutes les lettres
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

	# Gestion clic clavier
	def traitement(self,lettre):
		if lettre in self.__motSecret:
			mottemp=self.__mot.get()
			for i in range(len(self.__motSecret)):
				if lettre==self.__motSecret[i]:
					mottemp=mottemp[:i+6]+lettre+mottemp[i+7:]# remplace l'??toile ?? l'emplacement i par la lettre cliqu??e
			self.__mot.set(mottemp)
			if '*' not in self.__mot.get():
				self.gagne()# fonction qui g??re si la partie est finie en gagnant
		else:
			self.rate()# fonction qui g??re un coup rat?? (et g??re si la partie est finie en perdant)
		self.__coups.append(lettre)# utile plus tard pour impl??menter la fonction undo

	# Coup rat?? et fin de partie.
	def gagne(self):
		self.__fini=True
		for k in self.__clavierListe:
			if k['state']=='normal':
				self.__boutonsAllumes.append(k)
			k.config(state='disabled')
		mottemp=self.__mot.get()
		self.__mot.set("C'est gagn?? ! :) "+mottemp)
		self.__bdd.save_game(self.__idjoueur,self.__motSecret,1.0)# On enregistre la partie avec un score de 1.0

	def rate(self):
		self.__rates+=1
		if self.__rates>=10:
			self.perdu()
		self.__canva.etatForme(self.__rates,'normal')

	def perdu(self):
		self.__fini=True
		self.__perdu=self.__mot.get()

		actuel=self.__perdu[::-1][:len(self.__motSecret)][::-1]# Calcul score et insertion db
		nbetoiles=actuel.count('*')
		score=(len(self.__motSecret)-nbetoiles)/len(self.__motSecret)
		self.__bdd.save_game(self.__idjoueur,self.__motSecret,score)

		self.__boutonsAllumes=[]
		for k in self.__clavierListe:
			if k['state']=='normal':
				self.__boutonsAllumes.append(k)
			k.config(state='disabled')
		self.__mot.set("C'est perdu ! :( Mot : "+self.__motSecret)

	# Custom
	def changerFond(self):
		self.configure(bg=askcolor()[1])

	def changerFondClavier(self):
		couleur=askcolor()[1]
		self.__clavier.configure(bg=couleur)

	def changerCouleurBoutonsClavier(self):
		couleur=askcolor()[1]
		for i in range(len(self.__clavierListe)):
			self.__clavierListe[i].configure(bg=couleur)

	def changerFondBarre(self):
		couleur=askcolor()[1]
		self.__barreOutils.configure(bg=couleur)

	def changerCouleurBoutonsBarre(self):
		couleur=askcolor()[1]
		self.__boutonNouvellePartie.configure(bg=couleur)
		self.__boutonQuitter.configure(bg=couleur)

	def changerCouleurFondTexte(self):
		couleur=askcolor()[1]
		self.__texte.configure(bg=couleur)
	
	# Ex 8 : ajout Undo
	def triche(self):
		lettre=self.__coups.pop()
		for k in self.__clavierListe:# On d??grise la derni??re case
			if k['text']==lettre:
				k.config(state='normal')
		if lettre in self.__motSecret:# Si le dernier coup ??tait un bon coup, on remet les *
			mottemp=self.__mot.get()
			actuel=mottemp[::-1][:len(self.__motSecret)][::-1]
			for i in range(len(self.__motSecret)):
				if self.__motSecret[i]==lettre:
					actuel=actuel[:i]+'*'+actuel[i+1:]
			self.__mot.set("Mot : "+actuel)
			if self.__fini:
				self.__bdd.del_last()
		else:# Si c'??tait un mauvais coup
			if self.__fini:# Et que c'??tait fini, on remet le message tel quel
				self.__mot.set(self.__perdu)
				self.__bdd.del_last()
				self.__fini=False
			# Dans tous les cas, il faut retirer le dernier dessin et une erreur comptabilis??e.
			self.__canva.etatForme(self.__rates,'hidden')
			self.__rates-=1

		if self.__boutonsAllumes!=[]:# Si la partie ??tait finie (gagn??e/perdue), on remet les cases telles qu'elles ??taient
			for k in self.__boutonsAllumes:
				k.config(state='normal')
			self.__boutonsAllumes=[]

	def tricheClavier(self,event):# Bind control-z envoie event en argument et ce n'est pas accept?? par la fonction ci-dessus qui est une callback
		self.triche()

	def classement(self):
		if self.__joueur==None:
			self.authentification()
		self.__leaderboard_abs=self.__bdd.get_leaderboard_abs(self.__joueur)
		self.__leaderboard_rel=self.__bdd.get_leaderboard_rel(self.__joueur)
		fenClassement=FenStats(self.__leaderboard_abs,self.__leaderboard_rel)
		fenClassement.mainloop()

	def authentification(self):
		self.__joueur=None
		while self.__joueur==None or self.__joueur=='':
			self.__joueur=simpledialog.askstring("Choix joueur", "Quel est ton pseudo ?",parent=self)
		self.__idjoueur=self.__bdd.ajouter_connecter_joueur(self.__joueur)
		self.__canva.changerSkin(self.__joueur)

class JoueurDB:
	def __init__(self,nomDB):
		self.__conn=sqlite3.connect(nomDB)

	def __del__(self):
		self.__conn.close()

	def ajouter_connecter_joueur(self,pseudo):# Le joueur se connecte avec son pseudo, on recup ses ID
		try:
			assert type(pseudo)==str,'Le pseudo doit ??tre une cha??ne de caract??res'
			self.__curseur=self.__conn.cursor()
			self.__curseur.execute("SELECT idjoueur FROM joueurs WHERE pseudo=(?)",(pseudo,))
			return self.__curseur.fetchone()[0]
		except:
			assert type(pseudo)==str,'Le pseudo doit ??tre une cha??ne de caract??res'
			self.__curseur.execute("INSERT INTO joueurs (pseudo) VALUES (?)",(pseudo,))
			self.__conn.commit()
			return self.__curseur.lastrowid

	def save_game(self,idjoueur,mot,score):
		try:
			self.__curseur=self.__conn.cursor()
			self.__curseur.execute("INSERT INTO parties (idjoueur,mot,score) VALUES (?,?,?)",(idjoueur,mot,score))
			self.__dernierepartie=self.__curseur.lastrowid
			self.__conn.commit()
		except Exception as err:
			print('err:', str(err))
			print('type exception:', type(err).__name__)

	def get_leaderboard_abs(self,joueur):
		try:
			self.__curseur=self.__conn.cursor()
			self.__curseur.execute("SELECT joueurs.pseudo,sum(score),count(score) FROM parties JOIN joueurs ON joueurs.idjoueur=parties.idjoueur GROUP BY joueurs.pseudo ORDER BY sum(score) DESC")
			classement=self.__curseur.fetchall()
			if len(classement)<=5:
				return classement
			else:
				joueurtop5=False
				joueurclasse=False
				placement=None
				for i in range(len(classement)):
					if classement[i][0]==joueur:
						joueurclasse=True
						placement=i
						if i<5:
							joueurtop5=True
				if joueurtop5 or not joueurclasse:
					return classement[:5]
				else:
					res=classement[:5]
					res.append((classement[placement][0]+' ('+str(placement+1)+'??me)',classement[placement][1],classement[placement][2]))
					return res
		except Exception as err:
			print('err:', str(err))
			print('type exception:', type(err).__name__)
			return str(err)

	def get_leaderboard_rel(self,joueur):
		try:
			self.__curseur=self.__conn.cursor()
			self.__curseur.execute("SELECT joueurs.pseudo,sum(score),count(score) FROM parties JOIN joueurs ON joueurs.idjoueur=parties.idjoueur GROUP BY joueurs.pseudo ORDER BY sum(score)/count(score) DESC")
			classement=self.__curseur.fetchall()
			if len(classement)<=5:
				return classement
			else:
				joueurtop5=False
				joueurclasse=False
				placement=None
				for i in range(len(classement)):
					if classement[i][0]==joueur:
						joueurclasse=True
						placement=i
						if i<5:
							joueurtop5=True
				if joueurtop5 or not joueurclasse:
					return classement[:5]
				else:
					res=classement[:5]
					res.append((classement[placement][0]+' ('+str(placement+1)+'??me)',classement[placement][1],classement[placement][2]))
					return res
		except Exception as err:
			print('err:', str(err))
			print('type exception:', type(err).__name__)
			return str(err)

	def del_last(self):
		try:
			self.__curseur=self.__conn.cursor()
			self.__curseur.execute("DELETE FROM parties WHERE idpartie=(?)",(self.__dernierepartie,))
			self.__conn.commit()
		except Exception as err:
			print('err:', str(err))
			print('type exception:', type(err).__name__)

class FenStats(Tk):
	def __init__(self,leaderboard_abs,leaderboard_rel):
		Tk.__init__(self)
		self.configure(bg="#C0C0C0")
		self.title('Jeu du pendu')
		self.geometry("600x450")

		# Menu bouton changer fond
		self.__menu=Menu(self)
		self.__menu.add_cascade(label="Modifier la couleur du fond",command=self.changerFond)
		self.config(menu=self.__menu)

		# Classements : un en haut et un en bas, basique : score total et relatif : score / nb parties
		self.__top5Basique=Frame(self)
		self.__top5Relatif=Frame(self)
		self.__top5Basique.pack(side=TOP)
		self.__top5Relatif.pack(side=TOP)

		self.__labelBasique=Label(self.__top5Basique, text="Classement global (Top 5)")
		self.__labelRelatif=Label(self.__top5Relatif, text="Classement relatif au nombre de parties")
		self.__labelBasique.pack(side=TOP)
		self.__labelRelatif.pack(side=TOP)

		# Classement basique
		self.__tableauBasique=ttk.Treeview(self.__top5Basique,columns=('pseudo','scoretotal','nbparties'))
		self.__tableauBasique.heading('pseudo', text='Pseudo')
		self.__tableauBasique.heading('scoretotal', text='Score Total')
		self.__tableauBasique.heading('nbparties', text='Nombre de parties jou??es')
		self.__tableauBasique['show']='headings'# Cacher la premi??re colonne de libell??s

		# Classement relatif
		self.__tableauRelatif=ttk.Treeview(self.__top5Relatif,columns=('pseudo','scoremoyen'))
		self.__tableauRelatif.heading('pseudo', text='Pseudo')
		self.__tableauRelatif.heading('scoremoyen', text='Score moyen (Total / Parties)')
		self.__tableauRelatif['show']='headings'

		# Remplissage du classement
		for i in range(len(leaderboard_abs)):
			self.__tableauBasique.insert('','end',values=(leaderboard_abs[i][0],leaderboard_abs[i][1],leaderboard_abs[i][2]))
		for i in range(len(leaderboard_rel)):
			self.__tableauRelatif.insert('','end',values=(leaderboard_rel[i][0],leaderboard_rel[i][1]/leaderboard_rel[i][2]))
		
		self.__tableauBasique.pack()
		self.__tableauRelatif.pack()

	def changerFond(self):
		self.configure(bg=askcolor()[1])

if __name__=="__main__":
	fen = FenPrincipale()
	fen.mainloop()