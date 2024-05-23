import tkinter as tk
from tkinter import ttk
import time
from text import long_text

# Initialize variables
timer_running = False
start_time = 0
word_count = 0
lines = long_text.splitlines()

def reset_countdown():
    global timer_running
    if timer_running:
        stop_countdown()
    timer_label.config(text="01:00")

def start_countdown():
    global timer_running, start_time, word_count
    if not timer_running:
        timer_running = True
        start_time = time.time()
        word_count = 0
        countdown(60)
        display_text(lines)

def stop_countdown():
    global timer_running
    if timer_running:
        root.after_cancel(timer)
        timer_running = False
        timer_label.config(text="Stopped")

def countdown(time_left):
    global timer
    if time_left >= 0:
        minutes, seconds = divmod(time_left, 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        timer_label.config(text=time_str)
        timer = root.after(1000, countdown, time_left - 1)
    else:
        timer_label.config(text="Time's up!")
        global timer_running
        timer_running = False
        calculate_wpm()

def display_text(lines):
    text_widget.config(state="normal")
    text_widget.delete("1.0", "end")
    for line in lines:
        text_widget.insert("end", line + "\n")
    text_widget.config(state="disabled")

    scrollbar.config(command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)

def calculate_wpm():
    global start_time, word_count, lines
    end_time = time.time()
    elapsed_time = end_time - start_time
    user_input = entry_box.get()
    user_words = user_input.split()
    text_words = ' '.join(lines).split()

    mistakes = sum(1 for user_word, text_word in zip(user_words, text_words) if user_word != text_word)
    effective_word_count = max(0, len(user_words) - mistakes)
    wpm = int(effective_word_count / (elapsed_time / 60))

    accuracy = calculate_accuracy(user_input, ' '.join(lines))
    
    # Display typing speed and accuracy
    result_label.config(text=f"Your typing speed is: {wpm} WPM\nAccuracy: {accuracy:.2f}%")

def calculate_accuracy(user_input, reference_text):
    user_words = user_input.split()
    reference_words = reference_text.split()

    min_length = min(len(user_words), len(reference_words))
    correct_count = sum(1 for user_word, ref_word in zip(user_words[:min_length], reference_words[:min_length]) if user_word == ref_word)
    accuracy = (correct_count / min_length) * 100
    return accuracy

def compare_text():
    global word_count, lines
    user_input = entry_box.get().strip()
    user_words = user_input.split()
    text_words = ' '.join(lines).split()

    min_length = min(len(user_words), len(text_words))
    
    correct_count = 0
    for user_word, text_word in zip(user_words[:min_length], text_words[:min_length]):
        if user_word == text_word:
            correct_count += 1

    accuracy = (correct_count / min_length) * 100
    print(f"Accuracy: {accuracy:.2f}%")


# Create the main window
root = tk.Tk()
root.title("Typing WPM Test")
root.configure(bg='#000033')

# Create a frame for the text widget
text_frame = tk.Frame(root, bg='#000033')
text_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Create a Text widget for displaying the text 
text_widget = tk.Text(text_frame, font=('Helvetica', 18), bg='#000033', fg='white', wrap="word", width=60, height=15)
text_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Configure vertical scrollbar
scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
text_widget.config(yscrollcommand=scrollbar.set)

# Configure grid weights for text frame
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_columnconfigure(0, weight=1)

# Create a frame for the timer label
timer_frame = tk.Frame(root, bg='#000033')
timer_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

# Create a label to display the time
timer_label = tk.Label(timer_frame, font=('Helvetica', 24), text="01:00", bg='#000033', fg='white')
timer_label.pack(pady=20)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg='#000033')
button_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

# Create buttons to start, stop, and reset the countdown
start_button = tk.Button(button_frame, text="Start", command=start_countdown, bg='#003366', fg='white', padx=10)
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="Stop", command=stop_countdown, bg='#003366', fg='white', padx=10)
stop_button.grid(row=0, column=1, padx=10)

reset_button = tk.Button(button_frame, text="Reset", command=reset_countdown, bg='#003366', fg='white', padx=10)
reset_button.grid(row=0, column=2, padx=10)

# Create a frame for the entry box and label
entry_frame = tk.Frame(root, bg='#000033')
entry_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

# Create a label for the entry box
entry_label = tk.Label(entry_frame, font=('Helvetica', 18), text="Please enter text:", bg='#000033', fg='white')
entry_label.grid(row=0, column=0, padx=10, pady=10)

# Create an entry box for users to type words into
entry_box = tk.Entry(entry_frame, font=('Helvetica', 14), bg='#003366', fg='white')
entry_box.grid(row=0, column=1, padx=10, pady=10)

# Create a label to display typing speed and accuracy
result_label = tk.Label(entry_frame, font=('Helvetica', 14), bg='#000033', fg='white')
result_label.grid(row=1, columnspan=3, padx=10, pady=10)

# Create a button to compare text
compare_button = tk.Button(entry_frame, text="Submit", command=compare_text, bg='#003366', fg='white', padx=10)
compare_button.grid(row=0, column=2, padx=10, pady=10)

# Run the Tkinter event loop

root.mainloop()
