# Math Solver 🧮

AI-drevet løsning av matteoppgaver med detaljerte forklaringer, trinn-for-trinn løsninger og numerisk validering.

## Funksjoner

✨ **Intelligente Løsninger**
- LLM-basert analyse av oppgaver (GPT-4)
- Symbolsk løsning med SymPy
- Numerisk validering av resultater
- Detaljerte forklaringer på norsk

📚 **Matematiske Emner**
- **Calculus**: Derivasjon, Integrasjon
- **Lineær Algebra**: Matriser, Egenverdier
- **Differensialligninger**: ODE, Løsningsmetoder
- **Komplekse Tall**: Operasjoner, Polarform

🔍 **Formelsamling**
- 500+ matematiske formler
- Kategorisert etter emne
- Eksempler og referanser
- Søkbar database

## Arkitektur

```
math-solver/
├── backend/
│   ├── solver/
│   │   ├── llm_planner.py      # LLM-basert problemanalyse
│   │   ├── sympy_engine.py     # Symbolsk løsning
│   │   ├── validator.py        # Numerisk validering
│   │   └── formulas.py         # Formelatabase
│   ├── app.py                  # Flask-server
│   └── requirements.txt        # Python-avhengigheter
├── frontend/
│   ├── index.html              # HTML-grensesnitt
│   ├── css/style.css           # Styling
│   └── js/
│       ├── app.js              # Hovedapplikasjon
│       ├── solver.js           # API-klient
│       └── renderer.js         # Løsningsvisning
├── tests/                      # Enhetstester
└── README.md                   # Dokumentasjon
```

## Installasjon

### Forutsetninger
- Python 3.8+
- Node.js 14+ (for frontend)
- OpenAI API nøkkel

### Backend-oppsett

```bash
# Klon repository
git clone https://github.com/jonathanstenhjem-glitch/math-solver.git
cd math-solver

# Opprett virtuelt miljø
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Installer avhengigheter
pip install -r backend/requirements.txt

# Konfigurer miljøvariabler
cp .env.example .env
# Rediger .env og legg til din OpenAI API-nøkkel

# Start backend-server
python backend/app.py
```

### Frontend-oppsett

```bash
# Frontend er en enkel HTML/CSS/JS-applikasjon
# Åpne frontend/index.html i en nettleser
# eller serve via en lokal webserver:

python -m http.server 8000 --directory frontend
```

Åpne deretter `http://localhost:8000` i nettleseren din.

## Bruk

### Web-grensesnitt

1. Skriv inn en matteoppgave i tekstfeltet
2. Legg til kontekst eller grensebetingelser (valgfritt)
3. Klikk "Løs oppgaven"
4. Se den trinn-for-trinn løsningen med forklaringer
5. Validering viser om løsningen er korrekt

### API-endepunkter

#### Løs en oppgave
```bash
POST /solve
Content-Type: application/json

{
  "problem": "Finn den deriverte av x^3 + 2x",
  "context": "Bruk potenssregelen"
}
```

**Svar:**
```json
{
  "success": true,
  "problem_type": "calculation",
  "solution": {
    "steps": [
      {
        "step": 1,
        "description": "State the function",
        "calculation": "f(x) = x^3 + 2x",
        "result": "x^3 + 2x"
      }
    ],
    "final_answer": "3x^2 + 2",
    "formulas_used": [
      {
        "formula_id": "CALC-D-001",
        "description": "Power Rule"
      }
    ]
  },
  "validation": {
    "valid": true,
    "result": "Solution validated successfully",
    "checks": [...]
  }
}
```

#### Hent formler
```bash
GET /formulas?category=calculus&topic=derivatives
```

#### Helsekontroll
```bash
GET /health
```

## Eksempler

### Derivasjon
```
Problemet: Finn den deriverte av f(x) = x^3 + 2x
Svar: f'(x) = 3x^2 + 2
```

### Integrasjon
```
Problemet: Beregn ∫(2x) dx
Svar: x^2 + C
```

### Differensialligning
```
Problemet: Løs dy/dx = 2x
Svar: y = x^2 + C
```

## Testing

```bash
# Kjør alle tester
python -m pytest tests/

# Kjør spesifikk test
python -m pytest tests/test_solver.py -v

# Med dekningsrapport
python -m pytest tests/ --cov=backend/solver
```

## Konfigurering

### Miljøvariabler (.env)

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Solver
TOLERANCE=1e-6
MAX_COMPUTATION_TIME=30
```

## Feils øking

### "Could not connect to backend"
- Kontroller at backend kjører på `http://localhost:5000`
- Sjekk at Python-serveren er startet
- Verifiser at OpenAI API-nøkkel er konfigurert

### "Solution validation failed"
- Kontroller problemformuleringen
- Legg til kontekst eller grensebetingelser
- Verifiser toleranseverdi i .env

### "Formula not found"
- Formelbasen laster mulig ikke korrekt
- Kontroller databasefilen
- Restart backend-serveren

## Roadmap

- [ ] WebSocket for live-løsninger
- [ ] LaTeX-rendering av formler
- [ ] Grafisk visualisering av løsninger
- [ ] Mer avanserte differensialligninger
- [ ] Lokalisering (flere språk)
- [ ] Mobilapp
- [ ] Offlinemodus

## Lisens

MIT License - se LICENSE.md for detaljer

## Bidrag

Bidrag er velkomne! Vennligst:

1. Fork repository
2. Opprett en feature branch (`git checkout -b feature/ny-funksjon`)
3. Commit endringer (`git commit -am 'Add new feature'`)
4. Push til branch (`git push origin feature/ny-funksjon`)
5. Åpne en Pull Request

## Kontakt

Spørsmål eller forslag? Åpne en issue eller kontakt maintainer.

---

**Math Solver** - Gjør mattelekser enklere! 🚀
