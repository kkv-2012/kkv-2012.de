"""Erzeugt drei ausfüllbare PDF-Formulare im KKV-Stil (gleiche Kopf-/Fußzeile wie die Anzeigenbestellung)."""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LS", FD + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LSB", FD + "LiberationSans-Bold.ttf"))
PURPLE = HexColor("#8A2E7C"); PURPLE_LIGHT = HexColor("#F3E8F1"); GREY = HexColor("#6B6B6B"); LINE = HexColor("#B9B9B9")
W, H = A4; ML = MR = 20 * mm; CW = W - ML - MR
OUT = "/home/claude/kkv/site/dokumente/"
FOOT = ["Kürtener Karnevalsverein von 2012 e.V. · Vorstand: Peter Adelt, André van Herpt, Lisa Spiegel",
        "Kreissparkasse Köln · IBAN: DE48 3705 0299 0320 5528 30 · BIC: COKSDE33XXX",
        "Volksbank Berg eG · IBAN: DE04 3706 9125 0014 2860 12 · BIC: GENODED1RKO",
        "Finanzamt Bergisch Gladbach, Steuernummer: 204/5834/0477 · Vereinsregister beim Amtsgericht Köln, Blatt VR 17655"]


class Form:
    def __init__(self, filename, title, subtitle):
        self.c = canvas.Canvas(OUT + filename, pagesize=A4)
        self.c.setTitle(title + " – Kürtener Karnevalsverein von 2012 e.V.")
        self.c.setAuthor("Kürtener Karnevalsverein von 2012 e.V.")
        self.form = self.c.acroForm
        self.page = 1
        self.header(subtitle)

    def header(self, subtitle):
        c = self.c; top = H - 15 * mm; lw = 32 * mm
        c.drawImage("/home/claude/kkv/logo.jpg", ML, top - lw, lw, lw, mask="auto")
        tx = ML + lw + 6 * mm
        self.text(tx, top - 9 * mm, "Kürtener Karnevalsverein", "LSB", 19, PURPLE)
        self.text(tx, top - 16.5 * mm, "von 2012 e.V.", "LSB", 19, PURPLE)
        self.text(tx, top - 24 * mm, subtitle, "LS", 11.5, GREY)
        c.setStrokeColor(PURPLE); c.setLineWidth(1.6)
        c.line(ML, top - lw - 4 * mm, W - MR, top - lw - 4 * mm)
        self.y = top - lw - 12 * mm
        self.footer()

    def footer(self):
        c = self.c; fy = 22 * mm
        c.setStrokeColor(LINE); c.setLineWidth(0.5); c.line(ML, fy + 3 * mm, W - MR, fy + 3 * mm)
        for i, ln in enumerate(FOOT):
            self.text(W / 2 - c.stringWidth(ln, "LS", 7.5) / 2, fy - i * 3.8 * mm, ln, "LS", 7.5, GREY)

    def text(self, x, y, s, font="LS", size=10, color=black):
        self.c.setFont(font, size); self.c.setFillColor(color); self.c.drawString(x, y, s)

    def h2(self, s):
        self.y -= 1 * mm
        self.text(ML, self.y, s, "LSB", 12, PURPLE); self.y -= 6.5 * mm

    def para(self, lines, size=9.5, gap=4.6):
        for ln in lines:
            self.text(ML, self.y, ln, "LS", size); self.y -= gap * mm

    def field(self, name, label, w=None, x=None, h=6.8 * mm, tooltip=None):
        x = ML if x is None else x; w = CW if w is None else w
        self.text(x, self.y + 1.2 * mm, label, "LS", 8, GREY)
        self.form.textfield(name=name, tooltip=tooltip or label, x=x, y=self.y - h - 0.5 * mm, width=w, height=h,
                            borderWidth=0.6, borderColor=LINE, fillColor=white, textColor=black,
                            fontName="Helvetica", fontSize=10, forceBorder=True)

    def row(self, fields, h=6.8 * mm, gap=4 * mm):
        """fields: list of (name, label, weight)"""
        total = sum(f[2] for f in fields); x = ML; avail = CW - gap * (len(fields) - 1)
        for name, label, wt in fields:
            w = avail * wt / total
            self.field(name, label, w, x, h)
            x += w + gap
        self.y -= h + 5.2 * mm

    def check(self, name, label, x=None, tooltip=None, bold=False):
        x = ML if x is None else x
        self.form.checkbox(name=name, tooltip=tooltip or label, x=x + 1 * mm, y=self.y - 1.5 * mm, size=4.2 * mm,
                           buttonStyle="check", borderWidth=0.8, borderColor=PURPLE, fillColor=white, textColor=PURPLE, forceBorder=True)
        self.text(x + 8 * mm, self.y, label, "LSB" if bold else "LS", 10)

    def checks(self, items, cols=1, step=6.2 * mm):
        colw = CW / cols
        for i, (name, label) in enumerate(items):
            col = i % cols
            if col == 0 and i > 0: self.y -= step
            self.check(name, label, ML + col * colw)
        self.y -= step + 1 * mm

    def signature(self, label="Unterschrift"):
        c = self.c; self.y -= 6 * mm
        d_w = 45 * mm
        self.form.textfield(name="datum_" + str(self.page), tooltip="Datum", x=ML, y=self.y, width=d_w, height=6.8 * mm,
                            borderWidth=0.6, borderColor=LINE, fillColor=white, fontName="Helvetica", fontSize=10, forceBorder=True)
        sig_x = ML + d_w + 10 * mm
        c.setStrokeColor(black); c.setLineWidth(0.6); c.line(sig_x, self.y, W - MR, self.y)
        self.text(ML, self.y - 4.5 * mm, "Ort, Datum", "LS", 8.5, GREY)
        self.text(sig_x, self.y - 4.5 * mm, label, "LS", 8.5, GREY)
        self.y -= 14 * mm

    def box(self, lines, title=None):
        n = len(lines) + (1 if title else 0)
        h = n * 4.6 * mm + 6 * mm
        self.c.setFillColor(PURPLE_LIGHT); self.c.roundRect(ML, self.y - h + 4 * mm, CW, h, 2 * mm, fill=1, stroke=0)
        yy = self.y - 1 * mm
        if title:
            self.text(ML + 4 * mm, yy, title, "LSB", 9, PURPLE); yy -= 4.6 * mm
        for ln in lines:
            self.text(ML + 4 * mm, yy, ln, "LS", 8.5, black); yy -= 4.6 * mm
        self.y -= h + 2 * mm

    def banner(self, msg):
        if self.y < 44 * mm: return
        self.y -= 3 * mm
        self.c.setFillColor(PURPLE); self.c.roundRect(ML, self.y - 5 * mm, CW, 12 * mm, 2 * mm, fill=1, stroke=0)
        self.text(W / 2 - self.c.stringWidth(msg, "LSB", 11.5) / 2, self.y - 1 * mm, msg, "LSB", 11.5, white)
        self.y -= 14 * mm

    def newpage(self, subtitle):
        self.c.showPage(); self.page += 1; self.header(subtitle)

    def save(self):
        self.c.save()


