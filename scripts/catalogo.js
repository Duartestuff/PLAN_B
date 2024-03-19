const coloresValidos = [
    'Amarillo',
    'Azul',
    'Beige',
    'Blanca',
    'Blanco',
    'Cafe',
    'Gris',
    'Kamel',
    'Lila',
    'Negro',
    'Roja',
    'Rojo',
    'Rosa',
    'Terracota', 
    'Verde'
];

const tallasValidas = [
    '6',
    '8',
    '10',
    '12',
    '14',
    '16',
    '18',
    'XS',
    'S',
    'M',
    'L',
    'XL',
    'XXL'
];

function comprarProducto(colors, ref, name) {

    var colorstring = '';
    colors.forEach(color => {
        colorstring += ' ' + color;
    });
    const color = checkValid('Por favor introduzca el color que desea elegir, colores disponibles: ' + colorstring, coloresValidos);
    const talla = checkValid('Por favor introduzca la talla del ' + name, tallasValidas);
    const cantidad = prompt('Por favor introduzca la cantidad que desea ordenar')
    
    const url = `http://127.0.0.1:8080/process_order?product_id=${ref}&quantity=${cantidad}&size=${talla}&color=${color}`;
    
    sendToWhatsapp(url, {
        'ref': ref,
        'color': color,
        'talla': talla,
        'cantidad': cantidad,
        'nombre': name
    })

};

function checkValid(message, validVals) {
    let finalinput;
    while (true) {
        const input = prompt(message);
        let checkInput = input.toString();
        let finish = false;
        for (let i = 0; i < validVals.length; i++) {
            let checkVal = validVals[i].toString();
            if (checkInput === checkVal) {
                finalinput = input;
                finish = true;
                break; // Exit the for loop
            }
        }
        if(finish) break;
        else alert('Por favor introduzca uno de los valores proporcionados')
    };
    return finalinput
}

function sendToWhatsapp(url, product) {

    const phoneNumber = '573052553742';
    const message = encodeURIComponent(`
        Hola, quisiera hacer un pedido del siguiente producto:
        ${product.nombre} - ref: ${product.ref} - color: ${product.color} - talla: ${product.talla}
        Cantidad: ${product.cantidad}
        
        A continuanción está la orden de compra:
        ${url}
    `);

    const wpURL = `https://wa.me/${phoneNumber}?text=${message}`;
    window.open(wpURL, 'blank');


};