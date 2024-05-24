import tkinter as tk
from tkinter import ttk
import time
import difflib


class TypingSpeedApp:

    def __init__(self):
        self.init_variables()
        self.setup_window()
        self.create_widgets()
        self.display_text(self.display_lines)  # Display the instructional text

    def init_variables(self):
        self.timer_running = False
        self.start_time = 0
        self.word_count = 0
        self.accuracy_pct = 0
        self.wpm_calculation = 0
        self.instructional_text = ["This app allows you to check your typing speed. \n"
                                   "A set of words will be added after the START button is pressed. \n"
                                   "After each word, type a SINGLE SPACE. \n"
                                   "While typing, the test measures words per minute typed,\n"
                                   "as well as accuracy displayed as a percentage. \n"
                                   "Each mistake counts."]
        self.test_lines = ""
        self.display_lines = self.instructional_text

    def setup_window(self):
        self.window = tk.Tk()
        self.window.title("Typing Speed App")
        self.window.minsize(150, 150)
        self.window.config(padx=30, pady=10, bg="#000033")

    def create_widgets(self):
        self.create_text_frame()
        self.create_timer_label()
        self.create_button_frame()
        self.create_entry_frame()
        self.create_source_text_frame()

    def get_test_lines(self, test_lines):
        self.test_lines = test_lines

    def set_display_lines(self):
        self.display_lines = self.test_lines.split('\n')

    def create_text_frame(self):
        self.text_frame = tk.Frame(self.window, bg='#000033')
        self.text_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        self.text_widget = tk.Text(
            self.text_frame, font=('Helvetica', 18), bg='#000033', fg='white',
            wrap="word", width=60, height=15
        )
        self.text_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_widget.yview)
        self.text_widget.config(state="disabled")

    def create_timer_label(self):
        self.timer_label = tk.Label(
            self.window, font=('Helvetica', 24), text="01:00", bg='#000033', fg='white'
        )
        self.timer_label.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.wpm_label = tk.Label(
            self.window, font=('Helvetica', 18), text=f"WPM: {self.wpm_calculation}", bg='#000033', fg='white'
        )
        self.wpm_label.grid(row=1, column=1, padx=20, pady=(5, 0), sticky="nsew")

        self.accuracy_label = tk.Label(
            self.window, font=('Helvetica', 18), text=f"Accuracy %: {self.accuracy_pct:.2f}", bg='#000033', fg='white'
        )
        self.accuracy_label.grid(row=2, column=1, padx=20, pady=(5, 20), sticky="nsew")

    def create_button_frame(self):
        button_frame = tk.Frame(self.window, bg='#000033')
        button_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        start_button = tk.Button(
            button_frame, text="Start", command=self.start_countdown, bg='#003366', fg='white', padx=10
        )
        start_button.grid(row=0, column=0, padx=10)

        reset_button = tk.Button(
            button_frame, text="Reset", command=self.reset_countdown, bg='#003366', fg='white', padx=10
        )
        reset_button.grid(row=0, column=2, padx=10)

    def create_entry_frame(self):
        self.entry_frame = tk.Frame(self.window, bg='#000033')
        self.entry_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.entry_label = tk.Label(
            self.entry_frame, font=('Helvetica', 18), text="Please enter text:", bg='#000033', fg='white'
        )
        self.entry_label.grid(row=0, column=0, padx=10, pady=10)

        self.entry_box = tk.Entry(
            self.entry_frame, font=('Helvetica', 14), bg='#003366', fg='white'
        )
        self.entry_box.grid(row=0, column=1, padx=10, pady=10)

        self.entry_box.bind("<KeyRelease>", self.update_metrics)  # Bind key release event to update metrics

        compare_button = tk.Button(
            self.entry_frame, text="Submit", command=self.compare_text, bg='#003366', fg='white', padx=10
        )
        compare_button.grid(row=0, column=2, padx=10, pady=10)

        self.result_label = tk.Label(
            self.entry_frame, font=('Helvetica', 14), bg='#000033', fg='white'
        )
        self.result_label.grid(row=1, columnspan=3, padx=10, pady=10)

    def create_source_text_frame(self):
        self.source_text_frame = tk.Frame(self.window, bg='#000033')
        self.source_text_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.source_text_label = tk.Label(
            self.source_text_frame, font=('Helvetica', 18), text="Enter source text:", bg='#000033', fg='white'
        )
        self.source_text_label.grid(row=0, column=0, padx=10, pady=10)

        self.source_text_entry = tk.Entry(
            self.source_text_frame, font=('Helvetica', 14), bg='#003366', fg='white', width=85
        )
        self.source_text_entry.grid(row=0, column=1, padx=10, pady=10)

    def start_countdown(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.word_count = 0
            self.entry_box.delete(0, tk.END)
            self.result_label.config(text="")
            self.set_display_lines()
            self.display_text(self.display_lines)
            self.countdown(60)

    def countdown(self, time_left):
        if time_left >= 0:
            minutes, seconds = divmod(time_left, 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_str)
            self.timer = self.window.after(1000, self.countdown, time_left - 1)
        else:
            self.timer_label.config(text="Time's up!")
            self.calculate_wpm()
            self.timer_running = False

    def reset_countdown(self):
        if self.timer_running:
            self.window.after_cancel(self.timer)
            self.timer_running = False
        self.timer_label.config(text="01:00")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy %: 0")
        self.entry_box.delete(0, tk.END)
        self.result_label.config(text="")
        self.display_lines = self.instructional_text
        self.display_text(self.display_lines)

    def display_text(self, lines):
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        for line in lines:
            self.text_widget.insert("end", line + "\n")
        self.text_widget.config(state="disabled")

    def calculate_wpm(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        user_input = self.entry_box.get()
        user_words = user_input.split()
        text_words = ' '.join(self.display_lines).split()

        total_words_typed = len(user_words)
        mistakes = sum(1 for user_word, text_word in zip(user_words, text_words) if user_word != text_word)
        correct_words = total_words_typed - mistakes

        elapsed_minutes = elapsed_time / 60
        self.wpm_calculation = correct_words / elapsed_minutes if elapsed_minutes > 0 else 0

        partial_text = ' '.join(text_words[:total_words_typed])
        self.accuracy_pct = self.calculate_accuracy(user_input, partial_text)

        # Display typing speed and accuracy
        self.result_label.config(text=f"Your typing speed is: {self.wpm_calculation:.2f} WPM\nAccuracy: {self.accuracy_pct:.2f}%")
        self.wpm_label.config(text=f"WPM: {self.wpm_calculation:.2f}")
        self.accuracy_label.config(text=f"Accuracy %: {self.accuracy_pct:.2f}")

    def calculate_accuracy(self, user_input, reference_text):
        matcher = difflib.SequenceMatcher(None, user_input.split(), reference_text.split())
        return matcher.ratio() * 100

    def compare_text(self):
        self.stop_countdown()
        self.calculate_wpm()

    def update_metrics(self, event):
        if self.timer_running:
            self.calculate_wpm()

    def stop_countdown(self):
        if self.timer_running:
            self.window.after_cancel(self.timer)
            self.timer_running = False

    def start_mainloop(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TypingSpeedApp()
    app.start_mainloop()
