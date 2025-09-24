
# import io, base64, os
# from flask import Flask, render_template, request, send_file
# from PyPDF2 import PdfReader, PdfWriter
# from weasyprint import HTML
# from werkzeug.utils import secure_filename
# from reportlab.pdfgen import canvas

# app = Flask(__name__, template_folder="templates-html")
# app.config["UPLOAD_FOLDER"] = "uploads"

# # -------------------------
# # Field positions (POINTS)
# # -------------------------
# FIELD_POSITIONS = {
#     "register_number":   (110, 1065),
#     "introduced_by":     (350, 1065),
#     "inam":              (80, 1030),
#     "name":              (80, 1000),
#     "birth_place":       (110, 955),
#     "dob":               (120, 915),
#     "birth_time":        (350, 915),

#     "star":              (110, 868),
#     "raasi_text":        (340, 868),
#     "height":            (90, 826),
#     "colour":            (210, 826),

#     "laknam":            (380, 826),
#     "education":         (80, 790),
#     "work":              (100, 758),
#     "monthly_income":    (150, 659),

#     "birth_order":       (400, 659),
#     "elder_brother":     (100, 617),
#     "elder_sister":      (230, 617),
#     "younger_brother":   (330, 617),
#     "younger_sister":    (430, 617),

#     "father_name":       (140, 582),
#     "father_occupation": (160, 550),
#     "mother_name":       (130, 514),
#     "mother_occupation": (140, 480),

#     "expectation":       (140, 440),
#     "house_address":     (400, 401),
#     "addition_info":     (480, 1070),

#     # keep gender if you want it printed somewhere
#     "gender":            (120, 1175),
# }

# # Raasi & Navamsa (example positions in points; tune with /debug_grid)
# # RAASI_POSITIONS = {f"raasi_{i}": (100 + (i - 1) * 80, 700) for i in range(1, 13)}
# # NAVAMSA_POSITIONS = {f"navamsa_{i}": (100 + (i - 1) * 80, 650) for i in range(1, 13)}


# # -------------------------
# # Raasi & Navamsa positions
# # -------------------------
# RAASI_POSITIONS = {
#     "raasi_1":  (20, 350),
#     "raasi_2":  (90, 350),
#     "raasi_3":  (180, 350),
#     "raasi_4":  (260, 350),
#     "raasi_5":  (260, 275),
#     "raasi_6":  (260, 200),
#     "raasi_7":  (260, 130),
#     "raasi_8":  (180, 130),
#     "raasi_9":  (100, 130),
#     "raasi_10": (20, 130),
#     "raasi_11": (20, 270),
#     "raasi_12": (20, 200),
# }

# NAVAMSA_POSITIONS = {
#     "navamsa_1":  (360, 350),
#     "navamsa_2":  (435, 350),
#     "navamsa_3":  (510, 350),
#     "navamsa_4":  (590, 350),
#     "navamsa_5":  (590, 275),
#     "navamsa_6":  (590, 200),
#     "navamsa_7":  (590, 130),
#     "navamsa_8":  (435, 130),
#     "navamsa_9":  (510, 130),
#     "navamsa_10": (360, 130),
#     "navamsa_11": (360, 270),
#     "navamsa_12": (360, 200),
# }


# # Photo box in points (x1, y1, x2, y2)
# PHOTO_BOX = (469, 410, 920, 1041.5)


# @app.route('/')
# def form():
#     return render_template('form.html')


# # @app.route('/generate', methods=['POST'])
# # def generate_pdf():
# #     form_data = request.form.to_dict()

# #     # Handle photo upload
# #     photo_data = None
# #     if "photo" in request.files and request.files["photo"].filename != "":
# #         photo_file = request.files["photo"]
# #         filename = secure_filename(photo_file.filename)
# #         photo_bytes = photo_file.read()
# #         b64_str = base64.b64encode(photo_bytes).decode("utf-8")
# #         # Try to detect mime-type by filename ext (png/jpg)
# #         ext = os.path.splitext(filename)[1].lower()
# #         mime = "image/png" if ext == ".png" else "image/jpeg"
# #         photo_data = f"data:{mime};base64,{b64_str}"

# #     # Load template PDF
# #     template_path = "templates/matrimony_template.pdf"
# #     template_pdf = PdfReader(open(template_path, "rb"))
# #     first_page = template_pdf.pages[0]
# #     # width/height in PDF POINTS (1pt = 1/72in)
# #     width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

