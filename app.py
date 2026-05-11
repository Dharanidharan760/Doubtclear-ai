# ========================= INSTALL REQUIRED PACKAGES =========================
# pip install streamlit pandas textblob matplotlib wordcloud groq deep-translator SpeechRecognition pyaudio

# ========================= IMPORTS =========================
import streamlit as st
import re
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from groq import Groq
from deep_translator import GoogleTranslator

# ========================= PAGE CONFIG =========================
st.set_page_config(
    page_title="AI-Powered NLP Text Analysis and Smart Assistant System",
    page_icon="🧠",
    layout="wide"
)

# ========================= ONLY ONE GROQ API FOR ENTIRE PROJECT =========================
# IMPORTANT:
# Replace YOUR_GROQ_API_KEY with your real Groq API key

client = Groq(
    api_key="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"
)

# ========================= SESSION =========================
if "reviews" not in st.session_state:
    st.session_state.reviews = []

# ========================= CSS =========================
st.markdown("""
<style>

.stApp{
    background: linear-gradient(to right,#0f2027,#203a43,#2c5364);
}

h1,h2,h3,h4,h5,p,label,div{
    color:white !important;
}

section[data-testid="stSidebar"]{
    background: linear-gradient(to bottom,#141e30,#243b55);
}

textarea,input{
    background-color:white !important;
    color:black !important;
    border-radius:12px !important;
}

.card{
    background:rgba(255,255,255,0.12);
    padding:25px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.3);
    backdrop-filter: blur(12px);
    margin-top:15px;
}

.stButton>button{
    background-color:#ff4b5c;
    color:white;
    border-radius:10px;
    padding:10px 25px;
    border:none;
    font-size:16px;
    font-weight:bold;
}

.stButton>button:hover{
    background-color:#ff1f3d;
}

</style>
""", unsafe_allow_html=True)

# ========================= SIDEBAR =========================
st.sidebar.title("🧠 AI NLP Studio")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Home Dashboard",
        "🧹 Text Cleaning",
        "⭐ Reviews",
        "📧 Email Formatter",
        "🌍 Language Translator",
        "😊 Emotion Detection",
        "📝 AI Notes Summarizer"
    ]
)

# ========================= FUNCTIONS =========================
def remove_numbers(text):
    return re.sub(r'\d+', '', text)

def remove_punctuation_special(text):
    return re.sub(r'[^\w\s]', '', text)

def remove_extra_spaces(text):
    return " ".join(text.split())

def clean_text_steps(text):

    steps = {}

    steps["📝 Original Text"] = text

    text = text.lower()
    steps["🔡 Lowercase"] = text

    text = remove_numbers(text)
    steps["🔢 Removed Numbers"] = text

    text = remove_punctuation_special(text)
    steps["✂️ Removed Punctuation"] = text

    text = remove_extra_spaces(text)
    steps["📏 Removed Extra Spaces"] = text

    steps["✅ Final Output"] = text

    return steps

def find_sentiment(review):

    polarity = TextBlob(review).sentiment.polarity

    if polarity > 0:
        return "Positive 😊"

    elif polarity < 0:
        return "Negative 😔"

    else:
        return "Neutral 😐"

