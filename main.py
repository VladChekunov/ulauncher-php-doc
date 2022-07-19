from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

import logging
import requests

logger = logging.getLogger(__name__)
search_index = {}


class PhpDocsExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.getSearchIndex()

    def getSearchIndex(self):
        # TODO: Bind language to search index request
        # TODO: Bind delay
        global search_index

        response = requests.get(
            "https://www.php.net/js/search-index.php?lang=en")
        search_index = response.json()


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        results_count = 0
        query_string = event.get_argument()

        for page_index in search_index:
            if results_count == 5:
                break

            title = search_index[page_index][0]
            snippet = search_index[page_index][1]

            if query_string in title or query_string in snippet:
                results_count += 1
                # TODO: Bind language to url
                items.append(
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=title,
                        description=snippet,
                        on_enter=OpenUrlAction(
                            "https://www.php.net/manual/en/"+page_index
                        )
                    )
                )

        return RenderResultListAction(items)


if __name__ == '__main__':
    PhpDocsExtension().run()
