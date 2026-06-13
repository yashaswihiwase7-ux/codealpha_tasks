from tkinter import *
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyttsx3

root = Tk()
root.title("Language Translation Tool")
root.geometry("850x550")
root.resizable(False, False)

engine = pyttsx3.init()

languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Russian": "ru"
}

def translate_text():
    text = input_text.get("1.0", END).strip()

    if text == "":
        messagebox.showwarning("Warning", "Please enter text")
        return

    source = languages[source_lang.get()]
    target = languages[target_lang.get()]

    try:
        translated = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

        output_text.delete("1.0", END)
        output_text.insert(END, translated)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def copy_text():
    translated = output_text.get("1.0", END)

    root.clipboard_clear()
    root.clipboard_append(translated)

    messagebox.showinfo("Copied", "Translated text copied")

def speak_text():
    translated = output_text.get("1.0", END).strip()

    if translated:
        engine.say(translated)
        engine.runAndWait()

title = Label(
    root,
    text="Language Translation Tool",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

frame = Frame(root)
frame.pack(pady=10)

Label(frame, text="Source Language").grid(row=0, column=0, padx=20)

source_lang = ttk.Combobox(
    frame,
    values=list(languages.keys()),
    width=20,
    state="readonly"
)
source_lang.grid(row=1, column=0)
source_lang.set("English")

Label(frame, text="Target Language").grid(row=0, column=1, padx=20)

target_lang = ttk.Combobox(
    frame,
    values=list(languages.keys()),
    width=20,
    state="readonly"
)
target_lang.grid(row=1, column=1)
target_lang.set("Hindi")

Label(root, text="Enter Text").pack()

input_text = Text(root, height=8, width=90)
input_text.pack(pady=5)

Button(
    root,
    text="Translate",
    font=("Arial", 12),
    command=translate_text
).pack(pady=10)

Label(root, text="Translated Text").pack()

output_text = Text(root, height=8, width=90)
output_text.pack(pady=5)

button_frame = Frame(root)
button_frame.pack(pady=10)

Button(
    button_frame,
    text="Copy",
    width=15,
    command=copy_text
).grid(row=0, column=0, padx=10)

Button(
    button_frame,
    text="Speak",
    width=15,
    command=speak_text
).grid(row=0, column=1, padx=10)

root.mainloop()