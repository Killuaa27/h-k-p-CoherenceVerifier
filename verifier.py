#!/usr/bin/env python3

from collections import Counter
import csv
import itertools
import random

random.seed(42)

class Row:

    def __init__(self, id, row_pub, row_priv, public_items, private_items):
        self.id = id
        self.private = list() # private items
        self.public = list() # public items
        for item in row_pub:
            item = int(item)
            self.public.append(item)
            public_items.add(item)
        for item in row_priv:
            item = int(item)
            self.private.append(item)
            private_items.add(item)

    def delete_item(self, item):
        """Rimuove l'elemento passato dalla riga"""
        try:
            self.public.remove(item)
        except ValueError:
            pass

    def __repr__(self):
        return str(self.id)


class Table:

    def __init__(self, pub, priv, p, h, k):
        """
        pub - dataset with public items
        priv - dateset with private items
        p - numero massimo attributi conosciuti
        h - max probabilità che una transazione contenga 1 dato privato
        k - numero min di transazioni per ogni sottoinsieme di attributi pubblici conosciuti
        """
        self.p = p
        self.h = h
        self.k = k
        public_items = set()
        private_items = set()
        self.rows = list()
        with open(pub, "r") as dataset_pub:
            csv_pub = csv.reader(dataset_pub, delimiter=' ')            
            with open(priv, "r") as dateset_priv:
                csv_priv = csv.reader(dataset_priv, delimiter=' ')
                id = 0
                for row_pub, row_priv in zip(csv_pub, csv_priv):
                    id += 1
                    self.rows.append(Row(id, row_pub, row_priv, public_items, private_items))
        self.number_of_rows = id
        self.public_items = list(public_items)
        self.private_items = list(private_items)
        
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

def main(args):
    dataset = Table(args.pub, args.priv, args.p, args.h, args.k)
        
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
    import argparse

    parser = argparse.ArgumentParser(description='h-k-p-CoherenceVerifier')
    parser.add_argument('-pub', type=str, required=True, help='dataset with public items', metavar='filepath')
    parser.add_argument('-priv', type=str, required=True, help='dataset with private items', metavar='filepath')
    parser.add_argument('-p', type=int, required=True, help='', metavar='integer')
    parser.add_argument('-h', type=float, required=True, help='', metavar='percentage')
    parser.add_argument('-k', type=int, required=True, help='', metavar='integer')
    
    args = parser.parse_args()
    
    main(args)