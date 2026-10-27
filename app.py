
import streamlit as st

from src.answer import answer_question


st.set_page_config(
    page_title="IncidentLens | Incident Response Assistant",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ IncidentLens")
st.subheader("Book-grounded Incident Response Assistant")

st.write(
    "Ask questions about incident response. "
    "IncidentLens retrieves relevant passages from the book "
    "and uses Gemini to generate an answer with page citations."
)

st.info(
    "Answers are grounded in *Dynamic Incident Response: "
    "A Framework for Security Teams*. Check the source passages "
    "to verify the evidence."
)

with st.form("question_form"):
    question = st.text_area(
        "Your question",
        placeholder=(
            "Example: How should a security team respond to an incident?"
        ),
        height=100,
    )

    top_k = st.slider(
        "Number of source passages to retrieve",
        min_value=1,
        max_value=5,
        value=3,
    )

    submitted = st.form_submit_button(
        "Ask IncidentLens",
        type="primary",
    )

if submitted:
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        try:
            with st.spinner(
                "Searching the book and generating your answer..."
            ):
                result = answer_question(
                    question=question.strip(),
                    top_k=top_k,
                )

            st.divider()
            st.header("Answer")
            st.markdown(result["answer"])

            sources = result.get("sources", [])

            if sources:
                st.subheader(f"Sources ({len(sources)})")

                for index, source in enumerate(sources, start=1):
                    page = source.get("page", "Unknown")

                    with st.expander(f"Source {index} — Book page {page}"):
                        st.write(source.get("text", ""))

            else:
                st.caption("No supporting source passages were returned.")

        except Exception as error:
            st.error(
                "IncidentLens couldn't complete the request. "
                "Check your terminal for details."
            )
            st.caption(f"Error: {error}")
