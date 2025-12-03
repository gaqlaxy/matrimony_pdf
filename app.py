


# # import io, base64, os, html, json, re
# # from flask import Flask, render_template, request, send_file
# # from PyPDF2 import PdfReader, PdfWriter
# # from weasyprint import HTML
# # from werkzeug.utils import secure_filename
# # from reportlab.pdfgen import canvas



# # app = Flask(__name__, template_folder="templates-html")
# # app.config["UPLOAD_FOLDER"] = "uploads"

# import io, base64, os, html, json, re
# from flask import Flask, render_template, request, send_file, jsonify, session, redirect, url_for
# from PyPDF2 import PdfReader, PdfWriter
# from weasyprint import HTML
# from werkzeug.utils import secure_filename
# from reportlab.pdfgen import canvas

# import firebase_admin
# from firebase_admin import credentials, auth

# # -------------------------
# # App + Config
# # -------------------------
# app = Flask(__name__, template_folder="templates-html")
# app.secret_key = "supersecret"  # change in production
# app.config["UPLOAD_FOLDER"] = "uploads"

# # -------------------------
# # Firebase Init
# # -------------------------
# cred = credentials.Certificate("firebase-key.json")
# firebase_admin.initialize_app(cred)

# # -------------------------
# # Firebase Routes
# # -------------------------
# @app.route("/verify_token", methods=["POST"])
# def verify_token():
#     data = request.json
#     id_token = data.get("idToken")

#     try:
#         decoded_token = auth.verify_id_token(id_token)
#         uid = decoded_token["uid"]

#         # Save user session
#         session["user"] = uid
#         return jsonify({"status": "success", "uid": uid})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 401


# @app.route("/dashboard")
# def dashboard():
#     if "user" not in session:
#         return redirect(url_for("login_page"))
#     return f"Welcome {session['user']}! <a href='/logout'>Logout</a>"


# @app.route("/logout")
# def logout():
#     session.pop("user", None)
#     return redirect(url_for("login_page"))


# @app.route("/login")
# def login_page():
#     return """
#     <h2>Login with Firebase</h2>
#     <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
# <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>
# <script>
#   const firebaseConfig = {
#     apiKey: "AIzaSyC6Cekt-KpbH5rq480JxFZ77A580gXskVg",
#     authDomain: "balajimatri-67547.firebaseapp.com",
#     projectId: "balajimatri-67547"
#   };
#   firebase.initializeApp(firebaseConfig);

#   const auth = firebase.auth();

#   function login() {
#     const email = document.getElementById("email").value;
#     const password = document.getElementById("password").value;
#     auth.signInWithEmailAndPassword(email, password)
#       .then(userCredential => userCredential.user.getIdToken())
#       .then(idToken => fetch("/verify_token", {
#           method: "POST",
#           headers: {"Content-Type": "application/json"},
#           body: JSON.stringify({idToken})
#       }))
#       .then(res => res.json())
#       .then(data => window.location.href = "/dashboard")
#       .catch(err => alert(err.message));
#   }

#   function signup() {
#     const email = document.getElementById("email").value;
#     const password = document.getElementById("password").value;
#     auth.createUserWithEmailAndPassword(email, password)
#       .then(() => login()) // auto login
#       .catch(err => alert(err.message));
#   }
# </script>

#     <input type="email" id="email" placeholder="Email"><br>
#     <input type="password" id="password" placeholder="Password"><br>
#     <button onclick="login()">Login</button>
#     <button onclick="signup()">Signup</button>
#     """



# @app.route("/signup")
# def signup_page():
#     return """
#     <h2>Signup</h2>
#     <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
#     <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>
#     <script>
#       const firebaseConfig = {
#         apiKey: "AIzaSyC6Cekt-KpbH5rq480JxFZ77A580gXskVg",
#         authDomain: "balajimatri-67547.firebaseapp.com",
#         projectId: "balajimatri-67547"
#       };
#       firebase.initializeApp(firebaseConfig);

#       const auth = firebase.auth();

