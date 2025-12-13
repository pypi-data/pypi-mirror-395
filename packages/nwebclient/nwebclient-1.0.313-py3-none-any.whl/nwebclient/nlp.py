import re

from nltk.tokenize.api import TokenizerI


class SExprTokenizer(TokenizerI):
    """
    A tokenizer that divides strings into s-expressions.
    An s-expresion can be either:

      - a parenthesized expression, including any nested parenthesized
        expressions, or
      - a sequence of non-whitespace non-parenthesis characters.

    For example, the string ``(a (b c)) d e (f)`` consists of four
    s-expressions: ``(a (b c))``, ``d``, ``e``, and ``(f)``.

    By default, the characters ``(`` and ``)`` are treated as open and
    close parentheses, but alternative strings may be specified.

    :param parens: A two-element sequence specifying the open and close parentheses
        that should be used to find sexprs.  This will typically be either a
        two-character string, or a list of two strings.
    :type parens: str or list
    :param strict: If true, then raise an exception when tokenizing an ill-formed sexpr.
    """

    def __init__(self, parens="()", strict=True):
        if len(parens) != 2:
            raise ValueError("parens must contain exactly two strings")
        self._strict = strict
        self._open_paren = parens[0]
        self._close_paren = parens[1]
        self._paren_regexp = re.compile(
            f"{re.escape(parens[0])}|{re.escape(parens[1])}"
        )


    def tokenize(self, text):
        """
        Return a list of s-expressions extracted from *text*.
        For example:

            >>> SExprTokenizer().tokenize('(a b (c d)) e f (g)')
            ['(a b (c d))', 'e', 'f', '(g)']

        All parentheses are assumed to mark s-expressions.
        (No special processing is done to exclude parentheses that occur
        inside strings, or following backslash characters.)

        If the given expression contains non-matching parentheses,
        then the behavior of the tokenizer depends on the ``strict``
        parameter to the constructor.  If ``strict`` is ``True``, then
        raise a ``ValueError``.  If ``strict`` is ``False``, then any
        unmatched close parentheses will be listed as their own
        s-expression; and the last partial s-expression with unmatched open
        parentheses will be listed as its own s-expression:

            >>> SExprTokenizer(strict=False).tokenize('c) d) e (f (g')
            ['c', ')', 'd', ')', 'e', '(f (g']

        :param text: the string to be tokenized
        :type text: str or iter(str)
        :rtype: iter(str)
        """
        result = []
        pos = 0
        depth = 0
        for m in self._paren_regexp.finditer(text):
            paren = m.group()
            if depth == 0:
                result += text[pos : m.start()].split()
                pos = m.start()
            if paren == self._open_paren:
                depth += 1
            if paren == self._close_paren:
                if self._strict and depth == 0:
                    raise ValueError("Un-matched close paren at char %d" % m.start())
                depth = max(0, depth - 1)
                if depth == 0:
                    result.append(text[pos : m.end()])
                    pos = m.end()
        if self._strict and depth > 0:
            raise ValueError("Un-matched open paren at char %d" % pos)
        if pos < len(text):
            result.append(text[pos:])
        return result


def split_prompt(prompt):
    prompt = prompt.replace(',', ', ')
    tokens = list(SExprTokenizer().tokenize(prompt))
    tokens = map(lambda s: s.replace(',',' ').strip(), tokens)
    return tokens


class ParagraphParser:

    def __init__(self, text=''):
        self.parse(text)

    def contains_empty_lines(self):
        for line in self.lines:
            if line == '':
                return True
        return False

    def parse(self, text):
        lines = text.split("\n")
        self.lines = list(map(lambda x: x.strip(), lines))

    def split_empty_lines(self):
        lines = self.lines.copy()
        lines.append('')
        res = []
        p = []
        current = ''
        while len(lines) > 0:
            current = lines.pop(0)
            if current == '':
                res.append("\n".join(p))
                current = ''
                p = []
            else:
                p.append(current)
        return res

    def paragraphs(self):
        if self.contains_empty_lines():
            return self.split_empty_lines()
        else:
            return self.lines

    def non_empty_lines(self):
        return list(filter(lambda x: x != '', self.lines))

    def __iter__(self):
        return iter(self.paragraphs())

    def __len__(self):
        return len(self.paragraphs())

    def __repr__(self):
        return self.__class__.__name__ + "[" + str(len(self)) + "]"
