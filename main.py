from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent
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
        self.subscribe(PreferencesEvent, PreferencesEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        results_count = 0
        query_string = event.get_argument()

        for page_index in search_index:
            if results_count >= 200:
                break

            title = search_index[page_index][0]
            snippet = search_index[page_index][1]

            if query_string.lower() in title.lower() or query_string.lower() in snippet.lower():
                results_count += 1
                items.append(
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name=title,
                        description=snippet,
                        on_enter=OpenUrlAction(
                            "https://www.php.net/manual/" + extension.preferences['php_lang'] + "/" + page_index
                        )
                    )
                )

        return RenderResultListAction(items)


class PreferencesEventListener(EventListener):

    def on_event(self, event, extension):
        global search_index

        response = requests.get(
            "https://www.php.net/js/search-index.php?lang=" + event.preferences['php_lang']
        )
        search_index = response.json()

if __name__ == '__main__':
    PhpDocsExtension().run()
