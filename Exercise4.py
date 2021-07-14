import random #per i numeri casuali
import matplotlib.pyplot as plt #per i grafici
import crypto #contiene tutti i metodi per criptare e decriptare, insieme alle liste dei bigrafi, trigrafi e delle parole più frequenti della lingua inglese
import time #per il tempo di esecuzione

import argparse #per passare argomenti da riga di comando

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "A program which decrypts texts crypted with unknown method (using gen algos)")
    parser.add_argument('filename', help="Input (crypted) Text", type = str)
    parser.add_argument('nind', help="Number of individuals per population (suggested: 1500)", type = int)
    parser.add_argument('ngen', help="Number of generations (suggested: 100)", type = int)
    parser.add_argument('mut_prob', help="Mutation probability (suggested: 0.05)", type = float)

    args = parser.parse_args()

    filename = args.filename
    nind = args.nind
    ngen = args.ngen
    mut_prob = args.mut_prob

def convert(text):
    l = list(text)
    for i in range(len(l)):
        if l[i] != " ":
            l[i] = "-"

    return "".join(l)


class GAException(Exception):
    pass

class Individual_key(list):
    """Per la crittografia poli-alfabetica: ogni individuo è una chiave di cifratura di lunghezza variabile tra 4 e 15 lettere"""

    def mate(self, other, crossover=None):
        """Fa il crossover a un punto con un altro individuo"""

        if crossover == None:
            crossover = random.randint(0, len(self) - 1)

        return [Individual_key(self[:crossover] + other[crossover:]),
               Individual_key(other[:crossover] + self[crossover:])]

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





class Individual_perm(list):
    """Per la crittografia mono-alfabetica: gli individui sono permutazioni dell'alfabeto"""

    #il caching del fitness serve per la funzione che seleziona gli individui da sottoporre a crossover
    fitness = 0.

    def mate_modified_order(self, other, position=None):
        """Sceglie random una posizione e taglia i genitori lì. Le lettere del primo genitore a destra del taglio vengono cercate nel secondo genitore
        e vengono copiate nel figlio nell'ordine in cui compaiono nel primo genitore e nelle posizioni in cui compaiono nel secondo.
        I restanti buchi vengono riempiti prendendo le lettere dal secondo genitore nell'ordine e nella posizione in cui vi appaiono.
        Poi fa la stessa cosa scambiando i due genitori per generare l'altro figlio"""

        if position == None: #scelgo la posizione del taglio (può anche essere passata esplicitamente per il test)
            position = random.randint(0, len(self) - 1)

        son = other[:] #invece che riempire i buchi dopo, copio già tutte le lettere di other in son e sotto cambio quelle da cambiare
        index = 0
        for s in range(len(self)): #cerco in other le lettere a destra del taglio in self; quando trovo corrispondenza le copio in son nell'ordine di self
            for k in range(int(len(self) - 1 - position)):
                if other[s] == self[position + 1 + k]:
                    son[s] = self[index + position + 1]
                    index += 1

        #faccio la stessa cosa scambiando i genitori per generare il secondo figlio
        daughter = self[:]
        index = 0
        for s in range(len(self)):
            for k in range(int(len(self) - 1 - position)):
                if self[s] == other[position + 1 + k]:
                    daughter[s] = other[index + position + 1]
                    index += 1

        return [Individual_perm(son), Individual_perm(daughter)]

    def decrypt(self, text):
        return crypto.decrypt_mono_permutation(text, self)

    def mutate(self, mut_prob, text, positions=None):
        """La mutazione è implementata come lo scambio di due lettere nella chiave"""

        if random.random() < mut_prob:
            if positions == None:
                pos1 = random.randint(0, len(self) - 1)
                pos2 = random.randint(0, len(self)- 1)
                while pos2 == pos1:
                    pos2 = random.randint(0, len(self) - 1)
            else:
                pos1 = positions[0]
                pos2 = positions[1]

            a = self[pos1]
            b = self[pos2]

            self[pos2] = a
            self[pos1] = b

            self.fitness = self.get_fitness(text, decr = True)



    def get_fitness(self, text, decr=False, mode="normal"):
        """Il fitness è calcolato contando i bigrafi, trigrafi e le parole più frequenti della lingua inglese
        contenuti nel testo decriptato usando se stessi come chiave; c'è la possibilità di chiamare la funzione in due
        modalità, una serve a trovare il mapping dello spazio e l'altra è per l'evoluzione della popolazione"""

        if decr == True: #questa opzione serviva quando nei run di prova calcolavo anche lo score del testo orginale (non criptato)
            text = self.decrypt(text)

        n = sum([text.count(crypto.bigraphs[i]) for i in range(len(crypto.bigraphs) - 10)])
        m = sum([text.count(crypto.trigraphs[i]) for i in range(len(crypto.trigraphs))])
        r = sum([text.count(crypto.doubles[i]) for i in range(len(crypto.doubles))])
        j = sum([text.count(crypto.word1[i]) for i in range(len(crypto.word1))])
        h = sum([text.count(crypto.word2[i]) for i in range(len(crypto.word2) - 10)])
        k = sum([text.count(crypto.word3[i]) for i in range(len(crypto.word3) - 20)])
        l = sum([text.count(crypto.word4[i]) for i in range(len(crypto.word4) - 5)])

        if mode == "find_space":
            text = convert(text)
            f = text.count(" -------------------------") #conta quante parole lunghe ci sono nel testo decriptato
            n_space = text.count(" ") #conta quanti spazi ci sono nel testo decriptato

            fit = (n+m+r) + (h+k+l+j)*3 - f*200 #le parole pesano di più dei bigrafi e trigrafi, malus se ci sono parole lunghe

            if n_space == 0:
                fit = 0. #se nel testo decriptato non ci sono spazi, lo score è posto a zero
            if fit < 0:
                fit = 0.

        if mode == "normal":
            fit = (n+m+r) + (h+k+l+j)*3 #le parole pesano di più dei bigrafi e trigrafi

        self.fitness = fit

        return fit


