import unittest

import crypto

class Test_Crypto(unittest.TestCase): #testa il funzionamento dei metodi di criptazione e decriptazione contenuti in crypto.py

    def test_crypt_mono_shift(self):

        input = "ciao sono mattia"
        output = "fldrcvrqrcpdwwld"

        self.assertEqual(crypto.crypt_mono_shift(input, 3), output)

    def test_decrypt_mono_shift(self):

        input = "fldrcvrqrcpdwwld"
        output = "ciao sono mattia"

        self.assertEqual(crypto.decrypt_mono_shift(input, 3), output)


    def test_crypt_mono_permutation(self):
        #al = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', ' ']
        key = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m', ' ']
        input = "ciao sono mattia"
        output = "eoqg lgfg dqzzoq"

        self.assertEqual(crypto.crypt_mono_permutation(input, key), output)


    def test_decrypt_mono_permutation(self):

        #key = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m', ' ']
        #output = "ciao sono mattia"
        #input = "eoqg lgfg dqzzoq"

        output = "albert einstein was a germanborn theoretical physicist widely acknowledged to be one of the greatest physicists of all time einstein is known for developing the theory of relativity but he also made important contributions to the development of the theory of quantum mechanics relativity and quantum mechanics are together the two pillars of modern physics his massenergy equivalence formula which arises from relativity theory has been dubbed the worlds most famous equation his work is also known for its influence on the philosophy of science he received the nobel prize in physics for his services to theoretical physics and especially for his discovery of the law of the photoelectric effect a pivotal step in the development of quantum theory his intellectual achievements and originality resulted in einstein becoming synonymous with genius in nineteen zero five a year sometimes described as his miracle year einstein published four groundbreaking papers these outlined the theory of the photoelectric effect explained brownian motion introduced special relativity and demonstrated massenergy equivalence einstein thought that the laws of classical mechanics could no longer be reconciled with those of the electromagnetic field which led him to develop his special theory of relativity he then extended the theory to gravitational fields he published a paper on general relativity in nineteen sixteen introducing his theory of gravitation "

        input = "qcyefzxehrlzehrxtqlxqxnefmqrydfrxziedfezhuqcxaiplhuhlzxthsecpxqu rdtcesnesxzdxyexdrexdbxziexnfeqzelzxaiplhuhlzlxdbxqccxzhmexehrlzehrxhlx rdtrxbdfxsevecdahrnxziexziedfpxdbxfecqzhvhzpxyozxiexqcldxmqsexhmadfzqrzxudrzfhyozhdrlxzdxziexsevecdamerzxdbxziexziedfpxdbxjoqrzomxmeuiqrhulxfecqzhvhzpxqrsxjoqrzomxmeuiqrhulxqfexzdneziefxziexztdxahccqflxdbxmdsefrxaiplhulxihlxmqllerefnpxejohvqceruexbdfmocqxtihuixqfhlelxbfdmxfecqzhvhzpxziedfpxiqlxyeerxsoyyesxziextdfcslxmdlzxbqmdolxejoqzhdrxihlxtdf xhlxqcldx rdtrxbdfxhzlxhrbcoeruexdrxziexaihcdldaipxdbxluheruexiexfeuehvesxziexrdyecxafhgexhrxaiplhulxbdfxihlxlefvhuelxzdxziedfezhuqcxaiplhulxqrsxelaeuhqccpxbdfxihlxshludvefpxdbxziexcqtxdbxziexaidzdeceuzfhuxebbeuzxqxahvdzqcxlzeaxhrxziexsevecdamerzxdbxjoqrzomxziedfpxihlxhrzecceuzoqcxquihevemerzlxqrsxdfhnhrqchzpxfeloczesxhrxehrlzehrxyeudmhrnxlprdrpmdolxthzixnerholxhrxrhrezeerxgefdxbhvexqxpeqfxldmezhmelxselufhyesxqlxihlxmhfqucexpeqfxehrlzehrxaoychliesxbdofxnfdorsyfeq hrnxaqaeflxzielexdozchresxziexziedfpxdbxziexaidzdeceuzfhuxebbeuzxewacqhresxyfdtrhqrxmdzhdrxhrzfdsouesxlaeuhqcxfecqzhvhzpxqrsxsemdrlzfqzesxmqllerefnpxejohvqceruexehrlzehrxzidonizxziqzxziexcqtlxdbxucqllhuqcxmeuiqrhulxudocsxrdxcdrnefxyexfeudruhcesxthzixzidlexdbxziexeceuzfdmqnrezhuxbhecsxtihuixcesxihmxzdxsevecdaxihlxlaeuhqcxziedfpxdbxfecqzhvhzpxiexzierxewzersesxziexziedfpxzdxnfqvhzqzhdrqcxbhecslxiexaoychliesxqxaqaefxdrxnerefqcxfecqzhvhzpxhrxrhrezeerxlhwzeerxhrzfdsouhrnxihlxziedfpxdbxnfqvhzqzhdrx"

        key = ['q', 'y', 'u', 's', 'e', 'b', 'n', 'i', 'h', 'k', ' ', 'c', 'm', 'r', 'd', 'a', 'j', 'f', 'l', 'z', 'o', 'v', 't', 'w', 'p', 'g', 'x']

        self.assertEqual(crypto.decrypt_mono_permutation(input, key), output)


    def test_crypt_poli(self):

        keyword = "leclerc"
        input = "ciao sono mattia"
        #key =  "leclercleclercle"
        output = "nmczdiqysbxejvte"

        self.assertEqual(crypto.crypt_poli(input, keyword), output)


    def test_decrypt_poli(self):

        keyword = "leclerc"
        output = "ciao sono mattia"
        #key =  "leclercleclercle"
        input = "nmczdiqysbxejvte"

        self.assertEqual(crypto.decrypt_poli(input, keyword), output)









if __name__ == '__main__':
    unittest.main()
