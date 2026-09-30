# kkv-2012.de – Anleitung zur Pflege

Die Seite wird über eine **Redaktionsoberfläche im Browser** gepflegt, ohne Programmierkenntnisse.

## So änderst du Inhalte

1. `https://kkv-2012.de/admin` aufrufen → „Sign in with GitHub“.
2. Links den Bereich wählen: **Start: Instagram**, **Termine**, **Ansprechpartner**, **Dokumente**,
   **Über uns**, **Verein & Kontakt**, **Impressum & Datenschutz**.
3. Felder ausfüllen oder ändern. Listen (Termine, Ansprechpartner, Dokumente, Instagram-Links)
   haben einen Button „Hinzufügen“; Einträge lassen sich per Pfeil sortieren und mit dem
   Papierkorb löschen.
4. Oben rechts **„Speichern“**. Nach etwa einer Minute ist die Änderung live. Wer die Seite
   danach noch alt sieht, lädt einmal neu (Strg+F5).

Jede Änderung wird protokolliert (auf GitHub unter „Commits“) und lässt sich rückgängig machen.

## Die häufigsten Aufgaben

**Neuer Instagram-Beitrag:** Im Instagram-Beitrag auf „…“ → „Link kopieren“. In der Redaktion
unter „Start: Instagram“ → „Beitrag hinzufügen“, Link einfügen, mit dem Pfeil ganz nach oben
schieben, ältesten Eintrag unten löschen (6–9 Einträge sind ideal). Speichern.

**Termin eintragen:** „Termine“ → „Termin hinzufügen“ → Datum, Titel, Ort, Uhrzeit. Haken
„Noch nicht bestätigt“ setzen, solange der Termin vorläufig ist. Der nächste Zugtermin erscheint
automatisch groß auf der Startseite; vergangene Termine werden ausgegraut.

**Neues Sessionsheft oder Formular:** „Dokumente“ → beim Eintrag auf „PDF-Datei“ → „Datei
auswählen“ → PDF hochladen → Speichern. Für ein neues Dokument „Dokument hinzufügen“.

**Ansprechpartner ändern:** „Ansprechpartner“ → Eintrag öffnen → Name, E-Mail, Telefon ändern.
Den Haken „Angaben noch unvollständig“ entfernen, sobald alles stimmt (blendet das gelbe Schild aus).

**Motto oder Vereins-E-Mail ändern:** „Verein & Kontakt“.

## Instagram später automatisch?

Wenn der Vorstand einmal die Instagram-Zugangsdaten sortiert hat, kann man bei lightwidget.com
(kostenlos) ein Feed-Widget für `kkv_von_2012` erstellen und den Einbettcode in der Redaktion
unter „Start: Instagram“ → „Feed-Widget-Code“ eintragen. Dann aktualisieren sich die Beiträge
von selbst, und die Link-Liste wird nicht mehr gebraucht.

## Aufbau der Dateien (nur zur Info)

```
index.html           die Webseite (Gestaltung und Technik – muss nicht angefasst werden)
content/*.json       alle Inhalte – werden von der Redaktion geschrieben
dokumente/           hochgeladene PDFs
bilder/              Logo und Bilder
admin/               Redaktionsoberfläche (config.yml = Aufbau der Eingabemasken)
skripte/             Python-Skripte, mit denen die PDF-Formulare erzeugt wurden
```

## Bei Problemen

Seite zeigt alte Inhalte → Seite neu laden (Strg+F5), ggf. eine Minute warten.
Login unter /admin geht nicht → prüfen, ob der eigene GitHub-Account als Collaborator im
Repository eingetragen ist (Settings → Collaborators).
Design ändern → `index.html` bearbeiten; Farben stehen ganz oben im Block `:root`.
Formular-PDFs ändern → Skript in `skripte/` anpassen und mit Python ausführen oder PDF in einem
PDF-Editor öffnen; die neue Datei dann über die Redaktion hochladen.
