#! game/game.py python3
"""
This module is the core of Game. The idea behind the game is the following:
there is a meaning of a particular word. All words that are in this meaning and in the title of this word with high
similarity () are replaced by underscore. You need to select one of 4 options. If it's write you will get the full
description of this word.

For example:
    The question is:
        ________ is an interpreted, high-level, general-purpose ________ ________.
        Created by Guido van Rossum and first released in 1991, ________ has a design philosophy
        that emphasizes code readability, notably using significant whitespace.
        It provides constructs that enable clear ________ on both small and large scales.

    Options: ['Python (programming language)', 'New York City', 'Statistics', 'Computer science']
    Answer: Python (programming language)
    Original Text:
        Python is an interpreted, high-level, general-purpose programming language.
        Created by Guido van Rossum and first released in 1991, Python has a design philosophy
        that emphasizes code readability, notably using significant whitespace.
        It provides constructs that enable clear programming on both small and large scales.

The word similarity is calculated by the Levenshtein algorithm.
If the coefficient of similarity is higher than 67%, two string are consider to be similar and replaced with underscore.

"""


from difflib import SequenceMatcher
from repository.db_setup import Repository
from random import shuffle
from constants import DB_PATH
import re


class Game:
    """This class is designed to start a game. When initialized, the random words are selected from the database.
    Args:
        repo: Repository object (database)
        questions: number of question. By default questions=10
    """
    def __init__(self, repo: Repository, questions=10):
        self.repo = repo
        self.questions = questions
        self.words = repo.get_random_words(self.questions)
        self.questions = questions if questions * 4 == len(self.words) else len(self.words) // 4

    def get_questions(self) -> list:
        """This function parse result retruned from the database and aggregate it into the proper from
        (see class 'Question'). Every 4th word in 'questions' is considered to be questions and
        3 previous words are options. After choosing, all 4 options are suffered.

        Returns:
            questions: list of Question objects
        """

        questions = []

        for q in range(self.questions):
            title, meaning = self.words[q*4].title, self.words[q*4].meaning
            question = self._build_question(title, meaning)
            options = list(word.title for word in self.words[q*4:q*4+4])
            shuffle(options)
            questions.append(Question(answer=title, question=question,
                                      options=options, init_text=meaning))

        return questions

    def write_statistics(self, correct_answers: int, time_spent) -> None:
        """Write the result of the game into the database.
        Args:
            correct_answers: int, number of correct answers
            time_spent: float, time spent from the 1st question up to the last question.
        """

        self.repo.insert_statistic(correct_answers, time_spent, self.questions)

    @staticmethod
    def _build_question(title: str, meaning: str) -> str:
        """Static methods that takes title (aka word) and its meaning.
        All symbols in meaning and title that are not words or numbers are excluded.
        Than, title and meaning are split into lists and compared word by word.
        If ration of similarity is higher than 0.67, the following word is replaced with underscore.
        Returns:
            text - str, a new meaning (question) of a title (word) where all similar words are replaced with underscore.
        """
        regex = re.compile('[^a-zA-Z0-9_]')
        text = meaning

        split_title = list(regex.sub('', word.lower()) for word in title.split(' '))
        split_meaning = list(regex.sub('', word.lower()) for word in meaning.split(' '))

        for w1 in split_title:
            for w2 in split_meaning:
                if SequenceMatcher(a=w1, b=w2).ratio() >= .67:
                    text = re.sub(w2, '_'*8, text, flags=re.IGNORECASE)

        return text


class Question:
    """This class represents the Question object.
    Args:
        answer: str, answer for the question
        question: str, question (init_text with replaced similar words
        options: list, list of 4 possible options for a given question
        init_text: str, original text
    """

    def __init__(self, answer: str, question: str, options: list, init_text: str):
        self.answer = answer
        self.question = question
        self.options = options
        self.init_text = init_text

    def __repr__(self):
        return '{}'.format(self.__dict__)


if __name__ == '__main__':
    x = Game(Repository(DB_PATH))
    for i in x.get_questions():
        print(i.question)
        print(i.options)
        print(i.answer)
        print(i.init_text)
        print()
