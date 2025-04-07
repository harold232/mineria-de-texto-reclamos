document.addEventListener("DOMContentLoaded", function() {
    cargarDatos();
});

function cargarDatos() {
    fetch("/datos")
        .then(response => response.json())
        .then(data => mostrarDatos(data))
        .catch(error => console.error("Error al cargar datos:", error));
}

function mostrarDatos(data) {
    let tabla = document.getElementById("tabla-datos");
    tabla.innerHTML = "";
    data.forEach(reclamo => {
        let fila = `<tr>
                        <td>${reclamo.CO_UNICO_RECLAMO}</td>
                        <td>${reclamo.FE_PRESEN_RECLA}</td>
                        <td>${reclamo.DE_SERVICIO}</td>
                        <td>${reclamo.DE_ESTADO_RECLAMO}</td>
                    </tr>`;
        tabla.innerHTML += fila;
    });
}

function filtrarDatos() {
    let fechaInicio = document.getElementById("fecha_inicio").value;
    let fechaFin = document.getElementById("fecha_fin").value;
    
    let formData = new FormData();
    formData.append("fecha_inicio", fechaInicio);
    formData.append("fecha_fin", fechaFin);
    
    fetch("/filtrar", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => mostrarDatos(data))
    .catch(error => console.error("Error en filtrado:", error));
}
