from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter

def highlight_code(filename, code):
    try:
        lexer = guess_lexer_for_filename(filename, code)
    except:
        lexer = TextLexer()
    formatter = HtmlFormatter()
    highlighted_code = highlight(code, lexer, formatter)
    language = lexer.name if lexer else "unknown"
    return highlighted_code, language
