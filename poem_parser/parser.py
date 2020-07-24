from parsel import Selector
from typing import Optional, List


class TextPoem:
    def __init__(
        self,
        title: str, text: str,
        year: Optional[str] = None
    ) -> None:
        self.title: str = title
        self.text: str = text
        self.year: Optional[str] = year

    def __str__(self) -> str:
        year: str = ''
        if self.year is not None:
            year = self.year
        return(
            f"{self.title}\n\n{self.text}\n\n\n"
            f"{year}\n\n------\n\n"
        )


def get_title(src_title: Selector,
              text: str) -> str:
    title: str = src_title.get()
    if title == '* * *':
        title = text.split('\n')[0]
    return title


def parse_html_file(filepath: str) -> List[TextPoem]:
    """
    HTML File parser for https://rupoem.ru/ website,
    «all.aspx» pages, like:
    «https://rupoem.ru/axmadulina/all.aspx»
    Won't work with other websites or pages.

    Input:
        path to .html file from rupoem.ru
    Output:
        List of TextPoem objects
    """
    result: List[TextPoem] = []
    with open(filepath, mode='r', encoding='utf-8') as html:
        # parse html
        sel: Selector = Selector(html.read())
        titles_src: Selector = sel.css('h2::text')
        poems_src: Selector = sel.css('div.poem')
        quanity: int = min(len(titles_src), len(poems_src))

        # iterate through poems
        for idx in range(quanity):
            # get poem text
            src_poem: Selector = poems_src[idx]
            cats_src: Selector = src_poem.css(
                'a.btn.btn-outline-secondary::text'
            )
            text: str = src_poem.css(
                    'div.poem-text.font-size-larger::text'
                ).get().strip()

            # create TextPoem, if text is not empty
            if text != '':
                title: str = get_title(titles_src[idx], text)

                poem: TextPoem = TextPoem(title, text)
                if len(cats_src) >= 1:
                    poem.year = cats_src[0].get()
                result.append(poem)

    return result
