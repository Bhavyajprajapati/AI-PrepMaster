import streamlit as st

def display_quiz_result(marks, questions):
    # Calculate statistics
    total_questions = len(questions)
    correct_answers = marks
    incorrect_answers = total_questions - correct_answers

    # Create pie chart
    fig_pie = {
        "data": [
            {
                "values": [correct_answers, incorrect_answers],
                "labels": ["Correct", "Incorrect"],
                "type": "pie",
                "marker": {"colors": ["#4CAF50", "#F44336"]},
                "textinfo": "label+percent",
                "hoverinfo": "label+value",
            }
        ],
        "layout": {
            "title": "Quiz Performance Summary",
            "showlegend": True,
            "width": 400,
            "height": 400,
        },
    }

    st.plotly_chart(fig_pie, use_container_width=True)

    # Create bar chart
    fig_bar = {
        "data": [
            {
                "x": ["Total Questions", "Correct Answers", "Incorrect Answers"],
                "y": [total_questions, correct_answers, incorrect_answers],
                "type": "bar",
                "marker": {"color": ["#2196F3", "#4CAF50", "#F44336"]},
            }
        ],
        "layout": {
            "title": "Quiz Statistics",
            "yaxis": {"title": "Number of Questions"},
            "showlegend": False,
            "width": 400,
            "height": 400,
        },
    }

    st.plotly_chart(fig_bar, use_container_width=True)

    # Calculate and show percentage
    percentage = (marks / total_questions) * 100
    st.progress(percentage / 100)
    st.write(f"Score Percentage: {percentage:.2f}%")

    # Show performance message
    if percentage >= 80:
        st.success("🌟 Excellent Performance!")
    elif percentage >= 60:
        st.info("👍 Good Performance!")
    else:
        st.warning("📚 Keep practicing!")