#       function signup() {
#         const email = document.getElementById("email").value;
#         const password = document.getElementById("password").value;
#         auth.createUserWithEmailAndPassword(email, password)
#           .then(userCredential => userCredential.user.getIdToken())
#           .then(idToken => fetch("/verify_token", {
#               method: "POST",
#               headers: {"Content-Type": "application/json"},
#               body: JSON.stringify({idToken})
#           }))
#           .then(res => res.json())
#           .then(data => {
#               if (data.status === "success") {
#                   window.location.href = data.redirect;
#               } else {
#                   alert("Signup failed: " + data.message);
#               }
#           })
#           .catch(err => alert(err.message));
#       }
#     </script>
#     <input type="email" id="email" placeholder="Email"><br>
#     <input type="password" id="password" placeholder="Password"><br>
#     <button onclick="signup()">Sign Up</button>
#     <p>Already have an account? <a href="/login">Login here</a></p>
#     """

# @app.route("/verify_token", methods=["POST"])
# def verify_token():
#     data = request.json
#     id_token = data.get("idToken")

#     try:
#         decoded_token = auth.verify_id_token(id_token)
#         uid = decoded_token["uid"]

#         # Save user session
#         session["user"] = uid
#         return jsonify({"status": "success", "uid": uid})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 401


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
#     "elder_brother":     (110, 617),
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
#     "rentalhouse":       (10, 400),
#     "lease":             (100, 400),
#     "ownhouse":          (180, 400),
# }

# RAASI_POSITIONS = {
#     "raasi_1":  (20, 350),  "raasi_2":  (90, 350),  "raasi_3":  (180, 350),
#     "raasi_4":  (260, 350), "raasi_5":  (260, 275), "raasi_6":  (260, 200),
#     "raasi_7":  (260, 140), "raasi_8":  (180, 140), "raasi_9":  (100, 140),
#     "raasi_10": (20, 140),  "raasi_11": (20, 200),  "raasi_12": (20, 270),
# }
# NAVAMSA_POSITIONS = {
#     "navamsa_1":  (360, 350), "navamsa_2":  (435, 350), "navamsa_3":  (510, 350),
#     "navamsa_4":  (590, 350), "navamsa_5":  (590, 275), "navamsa_6":  (590, 200),
#     "navamsa_7":  (590, 140), "navamsa_8":  (435, 140), "navamsa_9":  (510, 140),
#     "navamsa_10": (360, 140), "navamsa_11": (360, 200), "navamsa_12": (360, 270),
# }

# PHOTO_BOX = (469, 410, 920, 1041.5)
# # -------------------------
# # Metadata helpers
# # -------------------------
# def save_pdf_with_metadata(pdf_stream, form_data):
#     reader = PdfReader(pdf_stream)
#     writer = PdfWriter()
#     writer.append_pages_from_reader(reader)
#     writer.add_metadata({
#         "/FormData": json.dumps(form_data, ensure_ascii=False)
#     })
#     out = io.BytesIO()
#     writer.write(out)
#     out.seek(0)
#     return out


# def extract_form_data_from_pdf(file_stream):
#     reader = PdfReader(file_stream)
#     metadata = reader.metadata
#     if metadata and "/FormData" in metadata:
#         try:
#             return json.loads(metadata["/FormData"])
#         except Exception:
#             return {}
#     return {}

# # -------------------------
# # Text helpers (Tamil detection + mixed runs)
# # -------------------------
# def contains_tamil(s: str) -> bool:
#     return bool(s) and any("\u0B80" <= ch <= "\u0BFF" for ch in s)

# _tamil_split_re = re.compile(r'[\u0B80-\u0BFF]+|[^\u0B80-\u0BFF]+')

# def split_into_runs(s: str):
#     if not s:
#         return []
#     return _tamil_split_re.findall(s)

# def render_mixed_html(value: str, eng_style: str, tam_style: str) -> str:
#     parts = split_into_runs(value)
#     out = []
#     for part in parts:
#         esc = html.escape(part)
#         if contains_tamil(part):
#             out.append(f"<span style=\"{tam_style}\">{esc}</span>")
#         else:
#             out.append(f"<span style=\"{eng_style}\">{esc}</span>")
#     return "".join(out)

# # -------------------------
# # Routes
# # -------------------------
# @app.route("/", methods=["GET", "POST"])
# def form():
#     form_data = {}