# ---------------- 1. Mitgliedschaftsantrag ----------------
f = Form("KKV_Mitgliedsantrag.pdf", "Mitgliedsantrag", "Antrag auf Mitgliedschaft")
f.h2("Antrag auf Mitgliedschaft")
f.para(["Hiermit beantrage ich die Aufnahme in den Kürtener Karnevalsverein von 2012 e.V. (KKV)."])
f.y -= 3 * mm
f.row([("nachname", "Name", 1), ("vorname", "Vorname", 1)])
f.row([("strasse", "Straße, Hausnummer", 2), ("plz", "PLZ", 0.6), ("ort", "Ort", 1.2)])
f.row([("geburtsdatum", "Geburtsdatum", 1), ("telefon", "Telefon / Mobil", 1), ("email", "E-Mail", 1.4)])
f.text(ML, f.y, "Art der Mitgliedschaft (bitte ankreuzen):", "LSB", 10); f.y -= 8 * mm
f.checks([("aktiv", "Aktives Mitglied"), ("passiv", "Passives / förderndes Mitglied"),
          ("jugend", "Jugendmitglied (bis 18 Jahre)"), ("familie", "Familienmitgliedschaft")], cols=2)
f.text(ML, f.y, "Interesse an (freiwillig):", "LSB", 10); f.y -= 8 * mm
f.checks([("i_zug", "Karnevalszug / Wagenbau"), ("i_sitzung", "Sitzungen / Veranstaltungen"),
          ("i_tanz", "Tanzgruppe / Garde"), ("i_helfer", "Helferteam")], cols=2)
