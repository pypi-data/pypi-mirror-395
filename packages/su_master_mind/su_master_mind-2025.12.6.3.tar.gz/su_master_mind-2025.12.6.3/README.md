# Master DAC

Code permettant de gérer les configurations des machines des étudiants DAC (packages python, jeux de données)

## Pour publier sur pypi

### Configuration initiale (à faire une fois)

Éditer `~/.config/hatch/config.toml` et ajouter:

```toml
[publish.index.repos.su-master-mind]
url = "https://upload.pypi.org/legacy/"
user = "__token__"
auth = "pypi-YOUR_PROJECT_SPECIFIC_TOKEN_HERE"
```

Remplacer `YOUR_PROJECT_SPECIFIC_TOKEN_HERE` par votre token PyPI spécifique au projet.

### Publier une nouvelle version

Après avoir mis à jour la version dans `pyproject.toml`:

```sh
# Build
hatch build

# Publish using the configured repository
hatch publish -r su-master-mind
```

Note: Le `-r su-master-mind` est nécessaire pour utiliser le dépôt configuré ci-dessus.
