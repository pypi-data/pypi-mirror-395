import re
from abc import ABC, abstractmethod

class MD(ABC):
    @abstractmethod
    def to_html_text(self) -> str:
        """Экспорт markdown в текст html-формата
        """
        pass

    @abstractmethod
    def to_html_file(self, path: str, encoding='utf-8') -> None:
        """Экспорт markdown в html файл
        """
        pass


class ReadMD(MD):
    def __init__(self, text: str) -> None:
        self._text = text

    @classmethod
    def file_import(cls, path_file: str, encoding='utf-8') -> MD:
        with open(path_file, 'r', encoding=encoding) as file:
            return cls(file.read())

    @staticmethod
    def _parse_elems(text: str) -> str:
        """Преобразуем маркированные и нумерованные списки и создаём параграфы
        """
        # Замена изображения на img элемент
        html = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', text)
        # Преобразуем блоки цитат
        html = re.sub(r'^>(.+)$', r'<blockquote><p>\1</p></blockquote>', html, flags=re.MULTILINE)
        # Преобразование маркированных списков
        html = re.sub(r'^\* (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.+</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)

        # Преобразование параграфов
        html = re.sub(r'^(?!<h|<ul|<ol|<li|<pre|<blockquote|<table|<tr|<td)(.*?)$', r'<p>\1</p>',
                       html, flags=re.MULTILINE)

        # Преобразование нумерованных списков
        html = re.sub(r'<p>\d+\.\s*(.*)</p>', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'</p>\n<li>', r'</p>\n<ol>\n<li>', html, flags=re.MULTILINE)
        return re.sub(r'</li>\n<p>', r'</li></ol>\n<p>', html, flags=re.MULTILINE)

    @staticmethod
    def _parse_style(text: str) -> str:
        '''Преобразуем стилистику текста
        '''
        # Преобразуем ссылки
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
        # Выделить жирным курсивом (три звезды)
        html = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<strong><em>\1</em></strong>', html)
        # Выделить жирным (две звезды)
        html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
        # Выделить курсивом (одна звезда)
        return re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)

    @staticmethod
    def _parse_code(text: str) -> str:
        ''' Преобразуем блоки кода
        '''
        html = re.sub(r'```math\n(.*?)\n```', r'<span class="math-tex">\(\1\)</span>', text, flags=re.DOTALL)
        html = re.sub(r'```(.*?)\n(.*?)\n```', r'<pre><code class="language-\1">\2</code></pre>',
                      html, flags=re.DOTALL)
        return re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    def _parser(self) -> str:
        """Парсинг заголовков и преобразование всех элементов Markdown в HTML
        """
        self._text = re.sub(r'^(#{1,6})\s*(.*?)\s*#*$',
                      lambda m: f"<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>",
                      self._text, flags=re.MULTILINE)
        self._text = re.sub(r'  ', r'\n', self._text, flags=re.MULTILINE)
        self._text = self._parse_code(self._text)
        self._text = self._parse_elems(self._text)
        self._text = self._parse_style(self._text)

    def to_html_text(self) -> str:
        """Экспорт markdown в текст html-формата
        """
        self._parser()
        return self._text

    def to_html_file(self, path: str, encoding='utf-8') -> None:
        """Экспорт markdown в html файл
        """
        if not path.endswith('.html'):
            raise ValueError("Неправильное расширение для файла")
        self._parser()
        with open(path, 'w', encoding=encoding) as file:
            file.write(self._text)
