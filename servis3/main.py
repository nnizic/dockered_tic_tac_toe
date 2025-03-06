"""Servis Igrač O"""

import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

SIMBOL = "O"


class PoljeModel(BaseModel):
    polje: list


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
    strategija = random.choice([odigraj_na_slobodno, odigraj_random])
    polje = strategija(polje)

    return {"polje": polje}
