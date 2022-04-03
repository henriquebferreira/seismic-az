from streamlit_app.page.news import news_content
from streamlit_app.page.visualization import visualization_content


class AppPages:
    # Insert new pages by adding new entries to the dictionary below
    PAGES = {
        "Data": {
            "icon": "server",
            "page": visualization_content},
        "News": {
            "icon": "info-circle-fill",
            "page": news_content},
    }

    @staticmethod
    def get_titles():
        return list(AppPages.PAGES.keys())

    @staticmethod
    def get_icons():
        return [AppPages.PAGES[t]["icon"] for t in AppPages.get_titles()]

    @staticmethod
    def get_content(title):
        return AppPages.PAGES.get(title)["page"]
