const listaMovimientosRequest = new XMLHttpRequest();
const nuevoMovimientoRequest = new XMLHttpRequest();
const calcularBalanceRequest = new XMLHttpRequest();
const respuestaEstadoRequest = new XMLHttpRequest();

const root_host = "http://127.0.0.1:5000/api/v1/";

// Manejo de errores

function  mensajes_error(response, error) {
    const errorDiv = document.getElementById("mensaje-error");
    const errorHTML = `<p>${error}: ${response.message}</p>`;
    errorDiv.innerHTML = errorHTML;
}

// Mostrar movimientos

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
            sin_movimientos.innerHTML = mensaje_mov
        }
    } else {
        mensajes_error(response, "Error al acceder a la base de datos")
    }
}

function cargarEstado() {
    const response = JSON.parse(this.responseText)

    if (this.readyState === 4 && this.status === 200) {
        const valores = response.data;

        const tabla_estado = document.getElementById("tabla_estado")
        const inversionHTML = `<td>${valores["inversion"].toFixed(2)}</td>`;
        const totalHTML = `<td>${valores["total"].toFixed(2)}</td>`;
        const resultadoHTML = `<td>${valores["resultado"].toFixed(2)}</td>`;
        tabla_estado.innerHTML = inversionHTML + totalHTML + resultadoHTML;

        if (valores["resultado"] <= 0) {
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
    
    const moneda_from = document.getElementById("moneda_from");
    const cantidad_from = document.getElementById("cantidad_from");
    const moneda_to = document.getElementById("moneda_to");
    
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
    
    

    
    // Nuevos movimientos

function respuestaAltaMovimiento() {
    if (this.readyState === 4 && this.status === 200) {
        const form = document.querySelector("#formulario-movimiento");
        form.classList.add("inactivo");

        const url = `${root_host}movimientos`;
        listaMovimientosRequest.open("GET", url, true);
        listaMovimientosRequest.onload = cargaMovimientos;
        listaMovimientosRequest.send();

    } else {
        const response = JSON.parse(this.responseText);
        mensajes_error(response, "Error al acceder a la base de datos");
    }
}

function calculaTasa() {
    const mensaje_error = document.querySelector("#mensaje-error");
    const errorHTML = "";
    mensaje_error.innerHTML = errorHTML;
    
    const response = JSON.parse(this.responseText);

    if (this.readyState === 4 && this.status === 201) {
        const cantidad_to = document.getElementById("cantidad_to");
        cantidad_to.value = response["cantidad_to"].toFixed(2);

        const precio_unitario = document.getElementById("precio_unitario");
        precio_unitario.value = response["precio_unitario"].toFixed(4);

        // Evitamos que se pueda alterar el formulario después de calcular la tasa.

        const moneda_from = document.getElementById("moneda_from");
        moneda_from.setAttribute("disabled", true);
        const cantidad_from = document.getElementById("cantidad_from");
        cantidad_from.setAttribute("disabled", true);
        const moneda_to = document.getElementById("moneda_to");
        moneda_to.setAttribute("disabled", true);

    } else {
        mensajes_error(response, "Error en la Request a la API")
    }
}

function compruebaBalance() {
    const moneda_from = document.getElementById("moneda_from").value
    const cantidad_from = document.getElementById("cantidad_from").value
    const moneda_to = document.getElementById("moneda_to").value
    
    const datos_balance = {
        message: "convert",
        moneda_from: moneda_from,
        cantidad_from: cantidad_from,
        moneda_to: moneda_to
    };

    const url = `${root_host}movimiento`;
    calcularBalanceRequest.open("POST", url, true);
    calcularBalanceRequest.setRequestHeader(
        "Content-Type",
        "application/json"
    );

    calcularBalanceRequest.send(JSON.stringify(datos_balance));
    calcularBalanceRequest.onload = calculaTasa;
}

function altaMovimiento(ev) {
    ev.preventDefault()
    
    let fecha_actual = new Date()
    const moneda_from = document.getElementById("moneda_from").value
    const cantidad_from = document.getElementById("cantidad_from").value
    const moneda_to = document.getElementById("moneda_to").value
    const cantidad_to = document.getElementById("cantidad_to").value
    const nuevo_movimiento = {
        message: "nuevo_movimiento",
        date: obtener_fecha(fecha_actual),
        time: obtener_hora(fecha_actual),
        moneda_from: moneda_from,
        cantidad_from: cantidad_from,
        moneda_to: moneda_to,
        cantidad_to: cantidad_to,
    };
    const url = `${root_host}movimiento`;
    
    nuevoMovimientoRequest.open("POST", url, true)
    nuevoMovimientoRequest.setRequestHeader("Content-Type", "application/json")
    nuevoMovimientoRequest.send(JSON.stringify(nuevo_movimiento))
    nuevoMovimientoRequest.onload = respuestaAltaMovimiento
    resetearFormulario();        
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
