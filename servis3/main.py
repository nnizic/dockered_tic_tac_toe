"""Servis 3 (Igrač O)"""

import random

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PoljeModel(BaseModel):
    polje: list


@app.post("/odigraj")
async def odigraj_potez(podaci: PoljeModel):
    """Igrač O bira nasumično slobodno mjesto."""
    polje = podaci.polje
    slobodna_mjesta = [(i, j) for i in range(3) for j in range(3) if polje[i][j] == " "]

    if slobodna_mjesta:
        i, j = random.choice(slobodna_mjesta)
        polje[i][j] = "O"

    return {"polje": polje}
