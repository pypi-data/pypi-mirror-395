# gai-init

gai-init is a utility for initializing Gai config and downloading local models.

## For Users

### a) To initialize Gai config

```bash
uvx gai-init@latest init
```

### b) To delete existing Gai config and start over

```bash
uvx gai-init@latest init --force
```

### c) To download local models

```bash
uvx gai-init@latest pull llama3.1-exl2
```

### d) To create a new project

```bash
uvx gai-init@latest create my_new_project --template minimal
```

---

## For Contributors

### a) To publish a new version

Make sure .pypirc is configured with your PyPI credentials.

```bash
make publish
```
