from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FD = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LS", FD + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LSB", FD + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LSI", FD + "LiberationSans-Italic.ttf"))

PURPLE = HexColor("#8A2E7C")     # aus dem Logo abgeleitet, leicht dunkler für Druck
PURPLE_LIGHT = HexColor("#F3E8F1")
GREY = HexColor("#6B6B6B")
LINE = HexColor("#B9B9B9")

W, H = A4
ML, MR = 20 * mm, 20 * mm
CW = W - ML - MR

OUT = "/home/claude/kkv/KKV_Anzeigenauftrag_Sessionsheft_2026-2027.pdf"
c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Anzeigen-Auftrag Sessionsheft 2026/2027 – Kürtener Karnevalsverein von 2012 e.V.")
c.setAuthor("Kürtener Karnevalsverein von 2012 e.V.")
c.setSubject("Anzeigenbestellung Sessionsheft 2026/2027")
form = c.acroForm


def text(x, y, s, font="LS", size=10, color=black):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, s)


def textbox(name, x, y, w, h=7 * mm, tooltip="", fontsize=10):
    form.textfield(name=name, tooltip=tooltip, x=x, y=y, width=w, height=h,
                   borderWidth=0.6, borderColor=LINE, fillColor=white,
                   textColor=black, fontName="Helvetica", fontSize=fontsize,
                   forceBorder=True)


def checkbox(name, x, y, tooltip="", size=4.2 * mm):
    form.checkbox(name=name, tooltip=tooltip, x=x, y=y, size=size,
                  buttonStyle="check", borderWidth=0.8, borderColor=PURPLE,
                  fillColor=white, textColor=PURPLE, forceBorder=True)


# ---------- Kopf ----------
top = H - 15 * mm
logo_w = 32 * mm
c.drawImage("/home/claude/kkv/logo.jpg", ML, top - logo_w, logo_w, logo_w, mask="auto")

tx = ML + logo_w + 6 * mm
text(tx, top - 9 * mm, "Kürtener Karnevalsverein", "LSB", 19, PURPLE)
text(tx, top - 16.5 * mm, "von 2012 e.V.", "LSB", 19, PURPLE)
text(tx, top - 24 * mm, "Anzeigen-Auftrag · Sessionsheft 2026/2027", "LS", 11.5, GREY)

# Purple rule
c.setStrokeColor(PURPLE)
c.setLineWidth(1.6)
c.line(ML, top - logo_w - 4 * mm, W - MR, top - logo_w - 4 * mm)

# ---------- Anschrift + Kontakt ----------
y = top - logo_w - 12 * mm
text(ML, y, "An den", "LS", 10, GREY)
for i, ln in enumerate(["Kürtener Karnevalsverein von 2012 e.V.", "c/o Peter Adelt",
                        "Hachenberger Weg 11 A", "51515 Kürten"]):
    text(ML, y - (i + 1) * 5 * mm, ln, "LSB" if i == 0 else "LS", 10)

# Kontakt-Kasten rechts
bx, bw, bh = W - MR - 72 * mm, 72 * mm, 24 * mm
c.setFillColor(PURPLE_LIGHT)
c.setStrokeColor(PURPLE_LIGHT)
c.roundRect(bx, y - 18 * mm, bw, bh, 2 * mm, fill=1, stroke=0)
text(bx + 4 * mm, y + 0.5 * mm, "Anzeigenvorlagen und Aufträge bitte an:", "LSB", 9, PURPLE)
text(bx + 4 * mm, y - 5.5 * mm, "peter.adelt@web.de", "LSB", 12, black)
text(bx + 4 * mm, y - 11 * mm, "Farbige und schwarz-weiße Anzeigen", "LS", 8.5, GREY)
text(bx + 4 * mm, y - 15 * mm, "zum gleichen Preis.", "LS", 8.5, GREY)

# ---------- Einleitung ----------
y -= 30 * mm
text(ML, y, "Anzeigen-Auftrag", "LSB", 13, PURPLE)
y -= 7 * mm
intro = ["Hiermit wird eine Anzeige für das Sessionsheft 2026/2027 des Kürtener Karnevalsvereins KKV",
         "in Auftrag gegeben (farbige oder schwarz-weiß-Anzeigen zum gleichen Preis)."]
for ln in intro:
    text(ML, y, ln, "LS", 10)
    y -= 5 * mm

# ---------- Anzeigengröße ----------
y -= 5 * mm
text(ML, y, "Der Auftrag umfasst eine Anzeige der Größe (bitte ankreuzen):", "LSB", 10)
y -= 9 * mm

sizes = [("groesse_1_1", "1/1-Seite", "12,5 x 17,7 cm", "120,- EUR netto"),
         ("groesse_1_2", "1/2-Seite", "12,5 x 8,8 cm", "60,- EUR netto"),
         ("groesse_1_3", "1/3-Seite", "12,5 x 5,8 cm", "45,- EUR netto")]
