# 🌟 Ciel Bot Místico - Documentación y Guía del Repositorio

> **Bot modular de automatización y entretenimiento para WhatsApp** impulsado con economía virtual, sistema Gacha de personajes de anime/ciencia, reacciones multimedia interactivas y motor de descargas de redes sociales.

---

## 📋 Tabla de Contenidos
1. [Descripción General](#-descripción-general)
2. [Estructura y Arquitectura del Repositorio](#-estructura-y-arquitectura-del-repositorio)
3. [Explicación Detallada de Archivos](#-explicación-detallada-de-archivos)
4. [Relación e Interconexión entre Módulos](#-relación-e-interconexión-entre-módulos)
5. [Método de Instalación y Despliegue](#-método-de-instalación-y-despliegue)
6. [Solución de Problemas](#️-solución-de-problemas)
7. [Recomendaciones de Seguridad](#-recomendaciones-de-seguridad)

---

## 🎯 Descripción General

**Ciel Bot Místico** es un proyecto de desarrollo backend en Python diseñado para operar como un bot interactivo multifuncional. Su arquitectura se divide de manera modular para separar la lógica de negocio económica, la invocación de coleccionables (*Gacha*), la manipulación multimedia orientada a redes sociales y las respuestas visuales de rol/anime con envío automático de imágenes locales.

---

## 📂 Estructura y Arquitectura del Repositorio

El proyecto combina un **cliente de WhatsApp en Node.js** (que recibe los mensajes) con **módulos de lógica en Python** (que procesan los comandos). Los datos se guardan en **MongoDB Atlas**.

```text
📦 Proyecto-Ciel/
 ┣ 📜 index.js           # Cliente de WhatsApp (Baileys): recibe mensajes, #on/#off, stickers, #ciel (Gemini) y llama a main.py.
 ┣ 📜 qr.js              # Vinculación inicial con WhatsApp (genera el QR y guarda la sesión).
 ┣ 📜 main.py            # Enrutador en Python: conecta con MongoDB y deriva cada comando al módulo correcto.
 ┣ 📜 economia.py        # Núcleo financiero, minijuegos y comandos globales.
 ┣ 📜 gacha.py           # Sistema de invocación, inventario, mercado y colección de personajes.
 ┣ 📜 anime.py           # Reacciones sociales y de rol con imágenes/videos.
 ┣ 📜 perfil.py          # Perfil de usuario.
 ┣ 📜 descargador.py     # Descargas multimedia (YouTube, TikTok, Instagram, Facebook).
 ┣ 📜 package.json       # Dependencias de Node.js (npm start → node index.js).
 ┣ 📜 requirements.txt   # Dependencias de Python.
 ┣ 🐳 Dockerfile         # Despliegue en contenedor (Node 20 + Python 3 + FFmpeg).
 ┗ 📁 imagenes/          # Recursos multimedia (personajes y reacciones).
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
* **Relación con otros archivos:** Los archivos descargados se almacenan temporalmente en la carpeta `imagenes/` para que el bot principal pueda adjuntarlos y enviarlos en la respuesta de WhatsApp.

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
    D[descargador.py / yt-dlp] -->|Guarda archivos multimedia| E[(Carpeta imagenes/)]
    C -->|Lee prefijos y archivos| E
    Gacha[gacha.py] -->|Lee avatares de personajes| E
```

* **Flujo Financiero:** El usuario genera ingresos trabajando o cometiendo delitos en `economia.py`. Con esas *Coins*, puede gastar capital en tiradas dentro de `gacha.py`.
* **Flujo Multimedia:** Tanto `anime.py` como `descargador.py` interactúan directamente con el sistema de archivos local (`imagenes/`) para suministrar recursos visuales enriquecidos al chat.

---

## ⚙️ Método de Instalación y Despliegue

Guía paso a paso para poner el bot en marcha desde cero.

### 📌 Cómo funciona el arranque (léelo primero)
1. `index.js` (Node) se conecta a WhatsApp y a MongoDB.
2. Cada mensaje que empieza con `#` se envía a Python ejecutando `python3 main.py ...`.
3. `main.py` consulta MongoDB, ejecuta el comando y devuelve la respuesta a Node.

Por eso necesitas **Node.js y Python instalados a la vez**, y los dos deben poder conectarse a la **misma base de datos**.

### ✅ Requisitos previos
| Herramienta | Versión | Para qué sirve |
|---|---|---|
| Node.js | 20 o superior | Cliente de WhatsApp (`index.js`) |
| Python | 3.10 o superior | Lógica de comandos (`main.py`) |
| FFmpeg | cualquiera reciente, en el `PATH` | Convertir audio/video en `descargador.py` |
| Git | cualquiera | Clonar el repositorio |
| Cuenta de MongoDB Atlas | plan gratuito (M0) | Base de datos en la nube |
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
Esto instala `yt-dlp`, `requests`, `pymongo` y `certifi`.

> 💡 **Importante:** como Node llama a `python3`, el entorno virtual debe estar **activado en la misma terminal** donde luego ejecutes `npm start`. Si no, verás `ModuleNotFoundError: No module named 'pymongo'`.

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

### Paso 5: Crear tu base de datos en MongoDB Atlas
1. Entra a [mongodb.com/atlas](https://www.mongodb.com/atlas) y crea un **cluster gratuito (M0)**.
2. En **Database Access**, crea un usuario con contraseña.
3. En **Network Access**, agrega tu IP (o `0.0.0.0/0` si el bot correrá en un servidor).
4. En **Connect → Drivers**, copia tu cadena de conexión (`mongodb+srv://usuario:contraseña@...`).
5. Pega **la misma cadena** en los dos archivos, en la constante `MONGO_URI`:
   * `index.js` (cerca de la línea 17)
   * `main.py` (cerca de la línea 17)

La base de datos `BotCielDB` y sus colecciones (`sistema_economia`, `chats_activos`, `usuarios_niveles`) se crean solas la primera vez.

### Paso 6: Configurar Gemini *(opcional, solo para `#ciel`)*
1. Genera una API Key gratuita en [Google AI Studio](https://aistudio.google.com/apikey).
2. En `index.js`, pégala en esta línea (cerca de la línea 12):
   ```js
   const ai = new GoogleGenAI({ apiKey: "TU_API_KEY" });
   ```
Si lo omites, el bot funciona igual, pero `#ciel` responderá con error.

### Paso 7: Configurar el propietario del bot
Los comandos `#on` y `#off` solo los puede ejecutar el **propietario**. En `index.js`, dentro del bloque `#on / #off`, cambia el arreglo `ADMINS_FIJOS` por **tu número** (con código de país, sin `+`):
```js
const ADMINS_FIJOS = ["57TUNUMERO", "TUNUMERO"];
```
Los mensajes enviados desde la propia cuenta vinculada (`fromMe`) también se aceptan.

### Paso 8: Vincular WhatsApp (se hace una sola vez)
```bash
node qr.js
```
1. Aparecerá un **código QR** en la terminal.
2. En el celular: **WhatsApp → Ajustes → Dispositivos vinculados → Vincular un dispositivo**.
3. Escanea el QR. Al terminar verás `✅ ¡VINCULACIÓN EXITOSA CON EL TELÉFONO!`.

Se crea la carpeta `sesion_whatsapp/` con tu sesión. **No la subas a GitHub ni la compartas** (da acceso total a la cuenta).

### Paso 9: Iniciar el bot
Con el entorno virtual activado:
```bash
npm start
```
Debes ver `🔮 [DATABASE] ¡Conexión permanente establecida con MongoDB Atlas!`.

Luego, **en cada chat o grupo donde quieras usarlo**, envía:
```text
#on
```
Prueba con `#help`, `#work` o `#gacha`. Para apagarlo en un chat: `#off`.

### Paso 10: Alternativa con Docker
El `Dockerfile` ya incluye Node 20, Python 3 y FFmpeg.
```bash
docker build -t ciel-bot .

# Vincular WhatsApp (una sola vez, guarda la sesión en tu máquina)
docker run -it --rm -v "$(pwd)/sesion_whatsapp:/app/sesion_whatsapp" ciel-bot node qr.js

# Correr el bot en segundo plano
docker run -d --name ciel-bot --restart unless-stopped \
  -v "$(pwd)/sesion_whatsapp:/app/sesion_whatsapp" ciel-bot
```
Ver los logs: `docker logs -f ciel-bot`.

---

## 🛠️ Solución de Problemas

| Problema | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: pymongo` | Entorno virtual sin activar | `source venv/bin/activate` y vuelve a ejecutar `npm start` |
| `python3: command not found` | Python no está en el PATH (Windows) | Usa WSL o Docker |
| `Error crítico de conexión` (MongoDB) | IP no permitida o URI incorrecta | Revisa **Network Access** en Atlas y que `MONGO_URI` sea igual en `index.js` y `main.py` |
| El bot no responde a nada | El chat no está activado | Envía `#on` desde el número propietario |
| `ACCESO DENEGADO` al usar `#on` | Tu número no está en `ADMINS_FIJOS` | Ver Paso 7 |
| `Sesión cerrada` en `qr.js` | Sesión inválida | Borra la carpeta `sesion_whatsapp/` y repite el Paso 8 |
| Fallan `#play`, `#mp4`, `#tiktok` | FFmpeg ausente o `yt-dlp` desactualizado | Instala FFmpeg y ejecuta `pip install -U yt-dlp` |
| `#ciel` responde "Mente Saturada" | Cuota gratuita de Gemini agotada (429) | Espera unos segundos o revisa tu API Key |

---

## 🔐 Recomendaciones de Seguridad
* **No subas credenciales al repositorio.** Mueve `MONGO_URI` y la API Key de Gemini a variables de entorno (`process.env` en Node y `os.environ` en Python) y, si alguna vez estuvieron publicadas, **cambia la contraseña** del usuario de MongoDB.
* Agrega un `.gitignore` con `sesion_whatsapp/`, `venv/` y `node_modules/`.

---
> *Desarrollado con rigor técnico y optimizado para alto rendimiento.*