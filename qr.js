const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');

async function generarQR() {
    console.log("「✿」Iniciando entorno de vinculación... Esperando respuesta de WhatsApp...");
    
    const { state, saveCreds } = await useMultiFileAuthState('sesion_whatsapp');
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false 
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log("\n✨ [SISTEMA] ¡QR recibido místicamente! Escanéalo con tu celular:");
            
            qrcode.generate(qr, { small: true }); 
        }

        if (connection === 'close') {
            const codigoRazon = lastDisconnect.error?.output?.statusCode;
            const debeReiniciar = codigoRazon !== DisconnectReason.loggedOut;
            
            if (debeReiniciar) {
                console.log("🔄 Reintentando conexión...");
                generarQR();
            } else {
                console.log("❌ Sesión cerrada. Borra la carpeta 'sesion_whatsapp' para reintentar.");
            }
        } else if (connection === 'open') {
            console.log('\n✅ ¡VINCULACIÓN EXITOSA CON EL TELÉFONO!');
            console.log('Cerrando verificador... Ya puedes iniciar el bot con: node index.js\n');
            process.exit(0);
        }
    });
}

generarQR();