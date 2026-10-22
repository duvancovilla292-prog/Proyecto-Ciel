// ==========================================
// ENVÍO DEL QR DE WHATSAPP POR CORREO (para servidores sin terminal, como Render)
//
// Usa la API de Resend por HTTPS (puerto 443), porque Render bloquea el correo
// SMTP (puertos 25, 465 y 587) en los servicios gratuitos.
//
// Variables de entorno:
//   QR_EMAIL_DESTINO   → correo al que llega el QR
//   RESEND_API_KEY     → API Key de Resend (resend.com → API Keys)
//   QR_EMAIL_REMITENTE → (opcional) remitente; por defecto 'Ciel Bot <onboarding@resend.dev>'
//
// Con el remitente de prueba (onboarding@resend.dev), Resend solo entrega al
// correo con el que creaste tu cuenta en Resend.
// ==========================================
const QRCode = require('qrcode');

const INTERVALO_MS = 90 * 1000; // mínimo entre correos (cada QR dura poco; no queremos inundar tu bandeja)
const MAX_INTENTOS = 5;         // tope de correos por arranque, hasta que WhatsApp quede vinculado

let ultimoEnvio = 0;
let intentos = 0;
let enviando = false;
let avisoTopeMostrado = false;

function correoQRConfigurado() {
    return Boolean((process.env.QR_EMAIL_DESTINO || '').trim() && (process.env.RESEND_API_KEY || '').trim());
}

async function enviarQRPorCorreo(qr) {
    if (!correoQRConfigurado() || enviando) return false;

    if (intentos >= MAX_INTENTOS) {
        if (!avisoTopeMostrado) {
            avisoTopeMostrado = true;
            console.warn(`⚠️ [CORREO-QR] Ya se enviaron ${MAX_INTENTOS} correos sin vincular. Reinicia el servicio para recibir otro.`);
        }
        return false;
    }
    if (Date.now() - ultimoEnvio < INTERVALO_MS) return false;

    enviando = true;
    ultimoEnvio = Date.now();
    intentos++;

    const destino = process.env.QR_EMAIL_DESTINO.trim();
    try {
        const png = await QRCode.toBuffer(qr, { width: 480, margin: 2 });

        const respuesta = await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${process.env.RESEND_API_KEY.trim()}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                from: (process.env.QR_EMAIL_REMITENTE || '').trim() || 'Ciel Bot <onboarding@resend.dev>',
                to: [destino],
                subject: '🔐 QR para vincular WhatsApp (Ciel Bot)',
                html: '<p>Abre la imagen adjunta <b>desde otra pantalla</b> (computador o tablet) y escanéala con tu celular:</p>'
                    + '<p><b>WhatsApp → Ajustes → Dispositivos vinculados → Vincular un dispositivo</b></p>'
                    + '<p>⏳ El QR dura menos de un minuto. Si caduca, llegará otro correo en un par de minutos.</p>',
                attachments: [{ filename: 'qr-whatsapp.png', content: png.toString('base64') }]
            })
        });

        if (!respuesta.ok) {
            const detalle = await respuesta.text();
            console.error(`🛑 [CORREO-QR] Resend respondió ${respuesta.status}: ${detalle}`);
            return false;
        }
        console.log(`📧 [CORREO-QR] QR enviado a ${destino} (${intentos}/${MAX_INTENTOS}). Escanéalo en menos de un minuto.`);
        return true;
    } catch (error) {
        console.error('🛑 [CORREO-QR] No se pudo enviar el correo:', error.message);
        return false;
    } finally {
        enviando = false;
    }
}

// Se llama cuando WhatsApp queda vinculado: el siguiente QR (si algún día hace falta) vuelve a enviarse
function reiniciarContadorQR() {
    ultimoEnvio = 0;
    intentos = 0;
    avisoTopeMostrado = false;
}

module.exports = { correoQRConfigurado, enviarQRPorCorreo, reiniciarContadorQR };
