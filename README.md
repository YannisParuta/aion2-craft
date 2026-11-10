# AION 2 — Calculateur de craft

Calculateur de matériaux de fabrication pour AION 2 (forge, alchimie, joaillerie, couture).

- **Version web** : publiée automatiquement sur GitHub Pages à chaque push sur `main`.
  Vos réglages (stock, prix, niveau…) sont enregistrés dans votre navigateur.
- **Version bureau (Windows)** : exécutable Go autonome qui ouvre l'interface dans une fenêtre Edge/Chrome.

## Structure

| Fichier | Rôle |
|---|---|
| `web/index.html`, `web/engine.js` | Interface et moteur de calcul |
| `gen_data.py` + `fr.json` | Génèrent `data.json` (recettes, prix, traductions) |
| `main.go`, `res.rc`, `icon.ico` | Exécutable bureau |

## Développement

```bash
python3 gen_data.py                     # régénère data.json
mkdir -p _site && cp web/* data.json _site/ && python3 -m http.server -d _site 8000
```

Compiler l'exécutable Windows :

```bash
GOOS=windows GOARCH=amd64 go build -ldflags "-H windowsgui" -o AION2-Craft.exe
```
