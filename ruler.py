from colorama import init, Fore, Style
import numpy as np
from itertools import product
import string
init(convert=True) #on met en marche le module colorama
class Ruler:
    def choix_mat(self, S): #on définit les matrices dans le cas où toutes les substitutions ont le même coût
        if S == "":
            M = np.zeros(shape=(26, 26))
            for i, j in product(range(25), range(25)):
                if i != j:
                    M[i][j] = 1
            return M
        else: # si on veut définir une autre matrice pour les coûts
            return S

    def __init__(self, A, B, d=1, S="", remplacement_cost=1, insert_cost=1):
        self.A = A #chaîne 1
        self.B = B #chaîne 2
        self.A_mod = None #chaîne 1 qu'on aligne avec la 2
        self.B_mod = None #chaîne 2 modifée pour être alignée avec la 2
        self.n = len(self.A) 
        self.m = len(self.B)
        self.distance = None #distance entre les deux chaînes de caractères
        self.d = d #coût d'un non alignement 
        self.remplacement_cost = remplacement_cost  #on définit la valeur de la distance liée à un remplacement
        self.insert_cost = insert_cost   #on définit la distance liée à un saut
        self.S=self.choix_mat(S) #matrice des coût de substitution entre les lettres
    def report(self):
        return self.A_mod, self.B_mod #fonction pour retourner les 2 chaînes modifiées 

    def cout_substitution(self, x, y): # on calcule le coût de substitution de 'x' et 'y'
        M = list(string.ascii_lowercase)  # liste où on retrouve les lettres de l'alphabet
        m_1 = x.lower()
        m_2 = y.lower()
        i = M.index(m_1)
        j = M.index(m_2)
        return self.S[i][j]
    
    def red_text(self, text):
        return f"{Fore.RED}{text}{Style.RESET_ALL}" #fonction pour mettre une chaîne de caractère en rouge

    def calculate(self): # on va calculer la distance entre les deux chaînes de caractères
        Score = np.empty(shape=(self.n + 1, self.m + 1)) 
        Chemin = np.zeros(shape=(self.n + 1, self.m + 1)) #la matrice qui note au fur et à mesure le chemin à remonter

        Score[0][0] = 0 #le cout en haut à gauche est nul
        Chemin[0][0] = 3 #dans la matrice Chemin, on associe la valeur 3 à la case en haut à gauche (l'arrêt)
        #on associe la valeur 0 quand on vient de la case en diagonale juste avant
        #on associe la valeur 1 quand on vient de la case juste au dessus
        #on associe la valeur 2 quand on vient de la case à gauche


        for l in range(1, self.m + 1):
            Score[0][l] = (l*self.d)
            Chemin[0][l] = 1

        for k in range(1, self.n + 1): #coûts et déplacements associés sur la première ligne
            Score[k][0] = (k*self.d)
            Chemin[k][0] = 2

        for (k, l) in product(range(1, self.n+1), range(1, self.m+1)): #le reste des cases
            cout = [Score[i-1][j-1] + self.cout_substitution(self.A[i-1], self.B[j-1]),
                    Score[i][j-1] + self.d,
                    Score[i-1][j] + self.d]
            m = min(cout)
            Score[k][l] = min(cout)
            Chemin[k][l] = cout.index(m) #on met 0,1 ou 2 en fonction de l'opération qui compte le moins cher

        x, y = (self.n, self.m) #ici, on part d'en bas à droit de Chemin, on remonte les cases jusqu'à la case de départ 
        #avec le chemin optimal

        etat = Chemin[x][y]
        n_1 = []
        n_2 = []
        self.distance = 0
        while etat != 3: #le critère d'arrêt en haut à gauche

            if etat == 0:#on test les valeurs pour savoir si on doit remonter en diagonale
                if self.B[y-1] != self.A[x-1]:
                    self.distance += self.remplacement_cost
                    n_1 = [self.red_text(self.A[x-1])] + n_1 #on met un "=" en rouge quand on met un gap
                    n_2 = [self.red_text(self.B[y-1])] + n_2
                else:
                    n_1 = [self.A[x-1]] + n_1
                    n_2 = [self.B[y-1]] + n_2
                x, y = (x-1, y-1)

            elif etat == 1:#on test les valeurs pour savoir si on doit remonter à la verticale
                n_1 = [self.red_text("=")] + n_1
                n_2 = [self.B[y-1]] + n_2
                x, y = (x, y-1)
                self.distance += self.insert_cost
            else: #on test les valeurs pour savoir si on doit remonter à l'horizontale
                n_1 = [self.A[x-1]] + n_1
                n_2 = [self.red_text("=")] + n_2
                x, y = (x-1, y)
                self.distance += self.insert_cost
            etat = Chemin[x][y]

        self.A_mod = "".join(n_1) 
        self.B_mod = "".join(n_2)