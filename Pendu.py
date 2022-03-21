from tkinter import *
from tkinter import ttk
from random import randint
from formes import *
from tkinter.colorchooser import askcolor
import sqlite3
from tkinter import simpledialog# a voir

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
		self.title('Jeu du pendu')
		self.geometry("600x600")
		self.__joueur=None # Pour plus tard

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

		# Bouton connexion
		self.__menu.add_cascade(label="Choix joueur",command=self.authentification)

		# Menu Personnalisation
		self.__ongletPerso=Menu(self.__menu,tearoff=0)
		self.__ongletPerso.add_command(label="Modifier la couleur de fond",command=self.changerFond)
		self.__ongletPerso.add_command(label="Modifier la couleur du canevas",command=self.__canva.changerFondCanva)
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


	# On récupère la liste des mots pour la nouvelle partie
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

	# Gestion clic clavier
	def traitement(self,lettre):
		if lettre in self.__motSecret:
			mottemp=self.__mot.get()
			for i in range(len(self.__motSecret)):
				if lettre==self.__motSecret[i]:
					mottemp=mottemp[:i+6]+lettre+mottemp[i+7:]# remplace l'étoile à l'emplacement i par la lettre cliquée
			self.__mot.set(mottemp)
			if '*' not in self.__mot.get():
				self.gagne()# fonction qui gère si la partie est finie en gagnant
		else:
			self.rate()# fonction qui gère un coup raté (et gère si la partie est finie en perdant)
		self.__coups.append(lettre)# utile plus tard pour implémenter la fonction undo

	# Coup raté et fin de partie.
	def gagne(self):
		self.__fini=True
		for k in self.__clavierListe:
			if k['state']=='normal':
				self.__boutonsAllumes.append(k)
			k.config(state='disabled')
		mottemp=self.__mot.get()
		self.__mot.set("C'est gagné ! :) "+mottemp)
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

	# Custom bg
	def changerFond(self):
		self.configure(bg=askcolor()[1])
	
	# Ex 8 : ajout Undo
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
			if self.__fini:
				self.__bdd.del_last()
		else:# Si c'était un mauvais coup
			if self.__fini:# Et que c'était fini, on remet le message tel quel
				self.__mot.set(self.__perdu)
				self.__bdd.del_last()
				self.__fini=False
			# Ensuite dans tous les cas, il faut retirer le dernier dessin et une erreur comptabilisée.
			self.__canva.etatForme(self.__rates,'hidden')
			self.__rates-=1

		if self.__boutonsAllumes!=[]:# Si la partie était finie (gagnée/perdue), on remet les cases telles qu'elles étaient
			for k in self.__boutonsAllumes:
				k.config(state='normal')
			self.__boutonsAllumes=[]

	def tricheClavier(self,event):# Bind control-z envoie event en argument et ce n'est pas accepté par la fonction ci-dessus qui est une callback
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


class JoueurDB:
	def __init__(self,nomDB):
		self.__conn=sqlite3.connect(nomDB)
	def __del__(self):
		self.__conn.close()
	def ajouter_connecter_joueur(self,pseudo):# Le joueur se connecte avec son pseudo, on recup ses ID
		try:
			assert type(pseudo)==str,'Le pseudo doit être une chaîne de caractères'
			self.__curseur=self.__conn.cursor()
			self.__curseur.execute("SELECT idjoueur FROM joueurs WHERE pseudo=(?)",(pseudo,))
			return self.__curseur.fetchone()[0]
		except:
			assert type(pseudo)==str,'Le pseudo doit être une chaîne de caractères'
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
					res.append((classement[placement][0]+' ('+str(placement+1)+'ème)',classement[placement][1],classement[placement][2]))
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
					res.append((classement[placement][0]+' ('+str(placement+1)+'ème)',classement[placement][1],classement[placement][2]))
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
		self.configure(bg="gray")
		self.title('Jeu du pendu')
		self.geometry("600x450")

		# Menu bouton changer fond
		self.__menu=Menu(self)
		self.__menu.add_cascade(label="Modifier la couleur du fond",command=self.changerFond)
		self.config(menu=self.__menu)

		# Classements : un à gauche et un à droite, basique : score total et relatif : score / nb parties
		self.__top5Basique=Frame(self)
		self.__top5Relatif=Frame(self)
		#self.__separateur=ttk.Separator(self,orient='horizontal')# vérif hor/ver (Orientation du séparateur ou du placement des éléments séparés ?)
		self.__top5Basique.pack(side=TOP)
		#self.__separateur.pack(side=LEFT,fill='x')
		self.__top5Relatif.pack(side=TOP)

		self.__labelBasique=Label(self.__top5Basique, text="Classement global (Top 5)")
		self.__labelRelatif=Label(self.__top5Relatif, text="Classement relatif au nombre de parties")
		self.__labelBasique.pack(side=TOP)
		self.__labelRelatif.pack(side=TOP)

		# Classement basique
		self.__gridBasique=ttk.Treeview(self.__top5Basique,columns=('pseudo','scoretotal','nbparties'))
		self.__gridBasique.heading('pseudo', text='Pseudo')
		self.__gridBasique.heading('scoretotal', text='Score Total')
		self.__gridBasique.heading('nbparties', text='Nombre de parties jouées')
		self.__gridBasique['show']='headings'# Cacher la première colonne de libellés

		# Classement relatif
		self.__gridRelatif=ttk.Treeview(self.__top5Relatif,columns=('pseudo','scoremoyen'))
		self.__gridRelatif.heading('pseudo', text='Pseudo')
		self.__gridRelatif.heading('scoremoyen', text='Score moyen (Total / Parties)')
		self.__gridRelatif['show']='headings'# Cacher la première colonne de libellés

		# Remplissage du classement
		for i in range(len(leaderboard_abs)):
			self.__gridBasique.insert('','end',values=(leaderboard_abs[i][0],leaderboard_abs[i][1],leaderboard_abs[i][2]))
		for i in range(len(leaderboard_rel)):
			self.__gridRelatif.insert('','end',values=(leaderboard_rel[i][0],leaderboard_rel[i][1]/leaderboard_rel[i][2]))
		
		self.__gridBasique.pack()
		self.__gridRelatif.pack()

	def changerFond(self):
		self.configure(bg=askcolor()[1])


	# implémenter ctrl+Z ?

	
				


if __name__=="__main__":
	fen = FenPrincipale()
	fen.mainloop()