# Viikko 5 – AI Chat ja CI/CD

## Sovellus
http://195.148.20.80/viikko5/

Python Flask, Gunicorn, Nginx, Ollama ja MariaDB.

## Arkkitehtuuri
Selain → Nginx → Gunicorn/Flask → Ollama ja MariaDB.

## CI/CD
GitHub Actions suorittaa lintterin ja unittest-testit.
Onnistunut main-haaran testaus käynnistää automaattisen julkaisun.
Epäonnistunut testi estää julkaisun.
Julkaisu päivittää riippuvuudet sekä Nginx- ja systemd-asetukset.
Nginx-asetukset testataan ennen uudelleenlatausta.
Health-endpoint tarkistaa julkaistun Git SHA:n.

## Turvallisuus
- SSH-yhteys GitHub Actionsista Tailscalen kautta.
- SSH-avain, palvelinavain ja Tailscale-avain GitHub Secretsissa.
- Sovellus toimii viikko5-palvelukäyttäjällä.
- .env: root:viikko5, oikeudet 640.
- MariaDB: SELECT ja INSERT messages-tauluun.
- Gunicorn: 127.0.0.1:8002.
- Ollama: 127.0.0.1:11434.

## Tekoälymalli
- Malli: qwen2.5:0.5b
- Levykoko: 397 MB
- Mallin muistinkäyttö: 486 MB
- Palvelimen RAM: 1,9 GiB
- Swap: 2 GiB
- RAM käytössä mallin kanssa: 1,0 GiB

## Testaus
Automaattinen julkaisu ja Git SHA tarkistettu.
Tarkoituksella epäonnistunut unittest esti julkaisun.
Palvelut on asetettu käynnistymään automaattisesti.

## Opitut asiat
CI/CD automatisoi testauksen ja julkaisun.
Rajatut käyttöoikeudet ja Tailscale parantavat turvallisuutta.
