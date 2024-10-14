def alumne_schema(fetchAlumnes):
    return {
        "NomAlumne": fetchAlumnes[0],
        "Cicle": fetchAlumnes[1],
        "Curs": fetchAlumnes[2],
        "Grup": fetchAlumnes[3],
        "DescAula": fetchAlumnes[4]
    }

def alumnes_schema(alumnes) -> list:
    return [alumne_schema(alumne) for alumne in alumnes]
