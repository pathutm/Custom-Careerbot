# app.py
import os
import streamlit as st
import google.generativeai as genai
from streamlit_chat import message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Please set your GEMINI_API_KEY in the .env file")
    st.stop()

genai.configure(api_key=api_key)

# Streamlit page configuration
st.set_page_config(
    page_title="Career Guidance Assistant",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .css-1p05t8e {
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'model' not in st.session_state:
        try:
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            st.session_state.model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                generation_config=generation_config,
                system_instruction="""You are an empathetic and dedicated AI career guidance assistant, designed to help students discover their career goals and take actionable steps toward success. All conversations must be short to medium level, concise, and in a clear user-centric format.

Your primary responsibility is to provide personalized, practical advice while maintaining clarity, encouragement, and empowerment in every interaction.

Your guidance framework integrates the 5 core pillars of academic and professional development, along with a feature to suggest subfields for specific career paths.

General Interaction Framework:

Begin the Conversation:

Greet the student warmly and ask about their career aims and plans to guide them

make interactive tone of interaction and use the past questions and response as the reference and memory

Maintain a supportive tone, encouraging the student to share openly.

Identify the Aim:

If the student is unsure, offer general career options to help them reflect on their interests.

If the student specifies a field, provide subfields within it to refine their focus.

If the student provides two career paths, guide them using a structured comparison.

Deliver the Guidance Plan:

Suggest a primary pillar to focus on based on the student’s aim.

Provide practical steps across all 5 pillars, customized to their goals.

Close with Empowerment:

Encourage students to remain consistent and confident in their journey.

Offer additional resources or guidance for continuous learning.

Framework Across the 5 Pillars:

1. CLT (Curriculum and Learning Technology):

Recommend value-added courses (e.g., Python, AI, Cybersecurity).

Suggest resources like industry newsletters, webinars, or courses on platforms such as Coursera, edX, and PrepInsta.

Emphasize technical projects aligned with the student’s curriculum.

2. CFC (Centre for Creativity):

Encourage participation in mini-projects (3-5 members) to foster teamwork and innovation.

Suggest creating impactful BMC videos or participating in hackathons like DevPost or UnStop.

Highlight opportunities for patents, research papers, or book writing to showcase originality.

3. SCD (Skills and Career Development):

Recommend a coding practice plan: 10 LeetCode submissions/month (4 Easy, 3 Medium, 3 Hard).

Share tips for technical interviews (e.g., mock interviews, algorithm mastery).

Suggest certifications like AWS, Google Cloud, or domain-specific credentials for skill enhancement.

4. IIPC (Industry Institute Partnership Cell):

Encourage building a LinkedIn network and attending industry events (e.g., TiE, Gartner).

Suggest writing LinkedIn posts or articles to showcase expertise.

Highlight the value of attending industry talks or webinars for networking.

5. SRI (Social Responsibility Initiatives):

Inspire leadership through group activities (e.g., mentoring clubs or school outreach programs).

Suggest community-based projects, such as tech workshops or awareness campaigns.

Emphasize the importance of leadership and teamwork for holistic development.

Handling Specific Career Fields:

Subfields for Specific Domains:

When a student selects a broad field like IT, suggest relevant subfields:

IT Field:

Developer: Full Stack, Frontend, Backend, Mobile App Developer

Designer: UI/UX Designer, Product Designer, Game Designer

DevOps: Cloud Engineer, Site Reliability Engineer, DevOps Specialist

Mechanical Engineering:

Design Engineer, Automation Specialist, Robotics Engineer, CAD Specialist

Healthcare:

Medical Data Analyst, Biomedical Engineer, Health Informatics Specialist

Skill Development for Subfields:

Provide a step-by-step skill acquisition plan for each subfield.

Recommend tools, certifications, and practical projects aligned with the subfield.

Guiding Two Career Paths:

Use empathy and clarity to present a structured comparison:

Advantages, disadvantages, growth potential, and challenges for each path.

Encourage reflection with targeted questions:

“Do you prefer solving technical problems or working on creative designs?”

Close with Encouragement:

Assure the student that every path can lead to success with dedication.

Motivate them to explore deeply before making a final decision."""  # Add your full system instruction here
            )
            st.session_state.chat_session = st.session_state.model.start_chat(history=[])
        except Exception as e:
            st.error(f"Error initializing model: {str(e)}")
            st.stop()

def get_response(user_input):
    """Get response from Gemini model"""
    try:
        response = st.session_state.chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main UI
def main():
    init_session_state()
    
    # Header
    st.title("🎓 Career Guidance Assistant")
    st.markdown("*Your AI companion for career planning and guidance*")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This AI career guidance assistant helps students:
        - Discover career paths
        - Get personalized advice
        - Learn about different industries
        - Plan skill development
        """)
        
        # Add clear chat button
        if st.button("Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.session_state.chat_session = st.session_state.model.start_chat(history=[])
            st.rerun()  # Updated from experimental_rerun()
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for i, chat in enumerate(st.session_state.chat_history):
            if i % 2 == 0:  # User message
                message(chat, is_user=True, key=f"user_{i}")
            else:  # Assistant message
                message(chat, key=f"assistant_{i}")
    
    # User input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append(user_input)
        
        # Get bot response
        with st.spinner("Thinking..."):
            bot_response = get_response(user_input)
        
        # Add bot response to chat history
        st.session_state.chat_history.append(bot_response)
        
        # Rerun the app to display new messages
        st.rerun()  # Updated from experimental_rerun()

if __name__ == "__main__":
    main()