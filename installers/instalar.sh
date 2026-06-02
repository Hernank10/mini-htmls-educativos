#!/bin/bash
# INSTALADOR - mini-htmls-educativos
# Lecciones HTML interactivas para aprender Lengua Castellana

echo "═══════════════════════════════════════════════════════════════════"
echo "   📖 MINI HTMLs EDUCATIVOS - INSTALADOR"
echo "═══════════════════════════════════════════════════════════════════"

INSTALL_DIR="$HOME/mini_htmls_educativos"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "✅ Instalando en: $INSTALL_DIR"

# Clonar repositorio
if [ -d "mini-htmls-educativos" ]; then
    cd mini-htmls-educativos && git pull && cd ..
else
    git clone https://github.com/Hernank10/mini-htmls-educativos.git
fi

# Crear lanzador
cat > servir.sh << 'LAUNCHER'
#!/bin/bash
cd "$HOME/mini_htmls_educativos/mini-htmls-educativos"
echo "🌐 Servidor: http://localhost:8000"
python3 -m http.server 8000
LAUNCHER
chmod +x servir.sh

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "🎉 ¡INSTALACIÓN COMPLETADA!"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Ubicación: $INSTALL_DIR/mini-htmls-educativos"
echo ""
echo "🚀 Para iniciar el servidor:"
echo "   cd $INSTALL_DIR && ./servir.sh"
echo ""
echo "🌐 O visita: https://hernank10.github.io/mini-htmls-educativos/"
