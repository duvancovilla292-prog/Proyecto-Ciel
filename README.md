# 🌟 Ciel Bot Místico - Documentación y Guía del Repositorio

> **Bot modular de automatización y entretenimiento para WhatsApp** impulsado con economía virtual, sistema Gacha de personajes de anime/ciencia, reacciones multimedia interactivas y motor de descargas de redes sociales.

---

## 📋 Tabla de Contenidos
1. [Descripción General](#-descripción-general)
2. [Estructura y Arquitectura del Repositorio](#-estructura-y-arquitectura-del-repositorio)
3. [Explicación Detallada de Archivos](#-explicación-detallada-de-archivos)
4. [Relación e Interconexión entre Módulos](#-relación-e-interconexión-entre-módulos)
5. [Método de Instalación y Despliegue](#-método-de-instalación-y-despliegue)
6. [Alternativas sin `sudo`](#-alternativas-sin-permisos-de-administrador-sin-sudo)
7. [Solución de Problemas](#️-solución-de-problemas)
8. [Recomendaciones de Seguridad](#-recomendaciones-de-seguridad)

---

## 🎯 Descripción General

**Ciel Bot Místico** es un proyecto de desarrollo backend en Python diseñado para operar como un bot interactivo multifuncional. Su arquitectura se divide de manera modular para separar la lógica de negocio económica, la invocación de coleccionables (*Gacha*), la manipulación multimedia orientada a redes sociales y las respuestas visuales de rol/anime con envío automático de imágenes locales.

---

## 📂 Estructura y Arquitectura del Repositorio

El proyecto combina un **cliente de WhatsApp en Node.js** (que recibe los mensajes) con **módulos de lógica en Python** (que procesan los comandos). Los datos se guardan en **Firebase Firestore**.

```text
📦 Proyecto-Ciel/
 ┣ 📜 index.js           # Cliente de WhatsApp (Baileys): recibe mensajes, #on/#off, stickers, #ciel (Gemini) y llama a main.py.
 ┣ 📜 qr.js              # Vinculación inicial con WhatsApp (genera el QR y guarda la sesión).
 ┣ 📧 correoQR.js        # Envía el QR por correo cuando el bot corre sin terminal (Render).
 ┣ 📜 main.py            # Enrutador en Python: conecta con Firestore y deriva cada comando al módulo correcto.
 ┣ 📜 economia.py        # Núcleo financiero, minijuegos y comandos globales.
 ┣ 📜 gacha.py           # Sistema de invocación, inventario, mercado y colección de personajes.
 ┣ 📜 anime.py           # Reacciones sociales y de rol con imágenes/videos.
 ┣ 📜 perfil.py          # Perfil de usuario.
 ┣ 📜 descargador.py     # Descargas multimedia (YouTube, TikTok, Instagram, Facebook).
 ┣ 📜 package.json       # Dependencias de Node.js (npm start → node index.js).
 ┣ 📜 requirements.txt   # Dependencias de Python.
 ┣ 🐳 Dockerfile         # Despliegue en contenedor (Node 20 + Python 3 + FFmpeg).
 ┣ 🚫 .gitignore         # Evita subir sesión de WhatsApp, .env, clave de Firebase, node_modules, etc.
 ┣ 🚫 .dockerignore      # Evita copiar sesión, clave de Firebase y secretos dentro de la imagen.
 ┣ 📁 imagenes/          # Recursos multimedia (personajes y reacciones).
 ┗ 📁 descargas/         # Videos y audios descargados (se crea sola; temporal).
```

---

## 🔍 Explicación Detallada de Archivos

### 1. `economia.py` — El Corazón Financiero y Central
* **¿Qué hace?** Actúa como el controlador principal del sistema. Gestiona la base de datos en memoria/diccionarios de los usuarios, controla los tiempos de espera (*cooldowns*) de los comandos de trabajo y delitos, administra los saldos en efectivo y banco, y aloja la tabla general de ayuda (`#help`) y comandos del sistema central (`#on`, `#off`).
* **Funciones Clave:**
  * `#work`, `#slut`, `#crime`: Mecánicas de obtención de recursos económicos con validación estricta de marcas de tiempo (*timestamps*).
  * `#deposit` / `#withdraw`: Métodos de seguridad financiera para resguardar las *Coins* frente al comando de asalto (`#rob`).
  * Apuestas y Minijuegos: `#cf` (Coinflip) y `#rt` (Ruleta).
* **Dependencia cruzada:** Conecta directamente con las estructuras de datos globales del usuario para actualizar su estado financiero y actúa como router centralizador para otros módulos.

### 2. `anime.py` — Módulo de Reacciones y Rol Interactivo
* **¿Qué hace?** Controla un catálogo masivo de más de 50 comandos de rol y reacciones sociales (*anime/emotes*) como `#hug`, `#kiss`, `#slap`, `#pat`, `#bored`, entre otros.
* **Lógica interna:**
  * Contiene el diccionario `TABLERO_REACCIONES` que mapea cada comando con su respectiva frase descriptiva en solitario, su frase dirigida a una mención (`@target`) y el prefijo de archivo multimedia asociado.
  * Escanea la carpeta `imagenes/` de manera dinámica buscando un archivo que coincida con el prefijo de la reacción elegida utilizando la librería nativa `os` y selecciona uno al azar mediante `random.choice()`.
* **Relación con otros archivos:** Trabaja de la mano con `economia.py` al recibir el objeto de base de datos del usuario emisor para extraer su nombre y procesar menciones a otros usuarios dentro del chat.

### 3. `descargador.py` — Motor de Descargas de Redes Sociales
* **¿Qué hace?** Gestiona la extracción y descarga de contenido multimedia externo (videos epios/mp3) utilizando la robusta librería `yt_dlp`.
* **Funciones Clave:**
  * `descargar_youtube(args, es_audio)`: Realiza búsquedas directas en YouTube o procesa enlaces URL para convertirlos a audio `.mp3` (mediante FFmpeg) o video `.mp4`.
  * `descargar_tiktok(link, pushName)`: Extrae videos libres de marca de agua desde TikTok.
  * `descargar_redes_sociales(link)`: Automatiza la descarga de Reels y videos públicos de Facebook e Instagram.
* **Relación con otros archivos:** Los archivos descargados se almacenan temporalmente en la carpeta `descargas/` para que el bot principal pueda adjuntarlos y enviarlos en la respuesta de WhatsApp.

### 4. `gacha.py` — Sistema de Invocación Coleccionable
* **¿Qué hace?** Implementa un sistema completo de tipo *Gacha* donde los usuarios pueden gastar sus *Coins* ganadas en `economia.py` para invocar personajes coleccionables de diferentes universos (*Tensura, Solo Leveling, Dr. Stone, Jujutsu Kaisen*, etc.).
* **Estructura:**
  * `CATALOGO_PERSONAJES`: Diccionario estructurado por rarezas (*Legendario, Épico, Raro, Común*) con sus respectivos multiplicadores de puntos, valor de venta en el mercado y descripciones lore.
  * `PRODUCTOS_TIENDA`: Ítems especiales como *Tickets Épicos* y *Amuletos de Suerte*.
* **Funciones Clave:** `#gacha` (tiradas aleatorias con probabilidades ponderadas), `#chars` (paginación de inventario), `#vender` (reciclaje de copias duplicadas por *Coins*), `#regalar` (transferencia de personajes entre usuarios) y `#gtop` (tabla de clasificación global de coleccionistas).
* **Relación con otros archivos:** Modifica directamente la billetera del usuario (restando el costo del tiro o sumando el reembolso por venta) administrada en `economia.py` y utiliza recursos de imagen locales del repositorio.

---

## 🔗 Relación e Interconexión entre Módulos

```mermaid
graph TD
    A[economia.py / Núcleo Central] -->|Valida saldo y Cooldowns| B[gacha.py / Sistema Coleccionable]
    A -->|Procesa nombres y base de datos| C[anime.py / Reacciones Sociales]
    D[descargador.py / yt-dlp] -->|Guarda archivos multimedia| E[(Carpeta descargas/)]
    C -->|Lee prefijos y archivos| E
    Gacha[gacha.py] -->|Lee avatares de personajes| E
```

* **Flujo Financiero:** El usuario genera ingresos trabajando o cometiendo delitos en `economia.py`. Con esas *Coins*, puede gastar capital en tiradas dentro de `gacha.py`.
* **Flujo Multimedia:** `anime.py` lee del sistema de archivos local (`imagenes/`) y `descargador.py` guarda en `descargas/` para suministrar recursos visuales enriquecidos al chat.

---

## ⚙️ Método de Instalación y Despliegue

Guía paso a paso para poner el bot en marcha desde cero.

### 📌 Cómo funciona el arranque (léelo primero)
1. `index.js` (Node) se conecta a WhatsApp y a Firebase (Firestore).
2. Cada mensaje que empieza con `#` se envía a Python ejecutando `python3 main.py ...`.
3. `main.py` consulta Firestore, ejecuta el comando y devuelve la respuesta a Node.

Por eso necesitas **Node.js y Python instalados a la vez**, y los dos deben poder conectarse a la **misma base de datos**.

### ✅ Requisitos previos
| Herramienta | Versión | Para qué sirve |
|---|---|---|
| Node.js | 20 o superior | Cliente de WhatsApp (`index.js`) |
| Python | 3.10 o superior | Lógica de comandos (`main.py`) |
| FFmpeg | cualquiera reciente, en el `PATH` | Convertir audio/video en `descargador.py` |
| Git | cualquiera | Clonar el repositorio |
| Cuenta de Google / Firebase | plan gratuito (Spark) | Base de datos Firestore en la nube |
| Un número de WhatsApp | — | La cuenta que será el bot |
| API Key de Google Gemini *(opcional)* | — | Solo para el comando `#ciel` |

> ⚠️ El código usa el comando `python3`. En **Linux, macOS, Termux o WSL** funciona directo. En **Windows nativo** usa WSL o Docker (ver Paso 10).

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/duvancovilla292-prog/Proyecto-Ciel.git
cd Proyecto-Ciel
```
*(Ajusta la URL al nombre real de tu repositorio.)*

### Paso 2: Instalar dependencias de Node.js
```bash
npm install
```

### Paso 3: Instalar dependencias de Python
Crea un entorno virtual y actívalo:
```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS / Termux
# venv\Scripts\activate         # Windows (CMD / PowerShell)

pip install -r requirements.txt
```
Esto instala `yt-dlp`, `requests` y `firebase-admin`.

> 💡 **Importante:** como Node llama a `python3`, el entorno virtual debe estar **activado en la misma terminal** donde luego ejecutes `npm start`. Si no, verás `ModuleNotFoundError: No module named 'firebase_admin'`.

### Paso 4: Instalar FFmpeg
```bash
# Ubuntu / Debian / WSL
sudo apt update && sudo apt install -y ffmpeg
# Termux
pkg install ffmpeg
# macOS
brew install ffmpeg
```
Comprueba con `ffmpeg -version`.

> 🔓 **¿No tienes permisos de administrador?** Mira la sección [Alternativas sin `sudo`](#-alternativas-sin-permisos-de-administrador-sin-sudo) más abajo.

### Paso 5: Crear tu base de datos en Firebase (Firestore)
1. Entra a [console.firebase.google.com](https://console.firebase.google.com) y crea un proyecto (puedes desactivar Google Analytics).
2. En el menú **Build → Firestore Database → Create database**. Elige una ubicación cercana y el modo **producción** (el bot usa el Admin SDK, que no depende de las reglas).
3. Ve a **⚙️ Configuración del proyecto → Cuentas de servicio → Generar nueva clave privada**. Se descarga un archivo `.json`.
4. Guárdalo como `firebase-key.json` en la raíz del proyecto (el `.gitignore` y el `.dockerignore` ya lo excluyen) o en cualquier carpeta fuera del repositorio. El bot te pedirá su **ruta** al iniciarlo (Paso 9).

> 🔐 **La clave JSON da acceso total a tu proyecto de Firebase: nunca la subas a GitHub ni la compartas.** La API Key de Gemini sí se escribe por terminal y vive solo en la memoria del proceso.

Las colecciones (`sistema_economia`, `chats_activos`, `usuarios_niveles`) se crean solas la primera vez que el bot guarda datos.

### Paso 6: Tener lista tu API Key de Gemini *(opcional, solo para `#ciel`)*
Genera una API Key gratuita en [Google AI Studio](https://aistudio.google.com/apikey). El bot te la pedirá en la terminal al iniciar (Paso 9). Si presionas **Enter** sin escribir nada, el bot funciona igual, pero `#ciel` queda desactivado.

### Paso 7: Configurar el propietario del bot
Los comandos `#on` y `#off` solo los puede ejecutar el **propietario**. En `index.js`, dentro del bloque `#on / #off`, cambia el arreglo `ADMINS_FIJOS` por **tu número** (con código de país, sin `+`):
```js
const ADMINS_FIJOS = ["57TUNUMERO", "TUNUMERO"];
```
Los mensajes enviados desde la propia cuenta vinculada (`fromMe`) también se aceptan.

### Paso 8: Vincular WhatsApp (se hace una sola vez)
Hay dos formas. Usa la que prefieras:

**Opción A: Código QR**
```bash
node qr.js
```
1. Aparecerá un **código QR** en la terminal (se renueva solo cada ~20 segundos).
2. En el celular: **WhatsApp → Ajustes → Dispositivos vinculados → Vincular un dispositivo**.
3. Escanea el QR.

**Opción B: Código de 8 caracteres (si el QR no se ve bien o no puedes escanearlo)**
```bash
node qr.js 573001234567
```
Cambia el número por el de la cuenta que será el bot (con código de país, sin `+`). Aparecerá un código como `ABCD-1234`. En el celular: **Dispositivos vinculados → Vincular un dispositivo → Vincular con el número de teléfono** y escribe el código.

En ambos casos, al terminar verás `✅ ¡VINCULACIÓN EXITOSA CON EL TELÉFONO!`.

Si quedó una sesión dañada de un intento anterior, empieza de cero con:
```bash
node qr.js --reset
```

Se crea la carpeta `sesion_whatsapp/` con tu sesión. **No la subas a GitHub ni la compartas** (da acceso total a la cuenta; el `.gitignore` ya la excluye).

### Paso 9: Iniciar el bot
Con el entorno virtual activado, en una **terminal interactiva**:
```bash
npm start
```
El bot te pedirá la ruta de la clave de Firebase (se ve al escribirla) y la API Key de Gemini (no se muestra, solo aparecen `*`):
```text
🔐 [CONFIG] Ingresa tus credenciales. La API Key de Gemini no se guarda en ningún archivo.
🔥 Ruta del JSON de Firebase (cuenta de servicio): ./firebase-key.json
🤖 Gemini API Key (Enter para omitir, desactiva #ciel): *********
✅ [CONFIG] Credenciales cargadas. Firebase: tu-proyecto | Gemini: activado
```
* Pega el valor con **clic derecho / Ctrl+Shift+V** (en Termux, mantén presionado → *Pegar*) y presiona **Enter**.
* Si el archivo no existe o no es una clave de cuenta de servicio de Firebase, te vuelve a pedir la ruta.
* Para no escribir la ruta en cada inicio, expórtala antes: `export FIREBASE_KEY_PATH="$PWD/firebase-key.json"`. La API Key de Gemini se pide en cada reinicio (así no queda guardada).

Después debes ver `🔮 [DATABASE] ¡Conexión establecida con Firebase Firestore!`.

Luego, **en cada chat o grupo donde quieras usarlo**, envía:
```text
#on
```
Prueba con `#help`, `#work` o `#gacha`. Para apagarlo en un chat: `#off`.

### 🔓 Alternativas para activar el bot sin `#on` (sin comandos de admin)

El bot solo responde en los chats que estén marcados como activos en Firestore (colección `chats_activos`). `#on` es solo una forma de crear ese registro; estas son otras:

#### Opción A: Activar el chat directamente en Firebase Console (sin tocar código)
1. Averigua el ID del chat (`chatJid`). Los grupos terminan en `@g.us` y los chats privados en `@s.whatsapp.net` o `@lid`. Para verlo, quita los `//` de esta línea de `index.js` (busca `[MENSAJE]`) y envía cualquier mensaje al chat:
   ```js
   console.log(`💬 [MENSAJE] De: ${pushName} | ID: ${sender} | Chat: ${chatJid} | Texto: "${texto}"`);
   ```
2. En Firebase Console ve a **Firestore Database → Data → chats_activos → Add document**. Como *Document ID* pon el `chatJid` y agrega dos campos:
   ```text
   Document ID: 120363000000000000@g.us
   chatJid  (string)  = 120363000000000000@g.us
   activo   (boolean) = true
   ```
3. El bot lee la colección en cada mensaje, así que **no necesitas reiniciarlo**.

Para desactivar el chat, elimina ese documento (o usa `#off`).

#### Opción B: Script de activación por terminal
Crea un archivo `activar.js` en la raíz del proyecto:
```js
const admin = require('firebase-admin');
const fs = require('fs');

const rutaClave = process.env.FIREBASE_KEY_PATH; // ruta del JSON de Firebase, no va en el archivo
const chatJid = process.argv[2];

if (!chatJid || !rutaClave) {
    console.log('Uso: FIREBASE_KEY_PATH=./firebase-key.json node activar.js <chatJid>');
    process.exit(1);
}

(async () => {
    admin.initializeApp({ credential: admin.credential.cert(JSON.parse(fs.readFileSync(rutaClave, 'utf8'))) });
    await admin.firestore().collection('chats_activos').doc(chatJid).set({ chatJid, activo: true });
    console.log(`✅ Chat activado: ${chatJid}`);
    await admin.app().delete();
})();
```
Uso:
```bash
export FIREBASE_KEY_PATH="$PWD/firebase-key.json"
node activar.js 120363000000000000@g.us
```

#### Opción C: Activar todos los chats automáticamente (cambio de código)
Útil si el bot es solo para ti o para pruebas. En `index.js` busca:
```js
if (!chatsActivos[chatJid]) return;
```
y cámbialo por:
```js
if (process.env.ACTIVAR_TODOS !== 'true' && !chatsActivos[chatJid]) return;
```
Luego inicia el bot así:
```bash
ACTIVAR_TODOS=true npm start
```
> ⚠️ Con esta opción el bot responderá en **todos** los chats y grupos de la cuenta vinculada, incluidos los de otras personas.

#### Opción D: Permitir `#on` / `#off` a los admins del grupo
Si quieres que cualquier admin de WhatsApp del grupo pueda usarlos (no solo el propietario), en `index.js` agrega **dentro del bloque `#on / #off`**, antes de `if (!esEnviadoPorMi && !esAdminEnGrupo)`, la consulta de admins del grupo con `sock.groupMetadata(chatJid)` y compara el `sender` con los participantes cuyo `admin` sea `'admin'` o `'superadmin'`.

| Opción | Requiere tocar código | Quién activa | Mejor para |
|---|---|---|---|
| A: Firebase Console | No | Tú, desde la consola | Activar pocos chats rápido |
| B: `activar.js` | Archivo nuevo | Tú, desde terminal | Automatizar varios chats |
| C: `ACTIVAR_TODOS` | 1 línea | Automático | Pruebas personales |
| D: Admins de grupo | Sí | Admins del grupo | Grupos con varios moderadores |

---

### Paso 10: Alternativa con Docker
El `Dockerfile` ya incluye Node 20, Python 3 y FFmpeg.
```bash
docker build -t ciel-bot .

# Vincular WhatsApp (una sola vez, guarda la sesión en tu máquina)
docker run -it --rm -v "$(pwd)/sesion_whatsapp:/app/sesion_whatsapp" ciel-bot node qr.js

# OPCIÓN 1 — Interactivo: el bot te pide la ruta de la clave (escribe /app/firebase-key.json) y la API Key
docker run -it --name ciel-bot \
  -v "$(pwd)/sesion_whatsapp:/app/sesion_whatsapp" \
  -v "$(pwd)/firebase-key.json:/app/firebase-key.json:ro" ciel-bot
# (para dejarlo corriendo y salir sin apagarlo: Ctrl+P y luego Ctrl+Q)

# OPCIÓN 2 — Segundo plano: la clave de Firebase se monta como archivo y la API Key la escribes (oculta) en tu terminal
read -rsp "GEMINI_API_KEY (Enter para omitir): " GEMINI_API_KEY; echo; export GEMINI_API_KEY
docker run -d --name ciel-bot --restart unless-stopped \
  -e FIREBASE_KEY_PATH=/app/firebase-key.json -e GEMINI_API_KEY \
  -v "$(pwd)/firebase-key.json:/app/firebase-key.json:ro" \
  -v "$(pwd)/sesion_whatsapp:/app/sesion_whatsapp" ciel-bot
```
> Con `--restart`, si el contenedor se reinicia solo (por ejemplo al reiniciar el servidor) conserva la configuración con la que se creó; la API Key de Gemini queda en la configuración del contenedor (visible con `docker inspect`), no en la imagen. La clave de Firebase nunca entra en la imagen: se monta como archivo de solo lectura. Con la Opción 1 no queda nada guardado, pero tendrás que escribir la API Key en cada reinicio.
>
> En plataformas en la nube que no permiten montar archivos, puedes pasar el contenido completo del JSON en la variable `FIREBASE_CREDENTIALS` (el bot la acepta en lugar de la ruta).

Ver los logs: `docker logs -f ciel-bot`.

---

### Paso 11: Vincular WhatsApp en Render (sin terminal)
En Render no hay terminal, así que el QR dibujado en los logs se ve mal. Hay dos formas de vincular; elige una.

#### Opción A (recomendada): código de 8 caracteres
Se lee como texto en los logs, no necesita correo y dura más que el QR.

1. En Render → **Environment Variables** agrega tu número de WhatsApp **con código de país y sin `+` ni espacios**:
   ```text
   WA_NUMERO = 573001234567
   ```
2. Guarda y despliega. En los **Logs** aparecerá algo así:
   ```text
   🔑 [SISTEMA] Sesión no vinculada. Tu código de vinculación es:

           ABCD-EFGH
   ```
3. En el celular: **WhatsApp → Ajustes → Dispositivos vinculados → Vincular un dispositivo → "Vincular con el número de teléfono"** y escribe el código.

Si el código caduca, el bot genera uno nuevo cuando reconecta (unos minutos después). Con `WA_NUMERO` definido ya no se muestra el QR; también funciona en tu computador.

#### Opción B: el QR llega por correo
Si el bot no tiene terminal y están definidas las dos variables de abajo, **envía el QR como imagen a tu correo**. (En tu computador, con terminal, se sigue dibujando en pantalla.)

1. Crea una cuenta gratis en [resend.com](https://resend.com) con **el correo donde quieres recibir el QR** y genera una API Key en **API Keys**.
2. En Render → **Environment Variables** agrega:

| Variable | Valor |
|---|---|
| `QR_EMAIL_DESTINO` | El correo que recibirá el QR (con el remitente de prueba debe ser el mismo con el que creaste la cuenta de Resend) |
| `RESEND_API_KEY` | La API Key de Resend |
| `QR_EMAIL_REMITENTE` | *(opcional)* remitente propio si verificaste un dominio en Resend; por defecto `Ciel Bot <onboarding@resend.dev>` |

3. Guarda y despliega. Te llegará un correo con `qr-whatsapp.png` adjunto. Ábrelo **desde otra pantalla** y escanéalo con el celular.

* El QR dura menos de un minuto. Si caduca, llega otro correo unos minutos después (máximo 5 por arranque; luego hay que reiniciar el servicio).
* Se usa la API de Resend (HTTPS) y no SMTP, porque Render bloquea los puertos SMTP en los servicios gratuitos.

> ⚠️ En Render la carpeta `sesion_whatsapp/` **se borra en cada deploy o reinicio** salvo que uses un disco persistente (plan de pago) montado en esa ruta. Sin disco tendrás que vincular de nuevo cada vez.

## 🔓 Alternativas sin permisos de administrador (sin `sudo`)

Si usas un computador compartido, un hosting o un entorno donde no puedes ejecutar `sudo`, todo se puede instalar **dentro de tu carpeta de usuario**.

### Node.js sin `sudo` (con nvm)
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc          # o abre una terminal nueva
nvm install 20
nvm use 20
```
Se instala en `~/.nvm`, así que `npm install` nunca pedirá permisos. **No uses `npm install -g`**: todas las dependencias del proyecto se instalan en local con `npm install`.

### Python sin `sudo`
* Si `python3` ya está instalado, el entorno virtual del Paso 3 **no requiere administrador**.
* Si `python3 -m venv` falla con *"ensurepip is not available"* (en Debian/Ubuntu necesita el paquete `python3-venv`, que sí pide `sudo`), usa `virtualenv`:
  ```bash
  python3 -m pip install --user virtualenv
  python3 -m virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
* Si no existe Python, instala [Miniforge](https://github.com/conda-forge/miniforge) (se instala en tu carpeta de usuario) y crea el entorno con `conda create -n ciel python=3.12`.

### FFmpeg sin `sudo`
**Opción A (la más simple, ya viene resuelta): el FFmpeg que trae Node.** Al ejecutar `npm install` se descarga el paquete `ffmpeg-static`, y `index.js` lo agrega al `PATH` automáticamente al iniciar. Como Python se ejecuta desde Node, hereda ese `PATH` y `yt-dlp` encuentra FFmpeg **sin instalar nada**. Solo necesitas agregarlo a mano si ejecutas `main.py` directamente:
```bash
export PATH="$PWD/node_modules/ffmpeg-static:$PATH"
```

**Opción B: binario estático en tu carpeta personal (Linux).**
```bash
mkdir -p ~/bin && cd ~/bin
# Descarga una build estática de FFmpeg (por ejemplo desde johnvansickle.com/ffmpeg),
# descomprímela y copia el ejecutable `ffmpeg` a ~/bin
export PATH="$HOME/bin:$PATH"
```
Para que sea permanente, agrega la línea `export PATH=...` a tu `~/.bashrc`.

### Mantener el bot encendido sin `sudo` ni `systemd`
En segundo plano no hay terminal para escribir las credenciales, así que las defines **antes**, en tu terminal, y el bot las toma del entorno:
```bash
export FIREBASE_KEY_PATH="$PWD/firebase-key.json"
read -rsp "GEMINI_API_KEY (Enter para omitir): " GEMINI_API_KEY; echo; export GEMINI_API_KEY

# Con nohup (viene en cualquier Linux)
nohup npm start > bot.log 2>&1 &
tail -f bot.log          # ver los logs

# O con PM2 instalado en local (sin -g)
npm install pm2
npx pm2 start index.js --name ciel-bot
npx pm2 logs ciel-bot
```
Activa el entorno virtual de Python **antes** de lanzar cualquiera de los dos. Si usas `tmux` o `screen`, basta con ejecutar `npm start` dentro de la sesión y escribir las credenciales cuando las pida.

### Contenedores sin `sudo`
Si Docker te exige `sudo`, usa **Podman** en modo *rootless*: acepta los mismos comandos del Paso 10 cambiando `docker` por `podman`.
```bash
podman build -t ciel-bot .
podman run -it --name ciel-bot -v "$(pwd)/sesion_whatsapp:/app/sesion_whatsapp" ciel-bot
```

### Sin computador propio o sin acceso al sistema
* **Android con Termux**: no necesita root ni `sudo`. Usa `pkg install nodejs python ffmpeg git` y sigue los mismos pasos.
* **Plataformas en la nube que despliegan desde un `Dockerfile`**: no necesitas administrar el servidor. Asegúrate de que ofrezcan un **volumen persistente** para la carpeta `sesion_whatsapp/`; si no, tendrás que escanear el QR en cada reinicio.

---

## 🛠️ Solución de Problemas

| Problema | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: firebase_admin` | Entorno virtual sin activar | `source venv/bin/activate` y vuelve a ejecutar `npm start` |
| `python3: command not found` | Python no está en el PATH (Windows) | Usa WSL o Docker |
| `aquí no hay una terminal interactiva` | Lo lanzaste en segundo plano (`nohup`, PM2, Docker `-d`) sin exportar las credenciales | Exporta `FIREBASE_KEY_PATH` primero (ver *Mantener el bot encendido*) o ejecútalo en primer plano con `npm start` |
| `Error crítico al conectar a Firebase` (`5 NOT_FOUND`, `PERMISSION_DENIED`) | No creaste Firestore, la clave es de otro proyecto o la API de Firestore no está habilitada | Crea la base en **Firebase Console → Firestore Database** y usa la clave JSON del mismo proyecto |
| El bot no responde a nada | El chat no está activado | Envía `#on` desde el número propietario |
| `ACCESO DENEGADO` al usar `#on` | Tu número no está en `ADMINS_FIJOS` | Ver Paso 7 o activa el chat sin `#on` ([alternativas](#-alternativas-para-activar-el-bot-sin-on-sin-comandos-de-admin)) |
| `qr.js` no muestra el QR o se queda reintentando | Versión de WhatsApp Web desactualizada (error 405), sin internet o sesión dañada | Ejecuta `npm install @whiskeysockets/baileys@latest`, luego `node qr.js --reset`; si el QR no se ve bien usa `node qr.js TUNUMERO` |
| En Render no aparece el código de vinculación | Falta `WA_NUMERO`, el número lleva `+`/espacios o no tiene código de país | Usa solo dígitos con código de país (ej. `573001234567`) y busca `[SISTEMA]` en los logs |
| En Render no llega el correo con el QR | Faltan `QR_EMAIL_DESTINO` o `RESEND_API_KEY`, o el destino no es el correo de tu cuenta de Resend | Revisa los logs: la línea `[CORREO-QR]` muestra la respuesta de Resend (ej. `403`) |
| `Sesión cerrada` en `qr.js` | Sesión inválida | `qr.js` ya la borra solo; si persiste, `node qr.js --reset` |
| `EACCES: permission denied` en `npm` | Node instalado a nivel de sistema | No uses `sudo`: instala Node con nvm (ver [alternativas sin `sudo`](#-alternativas-sin-permisos-de-administrador-sin-sudo)) |
| Fallan `#play`, `#mp4`, `#tiktok` | FFmpeg ausente o `yt-dlp` desactualizado | Instala FFmpeg y ejecuta `pip install -U yt-dlp` |
| `#ciel` responde "Mente Saturada" | Cuota gratuita de Gemini agotada (429) | Espera unos segundos o revisa tu API Key |

---

## 🔐 Recomendaciones de Seguridad
* **La API Key de Gemini se pide por terminal al iniciar** y vive solo en la memoria del proceso. La clave de Firebase es un archivo JSON que nunca va en el código ni en git.
* **No subas la clave JSON de Firebase** (`firebase-key.json`). Si alguna vez se publicó, bórrala en Firebase Console (Configuración → Cuentas de servicio → Administrar permisos → Claves) y genera otra. Y si alguna vez publicaste una contraseña de MongoDB en el repositorio, cámbiala o elimina ese usuario en Atlas: seguirá visible en el historial de commits antiguos.
* **No subas `sesion_whatsapp/`**: quien la tenga controla la cuenta de WhatsApp del bot.
* Los datos del mensaje (`sender`, `pushName`, texto) se pasan a Python como argumentos literales con `execFile`, sin shell, para evitar la inyección de comandos.

---
> *Desarrollado con rigor técnico y optimizado para alto rendimiento.*
