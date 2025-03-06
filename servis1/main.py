"""servis1 - upravljanje izvođenjem igre križić-kružić"""

import asyncio
import json
import sys

import aiohttp
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

# postavljanje encodinga na UTF-8
sys.stdout.reconfigure(encoding="utf-8")

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


async def async_retry_request(url, json_data, max_retries=5):
    """Asinkroni HTTP poziv s retry mehanizmom i exponential backoff-om"""
    delay = 1  # Početno kašnjenje u sekundama
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=json_data) as response:
                    if response.status == 200:
                        return await response.json()
                    print(f"Greška {response.status}, pokušaj {attempt+1}/{max_retries}")
        except aiohttp.ClientError as e:
            print(f"Greška: {e}, pokušaj {attempt + 1}/{max_retries}")

        await asyncio.sleep(delay)
        delay *= 2  # Exponential backoff

    raise Exception(f"Neuspješno dohvaćanje podataka s {url} nakon {max_retries} pokušaja.")


async def stream_game():
    """upravljanje igrom s retry mehanizmom"""
    polje = [[" "] * 3 for _ in range(3)]
    potez_broj = 0
    pobjednik = None

    while potez_broj < 9 and pobjednik is None:
        servis_url = SERVIS_2_URL if potez_broj % 2 == 0 else SERVIS_3_URL
        servis_naziv = "Igrač X" if servis_url == SERVIS_2_URL else "Igrač O"

        try:
            podaci = await async_retry_request(servis_url, {"polje": polje})
            polje = podaci["polje"]
            yield f'data: {{"poruka":"{servis_naziv} je odigrao", "polje": {polje}}}\n\n'
        except Exception as e:
            yield f'data: {{"poruka": "Greška u komunikaciji: {str(e)}"}}\n\n'
            break  # Ako servis ne odgovori nakon svih pokušaja prekid igre

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
