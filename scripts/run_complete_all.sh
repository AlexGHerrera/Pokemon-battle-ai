#!/bin/bash
# Script para ejecutar el completado de todos los Pokemon en background
# Uso: bash scripts/run_complete_all.sh

echo "🔥 Pokemon Data Completer - Ejecución Nocturna"
echo "================================================"
echo ""
echo "📊 Completando 229 Pokemon restantes..."
echo "⏱️  Tiempo estimado: 2-3 horas"
echo "📝 Log: logs/pokemon_completion.log"
echo ""

# Crear directorio de logs si no existe
mkdir -p logs

# Ejecutar en background con logging
nohup python scripts/complete_pokemon_data.py --all > logs/pokemon_completion.log 2>&1 &

# Guardar PID
PID=$!
echo $PID > logs/pokemon_completion.pid

echo "✅ Proceso iniciado en background"
echo "📋 PID: $PID"
echo ""
echo "🔍 Comandos útiles:"
echo "  • Ver progreso en tiempo real:"
echo "    tail -f logs/pokemon_completion.log"
echo ""
echo "  • Verificar si está corriendo:"
echo "    ps aux | grep $PID"
echo ""
echo "  • Detener el proceso (si necesario):"
echo "    kill $PID"
echo ""
echo "📧 Al terminar, revisa:"
echo "  • output/pokemon_completed.txt"
echo "  • output/pokemon_completed.json"
echo ""
echo "🌙 ¡Buenas noches! El script trabajará mientras duermes."
