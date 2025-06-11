# app.py
import json
from flask import Flask, render_template, request, jsonify
import io  # 保留io导入，以防其他未展示部分需要，但当前代码逻辑中未直接使用。

# 从 parser.py 文件中导入 Reference 类和解析函数
# 假设 parser.py 位于与 app.py 同级的目录中
from parser import Reference, parse_references_bulk

app = Flask(__name__)


# GET 请求：仅用于渲染初始页面
@app.route('/', methods=['GET'])
def index():
    """
    处理对根路径的GET请求。
    此路由主要用于加载初始HTML页面，不执行参考文献解析操作。
    前端JavaScript将通过异步请求（POST到/api/parse-references）处理实际的解析逻辑。
    """
    return render_template(
        'index.html',
        raw_input='',  # 初始加载页面时，文本区域为空
        style='gbt7714'  # 初始默认选择 GB/T 7714 格式
    )


# POST 请求：新的 API 路由，用于异步解析参考文献
@app.route('/api/parse-references', methods=['POST'])
def api_parse_references():
    """
    处理来自前端的异步POST请求，用于解析参考文献。
    接收用户输入的文本和上传的文件，调用后端解析器进行处理，
    然后返回结构化数据（JSON格式）给前端。
    """
    raw_input_content = ''
    duplicates_found = False
    parsed_references_dicts = []

    # --- 1. 处理文件上传 ---
    file = request.files.get('file')
    file_input_content = ''
    if file and file.filename:
        try:
            # 尝试读取文件内容，假设是UTF-8编码
            file_input_content = file.stream.read().decode('utf-8')
        except Exception as e:
            # 如果文件读取失败，返回错误信息和HTTP 400状态码
            return jsonify({'success': False, 'message': f'文件读取失败: {e}'}), 400

    # --- 2. 处理文本区输入 ---
    text_input_content = request.form.get('references', '')

    # --- 3. 合并文件和文本输入 ---
    # 去除合并后字符串的首尾空白，并处理只有换行符的情况
    raw_input_content = (file_input_content + '\n' + text_input_content).strip()
    if raw_input_content == '\n':  # 如果合并后的内容仅包含换行符，则视为空输入
        raw_input_content = ''

    # --- 4. 调用解析器并处理数据 ---
    if raw_input_content:  # 只有当有实际输入内容时才进行解析
        # 调用 parser.py 中导入的实际解析函数
        # parse_references_bulk 函数应返回 Reference 对象的列表
        refs_objects = parse_references_bulk(raw_input_content)

        # 用于存储去重后的参考文献字典（供前端使用）
        temp_parsed_data = []
        # 用于记录已处理的参考文献的唯一键，以便去重
        seen_keys = set()

        # 遍历解析出的 Reference 对象列表
        for r_obj in refs_objects:
            # 构造用于去重的唯一键 (作者, 年份, 标题)
            # 确保 authors 在 Reference 对象中是字符串形式，以便构建键
            author_key = r_obj.authors if isinstance(r_obj.authors, str) else ', '.join(r_obj.authors)
            key = (author_key, r_obj.year, r_obj.title)

            # 检查当前参考文献是否已经处理过（去重逻辑）
            if key in seen_keys:
                duplicates_found = True  # 标记检测到重复
                continue  # 跳过当前重复的参考文献，不将其添加到结果中

            seen_keys.add(key)  # 将当前参考文献的唯一键加入已见集合

            # 将 Reference 对象转换为 JSON 友好的字典格式
            # Reference 类中的 to_dict 方法会将 authors 属性处理为列表，适合前端JavaScript使用
            temp_parsed_data.append(r_obj.to_dict())

        parsed_references_dicts = temp_parsed_data
    else:
        # 如果没有有效的输入内容（包括空字符串），则返回空结果列表
        parsed_references_dicts = []
        duplicates_found = False

    # --- 5. 返回 JSON 格式的响应 ---
    # jsonify 会自动将Python字典转换为JSON字符串，并设置HTTP响应头 Content-Type: application/json
    return jsonify({
        'success': True,  # 表示后端请求处理成功
        'message': '参考文献解析成功。',  # 返回给前端的消息
        'parsed_references': parsed_references_dicts,  # 结构化元数据列表，供前端JavaScript渲染
        'duplicates_exist': duplicates_found  # 是否存在重复的标志，供前端显示去重提示
    })


# /export 路由现在不再需要，因为导出功能已完全在前端JavaScript中实现。

if __name__ == '__main__':
    # 启动 Flask 应用
    # debug=True 会在代码更改时自动重载，并提供调试信息，适合开发环境
    app.run(debug=True)
