from abc import ABC, abstractmethod
from datetime import timedelta

import streamlit as st
from crawlers.ipma import IpmaCrawler
from crawlers.ivar import IvarCrawler


class Section(ABC):
    def __init__(self, title, payload=None):
        self.title = title
        self.payload = payload
        self.__call__()

    @abstractmethod
    def content(self):
        pass

    def st_title(self):
        st.header(self.title)

    def st_horizontal_line(self):
        st.markdown("""---""")

    def __call__(self):
        self.st_title()
        self.content()
        self.st_horizontal_line()


class PageHeader(Section):
    def __init__(self, title, description):
        self.description = description
        super().__init__(title)

    def st_title(self):
        primary_color = st.get_option('theme.primaryColor')
        st.markdown(f"""<h1 style='text-align: center; color: {primary_color}'>
                        {self.title}
                    </h1>""",
                    unsafe_allow_html=True)

    def content(self):
        st.markdown(self.description)


class SelectDataSection(Section):
    SECTION_NAME = "Select Data"

    def __init__(self):
        super().__init__(self.SECTION_NAME)

    def content(self):
        pass