#     if request.method == "POST":
#         # Case 1: User uploaded PDF to edit
#         if "pdf" in request.files and request.files["pdf"].filename != "":
#             pdf_file = request.files["pdf"]
#             form_data = extract_form_data_from_pdf(pdf_file)
#             return render_template("form.html", form_data=form_data)

#         # Case 2: User submitted form to generate PDF
#         form_data = request.form.to_dict()

#         # Handle photo upload
#         photo_data = None
#         if "photo" in request.files and request.files["photo"].filename != "":
#             photo_file = request.files["photo"]
#             filename = secure_filename(photo_file.filename)
#             photo_bytes = photo_file.read()
#             b64_str = base64.b64encode(photo_bytes).decode("utf-8")
#             ext = os.path.splitext(filename)[1].lower()
#             mime = "image/png" if ext == ".png" else "image/jpeg"
#             photo_data = f"data:{mime};base64,{b64_str}"

#         # Load template PDF (adjust filename if yours is different)
#         template_path = "templates/matrimony.pdf"
#         template_pdf = PdfReader(open(template_path, "rb"))
#         first_page = template_pdf.pages[0]
#         width, height = float(first_page.mediabox.width), float(first_page.mediabox.height)

#         # Decide color based on gender
#         gender = form_data.get("gender", "").lower()
#         if gender == "male":
#             color = "rgb(168, 0, 0)"
#         elif gender == "female":
#             color = "rgb(0, 170, 0)"
#         else:
#             color = "#000000"

#         # Font files (Latha regular + bold) - ensure these files exist in fonts/
#         latha_regular = f"file://{os.path.join(app.root_path, 'fonts', 'Latha.ttf')}"
#         latha_bold = f"file://{os.path.join(app.root_path, 'fonts', 'Latha-Bold.ttf')}"

#         # Build overlay HTML
#         html_content = f"""<!doctype html>
# <html>
# <head>
# <meta charset="utf-8">
# <style>
#   @page {{ size: {width}pt {height}pt; margin: 0; }}

#   @font-face {{
#     font-family: 'Latha';
#     src: url('{latha_regular}') format('truetype');
#     font-weight: normal;
#     font-style: normal;
#   }}
#   @font-face {{
#     font-family: 'Latha';
#     src: url('{latha_bold}') format('truetype');
#     font-weight: bold;
#     font-style: normal;
#   }}

#   html, body {{
#     margin: 0;
#     padding: 0;
#     width: {width}pt;
#     height: {height}pt;
#     font-family: 'Latha', sans-serif;
#     /* don't force bold globally here */
#   }}

#   .field {{
#     position: absolute;
#     white-space: pre-wrap;
#     word-wrap: break-word;
#     /* color and weight applied per-span via render_mixed_html */
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

#         # Inline styles for main fields and raasi/navamsa (include color where relevant)
#         # Use medium weight (500) to reduce the heavy "bold" look; change to 400 if you want lighter.
#         eng_style_main = f"font-family:Arial, sans-serif; font-size:17pt; font-weight:500; color:{color}; line-height:1;"
#         tam_style_main = f"font-family:Latha, sans-serif; font-size:15pt; font-weight:500; color:{color}; line-height:1;"

#         # Raasi/Navamsa styles (smaller)
#         eng_style_raasi = f"font-family:Arial, sans-serif; font-size:14pt; font-weight:500; color:{color}; line-height:1.15;"
#         tam_style_raasi = f"font-family:Latha, sans-serif; font-size:14pt; font-weight:500; color:{color}; line-height:1.15;"

#         # --- Main Fields ---
#         for field, (x, y) in FIELD_POSITIONS.items():
#             value = form_data.get(field, "")
#             if value:
#                 left = x
#                 top = height - y
#                 safe_html = render_mixed_html(value, eng_style_main, tam_style_main)
#                 html_content += (
#                     f"<div class='field' style='left:{left}pt; top:{top}pt;'>"
#                     f"{safe_html}</div>\n"
#                 )

