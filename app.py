import streamlit as st
import json
import os
from datetime import datetime

LIBRARY_FILE = "library.json"

# ------------------ Helper Functions ------------------

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as f:
            return json.load(f)
    return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as f:
        json.dump(library, f, indent=4)

def get_genre_emoji(genre):
    emojis = {
        "romance": "❤️", "horror": "👻", "fantasy": "🐉",
        "sci-fi": "🚀", "fiction": "📘", "non-fiction": "📖",
        "mystery": "🕵️", "history": "🏺", "poetry": "📝"
    }
    return emojis.get(genre.lower(), "📚")

def recommend_books(library):
    genres = [book["genre"] for book in library if book["read"]]
    if not genres:
        return []
    top_genre = max(set(genres), key=genres.count)
    return [
        book for book in library
        if book["genre"] == top_genre and not book["read"]
    ]

def remove_book(library, title):
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            return True
    return False

def search_books(library, keyword, by):
    keyword = keyword.lower()
    return [
        book for book in library
        if keyword in book[by].lower()
    ]

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")

st.markdown("""
    <style>
        h1 {text-align:center;}
        .stButton>button {
            background: linear-gradient(90deg, #ff6ec4, #7873f5);
            color: white; border: none; border-radius: 8px;
        }
        .book-card {
            background-color: #111;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            color: #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap" rel="stylesheet">

<style>
    html, body, [class*="css"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 600;
        font-size: 2.5em;
        background: linear-gradient(90deg, #ff6ec4, #7873f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff !important;
    }

    .stForm label, .stTextInput label, .stTextArea label {
        font-weight: 500;
        font-size: 16px;
        color: #ffffff !important;
    }

    .stDownloadButton button, .stButton>button {
        background: linear-gradient(45deg, #ff4b2b, #ff416c);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }

    .stTextInput>div>div>input,
    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #444;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<h1 style='background: -webkit-linear-gradient(#8e2de2, #4a00e0);
-webkit-background-clip: text; -webkit-text-fill-color: transparent;'>📚 Personal Library Manager</h1>
""", unsafe_allow_html=True)

# ------------------ Language Toggle ------------------

lang = st.sidebar.radio("🌐 Language / زبان", ["English", "Urdu"])
t = lambda e, u: u if lang == "Urdu" else e

library = load_library()

# ------------------ Tabs ------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "➕ " + t("Add Book", "کتاب شامل کریں"),
    "🔍 " + t("Search", "تلاش کریں"),
    "📖 " + t("My Books", "میری کتب"),
    "📊 " + t("Stats", "اعدادوشمار"),
    "✨ " + t("Recommendations", "تجاویز")
])

# ------------------ Add Book ------------------

with tab1:
    st.subheader(t("Add a New Book", "نئی کتاب شامل کریں"))
    with st.form("add_form"):
        title = st.text_input(t("Title", "عنوان"))
        author = st.text_input(t("Author", "مصنف"))
        year = st.number_input(t("Publication Year", "اشاعت کا سال"), 0, 2100, 2024)
        genre = st.text_input(t("Genre", "صنف"))
        read = st.radio(t("Have you read it?", "کیا آپ نے اسے پڑھا ہے؟"), ["Yes", "No"]) == "Yes"
        cover = st.file_uploader("📷 " + t("Upload Cover (optional)", "کتاب کی تصویر اپ لوڈ کریں"), type=["jpg", "png"])
        submitted = st.form_submit_button(t("Add Book", "شامل کریں"))

        if submitted and title and author:
            book = {
                "title": title.title(),
                "author": author.title(),
                "year": year,
                "genre": genre.title(),
                "read": read,
                "date_added": str(datetime.now()),
                "cover": cover.name if cover else None
            }
            if cover:
                with open(f"covers/{cover.name}", "wb") as f:
                    f.write(cover.read())
            library.append(book)
            save_library(library)
            st.success(t(f"✅ Book '{title}' added!", f"کتاب '{title}' شامل کر دی گئی ہے!"))

# ------------------ Search ------------------

with tab2:
    st.subheader(t("Search Your Library", "اپنی لائبریری میں تلاش کریں"))
    by = st.selectbox(t("Search by", "تلاش کے طریقہ"), ["title", "author"])
    keyword = st.text_input(t("Enter keyword", "الفاظ درج کریں"))
    if keyword:
        results = search_books(library, keyword, by)
        st.write(t(f"🔎 Found {len(results)} result(s):", f"نتائج {len(results)} ملے:"))
        for book in results:
            emoji = get_genre_emoji(book["genre"])
            st.markdown(f"""
            <div class='book-card'>
                <h4>{book["title"]} {emoji}</h4>
                <p><b>{book["author"]}</b> | {book["year"]} | {book["genre"]}</p>
                <span>{'✅ Read' if book['read'] else '📖 Unread'}</span>
            </div>""", unsafe_allow_html=True)

# ------------------ Display All Books ------------------

with tab3:
    st.subheader(t("All Books", "تمام کتب"))
    if library:
        for book in library:
            emoji = get_genre_emoji(book["genre"])
            st.markdown(f"""
            <div class='book-card'>
                <h4>{book["title"]} {emoji}</h4>
                <p>{book["author"]} | {book["year"]} | {book["genre"]}</p>
                <span>{'✅ Read' if book['read'] else '📖 Unread'}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info(t("📂 Your library is empty.", "آپ کی لائبریری خالی ہے۔"))

# ------------------ Stats ------------------

with tab4:
    st.subheader(t("📊 Library Stats", "کتب کے اعداد"))
    total = len(library)
    read = sum(1 for b in library if b["read"])
    unread = total - read
    percent = (read / total) * 100 if total else 0

    st.metric(t("Total Books", "مکمل کتب"), total)
    st.metric(t("Books Read", "پڑھی گئی کتب"), read)
    st.progress(percent / 100, f"{percent:.1f}% " + t("Read", "پڑھی گئی"))

    if total >= 3:
        st.info(f"🔥 {read} day(s) streak! Keep going!")

# ------------------ Recommendations ------------------

with tab5:
    st.subheader(t("📌 Book Recommendations", "📌 کتابی تجاویز"))
    recs = recommend_books(library)
    if recs:
        for book in recs:
            emoji = get_genre_emoji(book["genre"])
            st.markdown(f"""
            <div class='book-card'>
                <h4>{book["title"]} {emoji}</h4>
                <p>{book["author"]} | {book["year"]} | {book["genre"]}</p>
                <span>🧠 Based on your reading style</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info(t("No recommendations yet. Start reading!", "کوئی تجویز نہیں۔ پہلے کچھ پڑھیں۔"))

# ------------------ Sidebar: Remove & Export ------------------

st.sidebar.header("⚙️ " + t("Manage Library", "لائبریری کا نظم"))
remove_title = st.sidebar.text_input(t("Enter title to remove", "حذف کرنے کے لیے عنوان درج کریں"))
if st.sidebar.button("🗑️ " + t("Remove Book", "کتاب حذف کریں")):
    if remove_book(library, remove_title):
        st.sidebar.success(t("Book removed!", "کتاب حذف کر دی گئی۔"))
    else:
        st.sidebar.error(t("Book not found.", "کتاب نہیں ملی۔"))

st.sidebar.download_button(
    label="📤 " + t("Export Library", "لائبریری برآمد کریں"),
    data=json.dumps(library, indent=4),
    file_name="my_library.json"
)