# #     # Decide global color based on gender
# #     selected_gender = form_data.get("gender", "").lower()
# #     if selected_gender == "male":
# #         # color = "#8B4513"  # brown
# #         color = "rgb(168, 0, 0)"
# #     elif selected_gender == "female":
# #         # color = "#228B22"  # green
# #         color = "rgb(0, 170, 0)"

# #     else:
# #         color = "#000000"  # black

# #     # Build overlay HTML using PT units to match PDF points
# #     # Use file:// path for local font Latha.ttf (must be in fonts/ and committed)
# #     latha_path = f"file://{os.path.join(app.root_path, 'fonts', 'Latha.ttf')}"
# #     html_content = f"""<!doctype html>
# # <html>
# # <head>
# # <meta charset="utf-8">
# # <style>
# #   @page {{ size: {width}pt {height}pt; margin: 0; }}
# #   @font-face {{
# #     font-family: 'Latha';
# #     src: url('{latha_path}') format('truetype');
# #   }}
# #   html, body {{
# #     margin: 0;
# #     padding: 0;
# #     width: {width}pt;
# #     height: {height}pt;
# #     font-family: 'Latha', sans-serif;
# #     font-size: 14pt;
# #   }}
# #   .field {{
# #     position: absolute;
# #     white-space: pre-wrap;
# #     word-wrap: break-word;
# #     color: {color};
# #     font-family: 'Latha', sans-serif;
# #   }}
# #   .photo {{
# #     position: absolute;
    
# #     object-fit: contain;
# # background-color: white;
# #   }}
# # </style>
# # </head>
# # <body>
# # """

# #     # Add regular fields (position in POINTS; top from top = height - y)
# #     for field, (x, y) in FIELD_POSITIONS.items():
# #         value = form_data.get(field, "")
# #         if value:
# #             left = x
# #             top = height - y
# #             # use pt units so positions match PDF points exactly
# #             html_content += f"<div class='field' style='left:{left}pt; top:{top}pt; font-size:14pt;'>{value}</div>\n"
    
# #     # Add raasi & navamsa
# #     for dct in (RAASI_POSITIONS, NAVAMSA_POSITIONS):
# #         for field, (x, y) in dct.items():
# #             value = form_data.get(field, "")
# #             if value:
# #                 left = x
# #                 top = height - y
# #                 html_content += f"<div class='field' style='left:{left}pt; top:{top}pt; font-size:10pt; text-align:center; width:60pt; white-space:pre-wrap;'>{value}</div>\n"

# #     # Photo (use pt units for width/height)
# #     if photo_data:
# #         x1, y1, x2, y2 = PHOTO_BOX
# #         box_w = x2 - x1
# #         box_h = y2 - y1
# #         left = x1
# #         top = height - y2  # top CSS coordinate
# #         html_content += (
# #             f"<img src='{photo_data}' class='photo' "
# #             f"style='left:{left}pt; top:{top}pt; width:{box_w}pt; height:{box_h}pt;'/>"
# #         )

# #     html_content += "</body></html>"

# #     # Render overlay with WeasyPrint (overlay_stream is PDF)
# #     overlay_stream = io.BytesIO()
# #     HTML(string=html_content).write_pdf(overlay_stream)
# #     overlay_stream.seek(0)
# #     overlay_pdf = PdfReader(overlay_stream)

# #     # Merge overlay page 0 into template page 0
# #     writer = PdfWriter()
# #     page0 = template_pdf.pages[0]
# #     page0.merge_page(overlay_pdf.pages[0])
# #     writer.add_page(page0)

# #     # add rest pages unchanged
# #     for p in template_pdf.pages[1:]:
# #         writer.add_page(p)

# #     # return combined pdf
# #     out_stream = io.BytesIO()
# #     writer.write(out_stream)
# #     out_stream.seek(0)
# #     return send_file(out_stream,
# #                      as_attachment=True,
# #                      download_name="matrimony_filled.pdf",
# #                      mimetype="application/pdf")
# @app.route('/generate', methods=['POST'])
# def generate_pdf():
#     import html  # ensure imported
#     form_data = request.form.to_dict()