#         # --- Raasi + Navamsa (fixed & unindented correctly) ---
#         for dct in (RAASI_POSITIONS, NAVAMSA_POSITIONS):
#             for field, (x, y) in dct.items():
#                 value = form_data.get(field, "")
#                 if not value:
#                     continue

#                 left = x
#                 top = height - y

#                 # Split the ORIGINAL value into logical lines entered by the user
#                 lines = value.splitlines()
#                 if not lines:
#                     lines = [""]

#                 # For each line produce mixed-span HTML (Tamil vs ASCII), preserving inline styles including color & weight
#                 rendered_lines = [render_mixed_html(line, eng_style_raasi, tam_style_raasi) for line in lines]

#                 # Wrap each rendered line in a block-level wrapper so flex stacks them correctly.
#                 line_blocks = "".join([f"<div style='display:block; width:100%;'>{ln or '&nbsp;'}</div>" for ln in rendered_lines])

#                 # Container: column flex centers vertically+horizontally; each line-block is stacked vertically.
#                 html_content += (
#                     f"<div style='position:absolute; left:{left}pt; top:{top}pt; "
#                     f"width:60pt; min-height:30pt; display:flex; flex-direction:column; "
#                     f"align-items:center; justify-content:center; text-align:center; "
#                     f"line-height:1.15; white-space:normal; word-break:normal; overflow:hidden;'>"
#                     f"{line_blocks}</div>\n"
#                 )

#         # --- Photo ---
#         if photo_data:
#             x1, y1, x2, y2 = PHOTO_BOX
#             box_w = x2 - x1
#             box_h = y2 - y1
#             left = x1
#             top = height - y2
#             html_content += (
#                 f"<img src='{photo_data}' class='photo' "
#                 f"style='left:{left}pt; top:{top}pt; width:{box_w}pt; height:{box_h}pt;'/>"
#             )

#         html_content += "</body></html>"

#         # Render overlay PDF with WeasyPrint
#         overlay_stream = io.BytesIO()
#         HTML(string=html_content).write_pdf(overlay_stream)
#         overlay_stream.seek(0)
#         overlay_pdf = PdfReader(overlay_stream)

#         # Merge overlay into template
#         writer = PdfWriter()
#         page0 = template_pdf.pages[0]
#         page0.merge_page(overlay_pdf.pages[0])
#         writer.add_page(page0)
#         for p in template_pdf.pages[1:]:
#             writer.add_page(p)

#         # Save with metadata and return
#         final_pdf = io.BytesIO()
#         writer.write(final_pdf)
#         final_pdf.seek(0)
#         final_pdf = save_pdf_with_metadata(final_pdf, form_data)

#         return send_file(final_pdf, as_attachment=True, download_name="matrimony_filled.pdf", mimetype="application/pdf")

#     # GET: render empty form
#     return render_template("form.html", form_data={})


# if __name__ == "__main__":
#     app.run(debug=True)




import io, base64, os, html, json, re
from flask import Flask, render_template, request, send_file, jsonify, session, redirect, url_for
from PyPDF2 import PdfReader, PdfWriter
from weasyprint import HTML
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas

import firebase_admin
from firebase_admin import credentials, auth

# -------------------------
# App Config
# -------------------------
app = Flask(__name__, template_folder="templates-html")
app.config["UPLOAD_FOLDER"] = "uploads"
app.secret_key = "supersecret"  # change in production

# Firebase init
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

# -------------------------
# Firebase Auth Routes
# -------------------------
@app.route("/verify_token", methods=["POST"])
def verify_token():
    data = request.json
    id_token = data.get("idToken")

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]

        # Save user session
        session["user"] = uid
        return jsonify({"status": "success", "uid": uid, "redirect": "/"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 401


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))



