#!/bin/bash

# ============================================
# INSTALADOR DE DIABOLIC CANARIAS v1.0
# Soporta: Termux (Android) y Linux
# ============================================

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # Sin color

# Función para mostrar mensajes
print_header() {
    echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}${BOLD}   🌊 DIABOLIC CANARIAS v1.0 - INSTALADOR AUTOMÁTICO 🌊   ${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_ok() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}➡️ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Detectar sistema operativo
detect_os() {
    if command -v pkg &> /dev/null; then
        OS="termux"
        print_ok "Sistema detectado: Termux (Android)"
    elif command -v apt &> /dev/null; then
        OS="linux"
        print_ok "Sistema detectado: Linux (Debian/Ubuntu)"
    else
        print_error "Sistema no soportado. Este instalador funciona solo en Termux o Linux con apt."
        exit 1
    fi
}

# Instalar dependencias del sistema
install_system_deps() {
    print_info "Actualizando repositorios e instalando dependencias del sistema..."
    if [ "$OS" == "termux" ]; then
        pkg update -y
        pkg upgrade -y
        pkg install python git -y
    else
        sudo apt update -y
        sudo apt upgrade -y
        sudo apt install python3 python3-pip git -y
    fi
    print_ok "Dependencias del sistema instaladas"
}

# Instalar dependencias Python
install_python_deps() {
    print_info "Instalando dependencias Python (requests, beautifulsoup4, flask)..."
    if [ "$OS" == "termux" ]; then
        pip install requests beautifulsoup4 flask
    else
        pip3 install requests beautifulsoup4 flask
    fi
    if [ $? -eq 0 ]; then
        print_ok "Dependencias Python instaladas"
    else
        print_error "Error al instalar dependencias Python"
        exit 1
    fi
}

# Clonar repositorio si no existe
clone_repo() {
    REPO_URL="https://github.com/Condor2026/Diabolic_Canarias"
    REPO_DIR="Diabolic_Canarias"
    if [ -d "$REPO_DIR" ]; then
        print_warning "El directorio $REPO_DIR ya existe. Se omitirá la clonación."
        cd "$REPO_DIR"
    else
        print_info "Clonando repositorio desde GitHub..."
        git clone "$REPO_URL" "$REPO_DIR"
        if [ $? -eq 0 ]; then
            print_ok "Repositorio clonado correctamente"
            cd "$REPO_DIR"
        else
            print_error "No se pudo clonar el repositorio. Verifica tu conexión a Internet."
            exit 1
        fi
    fi
}

# Crear archivo requirements.txt si no existe
create_requirements() {
    if [ ! -f "requirements.txt" ]; then
        print_info "Creando archivo requirements.txt..."
        cat > requirements.txt << EOF
# Dependencias para DIABOLIC CANARIAS v1.0
requests>=2.25.0
beautifulsoup4>=4.9.3
flask>=2.0.0
EOF
        print_ok "requirements.txt creado"
    else
        print_info "requirements.txt ya existe"
    fi
}

# Dar permisos de ejecución al script principal
set_permissions() {
    if [ -f "Diabolic_Canarias.py" ]; then
        chmod +x Diabolic_Canarias.py
        print_ok "Permisos de ejecución asignados"
    else
        print_warning "No se encontró Diabolic_Canarias.py. Asegúrate de que el script principal esté en el directorio."
    fi
}

# Mostrar mensaje final
print_footer() {
    echo ""
    echo -e "${GREEN}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD}              INSTALACIÓN COMPLETADA CON ÉXITO                ${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════════════${NC}"
    echo ""
    print_info "Para ejecutar DIABOLIC CANARIAS:"
    echo -e "   cd ${YELLOW}Diabolic_Canarias${NC}"
    echo -e "   python ${YELLOW}Diabolic_Canarias.py${NC}   (o python3 en Linux)"
    echo ""
    print_info "Si quieres ejecutar ahora mismo:"
    echo -e "   ${CYAN}cd Diabolic_Canarias && python Diabolic_Canarias.py${NC}"
    echo ""
    echo -e "${BLUE}🕷️  \"Un gran poder conlleva una gran responsabilidad\"${NC}"
    echo -e "${BLUE}   - Spider-Man${NC}"
    echo ""
}

# Ejecución principal
main() {
    print_header
    detect_os
    install_system_deps
    install_python_deps
    clone_repo
    create_requirements
    set_permissions
    print_footer
}

main
