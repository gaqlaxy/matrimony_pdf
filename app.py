
import io, base64, os
from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from weasyprint import HTML
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas

app = Flask(__name__, template_folder="templates-html")
app.config["UPLOAD_FOLDER"] = "uploads"

# -------------------------
# Field positions (POINTS)
# -------------------------
FIELD_POSITIONS = {
    "register_number":   (110, 1065),
    "introduced_by":     (350, 1065),
    "inam":              (80, 1030),
    "name":              (80, 1000),
    "birth_place":       (110, 955),
    "dob":               (120, 915),
    "birth_time":        (350, 915),

    "star":              (110, 868),
    "raasi_text":        (340, 868),
    "height":            (90, 826),
    "colour":            (210, 826),

    "laknam":            (380, 826),
    "education":         (80, 790),
    "work":              (100, 758),
    "monthly_income":    (150, 659),

    "birth_order":       (400, 659),
    "elder_brother":     (100, 617),
    "elder_sister":      (230, 617),
    "younger_brother":   (330, 617),
    "younger_sister":    (430, 617),

    "father_name":       (140, 582),
    "father_occupation": (160, 550),
    "mother_name":       (130, 514),
    "mother_occupation": (140, 480),

    "expectation":       (140, 440),
    "house_address":     (400, 401),

    # keep gender if you want it printed somewhere
    "gender":            (120, 1175),
}

# Raasi & Navamsa (example positions in points; tune with /debug_grid)
RAASI_POSITIONS = {f"raasi_{i}": (100 + (i - 1) * 80, 700) for i in range(1, 13)}
NAVAMSA_POSITIONS = {f"navamsa_{i}": (100 + (i - 1) * 80, 650) for i in range(1, 13)}

# Photo box in points (x1, y1, x2, y2)
PHOTO_BOX = (460, 410, 900, 1080)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/generate', methods=['POST'])
def generate_pdf():
    form_data = request.form.to_dict()

    # Handle photo upload
    photo_data = None
    if "photo" in request.files and request.files["photo"].filename != "":
        photo_file = request.files["photo"]
        filename = secure_filename(photo_file.filename)
        photo_bytes = photo_file.read()
        b64_str = base64.b64encode(photo_bytes).decode("utf-8")
        # Try to detect mime-type by filename ext (png/jpg)
        ext = os.path.splitext(filename)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        photo_data = f"data:{mime};base64,{b64_str}"

    # Load template PDF
    template_path = "templates/matrimony_template.pdf"
    template_pdf = PdfReader(open(template_path, "rb"))
    first_page = template_pdf.pages[0]
    # width/height in PDF POINTS (1pt = 1/72in)
    width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

    # Decide global color based on gender
    selected_gender = form_data.get("gender", "").lower()
    if selected_gender == "male":
        color = "#8B4513"  # brown
    elif selected_gender == "female":
        color = "#228B22"  # green
    else:
        color = "#000000"  # black

    # Build overlay HTML using PT units to match PDF points
    # Use file:// path for local font Latha.ttf (must be in fonts/ and committed)
    latha_path = f"file://{os.path.join(app.root_path, 'fonts', 'Latha.ttf')}"
    html_content = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{ size: {width}pt {height}pt; margin: 0; }}
  @font-face {{
    font-family: 'Latha';
    src: url('{latha_path}') format('truetype');
  }}
  html, body {{
    margin: 0;
    padding: 0;
    width: {width}pt;
    height: {height}pt;
    font-family: 'Latha', sans-serif;
    font-size: 14pt;
  }}
  .field {{
    position: absolute;
    white-space: pre-wrap;
    word-wrap: break-word;
    color: {color};
    font-family: 'Latha', sans-serif;
  }}
  .photo {{
    position: absolute;
    object-fit: cover;
  }}
</style>
</head>
<body>
"""

    # Add regular fields (position in POINTS; top from top = height - y)
    for field, (x, y) in FIELD_POSITIONS.items():
        value = form_data.get(field, "")
        if value:
            left = x
            top = height - y
            # use pt units so positions match PDF points exactly
            html_content += f"<div class='field' style='left:{left}pt; top:{top}pt; font-size:12pt;'>{value}</div>\n"

    # Add raasi & navamsa
    for dct in (RAASI_POSITIONS, NAVAMSA_POSITIONS):
        for field, (x, y) in dct.items():
            value = form_data.get(field, "")
            if value:
                left = x
                top = height - y
                html_content += f"<div class='field' style='left:{left}pt; top:{top}pt; font-size:10pt; text-align:center;'>{value}</div>\n"

    # Photo (use pt units for width/height)
    if photo_data:
        x1, y1, x2, y2 = PHOTO_BOX
        box_w = x2 - x1
        box_h = y2 - y1
        left = x1
        top = height - y2  # top CSS coordinate
        html_content += (
            f"<img src='{photo_data}' class='photo' "
            f"style='left:{left}pt; top:{top}pt; width:{box_w}pt; height:{box_h}pt;'/>"
        )

    html_content += "</body></html>"

    # Render overlay with WeasyPrint (overlay_stream is PDF)
    overlay_stream = io.BytesIO()
    HTML(string=html_content).write_pdf(overlay_stream)
    overlay_stream.seek(0)
    overlay_pdf = PdfReader(overlay_stream)

    # Merge overlay page 0 into template page 0
    writer = PdfWriter()
    page0 = template_pdf.pages[0]
    page0.merge_page(overlay_pdf.pages[0])
    writer.add_page(page0)

    # add rest pages unchanged
    for p in template_pdf.pages[1:]:
        writer.add_page(p)

    # return combined pdf
    out_stream = io.BytesIO()
    writer.write(out_stream)
    out_stream.seek(0)
    return send_file(out_stream,
                     as_attachment=True,
                     download_name="matrimony_filled.pdf",
                     mimetype="application/pdf")


# Debug grid generator (ReportLab) — still useful and matches point coords
@app.route('/debug_grid')
def debug_grid():
    template_path = "templates/matrimony_template.pdf"
    template_pdf = PdfReader(open(template_path, "rb"))
    first_page = template_pdf.pages[0]
    width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))

    step = 50
    can.setStrokeColorRGB(0.8, 0.8, 0.8)
    can.setFont("Helvetica", 6)

    for x in range(0, int(width)+1, step):
        can.line(x, 0, x, height)
        can.drawString(x + 2, height - 10, str(x))

    for y in range(0, int(height)+1, step):
        can.line(0, y, width, y)
        can.drawString(2, y + 2, str(y))

    can.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    writer = PdfWriter()

    page0 = template_pdf.pages[0]
    page0.merge_page(overlay_pdf.pages[0])
    writer.add_page(page0)

    for p in template_pdf.pages[1:]:
        writer.add_page(p)

    out_stream = io.BytesIO()
    writer.write(out_stream)
    out_stream.seek(0)

    return send_file(out_stream,
                     as_attachment=True,
                     download_name="debug_grid.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)
