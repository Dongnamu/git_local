from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter
from models.file_data import filesData, treeData

def get_tree_data():
    return treeData

def get_file_data(filename):
    return filesData.get(filename)

def highlight_code(filename, code):
    try:
        lexer = guess_lexer_for_filename(filename, code)
    except:
        lexer = TextLexer()
    formatter = HtmlFormatter()
    highlighted_code = highlight(code, lexer, formatter)
    language = lexer.name if lexer else "unknown"
    return highlighted_code, language
