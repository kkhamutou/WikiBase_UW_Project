#!gui/game_window.py python3
"""
game_window is designed to sore all corresponding functions and classes regarding game frame on the main window.
The idea of the game described in  /game/game.py. This module put GUI above the main idea.
Game is ended when the last question is answered.
"""

import tkinter as tk
import tkinter.messagebox as msg
import time
from game.game import Game
from constants import DB_PATH
from repository.db_setup import Repository


class GameMain(tk.Frame):
    """Game fame.
        args:
            game: Game object
            questions: list, list of Question objects
            questionIterator: list_iterator, iterator for questions
            question: object, current Question object
            isOver: bool, true if game is over, otherwise false
            pressed: bool, true is answer option button is pressed, otherwise false
            cur_question: int, current number of a question
            count_answer: int, number of correct answers
            num_of_questions: int, total number of questions
            start_time: object, started time of a game
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.game = Game(Repository(DB_PATH))

        self.questions = self.game.get_questions()
        self.questionIterator = iter(self.questions)
        self.question = None

        self.isOver = False
        self.pressed = True
        self.cur_question = 0

        self.count_answer = 0
        self.num_of_questions = len(self.questions)

        self._build_widgets()
        self.next_question()

        self.start_time = time.time()

    def _build_widgets(self):
        """build all widgets for the frame."""

        fm_top = tk.Frame(self)
        fm_top.pack(side=tk.TOP, fill=tk.X, pady=20, padx=5)

        fm_question = tk.Frame(self)
        fm_question.pack(side=tk.TOP, fill=tk.Y, expand=True)

        fm_next = tk.Frame(self)
        fm_next.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)

        self.btn_home = tk.Button(fm_top, text='Home')
        self.btn_home.pack(side=tk.LEFT)

        self.lbl_question = tk.Label(fm_question, wraplength=400)
        self.lbl_question.pack(expand=True, fill=tk.BOTH)

        self._build_buttons()

        self.btn_next_question = tk.Button(fm_next, text='Next question', command=self.next_question)
        self.btn_next_question.pack()

        self.lbl_counter = tk.Label(fm_next,
                                    text=f'Questions left: {self.num_of_questions}\n'
                                    f'Correct answers: {self.count_answer}/{self.num_of_questions}')
        self.lbl_counter.pack(side=tk.BOTTOM, pady=35)

    def _build_buttons(self):
        """build option buttons for the frame."""

        self.fm_option = tk.Frame(self)
        self.fm_option.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)

        for i in range(4):
            btn = tk.Button(self.fm_option,  bd=0)
            btn.configure(command=lambda j=btn: self.is_correct(j))
            btn.grid(row=i//2, column=0 if i % 2 == 0 else 1, padx=7, pady=7, sticky="ew")

    def is_correct(self, button: tk.Button):
        """This is an event assigned to all option buttons.
        if any of options is selected, than the result is checked.
        If you select correct answer, the foreground=green, otherwise red.
        After you select the answer, all buttons are disabled in order to prevent multiple answers.
        """

        if not self.pressed:
            self.pressed = True
            self.lbl_question['text'] = self.question.init_text
            self.cur_question += 1

            if button['text'] == self.question.answer:
                button['foreground'] = 'green'
                self.count_answer += 1
            else:
                button['foreground'] = 'red'
                for btn in self.fm_option.winfo_children():
                    btn['foreground'] = 'green' if btn['text'] == self.question.answer else None

            self.lbl_counter['text'] = f'Questions left: {self.num_of_questions-self.cur_question}\n' \
                                       f'Correct answers: {self.count_answer}/{self.num_of_questions}'

            if self.num_of_questions-self.cur_question == 0:
                self.next_question()

    def exit_game_window(self):
        """Check if game is in progress and ask when you re sure to exit it."""

        if not self.isOver:
            exit_msg = msg.askquestion('Game is running',
                                       'Are you sure you want to exit the game?\nYou result will be lost!')
            return True if exit_msg == 'yes' else False
        return True

    def next_question(self):
        """Next question button. Show the next question if there is such, otherwise show the result and write
        the statistics in the database."""

        if self.pressed:

            try:
                self.question = next(self.questionIterator)
            except StopIteration:
                self.pressed = True
                time_sent = time.time() - self.start_time
                self.game.write_statistics(self.count_answer, time_sent)

                msg.showinfo('Result', f"""
                Game is over.
                Number of correct answers: {self.count_answer}/{self.num_of_questions}
                Time spent: {time.strftime("%H:%M:%S", time.gmtime(time_sent))}""")

                self.isOver = True
                self.btn_home.invoke()

            else:
                self.pressed = False
                self.lbl_question['text'] = self.question.question

                for index, btn in enumerate(self.fm_option.winfo_children()):
                    btn['text'] = self.question.options[index]
                    btn["foreground"] = 'SystemButtonText'
        else:
            msg.showinfo('Missing', 'Please, select the answer!')


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x600')
    x = GameMain(root)
    x.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
    x.mainloop()
