
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
# RAASI_POSITIONS = {f"raasi_{i}": (100 + (i - 1) * 80, 700) for i in range(1, 13)}
# NAVAMSA_POSITIONS = {f"navamsa_{i}": (100 + (i - 1) * 80, 650) for i in range(1, 13)}


# -------------------------
# Raasi & Navamsa positions
# -------------------------
RAASI_POSITIONS = {
    "raasi_1":  (40, 350),
    "raasi_2":  (120, 350),
    "raasi_3":  (200, 350),
    "raasi_4":  (280, 350),
    "raasi_5":  (280, 275),
    "raasi_6":  (280, 200),
    "raasi_7":  (280, 130),
    "raasi_8":  (200, 130),
    "raasi_9":  (120, 130),
    "raasi_10": (40, 130),
    "raasi_11": (40, 270),
    "raasi_12": (40, 200),
}

NAVAMSA_POSITIONS = {
    "navamsa_1":  (380, 350),
    "navamsa_2":  (470, 350),
    "navamsa_3":  (540, 350),
    "navamsa_4":  (620, 350),
    "navamsa_5":  (620, 275),
    "navamsa_6":  (620, 200),
    "navamsa_7":  (620, 130),
    "navamsa_8":  (540, 130),
    "navamsa_9":  (470, 130),
    "navamsa_10": (380, 130),
    "navamsa_11": (380, 270),
    "navamsa_12": (380, 200),
}


# Photo box in points (x1, y1, x2, y2)
PHOTO_BOX = (469, 410, 920, 1041.5)


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


# import io, base64
# from flask import Flask, render_template, request, send_file
# from PyPDF2 import PdfReader, PdfWriter
# from weasyprint import HTML
# from werkzeug.utils import secure_filename
# from reportlab.pdfgen import canvas

# app = Flask(__name__, template_folder="templates-html")
# app.config["UPLOAD_FOLDER"] = "uploads"

# # ✅ Core field positions
# FIELD_POSITIONS = {
#     "register_number": (120, 1100),
#     "introduced_by": (350, 1100),
#     "inam": (580, 1100),
#     "name": (120, 1050),
#     "birth_place": (350, 1050),
#     "dob": (580, 1050),
#     "birth_time": (120, 1000),
#     "star": (350, 1000),
#     "raasi_text": (580, 1000),
#     "height": (120, 950),
#     "colour": (350, 950),
#     "laknam": (580, 950),
#     "education": (120, 900),
#     "work": (350, 900),
#     "monthly_income": (580, 900),
#     "birth_order": (120, 850),
#     "elder_brother": (350, 850),
#     "elder_sister": (580, 850),
#     "younger_brother": (120, 800),
#     "younger_sister": (350, 800),
#     "father_name": (120, 750),
#     "father_occupation": (350, 750),
#     "mother_name": (120, 700),
#     "mother_occupation": (350, 700),
#     "expectation": (120, 650),
#     "house_address": (120, 600),
#     # "gender": (580, 600),
# }

# # ✅ Manual Raasi positions (12 boxes)
# RAASI_POSITIONS = {
#     "raasi_1": (120, 500),
#     "raasi_2": (200, 500),
#     "raasi_3": (280, 500),
#     "raasi_4": (360, 500),
#     "raasi_5": (120, 440),
#     "raasi_6": (200, 440),
#     "raasi_7": (280, 440),
#     "raasi_8": (360, 440),
#     "raasi_9": (120, 380),
#     "raasi_10": (200, 380),
#     "raasi_11": (280, 380),
#     "raasi_12": (360, 380),
# }

# # ✅ Manual Navamsa positions (12 boxes)
# NAVAMSA_POSITIONS = {
#     "navamsa_1": (500, 500),
#     "navamsa_2": (580, 500),
#     "navamsa_3": (660, 500),
#     "navamsa_4": (740, 500),
#     "navamsa_5": (500, 440),
#     "navamsa_6": (580, 440),
#     "navamsa_7": (660, 440),
#     "navamsa_8": (740, 440),
#     "navamsa_9": (500, 380),
#     "navamsa_10": (580, 380),
#     "navamsa_11": (660, 380),
#     "navamsa_12": (740, 380),
# }

# # ✅ Photo box
# PHOTO_BOX = (460, 410, 900, 1080)  # (x1, y1, x2, y2)


# @app.route('/')
# def form():
#     return render_template('form.html')


# @app.route('/generate', methods=['POST'])
# def generate_pdf():
#     form_data = request.form.to_dict()

#     # Handle photo upload
#     photo_data = None
#     if "photo" in request.files and request.files["photo"].filename != "":
#         photo_file = request.files["photo"]
#         filename = secure_filename(photo_file.filename)
#         photo_bytes = photo_file.read()
#         b64_str = base64.b64encode(photo_bytes).decode("utf-8")
#         photo_data = f"data:image/png;base64,{b64_str}"

