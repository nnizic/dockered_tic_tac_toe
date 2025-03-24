import random


def odigraj_na_prvo_slobodno_polje(polje, _):
    for i in range(3):
        for j in range(3):
            if polje[i][j] == " ":
                return i, j
