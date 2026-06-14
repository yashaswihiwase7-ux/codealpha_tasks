
import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import string
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')


data = pd.read_csv(r"C:\Users\Asus Tuf\codealpha\faq_data.csv")

questions = data["question"].tolist()
answers = data["answer"].tolist()

stop_words = set(stopwords.words("english"))

def preprocess(text):
    text = text.lower()

    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )

    words = word_tokenize(text)

    words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(words)

processed_questions = [
    preprocess(question)
    for question in questions
]

vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(
    processed_questions
)

def get_response(user_input):

    processed_input = preprocess(user_input)

    input_vector = vectorizer.transform(
        [processed_input]
    )

    similarity_scores = cosine_similarity(
        input_vector,
        faq_vectors
    )

    best_match_index = similarity_scores.argmax()

    highest_score = similarity_scores[0][best_match_index]

    if highest_score < 0.2:
        return "Sorry, I could not find a relevant answer."

    return answers[best_match_index]

def send_message():

    user_message = entry_box.get()

    if user_message.strip() == "":
        return

    chat_area.config(state=tk.NORMAL)

    chat_area.insert(
        tk.END,
        "You: " + user_message + "\n"
    )

    bot_reply = get_response(user_message)

    chat_area.insert(
        tk.END,
        "Bot: " + bot_reply + "\n\n"
    )

    chat_area.config(state=tk.DISABLED)

    entry_box.delete(0, tk.END)

window = tk.Tk()

window.title("FAQ Chatbot")

window.geometry("700x500")

chat_area = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    state=tk.DISABLED,
    font=("Arial", 11)
)

chat_area.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

entry_box = tk.Entry(
    window,
    font=("Arial", 12)
)

entry_box.pack(
    padx=10,
    pady=5,
    fill=tk.X
)

send_button = tk.Button(
    window,
    text="Send",
    command=send_message,
    font=("Arial", 12)
)

send_button.pack(
    pady=5
)

window.mainloop()