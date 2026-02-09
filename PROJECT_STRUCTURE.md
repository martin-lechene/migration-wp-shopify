# 📁 Structure du Projet - Shopify to WordPress Migrator

Ce document décrit l'organisation complète du projet.

## Vue d'Ensemble de la Structure

```
shopify-wordpress-migrator/
├── backend/                    # Application Backend Python/FastAPI
│   ├── api/                   # Routes et endpoints API
│   │   └── routes/           # Définitions des routes
│   │       ├── auth.py       # Authentification et autorisation
│   │       ├── migration.py  # Endpoints de migration
│   │       ├── products.py   # Gestion des produits
│   │       ├── customers.py  # Gestion des clients
│   │       ├── orders.py     # Gestion des commandes
│   │       ├── monitoring.py # Monitoring et statistiques
│   │       ├── webhooks.py   # Webhooks entrants
│   │       └── backup.py     # Gestion des sauvegardes
│   │
│   ├── config/               # Configuration
│   │   ├── __init__.py
│   │   └── settings.py       # Paramètres de l'application
│   │
│   ├── core/                 # Fonctionnalités core
│   │   ├── __init__.py
│   │   ├── database.py       # Configuration base de données
│   │   ├── logging.py        # Configuration des logs
│   │   ├── exceptions.py     # Gestion des exceptions
│   │   ├── security.py       # Sécurité et chiffrement
│   │   └── dependencies.py   # Dépendances FastAPI
│   │
│   ├── models/               # Modèles de données (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── migration.py      # Modèle MigrationJob
│   │   ├── product.py        # Modèle Product
│   │   ├── customer.py       # Modèle Customer
│   │   ├── order.py          # Modèle Order
│   │   ├── user.py           # Modèle User
│   │   └── log.py            # Modèle Log
│   │
│   ├── services/             # Logique métier
│   │   ├── __init__.py
│   │   ├── product_migration_service.py    # Migration produits
│   │   ├── customer_migration_service.py   # Migration clients
│   │   ├── order_migration_service.py      # Migration commandes
│   │   ├── shopify_service.py              # Client API Shopify
│   │   ├── woocommerce_service.py          # Client API WooCommerce
│   │   ├── wordpress_service.py            # Client API WordPress
│   │   ├── image_service.py                # Optimisation d'images
│   │   ├── backup_service.py               # Sauvegardes
│   │   ├── seo_service.py                  # Gestion SEO
│   │   ├── notification_service.py         # Notifications
│   │   └── webhook_service.py              # Gestion webhooks
│   │
│   ├── tasks/                # Tâches Celery asynchrones
│   │   ├── __init__.py
│   │   ├── celery_app.py     # Configuration Celery
│   │   ├── migration_tasks.py # Tâches de migration
│   │   ├── image_tasks.py    # Traitement d'images
│   │   ├── backup_tasks.py   # Tâches de backup
│   │   └── scheduled_tasks.py # Tâches planifiées
│   │
│   ├── utils/                # Utilitaires
│   │   ├── __init__.py
│   │   ├── rate_limiter.py   # Limitation de taux
│   │   ├── retry.py          # Logique de retry
│   │   ├── validators.py     # Validateurs
│   │   ├── helpers.py        # Fonctions helper
│   │   └── mappers.py        # Mappers de données
│   │
│   ├── tests/                # Tests
│   │   ├── __init__.py
│   │   ├── conftest.py       # Configuration pytest
│   │   ├── test_api/         # Tests API
│   │   ├── test_services/    # Tests services
│   │   ├── test_models/      # Tests modèles
│   │   └── test_integration/ # Tests d'intégration
│   │
│   ├── alembic/              # Migrations de base de données
│   │   ├── versions/         # Versions de migration
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── scripts/              # Scripts utilitaires
│   │   ├── migrate.py        # Script CLI de migration
│   │   ├── test_connection.py # Test des connexions
│   │   ├── seed_database.py  # Données de test
│   │   └── backup.py         # Script de backup
│   │
│   ├── main.py               # Point d'entrée FastAPI
│   ├── requirements.txt      # Dépendances Python
│   ├── Dockerfile           # Configuration Docker
│   ├── .env.example         # Exemple de configuration
│   └── alembic.ini          # Configuration Alembic
│
├── frontend/                 # Application Frontend React
│   ├── public/              # Fichiers statiques
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── assets/
│   │
│   ├── src/
│   │   ├── assets/          # Images, fonts, etc.
│   │   │   ├── images/
│   │   │   ├── icons/
│   │   │   └── styles/
│   │   │
│   │   ├── components/      # Composants React
│   │   │   ├── common/      # Composants communs
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Table.tsx
│   │   │   │   ├── Loading.tsx
│   │   │   │   └── ErrorBoundary.tsx
│   │   │   │
│   │   │   ├── layouts/     # Layouts
│   │   │   │   ├── MainLayout.tsx
│   │   │   │   ├── AuthLayout.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Footer.tsx
│   │   │   │
│   │   │   ├── dashboard/   # Composants dashboard
│   │   │   │   ├── StatsCard.tsx
│   │   │   │   ├── MigrationJobCard.tsx
│   │   │   │   ├── RealtimeMonitor.tsx
│   │   │   │   └── ActivityChart.tsx
│   │   │   │
│   │   │   ├── migration/   # Composants migration
│   │   │   │   ├── MigrationSetup.tsx
│   │   │   │   ├── EntitySelector.tsx
│   │   │   │   ├── DirectionSelector.tsx
│   │   │   │   ├── ModeSelector.tsx
│   │   │   │   ├── ProgressBar.tsx
│   │   │   │   └── ResultsTable.tsx
│   │   │   │
│   │   │   └── settings/    # Composants paramètres
│   │   │       ├── APISettings.tsx
│   │   │       ├── GeneralSettings.tsx
│   │   │       ├── NotificationSettings.tsx
│   │   │       └── SecuritySettings.tsx
│   │   │
│   │   ├── hooks/           # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useMigration.ts
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useApi.ts
│   │   │   └── useLocalStorage.ts
│   │   │
│   │   ├── pages/           # Pages principales
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── MigrationSetup.tsx
│   │   │   ├── ProductsMigration.tsx
│   │   │   ├── CustomersMigration.tsx
│   │   │   ├── OrdersMigration.tsx
│   │   │   ├── Monitoring.tsx
│   │   │   ├── Reports.tsx
│   │   │   ├── Settings.tsx
│   │   │   └── Documentation.tsx
│   │   │
│   │   ├── services/        # Services API
│   │   │   ├── api.ts       # Client API axios
│   │   │   ├── authService.ts
│   │   │   ├── migrationService.ts
│   │   │   ├── productService.ts
│   │   │   ├── customerService.ts
│   │   │   └── websocketService.ts
│   │   │
│   │   ├── store/           # State management (Zustand)
│   │   │   ├── authStore.ts
│   │   │   ├── migrationStore.ts
│   │   │   ├── uiStore.ts
│   │   │   └── languageStore.ts
│   │   │
│   │   ├── types/           # TypeScript types
│   │   │   ├── api.types.ts
│   │   │   ├── migration.types.ts
│   │   │   ├── product.types.ts
│   │   │   └── user.types.ts
│   │   │
│   │   ├── utils/           # Utilitaires
│   │   │   ├── formatters.ts
│   │   │   ├── validators.ts
│   │   │   ├── helpers.ts
│   │   │   └── constants.ts
│   │   │
│   │   ├── locales/         # Internationalisation
│   │   │   ├── fr.json      # Traductions françaises
│   │   │   └── en.json      # Traductions anglaises
│   │   │
│   │   ├── App.tsx          # Composant principal
│   │   ├── main.tsx         # Point d'entrée
│   │   └── vite-env.d.ts
│   │
│   ├── package.json         # Dépendances Node.js
│   ├── tsconfig.json        # Configuration TypeScript
│   ├── vite.config.ts       # Configuration Vite
│   ├── tailwind.config.js   # Configuration Tailwind
│   ├── postcss.config.js    # Configuration PostCSS
│   ├── Dockerfile           # Configuration Docker
│   ├── nginx.conf           # Configuration Nginx
│   └── .env.example         # Exemple de configuration
│
├── config/                  # Configuration globale
│   ├── .env.example        # Template de configuration
│   ├── field_mappings.json # Mappings de champs personnalisés
│   └── currencies.json     # Configuration multi-devises
│
├── docs/                    # Documentation
│   ├── README_FR.md        # Documentation française
│   ├── QUICKSTART.md       # Guide de démarrage rapide
│   ├── API.md              # Documentation API
│   ├── ARCHITECTURE.md     # Architecture technique
│   ├── CONTRIBUTING.md     # Guide de contribution
│   │
│   ├── guides/             # Guides utilisateur
│   │   ├── installation.md
│   │   ├── first-migration.md
│   │   ├── advanced-usage.md
│   │   ├── performance.md
│   │   └── troubleshooting.md
│   │
│   ├── tutorials/          # Tutoriels
│   │   ├── shopify-to-woocommerce.md
│   │   ├── woocommerce-to-shopify.md
│   │   ├── batch-migration.md
│   │   └── webhook-setup.md
│   │
│   ├── deploy/             # Guides de déploiement
│   │   ├── aws.md
│   │   ├── gcp.md
│   │   ├── azure.md
│   │   └── docker.md
│   │
│   └── examples/           # Exemples de code
│       ├── custom-mapping.py
│       ├── webhook-handler.py
│       └── batch-script.py
│
├── scripts/                # Scripts d'automatisation
│   ├── setup.sh           # Installation automatique
│   ├── start.sh           # Démarrage de l'application
│   ├── stop.sh            # Arrêt de l'application
│   ├── start_backend.sh   # Démarrage backend seul
│   ├── start_frontend.sh  # Démarrage frontend seul
│   ├── deploy_production.sh # Déploiement production
│   ├── backup.sh          # Script de backup
│   ├── load_test.sh       # Tests de charge
│   └── run_integration_tests.sh # Tests d'intégration
│
├── nginx/                  # Configuration Nginx (production)
│   ├── nginx.conf         # Configuration principale
│   └── ssl/               # Certificats SSL
│
├── logs/                   # Fichiers de logs
│   ├── app.log
│   ├── celery.log
│   └── nginx.log
│
├── backups/                # Sauvegardes
│   └── README.md
│
├── tmp/                    # Fichiers temporaires
│   ├── images/            # Images en cours de traitement
│   └── exports/           # Exports temporaires
│
├── docker-compose.yml      # Configuration Docker Compose
├── .gitignore             # Fichiers ignorés par Git
├── .dockerignore          # Fichiers ignorés par Docker
├── LICENSE                # Licence MIT
├── README.md              # Documentation principale (EN)
├── CHANGELOG.md           # Journal des changements
└── CONTRIBUTING.md        # Guide de contribution

```