# ========================= HOME =========================
if page == "🏠 Home Dashboard":

    st.markdown("""
    <h1 style='text-align:center;font-size:50px;'>
    🧠 AI-Powered NLP Text Analysis & Smart Assistant System
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h2>📌 About Project</h2>

    <p>
    This project includes:
    </p>

    <ul>
    <li>🧹 Text Cleaning</li>
    <li>⭐ Sentiment Analysis</li>
    <li>📧 AI Email Formatter</li>
    <li>🌍 Language Translator</li>
    <li>😊 Emotion Detection</li>
    <li>📝 AI Notes Summarizer</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

# ========================= TEXT CLEANING =========================
elif page == "🧹 Text Cleaning":

    st.title("🧹 Smart AI Text Cleaner")

    user_text = st.text_area(
        "Enter Your Text",
        height=200
    )

    if st.button("🚀 Analyze & Clean Text"):

        result = clean_text_steps(user_text)

        for step, output in result.items():

            st.markdown(f"### {step}")

            st.code(output)

        final_output = list(result.values())[-1]

        st.subheader("📊 Word Frequency")

        words = final_output.split()

        freq = Counter(words)

        st.write(freq)

        st.subheader("☁️ Word Cloud")

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="black"
        ).generate(final_output)

        fig, ax = plt.subplots()

        ax.imshow(wordcloud)

        ax.axis("off")

        st.pyplot(fig)

# ========================= REVIEWS =========================
elif page == "⭐ Reviews":

    st.title("⭐ Review Analysis")

    name = st.text_input("Enter Name")

    review = st.text_area("Write Review")

    if st.button("Submit Review"):

        sentiment = find_sentiment(review)

        st.session_state.reviews.append({
            "Name": name,
            "Review": review,
            "Sentiment": sentiment
        })

        st.success(sentiment)

    if len(st.session_state.reviews) > 0:

        df = pd.DataFrame(st.session_state.reviews)

        st.dataframe(df)

# ========================= EMAIL FORMATTER =========================
elif page == "📧 Email Formatter":

    st.title("📧 AI Email Formatter")

    raw_email = st.text_area(
        "Enter Informal Message"
    )

    if st.button("✨ Convert to Professional Email"):

        prompt = f"""
        Convert this informal text into a professional email:

        {raw_email}
        """

        try:

            completion = client.chat.completions.create(

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                model="llama-3.3-70b-versatile"
            )

            result = completion.choices[0].message.content

            st.subheader("✅ Professional Email")

            st.success(result)

        except Exception as e:

            st.error(e)

# ========================= LANGUAGE TRANSLATOR =========================
elif page == "🌍 Language Translator":

    st.title("🌍 Language Translator")

    languages = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",

    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",

    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",

    "Danish": "da",
    "Dutch": "nl",

    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",

    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",

    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",

    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",

    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",

    "Japanese": "ja",
    "Javanese": "jw",

    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",

    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",

    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",

    "Nepali": "ne",
    "Norwegian": "no",

    "Odia": "or",

    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",

    "Romanian": "ro",
    "Russian": "ru",

    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",

    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",

    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",

    "Vietnamese": "vi",

    "Welsh": "cy",

    "Xhosa": "xh",

    "Yiddish": "yi",
    "Yoruba": "yo",

    "Zulu": "zu"
        
    }

    text = st.text_area("Enter Text")

    source = st.selectbox(
        "From",
        list(languages.keys())
    )

    target = st.selectbox(
        "To",
        list(languages.keys())
    )

    if st.button("🌍 Translate"):

        translated = GoogleTranslator(
            source=languages[source],
            target=languages[target]
        ).translate(text)

        st.success(translated)


# ========================= EMOTION DETECTION =========================
elif page == "😊 Emotion Detection":

    st.title("😊 Emotion Detection")

    emotion_text = st.text_area(
        "Enter Text"
    )

    if st.button("🔍 Detect Emotion"):

        prompt = f"""
        Detect the emotion from this text.

        Text:
        {emotion_text}
        """

        try:

            completion = client.chat.completions.create(

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                model="llama-3.3-70b-versatile"
            )

            result = completion.choices[0].message.content

            st.success(result)

        except Exception as e:

            st.error(e)

# ========================= AI NOTES SUMMARIZER =========================
elif page == "📝 AI Notes Summarizer":

    st.title("📝 AI Notes Summarizer")

    notes = st.text_area(
        "Paste Long Notes",
        height=300
    )

    if st.button("🧠 Summarize Notes"):

        prompt = f"""
        Summarize these notes into short points:

        {notes}
        """

        try:

            completion = client.chat.completions.create(

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                model="llama-3.3-70b-versatile"
            )

            result = completion.choices[0].message.content

            st.success(result)

        except Exception as e:

            st.error(e)

# ========================= FOOTER =========================
st.markdown("""
<hr>
<center>
<h4>
Made with ❤️ using Streamlit, NLP & AI
</h4>
</center>
""", unsafe_allow_html=True)
