const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, downloadContentFromMessage, fetchLatestBaileysVersion, Browsers } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');
const { Sticker, StickerTypes } = require('wa-sticker-formatter');
const admin = require('firebase-admin');

// FFmpeg incluido en el proyecto (ffmpeg-static): también lo ve Python (yt-dlp) sin instalar nada con sudo
const rutaFfmpeg = require('ffmpeg-static');
process.env.FFMPEG_PATH = rutaFfmpeg;
if (rutaFfmpeg) process.env.PATH = path.dirname(rutaFfmpeg) + path.delimiter + (process.env.PATH || '');

const { GoogleGenAI } = require('@google/genai');

// Gemini es opcional: si no se ingresa la API Key, solo se desactiva el comando #ciel.
// Se crea en configurarCredenciales(), después de pedir los datos por terminal.
let ai = null;

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

// Lee una línea visible (para datos que no son secretos, como la ruta de un archivo)
function leerLinea(pregunta) {
    const readline = require('readline');
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    return new Promise((resolve) => {
        rl.question(pregunta, (respuesta) => {
            rl.close();
            resolve(respuesta.trim());
        });
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
        return {};
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

async function iniciarBot() {
    await configurarCredenciales();

    const { state, saveCreds } = await useMultiFileAuthState('sesion_whatsapp');
    
    await conectarBaseDeDatos();
    let chatsActivos = await cargarChats();

    // Sin la versión actual de WhatsApp Web el servidor rechaza la conexión (error 405)
    let version;
    try {
        const info = await fetchLatestBaileysVersion();
        if (!info.error) version = info.version;
    } catch (e) {
        console.log("⚠️ [CONEXIÓN] No se pudo consultar la versión de WhatsApp Web. Se usará la incluida en Baileys.");
    }

    const loggerSilencioso = {
        level: 'silent',
        child() { return this; },
        trace() {}, debug() {}, info() {}, warn() {}, error() {}
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

        chatsActivos = await cargarChats();

        // ==========================================
        // COMANDOS RÁPIDOS DE ENCENDIDO / APAGADO
        // ==========================================
        //console.log(`💬 [MENSAJE] De: ${pushName} | ID: ${sender} | Chat: ${chatJid} | Texto: "${texto}"`);
        if (texto === '#on' || texto === '#off') {
            
            const ADMINS_FIJOS = [
                "573228595906",
                "3228595906"
            ]; 
        
            const numeroSender = sender ? sender.split(':')[0].split('@')[0] : "";
            const esEnviadoPorMi = msg.key && msg.key.fromMe === true;
            const esAdminEnGrupo = ADMINS_FIJOS.includes(numeroSender);
        
            if (!esEnviadoPorMi && !esAdminEnGrupo) {
                await sock.sendMessage(chatJid, { 
                    text: "🛑 *《 ACCESO DENEGADO 》*\n\nNo tienes los permisos místicos necesarios. Solo el **propietario del bot** puede modificar el estado del sistema." 
                }, { quoted: msg });
                return; 
            }
        
            if (texto === '#on') {
                chatsActivos[chatJid] = true;
                await guardarChat(chatJid, true);
                await sock.sendMessage(chatJid, { text: "✨ *¡Bot activado con éxito!* Las funciones místicas están listas para este chat." }, { quoted: msg });
                return;
            }
        
            if (texto === '#off') {
                if (chatsActivos[chatJid]) {
                    delete chatsActivos[chatJid];
                    await guardarChat(chatJid, false);
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
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log("\n✨ [SISTEMA] Sesión no vinculada. Escanea este QR (o usa 'node qr.js'):");
            qrcode.generate(qr, { small: true });
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
        }
    });
}

iniciarBot();