import streamlit as st

from app.api import load_data


def draw_table():
    # Display the text field to collect required directory ID
    dir_id_text_input = st.text_input(
        label="Directory ID",
        placeholder="Example, 12_abcdef...",
    )

    dir_id_value = dir_id_text_input

    if dir_id_value:
        try:
            # Show spinner while loading the data
            with st.spinner("Loading data... Please wait."):
                data = load_data(dir_id_value)

            st.dataframe(
                data=data,
                use_container_width=True,
            )

        # Display error text on loader failure with error trace
        except Exception as error:
            st.error(error)
