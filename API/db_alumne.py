from client import db_client

# Llegeix tots els alumnes
def read():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM alumne")
        fetch_alumnes = cur.fetchall()
        print(fetch_alumnes)
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}
    finally:
        conn.close()
    return fetch_alumnes



#Llegeix alumne per alumne a partir de l'id
def read_id(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "select * from alumne WHERE idAlumne = %s"
        value = (id,)
        cur.execute(query,value)
    
        student = cur.fetchone()

    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return student

#Comprova si l'aula existeix o no
def aula_exists(idAula):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM aula WHERE idAula = %s"
        cur.execute(query, (idAula,))
        aulaExists = cur.fetchone()

        return aulaExists is not None  # Retorna true si troba l'aula, si no, no.
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}
    finally:
        conn.close()

#Crea un alumne
def create(idAula,nomAlumne,cicle,curs,grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT INTO alumne (idAula, nomAlumne, cicle, curs, grup, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, NOW(), NOW());"
        values = (idAula, nomAlumne, cicle, curs, grup)
        cur.execute(query, values)

        conn.commit()
        
        #Obté l'id de l'alumne generat
        student_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return {"status": 0, "message": "Alumne creat correctament", "student_id": student_id}

# Permet modificar el camp d’un alumne de la BBDD definit per la id que arribar per paràmetre
def update_alumne(idAlumne, idAula, nomAlumne, cicle, curs, grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "UPDATE alumne SET idAula = %s, nomAlumne = %s, cicle = %s, curs = %s, grup = %s, updatedAt = NOW() WHERE idAlumne = %s;"
        values = (idAula, nomAlumne, cicle, curs, grup, idAlumne)
        cur.execute(query, values)
        
        updated_recs = cur.rowcount
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    
    finally:
        conn.close()

    return updated_recs

#Permet eliminar un alumne de la base de dades
def delete_alumne(idAlumne):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM ALUMNE WHERE idAlumne = %s;"
        cur.execute(query,(idAlumne,))
        deleted_recs = cur.rowcount
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return deleted_recs

#Llegeix tots els alumnes i tota la info de les seves aules
def read_all():
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT a.NomAlumne, a.Cicle, a.Curs, a.Grup, au.descAula FROM alumne a JOIN aula au ON a.idAula = au.idAula;"
        
        cur.execute(query)

        studentsAndClassrooms = cur.fetchall()

        print(studentsAndClassrooms)
        
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}
    finally:
        conn.close()
        
    return studentsAndClassrooms

# Obtenir l'id de l'aula a partir de la descripció
def get_aula_id(descAula):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT idAula FROM aula WHERE descAula = %s"
        cur.execute(query, (descAula,))
        aula_id = cur.fetchone()
        return aula_id[0] if aula_id else None
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}
    finally:
        conn.close()

# Crear aula si no existeix
def create_aula(descAula, edifici, pis):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT INTO aula (descAula, edifici, pis, createdAt, updatedAt) VALUES (%s, %s, %s, NOW(), NOW());"
        values = (descAula, edifici, pis)
        cur.execute(query, values)
        conn.commit()
        return cur.lastrowid  # Devuelve el ID del aula recién creada
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}
    finally:
        conn.close()

# Obtenir l'ID de l'alumne si existeix
def get_alumne_id(nomAlumne, cicle, curs, grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT idAlumne FROM alumne WHERE nomAlumne = %s AND cicle = %s AND curs = %s AND grup = %s"
        cur.execute(query, (nomAlumne, cicle, curs, grup))
        alumne_id = cur.fetchone()
        return alumne_id[0] if alumne_id else None
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}"}
    finally:
        conn.close()

