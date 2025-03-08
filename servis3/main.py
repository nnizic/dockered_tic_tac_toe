"""Servis Igrač O"""

import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

SIMBOL = "O"


class PoljeModel(BaseModel):
    polje: list


def ocijeni_polje(polje):
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
            return 1 if vrijednosti[0] == SIMBOL else -1
    return 0


def slobodna_polja(polje):
    """Vraća listu slobodnih polja na ploči"""
    return [(x, y) for x in range(3) for y in range(3) if polje[x][y] == " "]


def minimax(polje, dubina, max_igrac):
    """rekurzivna implementacija minimax algoritma"""
    ocjena = ocijeni_polje(polje)
    if ocjena != 0 or not slobodna_polja(polje):
        return ocjena
    if max_igrac:
        najbolja_vrijednost = -float("inf")
        for x, y in slobodna_polja(polje):
            polje[x][y] = SIMBOL
            vrijednost = minimax(polje, dubina + 1, False)
            polje[x][y] = " "
            najbolja_vrijednost = max(najbolja_vrijednost, vrijednost)
        return najbolja_vrijednost
    else:
        najbolja_vrijednost = float("inf")
        for x, y in slobodna_polja(polje):
            polje[x][y] = "X"
            vrijednost = minimax(polje, dubina + 1, True)
            polje[x][y] = " "
            najbolja_vrijednost = min(najbolja_vrijednost, vrijednost)
        return najbolja_vrijednost


def odigraj_minimax(polje):
    """Odabire najbolji potez pomoću minimax algoritma"""
    najbolji_potez = None
    najbolja_vrijednost = -float("inf")
    for x, y in slobodna_polja(polje):
        polje[x][y] = SIMBOL
        vrijednost = minimax(polje, 0, False)
        polje[x][y] = " "
        if vrijednost > najbolja_vrijednost:
            najbolja_vrijednost = vrijednost
            najbolji_potez = (x, y)
    potez = najbolji_potez if najbolji_potez else random.choice(slobodna_polja(polje))
    polje[potez[0]][potez[1]] = SIMBOL
    return polje


def odigraj_na_slobodno(polje):
    """postavlja O u prvo prazno polje"""
    for i in range(3):
        for j in range(3):
            if polje[i][j] == " ":
                polje[i][j] = SIMBOL

                return polje
    return polje


def odigraj_random(polje):
    """postavlja O u nasumično polje"""
    slobodna_polja = [(i, j) for i in range(3) for j in range(3) if polje[i][j] == " "]
    if slobodna_polja:
        i, j = random.choice(slobodna_polja)
        polje[i][j] = SIMBOL
    return polje


@app.post("/odigraj")
async def odigraj_potez(podaci: PoljeModel):
    """Prima trenutno stanje polja i vraća novo stanje ( nakon poteza )"""
    if random.random() < 0.2:  # dodaje 20% šanse da servis padne
        raise HTTPException(status_code=500, detail="Greška u servisu")
    polje = podaci.polje
    strategija = random.choice([odigraj_minimax, odigraj_random])
    polje = strategija(polje)

    return {"polje": polje}
