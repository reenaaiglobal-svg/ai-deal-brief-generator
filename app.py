import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="AI Deal Brief Generator",
    layout="wide"
)

st.title("AI Deal Brief Generator")

# ---------------------------------
# GEMINI API CONFIG
# ---------------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------------
# INPUT FORM
# ---------------------------------
with st.form("deal_form"):

    deal_name = st.text_input("Deal Name")

    client_name = st.text_input("Client")

    stage = st.selectbox(
        "Deal Stage",
        [
            "Discovery",
            "Qualified",
            "Proposal",
            "Negotiation",
            "Closed Won"
        ]
    )

    contacts = st.text_input("Client Contacts")

    amount = st.text_input("Deal Amount")

    date = st.date_input("Expected Close Date")

    tech_stack = st.text_area(
        "Tech Stack",
        placeholder="Azure, AWS, OpenAI, Salesforce, SAP..."
    )

    problem_statement = st.text_area(
        "Problem Statement / Notes",
        height=180
    )

    submitted = st.form_submit_button("Generate Deal Brief")

# ---------------------------------
# GENERATE OUTPUT
# ---------------------------------
if submitted:

    prompt = f"""
    You are a senior enterprise GenAI presales consultant.

    Generate a structured deal brief.

    Deal Name: {deal_name}
    Client: {client_name}
    Stage: {stage}
    Contacts: {contacts}
    Amount: {amount}
    Expected Close Date: {date}
    Tech Stack: {tech_stack}

    Problem Statement:
    {problem_statement}

    Generate:

    1. Executive Summary

    2. Recommended GenAI Use Cases

    3. Implementation Risks

    4. Competitive Positioning

    5. Resource Requirements

    6. Suggested Next Steps

    7. Key Qualification Questions

    Keep response professional, concise, and enterprise-focused.
    """

    with st.spinner("Generating deal brief..."):

        response = model.generate_content(prompt)

        output = response.text

    # ---------------------------------
    # DISPLAY OUTPUT
    # ---------------------------------
    st.subheader("Generated Deal Brief")

    st.markdown(output)

    # ---------------------------------
    # COPY SECTION
    # ---------------------------------
    st.code(output)

    # ---------------------------------
    # WORD DOC GENERATION
    # ---------------------------------
    doc = Document()

    doc.add_heading("AI Deal Brief", level=1)

    doc.add_paragraph(f"Deal Name: {deal_name}")
    doc.add_paragraph(f"Client: {client_name}")
    doc.add_paragraph(f"Stage: {stage}")
    doc.add_paragraph(f"Contacts: {contacts}")
    doc.add_paragraph(f"Amount: {amount}")
    doc.add_paragraph(f"Expected Close Date: {date}")

    doc.add_heading("Generated Brief", level=2)

    doc.add_paragraph(output)

    buffer = BytesIO()

    doc.save(buffer)

    buffer.seek(0)

    # ---------------------------------
    # DOWNLOAD BUTTON
    # ---------------------------------
    st.download_button(
        label="Download Word Document",
        data=buffer,
        file_name=f"{deal_name}_Deal_Brief.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
