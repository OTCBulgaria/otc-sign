from flask import Flask, request
import os, datetime

app = Flask(__name__)

# 📁 Директории за съхранение на данни
signed_folder = "signed_docs"       # За записани подписи
upload_folder = "public_docs"       # За качени документи

os.makedirs(signed_folder, exist_ok=True)
os.makedirs(upload_folder, exist_ok=True)

# ✅ Подписване на документ
@app.route('/sign', methods=['POST'])
def sign_document():
    name = request.form['username']
    doc_id = request.form['doc_id']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    entry = f"{timestamp} | {name} | {doc_id}\n"
    with open(os.path.join(signed_folder, "signatures.txt"), "a", encoding="utf-8") as f:
        f.write(entry)

    return f"""
        <h2>✅ Благодарим, {name}!</h2>
        <p>Документ с ID <strong>{doc_id}</strong> бе подписан на {timestamp}.</p>
        <a href="/podpisi.html">🔙 Назад</a>
    """

# 📤 Качване на документ (POST)
@app.route('/upload', methods=['POST'])
def upload_doc():
    file = request.files['doc']
    filename = file.filename
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    return f"<h3>✅ Документът <strong>{filename}</strong> е качен успешно!</h3><a href='/podpisi.html'>🔙 Назад</a>"

# 🌐 Страница за качване на документ (GET)
@app.route('/upload', methods=['GET'])
def show_upload_page():
    return """
    <h2>📄 Качване на документ</h2>
    <form action="/upload" method="POST" enctype="multipart/form-data">
      <input type="file" name="doc" required><br><br>
      <input type="submit" value="📤 Качи файла">
    </form>
    """
