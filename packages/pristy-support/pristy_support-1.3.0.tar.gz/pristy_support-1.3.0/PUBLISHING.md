# Guide de publication sur PyPI

Ce guide explique comment publier `pristy-support` sur PyPI en utilisant uv.

## Prérequis

### 1. Installer uv

Si vous n'avez pas uv installé :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ou avec pip :

```bash
pip install uv
```

### 2. Créer un compte PyPI

- Créez un compte sur [PyPI](https://pypi.org/account/register/)
- Créez également un compte sur [TestPyPI](https://test.pypi.org/account/register/) pour les tests

### 3. Configurer l'authentification PyPI

#### Option A : Token API (recommandé)

1. Allez sur [PyPI Account Settings](https://pypi.org/manage/account/)
2. Créez un token API avec le scope approprié
3. Configurez uv en créant un fichier `.pypirc` dans votre home directory :

```bash
cat > ~/.pypirc << EOF
[pypi]
username = __token__
password = pypi-VOTRE_TOKEN_ICI

[testpypi]
username = __token__
password = pypi-VOTRE_TOKEN_TESTPYPI
EOF
```

Ou utilisez les variables d'environnement :

```bash
export UV_PUBLISH_TOKEN=pypi-VOTRE_TOKEN_ICI
```

## Étapes de publication

### 1. Vérifier que tout fonctionne

```bash
# Synchroniser les dépendances
uv sync

# Lancer les tests
uv run pytest

# Vérifier que la commande fonctionne
uv run pristy-support --version
```

### 2. Mettre à jour la version

Éditez `pyproject.toml` et modifiez la version dans la section `[project]` :

```toml
[project]
version = "1.0.3"  # Incrémentez selon semver
```

Mettez également à jour `CHANGELOG.md` avec les changements de cette version.

### 3. Builder le package

```bash
uv build
```

Cela créera deux fichiers dans `dist/` :
- `pristy_support-X.Y.Z.tar.gz` (source distribution)
- `pristy_support-X.Y.Z-py3-none-any.whl` (wheel)

### 4. Tester sur TestPyPI (optionnel mais recommandé)

```bash
# Publier sur TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# Tester l'installation depuis TestPyPI
pip install --index-url https://test.pypi.org/simple/ pristy-support
```

### 5. Publier sur PyPI

```bash
uv publish
```

### 6. Vérifier la publication

Allez sur https://pypi.org/project/pristy-support/ pour vérifier que tout est bien publié.

Testez l'installation :

```bash
pip install --upgrade pristy-support
pristy-support --version
```

## Workflow de publication recommandé

1. **Développement** : Travaillez sur une branche
2. **Tests** : Assurez-vous que tous les tests passent (`uv run pytest`)
3. **Version** : Mettez à jour la version dans `pyproject.toml`
4. **Changelog** : Mettez à jour CHANGELOG.md avec les changements
5. **Commit** : `git commit -m "chore: bump version to X.Y.Z"`
6. **Tag** : `git tag vX.Y.Z`
7. **Build** : `uv build`
8. **TestPyPI** : `uv publish --publish-url https://test.pypi.org/legacy/` (optionnel)
9. **PyPI** : `uv publish`
10. **Push** : `git push && git push --tags`

## Automatisation avec GitLab CI/CD (optionnel)

Créez `.gitlab-ci.yml` :

```yaml
stages:
  - test
  - build
  - publish

test:
  stage: test
  image: python:3.9
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="$HOME/.cargo/bin:$PATH"
  script:
    - uv sync
    - uv run pytest
  only:
    - merge_requests
    - main

build:
  stage: build
  image: python:3.9
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="$HOME/.cargo/bin:$PATH"
  script:
    - uv build
  artifacts:
    paths:
      - dist/
  only:
    - tags

publish:
  stage: publish
  image: python:3.9
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="$HOME/.cargo/bin:$PATH"
  script:
    - export UV_PUBLISH_TOKEN=$PYPI_TOKEN
    - uv publish
  only:
    - tags
  dependencies:
    - build
```

N'oubliez pas d'ajouter la variable `PYPI_TOKEN` dans les settings CI/CD de GitLab.

## Dépannage

### Erreur "File already exists"

Si vous essayez de publier une version déjà existante :
- Incrémentez la version dans `pyproject.toml` (section `[project]`)
- Rebuild avec `uv build`
- Republiez

### Erreur d'authentification

Vérifiez vos credentials dans `~/.pypirc` ou la variable d'environnement `UV_PUBLISH_TOKEN`.

### Problème avec les fichiers inclus

Vérifiez que tous les fichiers nécessaires sont bien inclus :
```bash
tar -tzf dist/pristy-support-*.tar.gz
```

Si des fichiers manquent, vérifiez la configuration `[tool.hatch.build.targets.wheel]` dans `pyproject.toml`.

## Ressources

- [Documentation uv](https://docs.astral.sh/uv/)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)
