#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌊 DIABOLIC CANARIAS v1.0 - OSINT ANALYTICS PLATFORM
Monitorización de narcotráfico marítimo, migración irregular y crimen organizado
en las Islas Canarias (España)
"""

import os
import sys
import time
import json
import hashlib
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request
from collections import defaultdict

# ============================================
# IDIOMA (selector al inicio)
# ============================================
IDIOMA_ACTUAL = None

TEXTOS = {
    'es': {
        'app_name': '🌊 DIABOLIC CANARIAS',
        'elegir_idioma': 'Elige idioma: 1. Español  2. English',
        'menu_title': 'MENÚ PRINCIPAL',
        'cmd_buscar': '🔍 Buscar noticias (narco/migración)',
        'cmd_analisis': '📊 Análisis completo',
        'cmd_conexiones': '🔗 Conexiones entre incidentes',
        'cmd_evolucion': '📈 Evolución mensual',
        'cmd_web': '🌐 Iniciar servidor web',
        'cmd_ultimos': '📰 Últimos 20 incidentes',
        'cmd_exportar': '📥 Exportar datos (JSON/CSV)',
        'cmd_verificar': '🔍 Verificar periódicos',
        'cmd_tipos': '📊 Distribución por tipo',
        'cmd_salir': '🗑️ Salir',
        'stats_total': 'Total incidentes',
        'incidentes': 'incidentes',
        'fuentes': 'fuentes',
        'islas': 'islas',
        'servidor_web': 'Servidor web',
        'presiona_ctrl_c': 'Presiona Ctrl+C para volver',
        'hasta_pronto': 'Hasta pronto',
        'opcion_invalida': 'Opción no válida'
    },
    'en': {
        'app_name': '🌊 DIABOLIC CANARIAS',
        'elegir_idioma': 'Choose language: 1. Spanish  2. English',
        'menu_title': 'MAIN MENU',
        'cmd_buscar': '🔍 Search news (narco/migration)',
        'cmd_analisis': '📊 Full analysis',
        'cmd_conexiones': '🔗 Incident connections',
        'cmd_evolucion': '📈 Monthly evolution',
        'cmd_web': '🌐 Start web server',
        'cmd_ultimos': '📰 Last 20 incidents',
        'cmd_exportar': '📥 Export data (JSON/CSV)',
        'cmd_verificar': '🔍 Verify newspapers',
        'cmd_tipos': '📊 Distribution by type',
        'cmd_salir': '🗑️ Exit',
        'stats_total': 'Total incidents',
        'incidentes': 'incidents',
        'fuentes': 'sources',
        'islas': 'islands',
        'servidor_web': 'Web server',
        'presiona_ctrl_c': 'Press Ctrl+C to return',
        'hasta_pronto': 'Goodbye',
        'opcion_invalida': 'Invalid option'
    }
}

def seleccionar_idioma():
    global IDIOMA_ACTUAL
    print("\n" + "="*60)
    print(TEXTOS['es']['elegir_idioma'])
    opc = input("➤ ")
    IDIOMA_ACTUAL = 'en' if opc == '2' else 'es'
    print(f"\n✅ Idioma: {'English' if IDIOMA_ACTUAL == 'en' else 'Español'}\n")

def t(clave):
    return TEXTOS[IDIOMA_ACTUAL].get(clave, clave)

# ============================================
# COLORES (para terminal)
# ============================================
class Color:
    ROJO = '\033[91m'
    ROJO_OSCURO = '\033[31m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIAN = '\033[96m'
    GRIS = '\033[90m'
    BLANCO = '\033[97m'
    NEGRITA = '\033[1m'
    SUBRAYADO = '\033[4m'
    RESET = '\033[0m'
    FONDO_ROJO = '\033[41m'
    FONDO_VERDE = '\033[42m'
    FONDO_AMARILLO = '\033[43m'
    FONDO_AZUL = '\033[44m'

def cprint(texto, color=None, negrita=False, subrayado=False, fondo=False, fin='\n'):
    colores = {
        'rojo': Color.ROJO, 'rojo_oscuro': Color.ROJO_OSCURO,
        'verde': Color.VERDE, 'amarillo': Color.AMARILLO,
        'azul': Color.AZUL, 'magenta': Color.MAGENTA,
        'cian': Color.CIAN, 'gris': Color.GRIS, 'blanco': Color.BLANCO
    }
    col = colores.get(color, '')
    neg = Color.NEGRITA if negrita else ''
    sub = Color.SUBRAYADO if subrayado else ''
    fondo_color = ''
    if fondo:
        if color == 'rojo':
            fondo_color = Color.FONDO_ROJO
        elif color == 'verde':
            fondo_color = Color.FONDO_VERDE
        elif color == 'amarillo':
            fondo_color = Color.FONDO_AMARILLO
        elif color == 'azul':
            fondo_color = Color.FONDO_AZUL
    print(f"{fondo_color}{neg}{sub}{col}{texto}{Color.RESET}", end=fin)

# ============================================
# CONFIGURACIÓN - Periódicos de Canarias (35+ fuentes)
# ============================================
VERSION = "1.0"
PUERTO = 5014
ARCHIVO = 'diabolic_canarias.json'
ARCHIVO_ESTADO = 'estado_periodicos_canarias.json'
PAGINAS_BUSQUEDA = 10
TIEMPO_ESPERA = 1.2
TIMEOUT = 18

# User-Agents modernos (20+)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Android 14; Mobile; rv:123.0) Gecko/123.0 Firefox/123.0',
    'Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

PERIODICOS_BASE = [
    # === PRINCIPALES Y RECOMENDADOS (alta cobertura) ===
    {'nombre': 'Canarias7 Sucesos', 'url': 'https://www.canarias7.es/sucesos/', 'base': 'https://www.canarias7.es', 'isla': 'Gran Canaria', 'activo': True},
    {'nombre': 'La Provincia Sucesos', 'url': 'https://www.laprovincia.es/sucesos/sucesos-en-canarias/', 'base': 'https://www.laprovincia.es', 'isla': 'Gran Canaria', 'activo': True},
    {'nombre': 'El Día Sucesos', 'url': 'https://www.eldia.es/sucesos/sucesos-en-canarias/', 'base': 'https://www.eldia.es', 'isla': 'Tenerife', 'activo': True},
    {'nombre': 'Diario de Avisos Sucesos', 'url': 'https://diariodeavisos.elespanol.com/sucesos/', 'base': 'https://diariodeavisos.elespanol.com', 'isla': 'Tenerife', 'activo': True},
    {'nombre': 'Canarias Ahora Sucesos', 'url': 'https://www.eldiario.es/canariasahora/sucesos/', 'base': 'https://www.eldiario.es', 'isla': 'Canarias', 'activo': True},

    # === Fuentes fuertes adicionales ===
    {'nombre': 'Canarias Diario', 'url': 'https://www.canariasdiario.com/', 'base': 'https://www.canariasdiario.com', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'El Periódico de Canarias', 'url': 'https://elperiodicodecanarias.es/', 'base': 'https://elperiodicodecanarias.es', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'Canarias24Horas', 'url': 'http://www.canarias24horas.com/', 'base': 'http://www.canarias24horas.com', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'Atlántico Hoy', 'url': 'https://www.atlanticohoy.com/', 'base': 'https://www.atlanticohoy.com', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'Canarias Times', 'url': 'https://canariastimes.com/sucesos/', 'base': 'https://canariastimes.com', 'isla': 'Canarias', 'activo': True},

    # === Portales insulares y locales ===
    {'nombre': 'Crónicas de Lanzarote', 'url': 'https://www.cronicasdelanzarote.es/informacion/sucesos-70/', 'base': 'https://www.cronicasdelanzarote.es', 'isla': 'Lanzarote', 'activo': True},
    {'nombre': 'Diario Palmero', 'url': 'https://www.diariopalmero.es/sucesos.php', 'base': 'https://www.diariopalmero.es', 'isla': 'La Palma', 'activo': True},
    {'nombre': 'Gomera Noticias', 'url': 'https://www.gomeranoticias.com/', 'base': 'https://www.gomeranoticias.com', 'isla': 'La Gomera', 'activo': True},
    {'nombre': 'El Time La Palma', 'url': 'https://www.eltime.es/la-calle/144-sucesos.html', 'base': 'https://www.eltime.es', 'isla': 'La Palma', 'activo': True},
    {'nombre': 'Diario de Gran Canaria', 'url': 'https://diariodegrancanaria.opennemas.com/', 'base': 'https://diariodegrancanaria.opennemas.com', 'isla': 'Gran Canaria', 'activo': True},
    {'nombre': 'Sol del Sur Tenerife', 'url': 'https://www.soldelsurtenerife.com/', 'base': 'https://www.soldelsurtenerife.com', 'isla': 'Tenerife', 'activo': True},
    {'nombre': 'Fuerteventura Ahora', 'url': 'https://fuerteventuraahora.com/', 'base': 'https://fuerteventuraahora.com', 'isla': 'Fuerteventura', 'activo': True},
    {'nombre': 'Lanzarote Digital', 'url': 'https://www.lanzarotedigital.com/', 'base': 'https://www.lanzarotedigital.com', 'isla': 'Lanzarote', 'activo': True},
    {'nombre': 'El Digital de La Palma', 'url': 'https://www.eldigitaldelapalma.es/', 'base': 'https://www.eldigitaldelapalma.es', 'isla': 'La Palma', 'activo': True},
    {'nombre': 'Diario de Lanzarote', 'url': 'https://www.diariodelanzarote.com/sucesos/', 'base': 'https://www.diariodelanzarote.com', 'isla': 'Lanzarote', 'activo': True},
    {'nombre': 'La Voz de Lanzarote', 'url': 'https://www.lavozdelanzarote.com/sucesos/', 'base': 'https://www.lavozdelanzarote.com', 'isla': 'Lanzarote', 'activo': True},
    {'nombre': 'Gomera Actualidad', 'url': 'https://www.gomeraactualidad.com/sucesos/', 'base': 'https://www.gomeraactualidad.com', 'isla': 'La Gomera', 'activo': True},
    {'nombre': 'El Hierro Digital', 'url': 'https://www.elhierrodigital.es/sucesos/', 'base': 'https://www.elhierrodigital.es', 'isla': 'El Hierro', 'activo': True},

    # === Medios nacionales con sección Canarias ===
    {'nombre': '20minutos Canarias', 'url': 'https://www.20minutos.es/canarias/', 'base': 'https://www.20minutos.es', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'Europa Press Canarias', 'url': 'https://www.europapress.es/islas-canarias/', 'base': 'https://www.europapress.es', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'ABC Canarias', 'url': 'https://www.abc.es/espana/canarias/', 'base': 'https://www.abc.es', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'El País - Canarias', 'url': 'https://elpais.com/espana/canarias/', 'base': 'https://elpais.com', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'El Mundo - Canarias', 'url': 'https://www.elmundo.es/canarias.html', 'base': 'https://www.elmundo.es', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'La Vanguardia - Canarias', 'url': 'https://www.lavanguardia.com/local/canarias', 'base': 'https://www.lavanguardia.com', 'isla': 'Canarias', 'activo': True},
    {'nombre': 'La Opinión Tenerife', 'url': 'https://www.laopinion.es/sucesos/', 'base': 'https://www.laopinion.es', 'isla': 'Tenerife', 'activo': True},
]

ISLAS_CANARIAS = ['Gran Canaria', 'Tenerife', 'Lanzarote', 'Fuerteventura', 'La Palma', 'La Gomera', 'El Hierro', 'Canarias']

# ============================================
# LÉXICO CRIMINAL CANARIO (narco marítimo, migración, violencia)
# ============================================
DELITOS_CANARIAS = [
    # Narcotráfico marítimo
    'narcolancha', 'narcolanchas', 'goma', 'patera', 'cayuco', 'semirrígida',
    'droga', 'cocaína', 'hachís', 'marihuana', 'narcotráfico', 'alijos',
    'embarcación interceptada', 'velocidad', 'persecución marítima', 'narco',
    'capo', 'clan', 'organización criminal', 'ruta atlántica', 'planeadora',
    # Migración irregular
    'inmigrante', 'inmigrantes', 'mena', 'menas', 'menor extranjero',
    'rescate', 'naufragio', 'ahogado', 'cayuco interceptado', 'patera a la deriva',
    'sin papeles', 'salto de valla', 'centro de acogida', 'devolución en caliente',
    # Violencia y crimen organizado
    'ajuste de cuentas', 'sicariato', 'tiroteo', 'balacera', 'violencia machista',
    'asesinato', 'homicidio', 'apuñalamiento', 'pelea multitudinaria',
    'robo con violencia', 'atropello', 'vuelco', 'alunizaje', 'butrón',
    # Corrupción y delitos económicos
    'corrupción', 'mafia', 'blanqueo', 'testaferro', 'extorsión', 'amenazas',
    # Fuerzas de seguridad y sucesos
    'detenido', 'detenidos', 'arrestado', 'ingreso en prisión', 'juez',
    'Guardia Civil', 'Policía Nacional', 'vigilancia aduanera', 'SIVE'
]
DELITOS = DELITOS_CANARIAS

# ============================================
# TIPOS DE DELITO (enfoque canario)
# ============================================
TIPOS_DELITO = {
    'narcolancha': {'icono': '🚤', 'color': '#4b0082'},
    'migracion': {'icono': '🌊', 'color': '#cc6600'},
    'violencia': {'icono': '👊', 'color': '#ff0000'},
    'droga': {'icono': '💊', 'color': '#8b0000'},
    'robo': {'icono': '💰', 'color': '#8b6b00'},
    'asesinato': {'icono': '💀', 'color': '#000000'},
    'corrupcion': {'icono': '💼', 'color': '#990000'},
    'otro': {'icono': '❓', 'color': '#666666'}
}

ISLAS = ISLAS_CANARIAS

# ============================================
# DETECTOR AUTOMÁTICO DE URLs (MODO CANARIAS)
# ============================================
class DetectorURLs:
    def __init__(self):
        self.archivo_estado = ARCHIVO_ESTADO
        self.estado = self.cargar_estado()
        self.posibles_paths = [
            'sucesos', 'sucesos/', 'policial', 'policial/', 'tribunales',
            'judicial', 'judicial/', 'crimen', 'seguridad', 'narcotrafico',
            'inmigracion', 'violencia', 'operacion-policial'
        ]

    def cargar_estado(self):
        if os.path.exists(self.archivo_estado):
            try:
                with open(self.archivo_estado, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def guardar_estado(self):
        with open(self.archivo_estado, 'w', encoding='utf-8') as f:
            json.dump(self.estado, f, indent=2)

    def encontrar_url_correcta(self, periodico):
        dominio = periodico['base']
        nombre = periodico['nombre']
        if nombre in self.estado and self.estado[nombre].get('url'):
            url_guardada = self.estado[nombre]['url']
            try:
                r = requests.get(url_guardada, timeout=TIMEOUT, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    return url_guardada
            except:
                pass
        for path in self.posibles_paths:
            url = f"{dominio}/{path}"
            try:
                r = requests.get(url, timeout=TIMEOUT, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    texto = soup.get_text().lower()
                    if any(d in texto for d in DELITOS) or 'sucesos' in texto or 'narco' in texto:
                        self.estado[nombre] = {'url': url, 'path': path}
                        self.guardar_estado()
                        return url
            except:
                continue
        return None

    def verificar_todos(self, periodicos):
        cprint(f"\n{'='*70}", 'rojo', negrita=True)
        cprint(f"🔍 VERIFICANDO {len(periodicos)} PERIÓDICOS CANARIOS", 'rojo', negrita=True, fondo=True)
        cprint(f"{'='*70}", 'rojo', negrita=True)
        verificados = []
        activos = 0
        for p in periodicos:
            cprint(f"\n📰 {p['nombre']} ", 'amarillo', negrita=True, fin='')
            try:
                r = requests.get(p['url'], timeout=TIMEOUT, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    p['activo'] = True
                    cprint(f"✅ OK", 'verde')
                    activos += 1
                else:
                    nueva_url = self.encontrar_url_correcta(p)
                    if nueva_url:
                        p['url'] = nueva_url
                        p['activo'] = True
                        cprint(f"✅ NUEVA URL", 'verde')
                        activos += 1
                    else:
                        p['activo'] = False
                        cprint(f"❌ No encontrada", 'rojo')
            except Exception as e:
                nueva_url = self.encontrar_url_correcta(p)
                if nueva_url:
                    p['url'] = nueva_url
                    p['activo'] = True
                    cprint(f"✅ NUEVA URL", 'verde')
                    activos += 1
                else:
                    p['activo'] = False
                    cprint(f"❌ Error conexión", 'rojo')
            verificados.append(p)
            time.sleep(0.8)
        cprint(f"\n{'='*70}", 'verde', negrita=True)
        cprint(f"📊 ACTIVOS: {activos} de {len(periodicos)}", 'verde', negrita=True)
        cprint(f"{'='*70}", 'verde', negrita=True)
        return verificados

# ============================================
# GESTOR DE DATOS (ENFOQUE CANARIAS)
# ============================================
class GestorDatos:
    def __init__(self):
        self.archivo = ARCHIVO
        self.datos = self.cargar()
        self.detector = DetectorURLs()

    def cargar(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {'incidentes': [], 'ultima_actualizacion': None}
        return {'incidentes': [], 'ultima_actualizacion': None}

    def guardar(self):
        self.datos['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, indent=2, ensure_ascii=False)

    def agregar_incidentes(self, nuevos):
        ids_existentes = {inc['id'] for inc in self.datos['incidentes']}
        contador = 0
        for n in nuevos:
            if n['id'] not in ids_existentes:
                self.datos['incidentes'].append(n)
                contador += 1
        if contador:
            self.guardar()
        return contador

    def detectar_tipo(self, texto):
        texto_lower = texto.lower()
        # Prioridad: narcolanchas y tráfico marítimo
        if any(p in texto_lower for p in ['narcolancha', 'narcolanchas', 'goma', 'semirrígida',
                                          'embarcación interceptada', 'persecución marítima',
                                          'alijo', 'velocidad', 'ruta atlántica', 'planeadora']):
            return 'narcolancha'
        # Migración irregular
        if any(p in texto_lower for p in ['patera', 'cayuco', 'inmigrante', 'mena', 'rescate',
                                          'naufragio', 'ahogado', 'sin papeles', 'salto de valla',
                                          'centro de acogida', 'devolución en caliente']):
            return 'migracion'
        # Drogas (sin especificar embarcación)
        if any(p in texto_lower for p in ['cocaína', 'hachís', 'marihuana', 'droga', 'alijo']):
            return 'droga'
        # Violencia
        if any(p in texto_lower for p in ['violencia', 'agresión', 'tiroteo', 'balacera',
                                          'apuñalamiento', 'pelea', 'ajuste de cuentas']):
            return 'violencia'
        # Asesinatos
        if any(p in texto_lower for p in ['asesinato', 'homicidio', 'muerto', 'cadáver']):
            return 'asesinato'
        # Robos
        if any(p in texto_lower for p in ['robo', 'atraco', 'alunizaje', 'butrón', 'vuelco']):
            return 'robo'
        # Corrupción y crimen organizado
        if any(p in texto_lower for p in ['corrupción', 'mafia', 'blanqueo', 'testaferro', 'extorsión']):
            return 'corrupcion'
        return 'otro'

    def estadisticas(self, incidentes=None):
        if incidentes is None:
            incidentes = self.datos['incidentes']
        stats = {
            'total': len(incidentes),
            'islas': defaultdict(int),
            'tipos': defaultdict(int),
            'fuentes': defaultdict(int),
            'municipios': defaultdict(int),
            'ultimos_7dias': 0,
            'ultimos_30dias': 0,
            'ultimos_90dias': 0,
            'tendencia': {}
        }
        hoy = datetime.now()
        hace_7d = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')
        hace_30d = (hoy - timedelta(days=30)).strftime('%Y-%m-%d')
        hace_90d = (hoy - timedelta(days=90)).strftime('%Y-%m-%d')
        for inc in incidentes:
            if inc.get('isla'):
                stats['islas'][inc['isla']] += 1
            if inc.get('tipo'):
                stats['tipos'][inc['tipo']] += 1
            if inc.get('fuente'):
                stats['fuentes'][inc['fuente']] += 1
            fecha = inc.get('fecha', '')
            if fecha >= hace_7d:
                stats['ultimos_7dias'] += 1
            if fecha >= hace_30d:
                stats['ultimos_30dias'] += 1
            if fecha >= hace_90d:
                stats['ultimos_90dias'] += 1
            if fecha and len(fecha) >= 7:
                mes = fecha[:7]
                stats['tendencia'][mes] = stats['tendencia'].get(mes, 0) + 1
        return stats

    def evolucion_mensual(self):
        meses = {}
        for inc in self.datos['incidentes']:
            if inc.get('fecha') and len(inc['fecha']) >= 7:
                mes = inc['fecha'][:7]
                meses[mes] = meses.get(mes, 0) + 1
        return dict(sorted(meses.items()))


# ============================================
# EXTRACTOR DE NOTICIAS (CON BARRA DE PROGRESO)
# ============================================
class ExtractorNoticias:
    def __init__(self, periodicos):
        self.periodicos = periodicos
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        self.session.headers.update({'User-Agent': random.choice(self.user_agents)})
        self.cache_paginacion = {}
        self.timeout = TIMEOUT

    def _generar_url_pagina(self, url_base, pagina):
        dominio = url_base.split('/')[2] if '//' in url_base else url_base
        if dominio in self.cache_paginacion:
            formato = self.cache_paginacion[dominio]
            return formato.format(pagina=pagina)
        formatos = [
            f"{url_base}pagina/{{pagina}}/", f"{url_base}?page={{pagina}}", f"{url_base}{{pagina}}/",
            f"{url_base}page/{{pagina}}/", f"{url_base}index.php?page={{pagina}}", f"{url_base}listado?pag={{pagina}}",
            f"{url_base}?pag={{pagina}}", f"{url_base}?p={{pagina}}"
        ]
        for formato in formatos:
            url = formato.format(pagina=pagina)
            try:
                r = self.session.get(url, timeout=self.timeout)
                if r.status_code == 200:
                    self.cache_paginacion[dominio] = formato
                    return url
            except:
                continue
        return None

    def buscar_todo(self, paginas=10):
        cprint(f"\n{'='*80}", 'rojo', negrita=True)
        cprint(f"🌊 BÚSQUEDA EN CANARIAS - {len(self.periodicos)} FUENTES", 'rojo', negrita=True, fondo=True)
        cprint(f"{'='*80}", 'rojo', negrita=True)

        todas = []
        periodicos_activos = [p for p in self.periodicos if p.get('activo', True)]
        total_activos = len(periodicos_activos)
        if total_activos == 0:
            cprint(f"\n⚠️ No hay fuentes activas. Ejecuta verificación primero.", 'amarillo')
            return todas

        cprint(f"\n📊 Fuentes activas en Canarias: {total_activos}\n", 'cian')

        # Barra de progreso
        for idx, periodico in enumerate(periodicos_activos, 1):
            porcentaje = (idx / total_activos) * 100
            barra = '█' * int(porcentaje // 2) + '░' * (50 - int(porcentaje // 2))
            sys.stdout.write(f"\r   🌊 Progreso: [{barra}] {idx}/{total_activos} ({porcentaje:.1f}%)")
            sys.stdout.flush()

            cprint(f"\n📰 {periodico['nombre']}", 'amarillo', negrita=True)
            cprint(f"   Isla: {periodico['isla']}", 'gris')

            encontrados = 0
            for pagina in range(1, paginas + 1):
                url = self._generar_url_pagina(periodico['url'], pagina)
                if not url:
                    if pagina == 1:
                        cprint(f"   📄 Página {pagina}... ✗ No accesible", 'rojo')
                    else:
                        cprint(f"   📄 Página {pagina}... ✗ No hay más", 'amarillo')
                    break
                try:
                    cprint(f"   📄 Página {pagina}... ", 'gris', fin='')
                    r = self.session.get(url, timeout=self.timeout)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        articulos = []
                        articulos.extend(soup.find_all('article'))
                        articulos.extend(soup.find_all('div', class_=lambda x: x and ('article' in x or 'noticia' in x)))
                        articulos.extend(soup.find_all('h2'))
                        encontrados_pagina = 0
                        for art in articulos[:20]:
                            titulo_elem = art.find(['h2', 'h3']) if art.name != 'h2' else art
                            if not titulo_elem:
                                continue
                            titulo = titulo_elem.get_text().strip()
                            if len(titulo) < 20:
                                continue
                            titulo_lower = titulo.lower()
                            if any(d in titulo_lower for d in DELITOS):
                                isla = periodico['isla']
                                for i in ISLAS_CANARIAS:
                                    if i.lower() in titulo_lower:
                                        isla = i
                                        break
                                fecha_elem = art.find('time')
                                fecha = datetime.now().strftime('%Y-%m-%d')
                                if fecha_elem and fecha_elem.get('datetime'):
                                    fecha = fecha_elem.get('datetime')[:10]
                                gestor_temp = GestorDatos()
                                tipo = gestor_temp.detectar_tipo(titulo)
                                todas.append({
                                    'id': hashlib.md5(titulo.encode()).hexdigest()[:16],
                                    'titulo': titulo[:300],
                                    'fecha': fecha,
                                    'isla': isla,
                                    'tipo': tipo,
                                    'fuente': periodico['nombre']
                                })
                                encontrados_pagina += 1
                                encontrados += 1
                        cprint(f"✓ {encontrados_pagina}", 'verde')
                        if encontrados_pagina == 0 and pagina > 1:
                            break
                    elif r.status_code == 404:
                        cprint(f"✗ No existe (404)", 'amarillo')
                        break
                    else:
                        cprint(f"✗ Error {r.status_code}", 'rojo')
                except Exception as e:
                    cprint(f"✗ Error", 'rojo')
                time.sleep(TIEMPO_ESPERA)
            time.sleep(0.5)

        print()  # salto de línea después de la barra

        # Eliminar duplicados
        unicos = {}
        for n in todas:
            key = n['id']
            if key not in unicos:
                unicos[key] = n

        cprint(f"\n{'='*80}", 'verde', negrita=True)
        cprint(f"🌊 TOTAL CANARIAS: {len(unicos)} incidentes únicos de {total_activos} fuentes activas", 'verde', negrita=True)
        cprint(f"{'='*80}", 'verde', negrita=True)

        return list(unicos.values())

# ============================================
# HTML TEMPLATE (OCEANIC EDITION - CANARIAS)
# ============================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🌊 DIABOLIC CANARIAS v{{ version }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a1a2a; color: #fff; font-family: 'Segoe UI', Arial; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        @keyframes wavePulse {
            0% { text-shadow: 0 0 5px #00aaff, 0 0 10px #0088cc; opacity: 1; }
            100% { text-shadow: 0 0 2px #00aaff, 0 0 5px #0088cc; opacity: 0.9; }
        }
        .neon-header { font-family: 'Arial Black', sans-serif; font-size: 3.5em; color: #fff; animation: wavePulse 1.5s infinite alternate; text-align: center; margin-bottom: 20px; }
        .header { background: linear-gradient(135deg, #0a2a3a, #0a4a6a, #0a6a8a); padding: 30px; border-radius: 30px; text-align: center; margin-bottom: 30px; box-shadow: 0 0 40px rgba(0,100,150,0.5); border: 1px solid #0a8aba; }
        .version-badge { background: black; color: #00aaff; padding: 5px 20px; border-radius: 50px; display: inline-block; margin-top: 10px; font-family: monospace; }
        .stats-header { display: flex; justify-content: center; gap: 20px; margin: 20px 0; flex-wrap: wrap; }
        .stat-header-item { background: rgba(0,0,0,0.7); padding: 10px 25px; border-radius: 50px; border: 1px solid #00aaff; font-weight: bold; }
        .btn { background: #0a6a8a; color: white; border: none; padding: 15px 40px; border-radius: 50px; font-size: 1.2em; cursor: pointer; margin: 10px; border: 2px solid #00aaff; font-weight: bold; }
        .btn:hover { background: #0a8aba; transform: scale(1.02); }
        .config-btn { background: #0a2a3a; color: #00ffcc; border: 2px solid #0a6a8a; padding: 12px 25px; border-radius: 40px; cursor: pointer; margin: 10px; display: inline-flex; align-items: center; gap: 10px; text-decoration: none; font-weight: bold; }
        .config-btn:hover { background: #0a6a8a; color: white; }
        .filtros { display: flex; gap: 10px; justify-content: center; margin: 20px 0; flex-wrap: wrap; }
        .filtro-btn { background: #0a1a2a; color: white; border: 2px solid #0a6a8a; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: bold; }
        .filtro-btn:hover, .filtro-btn.activo { background: #0a6a8a; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
        .stat-card { background: #0a1a2a; padding: 25px; border-radius: 15px; border-left: 8px solid #00aaff; text-align: center; box-shadow: 0 0 10px rgba(0,150,200,0.3); }
        .stat-number { font-size: 3em; color: #00aaff; font-weight: bold; }
        .analysis-section { background: #0a1a2a; border-radius: 20px; padding: 25px; margin: 30px 0; border: 1px solid #0a6a8a; }
        .section-title { color: #00aaff; font-size: 1.8em; margin-bottom: 20px; border-bottom: 2px solid #0a6a8a; padding-bottom: 10px; font-family: monospace; }
        .chart-bar-bg { width: 100%; height: 25px; background: #0a2a3a; border-radius: 12px; margin: 10px 0; overflow: hidden; }
        .chart-bar-fill { height: 100%; background: linear-gradient(90deg, #0a6a8a, #00aaff); border-radius: 12px; transition: width 0.5s; }
        .chart-label { display: flex; justify-content: space-between; color: #00ffcc; margin: 5px 0; font-weight: bold; }
        .incidente-card { background: #0a1a2a; margin: 15px 0; padding: 20px; border-radius: 12px; border-left: 10px solid #00aaff; transition: 0.2s; }
        .incidente-card:hover { background: #0a2a3a; }
        .incidente-titulo { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; color: #fff; }
        .incidente-meta { color: #aaa; display: flex; gap: 20px; flex-wrap: wrap; margin-top: 8px; font-size: 0.9em; }
        .isla-badge { background: #0a6a8a; color: white; padding: 3px 12px; border-radius: 20px; font-size: 0.9em; font-weight: bold; }
        .footer { text-align: center; margin-top: 40px; padding: 20px; background: #0a1a2a; border-radius: 15px; color: #0a6a8a; border: 1px solid #0a6a8a; }
        a { text-decoration: none; }
        .boat-icon { font-size: 1.2em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="neon-header">🌊 DIABOLIC CANARIAS 🌊</h1>
            <div class="version-badge">v{{ version }} · Puerto {{ puerto }}</div>
            <div class="stats-header">
                <div class="stat-header-item">🚤 {{ total_incidentes }} incidentes</div>
                <div class="stat-header-item">📰 {{ total_fuentes }} fuentes</div>
                <div class="stat-header-item">🏝️ {{ total_islas }} islas</div>
            </div>
        </div>
        <div style="text-align: center;">
            <form action="/actualizar" method="post" style="display: inline;"><button class="btn">🔥 ACTUALIZAR DATOS</button></form>
            <a href="/exportar/json" class="config-btn">📥 JSON</a>
            <a href="/exportar/csv" class="config-btn">📥 CSV</a>
        </div>
        <div class="filtros">
            <a href="/" class="filtro-btn {% if filtro == 'todo' %}activo{% endif %}">TODOS</a>
            <a href="/filtro/7d" class="filtro-btn {% if filtro == '7d' %}activo{% endif %}">7 DÍAS</a>
            <a href="/filtro/30d" class="filtro-btn {% if filtro == '30d' %}activo{% endif %}">30 DÍAS</a>
            <a href="/filtro/90d" class="filtro-btn {% if filtro == '90d' %}activo{% endif %}">90 DÍAS</a>
        </div>
        <div class="stats-grid">
            <div class="stat-card"><div>TOTAL</div><div class="stat-number">{{ stats.total }}</div></div>
            <div class="stat-card"><div>ÚLTIMOS 7d</div><div class="stat-number">{{ stats.ultimos_7dias }}</div></div>
            <div class="stat-card"><div>ÚLTIMOS 30d</div><div class="stat-number">{{ stats.ultimos_30dias }}</div></div>
            <div class="stat-card"><div>ÚLTIMOS 90d</div><div class="stat-number">{{ stats.ultimos_90dias }}</div></div>
        </div>
        <div class="analysis-section">
            <div class="section-title">📍 POR ISLAS</div>
            {% set total_islas = stats.islas.values()|sum %}
            {% for isla, cantidad in stats.islas.items() %}
            <div class="chart-label"><span><span class="boat-icon">🏝️</span> {{ isla }}</span><span>{{ cantidad }} ({{ (cantidad / total_islas * 100)|round(1) }}%)</span></div>
            <div class="chart-bar-bg"><div class="chart-bar-fill" style="width: {{ (cantidad / total_islas * 100) }}%;"></div></div>
            {% endfor %}
        </div>
        <div class="analysis-section">
            <div class="section-title">🚤 TIPO DE INCIDENTE</div>
            {% set total_tipos = stats.tipos.values()|sum %}
            {% for tipo, cantidad in stats.tipos.items() %}
            {% set datos = TIPOS_DELITO.get(tipo, {'icono': '❓', 'color': '#666'}) %}
            <div class="chart-label"><span><span style="color: {{ datos.color }};">{{ datos.icono }}</span> {{ tipo|upper }}</span><span>{{ cantidad }} ({{ (cantidad / total_tipos * 100)|round(1) }}%)</span></div>
            <div class="chart-bar-bg"><div class="chart-bar-fill" style="width: {{ (cantidad / total_tipos * 100) }}%;"></div></div>
            {% endfor %}
        </div>
        <div class="analysis-section">
            <div class="section-title">📰 ÚLTIMOS SUCESOS ({{ incidentes|length }})</div>
            {% for inc in incidentes[:25] %}
            {% set tipo_color = TIPOS_DELITO.get(inc.tipo, {'color': '#666'}).color %}
            <div class="incidente-card" style="border-left-color: {{ tipo_color }};">
                <div class="incidente-titulo">{{ inc.titulo }}</div>
                <div class="incidente-meta">
                    <span class="isla-badge">🏝️ {{ inc.isla or '?' }}</span>
                    <span>📅 {{ inc.fecha }}</span>
                    <span>📰 {{ inc.fuente }}</span>
                    <span>🔍 {{ inc.tipo|upper }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="footer">
            <p>🌊 DIABOLIC CANARIAS v{{ version }} · {{ periodicos_activos }} FUENTES ACTIVAS</p>
            <p style="font-size:0.8em; color:#666;">"Un gran poder conlleva una gran responsabilidad"</p>
        </div>
    </div>
</body>
</html>
'''

# ============================================
# FLASK APP (CANARIAS EDITION)
# ============================================

app = Flask(__name__)

@app.route('/')
def home():
    global gestor, IDIOMA_ACTUAL
    incidentes = gestor.datos['incidentes']
    stats = gestor.estadisticas()
    periodicos_activos = len([p for p in PERIODICOS_BASE if p.get('activo', True)])
    return render_template_string(
        HTML_TEMPLATE,
        version=VERSION,
        puerto=PUERTO,
        stats=stats,
        incidentes=incidentes[::-1],
        total_incidentes=stats['total'],
        total_fuentes=len(stats['fuentes']),
        total_islas=len(stats['islas']),
        periodicos_activos=periodicos_activos,
        TIPOS_DELITO=TIPOS_DELITO,
        ISLAS=ISLAS,
        filtro='todo',
        idioma=IDIOMA_ACTUAL
    )

@app.route('/filtro/<periodo>')
def filtro(periodo):
    global gestor, IDIOMA_ACTUAL
    incidentes = gestor.datos['incidentes']
    if periodo == '7d':
        hace = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= hace]
    elif periodo == '30d':
        hace = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= hace]
    elif periodo == '90d':
        hace = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        incidentes = [i for i in incidentes if i.get('fecha', '') >= hace]
    stats = gestor.estadisticas(incidentes)
    periodicos_activos = len([p for p in PERIODICOS_BASE if p.get('activo', True)])
    return render_template_string(
        HTML_TEMPLATE,
        version=VERSION,
        puerto=PUERTO,
        stats=stats,
        incidentes=incidentes[::-1],
        total_incidentes=stats['total'],
        total_fuentes=len(stats['fuentes']),
        total_islas=len(stats['islas']),
        periodicos_activos=periodicos_activos,
        TIPOS_DELITO=TIPOS_DELITO,
        ISLAS=ISLAS,
        filtro=periodo,
        idioma=IDIOMA_ACTUAL
    )

@app.route('/actualizar', methods=['POST'])
def actualizar():
    global gestor
    cprint(f"\n{'='*80}", 'rojo', negrita=True)
    cprint(f"🌊 ACTUALIZANDO SUCESOS EN CANARIAS", 'rojo', negrita=True, fondo=True)
    cprint(f"{'='*80}", 'rojo', negrita=True)
    periodicos = gestor.detector.verificar_todos(PERIODICOS_BASE)
    extractor = ExtractorNoticias(periodicos)
    nuevas = extractor.buscar_todo(paginas=PAGINAS_BUSQUEDA)
    agregadas = gestor.agregar_incidentes(nuevas)
    cprint(f"\n{'='*80}", 'verde', negrita=True)
    cprint(f"✅ {agregadas} NUEVOS INCIDENTES REGISTRADOS", 'verde', negrita=True, fondo=True)
    cprint(f"{'='*80}", 'verde', negrita=True)
    return home()

@app.route('/exportar/json')
def exportar_json():
    global gestor
    return jsonify(gestor.datos)

@app.route('/exportar/csv')
def exportar_csv():
    global gestor, IDIOMA_ACTUAL
    import csv
    from io import StringIO
    si = StringIO()
    cw = csv.writer(si)
    if IDIOMA_ACTUAL == 'es':
        cw.writerow(['Título', 'Fecha', 'Isla', 'Tipo', 'Fuente'])
    else:
        cw.writerow(['Title', 'Date', 'Island', 'Type', 'Source'])
    for inc in gestor.datos['incidentes']:
        cw.writerow([inc['titulo'], inc['fecha'], inc.get('isla', ''), inc.get('tipo', ''), inc['fuente']])
    return si.getvalue()

# ============================================
# MENÚ TERMINAL (CANARIAS EDITION)
# ============================================

def menu():
    global gestor
    while True:
        print(f"\n{Color.ROJO}{'═'*90}{Color.RESET}")
        print(f"{Color.FONDO_ROJO}{Color.NEGRITA}{t('app_name')} v{VERSION} - PUERTO {PUERTO}{Color.RESET}")
        print(f"{Color.ROJO}{'═'*90}{Color.RESET}")

        stats = gestor.estadisticas()
        periodicos_activos = len([p for p in PERIODICOS_BASE if p.get('activo', True)])

        print(f"\n{Color.VERDE}📊 {t('stats_total')}: {stats['total']} {t('incidentes')}{Color.RESET}")
        if stats['total'] > 0:
            pct_7d = round((stats['ultimos_7dias'] / stats['total'] * 100), 1)
        else:
            pct_7d = 0
        print(f"   ⚡ Últimos 7 días: {stats['ultimos_7dias']} ({pct_7d}% del total)")
        print(f"   🔥 Últimos 30 días: {stats['ultimos_30dias']}")
        print(f"   📆 Últimos 90 días: {stats['ultimos_90dias']}")
        print(f"   🏝️ Islas activas: {len(stats['islas'])}")
        print(f"   📰 {t('fuentes')}: {periodicos_activos}")

        print(f"\n{Color.AMARILLO}📋 {t('menu_title')}:{Color.RESET}")
        print(f"{Color.ROJO}[1]{Color.RESET} {t('cmd_buscar')}")
        print(f"{Color.ROJO}[2]{Color.RESET} {t('cmd_analisis')}")
        print(f"{Color.ROJO}[3]{Color.RESET} {t('cmd_conexiones')}")
        print(f"{Color.ROJO}[4]{Color.RESET} {t('cmd_evolucion')}")
        print(f"{Color.ROJO}[5]{Color.RESET} {t('cmd_web')}")
        print(f"{Color.ROJO}[6]{Color.RESET} {t('cmd_ultimos')}")
        print(f"{Color.ROJO}[7]{Color.RESET} {t('cmd_exportar')}")
        print(f"{Color.ROJO}[8]{Color.RESET} {t('cmd_verificar')}")
        print(f"{Color.ROJO}[9]{Color.RESET} {t('cmd_tipos')}")
        print(f"{Color.ROJO}[10]{Color.RESET} {t('cmd_salir')}")

        op = input(f"\n{Color.ROJO}➤ Opción: {Color.RESET}")

        if op == '1':
            periodicos = gestor.detector.verificar_todos(PERIODICOS_BASE)
            extractor = ExtractorNoticias(periodicos)
            nuevas = extractor.buscar_todo(paginas=PAGINAS_BUSQUEDA)
            agregadas = gestor.agregar_incidentes(nuevas)
            cprint(f"\n✅ {agregadas} nuevos incidentes en Canarias", 'verde', negrita=True)
            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '2':
            stats = gestor.estadisticas()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📊 ANÁLISIS COMPLETO CANARIAS{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")

            print(f"\n{Color.VERDE}📈 TENDENCIAS:{Color.RESET}")
            print(f"   Total histórico: {stats['total']}")
            if stats['total'] > 0:
                pct_7d = round((stats['ultimos_7dias'] / stats['total'] * 100), 1)
                pct_30d = round((stats['ultimos_30dias'] / stats['total'] * 100), 1)
                pct_90d = round((stats['ultimos_90dias'] / stats['total'] * 100), 1)
            else:
                pct_7d = pct_30d = pct_90d = 0
            print(f"   Últimos 7 días: {stats['ultimos_7dias']} ({pct_7d}%)")
            print(f"   Últimos 30 días: {stats['ultimos_30dias']} ({pct_30d}%)")
            print(f"   Últimos 90 días: {stats['ultimos_90dias']} ({pct_90d}%)")

            print(f"\n{Color.VERDE}📍 DISTRIBUCIÓN POR ISLAS:{Color.RESET}")
            for isla, cant in sorted(stats['islas'].items(), key=lambda x: x[1], reverse=True):
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                print(f"   {isla}: {cant} ({pct}%)")

            print(f"\n{Color.VERDE}🚤 DISTRIBUCIÓN POR TIPO DE INCIDENTE:{Color.RESET}")
            for tipo, cant in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                print(f"   {tipo.upper()}: {cant} ({pct}%)")

            input(f"\n{Color.GRIS}Enter para continuar...{Color.RESET}")

        elif op == '3':
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}🔗 CONEXIONES ENTRE INCIDENTES (RUTAS MARÍTIMAS){Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")

            incidentes = gestor.datos['incidentes'][-150:]
            if len(incidentes) < 10:
                print(f"{Color.GRIS}   Insuficientes datos. Realiza más búsquedas primero.{Color.RESET}")
                input(f"\n{Color.GRIS}Enter...{Color.RESET}")
                continue

            grupos = defaultdict(list)
            hace_30d = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            for inc in incidentes:
                if inc.get('fecha', '') >= hace_30d:
                    clave = (inc.get('tipo', 'otro'), inc.get('isla', 'Desconocida'))
                    grupos[clave].append(inc)

            patrones = 0
            for (tipo, isla), lista in grupos.items():
                if len(lista) >= 3:
                    print(f"\n{Color.ROJO}🔥 PATRÓN: {len(lista)} {tipo.upper()} en {isla}{Color.RESET}")
                    for inc in sorted(lista, key=lambda x: x['fecha'], reverse=True)[:3]:
                        print(f"   • {inc['fecha']}: {inc['titulo'][:80]}...")
                    fechas = [inc['fecha'] for inc in lista]
                    if fechas:
                        try:
                            dias = (datetime.now() - datetime.strptime(min(fechas), '%Y-%m-%d')).days
                            if dias > 0:
                                freq = round(len(lista) / dias, 1)
                                print(f"   ⚡ Frecuencia: {freq} incidentes/día")
                        except:
                            pass
                    patrones += 1

            print(f"\n{Color.AMARILLO}🔍 PALABRAS CLAVE DESTACADAS (NARCO/MIGRACIÓN):{Color.RESET}")
            palabras_clave = ['narcolancha', 'patera', 'cayuco', 'alijo', 'cocaína', 'hachís', 'rescate', 'naufragio', 'sin papeles']
            for palabra in palabras_clave:
                relacionados = [inc for inc in incidentes if palabra in inc['titulo'].lower()]
                if len(relacionados) >= 2:
                    print(f"\n   {Color.ROJO}• {palabra.upper()}: {len(relacionados)} incidentes{Color.RESET}")
                    for inc in relacionados[:2]:
                        print(f"     - {inc['fecha']} ({inc['isla']}): {inc['titulo'][:60]}...")

            if patrones == 0:
                print(f"\n{Color.GRIS}   No se detectaron patrones significativos en los últimos 30 días.{Color.RESET}")

            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '4':
            evolucion = gestor.evolucion_mensual()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📈 EVOLUCIÓN MENSUAL{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for mes, cant in list(evolucion.items())[-12:]:
                print(f"   {mes}: {cant} incidentes")
            if not evolucion:
                print("   No hay datos suficientes.")
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '5':
            cprint(f"\n🌐 {t('servidor_web')}: http://localhost:{PUERTO}", 'verde', negrita=True)
            cprint(f"   {t('presiona_ctrl_c')}", 'gris')
            app.run(host='127.0.0.1', port=PUERTO, debug=False)

        elif op == '6':
            incidentes = gestor.datos['incidentes'][-20:][::-1]
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📰 ÚLTIMOS 20 SUCESOS EN CANARIAS{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for i, inc in enumerate(incidentes, 1):
                print(f"\n{Color.ROJO}{i:2d}.{Color.RESET} {inc['titulo'][:100]}...")
                print(f"      {inc['fecha']} | {inc.get('isla', '?')} | {inc['fuente']} | {inc.get('tipo', '?')}")
            if not incidentes:
                print("   No hay incidentes registrados.")
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '7':
            with open('export_canarias.json', 'w', encoding='utf-8') as f:
                json.dump(gestor.datos, f, indent=2, ensure_ascii=False)
            with open('export_canarias.csv', 'w', encoding='utf-8') as f:
                f.write("Título,Fecha,Isla,Tipo,Fuente\n")
                for inc in gestor.datos['incidentes']:
                    f.write(f"{inc['titulo'][:100].replace(',', ' ')},{inc['fecha']},{inc.get('isla','')},{inc.get('tipo','')},{inc['fuente']}\n")
            cprint(f"\n✅ Exportados export_canarias.json y export_canarias.csv", 'verde')
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '8':
            gestor.detector.verificar_todos(PERIODICOS_BASE)
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '9':
            stats = gestor.estadisticas()
            print(f"\n{Color.ROJO}{'═'*70}{Color.RESET}")
            print(f"{Color.AMARILLO}📊 DISTRIBUCIÓN POR TIPO{Color.RESET}")
            print(f"{Color.ROJO}{'═'*70}{Color.RESET}")
            for tipo, cant in sorted(stats['tipos'].items(), key=lambda x: x[1], reverse=True):
                pct = round((cant / stats['total'] * 100), 1) if stats['total'] > 0 else 0
                barra = '█' * int(pct // 2) + '░' * (50 - int(pct // 2))
                print(f"   {tipo}: [{barra}] {cant} ({pct}%)")
            input(f"\n{Color.GRIS}Enter...{Color.RESET}")

        elif op == '10':
            cprint(f"\n👋 {t('hasta_pronto')}", 'rojo', negrita=True)
            break

        else:
            cprint(f"\n❌ {t('opcion_invalida')}", 'rojo')
            time.sleep(1)


# ============================================
# MAIN - PUNTO DE ENTRADA (CANARIAS EDITION)
# ============================================

if __name__ == '__main__':
    seleccionar_idioma()

    print(f"""
{Color.ROJO}
╔══════════════════════════════════════════════════════════════════╗
║  🌊 DIABOLIC CANARIAS v{VERSION} - MONITOREO COSTERO 🌊                    ║
║  🚤 NARCOLANCHAS · MIGRACIÓN IRREGULAR · VIOLENCIA               ║
║  🏝️ 7 ISLAS · 35+ FUENTES · ALERTAS EN TIEMPO REAL               ║
║                                         - By Condor2026          ║
║                                            •SpectrumSecurity•    ║
╚══════════════════════════════════════════════════════════════════╝
{Color.RESET}""")
    print(f"{Color.GRIS}🕷️  \"Un gran poder conlleva una gran responsabilidad\" - Spider-Man{Color.RESET}")
    print(f"{Color.GRIS}⚖️  Uso ético y legal. Datos públicos. Enfoque: crimen organizado en el Atlántico.{Color.RESET}")
    print(f"{Color.CIAN}🌊 Especializado en: rutas de narcotráfico, pateras, cayucos,{Color.RESET}")
    print(f"{Color.CIAN}   violencia de bandas, corrupción y sucesos en el archipiélago.{Color.RESET}")

    gestor = GestorDatos()
    stats = gestor.estadisticas()
    print(f"{Color.VERDE}📊 Incidentes en base: {stats['total']}{Color.RESET}")
    print(f"{Color.AMARILLO}⏳ Última actualización: {gestor.datos.get('ultima_actualizacion', 'Nunca')}{Color.RESET}")

    print(f"\n{Color.CIAN}¿Cómo quieres ejecutar?{Color.RESET}")
    print(f"{Color.ROJO}1.{Color.RESET} Modo terminal (10 comandos)")
    print(f"{Color.ROJO}2.{Color.RESET} Modo web directo")

    modo = input(f"\n{Color.ROJO}➤ Elige: {Color.RESET}")

    if modo == '2':
        cprint(f"\n🌐 {t('servidor_web')}: http://localhost:{PUERTO}", 'verde', negrita=True)
        cprint(f"   {t('presiona_ctrl_c')}", 'gris')
        app.run(host='127.0.0.1', port=PUERTO, debug=True)
    else:
        menu()
