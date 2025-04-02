import streamlit as st
import google.generativeai as genai
from datetime import date

# Configure the app
st.set_page_config(page_title="Special Education Lesson Plan Generator", page_icon="📚")

# App title and description
st.title("📚 Special Education Lesson Plan Generator")
st.markdown("""
Create customized lesson plans for special education students using Gemini AI.
Adjust the parameters to meet your students' unique needs.
""")

# Sidebar for API key and settings
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Gemini API key:", type="password")
    st.markdown("[Get a Gemini API key](https://ai.google.dev/)")
    
    st.subheader("AI Settings")
    temperature = st.slider("Creativity level (temperature):", 0.0, 1.0, 0.7)
    st.caption("Higher values = more creative, Lower values = more focused")

# Initialize Gemini
def setup_gemini(api_key):
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    return None

# Main form for lesson plan parameters
with st.form("lesson_parameters"):
    st.subheader("Lesson Details")
    
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox(
            "Subject:",
            ["Reading", "Math", "Science", "Social Studies", "Life Skills", 
             "Communication", "Social Skills", "Occupational Therapy", "Physical Education"]
        )
        grade_level = st.selectbox(
            "Grade Level:",
            ["Pre-K", "K-2", "3-5", "6-8", "9-12", "Transition"]
        )
    with col2:
        duration = st.selectbox(
            "Lesson Duration:",
            ["30 minutes", "45 minutes", "60 minutes", "90 minutes", "120 minutes"]
        )
        date_range = st.date_input(
            "Lesson Date:",
            date.today()
        )
    
    st.subheader("Student Needs")
    disabilities = st.multiselect(
        "Student Disabilities (select all that apply):",
        ["Autism Spectrum Disorder", "Intellectual Disability", 
         "Learning Disability", "ADHD", "Emotional/Behavioral Disorder",
         "Speech/Language Impairment", "Physical Disability", 
         "Hearing Impairment", "Visual Impairment", "Multiple Disabilities"]
    )
    
    accommodations = st.multiselect(
        "Common Accommodations Needed:",
        ["Extended time", "Small group instruction", "One-on-one support",
         "Visual supports", "Modified assignments", "Assistive technology",
         "Sensory breaks", "Preferential seating", "Simplified language",
         "Hands-on activities", "Behavior support plan"]
    )
    
    st.subheader("Learning Objectives")
    objectives = st.text_area(
        "Specific Learning Objectives (leave blank for AI to suggest):",
        placeholder="Students will be able to..."
    )
    
    materials = st.text_area(
        "Available Materials/Resources:",
        placeholder="List any materials you have available (books, technology, manipulatives, etc.)"
    )
    
    submitted = st.form_submit_button("Generate Lesson Plan")

# Generate and display lesson plan
if submitted:
    if not api_key:
        st.error("Please enter your Gemini API key to continue.")
    else:
        model = setup_gemini(api_key)
        
        with st.spinner("Generating your customized lesson plan..."):
            # Create the prompt
            prompt = f"""
            Create a detailed special education lesson plan with the following parameters:
            
            Subject: {subject}
            Grade Level: {grade_level}
            Duration: {duration}
            Student Disabilities: {', '.join(disabilities) if disabilities else 'Not specified'}
            Accommodations Needed: {', '.join(accommodations) if accommodations else 'None specified'}
            Learning Objectives: {objectives if objectives else 'Please suggest appropriate objectives'}
            Available Materials: {materials if materials else 'Standard classroom materials'}
            
            The lesson plan should include:
            1. Clear, measurable objectives aligned with special education standards
            2. A detailed breakdown of instructional activities with time allocations
            3. Specific accommodations/modifications for the listed disabilities
            4. Assessment methods appropriate for diverse learners
            5. Differentiation strategies for varying ability levels
            6. Suggested visual supports or assistive technology if applicable
            7. Behavioral support strategies if needed
            
            Format the lesson plan with clear headings and bullet points for readability.
            """
            
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": 2000,
                    }
                )
                
                st.success("Lesson Plan Generated Successfully!")
                st.markdown("---")
                st.subheader(f"{subject} Lesson Plan for {grade_level}")
                st.markdown(response.text)
                
                # Add download button
                st.download_button(
                    label="Download Lesson Plan",
                    data=response.text,
                    file_name=f"Special_Ed_Lesson_Plan_{subject}_{date_range}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Add some usage tips
st.markdown("---")
st.subheader("Tips for Best Results")
st.markdown("""
- Be specific about your students' needs and available resources
- For complex needs, consider generating the plan and then refining with more details
- You can edit the generated plan directly in the app before downloading
- Save your API key to avoid re-entering it (but don't share it publicly)
""")
