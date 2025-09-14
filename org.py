

# import io
# from flask import Flask, render_template, request, send_file
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.utils import simpleSplit
# from PyPDF2 import PdfReader, PdfWriter
# from reportlab.lib.utils import ImageReader
# from PIL import Image

# app = Flask(__name__, template_folder="templates-html")

# # ✅ Register Tamil font (update path if needed)
# pdfmetrics.registerFont(TTFont('Latha', 'fonts/latha.ttf'))


# def draw_wrapped_text(can, text, x, y, max_width,
#                       font_name='Latha', font_size=12, leading=None):
#     """Draw text with wrapping (y is top line)."""
#     if not text:
#         return
#     lines = simpleSplit(text, font_name, font_size, max_width)
#     if leading is None:
#         leading = font_size * 1.25
#     can.setFont(font_name, font_size)
#     for i, line in enumerate(lines):
#         can.drawString(x, y - i * leading, line)


# def add_debug_grid(can, width, height, step=100):
#     """Draw debug grid with coordinates for alignment."""
#     can.setStrokeColorRGB(0.85, 0.85, 0.85)
#     can.setFont("Helvetica", 6)
#     for gx in range(0, int(width) + 1, step):
#         can.line(gx, 0, gx, height)
#         can.drawString(gx + 2, height - 8, str(gx))
#     for gy in range(0, int(height) + 1, step):
#         can.line(0, gy, width, gy)
#         can.drawString(2, gy + 2, str(gy))


# # ✅ Mapping: field → (x, y, max_width, font_size)
# FIELD_POSITIONS = {
#     "registernumber":   (110, 1052, 150, 12),
#     "introducedby":     (352, 1052, 150, 12),
#     "inam":             (80, 1025, 150, 12),
#     "name":             (100, 980, 200, 14),
#     "birth_city":       (110, 950, 150, 12),
#     "dob":              (120, 910, 150, 12),
#     "birth_time":       (350, 910, 150, 12),
#     "star":             (110, 850, 150, 12),
#     "raasi_text":       (350, 850, 150, 12),
#     "height":           (80, 800, 150, 12),
#     "colour":           (220, 800, 150, 12),
#     "laknam":           (380, 800, 150, 12),
#     "education":        (70, 820, 200, 12),
#     "work":             (100, 750, 200, 12),
#     "income":           (100, 380, 200, 12),
#     "birthorder":       (100, 350, 150, 12),
#     "elder_brother":    (100, 320, 150, 12),
#     "elder_sister":     (100, 290, 150, 12),
#     "younger_brother":  (100, 260, 150, 12),
#     "younger_sister":   (100, 230, 150, 12),
#     "father_name":      (350, 800, 200, 12),
#     "father_occupation":(350, 770, 200, 12),
#     "mother_name":      (350, 740, 200, 12),
#     "mother_occupation":(350, 710, 200, 12),
#     "expectation":      (350, 650, 250, 12),
#     "house_address":    (350, 590, 250, 12),
# }

# # ✅ Raasi and Navamsa placeholders (tune later using grid)
# RAASI_BOXES = {i: (100 + (i - 1) * 40, 150) for i in range(1, 13)}
# NAVAMSA_BOXES = {i: (100 + (i - 1) * 40, 80) for i in range(1, 13)}


# @app.route('/')
# def form():
#     return render_template('form.html')



# @app.route('/generate', methods=['POST'])
# def generate_pdf():
    
#     form_data = request.form.to_dict()
#     photo = request.files.get("photo")  # ✅ get uploaded photo

#     # Load template...
#     template_path = "templates/matrimony_template.pdf"
#     template_pdf = PdfReader(open(template_path, "rb"))

#     first_page = template_pdf.pages[0]
#     try:
#         media = first_page.mediabox
#         width, height = float(media.width), float(media.height)
#     except Exception:
#         width, height = A4

#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(width, height))

#     # Debug grid
#     add_debug_grid(can, width, height, step=50)

#     # ✅ Text color logic
#     gender = form_data.get("gender", "").lower()
#     if gender == "male":
#         can.setFillColorRGB(0.6, 0.3, 0.0)   # brown
#     elif gender == "female":
#         can.setFillColorRGB(0.0, 0.5, 0.0)   # green
#     else:
#         can.setFillColorRGB(0, 0, 0)

#     # ✅ Place fields
#     for field, (x, y, max_w, fs) in FIELD_POSITIONS.items():
#         draw_wrapped_text(
#             can,
#             form_data.get(field, ""),
#             x, y,
#             max_width=max_w,
#             font_name="Latha",
#             font_size=fs
#         )

#     # ✅ Place Raasi & Navamsa
#     for i, (x, y) in RAASI_BOXES.items():
#         draw_wrapped_text(can, form_data.get(f"raasi_{i}", ""), x, y, max_width=40, font_name="Latha", font_size=10)

#     for i, (x, y) in NAVAMSA_BOXES.items():
#         draw_wrapped_text(can, form_data.get(f"navamsa_{i}", ""), x, y, max_width=40, font_name="Latha", font_size=10)

#     # ✅ Place uploaded photo
#     if photo:
#         img = Image.open(photo.stream)
#         # Convert to RGB in case of PNG with alpha
#         if img.mode in ("RGBA", "P"):
#             img = img.convert("RGB")

#         img_reader = ImageReader(img)

#         # Calculate width/height of the box
#         box_width = 900 - 460
#         box_height = 1080 - 410

