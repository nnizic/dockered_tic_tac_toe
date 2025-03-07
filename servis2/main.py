"""Servis Igrač X"""

import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

SIMBOL = "X"


class PoljeModel(BaseModel):
    polje: list


def odigraj_na_slobodno(polje):
    """postavlja X u prvo prazno polje"""
    for i in range(3):
        for j in range(3):
            if polje[i][j] == " ":
                polje[i][j] = SIMBOL

                return polje
    return polje


def odigraj_optimalno(polje):
    """prvo bira sredinu, onda kutove, onda random"""
    sredina = (1, 1)
    if polje[sredina[0]][sredina[1]] == " ":
        polje[sredina[0]][sredina[1]] = SIMBOL
        return polje
    kutovi = [(0, 0), (0, 2), (2, 0), (2, 2)]
    slobodni_kutovi = [pos for pos in kutovi if polje[pos[0]][pos[1]] == " "]
    if slobodni_kutovi:
        slobodni_kut = random.choice(slobodni_kutovi)
        polje[slobodni_kut[0]][slobodni_kut[1]] = SIMBOL
        return polje

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
    strategija = random.choice([odigraj_na_slobodno, odigraj_optimalno])
    polje = strategija(polje)

    return {"polje": polje}
