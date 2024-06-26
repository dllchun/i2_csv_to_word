import streamlit as st
from services.data_processing import process_csv, combine_dfs, clean_data_folder
from services.doc_processing import generate_word_doc


def main():
    st.title("CSV to Word Processing App")

    uploaded_files = st.file_uploader(
        "Choose CSV files",
        type="csv",
        accept_multiple_files=True,
    )

    # Initiate the session_state
    if "generated_files" not in st.session_state:
        st.session_state["generated_files"] = {}

    if st.button("Generate Word File"):
        if uploaded_files and len(uploaded_files) >= 1:
            en_df, tc_df, sc_df = None, None, None

            for file in uploaded_files:
                if "EN" in file.name.upper():
                    en_df = process_csv(file, "EN")

                elif "TC" in file.name.upper():
                    tc_df = process_csv(file, "TC")

                elif "SC" in file.name.upper():
                    sc_df = process_csv(file, "SC")

            # Only EN and TC version
            if en_df is None and tc_df is None:
                st.error("Please upload at least both EN and TC files.")
                return

            en_tc_version = combine_dfs(en_df, tc_df)

            if not en_tc_version.empty:
                en_tc_version_filtered = en_tc_version[
                    [
                        "Ref#",
                        "Smart Area",
                        "Initiative Group",
                        "Initiative",
                        "Progress Update",
                        "Status",
                    ]
                ]

                doc_name = generate_word_doc(
                    en_tc_version_filtered, "EN_TC_Word_Document"
                )

                st.session_state.generated_files["en_tc"] = doc_name
                st.success("EN, TC document generated successfully.")

            # All version
            if sc_df is not None:
                en_tc_sc_combined = combine_dfs(en_tc_version, sc_df)

                if not en_tc_sc_combined.empty:
                    en_tc_sc_version_filtered = en_tc_sc_combined[
                        [
                            "Ref#",
                            "Smart Area",
                            "Initiative Group",
                            "Initiative",
                            "Progress Update",
                            "Status",
                        ]
                    ]
                    doc_name = generate_word_doc(
                        en_tc_sc_version_filtered, "All_Word_Document"
                    )
                    st.session_state.generated_files["all"] = doc_name
                    st.success(
                        "All (EN, TC, and SC) Word document generated successfully."
                    )

                else:
                    st.error("Combined DataFrame is empty.")

        else:
            st.warning("Please upload at least one file.")

    if "en_tc" in st.session_state.generated_files:
        with open(st.session_state.generated_files["en_tc"], "rb") as file:
            st.download_button(
                label="Download EN & TC Word Document",
                data=file,
                file_name="EN_TC_Word_Document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

    if "all" in st.session_state.generated_files:
        with open(st.session_state.generated_files["all"], "rb") as file:
            st.download_button(
                label="Download Full version document",
                data=file,
                file_name="All_Word_Document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )


if __name__ == "__main__":
    main()
