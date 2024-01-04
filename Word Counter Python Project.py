import tkinter as tk
from tkinter import filedialog, messagebox
import re
from collections import Counter
from datetime import datetime
import string

def count_punctuation(text):
    punctuation_count = Counter([char for char in text if char in string.punctuation])
    return punctuation_count

def count_words(text, ignore_punctuation=False, count_punctuation_line=False):
    if ignore_punctuation:
        text = re.sub(r'[^\w\s]', '', text)
    
    words = re.findall(r'\w+', text)
    word_count = len(words)

    if count_punctuation_line:
        punctuation_count = count_punctuation(text)
    else:
        punctuation_count = Counter()

    letter_count = Counter(text.replace('\n', '').replace('\r', ''))

    return word_count, letter_count, punctuation_count

def calculate_word_count():
    input_text = text_entry.get("1.0", tk.END).strip()
    ignore_punctuation = punctuation_checkbox_var.get()
    count_punctuation_line = punctuation_line_checkbox_var.get()

    if input_text:
        word_count, letter_count, punctuation_count = count_words(input_text, ignore_punctuation, count_punctuation_line)
        update_result_labels(word_count, letter_count, punctuation_count)
        save_to_history(word_count, letter_count, punctuation_count)
    else:
        messagebox.showerror("Error", "Input is empty. Please enter text.")

def browse_file():
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(tk.END, file_path)

def calculate_word_count_from_file():
    file_path = file_path_entry.get()
    ignore_punctuation = punctuation_checkbox_var.get()
    count_punctuation_line = punctuation_line_checkbox_var.get()

    if file_path:
        word_count, letter_count, punctuation_count = count_words_from_file(file_path, ignore_punctuation, count_punctuation_line)
        update_result_labels(word_count, letter_count, punctuation_count)
        save_to_history(word_count, letter_count, punctuation_count)
    else:
        messagebox.showerror("Error", "File path is empty. Please choose a file.")

def save_to_history(word_count, letter_count, punctuation_count):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    result = f"{timestamp}\nWord Count: {word_count}\nLetter Count: {letter_count}\nPunctuation Count: {punctuation_count}\n\n"
    
    with open("history.txt", "a") as history_file:
        history_file.write(result)

def update_result_labels(word_count, letter_count, punctuation_count):
    word_count_label.config(text=f"Word Count: {word_count}")
    letter_count_label.config(text=f"Letter Count: {letter_count}")
    punctuation_count_label.config(text=f"Punctuation Count: {punctuation_count}")

def start_main_functionality():
    welcome_frame.pack_forget()
    main_frame.pack()

def save_history():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    
    if file_path:
        try:
            with open(file_path, "w") as history_file:
                with open("history.txt", "r") as temp_file:
                    history_file.write(temp_file.read())
            messagebox.showinfo("Success", "History saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving history: {str(e)}")

# Customizing the Tkinter window
window = tk.Tk()
window.title("Word Counter SR")
window.geometry("800x500")  # Set a custom window size

# Color palette
background_color = "#f0f0f0"
text_color = "#333333"
button_color = "#4caf50"
button_text_color = "white"

window.configure(bg=background_color)

# Welcome Frame
welcome_frame = tk.Frame(window, bg=background_color)
welcome_frame.pack(padx=20, pady=20)

welcome_label = tk.Label(welcome_frame, text="Welcome to  Word Counter Application!", bg=background_color, fg=text_color, font=("Helvetica", 20))
welcome_label.pack(pady=10)

start_button = tk.Button(welcome_frame, text="Start", command=start_main_functionality, bg=button_color, fg=button_text_color, font=("Helvetica", 16))
start_button.pack()

# Main Frame
main_frame = tk.Frame(window, bg=background_color)

# Create and place widgets
text_entry = tk.Text(main_frame, height=10, width=60, bg=background_color, fg=text_color, font=("Helvetica", 14))
text_entry.pack(pady=10)

punctuation_checkbox_var = tk.BooleanVar()
punctuation_checkbox = tk.Checkbutton(main_frame, text="Ignore Punctuation", variable=punctuation_checkbox_var, bg=background_color, fg=text_color, font=("Helvetica", 14))
punctuation_checkbox.pack()

punctuation_line_checkbox_var = tk.BooleanVar()
punctuation_line_checkbox = tk.Checkbutton(main_frame, text="Count Punctuation on Separate Line", variable=punctuation_line_checkbox_var, bg=background_color, fg=text_color, font=("Helvetica", 14))
punctuation_line_checkbox.pack()

count_button = tk.Button(main_frame, text="Count Words", command=calculate_word_count, bg=button_color, fg=button_text_color, font=("Helvetica", 16))
count_button.pack(pady=10)

word_count_label = tk.Label(main_frame, text="Word Count: ", bg=background_color, fg=text_color, font=("Helvetica", 14))
word_count_label.pack()

letter_count_label = tk.Label(main_frame, text="Letter Count: ", bg=background_color, fg=text_color, font=("Helvetica", 14))
letter_count_label.pack()

punctuation_count_label = tk.Label(main_frame, text="Punctuation Count: ", bg=background_color, fg=text_color, font=("Helvetica", 14))
punctuation_count_label.pack()

save_history_button = tk.Button(main_frame, text="Save History", command=save_history, bg=button_color, fg=button_text_color, font=("Helvetica", 16))
save_history_button.pack(pady=10)

# Run the main loop
window.mainloop()
