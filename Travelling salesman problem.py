# -*- coding: utf-8 -*-
"""
author : ADJARIAN Stéphan
"""

import timeit
import random

class individu: 
    def __init__(self, val=None):
        if val==None:
            self.val=random.sample(list(range(4)), 4)
        else:
            self.val=val
        self.distanceParcourue=self.fitness()
                      
    def __str__(self):
        return str(self.val)  

    def fitness(self):
        """ evaluer l'individu c'est connaitre la distance parcourue."""
        self.distanceParcourue=0     
        for i in range(3):
            if (self.val[i]==0 and self.val[i+1]==1) or (self.val[i]==1 and self.val[i+1]==0):
                self.distanceParcourue+=4
            if (self.val[i]==0 and self.val[i+1]==2) or (self.val[i]==2 and self.val[i+1]==0):
                self.distanceParcourue+=3
            if (self.val[i]==0 and self.val[i+1]==3) or (self.val[i]==3 and self.val[i+1]==0):
                self.distanceParcourue+=1
            if (self.val[i]==1 and self.val[i+1]==2) or (self.val[i]==2 and self.val[i+1]==1):
                self.distanceParcourue+=1
            if (self.val[i]==1 and self.val[i+1]==3) or (self.val[i]==3 and self.val[i+1]==1):
                self.distanceParcourue+=2
            if (self.val[i]==2 and self.val[i+1]==3) or (self.val[i]==3 and self.val[i+1]==2):
                self.distanceParcourue+=5                
        return self.distanceParcourue
        
def create_rand_pop(count):
    return [individu() for i in range(count)]
       
def evaluate(pop):
    return sorted(pop, key=lambda x : x.fitness())

def selection(pop,hcount,lcount):
    return pop[0:hcount]+pop[len(pop)-lcount:]

def croisement(ind1,ind2):
    #on prend les 2 premières ville de ind1 et les 2 dernières de ind2 et inversement.
    a,b=(individu(ind1.val[:2]+ind2.val[2:]), individu(ind2.val[:2]+ind1.val[2:]))
    #on vérifie ici que l'individu n'a pas 2 fois la même ville (possiblement du au croisement)
    #un coup on modifera les 2 premières si besoin
    #l'autre coup on modifiera les 2 dernières.
    for i in range(3,-1,-1):
        for j in range(3,-1,-1):
            if a.val[i]==a.val[j] and i!=j:
                liste=[]
                s1=set([0,1,2,3])
                for k in range(4):
                    #j'ajoute à ma liste les villes n'étant pas dans mon individu.
                    if liste.count(a.val[k])==0:
                        liste.append(a.val[k])
                s2=set(liste)
                d=s1-s2
                d=list(d)
                #je choisis une de ces villes aléatoirement
                indice=random.randint(0,len(d)-1)
                a.val[i]=d[indice]   
    for i in range(4):
        for j in range(4):
            if b.val[i]==b.val[j] and i!=j:
                liste=[]
                s1=set([0,1,2,3])
                for k in range(4):
                    if liste.count(b.val[k])==0:
                        liste.append(b.val[k])
                s2=set(liste)
                d=s1-s2
                d=list(d)
                indice=random.randint(0,len(d)-1)
                b.val[i]=d[indice]       
    return a,b

def Mutation(ind):
    Ville1=random.randint(0,3)
    Ville2=random.randint(0,3)
    #on permute la ville 1 avec la ville 2
    permutant=ind.val[Ville1]
    ind.val[Ville1]=ind.val[Ville2]
    ind.val[Ville2]=permutant
    return ind

def algosimple():
    # on crée une population aléatoire d’un certain nombre d’individus (10)
    pop=create_rand_pop(10)
    nbiteration=0
    solutiontrouvee=False
    while not solutiontrouvee:
        print("iteration numero :",nbiteration)
        nbiteration+=1
        evaluation = evaluate(pop)
        """ pour afficher la génération de population
        for i in range(len(pop)):
            print("individu pop : ", pop[i].val, "de fitness :" ,pop[i].fitness()) 
        print(len(pop))
        """
        #Affiche la population trié selon la fonction de fitness car evaluation trie les ind.
        for i in range(len(evaluation)):
            print(i,": individu trié : ", evaluation[i], "de fitness :" ,evaluation[i].fitness()) 
        print(len(evaluation))
        #on l’évalue, si on on tombe sur un individu à fitness <5km
        if evaluation[0].fitness()<5:
            solutiontrouvee=True
        else:
            #On sélectionne les 6 meilleurs et les 2 plus mauvais individus
            #/!\ Il doit y en avoir un nombre pair 6+2=8 est pair
            select=selection(evaluation,6,2)
            #○on croise ces individus 2 à 2.
            croises=[]
            for i in range(0,len(select),2):
                croises+=croisement(select[i],select[i+1])
            #on mute tous les individus selectionnés
            mutes=[]
            for i in select:
                mutes.append(Mutation(i))
            #on créé de nouveaux individus aléatoirement.
            newalea=create_rand_pop(6)
            print("select =", len(select), "croise =", len(croises), "mute =", len(mutes), "newalea =", len(newalea))
            pop=select[:]+croises[:]+mutes[:]+newalea[:]
            #len(pop)=8+8+8+6=30
    #On affiche le meilleur des individus 
    print("Meilleure solution trouvée :", evaluation[0])       
#Affiche le temps nécessaire pour trouver une solution
starttime = timeit.default_timer()
print("The start time is :",starttime)
algosimple()
print("The time difference is :", timeit.default_timer() - starttime)