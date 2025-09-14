

# Sitaattipalvelin – README

## Projektin tarkoitus

Sovellus on Pythonilla, Flaskilla ja Socket.IO:lla toteutettu verkkopalvelu, joka kokoaa ja esittää Matti Nykäsen elämänviisauksia. Palvelu tarjoaa selaimessa satunnaisia sitaatteja, mahdollistaa uusien sitaattien lisäämisen sekä näyttää Matti Nykäsen kuvia ja satunnaisia numeroita reaaliaikaisesti Socket.IO:n avulla.

## Sovelluksen rakenne

- **server.py**  
  Flask-palvelin, joka:
  - Näyttää HTML-sivun ja toimittaa staattiset tiedostot selaimelle.
  - Tarjoaa HTTP-rajapinnat sitaattien hakemiseen ja lisäämiseen.
  - Käsittelee Socket.IO-yhteyksiä ja välittää kuvat + numerot kaikille asiakkaille reaaliaikaisesti.

- **client.py**  
  Komentoriviohjelma, joka:
  - Kysyy käyttäjältä enintään kolme uutta Matti Nykäsen sitaattia ja lähettää ne palvelimelle, jos eivät ole jo tallessa.
  - Käynnistää taustasäikeessä Socket.IO-yhteyden, joka lähettää palvelimelle Matti Nykäsen kuvia järjestyksessä ja satunnaisia numeroita viiden sekunnin välein.

- **quotes.json**  
  Sitaattien tallennustiedosto (JSON-muodossa, avain: id, arvo: {text, source}).

- **static/**  
  - `script.js`: Lomakkeen käsittely ja Socket.IO-päivitysten vastaanotto selaimessa.
  - `style.css`: Sivun ulkoasu.
  - `kuvat/`: Matti Nykäsen kuvat (5 kpl).

- **templates/index.html**  
  HTML-pohja, joka näyttää 5 satunnaista sitaattia, kuvan ja numeron sekä lomakkeen uuden sitaatin lisäämiseen.

## Sovelluksen toiminta

### Palvelin

- **GET /**  
  Palauttaa HTML-sivun, jossa näkyy 5 satunnaista sitaattia ja Matti Nykäsen kuva +  random generoitu numero (Socket.IO:n kautta).

- **POST /add**  
  Lisää uuden sitaatin, jos samaa ei ole jo tallessa. Sitaatti ja lähde annetaan JSON-muodossa.

- **GET /daily**  
  Palauttaa yhden satunnaisen sitaatin JSON-muodossa. daily sitaatin löytää JSON-muodossa osoitteesta http://127.0.0.1:5000/daily

- **Socket.IO**  
  - Kun asiakas liittyy, palvelin lähettää nykyisen kuvan ja numeron.
  - Kun palvelin saa uuden kuvan ja numeron (client.py:ltä), se lähettää ne asiakkaalle päivityksenä.

### Asiakasohjelma (client.py)

- Kysyy käyttäjältä enintään kolme uutta sitaattia ja lähettää ne palvelimelle, jos eivät ole duplikaatteja.
- Käynnistää taustasäikeessä Socket.IO-yhteyden, joka:
  - Lähettää palvelimelle kuvat `mattinykanen1.jpg` ... `mattinykanen5.jpg` järjestyksessä.
  - Jokaisen kuvan yhteydessä lähetetään satunnainen numero (1–100).
  - Lähetys tapahtuu 5 sekunnin välein, kunnes ohjelma lopetetaan painamalla Ctrl+C.

### Selain

- Näyttää 5 satunnaista sitaattia ja Matti Nykäsen kuvan + numeron, jotka päivittyvät reaaliaikaisesti Socket.IO:n kautta.
- Lomakkeella voi lisätä uuden sitaatin, joka tallentuu samaan tietokantaan kun client.pylläkin lisätyt sitaatit. Lomakkeen lähetys tapahtuu       
JavaScriptin (script.js) avulla, joka lähettää uuden sitaatin POST-pyynnöllä palvelimelle osoitteeseen /add. Tässä tapauksessa selain toimii "asiakkaana" eli clientinä. Käyttäjä ei tarvitse client.py-ohjelmaa lainkaan, vaan voi lisätä sitaatteja suoraan selaimen kautta.

## Käyttöohjeet

1. Varmista, että Python on asennettu.

### Tarvittavien pakettien asennus

Asenna seuraavat paketit komentorivillä:

```bash
pip install flask
```

```bash
pip install flask-socketio
```

```bash
pip install python-socketio
```

### Sovelluksen käynnistys

Käynnistä palvelin:

```bash
python server.py
```

Käynnistä asiakasohjelma toisessa terminaalissa:

```bash
python client.py
```

Avaa selaimessa osoite http://127.0.0.1:5000. Tai daily sitaatti nähdäksesi http://127.0.0.1:5000/daily(ääkköset bugaa).