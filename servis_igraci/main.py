import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from strategije import (
    strategija_blokiranje,
    strategija_minimax,
    strategija_optimalni,
    strategija_random,
)


app = FastAPI()


# Model za primanje podataka
class PotezRequest(BaseModel):
    polje: list[list[str]]
    simbol: str  # "X" ili "O"


# Mapiranje strategija
strategije_x = [
    strategija_random.odigraj_na_prvo_slobodno_polje,
    strategija_optimalni.odigraj_na_optimalno,
    strategija_blokiranje.odigraj_ako_mogu_pobjediti,
]
strategije_o = [
    strategija_random.odigraj_na_prvo_slobodno_polje,
    strategija_minimax.odigraj_minimax,
    strategija_blokiranje.odigraj_ako_mogu_pobjediti,
]


@app.post("/odigraj")
async def odigraj_potez(potez: PotezRequest):
    if random.random() < 0.2:  # dodaje 20% šanse da servis pukne
        raise HTTPException(status_code=500, detail="Greška u servisu")
    if potez.simbol == "X":
        strategija = random.choice(strategije_x)
    else:
        strategija = random.choice(strategije_o)

    x, y = strategija(potez.polje, potez.simbol)
    potez.polje[x][y] = potez.simbol

    return {"polje": potez.polje, "strategija": strategija.__name__}
