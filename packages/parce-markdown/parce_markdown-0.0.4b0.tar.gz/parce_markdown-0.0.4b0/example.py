import py_markdown as md

obj: md.MD = md.ReadMD.file_import("README.md")
result: str = obj.to_html_text()
print(result)