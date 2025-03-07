"""konkurentni zahtjevi prema servisu za križić kružić"""

import asyncio

import aiohttp


URL = "http://localhost:8001/start"


async def salji_zahtjev(session, request_id):
    """Šalje jedan zahtjev i ispisuje odgovor"""
    try:
        async with session.post(URL) as response:
            async for line in response.content:
                decoded_line = line.decode("utf-8").strip()
                print(f"[Zahtjev {request_id}] {decoded_line.encode().decode('unicode_escape')}")
    except Exception as e:
        print(type(e), e.args)


async def main():
    """glavna funkcija - pokreće više konkurentnih zahtjeva"""
    async with aiohttp.ClientSession() as session:
        igre = [salji_zahtjev(session, i) for i in range(25)]
        await asyncio.gather(*igre)


if __name__ == "__main__":
    asyncio.run(main())
