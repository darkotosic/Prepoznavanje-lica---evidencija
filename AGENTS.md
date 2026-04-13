# AGENTS.md

## Project identity

Ovo je repozitorijum za internu aplikaciju za evidenciju prisustva sa prepoznavanjem lica.

Primarni cilj je stabilan MVP koji realno radi u internoj organizaciji.

AI ne donosi konačnu odluku samostalno.  
AI daje predlog, čovek potvrđuje.

## Core engineering rules

1. Favorizuj jednostavno, stabilno i proširivo rešenje.
2. Ne pravi demo igračku; gradi osnovu za ozbiljan interni alat.
3. Baza je jedini source of truth.
4. Ne mešaj UI logiku i business logiku.
5. Svaka veća izmena mora biti modularna i reverzibilna.
6. Ne uvodi overengineering za MVP.
7. Ne radi širok refaktor van scope-a zadatka.
8. Svaka izmena mora biti odmah primenljiva i operativna.

## Required architecture boundaries

Poštuj sledeće slojeve:

- `app/ui/`
- `app/services/`
- `app/repositories/`
- `app/db/models/`
- `app/recognition/`
- `app/exports/`
- `app/security/`
- `tests/`

## Testing rules

Za svaku netrivijalnu izmenu:
- dodaj bar osnovni unit test ako postoji odgovarajuće mesto,
- ne ostavljaj kod bez minimalne validacije toka.

## Definition of done

Zadatak je završen tek kada:
- kod je konzistentan sa postojećom arhitekturom,
- nema nepotrebnih side-effect izmena,
- osnovni test scenario prolazi,
- dokumentacija je ažurirana ako treba,
- rezultat je production-safe za MVP nivo.