#     # 1️⃣ Load template PDF
#     template_path = "templates/matrimony_template.pdf"
#     template_pdf = PdfReader(open(template_path, "rb"))
#     first_page = template_pdf.pages[0]
#     width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

#     # 2️⃣ Build overlay HTML
#     selected_gender = form_data.get("gender", "").lower()
#     color = "black"
#     if selected_gender == "male":
#         color = "brown"
#     elif selected_gender == "female":
#         color = "green"

#     html_content = f"""
#     <html>
#     <head>
#         <style>
#             @page {{ size: {width}px {height}px; margin: 0; }}
#             body {{ margin: 0; font-family: 'Latha', sans-serif; }}
#             .field {{
#                 position: absolute;
#                 font-size: 14px;
#                 color: {color};
#             }}
#             .photo {{
#                 position: absolute;
#                 left: {PHOTO_BOX[0]}px;
#                 top: {height - PHOTO_BOX[3]}px;
#                 width: {PHOTO_BOX[2]-PHOTO_BOX[0]}px;
#                 height: {PHOTO_BOX[3]-PHOTO_BOX[1]}px;
#                 object-fit: cover;
#             }}
#         </style>
#     </head>
#     <body>
#     """

#     # 3️⃣ Normal fields
#     for field, (x, y) in FIELD_POSITIONS.items():
#         value = form_data.get(field, "")
#         if value:
#             html_content += f"<div class='field' style='left:{x}px;top:{height-y}px;'>{value}</div>"

#     # 4️⃣ Raasi + Navamsa
#     for field, (x, y) in {**RAASI_POSITIONS, **NAVAMSA_POSITIONS}.items():
#         value = form_data.get(field, "")
#         if value:
#             html_content += f"<div class='field' style='left:{x}px;top:{height-y}px;'>{value}</div>"

#     # 5️⃣ Photo
#     if photo_data:
#         html_content += f"<img src='{photo_data}' class='photo'/>"

#     html_content += "</body></html>"

#     # 6️⃣ Render overlay
#     overlay_stream = io.BytesIO()
#     HTML(string=html_content).write_pdf(overlay_stream)
#     overlay_stream.seek(0)
#     overlay_pdf = PdfReader(overlay_stream)

#     # 7️⃣ Merge
#     writer = PdfWriter()
#     page0 = template_pdf.pages[0]
#     page0.merge_page(overlay_pdf.pages[0])
#     writer.add_page(page0)

#     for p in template_pdf.pages[1:]:
#         writer.add_page(p)

#     # 8️⃣ Return
#     out_stream = io.BytesIO()
#     writer.write(out_stream)
#     out_stream.seek(0)

#     return send_file(out_stream,
#                      as_attachment=True,
#                      download_name="matrimony_filled.pdf",
#                      mimetype="application/pdf")


# # ✅ Debug grid with field markers
# @app.route('/debug_grid')
# def debug_grid():
#     template_path = "templates/matrimony_template.pdf"
#     template_pdf = PdfReader(open(template_path, "rb"))
#     first_page = template_pdf.pages[0]
#     width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(width, height))

#     step = 50  # grid step size
#     can.setStrokeColorRGB(0.8, 0.8, 0.8)
#     can.setFont("Helvetica", 6)

#     # Grid
#     for x in range(0, int(width), step):
#         can.line(x, 0, x, height)
#         can.drawString(x + 2, height - 10, str(x))

#     for y in range(0, int(height), step):
#         can.line(0, y, width, y)
#         can.drawString(2, y + 2, str(y))

#     # Field markers
#     all_fields = {**FIELD_POSITIONS, **RAASI_POSITIONS, **NAVAMSA_POSITIONS}
#     can.setFillColorRGB(1, 0, 0)  # red markers
#     for fid, (x, y) in all_fields.items():
#         can.circle(x, y, 3, fill=1)
#         can.drawString(x + 5, y + 5, fid)

#     can.save()
#     packet.seek(0)

#     overlay_pdf = PdfReader(packet)
#     writer = PdfWriter()

#     page0 = template_pdf.pages[0]
#     page0.merge_page(overlay_pdf.pages[0])
#     writer.add_page(page0)

#     for p in template_pdf.pages[1:]:
#         writer.add_page(p)

#     out_stream = io.BytesIO()
#     writer.write(out_stream)
#     out_stream.seek(0)

#     return send_file(out_stream,
#                      as_attachment=True,
#                      download_name="debug_grid.pdf",
#                      mimetype="application/pdf")


# if __name__ == "__main__":
#     app.run(debug=True)
