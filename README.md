# Prepoznavanje lica — evidencija prisustva

Interna desktop / interna web aplikacija za evidenciju prisustva na događajima uz detekciju i prepoznavanje lica sa fotografija.

## Svrha sistema

Cilj sistema je da omogući:

- unos osoba u bazu,
- unos jedne ili više referentnih fotografija po osobi,
- kreiranje događaja,
- upload jedne ili više fotografija sa događaja,
- detekciju lica na događajskim fotografijama,
- poređenje sa bazom poznatih osoba,
- predlog identiteta sa confidence score,
- ručnu potvrdu ili korekciju rezultata,
- generisanje konačne evidencije prisustva,
- eksport u Excel i PDF.

Sistem je namenjen za internu upotrebu.  
AI služi kao pomoć pri identifikaciji. Konačnu potvrdu rezultata vrši ovlašćeni korisnik.

---

## Ključni principi

- MVP prvo, bez overengineering-a.
- Baza podataka je jedini source of truth.
- AI ne donosi konačnu odluku samostalno.
- Svaka velika izmena mora biti modularna i reverzibilna.
- Kod mora biti čitljiv, testabilan i spreman za dalje širenje.
- Bezbednost i audit imaju prioritet nad “demo” efektom.

---

## Planirana arhitektura

### Tehnologije

- Python 3.12+
- PySide6 ili PyQt6 za desktop GUI
- FastAPI za internu web varijantu ako bude potrebna
- SQLAlchemy 2.x
- SQLite za MVP
- PostgreSQL za ozbiljniju multi-user verziju
- OpenCV + embedding/face recognition pipeline
- pandas + openpyxl za Excel eksport
- reportlab ili weasyprint za PDF eksport
- pytest za testove

### Slojevi sistema

- `app/ui/` — GUI ili web sloj
- `app/services/` — poslovna logika
- `app/repositories/` — pristup bazi
- `app/db/models/` — SQLAlchemy modeli
- `app/recognition/` — detekcija i prepoznavanje lica
- `app/exports/` — Excel/PDF eksport
- `app/security/` — autentikacija, autorizacija, password hashing
- `tests/` — unit i integration testovi

---

## Obavezni moduli MVP-a

1. Osobe  
2. Fotografije osoba  
3. Događaji  
4. Fotografije događaja  
5. Detekcija i prepoznavanje lica  
6. Ručna potvrda rezultata  
7. Evidencija prisustva  
8. Eksport u Excel/PDF  
9. Audit log  
10. Login i role ako su potrebni

---

## Minimalni entiteti baze

- `Person`
- `PersonPhoto`
- `Event`
- `EventPhoto`
- `DetectedFace`
- `AttendanceRecord`
- `User`
- `AuditLog`

---

## Pokretanje projekta (trenutni skeleton)

1. Napraviti virtuelno okruženje:
   - `python -m venv .venv`
2. Aktivirati okruženje:
   - Linux/macOS: `source .venv/bin/activate`
   - Windows (PowerShell): `.venv\\Scripts\\Activate.ps1`
3. Instalirati zavisnosti:
   - `pip install -r requirements.txt`
4. Pokrenuti aplikaciju:
   - `python -m app.main`

---

## Napomena za doprinos kodu

Za AI-assisted development u ovom repozitorijumu koristi se `AGENTS.md`.  
Sva pravila za Codex, patch redosled, stil rada, testiranje i scope discipline definisani su tamo.
