import random #per i numeri casuali
import matplotlib.pyplot as plt #per i grafici
import crypto #contiene tutti i metodi per criptare e decriptare, insieme alle liste dei bigrafi, trigrafi e delle parole più frequenti della lingua inglese
import time #per il tempo di esecuzione

import argparse #per passare argomenti da riga di comando

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "A program which decrypts texts crypted with poli-alphabetic method with unknown key length (using gen algos)")
    parser.add_argument('filename', help="Input (crypted) Text", type = str)
    parser.add_argument('nind', help="Number of individuals per population (suggested: 1500)", type = int)
    parser.add_argument('ngen', help="Number of generations (suggested: 100)", type = int)
    parser.add_argument('mut_prob', help="Mutation probability (suggested: 0.05)", type = float)

    args = parser.parse_args()

    filename = args.filename
    nind = args.nind
    ngen = args.ngen
    mut_prob = args.mut_prob

class GAException(Exception):
    pass

class Individual(list):
    """Ogni individuo è una chiave di cifratura di lunghezza variabile tra 4 e 15 lettere"""

    def mate(self, other, crossover=None):
        """Fa il crossover a un punto con un altro individuo"""

        if crossover == None:
            crossover = random.randint(0, len(self) - 1)

        return [Individual(self[:crossover] + other[crossover:]),
               Individual(other[:crossover] + self[crossover:])]

    def mutate(self, mut_prob, position=None):
        """La mutazione è implementata come la sostituzione di una lettera della chiave con una lettera casuale dell'alfabeto"""

        if random.random() < mut_prob:
            if position == None:
                position = random.randint(0, len(self) - 1)

            self[position] = crypto.alphabet[random.randint(0, len(crypto.alphabet) - 1)]

    def decrypt(self, text):
        return crypto.decrypt_poli(text, self)

    def get_fitness(self, text, decr=False):
        """Il fitness è calcolato contando i bigrafi, trigrafi e le parole più frequenti della lingua inglese
        contenuti nel testo decriptato usando se stessi come chiave"""

        if decr == True: #questa opzione serviva quando nei run di prova calcolavo anche lo score del testo orginale (non criptato)
            text = self.decrypt(text)

        n = sum([text.count(crypto.bigraphs[i]) for i in range(len(crypto.bigraphs) - 10)])
        m = sum([text.count(crypto.trigraphs[i]) for i in range(len(crypto.trigraphs))])
        r = sum([text.count(crypto.doubles[i]) for i in range(len(crypto.doubles))])
        j = sum([text.count(crypto.word1[i]) for i in range(len(crypto.word1))])
        h = sum([text.count(crypto.word2[i]) for i in range(len(crypto.word2) - 10)])
        k = sum([text.count(crypto.word3[i]) for i in range(len(crypto.word3) - 20)])
        l = sum([text.count(crypto.word4[i]) for i in range(len(crypto.word4) - 5)])

        return (n+m+r) + (h+k+l+j)*3 #le parole pesano di più dei bigrafi e trigrafi


def generate_population(nind):
    """Genera una popolazione iniziale di nind individui chiave di lunghezza casuale tra 4 e 15 lettere;
    tutte le liste sono di 15 caratteri, quelli che non sono lettere vengono posti uguali a trattini"""

    pop = []

    for i in range(nind):
        key = []
        length = random.randint(4, 15)
        for k in range(length):
            key.append(crypto.alphabet[random.randint(0, len(crypto.alphabet) - 1)])
        for k in range(15 - length):
            key.append("-")
        pop.append(Individual(key))

    return pop



def weighted_sample(in_pop, in_scores, n):
    """Restituisce n elementi distinti della in_pop con probabilità data dagli in_scores"""

    if n > len(in_pop) or n<0:
        raise GAException('Not valid n: %d' % n)

    chosen = []

    pop = in_pop[:]
    scores = in_scores[:]

    for i in range(n):
        totscore = sum(scores)
        r = random.random()
        tot = 0
        for j, s in enumerate(scores):
            tot += s / float(totscore)
            if tot > r:
                break
        chosen.append(pop.pop(j))
        scores.pop(j)

    return chosen