f.h2("SEPA-Lastschriftmandat")
f.para(["Ich ermächtige den Kürtener Karnevalsverein von 2012 e.V., den Mitgliedsbeitrag von meinem Konto mittels Lastschrift",
        "einzuziehen. Zugleich weise ich mein Kreditinstitut an, die vom Verein auf mein Konto gezogenen Lastschriften einzulösen.",
        "Hinweis: Ich kann innerhalb von acht Wochen, beginnend mit dem Belastungsdatum, die Erstattung des belasteten Betrages",
        "verlangen. Es gelten dabei die mit meinem Kreditinstitut vereinbarten Bedingungen."], size=8.5, gap=4.2)
f.y -= 2 * mm
f.row([("kontoinhaber", "Kontoinhaber/in", 1), ("bank", "Kreditinstitut", 1)])
f.row([("iban", "IBAN", 2), ("bic", "BIC", 1)])
f.box(["Gläubiger-ID: ______________________ (vom Verein)   ·   Mandatsreferenz: Mitgliedsnummer",
       "Der Jahresbeitrag richtet sich nach der aktuellen Beitragsordnung und wird jährlich eingezogen."], "Angaben des Vereins")
f.h2("Datenschutz und Unterschrift")
f.para(["Mit meiner Unterschrift erkenne ich die Satzung des Vereins an. Ich bin damit einverstanden, dass meine Daten zur",
        "Mitgliederverwaltung gespeichert werden. Eine Weitergabe an Dritte erfolgt nicht. Bei Minderjährigen unterschreibt",
        "ein/e Erziehungsberechtigte/r."], size=8.5, gap=4.2)
f.y -= 1 * mm; f.check("foto_ok", "Ich bin einverstanden, dass Fotos von Vereinsveranstaltungen, auf denen ich zu sehen bin,")
f.y -= 4.2 * mm; f.text(ML + 8 * mm, f.y, "auf der Vereinswebseite und bei Instagram veröffentlicht werden.", "LS", 10)
f.y -= 2 * mm
f.signature("Unterschrift (bei Minderjährigen: Erziehungsberechtigte/r)")
f.banner("Herzlich willkommen im KKV – Kürten Alaaf!")
f.save()

# ---------------- 2. Zuganmeldung ----------------
f = Form("KKV_Zuganmeldung_Gruppen.pdf", "Zuganmeldung", "Anmeldung zum Kürtener Karnevalszug 2027")
f.h2("Anmeldung einer Gruppe zum Kürtener Karnevalszug")
f.para(["Bitte vollständig ausfüllen und bis zum Anmeldeschluss per E-Mail an die Zugleitung senden."])
f.y -= 1 * mm
f.box(["Zugleitung: Robert Bechtel  ·  Telefon: 0157 57229780  ·  E-Mail: robert.bechtel@online.de",
       "Anmeldeschluss: ______________   ·   Zugtag: Samstag, 06.02.2027   ·   Aufstellung ab: __________"], "Zugleitung / Anmeldung")
f.y -= 1 * mm
f.row([("gruppe", "Name der Gruppe / des Vereins / der Firma", 2), ("teilnehmer", "Anzahl Teilnehmer/innen", 0.8)])
f.row([("motto", "Motto / Kostüm der Gruppe", 1)])
f.row([("ansprech", "Verantwortliche/r Ansprechpartner/in (volljährig)", 1.4), ("a_tel", "Telefon / Mobil (am Zugtag erreichbar)", 1)])
f.row([("a_strasse", "Straße, Hausnummer", 2), ("a_plz", "PLZ", 0.6), ("a_ort", "Ort", 1.2)])
f.row([("a_email", "E-Mail", 1.2), ("a_anzahl_kinder", "davon Kinder unter 14", 0.6)])
f.text(ML, f.y, "Art der Teilnahme (bitte ankreuzen):", "LSB", 10); f.y -= 8 * mm
f.checks([("fuss", "Fußgruppe"), ("wagen", "Festwagen (Zugmaschine + Anhänger)"),
          ("bollerwagen", "Handwagen / Bollerwagen"), ("musik", "Musikgruppe / Spielmannszug")], cols=2)