#     # Handle photo upload
#     photo_data = None
#     if "photo" in request.files and request.files["photo"].filename != "":
#         photo_file = request.files["photo"]
#         filename = secure_filename(photo_file.filename)
#         photo_bytes = photo_file.read()
#         b64_str = base64.b64encode(photo_bytes).decode("utf-8")
#         # detect mime-type
#         ext = os.path.splitext(filename)[1].lower()
#         mime = "image/png" if ext == ".png" else "image/jpeg"
#         photo_data = f"data:{mime};base64,{b64_str}"

#     # Load template PDF
#     template_path = "templates/matrimony_template.pdf"
#     template_pdf = PdfReader(open(template_path, "rb"))
#     first_page = template_pdf.pages[0]
#     width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

#     # Decide global color based on gender
#     selected_gender = form_data.get("gender", "").lower()
#     if selected_gender == "male":
#         color = "rgb(168, 0, 0)"
#     elif selected_gender == "female":
#         color = "rgb(0, 170, 0)"
#     else:
#         color = "#000000"

#     # Font path
#     latha_path = f"file://{os.path.join(app.root_path, 'fonts', 'Latha.ttf')}"

#     # Build overlay HTML
#     html_content = f"""<!doctype html>
# <html>
# <head>
# <meta charset="utf-8">
# <style>
#   @page {{ size: {width}pt {height}pt; margin: 0; }}
#   @font-face {{
#     font-family: 'Latha';
#     src: url('{latha_path}') format('truetype');
#   }}
#   html, body {{
#     margin: 0;
#     padding: 0;
#     width: {width}pt;
#     height: {height}pt;
#     font-family: 'Latha', sans-serif;
#   }}
#   .field {{
#     position: absolute;
#     white-space: pre-wrap;
#     word-wrap: break-word;
#     color: {color};
#   }}
#   .photo {{
#     position: absolute;
#     object-fit: contain;
#     background-color: white;
#   }}
# </style>
# </head>
# <body>
# """

#     # Add FIELD_POSITIONS with Option 1 font logic
#     for field, (x, y) in FIELD_POSITIONS.items():
#         value = form_data.get(field, "")
#         if value:
#             left = x
#             top = height - y
#             if value.isascii():
#                 font_family = "Arial, sans-serif"
#                 font_size = "15pt"
#             else:
#                 font_family = "'Latha', sans-serif"
#                 font_size = "15pt"
#             safe_value = html.escape(value)
#             html_content += (
#                 f"<div class='field' style='left:{left}pt; top:{top}pt; "
#                 f"font-family:{font_family}; font-size:{font_size};'>{safe_value}</div>\n"
#             )

#     # Add RAASI / NAVAMSA fields
#     for dct in (RAASI_POSITIONS, NAVAMSA_POSITIONS):
#         for field, (x, y) in dct.items():
#             value = form_data.get(field, "")
#             if value:
#                 left = x
#                 top = height - y
#                 if value.isascii():
#                     font_family = "Arial, sans-serif"
#                     font_size = "11pt"
#                 else:
#                     font_family = "'Latha', sans-serif"
#                     font_size = "10pt"
#                 safe_value = html.escape(value)
#                 html_content += (
#                     f"<div class='field' style='left:{left}pt; top:{top}pt; "
#                     f"font-family:{font_family}; font-size:{font_size}; "
#                     f"text-align:center; width:60pt; white-space:pre-wrap; word-break:break-word;'>"
#                     f"{safe_value}</div>\n"
#                 )
  

#     # Add photo
#     if photo_data:
#         x1, y1, x2, y2 = PHOTO_BOX
#         box_w = x2 - x1
#         box_h = y2 - y1
#         left = x1
#         top = height - y2
#         html_content += (
#             f"<img src='{photo_data}' class='photo' "
#             f"style='left:{left}pt; top:{top}pt; width:{box_w}pt; height:{box_h}pt;'/>"
#         )

#     html_content += "</body></html>"

#     # Render overlay PDF
#     overlay_stream = io.BytesIO()
#     HTML(string=html_content).write_pdf(overlay_stream)
#     overlay_stream.seek(0)
#     overlay_pdf = PdfReader(overlay_stream)

#     # Merge overlay
#     writer = PdfWriter()
#     page0 = template_pdf.pages[0]
#     page0.merge_page(overlay_pdf.pages[0])
#     writer.add_page(page0)

#     # Add remaining pages
#     for p in template_pdf.pages[1:]:
#         writer.add_page(p)

