import random


def odigraj_na_optimalno(polje, _):
    """igra u sredinu, ako ne može, onda traži kutove, ako ni to ne može onda random"""
    sredisnje = (1, 1)
    if polje[sredisnje[0]][sredisnje[1]] == " ":
        return sredisnje

    kutovi = [(0, 0), (0, 2), (2, 0), (2, 2)]
    slobodni_kutovi = [pos for pos in kutovi if polje[pos[0]][pos[1]] == " "]
    if slobodni_kutovi:
        return random.choice(slobodni_kutovi)

    slobodna_polja = [(x, y) for x in range(3) for y in range(3) if polje[x][y] == " "]
    return random.choice(slobodna_polja)
