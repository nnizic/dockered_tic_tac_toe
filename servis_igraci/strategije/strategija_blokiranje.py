def odigraj_ako_mogu_pobjediti(polje, simbol):
    """traži nedostaje li negdje jedno polje za pobjedu"""

    # Provjera redova i stupaca
    for i in range(3):
        if polje[i].count(simbol) == 2 and polje[i].count(" ") == 1:
            return i, polje[i].index(" ")
        col = [polje[j][i] for j in range(3)]
        if col.count(simbol) == 2 and col.count(" ") == 1:
            return col.index(" "), i

    # Provjera dijagonala
    diag1 = [polje[i][i] for i in range(3)]
    if diag1.count(simbol) == 2 and diag1.count(" ") == 1:
        idx = diag1.index(" ")
        return idx, idx

    diag2 = [polje[i][2 - i] for i in range(3)]
    if diag2.count(simbol) == 2 and diag2.count(" ") == 1:
        idx = diag2.index(" ")
        return idx, 2 - idx

    # Ako nema pobjede, vrati prvo slobodno polje
    for i in range(3):
        for j in range(3):
            if polje[i][j] == " ":
                return i, j