#     out_stream = io.BytesIO()
#     writer.write(out_stream)
#     out_stream.seek(0)

#     return send_file(
#         out_stream,
#         as_attachment=True,
#         download_name="matrimony_filled.pdf",
#         mimetype="application/pdf"
#     )


# # Debug grid generator (ReportLab) — still useful and matches point coords
# @app.route('/debug_fields')
# def debug_fields():
#     template_path = "templates/matrimony_template.pdf"
#     template_pdf = PdfReader(open(template_path, "rb"))
#     first_page = template_pdf.pages[0]
#     width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(width, height))

#     # helper function
#     def draw_marker(x, y, label, color=(1, 0, 0)):
#         box_w, box_h = 120, 20  # adjust per your needs
#         can.setFillColorRGB(*color, alpha=0.3)
#         can.rect(x, y - box_h, box_w, box_h, fill=True, stroke=False)
#         can.setFillColorRGB(0, 0, 0)
#         can.setFont("Helvetica", 8)
#         can.drawString(x + 2, y - 10, label)

#     # mark FIELD_POSITIONS
#     for field, (x, y) in FIELD_POSITIONS.items():
#         draw_marker(x, y, field, color=(1, 0, 0))

#     # mark RAASI
#     for field, (x, y) in RAASI_POSITIONS.items():
#         draw_marker(x, y, field, color=(0, 0, 1))

#     # mark NAVAMSA
#     for field, (x, y) in NAVAMSA_POSITIONS.items():
#         draw_marker(x, y, field, color=(0, 0.6, 0))

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
#                      download_name="debug_fields.pdf",
#                      mimetype="application/pdf")

# # @app.route('/debug_grid')
# # def debug_grid():
# #     template_path = "templates/matrimony_template.pdf"
# #     template_pdf = PdfReader(open(template_path, "rb"))
# #     first_page = template_pdf.pages[0]
# #     width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

# #     packet = io.BytesIO()
# #     can = canvas.Canvas(packet, pagesize=(width, height))

# #     step = 50
# #     can.setStrokeColorRGB(0.8, 0.8, 0.8)
# #     can.setFont("Helvetica", 6)

# #     for x in range(0, int(width)+1, step):
# #         can.line(x, 0, x, height)
# #         can.drawString(x + 2, height - 10, str(x))

# #     for y in range(0, int(height)+1, step):
# #         can.line(0, y, width, y)
# #         can.drawString(2, y + 2, str(y))

# #     can.save()
# #     packet.seek(0)

# #     overlay_pdf = PdfReader(packet)
# #     writer = PdfWriter()

# #     page0 = template_pdf.pages[0]
# #     page0.merge_page(overlay_pdf.pages[0])
# #     writer.add_page(page0)

# #     for p in template_pdf.pages[1:]:
# #         writer.add_page(p)

# #     out_stream = io.BytesIO()
# #     writer.write(out_stream)
# #     out_stream.seek(0)

# #     return send_file(out_stream,
# #                      as_attachment=True,
# #                      download_name="debug_grid.pdf",
# #                      mimetype="application/pdf")


# if __name__ == "__main__":
#     app.run(debug=True)





import io, base64, os, html, json
from flask import Flask, render_template, request, send_file, redirect, url_for

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
    "addition_info":     (480, 1070),
    "rentalhouse":       (10, 400),
    "lease":             (100, 400),
    "ownhouse":          (180, 400),
    
    # "gender":            (120, 1175),
}

# Raasi & Navamsa positions
RAASI_POSITIONS = {
    "raasi_1":  (20, 350),  "raasi_2":  (90, 350),  "raasi_3":  (180, 350),
    "raasi_4":  (260, 350), "raasi_5":  (260, 275), "raasi_6":  (260, 200),
    "raasi_7":  (260, 140), "raasi_8":  (180, 140), "raasi_9":  (100, 140),
    "raasi_10": (20, 140),  "raasi_11": (20, 270),  "raasi_12": (20, 200),
}
NAVAMSA_POSITIONS = {
    "navamsa_1":  (360, 350), "navamsa_2":  (435, 350), "navamsa_3":  (510, 350),
    "navamsa_4":  (590, 350), "navamsa_5":  (590, 275), "navamsa_6":  (590, 200),
    "navamsa_7":  (590, 140), "navamsa_8":  (435, 140), "navamsa_9":  (510, 140),
    "navamsa_10": (360, 140), "navamsa_11": (360, 270), "navamsa_12": (360, 200),
}

