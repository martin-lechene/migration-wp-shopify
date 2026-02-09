# 🚀 Guide de Démarrage Rapide - 5 Minutes

Ce guide vous permet de démarrer avec l'outil de migration en moins de 5 minutes.

## Prérequis Rapides

Assurez-vous d'avoir installé :
- ✅ Python 3.11+
- ✅ Node.js 18+
- ✅ PostgreSQL 14+
- ✅ Redis 7+

## Installation Express

### Option 1 : Script Automatique (Recommandé)

```bash
# Cloner le projet
git clone https://github.com/yourusername/shopify-wordpress-migrator.git
cd shopify-wordpress-migrator

# Exécuter l'installation automatique
chmod +x scripts/setup.sh
./scripts/setup.sh

# Démarrer l'application
./scripts/start.sh
```

✅ C'est tout ! Ouvrez http://localhost:3000

### Option 2 : Docker (Le Plus Rapide)

```bash
# Cloner le projet
git clone https://github.com/yourusername/shopify-wordpress-migrator.git
cd shopify-wordpress-migrator

# Copier et configurer .env
cp config/.env.example config/.env
nano config/.env  # Ajoutez vos identifiants API

# Démarrer avec Docker
docker-compose up -d

# Vérifier les logs
docker-compose logs -f
```

✅ Accédez à http://localhost:3000

## Configuration Minimale

Éditez le fichier `.env` avec au minimum :

```bash
# Shopify
SHOPIFY_SHOP_NAME=votre-boutique.myshopify.com
SHOPIFY_API_KEY=votre-clé-api
SHOPIFY_ACCESS_TOKEN=votre-token

# WooCommerce
WOOCOMMERCE_URL=https://votre-site.com
WOOCOMMERCE_CONSUMER_KEY=ck_votre_clé
WOOCOMMERCE_CONSUMER_SECRET=cs_votre_secret

# Base de données
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/migrator_db
```

## Première Migration (Test)

### Via l'Interface Web

1. Ouvrez http://localhost:3000
2. Connectez-vous (admin/admin)
3. Allez dans **Settings** → Testez la connexion
4. Cliquez sur **New Migration**
5. Sélectionnez :
   - Direction : Shopify → WooCommerce
   - Mode : **Test** (aucune modification)
   - Entités : Products
6. Cliquez sur **Start Migration**

### Via CLI

```bash
cd backend
source venv/bin/activate

# Migration test (aperçu uniquement, aucune modification)
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode test \
  --entities products
```

## Vérification Rapide

Testez que tout fonctionne :

```bash
# Backend
curl http://localhost:8000/health
# Devrait retourner : {"status": "healthy"}

# Test connexion API
cd backend
python scripts/test_connection.py

# Frontend
curl http://localhost:3000
# Devrait retourner le HTML de l'application
```

## Commandes Essentielles

```bash
# Démarrer l'application
./scripts/start.sh

# Arrêter l'application
./scripts/stop.sh

# Voir les logs
tail -f logs/app.log

# Migration rapide (CLI)
cd backend
python scripts/migrate.py --direction shopify_to_woocommerce --mode test --entities products

# Liste des jobs
python scripts/migrate.py list-jobs

# Statut d'un job
python scripts/migrate.py status <job-id>
```

## Prochaines Étapes

Maintenant que tout fonctionne :

1. 📖 Lisez la [documentation complète](README_FR.md)
2. 🎯 Configurez votre [première migration réelle](docs/guides/first-migration.md)
3. ⚙️ Optimisez les [paramètres de performance](docs/guides/performance.md)
4. 📊 Explorez le [dashboard de monitoring](http://localhost:3000/monitoring)

## Aide Rapide

### Problème : "Cannot connect to database"
```bash
# Vérifier PostgreSQL
sudo systemctl status postgresql
sudo systemctl start postgresql

# Créer la base de données
createdb migrator_db
```

### Problème : "Redis connection failed"
```bash
# Démarrer Redis
redis-server --daemonize yes

# Vérifier
redis-cli ping  # Devrait retourner PONG
```

### Problème : "API credentials invalid"
```bash
# Vérifier vos identifiants dans .env
nano backend/.env

# Tester la connexion
python backend/scripts/test_connection.py
```

## Support

- 🐛 Problème ? [Créer une issue](https://github.com/yourusername/shopify-wordpress-migrator/issues)
- 💬 Question ? [Forum communautaire](https://community.example.com)
- 📧 Email : support@example.com

## Ressources

- [Documentation complète](README_FR.md)
- [Guide de migration](docs/guides/migration-guide.md)
- [FAQ](docs/FAQ.md)
- [Exemples](docs/examples/)

---

**Prêt à migrer ? C'est parti ! 🚀**
