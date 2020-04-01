import sys
from ruler import Ruler #on importe notre classe

DataSet = sys.argv[1] #
fichier1 = open(DataSet, "r") #on met en deuxième le nom du fichier à lire
M = [] 

for l in fichier1:
    L = l.replace('\n', "") #on enlève les \n dans chaque string

    if L != "": 
        M.append(L)

i = 0

while i < len(L)-1: #on s'arrête à l'avant-avant-dernier
    ruler = Ruler(L[i], L[i+1]) #on applique la classe
    ruler.calculate()
    top, bottom = ruler.report()
    print(f'''-----------------example #{i//2} distance = {ruler.distance}
    {top}
    {bottom}''')
    i += 2