# Photo box in points (x1, y1, x2, y2)
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

        # Load template PDF
        template_path = "templates/matrimony_template.pdf"
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

        # Font path
        latha_path = f"file://{os.path.join(app.root_path, 'fonts', 'Latha.ttf')}"

        # Build overlay HTML
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
  }}
  .field {{
    position: absolute;
    white-space: pre-wrap;
    word-wrap: break-word;
    color: {color};
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

        # Add fields
        for field, (x, y) in FIELD_POSITIONS.items():
            value = form_data.get(field, "")
            if value:
                left = x
                top = height - y
                font_family = "Arial, sans-serif" if value.isascii() else "'Latha', sans-serif"
                font_size = "15pt"
                safe_value = html.escape(value)
                html_content += (
                    f"<div class='field' style='left:{left}pt; top:{top}pt; "
                    f"font-family:{font_family}; font-size:{font_size};'>{safe_value}</div>\n"
                )

        # Add Raasi + Navamsa
        for dct in (RAASI_POSITIONS, NAVAMSA_POSITIONS):
            for field, (x, y) in dct.items():
                value = form_data.get(field, "")
                if value:
                    left = x
                    top = height - y
                    font_family = "Arial, sans-serif" if value.isascii() else "'Latha', sans-serif"
                    font_size = "9pt" if value.isascii() else "8pt"
                    safe_value = html.escape(value)
                    # html_content += (
                    #     f"<div class='field' style='left:{left}pt; top:{top}pt; "
                    #     f"font-family:{font_family}; font-size:{font_size}; "
                    #     f"text-align:center; width:60pt; white-space:pre-wrap; word-break:break-word;'>"
                    #     f"{safe_value}</div>\n"
                    # )
                    html_content += (
    f"<div class='field' style='left:{left}pt; top:{top}pt; "
    f"width:60pt; height:30pt; display:flex; align-items:center; justify-content:center; "
    f"text-align:center; font-family:{font_family}; font-size:{font_size}; "
    f"white-space:pre-wrap; word-break:break-word;'>"
    f"{safe_value}</div>\n"
)

        # Add photo
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

        # Render overlay PDF
        overlay_stream = io.BytesIO()
        HTML(string=html_content).write_pdf(overlay_stream)
        overlay_stream.seek(0)
        overlay_pdf = PdfReader(overlay_stream)

        # Merge overlay
        writer = PdfWriter()
        page0 = template_pdf.pages[0]
        page0.merge_page(overlay_pdf.pages[0])
        writer.add_page(page0)
        for p in template_pdf.pages[1:]:
            writer.add_page(p)

        # Save with metadata
        final_pdf = io.BytesIO()
        writer.write(final_pdf)
        final_pdf.seek(0)
        final_pdf = save_pdf_with_metadata(final_pdf, form_data)

        return send_file(final_pdf, as_attachment=True, download_name="matrimony_filled.pdf", mimetype="application/pdf")

    # GET request → empty form
    return render_template("form.html", form_data={})


# @app.route('/debug_fields')
# def debug_fields():
#     template_path = "templates/matrimony_template.pdf"
#     template_pdf = PdfReader(open(template_path, "rb"))
#     first_page = template_pdf.pages[0]
#     width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(width, height))

#     # helper function
#     def draw_marker(x, y, label, color=(1, 0, 0)):
#         box_w, box_h = 120, 20  # adjust per your needs
#         can.setFillColorRGB(*color, alpha=0.3)
#         can.rect(x, y - box_h, box_w, box_h, fill=True, stroke=False)
#         can.setFillColorRGB(0, 0, 0)
#         can.setFont("Helvetica", 8)
#         can.drawString(x + 2, y - 10, label)

#     # mark FIELD_POSITIONS
#     for field, (x, y) in FIELD_POSITIONS.items():
#         draw_marker(x, y, field, color=(1, 0, 0))

#     # mark RAASI
#     for field, (x, y) in RAASI_POSITIONS.items():
#         draw_marker(x, y, field, color=(0, 0, 1))

#     # mark NAVAMSA
#     for field, (x, y) in NAVAMSA_POSITIONS.items():
#         draw_marker(x, y, field, color=(0, 0.6, 0))

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
#                      download_name="debug_fields.pdf",
#                      mimetype="application/pdf")

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
