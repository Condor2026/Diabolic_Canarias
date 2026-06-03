![Version](https://img.shields.io/badge/version-5.3-red)
![License](https://img.shields.io/badge/license-GPLv3-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![OSINT](https://img.shields.io/badge/OSINT-Si-brightgreen)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Termux-lightgrey)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)
![Communities](https://img.shields.io/badge/communities-15%20CCAA-brightgreen)
**DIABOLIC Canarias** es una herramienta OSINT pasiva y analítica que monitoriza **periódicos digitales de las Islas Canarias** (Tenerife, Gran Canaria, Lanzarote, Fuerteventura, La Palma, La Gomera, El Hierro) para detectar, clasificar y visualizar patrones delictivos.  
No guarda datos personales, solo titulares, fechas y ubicaciones por isla. Filosofía: *"Un gran poder conlleva una gran responsabilidad"*.

---

## 📌 Índice

- [🔍 ¿Qué hace DIABOLIC?](#-qué-hace-diabolic)
- [⚙️ Características clave](#️-características-clave)
- [🛠️ Tecnología y arquitectura](#️-tecnología-y-arquitectura)
- [📥 Instalación y uso](#-instalación-y-uso)
- [🖥️ Modo terminal (10 comandos)](#️-modo-terminal-10-comandos)
- [🌐 Modo web interactivo](#-modo-web-interactivo)
- [🗺️ Fuentes monitorizadas](#️-fuentes-monitorizadas)
- [🏝️ Islas cubiertas](#️-islas-cubiertas)
- [🧠 Tipo de OSINT y metodología](#-tipo-de-osint-y-metodología)
- [⚖️ Ética, legalidad y protección de datos](#️-ética-legalidad-y-protección-de-datos)
- [🤝 Contribuciones y futuro](#-contribuciones-y-futuro)
- [📜 Licencia](#-licencia)

---

## 🔍 ¿Qué hace DIABOLIC?

DIABOLIC automatiza el proceso de **scraping de noticias de sucesos** de medios locales y regionales de Canarias. En lugar de leer decenas de periódicos cada día, la herramienta:

- **Extrae** automáticamente titulares, fechas, fuentes y ubicación geográfica (isla) de noticias relacionadas con delitos.
- **Clasifica** los incidentes en categorías (robo, estafa, narcotráfico, violencia, asesinato, intrusismo turístico, etc.).
- **Almacena** los datos localmente en formato JSON, sin guardar ningún dato personal.
- **Analiza** tendencias temporales (7, 30, 90 días) y distribuciones por isla y tipo de delito.
- **Detecta conexiones** entre incidentes: misma zona, fechas cercanas, mismo modus operandi que pueden indicar una misma banda.
- **Visualiza** los resultados mediante una interfaz web interactiva con gráficos de barras y filtros dinámicos.
- **Exporta** los datos a CSV o JSON para análisis externos.

---

## ⚙️ Características clave

### 🔁 Rotación de User‑Agent
Evita bloqueos de los periódicos simulando diferentes navegadores y versiones en cada petición.

### 🧠 Paginación inteligente
Prueba automáticamente hasta 12 formatos diferentes de paginación (`/pagina/2`, `?page=2`, `?offset=2`, etc.) y recuerda el que funciona para cada dominio.

### 🔎 Detector automático de URLs
Si una URL de un periódico deja de funcionar, el sistema busca rutas alternativas (`/sucesos`, `/local`, `/tribunales`, `/actualidad/sucesos`, etc.) y actualiza la configuración.

### 📊 Clasificación avanzada de delitos
Utiliza una lista amplia de palabras clave, incluyendo jerga local canaria (ej. *"guagua"* en su contexto, aunque no es delito; pero se pueden añadir términos como *"alunicero"*, *"butrón"*, *"peta"*, etc.). Es fácilmente extensible.

### 🔗 Conexiones entre incidentes
- **Por tipo e isla** (ej. 5 robos en Tenerife en 7 días).
- **Por modus operandi** (detecta repetición de términos como “alunicero” o “butrón”).
- **Frecuencia temporal** (incidentes/día).

### 🌐 Interfaz web interactiva
- Gráficos de barras por isla y tipo de delito.
- Filtros por período (últimos 7, 30, 90 días).
- Lista de los últimos 20 incidentes.
- Botones para actualizar datos y exportar JSON/CSV.

### 🖥️ Menú terminal completo
10 comandos que permiten ejecutar todas las funciones sin necesidad de abrir el navegador.

---

## 🛠️ Tecnología y arquitectura

- **Lenguaje**: Python 3.8+
- **Framework web**: Flask (servidor ligero)
- **Scraping**: Requests + BeautifulSoup4
- **Almacenamiento**: JSON local (sin bases de datos externas)
- **Estructura modular**:
  - `DetectorURLs`: encargado de verificar y corregir URLs de periódicos.
  - `GestorDatos`: carga, guarda y procesa los incidentes.
  - `ExtractorNoticias`: realiza el scraping con rotación de User‑Agent y paginación inteligente.
- **Colores en terminal**: Códigos ANSI para una experiencia visual atractiva.

---

## 📥 Instalación y uso

### Requisitos
- Python 3.8 o superior.
- pip (gestor de paquetes de Python).

### Instalación manual
```bash
git clone https://github.com/Condor2026/Diabolic_Canarias
cd Diabolic_Canarias
pip install -r requirements.txt
python Diabolic_Canarias.py
```

### Instalación automática (Termux / Linux)
```bash
chmod +x install.sh
./install.sh
```

### Ejecución
Al arrancar, se mostrará un banner informativo y se preguntará:
- **1** → Modo terminal (10 comandos).
- **2** → Modo web (servidor en `http://localhost:5015`).

---

## 🖥️ Modo terminal (10 comandos)

Una vez en el menú principal, puedes ejecutar las siguientes opciones:

| Comando | Función |
|---------|---------|
| `[1]` | 🔍 Buscar noticias (con detección automática de URLs) |
| `[2]` | 📊 Ver análisis completo (tendencias, distribuciones) |
| `[3]` | 🔗 Ver conexiones entre incidentes (patrones y bandas) |
| `[4]` | 📈 Ver evolución mensual |
| `[5]` | 🌐 Iniciar servidor web |
| `[6]` | 📰 Ver últimos 20 incidentes |
| `[7]` | 📥 Exportar datos (JSON/CSV) |
| `[8]` | 🔍 Verificar periódicos (detector automático de URLs) |
| `[9]` | 📊 Ver distribución por tipo (con gráfico ASCII) |
| `[10]` | 🗑️ Salir |

Cada opción interactúa con los datos locales y permite explorar los patrones sin necesidad de abrir el navegador.

---

## 🌐 Modo web interactivo

Al elegir la opción `[2]` en el arranque, se levanta un servidor Flask local. Desde el navegador puedes:

- Ver estadísticas globales (total, últimos 7/30/90 días).
- Filtrar por período.
- Visualizar gráficos de barras con la distribución de incidentes por isla y por tipo.
- Consultar la lista de los últimos 20 incidentes.
- Actualizar la base de datos directamente desde la web (botón **ACTUALIZAR**).
- Exportar a JSON o CSV.

La interfaz está optimizada para dispositivos móviles y escritorio.

---

## 🗺️ Fuentes monitorizadas

La herramienta incluye periódicos digitales de todas las islas, entre ellos:

- **Tenerife**: Diario de Avisos, El Día, El Español – Canarias, Canarias7, La Opinión de Tenerife, El Periódico de Tenerife, etc.
- **Gran Canaria**: Canarias7 (edición Gran Canaria), La Provincia, InfoNorte Digital, El Periódico de Gran Canaria.
- **Lanzarote**: Diario de Lanzarote, Lancelot Digital, La Voz de Lanzarote.
- **Fuerteventura**: Diario de Fuerteventura, Fuerteventura Digital, Noticias Fuerteventura.
- **La Palma**: El Time, La Palma Ahora, El Apurón.
- **La Gomera**: La Voz de La Gomera, Gomera Noticias.
- **El Hierro**: El Hierro Digital, El Periódico de El Hierro.

El detector automático de URLs se encarga de corregir cambios en las direcciones. La lista completa se puede consultar y ampliar en el archivo `PERIODICOS_BASE` del código.

---

## 🏝️ Islas cubiertas

- Tenerife
- Gran Canaria
- Lanzarote
- Fuerteventura
- La Palma
- La Gomera
- El Hierro

---

## 🧠 Tipo de OSINT y metodología

DIABOLIC se clasifica como **OSINT pasivo y analítico**:

- **Pasivo**: porque no interactúa con los sistemas de los periódicos más allá de las peticiones HTTP que haría un usuario normal. No realiza inyecciones, no vulnera accesos, no utiliza credenciales.
- **Analítico**: porque no se limita a recopilar información; procesa los datos para extraer **patrones geográficos (islas), temporales (evolución diaria, mensual) y relacionales (conexiones entre incidentes)**.

### Flujo de trabajo
1. **Adquisición**: se descargan las páginas de sucesos de cada periódico respetando tiempos de espera y user-agents.
2. **Parseo**: se extraen títulos, fechas y se detecta la ubicación (isla) mediante comparación de palabras clave.
3. **Clasificación**: se etiqueta cada incidente con un tipo de delito basado en palabras clave.
4. **Almacenamiento**: se guardan los metadatos en un archivo JSON local, sin datos personales.
5. **Análisis**: se generan estadísticas, patrones temporales y conexiones.
6. **Visualización**: se muestran los resultados en terminal o web.

### Detección de conexiones (opción 3)
- Agrupa incidentes por **tipo + isla** en los últimos 30 días.
- Si hay **3 o más** incidentes del mismo tipo en la misma isla, los muestra como un patrón y calcula la frecuencia (incidentes/día).
- Busca palabras clave de modus operandi (`alunicero`, `butrón`, `escalo`, etc.) y agrupa incidentes que compartan la misma técnica, sugiriendo posibles bandas.

---

## ⚖️ Ética, legalidad y protección de datos

### Cumplimiento normativo
- **RGPD / LOPDGDD**: DIABOLIC no trata datos personales. Solo almacena metadatos (titular, fecha, isla, tipo, fuente). Por tanto, queda fuera del ámbito de aplicación de estas leyes.
- **Propiedad intelectual**: No republica el contenido íntegro de las noticias; solo extrae titulares y metadatos. Las peticiones son las mismas que haría un lector humano, respetando `robots.txt` y rate limiting.

### Principios éticos
- **Transparencia**: código abierto, cualquier persona puede auditar qué hace y qué guarda.
- **No vigilancia**: no perfila personas ni almacena información que pueda identificar a individuos.
- **Responsabilidad**: el usuario es el único responsable del uso que dé a la herramienta. El banner de inicio incluye la advertencia y la filosofía Spiderman.

### Exención de responsabilidad
La herramienta se proporciona “tal cual”, sin garantías de funcionamiento ininterrumpido. Cualquier modificación que introduzca funcionalidades lesivas (recogida de datos personales, vigilancia encubierta) es responsabilidad exclusiva de quien la realice.

---

## 🤝 Contribuciones y futuro

Las contribuciones son bienvenidas siempre que respeten la filosofía ética del proyecto. Puedes:

- Reportar errores o fuentes caídas.
- Sugerir mejoras en la detección de patrones.
- Añadir nuevas fuentes de noticias públicas (respetando siempre los términos de uso).
- Traducir la documentación.

Para el futuro se contemplan:
- Integración con mapas (Leaflet) para visualización geográfica.
- Alertas en tiempo real cuando se detecte un patrón anómalo.
- Soporte para RSS de ayuntamientos y boletines oficiales de las islas.

---

## 📜 Licencia

Este proyecto está bajo la **GNU General Public License v3.0 (GPLv3)**.  
Esto significa que:

- Puedes usar, estudiar, compartir y modificar el software libremente.
- Si distribuyes versiones modificadas, **debes hacerlo bajo la misma licencia**.
- **No puedes convertir el software en propietario**; cualquier obra derivada debe permanecer de código abierto.
- El software se proporciona “tal cual”, sin garantías (consulta el archivo [`LICENSE`](LICENSE) para más detalles).

Consulta el archivo `LICENSE` para el texto completo de la licencia.

---

⭐ **Si DIABOLIC te resulta útil, considera dejar una estrella en el repositorio y compartir el proyecto. ¡Juntos hacemos el OSINT más ético y accesible!**
```
