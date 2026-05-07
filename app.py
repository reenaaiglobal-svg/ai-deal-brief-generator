import streamlit as st
from openai import OpenAI
from docx import Document
from io import BytesIO

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Deal Brief Generator",
    layout="wide"
)

st.title("AI Deal Brief Generator")

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# -----------------------------
# INPUT FORM
# -----------------------------
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
        placeholder="Azure, AWS, SAP, Salesforce, Databricks..."
    )

    problem_statement = st.text_area(
        "Problem Statement / Notes",
        height=220
    )

    submitted = st.form_submit_button("Generate Deal Brief")

# -----------------------------
# GENERATE OUTPUT
# -----------------------------
if submitted:

    prompt = f"""
    You are a senior enterprise GenAI presales consultant.

    Generate a professional enterprise deal brief in structured bullet-point format.

    Client: {client_name}

    Deal Name: {deal_name}

    Stage: {stage}

    Contacts: {contacts}

    Amount: {amount}

    Expected Close Date: {date}

    Tech Stack:
    {tech_stack}

    Problem Statement:
    {problem_statement}

    Our Service Categories:
    - GenAI Strategy
    - AI/ML Engineering
    - Intelligent Automation
    - Legacy Modernization
    - Data & Analytics
    - Cloud Transformation
    - Platform Engineering

    Consider:
    - enterprise consulting positioning
    - reusable accelerators
    - scalability
    - governance
    - delivery feasibility
    - account farming opportunities
    - competitive differentiation

    Include the following sections:

    1. Executive Summary
    - concise bullets
    - business impact
    - transformation value

    2. Recommended GenAI Use Cases
    - prioritized recommendations
    - quick wins
    - strategic opportunities

    3. Competitive Positioning
    - likely competitors
    - differentiation strategy
    - why client should choose us

    4. Implementation Risks
    - technical risks
    - governance risks
    - adoption risks
    - data/security concerns

    5. Resource Requirements
    - suggested roles
    - skills needed
    - delivery structure

    6. Suggested Next Steps
    - workshops
    - assessments
    - POCs
    - roadmap steps

    7. Key Qualification Questions
    - stakeholder alignment
    - budget/timeline
    - platform readiness
    - data readiness
    - success metrics
   Refer our service offerings from here while suggsting solutions. https://www.accionlabs.com/

    Format professionally using headings and bullet points.
    """

    with st.spinner("Generating deal brief..."):

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior enterprise GenAI presales consultant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

        output = response.choices[0].message.content

    # -----------------------------
    # DISPLAY OUTPUT
    # -----------------------------
    st.subheader("Generated Deal Brief")

    st.markdown(output)

    st.code(output)

    # -----------------------------
    # WORD DOCUMENT
    # -----------------------------
    doc = Document()

    doc.add_heading("AI Deal Brief", level=1)

    doc.add_paragraph(f"Client: {client_name}")
    doc.add_paragraph(f"Deal Name: {deal_name}")
    doc.add_paragraph(f"Stage: {stage}")
    doc.add_paragraph(f"Amount: {amount}")

    doc.add_heading("Generated Brief", level=2)

    doc.add_paragraph(output)

    buffer = BytesIO()

    doc.save(buffer)

    buffer.seek(0)

    # -----------------------------
    # DOWNLOAD BUTTON
    # -----------------------------
    st.download_button(
        label="Download Word Document",
        data=buffer,
        file_name=f"{deal_name}_Deal_Brief.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
