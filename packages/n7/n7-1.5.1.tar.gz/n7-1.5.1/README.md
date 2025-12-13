# N7 CLI

CLI global pour gérer les projets N7 avec Docker Compose et les tests pytest.

## Table des matières

- [Installation](#installation)
- [Mise à jour](#mise-à-jour)
- [Commandes disponibles](#commandes-disponibles)
  - [Commandes globales](#commandes-globales)
  - [Commandes Docker Compose](#commandes-docker-compose)
  - [Commandes de tests](#commandes-de-tests)
- [Développement](#développement)

---

## Installation

### Installation depuis PyPI (Production)

#### Avec pip

```bash
pip install n7
```

#### Avec pipx (recommandé pour les CLI)

[pipx](https://pipx.pypa.io/) installe les outils CLI dans des environnements virtuels isolés, évitant les conflits de dépendances.

```bash
# Installation de pipx si nécessaire
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Installation de n7
pipx install n7
```

### Installation depuis PyPI Test

Si vous voulez tester la dernière version en développement :

```bash
pipx install --index-url https://test.pypi.org/simple/ --pip-args="--extra-index-url https://pypi.org/simple/" n7
```

---

## Mise à jour

### Avec pip

```bash
pip install --upgrade n7
```

### Avec pipx

```bash
pipx upgrade n7
```

Pour forcer la réinstallation :

```bash
pipx reinstall n7
```

---

## Commandes disponibles

### Commandes globales

#### Afficher la version

```bash
n7 --version
n7 -v
```

#### Mode debug

Active le mode debug avec traceback complet :

```bash
n7 --debug [commande]
```

#### Aide

```bash
n7 --help
n7 -h
```

---

### Commandes Docker Compose

Toutes les commandes Docker Compose sont préfixées par `n7 dkc`.

#### `n7 dkc up` - Démarrer les containers

Démarre les containers Docker Compose.

```bash
# Démarrage standard (en mode détaché)
n7 dkc up

# Démarrage sans mode détaché (voir les logs en direct)
n7 dkc up --no-detach

# Démarrage avec rebuild des images
n7 dkc up --build
n7 dkc up -b

# Combinaison
n7 dkc up --build --no-detach
```

**Options :**
- `--no-detach` : Ne pas démarrer en mode détaché (affiche les logs)
- `-b, --build` : Reconstruire les images avant de démarrer

---

#### `n7 dkc down` - Arrêter les containers

Arrête et supprime les containers Docker Compose.

```bash
# Arrêt standard
n7 dkc down

# Arrêt avec suppression des volumes
n7 dkc down --volumes
n7 dkc down -v
```

**Options :**
- `-v, --volumes` : Supprime également tous les volumes associés

---

#### `n7 dkc l` - Afficher les logs

Affiche les logs des containers.

```bash
# Logs de tous les services
n7 dkc l

# Logs d'un service spécifique
n7 dkc l api
n7 dkc l db

# Suivre les logs en temps réel
n7 dkc l --follow
n7 dkc l -f

# Logs d'un service en mode suivi
n7 dkc l api -f
```

**Arguments :**
- `service` : Nom du service (optionnel, tous les services si non spécifié)

**Options :**
- `-f, --follow` : Suivre les logs en temps réel

---

#### `n7 dkc sh` - Ouvrir un shell dans un container

Ouvre un shell interactif dans un container.

```bash
# Shell bash dans le service par défaut
n7 dkc sh

# Shell dans un service spécifique
n7 dkc sh --service api
n7 dkc sh -s db

# Utiliser sh au lieu de bash
n7 dkc sh --no-bash
```

**Options :**
- `-s, --service` : Service Docker cible (défaut : service configuré ou 'api')
- `--no-bash` : Utiliser `sh` au lieu de `bash`

---

#### `n7 dkc mana` - Exécuter manage.py (Django)

Exécute des commandes Django manage.py dans un container.

```bash
# Exemples de commandes Django
n7 dkc mana migrate
n7 dkc mana makemigrations
n7 dkc mana createsuperuser
n7 dkc mana shell
n7 dkc mana collectstatic --noinput

# Sur un service spécifique
n7 dkc mana migrate --service api
n7 dkc mana -s api migrate
```

**Arguments :**
- `args...` : Arguments à passer à manage.py

**Options :**
- `-s, --service` : Service Docker cible (défaut : service configuré ou 'api')

---

#### `n7 dkc t` - Tests pytest dans un container

Exécute les tests pytest dans un container Docker.

```bash
# Tous les tests
n7 dkc t

# Tests d'un fichier ou répertoire spécifique
n7 dkc t tests/test_api.py
n7 dkc t tests/unit/

# Mode verbose
n7 dkc t -v

# Arrêt au premier échec
n7 dkc t -x

# Exécution parallèle
n7 dkc t -n auto
n7 dkc t -n 4

# Avec couverture de code
n7 dkc t --cov=myapp
n7 dkc t --cov=myapp --cov-report=html
n7 dkc t --cov=myapp --cov-report=term-missing

# Rejouer uniquement les tests échoués
n7 dkc t --lf

# Exécuter les tests échoués en premier
n7 dkc t --ff

# Options Django
n7 dkc t --create-db
n7 dkc t --migrations

# Service spécifique
n7 dkc t --service api
n7 dkc t -s api

# Combinaisons
n7 dkc t tests/ -v -x -n auto --cov=myapp --cov-report=html
```

**Arguments :**
- `path` : Chemin vers les tests (optionnel)

**Options :**
- `-v` : Mode verbose
- `-x` : Arrêt au premier échec
- `-n` : Nombre de workers pour exécution parallèle (auto, 2, 4...)
- `--cov` : Module Python pour la couverture de code
- `--cov-report` : Type de rapport (html, term-missing)
- `--lf` : Rejouer uniquement les tests échoués
- `--ff` : Exécuter les tests échoués en premier
- `--create-db` : Forcer la création de la base de données de test
- `--migrations` : Forcer l'exécution des migrations
- `-s, --service` : Service Docker cible

---

### Commandes de tests

#### `n7 t` - Tests pytest en local

Exécute les tests pytest localement (sans Docker).

```bash
# Tous les tests
n7 t

# Tests d'un fichier ou répertoire spécifique
n7 t tests/test_api.py
n7 t tests/unit/

# Avec toutes les options disponibles (identiques à n7 dkc t)
n7 t -v
n7 t -x
n7 t -n auto
n7 t --cov=myapp --cov-report=html
n7 t --lf
n7 t --ff
n7 t --create-db
n7 t --migrations
```

**Arguments et options :** Identiques à `n7 dkc t`, sauf `--service` qui n'est pas disponible.

---

## Développement

### Installation pour le développement

```bash
# Cloner le projet
git clone <repository-url>
cd cli-nseven

# Créer un environnement virtuel
python3.13 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Installer en mode développement
pip install -e .
```

Cela permet d'utiliser la commande `n7` directement avec votre code en cours de développement.

### Tests

```bash
# Lancer tous les tests
pytest

# Mode verbose
pytest -v

# Avec couverture
pytest --cov=n7 --cov-report=html
```

### Outils de développement

#### Formatter (Black)

```bash
black .
```

#### Linter (Ruff)

```bash
# Vérification
ruff check

# Correction automatique
ruff check --fix
```

#### Type checking (mypy)

```bash
mypy .
```

#### Tout en une commande

Si n7 est installé en mode dev :

```bash
# Vérification seule
n7 py-lint

# Avec correction automatique
n7 py-lint --fix
```

---

## Configuration

Le CLI recherche automatiquement les fichiers de configuration Docker :
- `docker-compose.yml` ou fichier spécifié
- `.env` ou fichier d'environnement spécifié

Configuration via fichier `.n7.yml` (optionnel) :

```yaml
docker:
  compose_file: docker-compose.yml
  env_file: .env
  default_service: api
```

---

## Licence

MIT