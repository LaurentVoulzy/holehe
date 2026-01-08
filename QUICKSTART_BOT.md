# 🚀 Quick Start - PropFirm Tracker Bot

Guide de démarrage rapide pour utiliser le bot en 5 minutes.

## Étape 1: Installation (2 min)

```bash
# Installer les dépendances
pip install -r propfirm_bot/requirements.txt
```

## Étape 2: Créer votre bot Telegram (2 min)

1. Ouvrez Telegram
2. Cherchez **@BotFather**
3. Envoyez `/newbot`
4. Choisissez un nom pour votre bot (ex: "Mon PropFirm Tracker")
5. Choisissez un username (ex: "mon_propfirm_bot")
6. **Copiez le token** que BotFather vous donne (ressemble à `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

## Étape 3: Configurer le token (30 sec)

**Option A: Variable d'environnement**
```bash
export TELEGRAM_BOT_TOKEN='VOTRE_TOKEN_ICI'
```

**Option B: Argument direct**
```bash
python start_propfirm_bot.py VOTRE_TOKEN_ICI
```

## Étape 4: Lancer le bot (30 sec)

```bash
python start_propfirm_bot.py
```

Vous devriez voir:
```
🚀 Démarrage du PropFirm Tracker Bot...
📱 Ouvrez Telegram et cherchez votre bot!
⚠️  Appuyez sur Ctrl+C pour arrêter le bot

INFO - Bot is running...
```

## Étape 5: Utiliser le bot (immédiat)

1. Ouvrez Telegram
2. Cherchez votre bot (le nom que vous avez donné)
3. Cliquez sur **Start** ou envoyez `/start`
4. Le bot vous répond avec le menu d'aide

## 🎯 Premiers pas

### Créer votre premier compte

```
/add FTMO_Challenge 100000 FTMO
```

### Voir vos comptes

```
/list
```

### Mettre à jour votre compte

```
/update FTMO_Challenge 105000 105500
```

### Voir le dashboard

```
/dashboard FTMO_Challenge
```

## 📖 Documentation complète

Pour plus d'informations, consultez [README_PROPFIRM_BOT.md](README_PROPFIRM_BOT.md)

## ⚠️ Problèmes courants

### "Module not found"
```bash
pip install -r propfirm_bot/requirements.txt
```

### "Token non configuré"
Assurez-vous d'avoir défini `TELEGRAM_BOT_TOKEN` ou de le passer en argument.

### Le bot ne répond pas
- Vérifiez que le script Python tourne toujours
- Vérifiez votre connexion Internet
- Vérifiez que le token est correct

## 🎉 C'est tout !

Vous êtes prêt à tracker vos comptes PropFirm !

---

**Besoin d'aide ?** Consultez le [README complet](README_PROPFIRM_BOT.md) ou ouvrez une issue.
