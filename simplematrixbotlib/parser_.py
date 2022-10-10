from sly import Lexer, Parser
from dataclasses import dataclass

@dataclass
class Arg:
    name: str
    remainder: bool = False

@dataclass
class Chars:
    content: str

class RuleLexer(Lexer):
    tokens = {CHAR, SPACE, L_ANG, R_ANG, ASTER}

    L_ANG = r'<'
    R_ANG = r'>'
    ASTER = r'\*'
    SPACE = r' '
    CHAR = r'[\S]'
    
class RuleParser(Parser):
    tokens = RuleLexer.tokens

    @_('arg')
    def expr(self, p):
        return p.arg
    
    @_('chars')
    def expr(self, p):
        return p.chars
    
    @_('expr SPACE expr')
    def expr(self, p):
        return p[0], p[2]

    @_('L_ANG ASTER R_ANG')
    def arg(self, p):
        return Arg(name="", remainder=True)
    
    @_('L_ANG chars R_ANG')
    def arg(self, p):
        return Arg(name=p.chars.content)
    
    @_('L_ANG chars SPACE ASTER R_ANG')
    def arg(self, p):
        return Arg(name=p.chars, remainder=True)
    
    @_('chars CHAR')
    def chars(self, p):
        return Chars(p.chars.content+p.CHAR)

    @_('CHAR')
    def chars(self, p):
        return Chars(p.CHAR)
    
def parse(input_:str, rule:str) -> dict:
    lexer = RuleLexer()
    parser = RuleParser()

    formatted = []
    def un_nest(data):
        if isinstance(data, tuple):
            formatted.append(data[0])
            un_nest(data[1])
        else:
            formatted.append(data)
    un_nest(parser.parse(lexer.tokenize(rule)))

    return formatted