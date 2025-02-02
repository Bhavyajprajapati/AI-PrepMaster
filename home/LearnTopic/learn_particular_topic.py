import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components


# Set your Google API key

def learn_particular_topic_interface():
    genai.configure(api_key="AIzaSyB7n_R6Bs5JxGyzzS1V4DftNR9-Wu2j-2o")
    st.subheader("Learn Particular Topic")
    
    if "generated_details" not in st.session_state:
        st.session_state.generated_details = None
    
    topic = st.text_input("Enter a topic you want to Learn:")
    # Configure generation settings
    generation_config = {
        "temperature": 0.3,  # Controls randomness (0 = deterministic, 1 = creative)
        "max_output_tokens": 800,  # Limits the length of the response
        "top_p": 0.9,  # Controls diversity via nucleus sampling
        "top_k": 50,  # Limits sampling to the top-k most likely tokens
        # "presence_penalty": 0.2,  # Encourages relevant but slightly new insights
        # "frequency_penalty": 0.1,  # Reduces repetition while keeping explanations clear
        "stop_sequences": [
            "References:",
            "End of response",
        ],  # Prevents unnecessary text
    }
    prompt = f"""
        Task: Act as an expert educator and curriculum designer. Generate a structured, detailed educational overview for the topic: {topic}.

Requirements:

Overview: Start with a concise definition and significance of the topic.

Key Concepts & Terminology: List 5-8 core ideas/fundamentals with brief explanations.

Learning Objectives: Provide 3-5 actionable goals learners should achieve after studying the topic.

Subtopics Breakdown:

Divide the topic into 4-6 subtopics (use headings like "I. Subtopic 1").

For each subtopic, include:

A 2-3 sentence explanation.

1-2 real-world examples or analogies.

A simple diagram/flowchart idea (describe verbally).

Applications: Explain 3-5 practical or real-world uses of the {topic}.

Resources: Recommend 2-3 books, articles, or videos for deeper learning (with brief descriptions).

Common Misconceptions: Address 2-3 frequent misunderstandings about the {topic}.

Advanced Connections: Link the topic to 1-2 related advanced fields/concepts for further exploration.

Tone & Format:

Academic yet accessible (avoid jargon unless necessary).

Use clear headings, bullet points, and numbered lists.

Include emojis sparingly to highlight key sections (e.g., 🎯 for objectives).

Example Response Structure:


# [Topic Name]  

## 🎯 Learning Objectives  
- Objective 1  
- Objective 2  

## 🔑 Key Concepts  
1. **Concept 1**: Explanation...  
2. **Concept 2**: Explanation...  

## 📚 Subtopics Breakdown  
### I. Subtopic 1  
- **Explanation**: ...  
- **Example**: ...  
- **Visual Aid Idea**: "A flowchart showing..."  
...  
Response Guidelines:

Prioritize accuracy and depth.

Cite sources if applicable.

Avoid opinionated content; focus on factual clarity.


"""
    if st.button("Learn"):
        if topic:
            with st.spinner("Generating details..."):
                try:
                    model = genai.GenerativeModel("gemini-pro")
                    response = model.generate_content(prompt,generation_config=generation_config)
                    # st.write(response)
                    st.session_state.generated_details = response.text
                except Exception as e:
                    st.error(f"Error: {e}")
            # Store response in session state

        else:
            st.warning("Please enter a topic to generate a response.")

    # If response exists, display it
    if st.session_state.generated_details:
        st.write(st.session_state.generated_details)

        show_print_button ="""
        <script>
            function print_page(obj) {
                parent.window.print();
            }
        </script>
        <style>
            #save_pdf_button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: 0.3s;
            }
            #save_pdf_button:hover {
                background-color: #45a049;
            }
        </style>
        
        <button id="save_pdf_button" onclick="print_page(this)">
            Save as pdf
        </button>
        """
        components.html(show_print_button)    
        