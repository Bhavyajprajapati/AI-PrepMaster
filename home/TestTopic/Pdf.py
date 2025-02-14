from fpdf import FPDF
from datetime import datetime
import streamlit as st
import io
import zipfile


class QuizPDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Arial", "B", 9)
        self.cell(
            0,
            10,
            f'Quiz Report - Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            0,
            1,
            "R",
        )
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 5)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def create_title(self, title):
        self.add_page()
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, title, 0, 1, "C")
        self.ln(10)

    def create_questions_only(self, questions):
        self.set_font("Arial", "", 11)
        for i, question in enumerate(questions):
            self.set_font("Arial", "B", 10)
            self.multi_cell(0, 10, f"Q{i+1} :- {question['Mcq']}")

            self.set_font("Arial", "", 9)
            for option_key, option_value in question["Options"].items():
                self.multi_cell(0, 10, f"   {option_key}) {option_value}")
            self.ln(5)

    def create_answers_only(self, questions):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 10, "Correct Answers:")
        for i, question in enumerate(questions):
            self.set_font("Arial", "B", 10)

            correct_option = question["Correct_option"]
            correct_answer = question["Options"][correct_option]
            self.set_font("Arial", "", 9)
            self.multi_cell(0, 10, f"{correct_option} ) {correct_answer}")
            self.ln(5)

    def create_quiz_with_user_answers(self, questions, selected_options):
        self.set_font("Arial", "", 11)
        for i, question in enumerate(questions):
            self.set_font("Arial", "B", 10)
            self.multi_cell(0, 10, f"Q{i+1} :- {question['Mcq']}")

            self.set_font("Arial", "", 9)
            for option_key, option_value in question["Options"].items():
                prefix = (
                    " * "
                    if selected_options
                    and i in selected_options
                    and option_value == selected_options[i]
                    else "   "
                )
                self.multi_cell(0, 10, f"{prefix}{option_key}) {option_value}")

            if selected_options and i in selected_options:
                self.set_font("Arial", "I", 9)
                self.multi_cell(0, 10, f"Your answer: {selected_options[i]}")
            self.ln(5)


def generate_all_quiz_pdfs(quiz_data):
    """Generate three separate PDFs for questions, answers, and user responses."""

    # Generate questions-only PDF
    pdf_questions = QuizPDFGenerator()
    pdf_questions.create_title("Quiz Questions")
    if hasattr(st.session_state, "quiz_level"):
        pdf_questions.set_font("Arial", "", 12)
        pdf_questions.cell(
            0, 10, f"Difficulty Level: {st.session_state.quiz_level}", 0, 1
        )
    pdf_questions.create_questions_only(quiz_data["questions"])

    # Generate answers-only PDF
    pdf_answers = QuizPDFGenerator()
    pdf_answers.create_title("Quiz Answers")
    if hasattr(st.session_state, "quiz_level"):
        pdf_answers.set_font("Arial", "", 12)
        pdf_answers.cell(
            0, 10, f"Difficulty Level: {st.session_state.quiz_level}", 0, 1
        )
    pdf_answers.create_answers_only(quiz_data["questions"])

    # Generate user responses PDF
    pdf_user_answers = QuizPDFGenerator()
    pdf_user_answers.create_title("Quiz with Your Responses")
    if hasattr(st.session_state, "quiz_level"):
        pdf_user_answers.set_font("Arial", "", 12)
        pdf_user_answers.cell(
            0, 10, f"Difficulty Level: {st.session_state.quiz_level}", 0, 1
        )
    pdf_user_answers.create_quiz_with_user_answers(
        quiz_data["questions"], quiz_data.get("selected_options", {})
    )

    # Add score to user responses PDF
    if "selected_options" in quiz_data:
        correct_count = sum(
            1
            for i, question in enumerate(quiz_data["questions"])
            if quiz_data["selected_options"].get(i)
            == question["Options"].get(question["Correct_option"])
        )
        pdf_user_answers.add_page()
        pdf_user_answers.set_font("Arial", "B", 16)
        pdf_user_answers.cell(0, 10, "Quiz Results", 0, 1, "C")
        pdf_user_answers.ln(10)
        pdf_user_answers.set_font("Arial", "B", 10)
        pdf_user_answers.cell(
            0, 10, f"Final Score: {correct_count}/{len(quiz_data['questions'])}", 0, 1
        )

    return {
        "questions": pdf_questions.output(dest="S").encode("latin-1", errors="replace"),
        "answers": pdf_answers.output(dest="S").encode("latin-1", errors="replace"),
        "user_responses": pdf_user_answers.output(dest="S").encode(
            "latin-1", errors="replace"
        ),
    }


def generate_answer_key_text(quiz_data):
    """Generate a text file with comma-separated answer keys."""
    answer_keys = [question["Correct_option"].capitalize() for question in quiz_data["questions"]]
    return ",".join(answer_keys)


def generate_quiz_zip(quiz_data):
    """Generate a ZIP file containing all three PDFs and the answer key text file."""
    pdfs = generate_all_quiz_pdfs(quiz_data)

    # Generate answer key text
    answer_key_text = generate_answer_key_text(quiz_data)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        zip_file.writestr("quiz_questions.pdf", pdfs["questions"])
        zip_file.writestr("quiz_answers.pdf", pdfs["answers"])
        zip_file.writestr("quiz_with_responses.pdf", pdfs["user_responses"])
        zip_file.writestr("answer_key.txt", answer_key_text)

    zip_buffer.seek(0)
    return zip_buffer