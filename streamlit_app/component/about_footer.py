import streamlit as st


def about_footer(author_name, author_email):
    st.caption("---")
    st.title("About")
    st.info(
        f"""Contact: {author_name} ({author_email}) if you have any questions or comments.""")
