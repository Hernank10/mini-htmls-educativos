#!/bin/bash
echo "========================================="
echo "Compilando documentos LaTeX"
echo "========================================="

echo ""
echo "1. Compilando proyecto de investigación (Lengua Castellana)..."
pdflatex proyecto_investigacion_castellano.tex
pdflatex proyecto_investigacion_castellano.tex

echo ""
echo "2. Compilando artículo pedagógico (Lengua Castellana)..."
pdflatex articulo_pedagogico_castellano.tex
pdflatex articulo_pedagogico_castellano.tex

echo ""
echo "========================================="
echo "✅ Compilación completada"
echo "📄 Archivos generados:"
ls -la *.pdf
echo "========================================="