@app.route("/login")
def login_page():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Login | Balaji Matrimony</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
  <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
  <div class="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md text-center">
    <h2 class="text-2xl font-bold mb-6 text-gray-700">Welcome Back</h2>
    <input type="email" id="email" placeholder="Email"
      class="w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
    <input type="password" id="password" placeholder="Password"
      class="w-full mb-6 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
    <button onclick="login()"
      class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">Login</button>
    <p class="mt-4 text-gray-600 text-sm">Don’t have an account? 
      <a href="/signup" class="text-blue-600 hover:underline">Sign up here</a>
    </p>
  </div>

  <script>
    const firebaseConfig = {
      apiKey: "AIzaSyC6Cekt-KpbH5rq480JxFZ77A580gXskVg",
      authDomain: "balajimatri-67547.firebaseapp.com",
      projectId: "balajimatri-67547"
    };
    firebase.initializeApp(firebaseConfig);
    const auth = firebase.auth();

    function login() {
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      auth.signInWithEmailAndPassword(email, password)
        .then(userCredential => userCredential.user.getIdToken())
        .then(idToken => fetch("/verify_token", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({idToken})
        }))
        .then(res => res.json())
        .then(data => {
          if (data.status === "success") {
            window.location.href = data.redirect;
          } else {
            alert("Login failed: " + data.message);
          }
        })
        .catch(err => alert(err.message));
    }
  </script>
</body>
</html>
"""




@app.route("/signup")
def signup_page():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Signup | Balaji Matrimony</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>
  <script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
  <div class="bg-white shadow-xl rounded-2xl p-8 w-full max-w-md text-center">
    <h2 class="text-2xl font-bold mb-6 text-gray-700">Create an Account</h2>
    <input type="email" id="email" placeholder="Email"
      class="w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
    <input type="password" id="password" placeholder="Password"
      class="w-full mb-6 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
    <button onclick="signup()"
      class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">Sign Up</button>
    <p class="mt-4 text-gray-600 text-sm">Already have an account? 
      <a href="/login" class="text-blue-600 hover:underline">Login here</a>
    </p>
  </div>

  <script>
    const firebaseConfig = {
      apiKey: "AIzaSyC6Cekt-KpbH5rq480JxFZ77A580gXskVg",
      authDomain: "balajimatri-67547.firebaseapp.com",
      projectId: "balajimatri-67547"
    };
    firebase.initializeApp(firebaseConfig);
    const auth = firebase.auth();

    function signup() {
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      auth.createUserWithEmailAndPassword(email, password)
        .then(userCredential => userCredential.user.getIdToken())
        .then(idToken => fetch("/verify_token", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({idToken})
        }))
        .then(res => res.json())
        .then(data => {
          if (data.status === "success") {
            window.location.href = data.redirect;
          } else {
            alert("Signup failed: " + data.message);
          }
        })
        .catch(err => alert(err.message));
    }
  </script>
</body>
</html>
"""


# -------------------------
# PDF Section (only for logged in users)
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
    "elder_sister":      (220, 617),
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
    "navamsa_7":  (590, 140), "navamsa_8":  (510, 140), "navamsa_9":  (435, 140),
    "navamsa_10": (360, 140), "navamsa_11": (360, 200), "navamsa_12": (360, 270),
}
STAR_POSITIONS = {
    "Aswini": (750, 350),
    "Barani": (730, 335),
    "Karthigai": (760, 318),
    "Rohini": (750, 300),
    "Mirugashirisham": (770, 280),
    "Thiruvathirai": (765, 265),
    "Punaipoosam": (755, 245),
    "Poosam": (728, 230),
    "Ayilyam": (755, 215),
    "Magam": (728, 195),
    "Pooram": (728, 178),
    "Uthiram": (747, 164),
    "Astham": (747, 144),
    "Chitirai": (747, 124),
    "Swathi": (850, 350),
    "Visagam": (860, 335),
    "Anusham": (862, 318),
    "Kettai": (860, 300),
    "Moolam": (850, 280),
    "Pooradam": (865, 265),
    "Uthiradam": (880, 245),
    "Thiruvonam": (890, 230),
    "Avittam": (870, 215),
    "Sadhayam": (855, 195),
    "Pooratathi": (870, 178),
    "Uthiratathi": (890, 160),
    "Revathy": (855, 144)
}

PHOTO_BOX = (469, 410, 920, 1041.5)

def save_pdf_with_metadata(pdf_stream, form_data):
    reader = PdfReader(pdf_stream)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.add_metadata({"/FormData": json.dumps(form_data, ensure_ascii=False)})
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

