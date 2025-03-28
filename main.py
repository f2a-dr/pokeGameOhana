#!/usr/bin/env python3

import numpy as np
import yaml


def readFile(filename):
    with open(filename) as f:
        scores = yaml.load(f, Loader=yaml.FullLoader)
    return scores


def scoreCalculator():
    cardScores = {'olo': 0.5, 'ex': 1, 'FA': 1, 'exFA': 2, 'shiny': 1, 'shiny-ex':2, 'immersive': 3, 'gold':5,}
    scoreBusta = 0
    penalty = input('Sono stati trovati dei doppioni di carte comuni?[y/n] ')
    if penalty == 'yes' or penalty == 'y' or penalty == 'Yes' or penalty == 'Y':
        malus = input('Quanti punti devono essere tolti? (inserire valore assoluto) ')
        scoreBusta -= float(malus)
    elif penalty == 'no' or penalty == 'n' or penalty == 'No' or penalty == 'N':
        pass
    else:
        print('ERRORE: inserire `yes` o `no`.')
        return None
    rareFlag = input('Sono stati trovate carte rare?[y/n] ')
    if rareFlag == 'yes' or rareFlag == 'y' or rareFlag == 'Yes' or rareFlag == 'Y':
        rareCards = input('Inserire le tipologie di carte rare, separate da una virgola:\nPossibili tipologie {}\n'.format([i for i in cardScores]))
        rareCards = rareCards.split(',')
        rareCards = [i.strip() for i in rareCards]
        if len(rareCards) > 5:
            print('Hai inserito più di 5 carte, stai provando a fare il furbo?')
            return None
        for i in rareCards:
            if not(i in cardScores):
                print('ERRORE: {} non è una tipologia di carta.'.format(i))
                return None
        doubleFlag = input('Le carte rare trovate sono tutte nuove?[y/n] ' )
        if doubleFlag == 'yes' or doubleFlag == 'y' or doubleFlag == 'Yes' or doubleFlag == 'Y':
            doubleCards = [1 for i in rareCards]
        elif doubleFlag == 'no' or doubleFlag == 'n' or doubleFlag == 'No' or doubleFlag == 'N':
            doubleCards = input("Per ogni carta rara, inserire `yes` se è un doppione, `no` se non lo è separati da una virgola:\nÈ importante rispettare l'ordine delle carte rare inserite precedentemente\n")
            doubleCards = doubleCards.split(',')
            doubleCards = [i.strip() for i in doubleCards]
            if len(doubleCards) != len(rareCards):
                print('ERRORE: il numero di carte rare non corrisponde con il numero di `yes` e `no` inseriti')
                return None
            for i in range(len(doubleCards)):
                if not(doubleCards[i] == 'yes') and not(doubleCards[i] == 'no'):
                    print('ERRORE: formato errato, inserire `yes` o `no` separati da virgole per ogni carta rara')
                    return None
                doubleCards[i] = 1 if doubleCards[i] == 'no' else 0.5
        else:
            print('ERRORE: inserire `yes` o `no`.')
            return None
        for i in range(len(rareCards)):
            scoreBusta += cardScores[rareCards[i]]*doubleCards[i]
    elif rareFlag == 'no' or rareFlag == 'n' or rareFlag == 'No' or rareFlag == 'N':
        pass
    else:
        print('ERRORE: inserire `yes` o `no`.')
        return None
    return scoreBusta

def printScores(filename):
    scores = readFile(filename)
    print()
    print ('{:>15} {:^10} {:^10} {:^16}'.format('', 'Buste', 'Punti', 'Punti per busta'))
    for i in range(len(scores['players'])):
        name = scores['players'][i]['name']
        points = scores['players'][i]['score']
        count = scores['players'][i]['count']
        print('{:>15} {:^10} {:^10} {:^16.2}'.format(name, count, points, points/count))
    return None

def addScore(filename):
    scores = readFile(filename)
    names = [scores['players'][i]['name'] for i in range(len(scores['players']))]
    nameSbusto= input('Chi ha sbustato?\nPossibili nomi (attenzione alle maiuscole) {}\n'.format(names))
    if nameSbusto not in names:
        print('ERRORE: {} non è un giocatore.'.format(nameSbusto))
        return None
    else:
        positionSbusto = names.index(nameSbusto)
        scoreSbusto = scoreCalculator()
        if scoreSbusto == None:
            print('ERRORE: i dati dello sbusto non sono stati inseriti correttamente.')
            return None
        else:
            scores['players'][positionSbusto]['count'] += 1
            scores['players'][positionSbusto]['score'] += scoreSbusto
            with open(filename, 'w') as f:
                yaml.dump(scores, f)
    return None

if __name__ == '__main__':

    filename = "scores.yaml"

    add = input("Vuoi inserire uno sbusto?[y/N] ")
    if add == '' or add == 'n' or add == 'no' or add == 'No' or add == 'N':
        add = False
        show = input("Vuoi vedere i punteggi?[Y/n] ")
        if show == '' or show == 'y' or show == 'yes' or show == 'Yes' or show == 'Y':
            printScores(filename)
        elif show == 'n' or show == 'no' or show == 'No' or show == 'N':
            print("Non c'è altro da fare. Bye bye")
    elif add == 'y' or add == 'yes' or add == 'Yes' or add == 'Y':
        add = True
        addScore(filename)
        print("Per favore, dopo aver inserito uno sbusto ricorda di fare commit e push per tenere aggiornato il file dei punteggi")
    else:
        print('ERRORE: inserire `yes` o `no`.')
