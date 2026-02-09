# Helper script pour faciliter les commits atomiques
# Reference le mini-plan de commits

param(
    [Parameter(Mandatory = $false)]
    [string]$CommitNumber,
    
    [Parameter(Mandatory = $false)]
    [switch]$List,
    
    [Parameter(Mandatory = $false)]
    [switch]$Status
)

# Table de correspondance commits -> branches
$commitMap = @{
    # feature/infrastructure (1-5)
    "1"  = @{
        Branch      = "feature/infrastructure"
        Message     = "feat: initialize project structure with backend and frontend directories"
        Description = "Create root directory structure, add .gitignore, add README.md placeholder"
    }
    "2"  = @{
        Branch      = "feature/infrastructure"
        Message     = "feat(backend): add Dockerfile and requirements.txt"
        Description = "Create backend/Dockerfile for Python 3.11+, add requirements.txt with dependencies"
    }
    "3"  = @{
        Branch      = "feature/infrastructure"
        Message     = "feat(frontend): initialize React TypeScript project with Vite"
        Description = "Add package.json, vite.config.ts, tsconfig.json, tailwind.config.js, Dockerfile"
    }
    "4"  = @{
        Branch      = "feature/infrastructure"
        Message     = "feat: add Docker Compose for multi-service architecture"
        Description = "Create docker-compose.yml with PostgreSQL, Redis, Backend, Frontend, Celery"
    }
    "5"  = @{
        Branch      = "feature/infrastructure"
        Message     = "feat: add environment configuration templates"
        Description = "Create backend/.env.example and frontend/.env.example with documentation"
    }
    
    # feature/data-models (6-13)
    "6"  = @{
        Branch      = "feature/data-models"
        Message     = "feat(backend): add database core configuration"
        Description = "Create backend/core/database.py with SQLAlchemy engine and session management"
    }
    "7"  = @{
        Branch      = "feature/data-models"
        Message     = "feat(models): add User model with authentication fields"
        Description = "Create backend/models/user.py with password hashing utilities"
    }
    "8"  = @{
        Branch      = "feature/data-models"
        Message     = "feat(models): add Migration model for job tracking"
        Description = "Create backend/models/migration.py with status tracking"
    }
    "9"  = @{
        Branch      = "feature/data-models"
        Message     = "feat(models): add Product model for e-commerce data"
        Description = "Create backend/models/product.py supporting Shopify and WooCommerce"
    }
    "10" = @{
        Branch      = "feature/data-models"
        Message     = "feat(models): add Customer model"
        Description = "Create backend/models/customer.py with JSON fields for platform data"
    }
    "11" = @{
        Branch      = "feature/data-models"
        Message     = "feat(models): add Order model"
        Description = "Create backend/models/order.py with multi-currency support"
    }
    "12" = @{
        Branch      = "feature/data-models"
        Message     = "feat(models): add Log model for migration tracking"
        Description = "Create backend/models/log.py for detailed audit trail"
    }
    "13" = @{
        Branch      = "feature/data-models"
        Message     = "feat(models): add __init__.py to export all models"
        Description = "Create backend/models/__init__.py"
    }
    
    # feature/backend-core (14-24)
    "14" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(core): add settings and configuration management"
        Description = "Create backend/config/settings.py with Pydantic validation"
    }
    "15" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(core): add security utilities for JWT and password hashing"
        Description = "Create backend/core/security.py with JWT and bcrypt"
    }
    "16" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(core): add custom exception handlers"
        Description = "Create backend/core/exceptions.py with FastAPI handlers"
    }
    "17" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(core): add structured logging configuration"
        Description = "Create backend/core/logging.py with JSON logging"
    }
    "18" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(core): add FastAPI dependencies"
        Description = "Create backend/core/dependencies.py for DI"
    }
    "19" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(core): add core module initialization"
        Description = "Create backend/core/__init__.py"
    }
    "20" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(services): add Shopify API service"
        Description = "Create backend/services/shopify_service.py with rate limiting"
    }
    "21" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(services): add WooCommerce API service"
        Description = "Create backend/services/woocommerce_service.py"
    }
    "22" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(services): add image optimization service"
        Description = "Create backend/services/image_service.py with Pillow"
    }
    "23" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(services): add product migration orchestration service"
        Description = "Create backend/services/product_migration_service.py"
    }
    "24" = @{
        Branch      = "feature/backend-core"
        Message     = "feat(services): add services module initialization"
        Description = "Create backend/services/__init__.py"
    }
    
    # feature/api-layer (25-33)
    "25" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add API module structure"
        Description = "Create backend/api/__init__.py and routes/__init__.py"
    }
    "26" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add authentication endpoints"
        Description = "Create backend/api/routes/auth.py with JWT management"
    }
    "27" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add migration job endpoints"
        Description = "Create backend/api/routes/migration.py"
    }
    "28" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add product management endpoints"
        Description = "Create backend/api/routes/products.py"
    }
    "29" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add customer management endpoints"
        Description = "Create backend/api/routes/customers.py"
    }
    "30" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add order management endpoints"
        Description = "Create backend/api/routes/orders.py"
    }
    "31" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add monitoring and statistics endpoints"
        Description = "Create backend/api/routes/monitoring.py"
    }
    "32" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add backup management endpoints"
        Description = "Create backend/api/routes/backup.py"
    }
    "33" = @{
        Branch      = "feature/api-layer"
        Message     = "feat(api): add webhook handlers"
        Description = "Create backend/api/routes/webhooks.py"
    }
    
    # feature/frontend (34-38)
    "34" = @{
        Branch      = "feature/frontend"
        Message     = "feat(frontend): add source directory structure"
        Description = "Create frontend/src with components, pages, services, types, utils, hooks"
    }
    "35" = @{
        Branch      = "feature/frontend"
        Message     = "feat(frontend): add main App.tsx component"
        Description = "Create App.tsx with routing and theme provider"
    }
    "36" = @{
        Branch      = "feature/frontend"
        Message     = "feat(frontend): add index.html entry point"
        Description = "Create frontend/index.html with SEO meta tags"
    }
    "37" = @{
        Branch      = "feature/frontend"
        Message     = "feat(frontend): add main TypeScript entry point"
        Description = "Create frontend/src/main.tsx"
    }
    "38" = @{
        Branch      = "feature/frontend"
        Message     = "feat(frontend): add TypeScript types and utility functions"
        Description = "Create types and API client utilities"
    }
    
    # feature/documentation (39-44)
    "39" = @{
        Branch      = "feature/documentation"
        Message     = "docs: add comprehensive README.md"
        Description = "Complete README with features, installation, configuration, usage"
    }
    "40" = @{
        Branch      = "feature/documentation"
        Message     = "docs: add French README (README_FR.md)"
        Description = "Translate all content to French"
    }
    "41" = @{
        Branch      = "feature/documentation"
        Message     = "docs: add PROJECT_STRUCTURE.md"
        Description = "Document directory organization and architecture"
    }
    "42" = @{
        Branch      = "feature/documentation"
        Message     = "docs: add GETTING_STARTED.md"
        Description = "Step-by-step setup guide with prerequisites"
    }
    "43" = @{
        Branch      = "feature/documentation"
        Message     = "docs: add QUICKSTART.md"
        Description = "Fast installation and CLI quick reference"
    }
    "44" = @{
        Branch      = "feature/documentation"
        Message     = "docs: add EXAMPLES.md"
        Description = "Code examples and integration patterns"
    }
}

