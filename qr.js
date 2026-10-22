// ==========================================
// VINCULACIÓN DE WHATSAPP (se ejecuta una sola vez)
//
//   node qr.js                  → muestra un QR para escanear
//   node qr.js 573001234567     → muestra un CÓDIGO de 8 caracteres (sin escanear)
//   node qr.js --reset          → borra la sesión anterior y empieza de cero
//   node qr.js 573001234567 --reset
// ==========================================
const {
    default: makeWASocket,
    useMultiFileAuthState,
    DisconnectReason,
    fetchLatestBaileysVersion,
    Browsers
} = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const fs = require('fs');

const CARPETA_SESION = 'sesion_whatsapp';
const MAX_REINTENTOS = 5;
const CODIGO_REINICIO = DisconnectReason?.restartRequired ?? 515;
const CODIGO_SESION_CERRADA = DisconnectReason?.loggedOut ?? 401;

// Argumentos: un número de teléfono (opcional) y/o --reset
const args = process.argv.slice(2);
const reiniciarSesion = args.includes('--reset');
const numeroTelefono = (args.find(a => !a.startsWith('--')) || '').replace(/\D/g, '');

// Logger mínimo para que Baileys no llene la terminal de texto
const loggerSilencioso = {
    level: 'silent',
    child() { return this; },
    trace() {}, debug() {}, info() {}, warn() {}, error() {}
};

let reintentos = 0;

function esperar(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function borrarSesion() {
    fs.rmSync(CARPETA_SESION, { recursive: true, force: true });
}

async function generarQR() {
    const { state, saveCreds } = await useMultiFileAuthState(CARPETA_SESION);

    // Sin la versión actual de WhatsApp Web, el servidor rechaza la conexión (error 405)
    // y el QR nunca aparece. Por eso la consultamos antes de conectar.
    let version;
    try {
        const info = await fetchLatestBaileysVersion();
        if (info.error) throw info.error;
        version = info.version;
        console.log(`ℹ️  Versión de WhatsApp Web: ${version.join('.')}`);
    } catch (e) {
        console.log('⚠️  No se pudo consultar la última versión de WhatsApp Web (¿sin internet?). Se usará la que trae Baileys.');
    }

    const sock = makeWASocket({
        auth: state,
        ...(version ? { version } : {}),
        logger: loggerSilencioso,
        browser: Browsers ? Browsers.ubuntu('Chrome') : ['Ubuntu', 'Chrome', '20.0.04'],
        printQRInTerminal: false,
        syncFullHistory: false,
        markOnlineOnConnect: false
    });

    sock.ev.on('creds.update', saveCreds);

    let codigoSolicitado = false;

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            if (numeroTelefono) {
                // Modo código de emparejamiento (útil si el QR no se ve bien en la terminal)
                if (!codigoSolicitado && !sock.authState.creds.registered) {
                    codigoSolicitado = true;
                    try {
                        const codigo = await sock.requestPairingCode(numeroTelefono);
                        const bonito = codigo.match(/.{1,4}/g)?.join('-') || codigo;
                        console.log('\n🔑 [SISTEMA] Tu código de vinculación es:\n');
                        console.log(`        ${bonito}\n`);
                        console.log('En el celular: WhatsApp → Ajustes → Dispositivos vinculados →');
                        console.log('Vincular un dispositivo → "Vincular con el número de teléfono" y escribe el código.\n');
                    } catch (error) {
                        console.error('🛑 No se pudo generar el código de vinculación:', error?.message || error);
                    }
                }
            } else {
                console.log('\n✨ [SISTEMA] ¡QR recibido! Escanéalo con tu celular:');
                console.log('   WhatsApp → Ajustes → Dispositivos vinculados → Vincular un dispositivo\n');
                qrcode.generate(qr, { small: true });
                console.log('\n(El QR se renueva solo cada ~20 segundos. Si no lo ves completo, agranda la terminal');
                console.log(' o usa el código: node qr.js TUNUMERO  →  ej. node qr.js 573001234567)\n');
            }
        }

        if (connection === 'close') {
            const codigo = lastDisconnect?.error?.output?.statusCode;

            // 515: WhatsApp pide reiniciar justo después de escanear. Es normal, no cuenta como error.
            if (codigo === CODIGO_REINICIO) {
                console.log('🔄 Reiniciando conexión (es normal justo después de escanear)...');
                return generarQR();
            }

            reintentos++;

            if (codigo === CODIGO_SESION_CERRADA) {
                console.log('❌ La sesión guardada ya no es válida. Se borra y se pide un QR nuevo...');
                borrarSesion();
            } else if (codigo === 405) {
                console.log('⚠️  WhatsApp rechazó la conexión (405): la versión del cliente está desactualizada. Reintentando...');
            } else {
                console.log(`⚠️  Conexión cerrada (código ${codigo ?? 'desconocido'}). Reintentando...`);
            }

            if (reintentos > MAX_REINTENTOS) {
                console.log('\n🛑 No se pudo completar la vinculación después de varios intentos.');
                console.log('   Prueba lo siguiente:');
                console.log('   1) Revisa tu conexión a internet.');
                console.log('   2) Ejecuta: npm install @whiskeysockets/baileys@latest');
                console.log('   3) Ejecuta: node qr.js --reset');
                console.log('   4) Usa el código en vez del QR: node qr.js TUNUMERO');
                process.exit(1);
            }

            await esperar(3000);
            return generarQR();
        }

        if (connection === 'open') {
            console.log('\n✅ ¡VINCULACIÓN EXITOSA CON EL TELÉFONO!');
            console.log('Cerrando verificador... Ya puedes iniciar el bot con: npm start\n');
            // Pequeña espera para que las credenciales terminen de guardarse en disco
            setTimeout(() => process.exit(0), 1500);
        }
    });
}

(async () => {
    console.log('「✿」Iniciando entorno de vinculación... Esperando respuesta de WhatsApp...');
    if (reiniciarSesion) {
        borrarSesion();
        console.log('🧹 Sesión anterior eliminada.');
    }
    await generarQR();
})().catch(error => {
    console.error('🛑 Error inesperado en el verificador:', error);
    process.exit(1);
});
