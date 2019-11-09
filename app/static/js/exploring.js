$(function() {
    $('#guardarClienteButton').click(function() {
        $.ajax({
            type: 'POST',
            url: '/logicaIngresarUpdateClientes',
            data: {
                nitCliente:$("#NitCliente").val(),
                nombreCliente:$("#NombreCliente").val(),
                telefonoCliente:$("#TelefonoCliente").val(),
                direccionCliente:$("#DireccionCliente").val(),
                fechaNacimientoCliente:$("#FechaNacimientoCliente").val(),
                generoCliente:$("#GeneroCliente").val()
            },
            success: function(data) {

            },
        });
    });
});

$(function() {
    $('#guardarVentaButton').click(function() {
        $.ajax({
            type: 'POST',
            url: '/logicaIngresarUpdateVentas',
            data: {
                idVenta:$("#IdVenta").val(),
                fechaDeLaVenta:$("#FechaDeLaVenta").val(),
                modeloVehiculo:$("#modeloVehiculo").val(),
                elExtra:$("#elExtra").val(),
                nitCliente:$("#NitCliente").val()
            },
            success: function(data) {
                if (data == "no existe cliente"){
                    alert("usuario no existe, guardelo para poder guardar la venta")
                }else{
                    if(data.asignaIdVenta == "si"){
                        $("#IdVenta").val(data.idVenta)
                    }
                }
            },
        });
    });
});

$(function() {
    $('#actualizarVentaButton').click(function() {
        $.ajax({
            type: 'POST',
            url: '/logicaIngresarUpdateVentas',
            data: {
                idVenta:$("#IdVenta").val(),
                fechaDeLaVenta:$("#FechaDeLaVenta").val(),
                modeloVehiculo:$("#modeloVehiculo").val(),
                elExtra:$("#elExtra").val(),
                nitCliente:$("#NitCliente").val()
            },
            success: function(data) {
                if (data == "no existe cliente"){
                    alert("usuario no existe, guardelo para poder guardar la venta")
                }
            },
        });
    });
});
$(function() {
    $('#guardarRepaReviButton').click(function() {
        $.ajax({
            type: 'POST',
            url: '/logicaIngresarUpdateRepaRevi',
            data: {
                idVenta:$("#IdVenta").val(),
                fechaDeLaVenta:$("#FechaDeLaVenta").val(),
                modeloVehiculo:$("#modeloVehiculo").val(),
                elExtra:$("#elExtra").val(),
                nitCliente:$("#NitCliente").val(),
                fueRealizada:$('#fueRealizada').val(),
                motivoReviRepa:$('#MotivoReviRepa').val(),
                fechaReviRepa:$('#FechaReviRepa').val(),
                mecaDispo:$('#MecaDispo').val(),
                carroReviRepaPlaca:$('#carroReviRepaPlaca').val(),
                modeloVehiculo:$('#modeloVehiculo').val()
            },
            success: function(data) {
                if (data == "no existe cliente"){
                    alert("usuario no existe, guardelo para poder guardar la venta")
                }else{
                    if(data.asignaIdVenta == "si"){
                        $("#IdVenta").val(data.idVenta)
                    }
                }
            },
        });
    });
});
guardarRepaReviButton


///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////
///////////////////////////

$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(data) {
                $('#meterAquiElTextoDelPdf').text(String.raw`${data.textoDelPdf_rsp}`);               
                console.log('Success!');
            },
        });
    });
});

$(function() {
    $('#botonQueBuscaRegex').click(function() {
        $.ajax({
            type: 'POST',
            url: '/matchesEncontrada',
            data: {
                reguExpre:$("#aquiVaRegex").val(),
                texto:$("#meterAquiElTextoDelPdf").text()
            },
            success: function(data) {
                if(data =="patron no encontrado"){
                    alert(data)
                }else{
                    $("#meterAquiElTextoDelPdf").html(data.textoResaltado); 
                }
            },
        });
    });
});


$(function() {
    $('#Formato').click(function() {
        $.ajax({
            type: 'POST',
            url: '/addicionDeFormato',
            data: {
                seccion:$("#aquiVaRegex").val()
            },
            success: function(data) {
            },
        });
    });
});
$(function() {
    $('#DeterminadorDeFormato').click(function() {
        $.ajax({
            type: 'POST',
            url: '/determinadorDeFormato',
            data: {
                seccion:$("#aquiVaSeccion").val(),
                determinador:$("#aquiVaRegex").val()
            },
            success: function(data) {
            },
        });
    });
});
$(function() {
    $('#Variable').click(function() {
        $.ajax({
            type: 'POST',
            url: '/agregandoVariable',
            data: {
                seccion:$("#aquiVaSeccion").val(),
                regex:$("#aquiVaRegex").val(),
                variable:$("#aquiVaNombreVariable").val()
            },
            success: function(data) {
            },
        });
    });
});
$(function() {
    $('#Eliminables').click(function() {
        $.ajax({
            type: 'POST',
            url: '/agregandoEliminable',
            data: {
                seccion:$("#aquiVaSeccion").val(),
                regex:$("#aquiVaRegex").val(),
                eliminable:$("#aquiVaNombreVariable").val()
            },
            success: function(data) {
            },
        });
    });
});
$(function() {
    $('#SeparadorDeEventos').click(function() {
        $.ajax({
            type: 'POST',
            url: '/separadordueventos',
            data: {
                seccion:$("#aquiVaSeccion").val(),
                separador:$("#aquiVaRegex").val()
            },
            success: function(data) {
            },
        });
    });
});
$(function() {
    $('#ColumnasNoVacias').click(function() {
        $.ajax({
            type: 'POST',
            url: '/columnasnovacias',
            data: {
                noVacias:$("#aquiVaRegex").val()
            },
            success: function(data) {
            },
        });
    });
});





