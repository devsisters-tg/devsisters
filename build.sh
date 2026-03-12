#!/usr/bin/env bash
# ─── Script de build pour Render ──────────────────────────────────────────────
# Ce fichier est exécuté automatiquement par Render à chaque déploiement.
# Dans Render > Settings > Build Command : ./build.sh

set -o errexit  # Arrête le script si une commande échoue

echo "📦 Installation des dépendances..."
pip install -r requirements.txt

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "🗄️ Application des migrations..."
python manage.py migrate

echo "✅ Build terminé avec succès !"