## Description des Modules Principaux

### Backend

#### API Routes (`backend/api/routes/`)
- **auth.py**: Authentification JWT, login, logout, refresh token
- **migration.py**: Démarrage, arrêt, status des migrations
- **products.py**: CRUD produits, migration produits
- **customers.py**: CRUD clients, migration clients
- **orders.py**: CRUD commandes, migration commandes
- **monitoring.py**: Statistiques, logs, métriques
- **webhooks.py**: Réception webhooks Shopify/WooCommerce
- **backup.py**: Création, restauration sauvegardes

#### Services (`backend/services/`)
- **product_migration_service.py**: Logique complète de migration des produits
- **customer_migration_service.py**: Logique de migration des clients
- **order_migration_service.py**: Logique de migration des commandes
- **shopify_service.py**: Client API Shopify avec rate limiting
- **woocommerce_service.py**: Client API WooCommerce
- **image_service.py**: Téléchargement, optimisation, upload d'images
- **backup_service.py**: Sauvegarde locale et cloud (S3, GCS)
- **seo_service.py**: Génération redirections, sitemap
- **notification_service.py**: Emails, notifications push

#### Tasks (`backend/tasks/`)
- **celery_app.py**: Configuration Celery avec Redis
- **migration_tasks.py**: Tâches asynchrones de migration
- **image_tasks.py**: Traitement d'images en arrière-plan
- **backup_tasks.py**: Sauvegardes automatiques planifiées

