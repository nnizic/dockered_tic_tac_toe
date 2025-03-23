import random

from pydantic import BaseModel


class PoljeModel(BaseModel):
    polje: list
    simbol: str  # X ili O


def ocijeni_polje(polje, simbol):
    """Provjerava ima li pobjednika u trenutnom stanju igre"""
    pobjednicke_kombinacije = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],  # redovi
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],  # stupci
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],  # dijagonale
    ]
    for kombinacija in pobjednicke_kombinacije:
        vrijednosti = [polje[x][y] for x, y in kombinacija]
        if vrijednosti[0] != " " and vrijednosti.count(vrijednosti[0]) == 3:
            return 1 if vrijednosti[0] == simbol else -1
    return 0


def slobodna_polja(polje):
    """Vraća listu slobodnih polja na ploči"""
    return [(x, y) for x in range(3) for y in range(3) if polje[x][y] == " "]


def minimax(polje, dubina, max_igrac=False, simbol="X"):
    """rekurzivna implementacija minimax algoritma"""
    ocjena = ocijeni_polje(polje, simbol)

    if ocjena != 0 or not slobodna_polja(polje):
        return ocjena
    if max_igrac:
        najbolja_vrijednost = -float("inf")
        for x, y in slobodna_polja(polje):
            polje[x][y] = simbol
            vrijednost = minimax(polje, dubina + 1, False, simbol)
            polje[x][y] = " "
            najbolja_vrijednost = max(najbolja_vrijednost, vrijednost)
        return najbolja_vrijednost
    else:
        najbolja_vrijednost = float("inf")
        for x, y in slobodna_polja(polje):
            polje[x][y] = "X"
            vrijednost = minimax(polje, dubina + 1, True, simbol)
            polje[x][y] = " "
            najbolja_vrijednost = min(najbolja_vrijednost, vrijednost)
        return najbolja_vrijednost


def odigraj_minimax(polje, simbol):
    """Odabire najbolji potez pomoću Minimax algoritma"""
    najbolji_potez = None
    najbolja_vrijednost = -float("inf")

    for x, y in slobodna_polja(polje):
        polje[x][y] = simbol
        vrijednost = minimax(polje, 0, False, simbol)
        polje[x][y] = " "
        if vrijednost > najbolja_vrijednost:
            najbolja_vrijednost = vrijednost
            najbolji_potez = (x, y)

    return najbolji_potez