# Fonction pour lister tous les commits
function Show-CommitList {
    Write-Host ""
    Write-Host "[*] Liste des commits disponibles (44 au total)" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Gray
    
    $currentBranch = ""
    foreach ($key in 1..44) {
        $commit = $commitMap["$key"]
        if ($commit.Branch -ne $currentBranch) {
            $currentBranch = $commit.Branch
            Write-Host ""
            Write-Host "[BRANCH] $currentBranch" -ForegroundColor Yellow
            Write-Host ("-" * 80) -ForegroundColor Gray
        }
        Write-Host "  [$key] " -NoNewline -ForegroundColor Green
        Write-Host "$($commit.Message)" -ForegroundColor White
        Write-Host "      -> $($commit.Description)" -ForegroundColor DarkGray
    }
    Write-Host ""
}

# Fonction pour afficher le statut
function Show-Status {
    Write-Host ""
    Write-Host "[*] Statut Git actuel" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Gray
    
    $currentBranch = git branch --show-current
    Write-Host "Branche actuelle: " -NoNewline
    Write-Host "$currentBranch" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Fichiers modifies:" -ForegroundColor Yellow
    git status --short
    
    Write-Host ""
    Write-Host "Derniers commits:" -ForegroundColor Yellow
    git log --oneline -n 5 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  (Aucun commit encore)" -ForegroundColor DarkGray
    }
    Write-Host ""
}

