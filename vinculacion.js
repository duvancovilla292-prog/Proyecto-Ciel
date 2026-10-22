// ==========================================
// ELECCIÓN DEL MÉTODO DE VINCULACIÓN DE WHATSAPP (código de 8 caracteres o QR)
//
//  - Con terminal (tu computador): pregunta "¿código o QR?" y, si eliges código, tu número.
//  - Sin terminal (Render, Docker sin -it): asume CÓDIGO; el número sale de WA_NUMERO.
//  - Si defines WA_NUMERO, usa el código sin preguntar.
// ==========================================
const readline = require('readline');

let metodo = null; // { tipo: 'codigo' | 'qr', numero: string } — se decide una sola vez por arranque

// Lee una línea visible (para datos que no son secretos: opciones, número, rutas)
function leerLinea(pregunta) {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    return new Promise((resolve) => {
        rl.question(pregunta, (respuesta) => {
            rl.close();
            resolve(respuesta.trim());
        });
    });
}

async function elegirMetodoVinculacion() {
    if (metodo) return metodo; // los reinicios del socket no vuelven a preguntar

    const numeroEnv = (process.env.WA_NUMERO || '').replace(/\D/g, '');
    const hayTerminal = Boolean(process.stdin.isTTY && process.stdout.isTTY);

    if (numeroEnv) {
        metodo = { tipo: 'codigo', numero: numeroEnv };
    } else if (!hayTerminal) {
        // Sin terminal no se puede preguntar: se asume código (si falta WA_NUMERO, index.js lo avisa en los logs)
        metodo = { tipo: 'codigo', numero: '' };
    } else {
        console.log('\n🔗 [SISTEMA] WhatsApp aún no está vinculado. ¿Cómo quieres vincularlo?');
        console.log('   1) Código de 8 caracteres (escribes tu número y luego el código en el celular)');
        console.log('   2) Código QR (lo escaneas con el celular)\n');

        let opcion = '';
        while (opcion !== '1' && opcion !== '2') {
            opcion = await leerLinea('👉 Elige 1 o 2: ');
        }

        if (opcion === '2') {
            metodo = { tipo: 'qr', numero: '' };
        } else {
            let numero = '';
            while (numero.length < 8 || numero.length > 15) {
                numero = (await leerLinea('📱 Tu número con código de país, sin + ni espacios (ej. 573001234567): ')).replace(/\D/g, '');
            }
            metodo = { tipo: 'codigo', numero };
        }
    }
    return metodo;
}

function obtenerMetodoVinculacion() {
    return metodo || { tipo: 'qr', numero: '' };
}

module.exports = { elegirMetodoVinculacion, obtenerMetodoVinculacion, leerLinea };
