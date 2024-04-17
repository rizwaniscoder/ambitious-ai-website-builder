import streamlit as st
from openai import OpenAI
import base64

def initialize_app():
    """
    Initializes the Streamlit app with configuration and checks OpenAI API key.
    Improved setup for app aesthetics and early error detection.
    """
    try:
        st.set_page_config(page_title="Ambitious Labs AI-Powered Website Builder", layout="wide")
        st.title('🚀 Ambitious Labs AI-Powered Website Builder')
        st.text("")
        global client
        client = OpenAI()
        # client.api_key = os.environ.get('OPENAI_API_KEY')

    except Exception as e:
        st.error(f"App initialization failed: {e}")
        st.stop()

def generate_website_code(name: str, contact_info: str, products_services: str, feedback: str = "") -> str:
    """
    Generates website code using GPT with enhanced prompt, updated to use newer models if available,
    and improved error handling for a better user experience.
    """
    # Construct the prompt
    prompt = (f"Generate HTML and CSS for a modern, responsive landing page named '{name}'. "
              f"Include contact information: {contact_info}. "
              f"Highlight these products/services: {products_services}. "
              f"Consider this feedback: {feedback}. "
              f"\n\nImagination Prompt:\n"
              f"Create a visually stunning landing page with a catchy tagline, Do not create multiple pages, Create a single page with multiple sections in the landing page. First fold should be the hero section, second fold should be the About Us section, third fold should be the Services/Products section, and fourth fold should be the Customer Reviews section. "
              f"Use Dummy Text Generator to add as much text as possible. Use your imagination to make it modern and appealing. "
              f"Add dummy text to fill in various sections with meaningful content. Add as much text as possible to each section. Please your response must only contain the code. No text before or after the code.")
    
    try:
        # Call GPT-4
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Using GPT-4 model
            messages=[
                {"role": "system", "content": "Generate website code."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract generated website code from completion
        website_code = completion.choices[0].message.content if completion.choices else ""
        return website_code.strip()
    except Exception as e:
        st.error(f"Failed to generate website code: {e}")
    return None

def user_input_forms():
    """
    Creates user input forms for website details with an improved layout for a smoother user experience.
    """
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            business_name = st.text_input("Business Name:", placeholder="ACME Corporation")
            contact_info = st.text_area("Contact Information:", placeholder="Email: contact@acme.com\nPhone: +1-202-555-0168", height=150)
        with col2:
            products_services = st.text_area("Products/Services Offered:", placeholder="1. Product A\n2. Service B", height=150)
            user_feedback = st.text_area("Additional Feedback (optional):", placeholder="Include any specific design or content requests.", height=150)
    return business_name, contact_info, products_services, user_feedback

def display_output(website_code: str):
    """
    Improved management of output display including website HTML code and downloadable link generation.
    """
    if website_code:
        with st.expander("Your Generated HTML Code"):
            st.code(website_code, language='html')

        # Corrected the approach for creating a downloadable file link with HTML5 download attribute.
        b64 = base64.b64encode(website_code.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="generated_website.html">Download HTML File</a>'
        st.markdown(href, unsafe_allow_html=True)

        st.subheader("Preview of Your Generated Website:")
        st.components.v1.html(website_code, height=600, scrolling=True)
    else:
        st.error("Failed to generate website code. Please adjust your inputs or try again later.")

# Main function to encapsulate the logic
def main():
    # Initialize the app
    initialize_app()

    # Input form for user to enter details
    business_name, contact_info, products_services, user_feedback = user_input_forms()

    # Button to generate website code
    if st.button('Generate Landing Page'):
        with st.spinner('Generating your website code...'):
            website_code = generate_website_code(business_name, contact_info, products_services, user_feedback)

        # Display output
        display_output(website_code)

if __name__ == "__main__":
    main()
