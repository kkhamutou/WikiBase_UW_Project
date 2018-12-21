#!case_listbox.py Python3
import random
import time


class CaseListbox:

    def __init__(self, start="1/1/2000 1:30 PM", end="1/1/2018 1:30 PM", time_format='%m/%d/%Y %I:%M %p'):
        self.start = start
        self.end = end
        self.time_format = time_format

    def _random_date(self, prop):

        stime = time.mktime(time.strptime(self.start, self.time_format))
        etime = time.mktime(time.strptime(self.end, self.time_format))
        ptime = stime + prop * (etime - stime)

        return time.strftime(self.time_format, time.localtime(ptime))

    @staticmethod
    def normalized(word):
        return word.strip().replace('_', '').capitalize()

    def case_data(self, interval=1):

        test_case = []
        counter = 0

        with open('/Users/kirylkhamutou/IdeaProjects/WikiBase_UW_Project/test_cases/words', 'r') as words:
            for line in words:
                counter += 1
                if counter % interval == 0:
                    test_case.append([counter, random.randint(10000000, 99999999),
                                      CaseListbox.normalized(line), line, self._random_date(random.random())]
                                     )
        return tuple(test_case)


if __name__ == '__main__':
    x = CaseListbox()
    t = x.case_data()
