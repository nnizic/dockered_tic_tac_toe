"""Servis 2 (Igrač X)"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PoljeModel(BaseModel):
    polje: list


@app.post("/odigraj")
async def odigraj_potez(podaci: PoljeModel):
    """Igrač X bira prvo slobodno mjesto"""
    polje = podaci.polje

    for i in range(3):
        for j in range(3):
            if polje[i][j] == " ":
                polje[i][j] = "X"

                return {"polje": polje}

    return {"polje": polje}
