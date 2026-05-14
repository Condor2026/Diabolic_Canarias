# 🌊 DIABOLIC CANARIAS v1.0

**OSINT pasivo · Crimen organizado · Rutas atlánticas**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OSINT](https://img.shields.io/badge/OSINT-Passive-green)](https://osintframework.com/)
[![Canarias](https://img.shields.io/badge/Region-Canarias-blue)](https://es.wikipedia.org/wiki/Canarias)

**DIABOLIC CANARIAS** es una herramienta OSINT pasiva y analítica diseñada para monitorizar automáticamente **más de 20 periódicos digitales de las Islas Canarias**, extrayendo y procesando noticias de sucesos para detectar patrones delictivos, tendencias geográficas y conexiones entre incidentes, con **enfoque especial en narcotráfico marítimo, migración irregular y crimen organizado en el Atlántico**.

Nace con una filosofía clara: *“Un gran poder conlleva una gran responsabilidad”*. Por eso su diseño prioriza la transparencia, la ética y el respeto a la privacidad.

---

## 📌 Índice
- [🔍 ¿Qué hace DIABOLIC?](#-qué-hace-diabolic)
- [⚙️ Características clave](#️-características-clave)
- [🛠️ Tecnología y arquitectura](#️-tecnología-y-arquitectura)
- [📥 Instalación y uso](#-instalación-y-uso)
- [🖥️ Modo terminal (10 comandos)](#️-modo-terminal-10-comandos)
- [🌐 Modo web interactivo](#-modo-web-interactivo)
- [📰 Fuentes monitorizadas](#-fuentes-monitorizadas)
- [🏝️ Islas cubiertas](#️-islas-cubiertas)
- [🌊 Léxico criminal canario](#-léxico-criminal-canario)
- [🧠 Tipo de OSINT y metodología](#-tipo-de-osint-y-metodología)
- [⚖️ Ética, legalidad y protección de datos](#️-ética-legalidad-y-protección-de-datos)
- [🤝 Contribuciones y futuro](#-contribuciones-y-futuro)
- [📜 Licencia](#-licencia)

---

## 🔍 ¿Qué hace DIABOLIC?

DIABOLIC CANARIAS automatiza el proceso de scraping de noticias de sucesos de medios locales y nacionales que cubren el archipiélago canario. En lugar de leer decenas de periódicos cada día, la herramienta:

- Extrae automáticamente titulares, fechas, fuentes y ubicación geográfica (isla) de noticias relacionadas con delitos.
- Clasifica los incidentes en categorías específicas: **narcolancha, migración irregular, violencia, droga, robo, asesinato, corrupción** y otros.
- Almacena los datos localmente en formato JSON, sin guardar ningún dato personal.
- Analiza tendencias temporales (7, 30, 90 días) y distribuciones por isla y tipo de delito.
- Detecta conexiones entre incidentes: misma isla, fechas cercanas, mismo modus operandi (rutas marítimas, puntos de alijo, etc.) que pueden indicar una misma red criminal.
- Visualiza los resultados mediante una interfaz web interactiva con gráficos de barras y filtros dinámicos.
- Exporta los datos a CSV o JSON para análisis externos.

---

## ⚙️ Características clave

| Característica | Descripción |
|----------------|-------------|
| 🔁 Rotación de User‑Agent | Evita bloqueos de los periódicos simulando diferentes navegadores y versiones en cada petición. |
| 🧠 Paginación inteligente | Prueba automáticamente hasta 12 formatos diferentes de paginación y recuerda el que funciona para cada dominio. |
| 🔎 Detector automático de URLs | Si una URL de un periódico deja de funcionar, el sistema busca rutas alternativas (/sucesos, /policial, /tribunales, etc.) y actualiza la configuración. |
| 📊 Clasificación avanzada | Utiliza un léxico específico canario (narcolancha, patera, cayuco, alijo, rescate, sin papeles, devolución en caliente, ruta atlántica...). |
| 🔗 Conexiones entre incidentes | Por isla y tipo (ej. 5 narcolanchas interceptadas en Gran Canaria en 7 días). Por modus operandi (detección de rutas marítimas recurrentes). Frecuencia temporal (incidentes/día). |
| 🌐 Interfaz web interactiva | Gráficos de barras por isla y tipo de delito. Filtros por período (últimos 7, 30, 90 días). Lista de los últimos 20 incidentes. Botones para actualizar datos y exportar JSON/CSV. |
| 🖥️ Menú terminal completo | 10 comandos que permiten ejecutar todas las funciones sin necesidad de abrir el navegador. |
| 🌍 Multilingüe | Soporte español e inglés (selector al inicio). |

---

## 🛠️ Tecnología y arquitectura

- **Lenguaje:** Python 3.8+
- **Framework web:** Flask (servidor ligero)
- **Scraping:** Requests + BeautifulSoup4
- **Almacenamiento:** JSON local (sin bases de datos externas)
- **Estructura modular:**  
  - `DetectorURLs`: verifica y corrige URLs de periódicos.  
  - `GestorDatos`: carga, guarda y procesa los incidentes.  
  - `ExtractorNoticias`: scraping con rotación de User‑Agent y paginación inteligente.  
- **Colores en terminal:** Códigos ANSI para una experiencia visual atractiva.

---

## 📥 Instalación y uso

### Requisitos previos
- Python 3.8+
- `git`
- Conexión a Internet

### 🔧 Paso a paso

#### 📱 Opción 1: Termux (Android)
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests beautifulsoup4 flask
git clone https://github.com/Condor2026/Diabolic_Canarias
cd Diabolic_Canarias
python Diabolic_Canarias.py
