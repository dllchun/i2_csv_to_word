import streamlit as st
from services.app_logic import (
    upload_files,
    initialize_session_state,
    generate_documents,
    download_buttons,
    generate_with_progress,
)


def main():
    st.set_page_config(page_title="CSV to Word Processing App", layout="wide")

    st.title("CSV to Word Processing App")
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 0.5em 1em;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin-top: 1em;
            cursor: pointer;
            border-radius: 4px;
            transition: color 0.3s;
        }
        .stButton>button:hover {
            color: white;
        }
        .stFileUploader {
            margin-bottom: 1.5em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    initialize_session_state()

    uploaded_files = upload_files()

    if st.button("Generate Word File"):
        generate_with_progress(uploaded_files)

    # Using an expander for download buttons
    with st.expander("Download Documents"):
        download_buttons()


if __name__ == "__main__":
    main()
