document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch('https://alumnat.com/alumne/list').then(res => res.json()).then(data => console.log(data)).catch(err => console.error(err));______________________________________________
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res
            
            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");

                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.NomAlumne;
                row.appendChild(nomAluCell);

                // Repetir per tots els altres camps restants que retorna l'endpoint
                _____________________________________________

                //Itera sobre el cicle
                const cicleCell = document.createElement("td");
                cicleCell.textContent = alumne.Cicle;
                row.appendChild(cicleCell);

                //Itera sobre el curs
                const cursCell = document.createElement("td");
                cursCell.textContent = alumne.Curs;
                row.appendChild(cursCell);
                
                //Itera sobre el grup
                const grupCell = document.createElement("td");
                grupCell.textContent = alumne.Grup;
                row.appendChild(grupCell);

                //Itera sobre l'aula
                const aulaCell = document.createElement("td");
                aulaCell.textContent = alumne.DescAula;
                row.appendChild(aulaCell);

                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});