def generate_new_population(pop, scores):
    """Genera una nuova popolazione facendo i crossover tra elementi di pop scelti in base agli score
    dopo aver passato i due migliori individui immutati (elitarietà)"""
    new_pop = []

    maximum = 0
    posmax = 0

    for i in range(len(scores)):
        if scores[i] > maximum:
            maximum = scores[i]
            posmax = i

    best1 = pop[posmax]
    new_pop.append(best1)
    pop.pop(posmax)
    scores.pop(posmax)

    maximum = 0
    posmax = 0

    for i in range(len(scores)):
        if scores[i] > maximum:
            maximum = scores[i]
            posmax = i

    best2 = pop[posmax]
    new_pop.append(best2)

    pop.append(best1)

    for i in range(int(len(pop)/2) - 1):
        parent1, parent2 = weighted_sample(pop, scores, 2)
        new_pop.extend(parent1.mate(parent2))

    return new_pop


def mutate_population(pop, mut_prob):
    """Esegue mutate su tutti gli elementi della popolazione"""
    new_pop = []
    new_pop.append(pop[0])
    new_pop.append(pop[1])
    for i in range(2, len(pop), 1):
        pop[i].mutate(mut_prob)
        new_pop.append(pop[i])

    return new_pop



# ---------------- MAIN -------------- #

if __name__ == '__main__':

    t0 = time.time()

    #leggo il testo criptato passato da riga di comando
    file = open(filename)
    crypted = file.read()
    file.close()

    #genero la popolazione iniziale
    pop = generate_population(nind)

    #creo e inizio a riempire quello che stamperò
    avg_list = []
    max_list = []
    min_list = []

    x_list = []

    scores = [i.get_fitness(crypted, decr=True) for i in pop]

    avg_list.append(sum(scores)/float(len(scores)))
    max_list.append(max(scores))
    min_list.append(min(scores))

    x_list.append(-1)

    fig, ax = plt.subplots(1, 2)

    #preparo i grafici
    ax[0].set_xlim(-1, ngen)
    ax[0].set_ylim(0, max(scores)*3)

    #qua inizia l'evoluzione della popolazione
    for i in range(ngen):
        #genero una nuova popolazione a partire dalla precedente
        pop = generate_new_population(pop, scores)

        #muto la popolazione
        pop = mutate_population(pop, mut_prob)

        #calcolo gli score della nuova popolazione ottenuta
        scores = [i.get_fitness(crypted, decr=True) for i in pop]

        #aggiungo gli score della popolazione (massimo, minimo e medio) alle liste create prima per poi graficarle
        avg_list.append(sum(scores)/float(len(scores)))
        max_list.append(max(scores))
        min_list.append(min(scores))

        x_list.append(i)

        #grafico dell'evoluzione degli score in funzione del numero di generazioni
        ax[0].clear()
        ax[0].plot(x_list, min_list, label='Worst', color='blue')
        ax[0].plot(x_list, max_list, label='Best', color='red')
        ax[0].plot(x_list, avg_list, label='Average', color='green')
        ax[0].set_xlabel("Generation Number")
        ax[0].set_ylabel("Score")
        ax[0].set_title("Best, Worst and Average evolution")
        ax[0].legend()

        #istogramma degli score della popolazione
        ax[1].clear()
        ax[1].hist(scores, bins = 30)
        ax[1].set_xlabel("Score")
        ax[1].set_title("All Individual Scores Distribution")

        plt.draw()
        plt.pause(0.01)

    #stampo a terminale la soluzione: testo decriptato e chiave utilizzata per decriptarlo; data l'elitarietà
    #il primo elemento della popolazione è quello con score migliore
    print("Decrypted text:")
    print(pop[0].decrypt(crypted))
    for i in range(pop[0].count("-")):
        pop[0].remove("-") #tolgo i trattini per pulizia visiva
    print("with the key:")
    print(pop[0])

    #calcolo e stampo il tempo di esecuzione
    t1 = time.time()
    t = t1 - t0
    print("Elapsed: %d" %t)

    plt.show()
