const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, downloadContentFromMessage, fetchLatestBaileysVersion, Browsers } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');
const { Sticker, StickerTypes } = require('wa-sticker-formatter');
const admin = require('firebase-admin');
const { correoQRConfigurado, enviarQRPorCorreo, reiniciarContadorQR } = require('./correoQR');
const { elegirMetodoVinculacion, obtenerMetodoVinculacion, leerLinea } = require('./vinculacion');

// FFmpeg incluido en el proyecto (ffmpeg-static): también lo ve Python (yt-dlp) sin instalar nada con sudo
const rutaFfmpeg = require('ffmpeg-static');
process.env.FFMPEG_PATH = rutaFfmpeg;
if (rutaFfmpeg) process.env.PATH = path.dirname(rutaFfmpeg) + path.delimiter + (process.env.PATH || '');

const { GoogleGenAI } = require('@google/genai');

// Gemini es opcional: si no se ingresa la API Key, solo se desactiva el comando #ciel.
// Se crea en configurarCredenciales(), después de pedir los datos por terminal.
let ai = null;

// ==========================================
// SERVIDOR WEB MÍNIMO (solo para Render y similares)
// ==========================================
// Los "Web Services" de Render exigen un puerto abierto: si no lo detectan en unos minutos,
// marcan el despliegue como fallido ("No open ports detected"). Solo se abre cuando existe la
// variable PORT (la define Render); en tu computador no se abre nada.
if (process.env.PORT) {
    require('http').createServer((req, res) => {
        res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('Ciel Bot activo');
    }).listen(Number(process.env.PORT), '0.0.0.0', () => {
        console.log(`🌐 [WEB] Puerto ${process.env.PORT} abierto (necesario en Render).`);
    });
}

// ==========================================
// CONFIGURACIÓN DE FIREBASE (FIRESTORE)
// ==========================================
let firebaseListo = false; // se activa en configurarCredenciales()

// ==========================================
// CREDENCIALES POR TERMINAL
// La API Key de Gemini se pide al iniciar y vive solo en la memoria del proceso.
// Firebase usa un archivo JSON de cuenta de servicio que tú guardas fuera de git
// (se pasa por ruta: terminal o variable FIREBASE_KEY_PATH); nunca va en el código.
// ==========================================

// Lee una línea sin mostrar lo que escribes (muestra * por cada carácter)
function leerOculto(pregunta) {
    return new Promise((resolve) => {
        const stdin = process.stdin;
        process.stdout.write(pregunta);
        stdin.setRawMode(true);
        stdin.resume();
        stdin.setEncoding('utf8');

        let valor = '';
        const terminar = () => {
            stdin.removeListener('data', alRecibir);
            stdin.setRawMode(false);
            stdin.pause();
            process.stdout.write('\n');
        };
        const alRecibir = (chunk) => {
            if (chunk.startsWith('\u001b')) return; // ignora flechas y teclas especiales
            for (const c of chunk) {
                if (c === '\r' || c === '\n') {
                    terminar();
                    return resolve(valor.trim());
                }
                if (c === '\u0003') { // Ctrl+C
                    terminar();
                    process.exit(130);
                }
                if (c === '\u007f' || c === '\b') { // borrar
                    if (valor.length > 0) {
                        valor = valor.slice(0, -1);
                        process.stdout.write('\b \b');
                    }
                    continue;
                }
                if (c < ' ') continue; // otros caracteres de control
                valor += c;
                process.stdout.write('*');
            }
        };
        stdin.on('data', alRecibir);
    });
}

// Comprueba que el JSON sea una clave de cuenta de servicio de Firebase
function esClaveFirebaseValida(cred) {
    return Boolean(cred && cred.project_id && cred.client_email && cred.private_key);
}

