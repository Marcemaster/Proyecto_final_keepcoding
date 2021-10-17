const listaMovimientosRequest = new XMLHttpRequest()
const cambiaMovimientosRequest = new XMLHttpRequest()
const calculaTasaRequest = new XMLHttpRequest()
const root_host = "http://127.0.0.1:5000/api/v1/"
const coinMarket_host = ""



function calculaTasa(ev) {
    ev.preventDefault()

    // Acá consultamos a la api externa, a través de la llamada a views. Creo.

}


function respuestaAltaMovimiento() {
    if (this.readyState === 4 && this.status === 200) {
        const url = `${root_host}movimientos`
        listaMovimientosRequest.open("GET", url, true)
        listaMovimientosRequest.onload = muestraMovimientos
        listaMovimientosRequest.send()

    } else {
        alert("Se ha producido un error en el alta del movimiento")

    }
}

function muestraMovimientos() {
    if (this.readyState === 4 && this.status === 200) {
        const respuesta = JSON.parse(this.responseText)
        const movimientos = respuesta.movimientos
        const tabla = document.querySelector("#tabla-datos")
        let innerHTML = ""
        for (let i=0; i < movimientos.length; i++) {
        innerHTML = innerHTML +
        `<tr>
            <td>${movimientos[i].date}</td>
            <td>${movimientos[i].time}</td>
            <td>${movimientos[i].moneda_from}</td>
            <td>${movimientos[i].cantidad_from}</td>
            <td>${movimientos[i].moneda_to}</td>
            <td>${movimientos[i].cantidad_to}</td>
        </tr>`
        }
        tabla.innerHTML = innerHTML
    } else {
        alert("Se ha producido un error en la consulta de movimientos")
    }
}

function hazVisibleForm(ev) {
    ev.preventDefault()

    const form = document.querySelector("#formulario-movimiento")
    form.classList.remove("inactivo")
}

function altaMovimiento(ev) {
    ev.preventDefault()

    const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    const time = Date.getHours() + ":" + Date.getMinutes() + ":" + Date.getSeconds();
    const moneda_from = document.querySelector("#moneda_from").value
    const cantidad_from = document.querySelector("#cantidad_from").value
    const moneda_to = document.querySelector("#moneda_to").value
    const cantidad_to = calculaTasa // ¿Cómo se conecta esto con la llamada a la API de coinmarketcap? 
    // Primero hay que rellenar los datos en el form a través de otra función

    json_movimiento = {"date":date, "time":time, "moneda_from":moneda_from, "cantidad_from":cantidad_from, "moneda_to":moneda_to, "cantidad_to":cantidad_to}

    cambiaMovimientosRequest.open("POST", "/api/v1/movimiento", true)
    cambiaMovimientosRequest.setRequestHeader("Content-Type", "application/json")
    cambiaMovimientosRequest.onload = respuestaAltaMovimiento
    cambiaMovimientosRequest.send(JSON.stringify(json_movimiento))

}

window.onload = function() {
    const url = `${root_host}movimientos`
    listaMovimientosRequest.open("GET", url, true)
    listaMovimientosRequest.onload = muestraMovimientos
    listaMovimientosRequest.send()


    const btnNuevo = document.querySelector("#btn-nuevo")
    btnNuevo.addEventListener("click", hazVisibleForm)

    const btnCalc = document.querySelector("#btn-calcular")
    btnCalc.addEventListener("click", calculaTasa)

    const btnEnviar = document.querySelector("#btn-enviar")
    btnEnviar.addEventListener("click", altaMovimiento)
}