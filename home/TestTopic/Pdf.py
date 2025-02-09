from fpdf import FPDF
from datetime import datetime
import streamlit as st
import io


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

    def create_quiz_section(self, questions, selected_options=None, show_answers=False):
        self.set_font("Arial", "", 11)

        for i, question in enumerate(questions):
            self.set_font("Arial", "B", 10)
            self.multi_cell(0, 10, f"Q{i+1} :- {question['Mcq']}")

            self.set_font("Arial", "", 9)
            for option_key, option_value in question["Options"].items():
                prefix = "   "  # Default empty prefix

                if selected_options and i in selected_options:
                    if option_value == selected_options[i]:  # User-selected option
                        prefix = "->"  # Add tick mark

                self.multi_cell(0, 10, f"{prefix}{option_key}) {option_value}")

            self.ln(5)  # Space after each question


def generate_quiz_pdf(quiz_data, filename, include_answers=False):
    pdf = QuizPDFGenerator()
    pdf.create_title("Quiz Questions")

    if hasattr(st.session_state, "quiz_level"):
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Difficulty Level: {st.session_state.quiz_level}", 0, 1)

    pdf.create_quiz_section(
        quiz_data["questions"],
        quiz_data.get("selected_options", {}),
        show_answers=include_answers,
    )

    if include_answers:
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Quiz Results", 0, 1, "C")
        pdf.ln(10)

        correct_count = sum(
            1
            for i, question in enumerate(quiz_data["questions"])
            if quiz_data["selected_options"].get(i)
            == question["Options"].get(question["Correct_option"])
        )

        pdf.set_font("Arial", "B", 10)
        pdf.cell(
            0, 10, f"Final Score: {correct_count}/{len(quiz_data['questions'])}", 0, 1
        )

    # Return PDF as bytes
    return pdf.output(dest="S").encode("latin-1", errors="replace")