row_h = 8.5 * mm
for i, (nm, lab, dim, price) in enumerate(sizes):
    ry = y - i * row_h
    if i % 2 == 0:
        c.setFillColor(HexColor("#F8F8F8"))
        c.rect(ML, ry - 3 * mm, CW, row_h, fill=1, stroke=0)
    checkbox(nm, ML + 3 * mm, ry - 1.5 * mm, f"Anzeige {lab}")
    text(ML + 11 * mm, ry, lab, "LSB", 10.5)
    text(ML + 42 * mm, ry, dim, "LS", 10)
    text(W - MR - 4 * mm - c.stringWidth(price, "LSB", 10.5), ry, price, "LSB", 10.5, PURPLE)
y -= 3 * row_h

# ---------- Druckvorlage ----------
y -= 2 * mm
text(ML, y, "Eine Druckvorlage der Anzeige (möglichst PDF-Datei, oder druckfähiger Papierausdruck):", "LSB", 10)
y -= 9 * mm
checkbox("vorlage_liegt_vor", ML + 3 * mm, y - 1.5 * mm, "Druckvorlage liegt vor (früheres Sessionsheft)")
text(ML + 11 * mm, y, "liegt vor (früheres Sessionsheft)", "LS", 10)
y -= 7 * mm
checkbox("vorlage_beigefuegt", ML + 3 * mm, y - 1.5 * mm, "Druckvorlage ist beigefügt / wird per E-Mail übersandt")
text(ML + 11 * mm, y, "ist beigefügt / wird per Email übersandt", "LS", 10)

# ---------- Auftraggeber ----------
y -= 11 * mm
text(ML, y, "Firmenstempel / Name und Anschrift des Auftraggebers:", "LSB", 10)
y -= 4 * mm
fields = [("firma", "Firma / Name"), ("ansprechpartner", "Ansprechpartner/in"),
          ("strasse", "Straße, Hausnummer"), ("plz_ort", "PLZ, Ort"),
          ("email", "E-Mail"), ("telefon", "Telefon")]
lab_w = 38 * mm
fh = 6.8 * mm
gap = 2 * mm
# zweispaltig: links Felder, rechts Stempelfeld
left_w = 100 * mm
for i, (nm, lab) in enumerate(fields):
    fy = y - (i + 1) * (fh + gap)
    text(ML, fy + 2 * mm, lab, "LS", 8.5, GREY)
    textbox(nm, ML + lab_w, fy, left_w - lab_w, fh, tooltip=lab)

stamp_x = ML + left_w + 6 * mm
stamp_w = W - MR - stamp_x
stamp_h = len(fields) * (fh + gap) - gap
stamp_y = y - len(fields) * (fh + gap)
c.setStrokeColor(LINE)
c.setLineWidth(0.6)
c.setDash(2, 2)
c.rect(stamp_x, stamp_y, stamp_w, stamp_h, fill=0, stroke=1)
c.setDash()
text(stamp_x + stamp_w / 2 - c.stringWidth("Firmenstempel", "LS", 8.5) / 2,
     stamp_y + stamp_h / 2 - 1.5 * mm, "Firmenstempel", "LS", 8.5, GREY)
y = stamp_y

# ---------- Datum / Unterschrift ----------
y -= 12 * mm
d_w = 45 * mm
textbox("datum", ML, y, d_w, fh, tooltip="Datum")
sig_x = ML + d_w + 10 * mm
c.setStrokeColor(black)
c.setLineWidth(0.6)
c.line(sig_x, y, W - MR, y)
text(ML, y - 4.5 * mm, "Datum", "LS", 8.5, GREY)
text(sig_x, y - 4.5 * mm, "Unterschrift des Auftraggebers", "LS", 8.5, GREY)

# ---------- Dank ----------
y -= 17 * mm
c.setFillColor(PURPLE)
c.roundRect(ML, y - 5 * mm, CW, 12 * mm, 2 * mm, fill=1, stroke=0)
msg = "Wir danken Ihnen herzlich für die Unterstützung unserer Brauchtumsarbeit!"
text(W / 2 - c.stringWidth(msg, "LSB", 11.5) / 2, y - 1 * mm, msg, "LSB", 11.5, white)

# ---------- Fußzeile ----------
fy = 22 * mm
c.setStrokeColor(LINE)
c.setLineWidth(0.5)
c.line(ML, fy + 3 * mm, W - MR, fy + 3 * mm)
foot = ["Kürtener Karnevalsverein von 2012 e.V. · Vorstand: Peter Adelt, André van Herpt, Lisa Spiegel",
        "Kreissparkasse Köln · IBAN: DE48 3705 0299 0320 5528 30 · BIC: COKSDE33XXX",
        "Volksbank Berg eG · IBAN: DE04 3706 9125 0014 2860 12 · BIC: GENODED1RKO",
        "Finanzamt Bergisch Gladbach, Steuernummer: 204/5834/0477 · Vereinsregister beim Amtsgericht Köln, Blatt VR 17655"]
for i, ln in enumerate(foot):
    text(W / 2 - c.stringWidth(ln, "LS", 7.5) / 2, fy - i * 3.8 * mm, ln, "LS", 7.5, GREY)

c.save()
print("ok", OUT)