async function configurarCredenciales() {
    if (firebaseListo) return; // ya configuradas: los reinicios del socket no vuelven a preguntar

    const hayTerminal = Boolean(process.stdin.isTTY && process.stdout.isTTY);
    let geminiKey = process.env.GEMINI_API_KEY;
    let rutaClave = process.env.FIREBASE_KEY_PATH || process.env.GOOGLE_APPLICATION_CREDENTIALS;
    const jsonClave = process.env.FIREBASE_CREDENTIALS; // alternativa: el JSON completo en una variable (hosting/Docker)
    let credenciales = null;

    if ((!rutaClave && !jsonClave) || geminiKey === undefined) {
        if (hayTerminal) {
            console.log("\n🔐 [CONFIG] Ingresa tus credenciales. La API Key de Gemini no se guarda en ningún archivo.");
            console.log("   (La ruta de Firebase se ve al escribirla; la API Key de Gemini no. Ctrl+C para cancelar)\n");
        }
    }

    if (jsonClave) {
        try {
            credenciales = JSON.parse(jsonClave);
        } catch (error) {
            console.error("🛑 [CONFIG] FIREBASE_CREDENTIALS no contiene un JSON válido.");
            process.exit(1);
        }
    } else if (rutaClave) {
        try {
            credenciales = JSON.parse(fs.readFileSync(rutaClave, 'utf8'));
        } catch (error) {
            console.error(`🛑 [CONFIG] No pude leer la clave de Firebase en '${rutaClave}': ${error.message}`);
            process.exit(1);
        }
    } else {
        if (!hayTerminal) {
            console.error("🛑 [CONFIG] Este bot necesita la clave de Firebase al iniciar, pero aquí no hay una terminal interactiva.");
            console.error("   Define FIREBASE_KEY_PATH (ruta del JSON) o ejecútalo con 'npm start' en una terminal (consulta el README).");
            process.exit(1);
        }
        while (!credenciales) {
            let entrada = await leerLinea("🔥 Ruta del JSON de Firebase (cuenta de servicio): ");
            entrada = entrada.replace(/^["']|["']$/g, '').replace(/^~(?=$|\/)/, process.env.HOME || '~');
            try {
                const leida = JSON.parse(fs.readFileSync(entrada, 'utf8'));
                if (!esClaveFirebaseValida(leida)) throw new Error("ese JSON no parece una clave de cuenta de servicio de Firebase");
                credenciales = leida;
                rutaClave = entrada;
            } catch (error) {
                console.log(`   ⚠️  ${error.message} — inténtalo de nuevo.`);
            }
        }
    }

    if (!esClaveFirebaseValida(credenciales)) {
        console.error("🛑 [CONFIG] La clave de Firebase no es válida (faltan project_id, client_email o private_key).");
        process.exit(1);
    }

    if (geminiKey === undefined && hayTerminal) {
        geminiKey = await leerOculto("🤖 Gemini API Key (Enter para omitir, desactiva #ciel): ");
    }

    // Quedan solo en el entorno del proceso; los procesos hijos (main.py en Python) los heredan de aquí
    if (!jsonClave) process.env.FIREBASE_KEY_PATH = path.resolve(rutaClave);
    if (geminiKey) process.env.GEMINI_API_KEY = geminiKey;

    admin.initializeApp({ credential: admin.credential.cert(credenciales) });
    firebaseListo = true;
    ai = geminiKey ? new GoogleGenAI({ apiKey: geminiKey }) : null;
    console.log(`✅ [CONFIG] Credenciales cargadas. Firebase: ${credenciales.project_id} | Gemini: ${ai ? 'activado' : 'desactivado'}\n`);
}

let db, coleccionChats, coleccionNiveles;

async function conectarBaseDeDatos() {
    if (db) return; // ya conectado (evita reconectar en cada reinicio del socket)
    try {
        db = admin.firestore();
        db.settings({ ignoreUndefinedProperties: true });
        coleccionChats = db.collection('chats_activos');
        coleccionNiveles = db.collection('usuarios_niveles');
        // Prueba real de conexión: si la clave o el proyecto están mal, falla aquí y no en el primer mensaje
        await coleccionChats.limit(1).get();
        console.log("🔮 [DATABASE] ¡Conexión establecida con Firebase Firestore!");
    } catch (error) {
        db = undefined;
        console.error("🛑 [DATABASE] Error crítico al conectar a Firebase:", error.message);
        console.error("   Revisa que hayas creado la base de datos en Firebase Console → Firestore Database y que la clave JSON sea del mismo proyecto.");
        process.exit(1);
    }
}

// ==========================================
// CONTROLADORES DE ALMACENAMIENTO DE NIVELES (FIRESTORE)
// ==========================================

async function obtenerNivelUsuarioDB(senderId, pushName) {
    try {
        const ref = coleccionNiveles.doc(senderId);
        const snap = await ref.get();
        if (snap.exists) {
            return { _id: senderId, ...snap.data() };
        }
        const usuario = {
            _id: senderId,
            nombre: pushName,
            billetera: 0,
            banco: 0,
            inventario: {},
            nivel: 1,
            xp: 0
        };
        const { _id, ...datos } = usuario; // el ID ya es el nombre del documento
        await ref.set(datos);
        return usuario;
    } catch (error) {
        console.error("Error al obtener niveles de Firestore:", error);
        return { _id: senderId, nombre: pushName, billetera: 0, banco: 0, inventario: {}, nivel: 1, xp: 0 };
    }
}


async function guardarNivelUsuarioDB(usuario) {
    try {
        const { _id, ...datos } = usuario;
        // set() sin merge reemplaza el documento completo (igual que el $set anterior sobre el objeto entero)
        await coleccionNiveles.doc(_id).set(datos);
    } catch (error) {
        console.error("Error al guardar niveles en Firestore:", error);
    }
}


async function cargarChats() {
    try {
        const snapshot = await coleccionChats.get();
        const chats = {};
        snapshot.forEach(doc => {
            const datos = doc.data();
            chats[datos.chatJid || doc.id] = datos.activo;
        });
        return chats;
    } catch (error) {
        console.error("Error al cargar chats desde Firestore:", error);
        return null; // null = falló la lectura: se conserva la lista que ya estaba en memoria
    }
}


async function guardarChat(chatJid, estado) {
    try {
        const ref = coleccionChats.doc(chatJid);
        if (estado) {
            await ref.set({ chatJid: chatJid, activo: true });
        } else {
            await ref.delete();
        }
    } catch (error) {
        console.error("Error al guardar chat en Firestore:", error);
    }
}

const cooldownXP = new Set();

// WhatsApp envuelve algunos mensajes (chats con mensajes temporales, "ver una vez"...).
// Se desenvuelven para leer el contenido real y no perder el texto del comando.
function desenvolverMensaje(contenido) {
    let actual = contenido || {};
    for (let i = 0; i < 5; i++) {
        const interno = actual.ephemeralMessage?.message
            || actual.viewOnceMessage?.message
            || actual.viewOnceMessageV2?.message
            || actual.documentWithCaptionMessage?.message;
        if (!interno) break;
        actual = interno;
    }
    return actual;
}

// Si pones DEBUG_MENSAJES=true, se muestra en los logs TODO lo que le llega al bot (para diagnosticar mensajes que "no aparecen")
const MODO_DEBUG_MENSAJES = String(process.env.DEBUG_MENSAJES || '').toLowerCase() === 'true';

// Si pones CHATS_PRIVADOS_ACTIVOS=true, el bot responde en chats 1 a 1 sin necesidad de #on
const CHATS_PRIVADOS_ACTIVOS = String(process.env.CHATS_PRIVADOS_ACTIVOS || '').toLowerCase() === 'true';

async function iniciarBot() {
    await configurarCredenciales();

    const { state, saveCreds } = await useMultiFileAuthState('sesion_whatsapp');

    // Sin sesión vinculada: elegir código o QR (con terminal pregunta; sin terminal asume código)
    if (!state.creds.me) {
        await elegirMetodoVinculacion();
    }
    
    await conectarBaseDeDatos();
    let chatsActivos = (await cargarChats()) || {};
    let ultimaCargaChats = Date.now();

    // Sin la versión actual de WhatsApp Web el servidor rechaza la conexión (error 405)
    let version;
    try {
        const info = await fetchLatestBaileysVersion();
        if (!info.error) version = info.version;
    } catch (e) {
        console.log("⚠️ [CONEXIÓN] No se pudo consultar la versión de WhatsApp Web. Se usará la incluida en Baileys.");
    }

    // Baileys escribe aquí avisos y errores internos (p. ej. "failed to decrypt message").
    // Antes estaban ocultos; ahora salen resumidos. Para ocultarlos: LOG_BAILEYS=false
    const mostrarLogsBaileys = String(process.env.LOG_BAILEYS || '').toLowerCase() !== 'false';
    const registrarBaileys = (nivel) => (obj, msg) => {
        if (!mostrarLogsBaileys) return;
        const texto = typeof msg === 'string' ? msg : (typeof obj === 'string' ? obj : '');
        const detalle = obj?.err?.message || obj?.error?.message || '';
        const clave = obj?.key?.remoteJid ? ` | chat: ${obj.key.remoteJid}` : '';
        console.log(`📝 [BAILEYS-${nivel}] ${texto}${detalle ? ` → ${detalle}` : ''}${clave}`.slice(0, 300));
    };
    const loggerSilencioso = {
        level: mostrarLogsBaileys ? 'warn' : 'silent',
        child() { return this; },
        trace() {}, debug() {}, info() {},
        warn: registrarBaileys('AVISO'),
        error: registrarBaileys('ERROR')
    };

    const sock = makeWASocket({
        auth: state,
        ...(version ? { version } : {}),
        logger: loggerSilencioso,
        browser: Browsers ? Browsers.ubuntu('Chrome') : ['Ubuntu', 'Chrome', '20.0.04'],
        syncFullHistory: false,
        markOnlineOnConnect: false
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('messages.upsert', async (m) => {
        // WhatsApp puede entregar varios mensajes juntos (p. ej. al reconectar): se atienden todos
        for (const mensaje of m.messages) {
            if (MODO_DEBUG_MENSAJES) {
                console.log(`🔎 [DEBUG] llegó (${m.type}) de ${mensaje?.key?.remoteJid} | fromMe: ${Boolean(mensaje?.key?.fromMe)} | campos: ${Object.keys(mensaje?.message || {}).join(',') || '(vacío)'} | stub: ${mensaje?.messageStubType ?? '-'}`);
            }
            try {
                await procesarMensaje(mensaje);
            } catch (error) {
                console.error('Error procesando un mensaje:', error);
            }
        }
    });

    async function procesarMensaje(msg) {
        if (msg && !msg.message) {
            // Mensaje sin contenido: lo normal es que WhatsApp no pudo descifrarlo (sesión de cifrado nueva o dañada)
            if (msg.messageStubType === 2 || msg.messageStubType === 'CIPHERTEXT') {
                console.log(`⚠️ [NO DESCIFRADO] Llegó un mensaje de ${msg.key?.remoteJid} pero no se pudo leer (WhatsApp lo reintenta solo; si se repite, vuelve a vincular el bot).`);
            }
            return;
        }
        if (!msg) return;

        const chatJid = msg.key.remoteJid;
        if (!chatJid || chatJid === 'status@broadcast') return;

        const chatJidAlt = msg.key.remoteJidAlt; // WhatsApp migra a ids tipo LID: un mismo chat puede llegar con dos formatos
        const esGrupo = chatJid.endsWith('@g.us');
        const sender = msg.key.participant || chatJid;
        const pushName = msg.pushName || "Usuario";

        // El primer campo del mensaje no siempre es el texto (a veces es 'messageContextInfo'),
        // así que se busca el texto (o el pie de foto) en todos los lugares posibles
        const contenido = desenvolverMensaje(msg.message);
        let texto = contenido.conversation
            || contenido.extendedTextMessage?.text
            || contenido.imageMessage?.caption
            || contenido.videoMessage?.caption
            || contenido.documentMessage?.caption
            || "";
        texto = texto.trim();

        const contextInfo = contenido.extendedTextMessage?.contextInfo
            || contenido.imageMessage?.contextInfo
            || contenido.videoMessage?.contextInfo;
        const citoMensaje = contextInfo?.quotedMessage;

        const esComando = texto.startsWith('#');
        const textoCmd = texto.toLowerCase();

        // Muestra en la terminal (o en los logs de Render) cada mensaje dirigido al bot
        if (esComando) {
            console.log(`💬 [COMANDO] ${pushName} | ${esGrupo ? 'grupo' : 'privado'} | ${msg.key.fromMe ? 'yo' : 'otro'} | ${chatJid}${chatJidAlt ? ` (alt: ${chatJidAlt})` : ''} | "${texto.slice(0, 150)}"`);
        }

        // La lista de chats activos se guarda en memoria y se refresca cada 60 s (leer Firestore en cada mensaje gasta la cuota gratis)
        if (Date.now() - ultimaCargaChats > 60000) {
            ultimaCargaChats = Date.now();
            const cargados = await cargarChats();
            if (cargados) chatsActivos = cargados;
        }

        const chatActivo = () => Boolean(
            chatsActivos[chatJid]
            || (chatJidAlt && chatsActivos[chatJidAlt])
            || (!esGrupo && CHATS_PRIVADOS_ACTIVOS)
        );

        // ==========================================
        // COMANDOS RÁPIDOS DE ENCENDIDO / APAGADO
        // ==========================================
        //console.log(`💬 [MENSAJE] De: ${pushName} | ID: ${sender} | Chat: ${chatJid} | Texto: "${texto}"`);
        if (textoCmd === '#on' || textoCmd === '#off') {
            
            const ADMINS_FIJOS = [
                "573228595906",
                "3228595906"
            ]; 
        
            // Se revisan también los ids alternativos (LID ↔ número) por si el número del admin llega en el otro formato
            const idsSender = [sender, msg.key.participantAlt, esGrupo ? null : chatJidAlt].filter(Boolean);
            const esEnviadoPorMi = msg.key && msg.key.fromMe === true;
            const esAdminEnGrupo = idsSender.some(id => ADMINS_FIJOS.includes(id.split(':')[0].split('@')[0]));
        
            if (!esEnviadoPorMi && !esAdminEnGrupo) {
                await sock.sendMessage(chatJid, { 
                    text: "🛑 *《 ACCESO DENEGADO 》*\n\nNo tienes los permisos místicos necesarios. Solo el **propietario del bot** puede modificar el estado del sistema." 
                }, { quoted: msg });
                return; 
            }
        
            if (textoCmd === '#on') {
                chatsActivos[chatJid] = true;
                await guardarChat(chatJid, true);
                if (chatJidAlt) {
                    chatsActivos[chatJidAlt] = true;
                    await guardarChat(chatJidAlt, true);
                }
                await sock.sendMessage(chatJid, { text: "✨ *¡Bot activado con éxito!* Las funciones místicas están listas para este chat." }, { quoted: msg });
                return;
            }
        
            if (textoCmd === '#off') {
                for (const id of [chatJid, chatJidAlt].filter(Boolean)) {
                    if (chatsActivos[id]) {
                        delete chatsActivos[id];
                        await guardarChat(id, false);
                    }
                }
                await sock.sendMessage(chatJid, { text: "💤 *¡Bot apagado!* Me iré a dormir en este chat hasta que vuelvas a usar `#on`." }, { quoted: msg });
                return;
            }
        }

        if (!chatActivo()) {
            if (esComando) {
                console.log(`⏭️ [IGNORADO] Chat no activado: ${chatJid}. Escribe #on ahí${esGrupo ? '' : ' (o define CHATS_PRIVADOS_ACTIVOS=true para que los chats 1 a 1 no lo necesiten)'}.`);
            }
            return;
        }

        // ==========================================
        // ASIGNACIÓN Y GESTIÓN DE XP (SISTEMA DE EXPERIENCIA)
        // ==========================================
        if (texto && !texto.startsWith('#')) {
            if (!cooldownXP.has(sender)) {
                
                
                let usuario = await obtenerNivelUsuarioDB(sender, pushName);
                
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

                
                await guardarNivelUsuarioDB(usuario);

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

            if (contenido.imageMessage || contenido.videoMessage) {
                mensajeMultimedia = contenido.imageMessage || contenido.videoMessage;
                tipoMime = contenido.imageMessage ? 'image' : 'video';
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

            if (!ai) {
                await sock.sendMessage(chatJid, { text: "《✧》El comando `#ciel` está desactivado (no se ingresó la API Key de Gemini al iniciar el bot)." }, { quoted: msg });
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
        // execFile pasa cada dato como argumento literal (sin shell): un mensaje como
        // `#x "; rm -rf ~` ya no puede ejecutar comandos en el servidor.
        execFile('python3', ['main.py', sender, pushName, texto, chatJid], {
            cwd: __dirname,
            maxBuffer: 10 * 1024 * 1024
        }, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error ejecutando Python: ${error}`);
                return;
            }
            if (stderr) {
                console.error(`Python Stderr: ${stderr}`);
            }
            
            const respuestaRaw = stdout.trim();
            console.log(respuestaRaw
                ? `📤 [RESPUESTA] ${comando} → ${respuestaRaw.split('|')[0].replace(/\s+/g, ' ').slice(0, 80)}`
                : `📭 [SIN RESPUESTA] ${comando}: Python no devolvió nada`);
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

                // Las descargas (#play, #mp4, #tiktok...) viven en 'descargas'; las reacciones y personajes en 'imagenes'
                const esDescarga = nombreMultimedia.startsWith('descarga_');
                const rutaArchivo = path.join(__dirname, esDescarga ? 'descargas' : 'imagenes', nombreMultimedia);

                if (fs.existsSync(rutaArchivo)) {
                    if (nombreMultimedia.endsWith('.mp4')) {
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
    }

    let codigoSolicitado = false; // un código por conexión
    let avisoSinNumero = false;   // un aviso por conexión

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            const metodo = obtenerMetodoVinculacion();

            if (metodo.tipo === 'codigo' && metodo.numero) {
                // Código de emparejamiento: es texto, se lee bien en los logs de Render y dura más que el QR
                if (!codigoSolicitado) {
                    codigoSolicitado = true;
                    try {
                        const codigo = await sock.requestPairingCode(metodo.numero);
                        const bonito = codigo.match(/.{1,4}/g)?.join('-') || codigo;
                        console.log('\n🔑 [SISTEMA] Sesión no vinculada. Tu código de vinculación es:\n');
                        console.log(`        ${bonito}\n`);
                        console.log('En el celular: WhatsApp → Ajustes → Dispositivos vinculados → Vincular un dispositivo');
                        console.log('→ "Vincular con el número de teléfono" y escribe el código.\n');
                    } catch (error) {
                        console.error('🛑 [SISTEMA] No se pudo generar el código de vinculación:', error?.message || error);
                    }
                }
            } else if (metodo.tipo === 'codigo') {
                // Sin terminal y sin número: no se puede generar el código
                if (!avisoSinNumero) {
                    avisoSinNumero = true;
                    console.error('🛑 [SISTEMA] Sin terminal el bot vincula con un código de 8 caracteres, pero falta tu número.');
                    console.error('   Define la variable WA_NUMERO con tu número y código de país, sin + ni espacios (ej. 573001234567).');
                    if (correoQRConfigurado()) console.error('   Mientras tanto, te envío el QR por correo.');
                }
                // Respaldo: si configuraste el correo, el QR llega como imagen
                if (correoQRConfigurado()) await enviarQRPorCorreo(qr);
            } else {
                // Elegiste QR en tu terminal
                console.log("\n✨ [SISTEMA] Sesión no vinculada. Escanea este QR (o usa 'node qr.js'):");
                qrcode.generate(qr, { small: true });
            }
        }

        if (connection === 'close') {
            const codigoRazon = lastDisconnect?.error?.output?.statusCode;
            const mensajeError = lastDisconnect?.error?.output?.payload?.message || "Desconocido";
            
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
            reiniciarContadorQR();
        }
    });
}

iniciarBot();