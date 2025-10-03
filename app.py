


import io, base64, os, html, json, re
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
    "elder_brother":     (110, 617),
    "elder_sister":      (230, 617),
    "younger_brother":   (330, 617),
    "younger_sister":    (430, 617),
    "father_name":       (140, 582),
    "father_occupation": (160, 550),
    "mother_name":       (130, 514),
    "mother_occupation": (140, 480),
    "expectation":       (140, 440),
    "house_address":     (400, 401),
    "addition_info":     (480, 1070),
    "rentalhouse":       (10, 400),
    "lease":             (100, 400),
    "ownhouse":          (180, 400),
}

RAASI_POSITIONS = {
    "raasi_1":  (20, 350),  "raasi_2":  (90, 350),  "raasi_3":  (180, 350),
    "raasi_4":  (260, 350), "raasi_5":  (260, 275), "raasi_6":  (260, 200),
    "raasi_7":  (260, 140), "raasi_8":  (180, 140), "raasi_9":  (100, 140),
    "raasi_10": (20, 140),  "raasi_11": (20, 200),  "raasi_12": (20, 270),
}
NAVAMSA_POSITIONS = {
    "navamsa_1":  (360, 350), "navamsa_2":  (435, 350), "navamsa_3":  (510, 350),
    "navamsa_4":  (590, 350), "navamsa_5":  (590, 275), "navamsa_6":  (590, 200),
    "navamsa_7":  (590, 140), "navamsa_8":  (435, 140), "navamsa_9":  (510, 140),
    "navamsa_10": (360, 140), "navamsa_11": (360, 200), "navamsa_12": (360, 270),
}

PHOTO_BOX = (469, 410, 920, 1041.5)
# -------------------------
# Metadata helpers
# -------------------------
def save_pdf_with_metadata(pdf_stream, form_data):
    reader = PdfReader(pdf_stream)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.add_metadata({
        "/FormData": json.dumps(form_data, ensure_ascii=False)
    })
    out = io.BytesIO()
    writer.write(out)
    out.seek(0)
    return out


def extract_form_data_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    metadata = reader.metadata
    if metadata and "/FormData" in metadata:
        try:
            return json.loads(metadata["/FormData"])
        except Exception:
            return {}
    return {}

# -------------------------
# Text helpers (Tamil detection + mixed runs)
# -------------------------
def contains_tamil(s: str) -> bool:
    return bool(s) and any("\u0B80" <= ch <= "\u0BFF" for ch in s)

_tamil_split_re = re.compile(r'[\u0B80-\u0BFF]+|[^\u0B80-\u0BFF]+')

def split_into_runs(s: str):
    if not s:
        return []
    return _tamil_split_re.findall(s)

def render_mixed_html(value: str, eng_style: str, tam_style: str) -> str:
    parts = split_into_runs(value)
    out = []
    for part in parts:
        esc = html.escape(part)
        if contains_tamil(part):
            out.append(f"<span style=\"{tam_style}\">{esc}</span>")
        else:
            out.append(f"<span style=\"{eng_style}\">{esc}</span>")
    return "".join(out)

# -------------------------
# Routes
# -------------------------
@app.route("/", methods=["GET", "POST"])
def form():
    form_data = {}

    if request.method == "POST":
        # Case 1: User uploaded PDF to edit
        if "pdf" in request.files and request.files["pdf"].filename != "":
            pdf_file = request.files["pdf"]
            form_data = extract_form_data_from_pdf(pdf_file)
            return render_template("form.html", form_data=form_data)

        # Case 2: User submitted form to generate PDF
        form_data = request.form.to_dict()

        # Handle photo upload
        photo_data = None
        if "photo" in request.files and request.files["photo"].filename != "":
            photo_file = request.files["photo"]
            filename = secure_filename(photo_file.filename)
            photo_bytes = photo_file.read()
            b64_str = base64.b64encode(photo_bytes).decode("utf-8")
            ext = os.path.splitext(filename)[1].lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            photo_data = f"data:{mime};base64,{b64_str}"

        # Load template PDF (adjust filename if yours is different)
        template_path = "templates/matrimony.pdf"
        template_pdf = PdfReader(open(template_path, "rb"))
        first_page = template_pdf.pages[0]
        width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

        # Decide color based on gender
        gender = form_data.get("gender", "").lower()
        if gender == "male":
            color = "rgb(168, 0, 0)"
        elif gender == "female":
            color = "rgb(0, 170, 0)"
        else:
            color = "#000000"

        # Font files (Latha regular + bold) - ensure these files exist in fonts/
        latha_regular = f"file://{os.path.join(app.root_path, 'fonts', 'Latha.ttf')}"
        latha_bold = f"file://{os.path.join(app.root_path, 'fonts', 'Latha-Bold.ttf')}"

        # Build overlay HTML
        html_content = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{ size: {width}pt {height}pt; margin: 0; }}

  @font-face {{
    font-family: 'Latha';
    src: url('{latha_regular}') format('truetype');
    font-weight: normal;
    font-style: normal;
  }}
  @font-face {{
    font-family: 'Latha';
    src: url('{latha_bold}') format('truetype');
    font-weight: bold;
    font-style: normal;
  }}

  html, body {{
    margin: 0;
    padding: 0;
    width: {width}pt;
    height: {height}pt;
    font-family: 'Latha', sans-serif;
    /* don't force bold globally here */
  }}

  .field {{
    position: absolute;
    white-space: pre-wrap;
    word-wrap: break-word;
    /* color and weight applied per-span via render_mixed_html */
  }}

  .photo {{
    position: absolute;
    object-fit: contain;
    background-color: white;
  }}
