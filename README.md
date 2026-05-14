# 🌊 DIABOLIC CANARIAS v1.0

[![Version](https://img.shields.io/badge/version-1.0-red)](https://github.com/Condor2026/Diabolic_Canarias)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green)](https://python.org)
[![OSINT](https://img.shields.io/badge/OSINT-Passive-blueviolet)](https://es.wikipedia.org/wiki/OSINT)
[![Termux](https://img.shields.io/badge/Termux-Compatible-orange)](https://termux.com)
[![Linux](https://img.shields.io/badge/Linux-Compatible-lightgrey)](https://linux.org)
[![Web Scraping](https://img.shields.io/badge/Web%20Scraping-Legal-brightgreen)](https://es.wikipedia.org/wiki/Web_scraping)

**DIABOLIC CANARIAS** es una herramienta OSINT pasiva y analítica diseñada para **monitorizar automáticamente más de 35 periódicos digitales de las Islas Canarias**, extrayendo y procesando noticias de sucesos para detectar patrones delictivos (narcotráfico marítimo, migración irregular, violencia, crimen organizado, etc.), tendencias geográficas por isla y conexiones entre incidentes.

Nace con una filosofía clara: *“Un gran poder conlleva una gran responsabilidad”*. Por eso su diseño prioriza la transparencia, la ética y el respeto a la privacidad.

---

## 📌 Índice

- [🔍 ¿Qué hace DIABOLIC?](#-qué-hace-diabolic)
- [⚙️ Características clave](#️-características-clave)
- [🛠️ Tecnología y arquitectura](#️-tecnología-y-arquitectura)
- [⚖️ Web Scraping: marco legal](#️-web-scraping-marco-legal)
- [📥 Instalación y uso](#-instalación-y-uso)
- [🖥️ Modo terminal (10 comandos)](#️-modo-terminal-10-comandos)
- [🌐 Modo web interactivo](#-modo-web-interactivo)
- [📰 Fuentes monitorizadas](#-fuentes-monitorizadas)
- [🌊 Léxico criminal canario](#-léxico-criminal-canario)
- [🧠 Tipo de OSINT y metodología](#-tipo-de-osint-y-metodología)
- [⚖️ Ética, legalidad y protección de datos](#️-ética-legalidad-y-protección-de-datos)
- [🤝 Contribuciones y futuro](#-contribuciones-y-futuro)
- [📜 Licencia](#-licencia)

---

## 🔍 ¿Qué hace DIABOLIC?

DIABOLIC CANARIAS automatiza el proceso de scraping de noticias de sucesos de medios canarios. En lugar de leer decenas de periódicos cada día, la herramienta:

- **Extrae** automáticamente titulares, fechas, fuentes y ubicación geográfica (isla) de noticias relacionadas con delitos.
- **Clasifica** los incidentes en categorías: narcolancha, migración, violencia, droga, robo, asesinato, corrupción, etc.
- **Almacena** los datos localmente en formato JSON, sin guardar ningún dato personal.
- **Analiza** tendencias temporales (7, 30, 90 días) y distribuciones por isla y tipo de delito.
- **Detecta conexiones** entre incidentes: misma isla, fechas cercanas, mismo modus operandi (rutas de alijo, puntos de arribada, etc.).
- **Visualiza** los resultados mediante una interfaz web interactiva con gráficos de barras y filtros dinámicos.
- **Exporta** los datos a CSV o JSON para análisis externos.

---

## ⚙️ Características clave

| Característica | Descripción |
|----------------|-------------|
| 🔁 Rotación de User‑Agent | Evita bloqueos simulando diferentes navegadores y versiones. |
| 🧠 Paginación inteligente | Prueba 12 formatos de paginación y recuerda el que funciona. |
| 🔎 Detector automático de URLs | Si falla, busca rutas alternativas (/sucesos, /policial, /tribunales...). |
| 📊 Clasificación avanzada | Léxico canario: narcolancha, patera, cayuco, alijo, rescate... |
| 🔗 Conexiones entre incidentes | Por tipo/isla, modus operandi, frecuencia temporal. |
| 🌐 Interfaz web interactiva | Gráficos, filtros, exportación. |
| 🖥️ Menú terminal completo | 10 comandos. |

---

## 🛠️ Tecnología y arquitectura

- **Lenguaje**: Python 3.8+
- **Framework web**: Flask
- **Scraping**: Requests + BeautifulSoup4
- **Almacenamiento**: JSON local
- **Estructura modular**:
  - `DetectorURLs`: verifica y corrige URLs.
  - `GestorDatos`: carga, guarda y procesa incidentes.
  - `ExtractorNoticias`: scraping con rotación de User‑Agent y paginación inteligente.
- **Colores en terminal**: Códigos ANSI.

---

## ⚖️ Web Scraping: marco legal

El web scraping que realiza DIABOLIC CANARIAS es **completamente legal y ético** por las siguientes razones:

1. **Fuentes públicas**: Solo accede a contenido indexado y accesible sin autenticación. No vulnera sistemas de pago ni áreas restringidas.
2. **Cumplimiento del RGPD / LOPDGDD**: No extrae, almacena ni procesa datos personales (nombres, direcciones, teléfonos, emails, IPs, cookies). Solo almacena metadatos anónimos: titular de la noticia, fecha, isla aproximada, tipo de delito y fuente.
3. **Respeto a los términos de uso**: La herramienta respeta el archivo `robots.txt` de cada sitio (se puede configurar) y no sobrecarga los servidores con peticiones (limita la frecuencia y número de páginas).
4. **Sin republicación de contenido**: No copia íntegramente los artículos, solo extrae titulares y metadatos para análisis, citando siempre la fuente original.
5. **Uso legítimo**: La finalidad es exclusivamente académica, periodística, criminológica o de prevención comunitaria, sin ánimo de lucro ni vigilancia masiva.
6. **Transparencia total**: El código es abierto y auditable, lo que permite verificar que no se realizan prácticas lesivas.

> **Nota**: El scraping masivo o con fines de venta/redistribución de contenido puede vulnerar derechos de autor. Este proyecto se acoge al **uso justo** (fair use) y al **derecho a la información**.

---

## 📥 Instalación y uso

### En Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests beautifulsoup4 flask
git clone https://github.com/Condor2026/Diabolic_Canarias
cd Diabolic_Canarias
python Diabolic_Canarias.py
```

En Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
pip3 install requests beautifulsoup4 flask
git clone https://github.com/Condor2026/Diabolic_Canarias
cd Diabolic_Canarias
python3 Diabolic_Canarias.py
```

---

🖥️ Modo terminal (10 comandos)

Al ejecutar Diabolic_Canarias.py aparece un menú con las siguientes opciones:

```
╔════════════════════════════════════════════════════╗
║              M E N Ú   P R I N C I P A L           ║
╚════════════════════════════════════════════════════╝
[1] 🔍 Buscar noticias (narco/migración)
[2] 📊 Ver análisis completo
[3] 🔗 Ver conexiones entre incidentes
[4] 📈 Ver evolución mensual
[5] 🌐 Iniciar servidor web
[6] 📰 Ver últimos 20 incidentes
[7] 📥 Exportar datos (JSON/CSV)
[8] 🔍 Verificar periódicos
[9] 📊 Ver distribución por tipo
[0] 🗑️ Salir
```

Cada opción ejecuta la acción correspondiente y muestra los resultados en la terminal.

---

🌐 Modo web interactivo

La opción [5] lanza un servidor Flask local (por defecto en http://localhost:5014). Desde el navegador podrás:

· Ver gráficos de barras interactivos por isla y tipo de delito.
· Filtrar por período (7, 30, 90 días).
· Consultar la lista de incidentes.
· Exportar los datos a CSV o JSON con un clic.

---

📰 Fuentes monitorizadas

La herramienta rastrea más de 35 periódicos digitales canarios, incluyendo:

· Gran Canaria: Canarias7 (Sucesos), La Provincia (Sucesos), eldiario.es Canarias (Tribunales), Diario de Gran Canaria, InfoGranCanaria.
· Tenerife: El Día (Sucesos), Diario de Avisos (Sucesos), La Opinión de Tenerife, Atlántico Hoy, Sol del Sur, InfoTenerife.
· Lanzarote: Diario de Lanzarote, La Voz de Lanzarote, Crónicas de Lanzarote, Lanzarote Digital.
· Fuerteventura: Puerto del Rosario Digital, Fuerteventura Ahora.
· La Palma: El Time (Sucesos), Diario Palmero, El Digital de La Palma.
· La Gomera: Gomera Actualidad, Gomera Noticias.
· El Hierro: El Hierro Digital.
· Medios nacionales con sección Canarias: El País, El Mundo, ABC, La Vanguardia, 20minutos, Europa Press.

La lista completa se puede consultar/editando dentro del script (PERIODICOS_BASE).

---

🌊 Léxico criminal canario

La herramienta incluye términos específicos de la región y del ámbito marítimo:

· Narcotráfico marítimo: narcolancha, semirrígida, goma, alijo, ruta atlántica, planeadora, persecución marítima.
· Migración irregular: patera, cayuco, rescate, naufragio, sin papeles, mena, devolución en caliente.
· Violencia y crimen organizado: ajuste de cuentas, sicariato, tiroteo, balacera, violencia machista.
· Robos y hurtos: alunizaje, butrón, escalo, lanzazo, motochorro.
· Corrupción y delitos económicos: corrupción, mafia, blanqueo, testaferro, extorsión.

---

🧠 Tipo de OSINT y metodología

· OSINT Pasivo: No interactúa con los sistemas de los periódicos más allá de lo que un usuario normal haría.
· Extracción selectiva: Solo recoge información de sucesos (policial, judicial, seguridad ciudadana, migración).
· Anonimización: No almacena datos personales de los implicados, solo el lugar, fecha y tipo de delito.
· Enfoque analítico: Busca patrones para entender la criminalidad en Canarias, especialmente rutas de narcotráfico y migración irregular.

---

⚖️ Ética, legalidad y protección de datos

DIABOLIC CANARIAS respeta estrictamente la legalidad española y europea:

· Solo accede a contenido público y no requiere autenticación.
· No almacena información personal (nombres, DNI, direcciones, IPs, cookies).
· El código es abierto y transparente.
· Se recomienda utilizar la herramienta únicamente con fines académicos, periodísticos o de investigación criminal legítima.

⚠️ ADVERTENCIA LEGAL
Esta herramienta es exclusivamente para fines educativos y de investigación legítima. No debe utilizarse para acosar, doxear, realizar actividades ilegales o violar la privacidad de las personas. El autor no se responsabiliza del mal uso. El usuario es el único responsable de cumplir con las leyes de su país.

---

🤝 Contribuciones y futuro

Las contribuciones son bienvenidas. Puedes:

· Reportar errores en Issues.
· Ampliar la lista de periódicos o islas.
· Mejorar el detector automático de URLs.
· Añadir nuevas categorías de delitos (especialmente relacionados con el ámbito marítimo).
· Optimizar el análisis de conexiones entre rutas de narcotráfico.

---

📜 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

🙏 Agradecimientos

· BeautifulSoup4 – scraping.
· Flask – interfaz web.
· Inspiración: proyectos OSINT como Sherlock, Maigret.
· Comunidad de investigación OSINT en Canarias.

⭐ ¡Si te gusta el proyecto, no olvides darle una estrella en GitHub!

``` 
