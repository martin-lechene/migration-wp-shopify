# Script d'initialisation de la structure Git
# Basé sur le mini-plan de commits approuvé

Write-Host "🚀 Initialisation de la structure Git pour migration-wp-shopify" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Git est déjà initialisé
if (Test-Path ".git") {
    Write-Host "⚠️  Git est déjà initialisé dans ce projet" -ForegroundColor Yellow
    $response = Read-Host "Voulez-vous continuer quand même? (o/n)"
    if ($response -ne "o") {
        Write-Host "❌ Opération annulée" -ForegroundColor Red
        exit 1
    }
} else {
    # Initialiser le dépôt Git
    Write-Host "📦 Initialisation du dépôt Git..." -ForegroundColor Green
    git init
    git branch -M main
}

# Créer la branche develop
Write-Host "🌱 Création de la branche develop..." -ForegroundColor Green
git checkout -b develop 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Branch develop existe déjà, passage à develop" -ForegroundColor Yellow
    git checkout develop
}

# Créer toutes les feature branches
$featureBranches = @(
    "feature/infrastructure",
    "feature/data-models",
    "feature/backend-core",
    "feature/api-layer",
    "feature/frontend",
    "feature/documentation"
)

Write-Host ""
Write-Host "🌳 Création des branches de fonctionnalités..." -ForegroundColor Green
foreach ($branch in $featureBranches) {
    git checkout -b $branch develop 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Créé: $branch" -ForegroundColor Cyan
    } else {
        Write-Host "   → Existe déjà: $branch" -ForegroundColor Yellow
    }
}

# Retourner sur develop
git checkout develop

Write-Host ""
Write-Host "📊 Structure des branches créée:" -ForegroundColor Green
git branch -a

Write-Host ""
Write-Host "✅ Initialisation terminée!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Prochaines étapes:" -ForegroundColor Cyan
Write-Host "   1. Checkout feature/infrastructure: git checkout feature/infrastructure" -ForegroundColor White
Write-Host "   2. Commencer les commits selon le plan (commits 1-5)" -ForegroundColor White
Write-Host "   3. Utiliser le script commit-helper.ps1 pour faciliter les commits" -ForegroundColor White
Write-Host ""
