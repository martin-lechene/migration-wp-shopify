# 🚀 Shopify to WordPress/WooCommerce Migration Tool

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/shopify-wordpress-migrator)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.2+-blue.svg)](https://reactjs.org/)

**Enterprise-grade migration tool for seamless e-commerce platform transitions**

> 🌍 **Bilingual:** This tool supports both French (Français) and English interfaces and documentation.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Migration Capabilities

- **🔄 Bidirectional Migration**
  - Shopify → WordPress/WooCommerce
  - WordPress/WooCommerce → Shopify
  
- **📦 Complete Data Migration**
  - ✅ Products (>10,000 products supported)
  - ✅ Product variants and attributes
  - ✅ Customers and customer groups
  - ✅ Orders and order history
  - ✅ Stock levels and SKU management
  - ✅ Product images with optimization
  - ✅ Categories and collections
  - ✅ Tags and metadata
  - ✅ SEO data (meta titles, descriptions)
  - ✅ Customer reviews and ratings
  - ✅ Coupons and discounts
  - ✅ Blog posts and articles
  - ✅ Digital/downloadable products
  - ✅ Multi-currency support
  - ✅ Loyalty points and rewards

### Advanced Features

- **⚡ Performance & Scalability**
  - Asynchronous task processing with Celery
  - Batch processing for large datasets
  - Rate limiting and API throttling
  - Redis caching for optimal performance
  - Concurrent task execution
  
- **🎨 Image Optimization**
  - Automatic image compression
  - Multiple thumbnail sizes
  - Format conversion (JPEG, PNG, WebP)
  - Intelligent resizing
  
- **🔒 Security & Reliability**
  - Encrypted credential storage
  - Automatic backup before migration
  - Retry mechanism with exponential backoff
  - Detailed error logging
  - Transaction rollback on failure
  
- **📊 Monitoring & Reporting**
  - Real-time migration dashboard
  - Progress tracking with WebSockets
  - Detailed migration reports
  - Export statistics to Excel/CSV
  - Email notifications
  - Prometheus metrics
  
- **🛠️ Migration Modes**
  - **Full Migration:** Complete store transfer
  - **Incremental:** Update existing data
  - **Test Mode:** Preview without changes
  - **Batch Mode:** Process in chunks
  - **Real-time Sync:** Continuous synchronization

### SEO & Marketing

- **🔍 SEO Preservation**
  - Meta titles and descriptions
  - URL slug mapping
  - 301 redirects generation (Nginx/Apache)
  - Sitemap.xml generation
  - Canonical URLs
  
- **📱 Additional Features**
  - Webhook integration for third-party tools
  - Custom field mapping
  - Navigation menu migration
  - Multi-language support
  - Barcode and vendor references

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Migration │  │Monitoring│  │ Settings │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                  Backend API (FastAPI)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Auth    │  │Migration │  │Monitoring│  │ Webhooks │   │
│  │ Service  │  │ Service  │  │ Service  │  │ Service  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────┬──────────────┬──────────────┬─────────────────────┘
         │              │              │
    ┌────▼────┐    ┌────▼────┐    ┌───▼────┐
    │PostgreSQL│    │  Redis  │    │ Celery │
    │   DB    │    │  Cache  │    │Workers │
    └─────────┘    └─────────┘    └────────┘
         │              │              │
    ┌────▼──────────────▼──────────────▼────┐
    │          External APIs                │
    │  ┌──────────┐      ┌──────────┐      │
    │  │ Shopify  │      │WooCommerce│      │
    │  │   API    │      │    API    │      │
    │  └──────────┘      └──────────┘      │
    └───────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** and npm/yarn
- **PostgreSQL 14+**
- **Redis 7+**
- **Shopify Store** with API credentials
- **WordPress/WooCommerce** site with REST API enabled

### Installation (Quick)

```bash
# Clone the repository
git clone https://github.com/yourusername/shopify-wordpress-migrator.git
cd shopify-wordpress-migrator

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Start the application
./scripts/start.sh
```

Visit `http://localhost:3000` to access the application.

## 📦 Installation (Detailed)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../config/.env.example .env

# Edit .env with your credentials
nano .env

# Initialize database
alembic upgrade head

# Start Redis (if not running)
redis-server

# Start Celery workers
celery -A tasks.celery_app worker --loglevel=info -c 4

# In a new terminal, start Celery beat (for scheduled tasks)
celery -A tasks.celery_app beat --loglevel=info

# Start FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Copy environment file
cp .env.example .env.local

# Edit .env.local
nano .env.local

# Start development server
npm run dev
# or
yarn dev
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb migrator_db

# Run migrations
cd backend
alembic upgrade head

# (Optional) Seed with sample data
python scripts/seed_database.py
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following:

```bash
# Application
APP_NAME=Shopify-WordPress Migrator
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-secret-key-here

# Shopify Configuration
SHOPIFY_SHOP_NAME=your-store.myshopify.com
SHOPIFY_API_KEY=your-api-key
SHOPIFY_API_SECRET=your-api-secret
SHOPIFY_ACCESS_TOKEN=your-access-token

# WooCommerce Configuration
WOOCOMMERCE_URL=https://your-wordpress-site.com
WOOCOMMERCE_CONSUMER_KEY=ck_your_consumer_key
WOOCOMMERCE_CONSUMER_SECRET=cs_your_consumer_secret

# WordPress (for blog migration)
WORDPRESS_URL=https://your-wordpress-site.com
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=your-application-password

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/migrator_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Email Notifications (optional)
ENABLE_EMAIL_NOTIFICATIONS=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Obtaining API Credentials

#### Shopify

1. Log in to your Shopify admin panel
2. Go to **Apps** → **Develop apps**
3. Click **Create an app**
4. Configure the following scopes:
   - `read_products`, `write_products`
   - `read_customers`, `write_customers`
   - `read_orders`, `write_orders`
   - `read_inventory`, `write_inventory`
   - `read_content`, `write_content`
5. Install the app and copy the **Access Token**

#### WooCommerce

1. Log in to your WordPress admin
2. Go to **WooCommerce** → **Settings** → **Advanced** → **REST API**
3. Click **Add key**
4. Set permissions to **Read/Write**
5. Copy the **Consumer Key** and **Consumer Secret**

#### WordPress (for blog posts)

1. Go to **Users** → **Profile**
2. Scroll to **Application Passwords**
3. Create a new application password
4. Copy the generated password

## 🎯 Usage

### Web Interface

1. **Access the Dashboard**
   ```
   http://localhost:3000
   ```

2. **Login** with your credentials (default: admin/admin)

3. **Configure Connection**
   - Navigate to **Settings**
   - Enter your Shopify and WooCommerce credentials
   - Test the connection

4. **Start Migration**
   - Go to **Migration** → **Setup**
   - Select migration direction
   - Choose what to migrate
   - Select migration mode
   - Click **Start Migration**

5. **Monitor Progress**
   - View real-time progress in the dashboard
   - Check detailed logs in **Monitoring**
   - Download reports when complete

### Python Script (CLI)

```bash
cd backend

# Full migration (Shopify → WooCommerce)
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode full \
  --entities products,customers,orders

# Test migration (preview only)
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode test \
  --entities products

# Batch migration
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode batch \
  --batch-size 100 \
  --entities products

# Migrate specific products
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --product-ids 123456,789012 \
  --entities products

# With backup
python scripts/migrate.py \
  --direction shopify_to_woocommerce \
  --mode full \
  --entities products,customers \
  --backup
```

### CLI Options

```
Options:
  --direction       Migration direction (shopify_to_woocommerce | woocommerce_to_shopify)
  --mode           Migration mode (full | incremental | test | batch)
  --entities       Comma-separated list of entities (products, customers, orders, etc.)
  --batch-size     Number of items per batch (default: 50)
  --product-ids    Comma-separated list of product IDs
  --backup         Create backup before migration
  --optimize-images Optimize images during migration
  --generate-redirects Generate 301 redirects
  --dry-run        Preview changes without executing
  --verbose        Enable verbose logging
  --config         Path to custom config file
```

## 📚 API Documentation

### Authentication

All API requests require a JWT token:

```bash
# Get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Use token
curl -X GET http://localhost:8000/api/products \
  -H "Authorization: Bearer <your-token>"
```

### Key Endpoints

```http
# Migration
POST   /api/migration/start          # Start a new migration
GET    /api/migration/jobs           # List all jobs
GET    /api/migration/jobs/{id}      # Get job details
POST   /api/migration/jobs/{id}/cancel  # Cancel a job

# Products
GET    /api/products                 # List products
POST   /api/products/migrate         # Migrate products
GET    /api/products/{id}            # Get product details

# Monitoring
GET    /api/monitoring/stats         # Get statistics
GET    /api/monitoring/jobs/{id}/progress  # Get job progress
GET    /api/monitoring/logs          # Get migration logs

# Webhooks
POST   /api/webhooks/shopify         # Shopify webhook endpoint
POST   /api/webhooks/woocommerce     # WooCommerce webhook endpoint
```

Full API documentation available at: `http://localhost:8000/api/docs`

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Failed

**Problem:** Cannot connect to Shopify/WooCommerce API

**Solution:**
- Verify API credentials in `.env`
- Check API permissions/scopes
- Ensure store URL is correct
- Test connection: `python scripts/test_connection.py`

#### 2. Migration Stalled

**Problem:** Migration stops at certain percentage

**Solution:**
- Check Celery workers are running
- Review logs: `tail -f /var/log/migrator/app.log`
- Increase worker concurrency
- Check rate limits

#### 3. Images Not Migrating

**Problem:** Product images are missing

**Solution:**
- Verify image URLs are accessible
- Check disk space in `IMAGE_STORAGE_PATH`
- Enable debug logging
- Try manual image upload

#### 4. Database Errors

**Problem:** PostgreSQL connection errors

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Reset database
dropdb migrator_db
createdb migrator_db
alembic upgrade head
```

#### 5. Rate Limit Errors

**Problem:** Too many API requests

**Solution:**
- Reduce `BATCH_SIZE` in config
- Increase `RATE_LIMIT_WINDOW`
- Use incremental mode
- Schedule migration during off-peak hours

### Debug Mode

Enable detailed logging:

```bash
# In .env
DEBUG=true
LOG_LEVEL=DEBUG

# Run with verbose output
python scripts/migrate.py --verbose
```

### Support

- 📖 Check [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/shopify-wordpress-migrator/issues)
- 💬 [Community Forum](https://community.example.com)
- 📧 Email: support@example.com

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
./scripts/run_integration_tests.sh

# Load testing
./scripts/load_test.sh
```

## 🚀 Deployment

### Production Deployment

```bash
# Build frontend
cd frontend
npm run build

# Deploy to production
./scripts/deploy_production.sh
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Cloud Deployment

- **AWS:** See [docs/deploy/aws.md](docs/deploy/aws.md)
- **Google Cloud:** See [docs/deploy/gcp.md](docs/deploy/gcp.md)
- **Azure:** See [docs/deploy/azure.md](docs/deploy/azure.md)

## 📊 Performance

Typical migration speeds (tested on AWS t3.large):

- **Products:** ~500-1000 per hour
- **Customers:** ~2000-3000 per hour
- **Orders:** ~1000-1500 per hour

For stores with >10,000 products, we recommend:
- Using batch mode
- Running during off-peak hours
- Increasing Celery workers
- Enabling Redis caching

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- Shopify API Documentation
- WooCommerce REST API
- FastAPI Framework
- React Community

---

**Made with ❤️ for the e-commerce community**

*For detailed documentation in French, see [README_FR.md](README_FR.md)*