@app.route("/", methods=["GET", "POST"])
def form():
    if "user" not in session:
        return redirect(url_for("login_page"))
    
    form_data = {}
    if request.method == "POST":
        # Case 1: User uploaded PDF to edit
        if "pdf" in request.files and request.files["pdf"].filename != "":
            pdf_file = request.files["pdf"]
            form_data = extract_form_data_from_pdf(pdf_file)
            return render_template("form.html", form_data=form_data)

        # Case 2: User submitted form to generate PDF
        # form_data = request.form.to_dict()
        form_data = request.form.to_dict(flat=False)

# Convert single values back to strings (except star list)
        for k, v in form_data.items():
            if k != "star_select" and isinstance(v, list) and len(v) == 1:
                form_data[k] = v[0]

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
    font-weight: 600;
    font-style: normal;
  }}
  @font-face {{
    font-family: 'Latha';
    src: url('{latha_bold}') format('truetype');
    font-weight: 600;
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
        eng_style_main = f"font-family:Arial, sans-serif; font-size:18pt; font-weight:600; color:{color}; line-height:1;"
        tam_style_main = f"font-family:Latha, sans-serif; font-size:18pt; font-weight:600; color:{color}; line-height:1;"

        # Raasi/Navamsa styles (smaller)
        eng_style_raasi = f"font-family:Arial, sans-serif; font-size:14pt; font-weight:600; color:{color}; line-height:1.15;"
        tam_style_raasi = f"font-family:Latha, sans-serif; font-size:14pt; font-weight:600; color:{color}; line-height:1.15;"

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
                
        # --- Raasi + Navamsa (Tamil/English + gender color + correct alignment + smart line split) ---
        for dct in (RAASI_POSITIONS, NAVAMSA_POSITIONS):
            for field, (x, y) in dct.items():
                value = form_data.get(field, "")
                if not value:
                    continue

                left = x
                top = height - y  # top-left origin

                # Choose text color by gender
                

                # Base styles
                eng_style_base = f"font-family:Arial, sans-serif; font-weight:600; color:{color}; line-height:1.1;"
                tam_style_base = f"font-family:Latha, sans-serif; font-weight:600; color:{color}; line-height:1.1;"

                # Split words and group 2 per line
                words = value.split()
                lines = []
                for i in range(0, len(words), 2):
                    lines.append(" ".join(words[i:i+2]))

                # Auto font sizing based on word count
                if len(words) <= 2:
                    font_size = "17pt"
                elif len(words) <= 3:
                    font_size = "15pt"
                elif len(words) <= 4:
                    font_size = "13pt"
                else:
                    font_size = "9pt"

                eng_style_box = eng_style_base.replace("line-height:1.1;", f"font-size:{font_size}; line-height:1.1;")
                tam_style_box = tam_style_base.replace("line-height:1.1;", f"font-size:{font_size}; line-height:1.1;")

                # Render Tamil/English mixed HTML for each line
                rendered_lines = [render_mixed_html(line.strip(), eng_style_box, tam_style_box) for line in lines]

                # Stack vertically inside the box
                line_blocks = "".join(
                    [f"<div style='width:100%; text-align:center;'>{ln or '&nbsp;'}</div>" for ln in rendered_lines]
                )

                # Container
                html_content += (
                    f"<div style='position:absolute; left:{left}pt; top:{top}pt; "
                    f"width:60pt; height:30pt; display:flex; flex-direction:column; "
                    f"justify-content:center; align-items:center; text-align:center; "
                    f"font-weight:600; white-space:pre-wrap; word-break:break-word;'>"
                    f"{line_blocks}</div>\n"
                )


        selected_stars = form_data.get("star_select", [])

        for star in selected_stars:
            if star in STAR_POSITIONS:
                x, y = STAR_POSITIONS[star]
                tick_left = x
                tick_top = height - y

                html_content += (
                    f"<div style='position:absolute; left:{tick_left}pt; top:{tick_top}pt; "
                    f"font-size:18pt; font-weight:bold; color:{color};'>✔</div>"
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

   
        
    
    return render_template("form.html", form_data={})


@app.route('/debug_grid')
def debug_grid():
    template_path = "templates/matrimony.pdf"
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
# if __name__ == "__main__":
#     app.run(debug=True)


# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
