from tkinter import *
from tkinter import ttk
from quiz_brain import QuizBrain
from data import parameter

THEME_COLOR = "#375362"
SETTINGS_COLOR = "#00ffcc"
SETTINGS_FONT = ("Ariel", 11)
MY_CATEGORIES = {
    "General": "",
    "General Knowledge": "9",
    "Entertainment: Books": "10",
    "Film": "11",
    "Music": "12",
    "Musicals & Theatres": "13",
    "Television": "14",
    "Video Games": "15",
    "Board Games": "16",
    "Science & Nature": "17",
    "Science: Computers": "18",
    "Science: Mathematics": "19",
    "Mythology": "20",
    "Sports": "21",
    "Geography": "22",
    "History": "23",
    "Politics": "24",
    "Art": "25",
    "Celebrities": "26",
    "Animals": "27",
    "Vehicles": "28",
    "Comics": "29",
    "Science: Gadgets": "30",
    "Japanese Anime & Manga": "31",
    "Cartoon & Animations": "32",
}


class SettingsWindow:

    def __init__(self):
        self.settings_popup = Toplevel()
        self.settings_popup.title("Quizzler - Settings")
        self.settings_popup.iconbitmap("./images/question_mark.ico")
        self.settings_popup.config(bg=THEME_COLOR, padx=20)

        # number of questions label and spinbox
        self.num_of_ques_label = Label(
            self.settings_popup,
            text="Number of questions (Max. 50):    ",
            font=SETTINGS_FONT, bg=THEME_COLOR, fg="white",
            # wraplength=150
        )
        self.num_of_ques_label.grid(row=7, column=0, pady=20)
        self.num_of_ques_spinbox = Spinbox(self.settings_popup, from_=3, to=70, width=28)
        self.num_of_ques_spinbox.grid(row=7, column=1)

        # Combobox for quiz category
        self.category_label = Label(
            self.settings_popup,
            text="Category:",
            font=SETTINGS_FONT, bg=THEME_COLOR, fg="white",
        )
        self.category_label.grid(row=0, column=0, sticky="w", pady=20)

        self.category_state = StringVar()
        category_combobox = ttk.Combobox(self.settings_popup, width=27, textvariable=self.category_state)
        category_combobox["values"] = [item for item in MY_CATEGORIES]
        category_combobox.current(0)
        category_combobox.grid(row=0, column=1)

        # difficulty label and defficulty self listbox
        self.difficulty_label = Label(
            self.settings_popup,
            text="Difficulty:",
            font=SETTINGS_FONT, bg=THEME_COLOR, fg="white",
        )
        self.difficulty_label.grid(row=6, column=0, sticky="w", pady=20)

        self.difficulty_state = StringVar()
        difficulty_combobox = ttk.Combobox(self.settings_popup, width=27, textvariable=self.difficulty_state)
        difficulty_combobox["values"] = ["Easy", "Medium", "Hard"]
        difficulty_combobox.current(0)
        difficulty_combobox.grid(row=6, column=1)

        # apply button and cancel button
        self.apply_button = Button(self.settings_popup, text="Apply", bg="#0000ff", borderwidth=0, fg="white",
                                   font=("Ariel", 11, "bold"), width=22, command=self.apply)
        self.apply_button.grid(row=8, column=0, pady=20, sticky="w")

        self.cancel_button = Button(self.settings_popup, text="Exit", bg="#ff0000", borderwidth=0,
                                    fg="white", font=("Ariel", 11, "bold"), width=22,
                                    command=self.settings_popup.destroy)
        self.cancel_button.grid(row=8, column=1, pady=20)

        self.settings_popup.mainloop()

    def apply(self):
        parameter["amount"] = self.num_of_ques_spinbox.get()
        if int(parameter["amount"]) > 50:
            parameter["amount"] = "50"

        parameter["category"] = MY_CATEGORIES[self.category_state.get()]

        parameter["difficulty"] = self.difficulty_state.get().lower()


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.score = self.quiz.score
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.iconbitmap("./images/question_mark.ico")
        self.window.config(padx=25, pady=20, bg=THEME_COLOR)

        # Canvas for question
        self.canvas = Canvas(width=600, height=350)
        self.ques_label = self.canvas.create_text(
            300,
            175,
            text="......",
            font=("Ariel", 20, "italic"),
            width=550
        )
        self.canvas.grid(row=1, column=0, columnspan=4, pady=20)

        # true and false buttons
        true_image = PhotoImage(file="./images/true.png")
        self.true = Button(image=true_image, borderwidth=0, bg=THEME_COLOR, command=self.if_true)
        self.true.grid(row=2, column=0, pady=20)

        false_image = PhotoImage(file="./images/false.png")
        self.false = Button(image=false_image, borderwidth=0, bg=THEME_COLOR, command=self.if_false)
        self.false.grid(row=2, column=3, pady=20)

        # scoreboard label
        self.scoreboard = Label(
            text=f"Score: {self.quiz.score}",
            font=("Ariel", 15, "bold"), bg=THEME_COLOR,
            fg="white"
        )
        self.scoreboard.grid(row=0, column=3, sticky="e")
        self.get_next_question()

        # Heading label
        self.heading = Label(
            text=f"General",
            font=("Ariel", 15, "bold"), bg=THEME_COLOR,
            fg="white",
            width=30,
        )
        self.heading.grid(row=0, column=1)

        # settings button
        settings_image = PhotoImage(file="./images/settings.png")
        self.settings_button = Button(
            image=settings_image, borderwidth=0,
            bg=THEME_COLOR,
            command=SettingsWindow,
        )
        self.settings_button.grid(row=0, column=0, sticky="w")

        # Restart button
        restart_image = PhotoImage(file="./images/restart.png")
        self.restart_button = Button(image=restart_image, borderwidth=0, bg=THEME_COLOR, command=self.restart)
        self.restart_button.grid(row=0, column=2, sticky="e")

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.configure(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.ques_label, text=q_text)
        else:
            self.finished()
            self.true.config(state="disabled")
            self.false.config(state="disabled")
        self.scoreboard.config(text=f"Score: {self.quiz.score}")

    def if_true(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def if_false(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def finished(self):
        self.canvas.itemconfig(
            self.ques_label,
            text=f"You have completed the Quiz.\nYou Scored {self.quiz.score}/{self.quiz.question_number}",
            font=("Ariel", 30, "bold")
        )

    def give_feedback(self, feed):
        if feed:
            self.canvas.configure(bg="green")
        else:
            self.canvas.configure(bg="red")
        self.window.after(1000, self.get_next_question)

    def restart(self):
        self.quiz.score = 0
        self.quiz.question_number = 0
        self.quiz.get_question_bank()
        self.get_next_question()
        self.canvas.itemconfig(self.ques_label, font=("Ariel", 20, "italic"))
        self.true.config(state="normal")
        self.false.config(state="normal")
        name = [item for item in MY_CATEGORIES if MY_CATEGORIES[item] == parameter["category"]]
        self.heading.config(text=f"{name[0]}")
