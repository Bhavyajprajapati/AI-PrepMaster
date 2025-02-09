# Add these imports at the top of your file
from fpdf import FPDF
from datetime import datetime
import streamlit as st

# Add the PDF generator class and functions here (from previous code)
class QuizPDFGenerator(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0,10,f'Quiz Report - Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',0, 1,"R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def create_title(self, title):
        self.add_page()
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, title, 0, 1, "C")
        self.ln(10)

    def create_quiz_section(self, questions, selected_options=None, show_answers=False):
        self.set_font("Arial", "", 12)

        for i, question in enumerate(questions):
            self.set_font("Arial", "B", 12)
            self.multi_cell(0, 10, f"Q{i+1}: {question['Mcq']}")

            self.set_font("Arial", "", 12)
            for option_key, option_value in question["Options"].items():
                prefix = (
                    "→ "
                    if show_answers and option_key == question["Correct_option"]
                    else "  "
                )
                if selected_options and i in selected_options:
                    if option_value == selected_options[i]:
                        prefix = "* "
                self.multi_cell(0, 10, f"{prefix}{option_key}) {option_value}")

            self.ln(5)

# Add the generate_quiz_pdf function
def generate_quiz_pdf(quiz_data, filename="quiz.pdf", include_answers=False):
    pdf = QuizPDFGenerator()
    print(quiz_data)
    # Create title page
    pdf.create_title("Quiz Questions")

    # Add difficulty level if available
    if hasattr(st.session_state, "quiz_level"):
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Difficulty Level: {st.session_state.quiz_level}", 0, 1)

    # Add questions
    pdf.create_quiz_section(
        quiz_data["questions"],
        quiz_data.get("selected_options", {}),
        show_answers=include_answers,
    )

    # Add results page if answers are included
    if include_answers and "selected_options" in quiz_data:
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Quiz Results", 0, 1, "C")
        pdf.ln(10)

        # Calculate score
        correct_count = 0
        total_questions = len(quiz_data["questions"])

        for i, question in enumerate(quiz_data["questions"]):
            selected = quiz_data["selected_options"].get(i, "Not Answered")
            correct = question["Options"].get(question["Correct_option"], "Unknown")
            if selected == correct:
                correct_count += 1

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Final Score: {correct_count}/{total_questions}", 0, 1)

    pdf.output(filename)