def generate_population_key(nind):
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
        pop.append(Individual_key(key))

    return pop


def generate_population_perm(nind, in_text, mode="normal", space=None):
    """Genera una popolazione iniziale di permutazioni dell'alfabeto; se il mapping dello spazio è già stato trovato dal codice,
    esso viene assegnato di default a tutti gli individui della popolazione iniziale"""

    pop = []

    if mode == "find_space":
        for i in range(nind):
            key = []
            alph = crypto.alphabet[:]
            for k in range(len(alph)):
                key.append(alph.pop(random.randint(0, len(alph) - 1)))
            indkey = Individual_perm(key)
            pop.append(indkey)

    if mode == "normal":
        for i in range(nind):
            key = []
            alph = crypto.alphabet[:]
            alph.remove(space) #il mapping dello spazio che è stato trovato lo metto alla fine
            for k in range(len(alph)):
                key.append(alph.pop(random.randint(0, len(alph) - 1)))
            key.append(space) #metto il mapping dello spazio
            indkey = Individual_perm(key)
            pop.append(indkey)

    return pop

def return_fitness(individual):

    return individual.fitness


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


def choose(in_pop):
    """Sceglie due elementi della in_pop ordinandoli per score crescente e poi estraendo due numeri casuali tra 0 e la lunghezza della popolazione
    distribuiti come 6x^5, in modo da sbilanciare la selezione verso gli individui di score più alto"""

    pop = in_pop[:]

    pop.sort(key=return_fitness)

    i = int(len(pop) * (random.random() ** (1./6.)))
    j = int(len(pop) * (random.random() ** (1./6.)))
    while j == i:
        j = int(len(pop) * (random.random() ** (1./6.)))

    return pop[i], pop[j]


def generate_new_population_key(pop, scores):
    """Genera una nuova popolazione facendo i crossover tra elementi di pop scelti in base agli score
    (usando weighted sample) dopo aver passato i due migliori individui immutati (elitarietà)"""
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


def generate_new_population_perm(in_pop, in_scores):
    """Genera una nuova popolazione facendo i crossover tra elementi di pop scelti in base agli score
    (usando choose) dopo aver passato i due migliori individui immutati (elitarietà)"""
    new_pop = []
    scores = in_scores[:]
    pop = in_pop[:]

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
        parent1, parent2 = choose(pop)
        new_pop.extend(parent1.mate_modified_order(parent2))

    return new_pop


def mutate_population_key(pop, mut_prob):
    """Esegue mutate su tutti gli elementi della popolazione"""
    new_pop = []
    new_pop.append(pop[0])
    new_pop.append(pop[1])
    for i in range(2, len(pop), 1):
        pop[i].mutate(mut_prob)
        new_pop.append(pop[i])

    return new_pop

def mutate_population_perm(pop, mut_prob, text):
    """Esegue mutate su tutti gli elementi della popolazione"""
    new_pop = []
    new_pop.append(pop[0])
    new_pop.append(pop[1])
    for i in range(2, len(pop), 1):
        pop[i].mutate(mut_prob, text)
        new_pop.append(pop[i])

    return new_pop



# ---------------- MAIN -------------- #