### Frontend

#### Pages (`frontend/src/pages/`)
- **Dashboard.tsx**: Tableau de bord principal avec statistiques
- **MigrationSetup.tsx**: Configuration et lancement de migration
- **ProductsMigration.tsx**: Interface spécifique produits
- **Monitoring.tsx**: Monitoring temps réel avec graphiques
- **Settings.tsx**: Paramètres de l'application

#### Components (`frontend/src/components/`)
- **common/**: Composants réutilisables (Button, Modal, Table, etc.)
- **dashboard/**: Composants spécifiques au dashboard
- **migration/**: Composants de configuration de migration
- **layouts/**: Layouts et navigation

#### Services (`frontend/src/services/`)
- **api.ts**: Client HTTP axios configuré
- **migrationService.ts**: Appels API de migration
- **websocketService.ts**: Communication temps réel

#### Store (`frontend/src/store/`)
- **authStore.ts**: État d'authentification (Zustand)
- **migrationStore.ts**: État des migrations en cours
- **languageStore.ts**: Gestion i18n (FR/EN)

## Flux de Données

### Migration de Produits (Exemple)

```
1. Frontend (React)
   └─> MigrationSetup.tsx
       └─> migrationService.startMigration()

2. Backend API (FastAPI)
   └─> /api/migration/start
       └─> migration.router.start_migration()

3. Service Layer
   └─> ProductMigrationService.migrate_products()
       ├─> ShopifyService.get_all_products()
       ├─> ImageService.optimize_images()
       └─> WooCommerceService.create_products()

4. Task Queue (Celery)
   └─> migration_tasks.migrate_product_batch.delay()
       └─> Traitement asynchrone par lots

5. Database (PostgreSQL)
   └─> Enregistrement progression et résultats

6. WebSocket (temps réel)
   └─> Notification frontend de la progression

7. Frontend Update
   └─> Dashboard affiche progression en temps réel
```

## Technologies Utilisées

### Backend
- **FastAPI**: Framework web asynchrone
- **SQLAlchemy**: ORM pour PostgreSQL
- **Celery**: Queue de tâches asynchrones
- **Redis**: Cache et broker Celery
- **Alembic**: Migrations de base de données
- **Pydantic**: Validation de données
- **Structlog**: Logging structuré
- **Pillow**: Traitement d'images

### Frontend
- **React 18**: Bibliothèque UI
- **TypeScript**: Typage statique
- **Vite**: Build tool rapide
- **TanStack Query**: Gestion des requêtes
- **Zustand**: State management
- **Tailwind CSS**: Framework CSS
- **Recharts**: Graphiques
- **Framer Motion**: Animations
- **Socket.io**: WebSocket client

### Infrastructure
- **PostgreSQL**: Base de données relationnelle
- **Redis**: Cache et message broker
- **Docker**: Conteneurisation
- **Nginx**: Reverse proxy
- **Prometheus**: Métriques
- **Sentry**: Error tracking

## Points d'Extension

### Ajouter une Nouvelle Plateforme

1. Créer un service dans `backend/services/`
   ```python
   class NewPlatformService:
       async def get_products(self): ...
       async def create_product(self, data): ...
   ```

2. Ajouter les routes dans `backend/api/routes/`

3. Créer les tâches Celery dans `backend/tasks/`

4. Ajouter l'interface dans le frontend

### Ajouter une Nouvelle Entité

1. Créer le modèle dans `backend/models/`
2. Créer la migration Alembic
3. Créer le service de migration
4. Ajouter les routes API
5. Créer l'interface frontend

## Bonnes Pratiques

1. **Backend**: Suivre les principes SOLID
2. **Frontend**: Composants réutilisables, props typés
3. **Tests**: Coverage minimum 80%
4. **Documentation**: Docstrings + TypeDoc
5. **Commits**: Convention Conventional Commits
6. **Code Review**: Obligatoire pour merge

## Ressources Supplémentaires

- [Guide d'Installation](docs/guides/installation.md)
- [Architecture Détaillée](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Guide de Contribution](CONTRIBUTING.md)