# Fonction pour créer un commit
function New-AtomicCommit {
    param([string]$Number)
    
    if (-not $commitMap.ContainsKey($Number)) {
        Write-Host "[ERROR] Numero de commit invalide: $Number" -ForegroundColor Red
        Write-Host "   Utilisez -List pour voir tous les commits disponibles" -ForegroundColor Yellow
        exit 1
    }
    
    $commit = $commitMap[$Number]
    $currentBranch = git branch --show-current
    
    Write-Host ""
    Write-Host "[*] Preparation du commit #$Number" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Gray
    Write-Host "Branche attendue: " -NoNewline
    Write-Host "$($commit.Branch)" -ForegroundColor Green
    Write-Host "Branche actuelle: " -NoNewline
    
    if ($currentBranch -eq $commit.Branch) {
        Write-Host "$currentBranch" -ForegroundColor Green
    }
    else {
        Write-Host "$currentBranch" -ForegroundColor Red
        Write-Host ""
        Write-Host "[WARNING] Vous n'etes pas sur la bonne branche!" -ForegroundColor Yellow
        $response = Read-Host "Voulez-vous changer vers $($commit.Branch)? (o/n)"
        if ($response -eq "o") {
            git checkout $commit.Branch
        }
        else {
            Write-Host "[CANCELLED] Operation annulee" -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host ""
    Write-Host "Message: " -NoNewline
    Write-Host "$($commit.Message)" -ForegroundColor Cyan
    Write-Host "Description: $($commit.Description)" -ForegroundColor Gray
    Write-Host ""
    
    # Afficher les fichiers à ajouter
    Write-Host "Fichiers modifies/ajoutes:" -ForegroundColor Yellow
    git status --short
    
    Write-Host ""
    Write-Host "[INFO] Conseils:" -ForegroundColor Cyan
    Write-Host "   1. Verifiez que les fichiers correspondent a ce commit" -ForegroundColor White
    Write-Host "   2. Utilisez: git add <fichiers>" -ForegroundColor White
    Write-Host "   3. Puis executez a nouveau ce script pour valider le commit" -ForegroundColor White
    Write-Host ""
    
    $response = Read-Host "Voulez-vous creer le commit maintenant? (o/n)"
    if ($response -eq "o") {
        git add .
        git commit -m "$($commit.Message)"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "[SUCCESS] Commit #$Number cree avec succes!" -ForegroundColor Green
            Write-Host ""
        }
        else {
            Write-Host ""
            Write-Host "[ERROR] Erreur lors de la creation du commit" -ForegroundColor Red
            Write-Host ""
        }
    }
    else {
        Write-Host "[CANCELLED] Commit annule" -ForegroundColor Red
    }
}

# Main
if ($List) {
    Show-CommitList
}
elseif ($Status) {
    Show-Status
}
elseif ($CommitNumber) {
    New-AtomicCommit -Number $CommitNumber
}
else {
    Write-Host ""
    Write-Host "[*] Helper de commits atomiques - Migration WP-Shopify" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Gray
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\commit-helper.ps1 -List          " -NoNewline -ForegroundColor White
    Write-Host "# Lister tous les commits disponibles" -ForegroundColor DarkGray
    Write-Host "  .\commit-helper.ps1 -Status        " -NoNewline -ForegroundColor White
    Write-Host "# Afficher le statut Git" -ForegroundColor DarkGray
    Write-Host "  .\commit-helper.ps1 -CommitNumber 1" -NoNewline -ForegroundColor White
    Write-Host "# Creer le commit #1" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "Exemples:" -ForegroundColor Yellow
    Write-Host "  .\commit-helper.ps1 -List" -ForegroundColor Cyan
    Write-Host "  .\commit-helper.ps1 1" -ForegroundColor Cyan
    Write-Host ""
}
