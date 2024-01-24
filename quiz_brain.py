import html
from data import APIResponse

api = APIResponse()


class QuizBrain:

    def __init__(self):
        self.question_number = 0
        self.score = 0
        self.current_question = None
        self.question_list = None
        self.get_question_bank()

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question["question"])
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        correct_answer = self.current_question["correct_answer"]
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False

    def get_question_bank(self):
        self.question_list = [{"question": ques["question"], "correct_answer": ques["correct_answer"]} for ques in
                              api.get_response()]
