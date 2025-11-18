````md
# Session Manager

Een krachtige en uitbreidbare Python-module voor het beheren, beveiligen en opslaan van sessies in JSON, CSV, SQLite of PostgreSQL formaten. Ideaal voor toepassingen die tijdelijke of beveiligde gebruikerssessies vereisen.

---

## 📦 Inhoud

- [Beschrijving](#beschrijving)
- [Installatie](#installatie)
- [Gebruik](#gebruik)
  - [SessionManager](#sessionmanager)
  - [SessionStoring](#sessionstoring)
- [Bestandsopslag](#bestandsopslag)
- [Voorbeelden](#voorbeelden)
- [Structuur van een sessie](#structuur-van-een-sessie)
- [Berichten en logging](#berichten-en-logging)
- [Extensies](#extensies)

---

## 📘 Beschrijving

De `SessionManager` beheert gebruikerssessies met functies zoals:
- Automatisch verlopen van sessies
- Wachtwoordbeveiligde sessies
- Exporteren en importeren naar JSON, CSV, SQLite of PostgreSQL
- Sessies ontgrendelen / vergrendelen
- Logging van fouten en successen

De `SessionStoring` klasse biedt methodes om sessies op te slaan of te laden in diverse formaten.

---

## 🛠️ Installatie

Installeer afhankelijkheden met pip:

```bash
pip install psycopg2
````

Zorg ervoor dat de volgende modules beschikbaar zijn in je project:

* `pysessionmanager.codes` voor `SessionMessages`
* `security.py` met:

  * `generate_session_id()`
  * `hash_password()`
  * `verify_password()`
* `utils.py` met:

  * `get_default_unick_name()`

---

## 🚀 Gebruik

### ✨ SessionManager

```python
manager = SessionManager("my_app", protect=True, auto_renew=True)
```

### ➕ Sessie aanmaken

```python
session_id = manager.create(
    unick_name="user1",
    duration_seconds=3600,
    value="some data",
    password="secure123"
)
```

### 🔐 Vergrendelen / Ontgrendelen

```python
manager.lock(session_id, "newpassword")
manager.unlock("user1", "newpassword")
```

### 🔎 Ophalen

```python
session_data = manager.get(session_id)
```

### 🧼 Opruimen van verlopen sessies

```python
active, removed, protected = manager.get_all()
```

---

## 💾 SessionStoring

```python
store = SessionStoring()
store.store_sessions_json(manager.sessions, "backup.json")
loaded = store.load_sessions_csv("sessions.csv")
```

---

## 🗃️ Bestandsopslag

### JSON

```python
store.store_sessions_json(manager.sessions, "data.json")
```

### CSV

```python
store.store_sessions_csv(manager.sessions, "data.csv")
```

### SQLite

```python
store.store_sessions_sqlite("sessions.db", manager.sessions)
```

### PostgreSQL

```python
store.store_sessions_postgresql(sessions=manager.sessions, conn_string="dbname=test user=postgres")
```

---

## ✅ Structuur van een sessie

```json
{
  "session_id_123": {
    "unick_name": "john_doe",
    "start_time": "2025-06-12T12:00:00",
    "end_time": "2025-06-12T13:00:00",
    "protected": true,
    "password": "<hashed_password>",
    "value": "extra data"
  }
}
```

---

## 🔔 Berichten en logging

De module gebruikt `SessionMessages` voor gestandaardiseerde fout- en succesmeldingen, en `logging` om informatie te loggen.

Voorbeeld logstructuur:

```python
manager.logs = {
  "errors": ["Fout bij sessie"],
  "successful": ["Sessie succesvol aangemaakt"],
  "debug": ["IS_ACTIVE -- session_id"]
}
```

---

## 📚 Voorbeelden

### 1. Sessie aanmaken zonder wachtwoord

```python
manager = SessionManager("test_app")
session_id = manager.create(unick_name="anon")
```

### 2. Beschermde sessie aanmaken

```python
manager = SessionManager("secure_app", protect=True)
session_id = manager.create(unick_name="admin", password="supersecret")
```

### 3. Sessie ophalen op basis van naam

```python
session_id = manager.get_with_unick_name("admin")
```

### 4. Gegevens van sessie ophalen

```python
value = manager.get_value(session_id)
```

### 5. Tijd over of verstreken

```python
remaining = manager.get_time_remaining(session_id)
elapsed = manager.time_passed(session_id)
```

---

## 🧩 Extensies

* Implementeer opslag in MongoDB of Redis
* Voeg API-integratie toe (bv. via Flask)
* Voeg auditlogs toe voor sessiebeheer
* Ondersteuning voor sessiehernieuwing (auto-renewal)

---

## 🧾 Licentie

MIT License © 2025 – Ontwikkeld door \[Ahmad Al Dibo]

```

