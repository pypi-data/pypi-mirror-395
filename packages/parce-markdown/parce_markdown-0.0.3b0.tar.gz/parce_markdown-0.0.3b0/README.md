# py-markdown
Library for parcing markdown and convert to html text or file.

Библиотека для парсинга markdown-файла и его преобразование в html-текст или файл.
## Установка библиотеки
Установка библиотеки осуществляется без всяких зависимостей:
```bash
pip install parce-markdown
```
После успешной установки импортируем библиотеку в файл:
```python
import py_markdown as md
```
## Работа с исходным текстом
Теперь преобразуем текст c markdown-разметкой в html. Для этого создадим экземпляр класса `ReadMD`:
```python
TEXT = "# Header of MD\nMarkdown is a super-simple text presentation format."
obj: md.MD = md.ReadMD(TEXT)
```
Распознать markdown-файл можно с помощью классового метода `file_import`:
```python
PATH = "README.md"
obj: md.MD = md.ReadMD.file_import(PATH)
```
По умолчанию установлена кодировка `utf-8`.

## Представление html-разметки
Чтобы преобразовать markdown-разметку в html-разметку можно воспользоваться следующим методом:
```python
result: str = obj.to_html_text()
```
Чтобы преобразовать markdown-разметку в html-файл воспользуемся следующим методом:
```python
PATH_EXPORT = "/export/sample.html"
obj.to_html_file(PATH_EXPORT)
```
Представленные методы позволяют успростить и автоматизировать создание html-контента, освоив только азы разметки markdown, а также LaTex-запись формул.
