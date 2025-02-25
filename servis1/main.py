"""servis1 - upravljanje izvođenjem igre križić-kružić"""

import asyncio
import json

import aiohttp
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

SERVIS_2_URL = "http://servis2:8002/odigraj"
SERVIS_3_URL = "http://servis3:8003/odigraj"


def provjeri_pobjednika(polje):
    """Provjerava ima li pobjednika"""
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
        print(f"Provjera kombinacije: {kombinacija}")
        try:
            vrijednosti = [polje[x][y] for x, y in kombinacija]
            if vrijednosti[0] != " " and vrijednosti.count(vrijednosti[0]) == 3:
                return vrijednosti[0]
        except IndexError as e:
            print(f"Greška pri pristupu: {e}")
            return None
    return None


async def stream_game():
    polje = [[" "] * 3 for _ in range(3)]
    potez_broj = 0
    pobjednik = None

    while potez_broj < 9 and pobjednik is None:
        servis_url = SERVIS_2_URL if potez_broj % 2 == 0 else SERVIS_3_URL
        async with aiohttp.ClientSession() as session:
            response = await session.post(servis_url, json={"polje": polje})
            podaci = await response.json()
            polje = podaci["polje"]
            pobjednik = provjeri_pobjednika(polje)
            json_data = json.dumps({"poruka": f"Potez {potez_broj+1}", "polje": polje})  # Ispravni JSON
            yield f"data: {json_data}\n\n"  # Ispravan SSE format
        potez_broj += 1
        await asyncio.sleep(1)

    if pobjednik:
        json_data = json.dumps({"poruka": f"Pobjednik je {pobjednik}!", "polje": polje})
    else:
        json_data = json.dumps({"poruka": "Neriješeno!", "polje": polje})
    yield f"data: {json_data}\n\n"


@app.post("/start")
async def start_game():
    """Pokretanje strimanja igre"""
    return StreamingResponse(stream_game(), media_type="text/event-stream")
