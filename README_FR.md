# 🚀 Outil de Migration Shopify vers WordPress/WooCommerce

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/shopify-wordpress-migrator)
[![Licence](https://img.shields.io/badge/licence-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.2+-blue.svg)](https://reactjs.org/)

**Outil de migration de qualité professionnelle pour des transitions fluides entre plateformes e-commerce**

[English Version](README.md) | **Version Française**

## 📋 Table des Matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Démarrage Rapide](#-démarrage-rapide)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Documentation API](#-documentation-api)
- [Dépannage](#-dépannage)
- [FAQ](#-faq)

## ✨ Fonctionnalités

### Capacités de Migration Principales

- **🔄 Migration Bidirectionnelle**
  - Shopify → WordPress/WooCommerce
  - WordPress/WooCommerce → Shopify
  
- **📦 Migration Complète des Données**
  - ✅ Produits (>10 000 produits supportés)
  - ✅ Variantes et attributs de produits
  - ✅ Clients et groupes de clients
  - ✅ Commandes et historique des commandes
  - ✅ Niveaux de stock et gestion SKU
  - ✅ Images de produits avec optimisation
  - ✅ Catégories et collections
  - ✅ Tags et métadonnées
  - ✅ Données SEO (méta-titres, descriptions)
  - ✅ Avis et notes clients
  - ✅ Coupons et réductions
  - ✅ Articles de blog
  - ✅ Produits numériques/téléchargeables
  - ✅ Support multi-devises
  - ✅ Points de fidélité et récompenses

### Fonctionnalités Avancées

- **⚡ Performance et Scalabilité**
  - Traitement asynchrone des tâches avec Celery
  - Traitement par lots pour grands volumes de données
  - Limitation du taux et throttling API
  - Cache Redis pour performances optimales
  - Exécution concurrente des tâches
  
- **🎨 Optimisation des Images**
  - Compression automatique des images
  - Génération de miniatures multiples
  - Conversion de format (JPEG, PNG, WebP)
  - Redimensionnement intelligent
  
- **🔒 Sécurité et Fiabilité**
  - Stockage chiffré des identifiants
  - Sauvegarde automatique avant migration
  - Mécanisme de nouvelle tentative avec backoff exponentiel
  - Journalisation détaillée des erreurs
  - Rollback des transactions en cas d'échec
  
- **📊 Monitoring et Rapports**
  - Tableau de bord de migration en temps réel
  - Suivi de la progression avec WebSockets
  - Rapports de migration détaillés
  - Export des statistiques vers Excel/CSV
  - Notifications par email
  - Métriques Prometheus
  
- **🛠️ Modes de Migration**
  - **Migration Complète :** Transfert complet de boutique
  - **Incrémentale :** Mise à jour des données existantes
  - **Mode Test :** Aperçu sans modifications
  - **Mode Batch :** Traitement par lots
  - **Synchro Temps Réel :** Synchronisation continue

### SEO & Marketing

- **🔍 Préservation du SEO**
  - Méta-titres et descriptions
  - Mapping des slugs d'URL
  - Génération de redirections 301 (Nginx/Apache)
  - Génération de sitemap.xml
  - URLs canoniques
  
- **📱 Fonctionnalités Supplémentaires**
  - Intégration de webhooks pour outils tiers
  - Mapping de champs personnalisés
  - Migration des menus de navigation
  - Support multilingue
  - Codes-barres et références fournisseurs

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Frontend (React)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Tableau   │  │Migration │  │Monitoring│  │Paramètres│   │
│  │de bord   │  │          │  │          │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
┌────────────────────────▼────────────────────────────────────┐
│              Backend API (FastAPI)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Service   │  │Service   │  │Service   │  │Service   │   │
│  │Auth      │  │Migration │  │Monitoring│  │Webhooks  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────┬──────────────┬──────────────┬─────────────────────┘
         │              │              │
    ┌────▼────┐    ┌────▼────┐    ┌───▼────┐
    │PostgreSQL│    │  Redis  │    │ Celery │
    │   DB    │    │  Cache  │    │Workers │
    └─────────┘    └─────────┘    └────────┘
```

## 🚀 Démarrage Rapide

### Prérequis

- **Python 3.11+**
- **Node.js 18+** et npm/yarn
- **PostgreSQL 14+**
- **Redis 7+**
- **Boutique Shopify** avec identifiants API
- **Site WordPress/WooCommerce** avec API REST activée

### Installation Rapide

```bash
# Cloner le dépôt
git clone https://github.com/yourusername/shopify-wordpress-migrator.git
cd shopify-wordpress-migrator

# Exécuter le script d'installation
chmod +x scripts/setup.sh
./scripts/setup.sh

# Démarrer l'application
./scripts/start.sh
```

Visitez `http://localhost:3000` pour accéder à l'application.

## 📦 Installation Détaillée

### 1. Configuration du Backend

```bash
# Naviguer vers le répertoire backend
cd backend

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier d'environnement
cp ../config/.env.example .env

# Éditer .env avec vos identifiants
nano .env

# Initialiser la base de données
alembic upgrade head

# Démarrer Redis (si pas déjà en cours d'exécution)
redis-server

# Démarrer les workers Celery
celery -A tasks.celery_app worker --loglevel=info -c 4

# Dans un nouveau terminal, démarrer Celery beat
celery -A tasks.celery_app beat --loglevel=info

# Démarrer le serveur FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Configuration du Frontend

```bash
# Naviguer vers le répertoire frontend
cd frontend

# Installer les dépendances
npm install
# ou
yarn install

# Copier le fichier d'environnement
cp .env.example .env.local

# Éditer .env.local
nano .env.local

# Démarrer le serveur de développement
npm run dev
# ou
yarn dev
```

### 3. Configuration de la Base de Données

```bash
# Créer la base de données PostgreSQL
createdb migrator_db

# Exécuter les migrations
cd backend
alembic upgrade head

# (Optionnel) Alimenter avec des données d'exemple
python scripts/seed_database.py
```

## ⚙️ Configuration

### Variables d'Environnement

Créez un fichier `.env` avec les paramètres suivants :

```bash
# Application
APP_NAME=Shopify-WordPress Migrator
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=votre-clé-secrète

# Configuration Shopify
SHOPIFY_SHOP_NAME=votre-boutique.myshopify.com
SHOPIFY_API_KEY=votre-clé-api
SHOPIFY_API_SECRET=votre-secret-api
SHOPIFY_ACCESS_TOKEN=votre-token-accès

# Configuration WooCommerce
WOOCOMMERCE_URL=https://votre-site-wordpress.com
WOOCOMMERCE_CONSUMER_KEY=ck_votre_clé_consommateur
WOOCOMMERCE_CONSUMER_SECRET=cs_votre_secret_consommateur

# WordPress (pour migration de blog)
WORDPRESS_URL=https://votre-site-wordpress.com
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=votre-mot-de-passe-application

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/migrator_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Notifications Email (optionnel)
ENABLE_EMAIL_NOTIFICATIONS=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre-email@gmail.com
SMTP_PASSWORD=votre-mot-de-passe-app
```

### Obtention des Identifiants API

#### Shopify

1. Connectez-vous à votre panneau d'administration Shopify
2. Allez dans **Apps** → **Développer des apps**
3. Cliquez sur **Créer une app**
4. Configurez les scopes suivants :
   - `read_products`, `write_products`
   - `read_customers`, `write_customers`
   - `read_orders`, `write_orders`
   - `read_inventory`, `write_inventory`
   - `read_content`, `write_content`
5. Installez l'app et copiez le **Token d'accès**

#### WooCommerce

1. Connectez-vous à votre admin WordPress
2. Allez dans **WooCommerce** → **Réglages** → **Avancé** → **API REST**
3. Cliquez sur **Ajouter une clé**
4. Définissez les permissions en **Lecture/Écriture**
5. Copiez la **Clé consommateur** et le **Secret consommateur**

#### WordPress (pour articles de blog)

1. Allez dans **Utilisateurs** → **Profil**
2. Descendez jusqu'à **Mots de passe d'application**
3. Créez un nouveau mot de passe d'application
4. Copiez le mot de passe généré

## 🎯 Utilisation

### Interface Web

1. **Accéder au Tableau de Bord**
   ```
   http://localhost:3000
   ```

2. **Connexion** avec vos identifiants (par défaut : admin/admin)

3. **Configurer la Connexion**
   - Naviguez vers **Paramètres**
   - Entrez vos identifiants Shopify et WooCommerce
   - Testez la connexion

4. **Démarrer la Migration**
   - Allez dans **Migration** → **Configuration**
   - Sélectionnez la direction de migration
   - Choisissez ce que vous souhaitez migrer
   - Sélectionnez le mode de migration
   - Cliquez sur **Démarrer la Migration**

5. **Surveiller la Progression**
   - Visualisez la progression en temps réel dans le tableau de bord
   - Consultez les logs détaillés dans **Monitoring**
   - Téléchargez les rapports une fois terminé

### Script Python (CLI)

```bash
cd backend

# Migration complète (Shopify → WooCommerce)
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode full \
  --entities products,customers,orders

# Migration test (aperçu uniquement)
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode test \
  --entities products

# Migration par lots
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode batch \
  --batch-size 100 \
  --entities products

# Migrer des produits spécifiques
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --product-ids 123456,789012 \
  --entities products

# Avec sauvegarde
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode full \
  --entities products,customers \
  --backup
```

### Options CLI

```
Options:
  --direction       Direction de migration (shopify_to_woocommerce | woocommerce_to_shopify)
  --mode           Mode de migration (full | incremental | test | batch)
  --entities       Liste séparée par virgules d'entités (products, customers, orders, etc.)
  --batch-size     Nombre d'éléments par lot (défaut: 50)
  --product-ids    Liste séparée par virgules d'IDs de produits
  --backup         Créer une sauvegarde avant migration
  --optimize-images Optimiser les images pendant la migration
  --generate-redirects Générer les redirections 301
  --dry-run        Aperçu des modifications sans exécution
  --verbose        Activer les logs détaillés
  --config         Chemin vers un fichier de configuration personnalisé
```

## 📚 Documentation API

### Authentification

Toutes les requêtes API nécessitent un token JWT :

```bash
# Obtenir le token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Utiliser le token
curl -X GET http://localhost:8000/api/products \
  -H "Authorization: Bearer <votre-token>"
```

### Points de Terminaison Principaux

```http
# Migration
POST   /api/migration/start          # Démarrer une nouvelle migration
GET    /api/migration/jobs           # Lister tous les jobs
GET    /api/migration/jobs/{id}      # Obtenir les détails d'un job
POST   /api/migration/jobs/{id}/cancel  # Annuler un job

# Produits
GET    /api/products                 # Lister les produits
POST   /api/products/migrate         # Migrer les produits
GET    /api/products/{id}            # Obtenir les détails d'un produit

# Monitoring
GET    /api/monitoring/stats         # Obtenir les statistiques
GET    /api/monitoring/jobs/{id}/progress  # Progression d'un job
GET    /api/monitoring/logs          # Logs de migration

# Webhooks
POST   /api/webhooks/shopify         # Point de terminaison webhook Shopify
POST   /api/webhooks/woocommerce     # Point de terminaison webhook WooCommerce
```

Documentation API complète disponible à : `http://localhost:8000/api/docs`

## 🔧 Dépannage

### Problèmes Courants

#### 1. Échec de Connexion

**Problème :** Impossible de se connecter à l'API Shopify/WooCommerce

**Solution :**
- Vérifier les identifiants API dans `.env`
- Vérifier les permissions/scopes de l'API
- S'assurer que l'URL de la boutique est correcte
- Tester la connexion : `python scripts/test_connection.py`

#### 2. Migration Bloquée

**Problème :** La migration s'arrête à un certain pourcentage

**Solution :**
- Vérifier que les workers Celery sont en cours d'exécution
- Consulter les logs : `tail -f /var/log/migrator/app.log`
- Augmenter la concurrence des workers
- Vérifier les limites de taux

#### 3. Images Non Migrées

**Problème :** Les images de produits sont manquantes

**Solution :**
- Vérifier que les URLs d'images sont accessibles
- Vérifier l'espace disque dans `IMAGE_STORAGE_PATH`
- Activer les logs de débogage
- Essayer le téléchargement manuel d'images

#### 4. Erreurs de Base de Données

**Problème :** Erreurs de connexion PostgreSQL

**Solution :**
```bash
# Vérifier que PostgreSQL est en cours d'exécution
sudo systemctl status postgresql

# Réinitialiser la base de données
dropdb migrator_db
createdb migrator_db
alembic upgrade head
```

#### 5. Erreurs de Limite de Taux

**Problème :** Trop de requêtes API

**Solution :**
- Réduire `BATCH_SIZE` dans la config
- Augmenter `RATE_LIMIT_WINDOW`
- Utiliser le mode incrémental
- Planifier la migration en heures creuses

### Mode Débogage

Activer les logs détaillés :

```bash
# Dans .env
DEBUG=true
LOG_LEVEL=DEBUG

# Exécuter avec sortie détaillée
python scripts/migrate.py --verbose
```

## ❓ FAQ

### Questions Générales

**Q : Combien de temps prend une migration ?**
R : Cela dépend de la taille de votre boutique. En moyenne :
- 100 produits : ~15 minutes
- 1000 produits : ~2 heures
- 10000+ produits : 4-8 heures

**Q : Puis-je annuler une migration en cours ?**
R : Oui, vous pouvez annuler via le tableau de bord ou la CLI. Les données déjà migrées resteront.

**Q : La migration affecte-t-elle ma boutique en production ?**
R : Non, la migration lit les données sans modifier la source. Utilisez le mode test pour un aperçu.

**Q : Que se passe-t-il en cas d'erreur ?**
R : Le système effectue automatiquement des nouvelles tentatives. Les erreurs sont enregistrées dans les rapports.

**Q : Puis-je migrer plusieurs fois ?**
R : Oui, utilisez le mode incrémental pour mettre à jour les données existantes.

### Questions Techniques

**Q : Quelles sont les limites de taux API ?**
R : 
- Shopify : 2 appels/seconde (REST API)
- WooCommerce : 25 requêtes/10 secondes

**Q : Comment optimiser pour les grandes boutiques ?**
R :
- Augmenter les workers Celery
- Utiliser le mode batch
- Activer le cache Redis
- Planifier en heures creuses

**Q : Les mots de passe clients sont-ils migrés ?**
R : Les mots de passe hashés peuvent être migrés, ou vous pouvez forcer une réinitialisation.

**Q : Le multi-devises est-il supporté ?**
R : Oui, avec le paramètre `FEATURE_MULTI_CURRENCY=true`

## 📊 Performance

Vitesses de migration typiques (testé sur AWS t3.large) :

- **Produits :** ~500-1000 par heure
- **Clients :** ~2000-3000 par heure
- **Commandes :** ~1000-1500 par heure

Pour les boutiques avec >10 000 produits, nous recommandons :
- Utiliser le mode batch
- Exécuter en heures creuses
- Augmenter les workers Celery
- Activer le cache Redis

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md)

## 📞 Support

- 📖 Consultez la [Documentation](docs/)
- 🐛 [Signaler un Problème](https://github.com/yourusername/shopify-wordpress-migrator/issues)
- 💬 [Forum Communautaire](https://community.example.com)
- 📧 Email : support@example.com

## 📄 Licence

Ce projet est sous licence MIT - voir [LICENSE](LICENSE)

## 🙏 Remerciements

- Documentation API Shopify
- API REST WooCommerce
- Framework FastAPI
- Communauté React

---

**Fait avec ❤️ pour la communauté e-commerce**

*For English documentation, see [README.md](README.md)*
