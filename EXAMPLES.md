# 📚 Exemples Pratiques et Cas d'Usage

Ce guide présente des exemples concrets d'utilisation de l'outil de migration.

## Table des Matières

1. [Scénarios de Migration](#scénarios-de-migration)
2. [Exemples CLI](#exemples-cli)
3. [Exemples d'API](#exemples-dapi)
4. [Scripts Personnalisés](#scripts-personnalisés)
5. [Cas d'Usage Avancés](#cas-dusage-avancés)

---

## Scénarios de Migration

### Scénario 1 : Petite Boutique (< 500 produits)

**Contexte**: Migration complète d'une boutique Shopify avec 300 produits vers WooCommerce.

#### Via Interface Web

1. Accédez au tableau de bord
2. Cliquez sur "Nouvelle Migration"
3. Configuration :
   - Direction: Shopify → WooCommerce
   - Mode: Full (complet)
   - Entités: Products, Customers, Orders
   - Options: Optimiser images, Générer redirections

#### Via CLI

```bash
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode full \
  --entities products,customers,orders \
  --optimize-images \
  --generate-redirects \
  --backup
```

**Temps estimé**: 30-45 minutes  
**Résultat**: Migration complète avec backups et redirections

---

### Scénario 2 : Grande Boutique (> 10,000 produits)

**Contexte**: Boutique avec 15,000 produits. Migration progressive pour minimiser les risques.

#### Approche Recommandée: Migration par Lots

```bash
# Étape 1: Test avec 100 produits
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode test \
  --entities products \
  --batch-size 100 \
  --dry-run

# Étape 2: Migration par catégories
# Migrer les 5000 premiers produits
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode batch \
  --entities products \
  --batch-size 500 \
  --product-ids $(seq -s, 1 5000)

# Étape 3: Continuer avec le reste
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode batch \
  --entities products \
  --batch-size 500 \
  --optimize-images

# Étape 4: Clients et commandes
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode full \
  --entities customers,orders
```

**Temps estimé**: 6-8 heures (réparties sur plusieurs jours)

---

### Scénario 3 : Migration Inverse (WooCommerce → Shopify)

**Contexte**: Passage de WordPress/WooCommerce vers Shopify pour meilleure scalabilité.

```bash
# Migration complète
python scripts/migrate.py \
  --direction woocommerce_to_shopify \
  --mode full \
  --entities products,customers,orders,categories \
  --backup \
  --verbose
```

---

### Scénario 4 : Synchronisation Continue

**Contexte**: Garder deux boutiques synchronisées pendant une période de transition.

#### Configuration

```python
# config/sync_config.json
{
  "enabled": true,
  "direction": "shopify_to_woocommerce",
  "sync_interval": 3600,  # 1 heure
  "entities": ["products", "inventory"],
  "webhooks": true
}
```

#### Activation

```bash
# Démarrer la synchronisation
python scripts/start_sync.py \
  --config config/sync_config.json

# Vérifier le statut
python scripts/sync_status.py
```

---

## Exemples CLI

### Migration Basique

```bash
# Migration test (pas de modifications)
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode test \
  --entities products

# Migration complète
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode full \
  --entities products,customers,orders \
  --backup
```

### Migration Sélective

```bash
# Migrer uniquement certains produits
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --entities products \
  --product-ids 123456,234567,345678

# Migrer une catégorie spécifique
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --entities products \
  --category "Electronics"
```

### Options Avancées

```bash
# Migration avec tous les extras
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode full \
  --entities products,customers,orders,blog \
  --batch-size 100 \
  --backup \
  --optimize-images \
  --generate-redirects \
  --verbose \
  --config custom_config.env
```

### Gestion des Jobs

```bash
# Lister les migrations récentes
python scripts/migrate.py list-jobs --limit 20

# Voir le statut d'une migration
python scripts/migrate.py status abc123def

# Annuler une migration en cours
python scripts/migrate.py cancel abc123def
```

### Sauvegardes

```bash
# Créer un backup avant migration
python scripts/migrate.py backup \
  --source shopify \
  --entities products,customers,orders \
  --output /backups/shopify-backup-2024-01-15.zip

# Restaurer depuis un backup
python scripts/migrate.py restore \
  --backup /backups/shopify-backup-2024-01-15.zip \
  --destination woocommerce
```

---

## Exemples d'API

### Authentification

```bash
# Obtenir un token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password"
  }'

# Réponse
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Démarrer une Migration

```bash
curl -X POST http://localhost:8000/api/migration/start \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "direction": "shopify_to_woocommerce",
    "mode": "full",
    "entities": ["products", "customers"],
    "config": {
      "batch_size": 50,
      "optimize_images": true,
      "generate_redirects": true
    }
  }'

# Réponse
{
  "job_id": "abc123def456",
  "status": "queued",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Vérifier la Progression

```bash
curl -X GET http://localhost:8000/api/migration/jobs/abc123def456 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Réponse
{
  "id": "abc123def456",
  "status": "in_progress",
  "progress": 45,
  "entities": {
    "products": {
      "total": 1000,
      "migrated": 450,
      "failed": 5
    }
  },
  "started_at": "2024-01-15T10:30:00Z",
  "estimated_completion": "2024-01-15T12:00:00Z"
}
```

### WebSocket (Temps Réel)

```javascript
// JavaScript/TypeScript
import io from 'socket.io-client';

const socket = io('http://localhost:8000');

socket.on('connect', () => {
  console.log('Connected to migration server');
  
  // Subscribe to job updates
  socket.emit('subscribe_job', { job_id: 'abc123def456' });
});

socket.on('migration_progress', (data) => {
  console.log(`Progress: ${data.progress}%`);
  console.log(`Migrated: ${data.migrated}/${data.total}`);
});

socket.on('migration_complete', (data) => {
  console.log('Migration completed!', data);
});

socket.on('migration_error', (error) => {
  console.error('Migration error:', error);
});
```

---

## Scripts Personnalisés

### Script 1: Migration avec Mapping Personnalisé

```python
# scripts/custom_migration.py
import asyncio
from services.product_migration_service import ProductMigrationService
from core.database import SessionLocal

async def migrate_with_custom_mapping():
    """Migration avec mapping de champs personnalisés"""
    
    db = SessionLocal()
    service = ProductMigrationService(db)
    
    # Mapping personnalisé
    field_mapping = {
        'shopify_vendor': 'woocommerce_brand',
        'shopify_type': 'woocommerce_product_type',
        'custom_field_1': 'woocommerce_meta_key_1'
    }
    
    # Charger la configuration
    service.load_field_mapping(field_mapping)
    
    # Démarrer la migration
    result = await service.migrate_products(
        job_id='custom-job-001',
        direction='shopify_to_woocommerce',
        mode='full'
    )
    
    print(f"Migration completed: {result}")
    db.close()

if __name__ == '__main__':
    asyncio.run(migrate_with_custom_mapping())
```

### Script 2: Migration Progressive avec Pause

```python
# scripts/progressive_migration.py
import time
import asyncio
from services.product_migration_service import ProductMigrationService
from core.database import SessionLocal

async def progressive_migration(batch_size=100, pause_between_batches=300):
    """
    Migration progressive avec pauses entre les lots
    
    Args:
        batch_size: Taille des lots
        pause_between_batches: Pause en secondes entre les lots
    """
    
    db = SessionLocal()
    service = ProductMigrationService(db)
    
    # Récupérer le nombre total de produits
    total_products = await service.shopify.get_product_count()
    num_batches = (total_products // batch_size) + 1
    
    print(f"Total products: {total_products}")
    print(f"Number of batches: {num_batches}")
    print(f"Pause between batches: {pause_between_batches}s")
    
    for batch_num in range(num_batches):
        print(f"\n--- Batch {batch_num + 1}/{num_batches} ---")
        
        # Calculer les IDs pour ce lot
        start_id = batch_num * batch_size
        end_id = start_id + batch_size
        
        # Migrer ce lot
        result = await service.migrate_products(
            job_id=f'progressive-{batch_num}',
            direction='shopify_to_woocommerce',
            mode='batch',
            batch_size=batch_size
        )
        
        print(f"Batch completed: {result['migrated']} products migrated")
        
        # Pause avant le prochain lot
        if batch_num < num_batches - 1:
            print(f"Pausing for {pause_between_batches}s...")
            time.sleep(pause_between_batches)
    
    print("\n=== Migration Complete ===")
    db.close()

if __name__ == '__main__':
    asyncio.run(progressive_migration(
        batch_size=100,
        pause_between_batches=300  # 5 minutes
    ))
```

### Script 3: Validation Post-Migration

```python
# scripts/validate_migration.py
import asyncio
from services.shopify_service import ShopifyService
from services.woocommerce_service import WooCommerceService

async def validate_migration():
    """Valider que tous les produits ont été migrés correctement"""
    
    shopify = ShopifyService()
    woocommerce = WooCommerceService()
    
    # Récupérer tous les produits Shopify
    shopify_products = await shopify.get_all_products()
    
    print(f"Validating {len(shopify_products)} products...")
    
    missing = []
    mismatched = []
    
    for sp_product in shopify_products:
        # Chercher le produit correspondant dans WooCommerce
        sku = sp_product.get('variants', [{}])[0].get('sku')
        
        if not sku:
            continue
        
        wc_product = await woocommerce.get_product_by_sku(sku)
        
        if not wc_product:
            missing.append(sp_product)
            continue
        
        # Vérifier la correspondance
        if sp_product['title'] != wc_product['name']:
            mismatched.append({
                'shopify': sp_product,
                'woocommerce': wc_product
            })
    
    # Rapport
    print("\n=== Validation Report ===")
    print(f"Total Shopify products: {len(shopify_products)}")
    print(f"Missing in WooCommerce: {len(missing)}")
    print(f"Mismatched: {len(mismatched)}")
    
    if missing:
        print("\nMissing products:")
        for product in missing[:10]:  # Afficher les 10 premiers
            print(f"  - {product['title']} (ID: {product['id']})")
    
    if mismatched:
        print("\nMismatched products:")
        for pair in mismatched[:10]:
            print(f"  - Shopify: {pair['shopify']['title']}")
            print(f"    WooCommerce: {pair['woocommerce']['name']}")
    
    return {
        'total': len(shopify_products),
        'missing': len(missing),
        'mismatched': len(mismatched),
        'success_rate': ((len(shopify_products) - len(missing)) / len(shopify_products)) * 100
    }

if __name__ == '__main__':
    result = asyncio.run(validate_migration())
    print(f"\nSuccess Rate: {result['success_rate']:.2f}%")
```

---

## Cas d'Usage Avancés

### Cas 1: Migration Multi-Boutiques

Migrer plusieurs boutiques Shopify vers plusieurs sites WooCommerce.

```python
# scripts/multi_store_migration.py
stores_config = [
    {
        'name': 'US Store',
        'shopify_shop': 'us-store.myshopify.com',
        'woocommerce_url': 'https://us.example.com'
    },
    {
        'name': 'EU Store',
        'shopify_shop': 'eu-store.myshopify.com',
        'woocommerce_url': 'https://eu.example.com'
    }
]

for store in stores_config:
    print(f"Migrating {store['name']}...")
    # Configuration pour chaque boutique
    # Migration...
```

### Cas 2: Migration avec Transformation de Données

Transformer les données pendant la migration (ex: conversion de devises).

```python
# scripts/transform_migration.py
async def transform_prices(product):
    """Convertir les prix de USD à EUR"""
    exchange_rate = 0.92  # USD to EUR
    
    if product.get('price'):
        product['price'] = float(product['price']) * exchange_rate
    
    return product

# Utiliser dans la migration
service.register_transformer('product', transform_prices)
```

### Cas 3: Migration avec Webhooks

Déclencher des actions personnalisées pendant la migration.

```python
# scripts/webhook_migration.py
def on_product_migrated(product_data):
    """Callback appelé après chaque produit migré"""
    # Envoyer notification
    send_slack_notification(f"Product migrated: {product_data['name']}")
    
    # Mettre à jour un système externe
    update_erp_system(product_data)

service.on('product_migrated', on_product_migrated)
```

---

## Bonnes Pratiques

### Avant la Migration

1. **Backup complet** de vos deux plateformes
2. **Test en mode preview** avec quelques produits
3. **Vérifier les limites API** de vos plateformes
4. **Planifier en heures creuses** pour les grandes migrations

### Pendant la Migration

1. **Surveiller les logs** en temps réel
2. **Vérifier la progression** régulièrement
3. **Préparer un plan B** en cas d'erreur majeure
4. **Ne pas interrompre brutalement** (utiliser cancel si nécessaire)

### Après la Migration

1. **Valider les données** avec le script de validation
2. **Tester les fonctionnalités** sur le nouveau site
3. **Activer les redirections 301**
4. **Surveiller les erreurs** les premiers jours
5. **Garder les backups** pendant au moins 30 jours

---

## Support et Ressources

- 📖 [Documentation complète](../README_FR.md)
- 🎥 [Vidéos tutorielles](https://youtube.com/example)
- 💬 [Forum communautaire](https://community.example.com)
- 📧 Email: support@example.com

---

**Besoin d'aide personnalisée ?** Contactez notre équipe de support ! 🚀
