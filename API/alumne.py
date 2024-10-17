#Programa que defineix els camps d'un alumne i la seva aula
def alumne_schema(student):
    return {
        "idAlumne": student[0],
        "idAula": student[1],
        "nomAlumne": student[2],
        "cicle": student[3],
        "curs": student[4],
        "grup": student[5],
        "createdAt": student[6],
        "updatedAt": student[7]      
    }


def alumnes_schema(alumnes) -> list:
    return [alumne_schema(alumne) for alumne in alumnes]
