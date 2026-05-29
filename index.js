const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, downloadContentFromMessage } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const { Sticker, StickerTypes } = require('wa-sticker-formatter');
process.env.FFMPEG_PATH = require('ffmpeg-static');

const { GoogleGenAI } = require('@google/genai');

const ai = new GoogleGenAI({ apiKey: "AIzaSyCJ4ek9FK4iPChSh1r-wB22fu34sY9Irjk" }); 

const RUTA_CHATS = path.join(__dirname, 'chats_activos.json');
const RUTA_DB = path.join(__dirname, 'database.json');
// ==========================================
// CONTROLADORES DE ALMACENAMIENTO
// ==========================================
function cargarDB() {
    if (!fs.existsSync(RUTA_DB)) return {};
    try { return JSON.parse(fs.readFileSync(RUTA_DB, 'utf-8')); } catch (e) { return {}; }
}

function guardarDB(data) {
    fs.writeFileSync(RUTA_DB, JSON.stringify(data, null, 4));
}

function cargarChats() {
    if (!fs.existsSync(RUTA_CHATS)) return {};
    try { 
        return JSON.parse(fs.readFileSync(RUTA_CHATS, 'utf-8')); 
    } catch (e) { 
        return {}; 
    }
}

function guardarChats(data) {
    fs.writeFileSync(RUTA_CHATS, JSON.stringify(data, null, 4));
}

const cooldownXP = new Set();

