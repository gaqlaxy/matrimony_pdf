

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

# # ✅ Raasi + Navamsa 12 positions each
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

#     # 2️⃣ Detect gender → set global text color
#     gender_value = form_data.get("gender", "").lower()
#     if gender_value == "male":
#         global_color = "brown"
#     elif gender_value == "female":
#         global_color = "green"
#     else:
#         global_color = "black"

#     # 3️⃣ Build overlay HTML
#     html_content = f"""
#     <html>
#     <head>
#         <style>
#             @page {{ size: {width}px {height}px; margin: 0; }}
#             body {{ margin: 0; font-family: 'Noto Sans Tamil', sans-serif; position: relative; }}
#             .field {{
#                 position: absolute;
#                 font-size: 14px;
#                 color: {global_color};
#             }}
#             .photo {{
#                 position: absolute;
#                 left: {PHOTO_BOX[0]}px;
#                 top: {height - PHOTO_BOX[3]}px;
#                 width: {PHOTO_BOX[2]-PHOTO_BOX[0]}px;
#                 height: {PHOTO_BOX[3]-PHOTO_BOX[1]}px;
#                 object-fit: cover;
#             }}
#             .grid-line {{
#                 position: absolute;
#                 background: rgba(0,0,0,0.1);
#                 font-size: 8px;
#                 color: gray;
#             }}
#             <div style="
#     position:absolute;
#     left:0;top:0;
#     width:{width}px;
#     height:{height}px;
#     background-image:
#         linear-gradient(to right, rgba(0,0,0,0.2) 1px, transparent 1px),
#         linear-gradient(to bottom, rgba(0,0,0,0.2) 1px, transparent 1px);
#     background-size: 50px 50px;
#     z-index:9999;
# "></div>
#         </style>
#     </head>
#     <body>
#     """

#     # 4️⃣ Normal fields
#     for field, (x, y) in FIELD_POSITIONS.items():
#         value = form_data.get(field, "")
#         if value:
#             html_content += f"<div class='field' style='left:{x}px;top:{height-y}px;'>{value}</div>"

#     # 5️⃣ Raasi + Navamsa
#     for field, (x, y) in {**RAASI_POSITIONS, **NAVAMSA_POSITIONS}.items():
#         value = form_data.get(field, "")
#         if value:
#             html_content += f"<div class='field' style='left:{x}px;top:{height-y}px;'>{value}</div>"

#     # 6️⃣ Photo
#     if photo_data:
#         html_content += f"<img src='{photo_data}' class='photo'/>"

#     # 7️⃣ Debug grid (every 50px)
#     grid_step = 50
#     max_width = int(width)
#     max_height = int(height)
#     for gx in range(0, max_width + 1, grid_step):
#         html_content += f"<div class='grid-line' style='left:{gx}px;top:0;height:{max_height}px;width:1px;'></div>"
#         html_content += f"<div class='grid-line' style='left:{gx+2}px;top:2px;'>{gx}</div>"

#     for gy in range(0, max_height + 1, grid_step):
#         html_content += f"<div class='grid-line' style='left:0;top:{gy}px;width:{max_width}px;height:1px;'></div>"
#         html_content += f"<div class='grid-line' style='left:2px;top:{gy+2}px;'>{max_height-gy}</div>"
#     # for gx in range(0, int(width), grid_step):
#     #     html_content += f"<div class='grid-line' style='left:{gx}px;top:0;height:{height}px;width:1px;'></div>"
#     #     html_content += f"<div class='grid-line' style='left:{gx+2}px;top:2px;'>{gx}</div>"
#     # for gy in range(0, int(height), grid_step):
#     #     html_content += f"<div class='grid-line' style='left:0;top:{gy}px;width:{width}px;height:1px;'></div>"
#     #     html_content += f"<div class='grid-line' style='left:2px;top:{gy+2}px;'>{height-gy}</div>"
     

#     html_content += "</body></html>"

#     # 8️⃣ Render overlay
#     overlay_stream = io.BytesIO()
#     HTML(string=html_content).write_pdf(overlay_stream)
#     overlay_stream.seek(0)
#     overlay_pdf = PdfReader(overlay_stream)

#     # 9️⃣ Merge
#     writer = PdfWriter()
#     page0 = template_pdf.pages[0]
#     page0.merge_page(overlay_pdf.pages[0])
#     writer.add_page(page0)

#     for p in template_pdf.pages[1:]:
#         writer.add_page(p)

#     # 🔟 Return
#     out_stream = io.BytesIO()
#     writer.write(out_stream)
#     out_stream.seek(0)

