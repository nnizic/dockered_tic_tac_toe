"""provjera pobjednika"""


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


def main() -> None:
    """glavna funkcija"""

    test_polje = [["X", "O", "X"], ["0", "X", "X"], ["O", "O", "O"]]

    print(test_polje)
    print("Pobjednik je:", provjeri_pobjednika(test_polje))


if __name__ == "__main__":
    main()