f.text(ML, f.y, "Nur bei Festwagen:", "LSB", 10); f.y -= 8 * mm
f.row([("zugmaschine", "Zugmaschine (Typ, Kennzeichen)", 1), ("fahrer", "Fahrer/in (Name, Führerscheinklasse)", 1)])
f.row([("wagenmasse", "Maße des Wagens (Länge x Breite x Höhe in m)", 1), ("wagenbauer", "Verantwortliche/r für den Wagenbau", 1)])
f.text(ML, f.y, "Wurfmaterial:", "LSB", 10); f.y -= 7 * mm
f.checks([("wurf_ja", "Wir werfen Kamelle (kein Glas, nichts Hartes)"), ("wurf_nein", "Wir werfen nichts")], cols=2)
f.h2("Erklärung")
f.para(["Die Gruppe befolgt die Zugordnung und die Anweisungen von Zugleitung und Ordnungskräften. Spirituosen sind untersagt,",
        "Jugendliche unter 16 Jahren erhalten keinen Alkohol. Wurfmaterial wird zugeworfen, nicht in die Zuschauer geworfen.",
        "Festwagen führen mindestens 4 Wagenbegleiter mit, die Räder sind gesichert. Der/die Ansprechpartner/in haftet für die",
        "Gruppe und bestätigt, dass für Fahrzeuge eine gültige Haftpflichtversicherung besteht."], size=8.5, gap=4.2)
f.y -= 2 * mm
f.check("erkl", "Wir haben die Erklärung gelesen und akzeptieren die Zugordnung.", bold=True)
f.y -= 2 * mm
f.signature("Unterschrift Ansprechpartner/in")
f.banner("Wir freuen uns auf euch beim Kürtener Karnevalszug – Alaaf!")
f.save()

# ---------------- 3. Spendenvordruck ----------------
f = Form("KKV_Spendenvordruck.pdf", "Spendenvordruck", "Spende für die Brauchtumsarbeit")
f.h2("Spendenerklärung")
f.para(["Ich / Wir unterstütze(n) die Brauchtumsarbeit des Kürtener Karnevalsvereins von 2012 e.V. mit einer Spende.",
        "Der Verein ist als gemeinnützig anerkannt; Spenden sind steuerlich abzugsfähig."])
f.y -= 3 * mm
f.row([("sp_name", "Name / Firma", 1.4), ("sp_ansprech", "Ansprechpartner/in", 1)])
f.row([("sp_strasse", "Straße, Hausnummer", 2), ("sp_plz", "PLZ", 0.6), ("sp_ort", "Ort", 1.2)])
f.row([("sp_email", "E-Mail", 1), ("sp_tel", "Telefon", 1)])
f.text(ML, f.y, "Art der Spende:", "LSB", 10); f.y -= 8 * mm
f.checks([("geld", "Geldspende"), ("sach", "Sachspende (z. B. Wurfmaterial, Material für den Wagenbau)"),
          ("einmal", "einmalig"), ("jaehrlich", "jährlich")], cols=2)
f.row([("betrag", "Betrag in EUR (bei Geldspende)", 1), ("sachbeschreibung", "Beschreibung / Wert der Sachspende", 2)])
f.text(ML, f.y, "Verwendungszweck (Wunsch):", "LSB", 10); f.y -= 8 * mm
f.checks([("vz_allgemein", "Allgemeine Brauchtumsarbeit"), ("vz_zug", "Karnevalszug"),
          ("vz_jugend", "Kinder- und Jugendarbeit"), ("vz_heft", "Sessionsheft")], cols=2)
f.text(ML, f.y, "Zahlungsweise (bei Geldspende):", "LSB", 10); f.y -= 8 * mm
f.checks([("ueberweisung", "Überweisung auf eines der unten genannten Vereinskonten (Verwendungszweck: „Spende“ + Name)"),
          ("lastschrift", "Einzug per SEPA-Lastschrift (Mandat siehe unten)")], cols=1)
f.row([("sp_iban", "IBAN (nur bei Lastschrift)", 2), ("sp_bic", "BIC", 1)])
f.text(ML, f.y, "Zuwendungsbestätigung:", "LSB", 10); f.y -= 8 * mm
f.checks([("zb_ja", "Ich wünsche eine Zuwendungsbestätigung (Spendenquittung) an die oben genannte Anschrift."),
          ("zb_nein", "Nicht nötig (bis 300 EUR genügt dem Finanzamt der Kontoauszug zusammen mit diesem Vordruck).")], cols=1)
f.para(["Ich ermächtige den Kürtener Karnevalsverein von 2012 e.V., bei Wahl der Lastschrift den angegebenen Betrag von meinem",
        "Konto einzuziehen. Meine Daten werden ausschließlich zur Abwicklung der Spende und zur Ausstellung der Bestätigung",
        "gespeichert."], size=8.5, gap=4.2)
f.signature("Unterschrift Spender/in")
f.banner("Herzlichen Dank für Ihre Unterstützung unserer Brauchtumsarbeit!")
f.save()
print("ok")
