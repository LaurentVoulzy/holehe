#!/bin/bash
# Script de conversion Markdown → PDF
# La Bête V6 Ultimate

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║        📄 CONVERSION GUIDE PDF - LA BÊTE 🐺             ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Vérifier si pandoc est installé
if ! command -v pandoc &> /dev/null
then
    echo "❌ Pandoc n'est pas installé!"
    echo ""
    echo "Installation:"
    echo "  Ubuntu/Debian: sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra"
    echo "  MacOS: brew install pandoc basictex"
    echo "  Windows: https://pandoc.org/installing.html"
    echo ""
    exit 1
fi

echo "✅ Pandoc détecté"
echo ""

# Fichier source
INPUT="GUIDE_INSTALLATION_PDF.md"
OUTPUT="LA_BETE_V6_GUIDE_INSTALLATION.pdf"

echo "📄 Fichier source: $INPUT"
echo "📄 Fichier sortie: $OUTPUT"
echo ""

# Conversion
echo "🔄 Conversion en cours..."
echo ""

pandoc "$INPUT" \
    -o "$OUTPUT" \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --highlight-style=tango \
    --variable geometry:margin=2cm \
    --variable fontsize=11pt \
    --variable papersize=a4 \
    --variable colorlinks=true \
    --variable linkcolor=blue \
    --variable urlcolor=blue \
    --variable toccolor=black \
    -V mainfont="DejaVu Sans" \
    -V monofont="DejaVu Sans Mono"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ CONVERSION RÉUSSIE!"
    echo ""
    echo "📄 PDF créé: $OUTPUT"
    echo "📊 Taille: $(du -h "$OUTPUT" | cut -f1)"
    echo ""
    echo "🎉 Votre guide PDF est prêt!"
    echo ""
else
    echo ""
    echo "❌ Erreur lors de la conversion"
    echo ""
    echo "Si erreur LaTeX:"
    echo "  - Installer: sudo apt-get install texlive-xetex texlive-fonts-extra"
    echo ""
fi
