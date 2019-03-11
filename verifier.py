#!/usr/bin/env python3

from collections import Counter
import csv
import itertools
import random

random.seed(42)

class Row:

    def __init__(self, id, row, public_items):
        self.id = id
        self.private = list() # private items
        self.public = list() # public items
        for item in row:
            try:
                item = int(item)
            except ValueError:
                continue
            if item in public_items:
                self.public.append(item)
            else:
                self.private.append(item)

    def delete_item(self, item):
        """Rimuove l'elemento passato dalla riga"""
        try:
            self.public.remove(item)
        except ValueError:
            pass

    def __repr__(self):
        return str(self.id)


class Table:

    def __init__(self, filename, n_items, delta, p, h, k):
        """
        n_items - numero di item nell'universo del database
        delta - percentuale di attributi pubblici
        p - numero massimo attributi conosciuti
        h - max probabilità che una transazione contenga 1 dato privato
        k - numero min di transazioni per ogni sottoinsieme di attributi pubblici conosciuti
        """
        self.p = p
        self.h = h
        self.k = k
        self.U = range(1, n_items + 1) # lista di tutti gli items (Universo)
        self.public_items = [1,2,3] # TODO: prendere i pubblici
        self.private_items = [4,5,6] # TODO: prendere i privati
        self.rows = list()
        with open(filename, "r") as dataset:
            csv_reader = csv.reader(dataset, delimiter=' ')
            id = 0
            for row in csv_reader:
                id += 1
                self.rows.append(Row(id, row, self.public_items))
        self.number_of_rows = id
        
    def is_mole(self, beta):
        """
        beta - insieme di attributi
        """
        k = self.Sup(beta)
        if k == 0:
            return False
        if k <= self.k:
            return True
        for e in self.private_items:
            if self.p_breach(beta, e, k) > self.h:
                return True
        return False

    def Sup(self, beta):
        k = 0
        for row in self.rows:
            if set(row.public).issuperset(beta):
                k += 1
        return k

    def p_breach(self, beta, private_item, k):
        """ Restituisce la probabilità che beta implichi private_item
        beta - insieme di attributi della beta-cohorte
        private_item - attributo privato
        k - Sup(beta)
        """
        temp_beta = beta[:]
        temp_beta.append(private_item)
        return self.Sup(temp_beta) / k

def main(**params):
    dataset = Table(**params)
        
    """brain storming"""

    C1 = dataset.public_items
    M1 = list()
    F1 = list() # non moli
    for e in C1:
        if dataset.is_mole([e]):
            M1.append([e])
        else:
            F1.append([e])

    F = [F1]
    M = [M1]
    del F1, M1, C1
    i = 0
    while i < dataset.p - 2 and len(F[i]) > 0:
        F_, M_ = foo(dataset, F[i], M[i])
        F.append(F_)
        M.append(M_)
        i += 1

    anonymized = True
    for possible_mole in M:
        if(len(possible_mole) != 0):
            print("Dataset is not anonymized, size -", len(possible_mole[0]), "moles: ", possible_mole)
            anonymized = False
    if anonymized:
        print("Il dataset è anonimzizato secondo i parametri:\n-) h: ", dataset.h, "\n-) k: ", dataset.k, "\n-) p: ", dataset.p)



if __name__ == "__main__":
    params = {
        'filename':'anonymized_dataset.dat',
        'n_items':129,
        'delta':0.5,
        'p':3,
        'h':0.4,
        'k':4
    }
    main(**params)