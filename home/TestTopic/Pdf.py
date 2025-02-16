from fpdf import FPDF
from datetime import datetime
import streamlit as st
import io
import zipfile36 as zipfile  # Changed to use zipfile36


class QuizPDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(15, 20, 15)  # left, top, right margins

    def header(self):
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, "Ai-prepMaster", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "B", 8)
        self.cell(
            0,
            10,
            f'Quiz Report - Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            new_x="LMARGIN",
            new_y="NEXT",
            align="R",
        )
        self.set_font("helvetica", "I", 5)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def create_title(self, title):
        self.add_page()
        self.set_font("helvetica", "B", 13)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

    def set_highlight_color(self, color):
        """Set fill color based on the specified color name"""
        if color == "yellow":
            self.set_fill_color(255, 255, 0)  # Yellow
        elif color == "green":
            self.set_fill_color(144, 238, 144)  # Light Green
        elif color == "red":
            self.set_fill_color(255, 182, 193)  # Light Red

    def create_questions_only(self, questions):
        self.set_font("helvetica", "", 11)
        for i, question in enumerate(questions):
            self.set_font("helvetica", "B", 10)
            self.multi_cell(
                0, 7, f"Q{i+1} :- {question['Mcq']}", new_x="LMARGIN", new_y="NEXT"
            )

            self.set_font("helvetica", "", 9)
            for option_key, option_value in question["Options"].items():
                self.multi_cell(
                    0,
                    7,
                    f"   {option_key}) {option_value}",
                    new_x="LMARGIN",
                    new_y="NEXT",
                )
            self.ln(3)

    def create_answers_only(self, questions):
        self.set_font("helvetica", "", 11)
        self.multi_cell(0, 7, "Correct Answers:", new_x="LMARGIN", new_y="NEXT")
        for i, question in enumerate(questions):
            correct_option = question["Correct_option"]
            correct_answer = question["Options"][correct_option]
            self.set_font("helvetica", "", 9)
            self.multi_cell(
                0,
                7,
                f"{correct_option}) {correct_answer}",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            self.ln(3)

    def create_quiz_with_user_answers(self, questions, selected_options):
        for i, question in enumerate(questions):
            # Question text
            self.set_font("helvetica", "B", 12)
            self.multi_cell(
                0, 7, f"Q{i+1} :- {question['Mcq']}", new_x="LMARGIN", new_y="NEXT"
            )

            correct_option = question["Correct_option"]
            correct_answer = question["Options"][correct_option]
            user_answer = selected_options.get(i) if selected_options else None

            self.set_font("helvetica", "", 10)
            for option_key, option_value in question["Options"].items():
                # Reset fill color
                fill = False

                if selected_options and i in selected_options:
                    if option_value == user_answer:
                        if option_value == correct_answer:
                            self.set_highlight_color("green")
                            fill = True
                        else:
                            self.set_highlight_color("red")
                            fill = True
                    elif (
                        option_value == correct_answer and user_answer != correct_answer
                    ):
                        self.set_highlight_color("yellow")
                        fill = True

                # Format option text
                prefix = (
                    " * "
                    if (
                        selected_options
                        and i in selected_options
                        and option_value == user_answer
                    )
                    else "   "
                )
                option_text = f"{prefix}{option_key}) {option_value}"

                # Use multi_cell with fill parameter
                self.multi_cell(
                    0, 7, option_text, new_x="LMARGIN", new_y="NEXT", fill=fill
                )

            # Add result text if user answered
            if selected_options and i in selected_options:
                self.set_font("helvetica", "I", 9)
                if user_answer == correct_answer:
                    result_text = "Correct!"
                else:
                    result_text = (
                        f"Incorrect. Correct answer: {correct_option}) {correct_answer}"
                    )
                self.multi_cell(0, 7, result_text, new_x="LMARGIN", new_y="NEXT")

            self.ln(3)


def generate_all_quiz_pdfs(quiz_data):
    """Generate three separate PDFs for questions, answers, and user responses."""
    # Generate questions-only PDF
    pdf_questions = QuizPDFGenerator()
    pdf_questions.create_title("Quiz Questions")
    if hasattr(st.session_state, "quiz_level"):
        pdf_questions.set_font("helvetica", "", 12)
        pdf_questions.cell(
            0,
            10,
            f"Difficulty Level: {st.session_state.quiz_level}",
            new_x="LMARGIN",
            new_y="NEXT",
        )
    pdf_questions.create_questions_only(quiz_data["questions"])

    # Generate answers-only PDF
    pdf_answers = QuizPDFGenerator()
    pdf_answers.create_title("Quiz Answers")
    if hasattr(st.session_state, "quiz_level"):
        pdf_answers.set_font("helvetica", "", 12)
        pdf_answers.cell(
            0,
            10,
            f"Difficulty Level: {st.session_state.quiz_level}",
            new_x="LMARGIN",
            new_y="NEXT",
        )
    pdf_answers.create_answers_only(quiz_data["questions"])

    # Generate user responses PDF
    pdf_user_answers = QuizPDFGenerator()
    pdf_user_answers.create_title("Quiz with Your Responses")
    if hasattr(st.session_state, "quiz_level"):
        pdf_user_answers.set_font("helvetica", "", 12)
        pdf_user_answers.cell(
            0,
            10,
            f"Difficulty Level: {st.session_state.quiz_level}",
            new_x="LMARGIN",
            new_y="NEXT",
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
        pdf_user_answers.set_font("helvetica", "B", 16)
        pdf_user_answers.cell(
            0, 10, "Quiz Results", new_x="LMARGIN", new_y="NEXT", align="C"
        )
        pdf_user_answers.ln(5)
        pdf_user_answers.set_font("helvetica", "B", 10)
        pdf_user_answers.cell(
            0,
            10,
            f"Final Score: {correct_count}/{len(quiz_data['questions'])}",
            new_x="LMARGIN",
            new_y="NEXT",
        )

    return {
        "questions": pdf_questions.output(dest="S"),
        "answers": pdf_answers.output(dest="S"),
        "user_responses": pdf_user_answers.output(dest="S"),
    }


def generate_answer_key_text(quiz_data):
    """Generate a text file with comma-separated answer keys."""
    answer_keys = [
        question["Correct_option"].capitalize() for question in quiz_data["questions"]
    ]
    return ",".join(answer_keys)


def generate_quiz_zip(quiz_data):
    """Generate a ZIP file containing all three PDFs and the answer key text file."""
    pdfs = generate_all_quiz_pdfs(quiz_data)
    answer_key_text = generate_answer_key_text(quiz_data)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:  # Using zipfile36
        zip_file.writestr("quiz_questions.pdf", pdfs["questions"])
        zip_file.writestr("quiz_answers.pdf", pdfs["answers"])
        zip_file.writestr("quiz_with_responses.pdf", pdfs["user_responses"])
        zip_file.writestr("answer_key.txt", answer_key_text.encode("utf-8"))

    zip_buffer.seek(0)
    return zip_buffer
