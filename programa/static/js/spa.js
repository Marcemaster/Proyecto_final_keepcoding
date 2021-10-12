const xhr = new XMLHttpRequest()
const root_host = "http://127.0.0.1:5000/api/v1/"

function muestraMovimientos() {
    if (this.readyState === 4 && this.status === 200) {
        const movimientos = JSON.parse(this.responseText)
        const tabla = document.querySelector("#tabla-datos")
        let innerHTML = ""
        for (let i=0; i < movimientos.length; i++) {
        innerHTML = innerHTML +
        `<tr>
            <td>${movimientos[i].id}</td>
            <td>${movimientos[i].date}</td>
            <td>${movimientos[i].time}</td>
            <td>${movimientos[i].moneda_from}</td>
            <td>${movimientos[i].cantidad_from}</td>
            <td>${movimientos[i].moneda_to}</td>
            <td>${movimientos[i].cantidad_to}</td>
            <td>${movimientos[i].moneda_to}</td>
        </tr>`
        }
        tabla.innerHTML = innerHTML
    } else {
        alert("Se ha producido un error en la consulta de movimientos")
    }
}

window.onload = function() {
    const url = `${root_host}movimientos`
    xhr.open("GET", url, true)
    xhr.onload = muestraMovimientos
    xhr.send()
}