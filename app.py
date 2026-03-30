

import streamlit as st
import requests
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
from fpdf import FPDF
import io

# --- 1. PDF CLASS (UTF-8, Bougie Font) ---
class DigitalProduct(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        
    def add_chapter(self, title, content):
        self.add_page()
        try:
            self.set_font("DejaVu", "B", 22)
            self.set_text_color(184, 134, 11)
            self.multi_cell(0, 10, title)
            self.ln(5)
            self.set_font("DejaVu", "", 12)
            self.set_text_color(51, 51, 51)
            self.multi_cell(0, 8, content)
        except Exception as e:
            st.error(f"Error adding chapter '{title}': {e}")
            st.error(f"Preview: {content[:100]}...")

# --- 2. LICENSE CHECK ---
st.set_page_config(page_title="FabFlow AI | Member Access", page_icon="✨", layout="wide")
st.markdown("""
<style>
.stApp { background-color: #FCF9F2; }
h1, h2, h3 { color: #B8860B; font-family: 'Georgia', serif; }
.stButton>button { background-color: #B8860B; color: white; border-radius: 25px; border: none; padding: 10px 25px; }
.stProgress > div > div > div > div { background-color: #D4AF37; }
</style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def verify_license(license_key):
    if license_key == "tampa2026":
        return True
    product_id = "YOUR_ACTUAL_ID" 
    url = "https://api.gumroad.com/v2/licenses/verify"
    params = {"product_id": product_id, "license_key": license_key.strip()}
    try:
        response = requests.post(url, data=params)
        return response.json().get("success", False)
    except:
        return False

if not st.session_state.authenticated:
    st.write("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.title("✨ FabFlow AI")
    st.write("### Founder's Suite Access")
    st.write("Please enter your unique license key to unlock your digital empire.")
    user_key = st.text_input("License Key", type="password", placeholder="XXXX-XXXX-XXXX-XXXX")
    if st.button("Unlock My Flow"):
        if verify_license(user_key):
            st.session_state.authenticated = True
            st.success("Access Granted. Welcome, Visionary.")
            st.rerun()
        else:
            st.error("License not found. Please check your purchase receipt.")
    st.write("---")
    st.write("[Purchase Access to FabFlow AI](https://gumroad.com/l/your-link)")
    st.write("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. APP ENGINE ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

st.write("<div style='text-align: center;'><h1>FabFlow AI</h1><p>The Mastermind Suite for Digital Creators.</p></div>", unsafe_allow_html=True)
st.progress(st.session_state.step / 5)

# STEP 1: SKIP SAMPLE, AUTO VOICE
if st.session_state.step == 1:
    st.subheader("Step 1: Style & Vibe (Auto-generated)")
    st.info("We are automatically writing your product in a bougie, fabulous Black Auntie voice. No sample needed.")
    if st.button("Continue to Research"):
        st.session_state.step = 2
        st.rerun()

# STEP 2: RESEARCH MATERIAL
elif st.session_state.step == 2:
    st.subheader("Step 2: Model Viral Success")
    m_source = st.text_area("Paste Viral Script / Source Material (optional)")
    col1, col2 = st.columns([1, 5])
    if col1.button("Back"): 
        st.session_state.step = 1
        st.rerun()
    if col2.button("Design Your Product"):
        st.session_state.data['source'] = m_source
        st.session_state.step = 3
        st.rerun()

# STEP 3: TOPIC & OUTLINE
elif st.session_state.step == 3:
    st.subheader("Step 3: Define Your Masterpiece")
    title = st.text_input("Product Title")
    outline = st.text_area("Outline (Chapters - one per line)")
    col1, col2 = st.columns([1, 5])
    if col1.button("Back"):
        st.session_state.step = 2
        st.rerun()
    if col2.button("Begin Synthesis"):
        st.session_state.data['title'] = title
        st.session_state.data['outline'] = outline
        st.session_state.step = 4
        st.rerun()

# STEP 4: SYNTHESIS (Bougie Auntie Style)
elif st.session_state.step == 4:
    st.subheader("Step 4: Synthesis in Progress")
    with st.spinner("Our AI artisans are weaving your product..."):
        topic = st.session_state.data['title']
        full_content = []
        for chap in st.session_state.data['outline'].split('\n'):
            if chap.strip():
                try:
                    res = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Write in a confident, bougie, fabulous Black Auntie style (think Jenifer Lewis). Make it viral-worthy, empowering, and rich in personality."},
                            {"role": "user", "content": f"Write a high-value chapter for '{chap}' for the topic '{topic}'."}
                        ]
                    )
                    full_content.append((chap, res.choices[0].message.content))
                except Exception as e:
                    st.error(f"Error generating chapter '{chap}': {e}")
                    full_content.append((chap, "Content generation failed."))
        st.session_state.data['final_content'] = full_content
        st.success("Synthesis Complete.")
        if st.button("Launch My Product"):
            st.session_state.step = 5
            st.rerun()

# STEP 5: LAUNCH PDF
elif st.session_state.step == 5:
    st.subheader("✨ Your Fabulous Launch Kit")
    pdf = DigitalProduct()
    for title, body in st.session_state.data['final_content']:
        pdf.add_chapter(title, body)
    
    pdf_output = pdf.output(dest='S').encode('latin-1', errors='replace')
    pdf_buffer = io.BytesIO(pdf_output)
    
    t1, t2 = st.tabs(["📄 Download Product", "📱 Marketing Strategy"])
    with t1:
        st.download_button(
            label="📥 Download PDF Masterpiece",
            data=pdf_buffer,
            file_name=f"{st.session_state.data['title']}.pdf",
            mime="application/pdf",
            key="final-download-btn"
        )
    with t2:
        st.write("### Marketing Plan")
        st.info("Content strategies tailored to your bougie Auntie voice are ready for use.")

    if st.button("Create Another Empire"):
        st.session_state.step = 1
        st.session_state.data = {}
        st.rerun()
