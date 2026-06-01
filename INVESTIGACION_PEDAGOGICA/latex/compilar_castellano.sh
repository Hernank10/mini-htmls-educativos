#!/bin/bash
echo "========================================="
echo "Compilando proyecto de investigación"
echo "Lengua Castellana"
echo "========================================="

echo ""
echo "1. Compilación principal..."
pdflatex proyecto_investigacion_castellano.tex

echo ""
echo "2. Segunda pasada para referencias..."
pdflatex proyecto_investigacion_castellano.tex

echo ""
echo "========================================="
echo "✅ Compilación completada"
echo "📄 Archivo: proyecto_investigacion_castellano.pdf"
echo "========================================="
ls -la *.pdf