</style>
</head>
<body>
"""

        # Inline styles for main fields and raasi/navamsa (include color where relevant)
        # Use medium weight (500) to reduce the heavy "bold" look; change to 400 if you want lighter.
        eng_style_main = f"font-family:Arial, sans-serif; font-size:17pt; font-weight:500; color:{color}; line-height:1;"
        tam_style_main = f"font-family:Latha, sans-serif; font-size:15pt; font-weight:500; color:{color}; line-height:1;"

        # Raasi/Navamsa styles (smaller)
        eng_style_raasi = f"font-family:Arial, sans-serif; font-size:14pt; font-weight:500; color:{color}; line-height:1.15;"
        tam_style_raasi = f"font-family:Latha, sans-serif; font-size:14pt; font-weight:500; color:{color}; line-height:1.15;"

        # --- Main Fields ---
        for field, (x, y) in FIELD_POSITIONS.items():
            value = form_data.get(field, "")
            if value:
                left = x
                top = height - y
                safe_html = render_mixed_html(value, eng_style_main, tam_style_main)
                html_content += (
                    f"<div class='field' style='left:{left}pt; top:{top}pt;'>"
                    f"{safe_html}</div>\n"
                )

        # --- Raasi + Navamsa (fixed & unindented correctly) ---
        for dct in (RAASI_POSITIONS, NAVAMSA_POSITIONS):
            for field, (x, y) in dct.items():
                value = form_data.get(field, "")
                if not value:
                    continue

                left = x
                top = height - y

                # Split the ORIGINAL value into logical lines entered by the user
                lines = value.splitlines()
                if not lines:
                    lines = [""]

                # For each line produce mixed-span HTML (Tamil vs ASCII), preserving inline styles including color & weight
                rendered_lines = [render_mixed_html(line, eng_style_raasi, tam_style_raasi) for line in lines]

                # Wrap each rendered line in a block-level wrapper so flex stacks them correctly.
                line_blocks = "".join([f"<div style='display:block; width:100%;'>{ln or '&nbsp;'}</div>" for ln in rendered_lines])

                # Container: column flex centers vertically+horizontally; each line-block is stacked vertically.
                html_content += (
                    f"<div style='position:absolute; left:{left}pt; top:{top}pt; "
                    f"width:60pt; min-height:30pt; display:flex; flex-direction:column; "
                    f"align-items:center; justify-content:center; text-align:center; "
                    f"line-height:1.15; white-space:normal; word-break:normal; overflow:hidden;'>"
                    f"{line_blocks}</div>\n"
                )

        # --- Photo ---
        if photo_data:
            x1, y1, x2, y2 = PHOTO_BOX
            box_w = x2 - x1
            box_h = y2 - y1
            left = x1
            top = height - y2
            html_content += (
                f"<img src='{photo_data}' class='photo' "
                f"style='left:{left}pt; top:{top}pt; width:{box_w}pt; height:{box_h}pt;'/>"
            )

        html_content += "</body></html>"

        # Render overlay PDF with WeasyPrint
        overlay_stream = io.BytesIO()
        HTML(string=html_content).write_pdf(overlay_stream)
        overlay_stream.seek(0)
        overlay_pdf = PdfReader(overlay_stream)

        # Merge overlay into template
        writer = PdfWriter()
        page0 = template_pdf.pages[0]
        page0.merge_page(overlay_pdf.pages[0])
        writer.add_page(page0)
        for p in template_pdf.pages[1:]:
            writer.add_page(p)

        # Save with metadata and return
        final_pdf = io.BytesIO()
        writer.write(final_pdf)
        final_pdf.seek(0)
        final_pdf = save_pdf_with_metadata(final_pdf, form_data)

        return send_file(final_pdf, as_attachment=True, download_name="matrimony_filled.pdf", mimetype="application/pdf")

    # GET: render empty form
    return render_template("form.html", form_data={})


if __name__ == "__main__":
    app.run(debug=True)
