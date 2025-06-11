from dataclasses import dataclass
import re


class Author:
    def __init__(self, country, firstName, lastName):
        self.country = country
        self.firstName = firstName
        self.lastName = lastName


class Reference:
    def __init__(self, raw) :
        self.raw=''                # 原始参考文献字符串
        # self.authors = []          # 作者
        self.authors = ''          # 作者
        self.year = ''             # 出版年份
        self.title = ''            # 文章或书籍标题
        self.venue = ''            # 发表的期刊、会议
        self.volume = ''           # 期刊卷号
        self.issue = ''            # 期刊期号
        self.pages = ''            # 页码范围
        self.pubplace = ''         # 出版地
        self.publisher = ''        # 出版社（书籍或会议）
        self.access_date= ''       # 网页访问日期
        self.doi = ''              # DOI编号
        self.url = ''              # URL链接
        self.ref_type = ''         # 文献类型（期刊、会议、书籍、网页等）

def extract_doi(text: str) -> str:
    m = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.IGNORECASE)
    return m.group(0) if m else ''


def extract_url(text: str) -> str:
    m = re.search(r"https?://\S+", text)
    return m.group(0).rstrip('.,') if m else ''


def extract_year(text: str) -> str:
    m = re.search(r"(19\d{2}|20\d{2})", text)
    return m.group(1) if m else ''


def parse_reference(text: str) -> Reference:
    # 如果语法解析失败，返回空字段，仅保留 raw
    return Reference(raw=text)

# def parse_references_bulk(text_block: str, auto_doi: bool = True) -> list[Reference]:
#     """
#     使用 ANTLR4 解析多行单条参考文献（Grammar 顶层是 citation），返回 Reference 列表。
#     解析错误时，返回空字段的 Reference。
#     """
#     results = []
#     lines = [line.strip() for line in text_block.splitlines() if line.strip()]
#     for line in lines:
#         try:
#             # 用 ANTLR4 解析单条 citation
#             stream = InputStream(line)
#             lexer = CitationLexer.CitationLexer(stream)
#             tokens = CommonTokenStream(lexer)
#             parser = CitationParser.CitationParser(tokens)
#             tree = parser.citation()
#
#             listener = CitationListener.CitationCustomListener(auto_doi=auto_doi)
#             walker = ParseTreeWalker()
#             walker.walk(listener, tree)
#
#             ref = listener.reference
#             if ref:
#                 results.append(ref)
#             else:
#                 results.append(Reference(raw=line))
#         except Exception as e:  # 捕获所有异常
#             print(f"发生错误: {e}")  # 打印错误信息
#             results.append(Reference(raw='错误！非标准格式'))
#     return results