#         can.drawImage(
#             img_reader,
#             460, 410,               # bottom-left corner
#             width=box_width,
#             height=box_height,
#             preserveAspectRatio=True,
#             mask='auto'
#         )

#     can.save()


#     packet.seek(0)

#     # Merge overlay into template
#     overlay_pdf = PdfReader(packet)
#     writer = PdfWriter()
#     page0 = template_pdf.pages[0]
#     page0.merge_page(overlay_pdf.pages[0])
#     writer.add_page(page0)

#     # Add remaining pages (if any)
#     for p in template_pdf.pages[1:]:
#         writer.add_page(p)

#     # Return PDF download
#     out_stream = io.BytesIO()
#     writer.write(out_stream)
#     out_stream.seek(0)

#     return send_file(out_stream,
#                      as_attachment=True,
#                      download_name="matrimony_filled.pdf",
#                      mimetype="application/pdf")















# import io
# from flask import Flask, render_template, request, send_file
# from PyPDF2 import PdfReader, PdfWriter
# from weasyprint import HTML, CSS

# app = Flask(__name__, template_folder="templates-html")

# # ✅ Mapping: field → (x, y)
# FIELD_POSITIONS = {
#     "name": (120, 980),
#     "dob": (120, 910),
#     "birth_time": (350, 910),
#     "star": (110, 850),
#     "raasi_text": (350, 850),
#     "father_name": (350, 800),
#     "mother_name": (350, 740),
#     "house_address": (350, 590),
# }


# @app.route('/')
# def form():
#     return render_template('form.html')


# @app.route('/generate', methods=['POST'])
# def generate_pdf():
#     form_data = request.form.to_dict()

#     # 1️⃣ Load template PDF
#     template_path = "templates/matrimony_template.pdf"
#     template_pdf = PdfReader(open(template_path, "rb"))

#     # Get page size
#     first_page = template_pdf.pages[0]
#     media = first_page.mediabox
#     width, height = float(media.width), float(media.height)

#     # 2️⃣ Build overlay HTML with absolute positioning
#     html_content = """
#     <html>
#     <head>
#         <style>
#             @page { size: %dpx %dpx; margin: 0; }
#             body { margin: 0; font-family: 'Noto Sans Tamil', sans-serif; }
#             .field {
#                 position: absolute;
#                 font-size: 14px;
#                 color: black;
#             }
#     """ % (width, height)

#     # ✅ Add fields dynamically
#     for field, (x, y) in FIELD_POSITIONS.items():
#         value = form_data.get(field, "")
#         html_content += f"""
#             .{field} {{ left: {x}px; top: {height - y}px; }}
#         """

#     html_content += "</style></head><body>"

#     # ✅ Place actual values
#     for field, (x, y) in FIELD_POSITIONS.items():
#         value = form_data.get(field, "")
#         html_content += f"<div class='field {field}'>{value}</div>"

#     html_content += "</body></html>"

#     # 3️⃣ Render overlay as PDF
#     overlay_stream = io.BytesIO()
#     HTML(string=html_content).write_pdf(overlay_stream)
#     overlay_stream.seek(0)

#     overlay_pdf = PdfReader(overlay_stream)

#     # 4️⃣ Merge overlay into template
#     writer = PdfWriter()
#     page0 = template_pdf.pages[0]
#     page0.merge_page(overlay_pdf.pages[0])
#     writer.add_page(page0)

#     for p in template_pdf.pages[1:]:
#         writer.add_page(p)

#     # 5️⃣ Return file
#     out_stream = io.BytesIO()
#     writer.write(out_stream)
#     out_stream.seek(0)

#     return send_file(out_stream,
#                      as_attachment=True,
#                      download_name="matrimony_filled.pdf",
#                      mimetype="application/pdf")


# if __name__ == "__main__":
#     app.run(debug=True)


# WORKING 

# import io, base64
# from flask import Flask, render_template, request, send_file
# from PyPDF2 import PdfReader, PdfWriter
# from weasyprint import HTML
# from werkzeug.utils import secure_filename

# app = Flask(__name__, template_folder="templates-html")
# app.config["UPLOAD_FOLDER"] = "uploads"

# # ✅ Core field positions
# FIELD_POSITIONS = {
#     "name": (120, 980),
#     "dob": (120, 910),
#     "birth_time": (350, 910),
#     "star": (110, 850),
#     "raasi_text": (350, 850),
#     "father_name": (350, 800),
#     "mother_name": (350, 740),
#     "house_address": (350, 590),
#     "gender": (120, 1050),
# }

# # ✅ Raasi + Navamsa 12 positions each (dummy coordinates — replace with yours)
# RAASI_POSITIONS = {f"raasi_{i}": (100 + (i-1) * 40, 700) for i in range(1, 13)}
# NAVAMSA_POSITIONS = {f"navamsa_{i}": (100 + (i-1) * 40, 650) for i in range(1, 13)}

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
#     html_content = f"""
#     <html>
#     <head>
#         <style>
#             @page {{ size: {width}px {height}px; margin: 0; }}
#             body {{ margin: 0; font-family: 'Noto Sans Tamil', sans-serif; }}
#             .field {{
#                 position: absolute;
#                 font-size: 14px;
#                 color: black;
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
#         if not value:
#             continue

#         color = "black"
#         if field == "gender":
#             if value.lower() == "male":
#                 color = "brown"
#             elif value.lower() == "female":
#                 color = "green"

#         html_content += f"<div class='field' style='left:{x}px;top:{height-y}px;color:{color};'>{value}</div>"

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


# if __name__ == "__main__":
#     app.run(debug=True)
