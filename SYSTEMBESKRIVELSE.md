# Math Solver – Systembeskrivelse

## Formål
En webapp som løser typiske førsteårsoppgaver i matematikk ved hjelp av KI-assistert utvikling ("vibe coding"). Appen kombinerer språkmodeller for resonnering med SymPy for deterministisk symbolsk/numerisk beregning.

## Fagområder
- Derivasjon og integrasjon (Thomas' Calculus)
- Lineær algebra
- Differensialligninger
- Komplekse tall
- Referanser: Edwards & Penney: *Differential Equations & Linear Algebra*, Thomas' *Calculus*

## Kravspesifikasjon

### 1. Input
- Bruker legger inn en matteoppgave som tekst
- Appen identifiserer oppgavetype (beregning, bevis, resonnering)

### 2. Løsning
- **Beregningsoppgaver**: Språkmodell (via API) planlegger løsning → SymPy utfører deterministisk beregning
- **Bevis/resonnering**: Språkmodell gir tekstsvar med disclaimer om manglende verifikasjon
- Alle mellomtrinn vises med forklaring

### 3. Formelreferanser
- Innebygd formelsamling (Jarle Johannessen: *Tekniske Tabeller*-stil)
- Hver formel har: ID, navn, bok-/kapittelreferanse
- Knyttes til steget der den brukes

### 4. Validering
- Numerisk validering av svar (f.eks. innsetting i differensialligningen)
- Valideringsresultat vises i frontend
- Margin for floating-point avrunding

### 5. Frontend
- Stegvis løsning med forklaringer
- Formelreferanser med kilder
- Valideringsresultat

## Arkitektur

```
math-solver/
├── backend/
│   ├── app.py                 # Flask/FastAPI app
│   ├── solver/
│   │   ├── __init__.py
│   │   ├── sympy_engine.py    # SymPy-integrasjon
│   │   ├── llm_planner.py     # LLM-basert planlegging
│   │   ├── validator.py       # Numerisk validering
│   │   └── formulas.py        # Formelsamling
│   ├── routes/
│   │   ├── solve.py           # POST /solve
│   │   └── formulas.py        # GET /formulas
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── solver.js
│   │   └── renderer.js
│   └── assets/
├── tests/
│   ├── test_solver.py
│   └── test_validation.py
├── SYSTEMBESKRIVELSE.md
├── README.md
└── .gitignore
```

## API-kontakter
- **LLM API**: OpenAI API (eller tilsvarende) for planlegging og resonnering
- **Backend**: Flask/FastAPI
- **Frontend**: Vanilla JS + HTML/CSS

## Dataflow
1. Frontend: Bruker legger inn oppgave
2. Backend: `/solve` mottar oppgave
3. LLM-planner: Identifiserer oppgavetype, planlegger løsningstrinn
4. SymPy-engine: Utfører beregninger steg for steg
5. Validator: Sjekker svar numerisk
6. Frontend: Viser stegvis løsning, formler, validering

## Validering
- For differensialligninger: Innsetting av løsning i ligning
- For likninger: Løsning skal oppfylle likningen
- Toleranse for floating-point: ±1e-6 eller lignende
- Ugyldige eller uløselige oppgaver rapporteres med årsak

## Fremtidsutvidelser
- Grafisk visualisering av løsninger
- LaTeX-rendering for formler
- Støtte for flere LLM-leverandører
- Oppgavebank med kjente oppgaver og løsninger
