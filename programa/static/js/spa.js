const listaMovimientosRequest = new XMLHttpRequest();
const cambiaMovimientosRequest = new XMLHttpRequest();
const calcularBalanceRequest = new XMLHttpRequest();
const statusBalanceRequest = new XMLHttpRequest();

const root_host = "http://127.0.0.1:5000/api/v1/";

function  mensajes_error(response, error) {
    const errorDiv = document.getElementById("mensaje-error");
    const errorHTML = `<p>${error}: ${response.message}</p>`;
    errorDiv.innerHTML = errorHTML;
}

function requestAltaMovimiento() {
    if (this.readyState === 4 && this.status === 200) {
        const formulario = document.querySelector("#formulario");
        
        const url = `${root_host}movimientos`;
        listaMovimientosRequest.open("GET", url, true);
        listaMovimientosRequest.onload = cargaMovimientos;
        listaMovimientosRequest.send();
    } else {
        const response = JSON.parse(this.responseText);
        mensajes_error(response, "Error al acceder a la base de datos")
    }
}


function cargaMovimientos() {
    const response = JSON.parse(this.responseText)

    if (this.readyState === 4 && this.status === 200) {
        const movimientos = response.movimientos;
        if (movimientos.length != 0) {

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
            const sin_movimientos = document.querySelector("#sin-movimientos");

            const mensaje_mov = `<p>Aquí aparecerán los movimientos. Realice la primera compra</p>`;
            mensaje_mov.innerHTML = mensaje_mov
        }
    }
}

function calculaTasa() {
    const mensaje_error = document.querySelector("#mensaje-error");
    const errorHTML = "";
    mensaje_error.innerHTML = errorHTML;
    const response = JSON.parse(this.responseText);

    if (this.readyState === 4 && this.status === 201) {
        const cantidad_to = document.querySelector("#cantidad_to");
        cantidad_to.value = response["cantidad_to"]
    } else {
        mensaje_error(respones, "Error en la Request a la API")
    }


    ev.preventDefault()

    const moneda_from = document.querySelector("#moneda_from").value
    const cantidad_from = document.querySelector("#cantidad_from").value
    const moneda_to = document.querySelector("#moneda_to").value

    json_calcular = {"moneda_from":moneda_from, "cantidad_from":cantidad_from, "moneda_to":moneda_to}
    console.log(json_calcular)
    alert(json_calcular)

    cambiaMovimientosRequest.open("POST", "/calcular", true)
    cambiaMovimientosRequest.setRequestHeader("Content-Type", "application/json")
    cambiaMovimientosRequest.onload = respuestaAltaMovimiento
    cambiaMovimientosRequest.send(JSON.stringify(json_calcular))

}

function respuestaTasa() {

}




function hazVisibleForm(ev) {
    ev.preventDefault()

    const form = document.querySelector("#formulario-movimiento")
    form.classList.remove("inactivo")
}

function altaMovimiento(ev) {
    ev.preventDefault()

    const date = "17/10/2021"//today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    const time = "20:29:10" // Date.getHours() + ":" + Date.getMinutes() + ":" + Date.getSeconds();
    const moneda_from = document.querySelector("#moneda_from").value
    const cantidad_from = document.querySelector("#cantidad_from").value
    const moneda_to = document.querySelector("#moneda_to").value
    const cantidad_to = 100000//calculaTasa // ¿Cómo se conecta esto con la llamada a la API de coinmarketcap? 
    // Primero hay que rellenar los datos en el form a través de otra función

    json_movimiento = {"date":date, "time":time, "moneda_from":moneda_from, "cantidad_from":cantidad_from, "moneda_to":moneda_to, "cantidad_to":cantidad_to}

    cambiaMovimientosRequest.open("POST", "/api/v1/movimiento", true)
    cambiaMovimientosRequest.setRequestHeader("Content-Type", "application/json")
    cambiaMovimientosRequest.onload = respuestaAltaMovimiento
    cambiaMovimientosRequest.send(JSON.stringify(json_movimiento))

}

function respuestaAltaMovimiento() {
    if (this.readyState === 4 && this.status === 200) {
        const url = `${root_host}movimientos`
        listaMovimientosRequest.open("GET", url, true)
        listaMovimientosRequest.onload = muestraMovimientos
        listaMovimientosRequest.send()

    } else {
        const response = JSON.parse(this.responseText);
        errorMessage(response, "Error al acceder a la base de datos");
    }
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