#     return send_file(out_stream,
#                      as_attachment=True,
#                      download_name="matrimony_filled.pdf",
#                      mimetype="application/pdf")


# if __name__ == "__main__":
#     app.run(debug=True)


import io, base64
from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from weasyprint import HTML
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas

app = Flask(__name__, template_folder="templates-html")
app.config["UPLOAD_FOLDER"] = "uploads"

# ✅ Core field positions
FIELD_POSITIONS = {
    "name": (120, 980),
    "dob": (120, 910),
    "birth_time": (350, 910),
    "star": (110, 850),
    "raasi_text": (350, 850),
    "father_name": (350, 800),
    "mother_name": (350, 740),
    "house_address": (350, 590),
    "gender": (120, 1050),
}

# ✅ Raasi + Navamsa 12 positions each
RAASI_POSITIONS = {f"raasi_{i}": (100 + (i - 1) * 40, 700) for i in range(1, 13)}
NAVAMSA_POSITIONS = {f"navamsa_{i}": (100 + (i - 1) * 40, 650) for i in range(1, 13)}

# ✅ Photo box
PHOTO_BOX = (460, 410, 900, 1080)  # (x1, y1, x2, y2)


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
        photo_data = f"data:image/png;base64,{b64_str}"

    # 1️⃣ Load template PDF
    template_path = "templates/matrimony_template.pdf"
    template_pdf = PdfReader(open(template_path, "rb"))
    first_page = template_pdf.pages[0]
    width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

    # 2️⃣ Build overlay HTML
    selected_gender = form_data.get("gender", "").lower()
    color = "black"
    if selected_gender == "male":
        color = "brown"
    elif selected_gender == "female":
        color = "green"

    html_content = f"""
    <html>
    <head>
        <style>
            @page {{ size: {width}px {height}px; margin: 0; }}
            body {{ margin: 0; font-family: 'Noto Sans Tamil', sans-serif; }}
            .field {{
                position: absolute;
                font-size: 14px;
                color: {color};
            }}
            .photo {{
                position: absolute;
                left: {PHOTO_BOX[0]}px;
                top: {height - PHOTO_BOX[3]}px;
                width: {PHOTO_BOX[2]-PHOTO_BOX[0]}px;
                height: {PHOTO_BOX[3]-PHOTO_BOX[1]}px;
                object-fit: cover;
            }}
        </style>
    </head>
    <body>
    """

    # 3️⃣ Normal fields
    for field, (x, y) in FIELD_POSITIONS.items():
        value = form_data.get(field, "")
        if value:
            html_content += f"<div class='field' style='left:{x}px;top:{height-y}px;'>{value}</div>"

    # 4️⃣ Raasi + Navamsa
    for field, (x, y) in {**RAASI_POSITIONS, **NAVAMSA_POSITIONS}.items():
        value = form_data.get(field, "")
        if value:
            html_content += f"<div class='field' style='left:{x}px;top:{height-y}px;'>{value}</div>"

    # 5️⃣ Photo
    if photo_data:
        html_content += f"<img src='{photo_data}' class='photo'/>"

    html_content += "</body></html>"

    # 6️⃣ Render overlay
    overlay_stream = io.BytesIO()
    HTML(string=html_content).write_pdf(overlay_stream)
    overlay_stream.seek(0)
    overlay_pdf = PdfReader(overlay_stream)

    # 7️⃣ Merge
    writer = PdfWriter()
    page0 = template_pdf.pages[0]
    page0.merge_page(overlay_pdf.pages[0])
    writer.add_page(page0)

    for p in template_pdf.pages[1:]:
        writer.add_page(p)

    # 8️⃣ Return
    out_stream = io.BytesIO()
    writer.write(out_stream)
    out_stream.seek(0)

    return send_file(out_stream,
                     as_attachment=True,
                     download_name="matrimony_filled.pdf",
                     mimetype="application/pdf")


# ✅ NEW Debug grid route
@app.route('/debug_grid')
def debug_grid():
    template_path = "templates/matrimony_template.pdf"
    template_pdf = PdfReader(open(template_path, "rb"))
    first_page = template_pdf.pages[0]
    width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))

    step = 50  # grid step size
    can.setStrokeColorRGB(0.8, 0.8, 0.8)
    can.setFont("Helvetica", 6)

    for x in range(0, int(width), step):
        can.line(x, 0, x, height)
        can.drawString(x + 2, height - 10, str(x))

    for y in range(0, int(height), step):
        can.line(0, y, width, y)
        can.drawString(2, y + 2, str(y))

    can.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    writer = PdfWriter()

    # merge overlay with template page
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
