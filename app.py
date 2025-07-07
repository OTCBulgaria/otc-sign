from flask import Flask, request
import os, datetime

app = Flask(__name__)
app.static_folder = 'public_docs'
app.static_url_path = '/public_docs'

# 📁 Директории
signed_folder = "signed_docs"
upload_folder = "public_docs"

os.makedirs(signed_folder, exist_ok=True)
os.makedirs(upload_folder, exist_ok=True)

# ✅ Подписване
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

# 📤 Качване
@app.route('/upload', methods=['POST'])
def upload_doc():
    file = request.files['doc']
    filename = file.filename
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)

    file_url = f"https://otc-sign.onrender.com/public_docs/{filename}"

    return f"""
        <h3>✅ Документът <strong>{filename}</strong> е качен успешно!</h3>
        <p>📎 Изпрати този линк на баба:</p>
        <a href="{file_url}" target="_blank">{file_url}</a>
        <br><br><a href="/podpisi.html">🔙 Назад</a>
    """

# 📄 Статичен ъплоуд формуляр
@app.route('/upload', methods=['GET'])
def show_upload_page():
    return """
    <h2>📄 Качване на документ</h2>
    <form action="/upload" method="POST" enctype="multipart/form-data">
      <input type="file" name="doc" required><br><br>
      <input type="submit" value="📤 Качи файла">
    </form>
    """
