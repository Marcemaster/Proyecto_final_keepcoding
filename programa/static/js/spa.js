const listaMovimientosRequest = new XMLHttpRequest();
const cambiaMovimientosRequest = new XMLHttpRequest();
const calcularBalanceRequest = new XMLHttpRequest();
const respuestaEstadoRequest = new XMLHttpRequest();

const root_host = "http://127.0.0.1:5000/api/v1/";

// Manejo de errores

function  mensajes_error(response, error) {
    const errorDiv = document.getElementById("mensaje-error");
    const errorHTML = `<p>${error}: ${response.message}</p>`;
    errorDiv.innerHTML = errorHTML;
}

// Mostrar tablas de movimientos

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

// Calcular tasa de cambio

function calculaTasa() {
    const mensaje_error = document.querySelector("#mensaje-error");
    const errorHTML = "";
    mensaje_error.innerHTML = errorHTML;
    const response = JSON.parse(this.responseText);

    if (this.readyState === 4 && this.status === 201) {
        const cantidad_to = document.getElementById("cantidad_to");
        cantidad_to.value = response["cantidad_to"]

        const precio_unitario = document.getElementById("precio_unitario")
        precio_unitario.value = response["precio_unitario"]

        // Evitamos que se pueda alterar el formulario después de calcular la tasa.

        const moneda_from = document.getElementById("moneda_from");
        moneda_from.setAttribute("disabled", true);
        const cantidad_from = document.getElementById("cantidad_from");
        cantidad_from.setAttribute("disabled", true);
        const moneda_to = document.getElementById("moneda_to");
        moneda_to.setAttribute("disabled", true);

    } else {
        mensaje_error(response, "Error en la Request a la API")
    }
}

function respuestaTasa() {
}

// Status 

function cargarEstado() {
    const response = JSON.parse(this.responseText)

    if (this.readyState === 4 && this.status === 200) {
        const valores = response.data;

        const tabla_estado = document.getElementById("tabla_estado")
        const inversionHTML = `<td>${valueStatus["inversion"]}</td>`;
        const totalHTML = `<td>${valueStatus["total"]}</td>`;
        const resultadoHTML = `<td>${valueStatus["resultado"]}</td>`;
        tabla_estado.innerHTML = inversionHTML + totalHTML + resultadoHTML;

        if (valueStatus["resultado"] <= 0) {
            const tabla_estado = document.getElementById("tabla_estado").getElementsByTagName("td");
            tabla_estado[2].style.color = "red";
        }
    } else {
        mensajes_error(response, "Error en la request a CoinApi")
    }
}

function respuestaEstado() {
    const url = `${root_host}status`;
    respuestaEstadoRequest.open("GET", url, true);
    respuestaEstadoRequest.onload = cargarEstado;
    respuestaEstadoRequest.send();
}

// Manejo del formulario 

function hazVisibleForm(ev) {
    ev.preventDefault()

    const form = document.querySelector("#formulario-movimiento")
    form.classList.remove("inactivo")

    const aceptar = document.getElementById("btn-enviar")
    aceptar.classList.add("inactivo")

}

function resetearFormulario() {
    document.getElementById("moneda_from").value = "EUR";
    document.getElementById("cantidad_from").value = "";
    document.getElementById("moneda_to").value = "BTC";
    document.getElementById("cantidad_to").value = "EUR";
    document.getElementById("precio_unitario").value = "EUR";

    const moneda_from = document.getElementById("moneda_from");
    moneda_from.removeAttribute("inactivo")
    const cantidad_from = document.getElementById("cantidad_from");
    cantidad_from.removeAttribute("inactivo")
    const moneda_to = document.getElementById("moneda_to");
    moneda_to.removeAttribute("inactivo")
    const boton_aceptar = document.querySelector("#btn-enviar");
    boton_aceptar.classList.remove("inactivo");
}


// Funciones para conseguir la fecha 

function obtener_fecha(date) {
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

function obtener_hora(date) {
    return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
}


// Validación de inputs del formulario

function validaInputs(ev) {
    ev.preventDefault();
    
    const moneda_from = document.getElementById("moneda_from")
    const moneda_to = document.getElementById("moneda_to")
    const cantidad_from = document.getElementById("cantidad_from")
    
    if ( 
        cantidad_from.value == ""
        ) {
            mensajes_error("Por favor, rellena todos los campos");
        } else if (moneda_from.value == moneda_to.value ) {
            mensajes_error("Las monedas deben ser distintas");
        } else {
            compruebaBalance();
        } 
        
    }
    
    
    function compruebaBalance() {
        
        
    }
    

    // Nuevos movimientos
    
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


// FINAL Window onload.

window.onload = function() {
    const url = `${root_host}movimientos`;
    listaMovimientosRequest.open("GET", url, true);
    listaMovimientosRequest.onload = cargaMovimientos;
    listaMovimientosRequest.send();

    const btnNuevo = document.querySelector("#btn-nuevo")
    btnNuevo.addEventListener("click", hazVisibleForm)

    const btnCalc = document.querySelector("#btn-calcular")
    btnCalc.addEventListener("click", validaInputs)

    const btnEnviar = document.querySelector("#btn-enviar")
    btnEnviar.addEventListener("click", altaMovimiento)
}
