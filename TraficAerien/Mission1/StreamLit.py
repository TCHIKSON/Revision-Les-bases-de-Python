import streamlit as st

from Réponse import render_mission1_responses_tab


st.set_page_config(page_title="TP SL/SQL 2025 – Mission 1", layout="wide")
st.title("TP SL/SQL 2025 – Réponses Mission 1")
st.caption("Explorez les réponses du notebook Mission 1.")


def main() -> None:
    render_mission1_responses_tab()


if __name__ == "__main__":
    main()