async function iniciarBot() {
    const { state, saveCreds } = await useMultiFileAuthState('sesion_whatsapp');
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true 
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('messages.upsert', async (m) => {
        const msg = m.messages[0];
        if (!msg || !msg.message) return;

        const chatJid = msg.key.remoteJid;
        const sender = msg.key.participant || chatJid;
        const pushName = msg.pushName || "Usuario";

        const tipoMensaje = Object.keys(msg.message)[0];
        let texto = "";

        if (tipoMensaje === 'conversation') {
            texto = msg.message.conversation;
        } else if (tipoMensaje === 'extendedTextMessage') {
            texto = msg.message.extendedTextMessage.text;
        }

        const citoMensaje = msg.message?.extendedTextMessage?.contextInfo?.quotedMessage;

        const chatsActivos = cargarChats();

        // ==========================================
        // COMANDOS RÁPIDOS DE ENCENDIDO / APAGADO
        // ==========================================
        if (texto === '#on' || texto === '#off') {
        
            const NUMERO_PROPIETARIO = "3228595906"; 
        
            const numeroBot = sock.user.id.split(':')[0].split('@')[0];
            const numeroSender = sender.split(':')[0].split('@')[0];
        
            const esBot = numeroBot.includes(NUMERO_PROPIETARIO);
            const esDuenio = numeroSender.includes(NUMERO_PROPIETARIO);
        
            if (!esBot && !esDuenio) {
                await sock.sendMessage(chatJid, { 
                    text: "🛑 *《 ACCESO DENEGADO 》*\n\nNo tienes los permisos místicos necesarios. Solo el **propietario del bot** puede encender o apagar mis funciones." 
                }, { quoted: msg });
                return; 
            }
        
            if (texto === '#on') {
                chatsActivos[chatJid] = true;
                guardarChats(chatsActivos);
                await sock.sendMessage(chatJid, { text: "✨ *¡Bot activado con éxito!* Las funciones místicas están listas para este chat." }, { quoted: msg });
                return;
            }
        
            if (texto === '#off') {
                if (chatsActivos[chatJid]) {
                    delete chatsActivos[chatJid];
                    guardarChats(chatsActivos);
                }
                await sock.sendMessage(chatJid, { text: "💤 *¡Bot apagado!* Me iré a dormir en este chat hasta que vuelvas a usar `#on`." }, { quoted: msg });
                return;
            }
        }

        if (!chatsActivos[chatJid]) return;

        // ==========================================
        // ASIGNACIÓN Y GESTIÓN DE XP (SISTEMA DE EXPERIENCIA)
        // ==========================================
        if (texto && !texto.startsWith('#')) {
            if (!cooldownXP.has(sender)) {
                const db = cargarDB();
                
                if (!db[sender]) {
                    db[sender] = { nombre: pushName, billetera: 0, banco: 0, inventario: {} };
                }
                
                let usuario = db[sender];
                if (!usuario.nivel) usuario.nivel = 1;
                if (!usuario.xp) usuario.xp = 0;
                if (!usuario.nombre) usuario.nombre = pushName;

                const xpGanada = Math.floor(Math.random() * (25 - 15 + 1)) + 15;
                usuario.xp += xpGanada;

                const xpRequerida = usuario.nivel * 1000;

                if (usuario.xp >= xpRequerida) {
                    usuario.xp -= xpRequerida;
                    usuario.nivel += 1;

                    const textoLevelUp = `⚡ *¡LEVEL UP MULTIVERSAL!* ⚡\n\n👤 *Usuario:* @${usuario.nombre}\n✨ ¡Has ascendido al **Nivel ${usuario.nivel}**!\n\n> _Sigue interactuando para desbloquear más poder místico._`;
                    await sock.sendMessage(chatJid, { text: textoLevelUp }, { quoted: msg });
                }

                guardarDB(db);

                cooldownXP.add(sender);
                setTimeout(() => {
                    cooldownXP.delete(sender);
                }, 60000);
            }
        }

        if (!texto.startsWith('#')) return;

        const comando = texto.trim().split(/ +/)[0].toLowerCase();
        const args = texto.trim().split(/ +/).slice(1);

        // ==========================================
        // SISTEMA DE STICKERS MULTIMEDIA (#s | #sticker)
        // ==========================================
        if (comando === '#s' || comando === '#sticker') {
            let mensajeMultimedia = null;
            let tipoMime = '';

            if (msg.message?.imageMessage || msg.message?.videoMessage) {
                mensajeMultimedia = msg.message?.imageMessage || msg.message?.videoMessage;
                tipoMime = msg.message?.imageMessage ? 'image' : 'video';
            } else if (citoMensaje?.imageMessage || citoMensaje?.videoMessage) {
                mensajeMultimedia = citoMensaje.imageMessage || citoMensaje.videoMessage;
                tipoMime = citoMensaje.imageMessage ? 'image' : 'video';
            }

            if (!mensajeMultimedia) {
                await sock.sendMessage(chatJid, { text: "《✧》Debes enviar una imagen o video corto junto al comando, o responder a uno existente." }, { quoted: msg });
                return;
            }

            if (tipoMime === 'video' && mensajeMultimedia.seconds > 10) {
                await sock.sendMessage(chatJid, { text: "《✧》El video es demasiado largo. Debe durar menos de 10 segundos para convertirse en sticker animado." }, { quoted: msg });
                return;
            }

            try {
                await sock.sendMessage(chatJid, { text: '⏳ _Creando tu sticker místico, un momento..._' }, { quoted: msg });

                const stream = await downloadContentFromMessage(mensajeMultimedia, tipoMime);
                let buffer = Buffer.from([]);
                for await (const chunk of stream) {
                    buffer = Buffer.concat([buffer, chunk]);
                }

                const stickerMistico = new Sticker(buffer, {
                    pack: 'CielBot Gacha 🔮',
                    author: `${pushName}`,
                    type: StickerTypes.FULL,
                    quality: 60 
                });

                const bufferSticker = await stickerMistico.toBuffer();
                
                
                await sock.sendMessage(chatJid, { 
                    sticker: bufferSticker
                }, { 
                    quoted: msg,
                    mimetype: 'image/webp'
                });

            } catch (error) {
                console.error('Error al generar el sticker:', error);
                await sock.sendMessage(chatJid, { text: '❌ Ocurrió un error mágico al intentar procesar el archivo multimedia.' }, { quoted: msg });
            }
            return;
        }

        // ==========================================
        // PROCESAMIENTO DE GEMINI AI (#ciel)
        // ==========================================
        if (texto.toLowerCase().startsWith('#ciel ')) {
            const pregunta = texto.substring(6).trim();
            
            if (!pregunta) {
                await sock.sendMessage(chatJid, { text: "《✧》Dime, ¿qué duda mística deseas que resuelva hoy?" }, { quoted: msg });
                return;
            }

            try {
                await sock.sendPresenceUpdate('composing', chatJid);

                const response = await ai.models.generateContent({
                    model: 'gemini-2.5-flash',
                    contents: pregunta,
                    config: {
                        systemInstruction: "Eres Ciel, un asistente místico, inteligente, astuto y con un toque de ingenio. Responde de forma clara, carismática and concisa."
                    }
                });

                const respuestaIA = response.text;
                await sock.sendMessage(chatJid, { text: respuestaIA }, { quoted: msg });
            } catch (error) {
                const errorTexto = error.message || String(error);
                const esLimiteCuota = errorTexto.includes("429") || errorTexto.includes("RESOURCE_EXHAUSTED");

                if (esLimiteCuota) {
                    console.warn("⚠️ [CUOTA] Se alcanzó el límite de solicitudes gratuitas en Gemini.");
                    await sock.sendMessage(chatJid, { 
                        text: "⏳ *[Mente Saturada]* He respondido muchas preguntas seguidas. Mi energía mística necesita descansar unos segundos antes de continuar con `#Ciel`." 
                    }, { quoted: msg });
                } else {
                    console.error("Error crítico al consultar Gemini AI:", error);
                    await sock.sendMessage(chatJid, { text: "❌ Hubo un error cósmico al intentar conectar con mi matriz de pensamiento artificial." }, { quoted: msg });
                }
            }
            return; 
        }
        
        // ==========================================
        // ENRUTADOR HACIA PYTHON (main.py)
        // ==========================================
        const comandoPython = `python3 main.py "${sender}" "${pushName}" "${texto}" "${chatJid}"`;
        
        exec(comandoPython, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error ejecutando Python: ${error}`);
                return;
            }
            if (stderr) {
                console.error(`Python Stderr: ${stderr}`);
            }
            
            const respuestaRaw = stdout.trim();
            if (!respuestaRaw) return;
            // ==========================================
            // VISOR MULTIMEDIA
            // ==========================================
            if (respuestaRaw.includes('|')) {
                const partes = respuestaRaw.split('|');
                const mensajeTexto = partes[0];
                const nombreMultimedia = partes[1].trim().toLowerCase();
                
                if (!nombreMultimedia) {
                    sock.sendMessage(chatJid, { text: mensajeTexto }, { quoted: msg });
                    return;
                }

                const rutaArchivo = path.join(__dirname, 'imagenes', nombreMultimedia);

                if (fs.existsSync(rutaArchivo)) {
                    if (nombreMultimedia.endsWith('.mp4')) {
                        const esDescarga = nombreMultimedia.includes('descarga');

                        sock.sendMessage(chatJid, {
                            video: fs.readFileSync(rutaArchivo),
                            caption: mensajeTexto,
                            gifPlayback: !esDescarga 
                        }, { quoted: msg });
                    } 
                    else if (nombreMultimedia.endsWith('.mp3')) {
                        sock.sendMessage(chatJid, {
                            audio: fs.readFileSync(rutaArchivo),
                            mimetype: 'audio/mp4',
                            ptt: false 
                        }, { quoted: msg });
                    }
                    else {
                        sock.sendMessage(chatJid, {
                            image: fs.readFileSync(rutaArchivo),
                            caption: mensajeTexto
                        }, { quoted: msg });
                    }
                }
                else {
                    sock.sendMessage(chatJid, { text: mensajeTexto }, { quoted: msg });
                }
            } 
            else {
                sock.sendMessage(chatJid, { text: respuestaRaw }, { quoted: msg });
            }
        });
    });

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect } = update;
        
        if (connection === 'close') {
            const codigoRazon = lastDisconnect.error?.output?.statusCode;
            const mensajeError = lastDisconnect.error?.output?.payload?.message || "Desconocido";
            
            console.log(`⚠️ [CONEXIÓN] Conexión cerrada. Razón: ${mensajeError} (Código: ${codigoRazon})`);
            
            const sesionCerradaPorUsuario = codigoRazon === DisconnectReason.loggedOut;
            
            if (!sesionCerradaPorUsuario) {
                console.log("🔄 [SISTEMA] Intentando reconexión mística automática en 5 segundos...");
                setTimeout(() => {
                    iniciarBot();
                }, 5000); 
            } else {
                console.log("❌ [ALERTA] La sesión fue cerrada desde el teléfono. Borra 'sesion_whatsapp' y usa qr.js");
            }
        } else if (connection === 'open') {
            console.log('✨ ¡Conexión mística establecida con éxito en WhatsApp!');
        }
    });
}

iniciarBot();