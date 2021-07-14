import random #per i numeri casuali
import matplotlib.pyplot as plt #per i grafici
import crypto #contiene tutti i metodi per criptare e decriptare, insieme alle liste dei bigrafi, trigrafi e delle parole più frequenti della lingua inglese
import time #per il tempo di esecuzione

import argparse #per passare argomenti da riga di comando

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= "A program which decrypts texts crypted with mono-alphabetic method (using gen algos)")
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
    """Prende una stringa e sostituisce tutti i caratteri che non sono uno spazio con un trattino - (serve per il fitness)"""
    l = list(text)
    for i in range(len(l)):
        if l[i] != " ":
            l[i] = "-"

    return "".join(l)

class GAException(Exception):
    pass


class Individual(list):
    """Gli individui sono permutazioni dell'alfabeto"""

    #il caching del fitness serve per la funzione che seleziona gli individui da sottoporre a crossover
    fitness = 0.

    def mate_modified_order(self, other, position=None):
        """Sceglie random una posizione e taglia i genitori lì. Le lettere del primo genitore a destra del taglio vengono cercate nel secondo genitore
        e vengono copiate nel figlio nell'ordine in cui compaiono nel primo genitore e nelle posizioni in cui compaiono nel secondo.
        I restanti buchi vengono riempiti prendendo le lettere dal secondo genitore nell'ordine e nella posizione in cui vi appaiono.
        Poi fa la stessa cosa scambiando i due genitori per generare l'altro figlio"""

        if position == None: #scelgo la posizione del taglio (può anche essere passata esplicitamente per il test)
            position = random.randint(0, len(self) - 1)

        son = other[:] #invece che riempire i buchi dopo, copio già tutte le lettere di other in son e sotto cambio quelli da cambiare
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

        return [Individual(son), Individual(daughter)]

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



def generate_population(nind, in_text, mode="normal", space=None):
    """Genera una popolazione iniziale di permutazioni dell'alfabeto; se il mapping dello spazio è già stato trovato dal codice,
    esso viene assegnato di default a tutti gli individui della popolazione iniziale"""

    pop = []

    if mode == "find_space":
        for i in range(nind):
            key = []
            alph = crypto.alphabet[:]
            for k in range(len(alph)):
                key.append(alph.pop(random.randint(0, len(alph) - 1)))
            indkey = Individual(key)
            pop.append(indkey)

    if mode == "normal":
        for i in range(nind):
            key = []
            alph = crypto.alphabet[:]
            alph.remove(space) #il mapping dello spazio che è stato trovato lo metto alla fine
            for k in range(len(alph)):
                key.append(alph.pop(random.randint(0, len(alph) - 1)))
            key.append(space) #metto il mapping dello spazio
            indkey = Individual(key)
            pop.append(indkey)

    return pop

def return_fitness(individual):

    return individual.fitness


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


def generate_new_population(in_pop, in_scores):
    """Genera una nuova popolazione facendo i crossover tra elementi di pop scelti in base agli score
    dopo aver passato i due migliori individui immutati (elitarietà)"""
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


def mutate_population(pop, mut_prob, text):
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

    #fase preliminare: cerco il mapping dello spazio
    print("Searching for the space...")
    pop = generate_population(nind, crypted, mode="find_space")
    scores = [i.get_fitness(crypted, decr=True, mode="find_space") for i in pop]

    for i in range(5):
        pop = generate_new_population(pop, scores)
        pop = mutate_population(pop, mut_prob, crypted)
        scores = [i.get_fitness(crypted, decr=True, mode="find_space") for i in pop]

    map_space = pop[0][len(pop[0]) - 1]

    print("Found! The space has been mapped to the letter:")
    print(map_space)
    print("---------------------------------")

    print("Generating starting population knowing the mapping of the space...")

    #genero la popolazione iniziale assegnando il mapping dello spazio trovato nella fase preliminare
    pop = generate_population(nind, crypted, space=map_space)

    print("Generated!")

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

    #preparo i grafici
    fig, ax = plt.subplots(1, 2)

    ax[0].set_xlim(-1, ngen)
    ax[0].set_ylim(0, 1)

    #qua inizia l'evoluzione della popolazione
    for i in range(ngen):
        #genero una nuova popolazione a partire dalla precedente
        pop = generate_new_population(pop, scores)

        #muto la popolazione
        pop = mutate_population(pop, mut_prob, crypted)

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
        ax[0].set_xlabel("Generation number")
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
    print("with the key:")
    print(pop[0])

    #calcolo e stampo il tempo di esecuzione
    t1 = time.time()
    t = t1 - t0
    print("Elapsed: %d" %t)

    plt.show()
