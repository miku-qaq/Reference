import requests
from typing import List
import openai
import json  # 添加json模块

# 设置 DeepSeek API
openai.api_key = "sk-4a9e01274c4f48dbafa94c2c04b32a30"  # 请替换成您自己的有效API Key


class Reference:
    def __init__(self, raw: str):
        self.raw = raw.strip()
        self.authors = ''
        self.year = ''
        self.title = ''
        self.venue = ''
        self.volume = ''
        self.issue = ''
        self.pages = ''
        self.pubplace = ''
        self.publisher = ''
        self.access_date = ''
        self.doi = ''
        self.url = ''
        self.ref_type = ''

    def __repr__(self):
        return f"<Reference title={self.title!r} authors={self.authors!r} year={self.year!r} doi={self.doi!r}>"

    def to_dict(self):
        """
        将 Reference 对象的属性转换为一个字典，以便进行 JSON 序列化并发送给前端。
        特别处理 'authors' 字段，确保它是一个列表（前端JavaScript期望的格式）。
        """
        return {
            'raw': self.raw,
            # 将作者字符串（如 "Smith J., Chen L."）分割成列表
            'authors': self.authors.split(', ') if isinstance(self.authors, str) and self.authors else [],
            'year': self.year,
            'title': self.title,
            'venue': self.venue,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
            'pubplace': self.pubplace,
            'publisher': self.publisher,
            'access_date': self.access_date,
            'doi': self.doi,
            'url': self.url,
            'ref_type': self.ref_type,
        }


# CrossRef API
CROSSREF_API = 'https://api.crossref.org/works'


def extract_metadata_deepseek(raw_reference: str) -> dict:
    """
    使用 DeepSeek 模型调用接口进行中文参考文献结构化抽取。
    """
    prompt = f"""
你是一个文献解析助手，请从下面这条参考文献中提取以下字段，并返回标准 JSON 格式：
- authors（作者列表，用逗号分隔）
- year（年份）
- title（标题）
- venue（期刊或会议名称）
- volume（卷号）
- issue（期号）
- pages（页码）
- pubplace（出版地）
- publisher（出版社）
- access_date（访问日期）
- url（链接）
- ref_type（文献类型，如 journal/book/web/conference）
- doi（数字对象唯一标识符）

参考文献：
{raw_reference}
"""
    try:
        client = openai.OpenAI(
            api_key=openai.api_key,
            base_url='https://api.deepseek.com/v1'  # 添加/v1路径
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}  # 确保返回JSON格式
        )

        # 正确访问响应对象的方式（使用属性而不是下标）
        reply = response.choices[0].message.content

        return json.loads(reply)  # 使用json模块解析
    except Exception as e:
        print(f"DeepSeek 解析失败：{e}")
        return {}


def fetch_crossref_metadata(query: str) -> dict:
    try:
        params = {'query.bibliographic': query, 'rows': 1}
        r = requests.get(CROSSREF_API, params=params, timeout=10)
        r.raise_for_status()
        items = r.json().get('message', {}).get('items', [])
        if items:
            return items[0]
    except Exception:
        pass
    return {}

def parse_reference(raw: str) -> Reference:
    ref = Reference(raw)
    meta = extract_metadata_deepseek(ref.raw)
    for field in ['authors', 'year', 'title', 'venue', 'volume', 'issue', 'pages', 'pubplace', 'publisher', 'access_date', 'url', 'ref_type', 'doi']:
        if meta.get(field):
            setattr(ref, field, meta[field])
    if not ref.doi and ref.title:
        query_str = ' '.join(filter(None, [ref.title, ref.authors, ref.year]))
        cr_meta = fetch_crossref_metadata(query_str)
        if cr_meta:
            ref.doi = cr_meta.get('DOI', '')
            if not ref.authors:
                ref.authors = ', '.join(f"{p.get('family','')} {p.get('given','')}" for p in cr_meta.get('author', []))
            if not ref.venue:
                ref.venue = (cr_meta.get('container-title') or [''])[0]
            if not ref.year:
                dates = cr_meta.get('issued', {}).get('date-parts', [[None]])
                ref.year = str(dates[0][0]) if dates[0][0] else ''
            if not ref.title:
                ref.title = (cr_meta.get('title') or [''])[0]
    return ref

def parse_references_bulk(text_block: str) -> List[Reference]:
    lines = [line for line in text_block.strip().splitlines() if line.strip()]
    results: List[Reference] = []
    for line in lines:
        try:
            results.append(parse_reference(line))
        except Exception:
            results.append(Reference(line))
    return results