if __name__ == '__main__':

    t0 = time.time()

    #leggo il testo criptato passato da riga di comando
    file = open(filename)
    crypted = file.read()
    file.close()

    #genero la popolazione di individui chiave
    pop_key = generate_population_key(nind)

    #cerco il mapping ndello spazio nel caso in cui il metodo usato sia quello della permutazione
    print("Searching for the space (needed if it's permutation method)...")

    pop_perm = generate_population_perm(nind, crypted, mode="find_space")

    scores_perm = [i.get_fitness(crypted, decr=True, mode="find_space") for i in pop_perm]

    for i in range(5):
        pop_perm = generate_new_population_perm(pop_perm, scores_perm)

        pop_perm = mutate_population_perm(pop_perm, mut_prob, crypted)

        scores_perm = [i.get_fitness(crypted, decr=True, mode="find_space") for i in pop_perm]

    map_space = pop_perm[0][len(pop_perm[0]) - 1]

    print("Found! The space has been mapped to the letter:")
    print(map_space)
    print("---------------------------------")

    #genero la popolazione di individui permutazione sapendo il mapping dello spazio
    pop_perm = generate_population_perm(nind, crypted, space=map_space)

    #creo e inizio a riempire quello che stamperò
    avg_list_key = []
    max_list_key = []
    min_list_key = []

    avg_list_perm = []
    max_list_perm = []
    min_list_perm = []

    x_list_key = []
    x_list_perm = []

    scores_key = [i.get_fitness(crypted, decr=True) for i in pop_key]
    scores_perm = [i.get_fitness(crypted, decr=True) for i in pop_perm]

    avg_list_key.append(sum(scores_key)/float(len(scores_key)))
    max_list_key.append(max(scores_key))
    min_list_key.append(min(scores_key))

    avg_list_perm.append(sum(scores_perm)/float(len(scores_perm)))
    max_list_perm.append(max(scores_perm))
    min_list_perm.append(min(scores_perm))

    x_list_key.append(-1)
    x_list_perm.append(-1)

    fig, ax = plt.subplots(1, 2)

    #preparo i grafici
    ax[0].set_xlim(-1, ngen)
    ax[0].set_ylim(0, max(scores_key)*3)
    ax[1].set_xlim(-1, ngen)
    ax[1].set_ylim(0, max(scores_perm)*3)

    #variabili che servono per fermare la popolazione che sta andando male (quella del metodo sbagliato)
    stopped = False
    cont = "aaa"

    #comincia l'evoluzione delle due popolazioni
    for i in range(ngen):
        if cont != "perm": #evoluzione della popolazione chiave
            pop_key = generate_new_population_key(pop_key, scores_key)
            pop_key = mutate_population_key(pop_key, mut_prob)
            scores_key = [i.get_fitness(crypted, decr=True) for i in pop_key]
            avg_list_key.append(sum(scores_key)/float(len(scores_key)))
            max_list_key.append(max(scores_key))
            min_list_key.append(min(scores_key))
            x_list_key.append(i)
            ax[0].clear()
            ax[0].plot(x_list_key, min_list_key, label='Worst', color='blue')
            ax[0].plot(x_list_key, max_list_key, label='Best', color='red')
            ax[0].plot(x_list_key, avg_list_key, label='Average', color='green')
            ax[0].set_xlabel("Generation number")
            ax[0].set_ylabel("Score")
            ax[0].set_title("Key method")
            ax[0].legend()

        if cont != "key": #evoluzione della popolazione permutazione
            pop_perm = generate_new_population_perm(pop_perm, scores_perm)
            pop_perm = mutate_population_perm(pop_perm, mut_prob, crypted)
            scores_perm = [i.get_fitness(crypted, decr=True) for i in pop_perm]
            avg_list_perm.append(sum(scores_perm)/float(len(scores_perm)))
            max_list_perm.append(max(scores_perm))
            min_list_perm.append(min(scores_perm))
            x_list_perm.append(i)
            ax[1].clear()
            ax[1].plot(x_list_perm, min_list_perm, label='Worst', color='blue')
            ax[1].plot(x_list_perm, max_list_perm, label='Best', color='red')
            ax[1].plot(x_list_perm, avg_list_perm, label='Average', color='green')
            ax[1].set_xlabel("Generation number")
            ax[1].set_ylabel("Score")
            ax[1].set_title("Permutation method")
            ax[1].legend()

        plt.draw()
        plt.pause(0.01)

        #dopo 10 generazioni, ad ogni generazione verifico se una delle due popolazioni ha score massimo maggiore
        #del massimo dell'altra, in tal caso cambio le variabili in modo tale che la popolazione scarsa si fermi
        #e quella buona prosegua fino a trovare il massimo
        if (i >= 10) and (stopped == False):
            if pop_key[0].get_fitness(crypted, decr=True) > 2*pop_perm[0].get_fitness(crypted, decr=True):
                stopped = True #così non entro più nella verifica
                cont = "key" #la popolazione che continua è quella chiave
                print("I killed the permutation population")
            if pop_perm[0].get_fitness(crypted, decr=True) > 2*pop_key[0].get_fitness(crypted, decr=True):
                stopped = True #così non entro più nella verifica
                cont = "perm" #la popolazione che continua è quella permutazione
                print("I killed the key population")

    #ora stampo la soluzione della popolazione che è sopravvissuta

    if pop_key[0].get_fitness(crypted, decr=True) > pop_perm[0].get_fitness(crypted, decr=True):
        print("The text has been crypted with the key method")
        print("Decrypted text:")
        print(pop_key[0].decrypt(crypted))
        for i in range(pop_key[0].count("-")):
            pop_key[0].remove("-") #tolgo i trattini per pulizia visiva
        print("with the key:")
        print(pop_key[0])

    if pop_key[0].get_fitness(crypted, decr=True) < pop_perm[0].get_fitness(crypted, decr=True):
        print("The text has been crypted with the permutation method")
        print("Decrypted text:")
        print(pop_perm[0].decrypt(crypted))
        print("with the permutation:")
        print(pop_perm[0])

    #calcolo e stampo il tempo di esecuzione
    t1 = time.time()
    t = t1-t0
    print("Elapsed: %d" %t)


    plt.show()
