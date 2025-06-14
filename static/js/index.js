// 全局变量，用于存储解析后的结构化参考文献数据
// 它们在页面初始化时为空，会在接收到后端数据后更新
let parsedReferences = [];

// 全局变量，用于存储当前显示或即将导出的格式化参考文献字符串列表
let currentFormattedReferences = [];

// 全局变量，用于存储当前作者对象列表
let authors = [];


// 全局变量，表示当前选择的参考文献格式（默认为GB/T 7714）
// 该值会在用户点击格式按钮时更新，并可能从Flask模板中初始化
let currentStyle = 'gbt7714';

// 全局变量，指示是否在解析过程中检测到重复引用
let duplicatesExist = false;

// 获取DOM元素
const referenceForm = document.getElementById('referenceForm');
const resultsList = document.getElementById('resultsList');
const duplicateNotice = document.getElementById('duplicate-notice');
const exportForm = document.getElementById('exportForm');
const loadingIndicator = document.getElementById('loading-indicator');
const styleButtons = document.querySelectorAll('.style-button');
const parseButton = document.getElementById('parseButton');
const exportButton = document.getElementById('exportButton');
const exportTypeSelect = document.getElementById('export_type');

/**
 * 显示自定义消息框。
 * @param {string} title - 消息框的标题。
 * @param {string} message - 消息框的内容。
 */
function showMessageBox(title, message) {
    const msgBox = document.getElementById('message-box');
    document.getElementById('message-title').textContent = title;
    document.getElementById('message-content').HTMLContent = message;
    msgBox.classList.remove('hidden'); // 显示消息框
    document.getElementById('message-close').onclick = () => {
        msgBox.classList.add('hidden'); // 点击确定按钮隐藏消息框
    };
}

/**
 * 检查一个字符是否为中文字符。
 * @param {string} char - 要检查的字符。
 * @returns {boolean} 如果是中文字符则返回 true，否则返回 false。
 */
function isChinese(char) {
    return /[\u4e00-\u9fa5]/.test(char);
}


/**
 * 使用 pinyin-pro 库将中文姓名转换为拼音。
 * 重要提示：此函数依赖于本地的 `pinyin-pro` 库（index.min.js）。
 *
 * @param {string} chineseName - 中文姓名字符串。
 * @returns {object} 包含 `last` (姓的拼音) 和 `first` (名的拼音) 的对象。
 */
function convertToPinyin(chineseName) {
    // 检查 pinyin-pro 库是否已加载
    if (typeof window.pinyinPro === 'undefined' || typeof window.pinyinPro.pinyin !== 'function') {
        console.error("Error: pinyin-pro 库未加载，无法转换拼音。");
        return { last: '', first: '' };
    }

    // 调用 pinyin-pro, mode: 'surname' 确保第一个是姓
    const arr = window.pinyinPro.pinyin(chineseName, {
        toneType: "none",
        type: "array",
        mode: "surname"
    });

    let last = '';
    let first = '';

    if (arr.length > 0) {
        last = arr[0] || '';
        if (arr.length > 1) {
            first = arr.slice(1).join('');
        }
    }

    return {
        last: last.toLowerCase(),
        first: first.toLowerCase()
    };
}


/**
 * 解析单个作者字符串（英文或中文）为结构化组件。
 * 保留原有的首字母大写、缩写和中间名处理规则。
 *
 * @param {string} authorString - 单个作者的原始字符串（例如 'M. Aspelmeyer' 或 '张三'）。
 * @returns {object} 包含以下属性的对象：
 *   - chineseName: 如果是中文名，则为原始中文名字符串，否则为空字符串。
 *   - LastName: 首字母大写的姓氏（中文为拼音，英文则从英文名中提取）。
 *   - FirstName: 首字母大写后的名字/缩写（中文为拼音，英文则从英文名中提取）。
 *   - MiddleName: 首字母大写后的中间名缩写（如果存在，否则为空字符串）。
 */
function parseAuthor(authorString) {
    const trimmedAuthor = authorString.trim();
    let result = {
        chineseName: '',
        LastName: '',
        FirstName: '',
        MiddleName: '' // 默认为空字符串，在英文名解析时可能被填充
    };

    if (trimmedAuthor === '') {
        return result;
    }

    // 检查是否包含中文字符，判断为中文名
    if (isChinese(trimmedAuthor.charAt(0))) {
        result.chineseName = trimmedAuthor;
        const pinyin = convertToPinyin(trimmedAuthor);

        // 拼音转换后的姓和名首字母大写
        result.LastName = pinyin.last
            ? pinyin.last.charAt(0).toUpperCase() + pinyin.last.slice(1)
            : '';
        result.FirstName = pinyin.first
            ? pinyin.first.charAt(0).toUpperCase() + '.'
            : '';
    } else {
        // 处理英文名格式：通常为 First Middle Last 或 F. M. Last
        const parts = trimmedAuthor.split(' ').filter(p => p !== '');

        if (parts.length === 0) {
            return result;
        }

        // 最后一个部分通常是姓氏
        result.LastName = parts.pop();
        result.LastName = result.LastName.charAt(0).toUpperCase() + result.LastName.slice(1);

        // 处理剩余的部分作为名字 (FirstName 和 MiddleName)
        let remainingNameParts = parts;

        // 如果剩余部分多于一个，并且最后一个部分看起来像中间名缩写（以点号结尾）
        if (
            remainingNameParts.length > 1 &&
            remainingNameParts[remainingNameParts.length - 1].endsWith('.')
        ) {
            result.MiddleName = remainingNameParts.pop();
            result.MiddleName = result.MiddleName.charAt(0).toUpperCase() + result.MiddleName.slice(1);
        }

        // 处理剩余的作为 FirstName，统一缩写形式
        let firstNameComponents = [];
        remainingNameParts.forEach(part => {
            if (part.length > 0) {
                if (part.endsWith('.')) {
                    // 已有缩写，如 'M.'
                    firstNameComponents.push(part.charAt(0).toUpperCase() + '.');
                } else {
                    // 全名，转换为首字母加点
                    firstNameComponents.push(part.charAt(0).toUpperCase() + '.');
                }
            }
        });
        result.FirstName = firstNameComponents.join(' ');
    }

    return result;
}
/**
 * 将逗号分隔的作者字符串解析为结构化的作者对象列表。
 *
 * @param {string} authorsString - 逗号分隔的作者姓名字符串，
 * 例如：'M. Aspelmeyer, T. J. Kippenberg, F. Marquardt,张三'。
 * @returns {Array<object>} 一个包含作者对象的列表，每个对象具有 `chineseName`, `LastName`, `FirstName`, `MiddleName` 属性。
 * 如果输入字符串为空或解析后无有效作者，则返回空数组。
 */
function formatAuthors(authorsString) {
    const parsedAuthorsList = [];
    if (!authorsString || authorsString.trim() === '') {
        return parsedAuthorsList; // 返回空数组而不是“佚名”
    }

    // 分割作者字符串，去除空格，并过滤空字符串
    const authorStrings = authorsString.split(',').map(s => s.trim()).filter(s => s !== '');

    // 遍历每个作者字符串并进行解析
    authorStrings.forEach(authorString => {
        parsedAuthorsList.push(parseAuthor(authorString));
    });

    return parsedAuthorsList;
}


/**
 * 根据GB/T 7714标准格式化参考文献对象。
 * @param {object} ref - 解析后的参考文献对象。
 * @returns {string} 格式化后的参考文献字符串。
 */
function format_gbt7714_js(ref) {
    let parts = [];
    const title = ref.title || '无标题';

    let displayedAuthors = [];
    for (let i = 0; i < authors.length; i++) {
        const author = authors[i];
        if (author.chineseName) {
            // 中文名直接使用原始中文名
            displayedAuthors.push(author.chineseName);
        } else {
            // 英文名：姓在前，名（缩写）和中间名（缩写）在后，用逗号分隔
            let englishNameParts = [];
            englishNameParts.push(author.LastName); // 姓氏
            englishNameParts.push(' ');

            let initials = [];
            if (author.FirstName) {
                initials.push(author.FirstName);
            }
            if (author.MiddleName) {
                initials.push(author.MiddleName);
            }
            // 将名和中间名缩写用空格连接
            const initialsString = initials.join(' ');

            // 如果有缩写，则添加逗号和缩写部分
            if (initialsString) {
                englishNameParts.push(initialsString);
            }
            displayedAuthors.push(englishNameParts.join(''));
        }
    }

    let finalAuthorString = displayedAuthors.join(','); // 作者之间用全角逗号

    if (finalAuthorString !== "") {
        finalAuthorString += '.'; // 末尾加句号
        parts.push(finalAuthorString);
    }

    let suffix = '';
    if (ref.ref_type === 'journal') {
        suffix = '[J]';
    } else if (ref.ref_type === 'conference') {
        suffix = '[C]//';
    } else if (ref.ref_type === 'book') {
        suffix = '[M]';
    } else if (ref.ref_type === 'web') {
        suffix = '[EB/OL]';
    }
    if (title)
        parts.push(`${title}${suffix}.`);

    if (ref.ref_type === 'journal') {
        if (ref.venue) parts.push(`${ref.venue},`);
        if (ref.year) parts.push(`${ref.year},`);
        if (ref.volume) {
            if (ref.issue) {
                parts.push(`${ref.volume}(${ref.issue}):`);
            } else {
                parts.push(`${ref.volume}:`);
            }
        }
        if (ref.pages) parts.push(`${ref.pages}.`);
        if (ref.doi) parts.push(`DOI:${ref.doi}.`);
    } else if (ref.ref_type === 'conference') {
        if (ref.venue) parts.push(`${ref.venue},`);
        if (ref.year) parts.push(`${ref.year}:`);
        if (ref.pages) parts.push(`${ref.pages}.`);
        if (ref.doi) parts.push(`DOI:${ref.doi}.`);
    } else if (ref.ref_type === 'book') {
        if (ref.pubplace && ref.publisher) {
            parts.push(`${ref.pubplace}: ${ref.publisher},`);
        } else if (ref.publisher) {
            parts.push(`${ref.publisher},`);
        }
        if (ref.year) parts.push(`${ref.year}.`);
    } else if (ref.ref_type === 'web') {
        if (ref.year) parts.push(`${ref.year}.`);
        if (ref.url) parts.push(ref.url);
        if (ref.access_date) parts.push(`(${ref.access_date}).`);
    } else {
        return ref.raw.trim();
    }

    return parts.join(' ').replace(/\s\s+/g, ' ').trim(); // 替换多个空格为单个空格
}

/**
 * 根据APA标准格式化参考文献对象。
 * @param {object} ref - 解析后的参考文献对象。
 * @returns {string} 格式化后的参考文献字符串。
 */
function format_apa_js(ref) {
    let parts = [];
    const year = ref.year ? `(${ref.year})` : '(n.d.)'; // 如果年份缺失，使用(n.d.)
    const title = ref.title || '无标题';

    let displayedAuthors = [];
    for (let i = 0; i < authors.length; i++) {
        const author = authors[i];

        // 英文名：姓在前，名（缩写）和中间名（缩写）在后，用逗号分隔
        let englishNameParts = [];

        let initials = [];
        if (author.FirstName) {
            initials.push(author.FirstName);
        }
        if (author.MiddleName) {
            initials.push(author.MiddleName);
        }
        // 将名和中间名缩写用空格连接
        const initialsString = initials.join(' ');

        // 如果有缩写，则添加逗号和缩写部分
        if (initialsString) {
            englishNameParts.push(initialsString);

        }
        englishNameParts.push(' ');
        englishNameParts.push(author.LastName); // 姓氏

        displayedAuthors.push(englishNameParts.join(''));
    }
    if(authors.length > 1) {
        let lastAuthor = displayedAuthors.pop()
        displayedAuthors.push('& ' + lastAuthor)
    }

    let finalAuthorString = displayedAuthors.join(',');
    if(finalAuthorString)
        parts.push(finalAuthorString);

    if (year)
        parts.push(`${year}.`);
    if (title)
        parts.push(`${title}.`);

    if (ref.ref_type === 'journal') {
        if (ref.venue) parts.push(`${ref.venue},`); // 期刊名斜体
        if (ref.volume) {
            if (ref.issue) {
                parts.push(`${ref.volume}(${ref.issue}),`);
            } else {
                parts.push(`${ref.volume},`);
            }
        }
        if (ref.pages) parts.push(`${ref.pages}.`);
        if (ref.doi) parts.push(`https://doi.org/${ref.doi}`);
    } else if (ref.ref_type === 'conference') {
        if (ref.venue) parts.push(`In ${ref.venue} (pp. ${ref.pages || 'N/A'}).`);
        if (ref.doi) parts.push(`https://doi.org/${ref.doi}`);
        else if (ref.url) parts.push(ref.url);
    } else if (ref.ref_type === 'book') {
        if (ref.pubplace && ref.publisher) {
            parts.push(`${ref.pubplace}: ${ref.publisher}.`);
        } else if (ref.publisher) {
            parts.push(`${ref.publisher},`);
        }
    } else if (ref.ref_type === 'web') {
        if (ref.url) parts.push(`Retrieved from ${ref.url}`);
    } else {
        return ref.raw.trim();
    }

    return parts.join(' ').replace(/\s\s+/g, ' ').trim();
}

/**
 * 根据IEEE标准格式化参考文献对象。
 * @param {object} ref - 解析后的参考文献对象。
 * @returns {string} 格式化后的参考文献字符串。
 */
function format_ieee_js(ref) {
    let parts = [];
    const title = ref.title || '无标题';

    let displayedAuthors = [];
    for (let i = 0; i < authors.length; i++) {
        const author = authors[i];

        let englishNameParts = [];
        englishNameParts.push(author.LastName); // 姓氏
        englishNameParts.push(', ');

        let initials = [];
        if (author.FirstName) {
            initials.push(author.FirstName);
        }
        if (author.MiddleName) {
            initials.push(author.MiddleName);
        }
        // 将名和中间名缩写用空格连接
        const initialsString = initials.join(' ');

        // 如果有缩写，则添加逗号和缩写部分
        if (initialsString) {
            englishNameParts.push(initialsString);
        }

        displayedAuthors.push(englishNameParts.join(''));
    }

    if(authors.length > 1) {
        let lastAuthor = displayedAuthors.pop();
        displayedAuthors.push('and ' + lastAuthor);
    }

    let finalAuthorString = displayedAuthors.join(',');

    if(finalAuthorString) {
        finalAuthorString += ',';
        parts.push(finalAuthorString);
    }


    if (title)
        parts.push(`"${title}",`); // 标题用双引号包裹

    if (ref.ref_type === 'journal') {
        if (ref.venue) parts.push(`${ref.venue},`);
        if (ref.volume) parts.push(`vol. ${ref.volume},`);
        if (ref.issue) parts.push(`no. ${ref.issue},`);
        if (ref.pages) parts.push(`pp. ${ref.pages},`);
        if (ref.year) parts.push(`${ref.year}.`);
        if (ref.doi) parts.push(`DOI:${ref.doi}`);
    } else if (ref.ref_type === 'conference') {
        if (ref.venue) parts.push(`in Proc. of ${ref.venue},`);
        if (ref.pages) parts.push(`pp. ${ref.pages},`);
        if (ref.year) parts.push(`${ref.year}.`);
        if (ref.doi) parts.push(`DOI:${ref.doi}`);
    } else if (ref.ref_type === 'book') {
        if (ref.pubplace && ref.publisher) {
            parts.push(`${ref.pubplace}: ${ref.publisher},`);
        } else if (ref.publisher) {
            parts.push(`${ref.publisher},`);
        }
        if (ref.year) parts.push(`${ref.year}.`);
    } else if (ref.ref_type === 'web') {
        parts.push("[Online].");
        if (ref.url) parts.push(`Available: ${ref.url}`);
    } else {
        return ref.raw.trim();
    }

    let formatted = parts.join(' ').replace(/\s\s+/g, ' ').trim();
    // 移除末尾可能多余的逗号或空格
    while (formatted.endsWith(',') || formatted.endsWith(' ')) {
        formatted = formatted.slice(0, -1);
    }
    return formatted.trim();
}


/**
 * 根据当前选定的样式，调度到相应的格式化函数。
 * @param {object} ref - 解析后的参考文献对象。
 * @param {string} style - 要应用的引用样式 ('gbt7714', 'apa', 'ieee')。
 * @returns {string} 格式化后的参考文献字符串。
 */
function formatReference(ref, style) {
    authors = formatAuthors(ref.authors);
    console.log(authors);
    switch (style) {
        case 'gbt7714':
            return format_gbt7714_js(ref);
        case 'apa':
            return format_apa_js(ref);
        case 'ieee':
            return format_ieee_js(ref);
        default:
            return ref.raw.trim(); // 未知样式时返回原始文本
    }
}

/**
 * 将格式化后的参考文献渲染到DOM中，并更新 currentFormattedReferences 数组。
 * @param {string} style - 要应用的样式 ('gbt7714', 'apa', 'ieee')。
 */
function renderReferences(style) {
    resultsList.innerHTML = ''; // 清空现有结果
    currentFormattedReferences = []; // 清空之前格式化的参考文献

    if (parsedReferences.length === 0) {
        resultsList.innerHTML = '<p class="text-gray-500">暂无参考文献数据。</p>';
        duplicateNotice.classList.add('hidden'); // 隐藏去重提示
        exportForm.classList.add('hidden'); // 隐藏导出表单
        return;
    }

    exportForm.classList.remove('hidden'); // 显示导出表单

    // 遍历解析后的参考文献，进行格式化并添加到页面
    parsedReferences.forEach((ref) => {
        const formattedRef = formatReference(ref, style);
        currentFormattedReferences.push(formattedRef); // 存储格式化后的字符串

        const div = document.createElement('div');
        div.className = 'result-item bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500 text-gray-800 text-sm break-words';
        div.textContent = formattedRef;
        resultsList.appendChild(div);
    });

    // 根据duplicatesExist状态显示或隐藏去重提示
    if (duplicatesExist) {
        duplicateNotice.classList.remove('hidden');
    } else {
        duplicateNotice.classList.add('hidden');
    }
}

// ============== 事件监听器 ==============

// 监听样式按钮的点击事件
styleButtons.forEach(button => {
    button.addEventListener('click', () => {
        // 移除所有按钮的激活状态样式
        styleButtons.forEach(btn => {
            btn.classList.remove('bg-blue-100', 'text-blue-700', 'border-blue-200');
            btn.classList.add('bg-white', 'text-gray-900', 'border-gray-200');
        });

        // 为当前点击的按钮添加激活状态样式
        button.classList.add('bg-blue-100', 'text-blue-700', 'border-blue-200');
        button.classList.remove('bg-white', 'text-gray-900', 'border-gray-200');

        currentStyle = button.dataset.style; // 更新当前样式
        // 更新隐藏的输入字段，以便在需要时（虽然异步提交不再需要）可以发送到后端
        document.getElementById('selectedStyleHiddenInput').value = currentStyle;
        renderReferences(currentStyle); // 根据新样式重新渲染参考文献
    });
});

// 监听“解析参考文献”表单的提交事件
referenceForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // 阻止表单默认提交行为（阻止页面刷新）

    // 显示加载指示器
    loadingIndicator.classList.remove('hidden');
    parseButton.disabled = true; // 禁用按钮，防止重复点击
    exportButton.disabled = true; // 禁用导出按钮

    const form = event.target;
    const formData = new FormData(form);

    try {
        // 发送异步请求到后端API
        const response = await fetch('/api/parse-references', {
            method: 'POST',
            body: formData // 直接发送FormData对象，支持文件和文本混合
        });

        if (!response.ok) {
            // 如果HTTP响应状态码不是2xx，抛出错误
            const errorText = await response.text();
            throw new Error(`Server responded with status ${response.status}: ${errorText}`);
        }

        // 解析后端返回的JSON数据
        const result = await response.json();

        if (result.success) {
            parsedReferences = result.parsed_references || []; // 更新解析后的结构化数据
            duplicatesExist = result.duplicates_exist || false; // 更新去重标志
            renderReferences(currentStyle); // 使用新数据渲染结果
        } else {
            // 后端逻辑错误
            showMessageBox('解析失败', result.message || '服务器返回错误。');
        }
    } catch (error) {
        console.error('解析请求失败:', error);
        showMessageBox('错误', `发送解析请求时发生错误，请检查网络连接或联系管理员。<br>错误信息: ${error.message}`);
    } finally {
        // 隐藏加载指示器并重新启用按钮
        loadingIndicator.classList.add('hidden');
        parseButton.disabled = false;
        exportButton.disabled = false;
    }
});

// 监听“导出”表单的提交事件（客户端本地导出）
exportForm.addEventListener('submit', (event) => {
    event.preventDefault(); // 阻止表单默认提交行为

    // 如果没有参考文献可导出，则显示提示
    if (currentFormattedReferences.length === 0) {
        showMessageBox('导出失败', '没有可导出的参考文献。请先解析参考文献。');
        return;
    }

    const exportType = exportTypeSelect.value; // 获取选择的导出类型
    let fileContent = '';
    let filename = `参考文献.${exportType}`;
    let mimeType = '';

    // 根据导出类型生成文件内容
    if (exportType === 'txt') {
        fileContent = currentFormattedReferences.join('\n'); // 文本文件，每条参考文献一行
        mimeType = 'text/plain';
        filename = '参考文献.txt';
    } else if (exportType === 'latex') {
        // 为LaTeX文件生成一个非常基本的biblio环境
        const latexEntries = currentFormattedReferences.map((ref, index) => {
            // 对LaTeX特殊字符进行简单转义
            const escapedRef = ref.replace(/&/g, '\\&')
                                .replace(/%/g, '\\%')
                                .replace(/\$/g, '\\$')
                                .replace(/#/g, '\\#')
                                .replace(/_/g, '\\_')
                                .replace(/{/g, '\\{')
                                .replace(/}/g, '\\}')
                                .replace(/~/g, '\\textasciitilde{}')
                                .replace(/\^/g, '\\textasciicircum{}')
                                .replace(/\\/g, '\\textbackslash{}'); // 处理反斜杠本身

            return `\\bibitem{ref${index + 1}}{${escapedRef}}`; // 生成 \bibitem 条目
        }).join('\n\n'); // 条目之间用双换行符分隔

        fileContent = `
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{hyperref} % 可选: 用于超链接
\\usepackage{url}      % 可选: 用于URL
\\begin{document}

\\section*{参考文献}
\\begin{thebibliography}{99}
${latexEntries}
\\end{thebibliography}

\\end{document}
        `.trim(); // 移除首尾空白

        mimeType = 'application/x-latex';
        filename = '参考文献.tex';
    } else {
        // 不支持的导出类型
        showMessageBox('导出失败', '不支持的导出类型。');
        return;
    }

    try {
        // 创建Blob对象和URL，触发文件下载
        const blob = new Blob([fileContent], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename; // 设置下载文件名
        document.body.appendChild(a); // 将a标签添加到DOM
        a.click(); // 模拟点击，触发下载
        document.body.removeChild(a); // 移除a标签
        URL.revokeObjectURL(url); // 释放URL对象，避免内存泄漏
        showMessageBox('导出成功', `参考文献已导出为 ${exportType.toUpperCase()} 文件。`);
    } catch (error) {
        console.error('客户端导出失败:', error);
        showMessageBox('错误', '执行客户端导出时发生错误。');
    }
});

// 初始化：设置当前激活的样式按钮
// 确保在页面加载后正确显示默认或从Flask传入的样式
document.addEventListener('DOMContentLoaded', () => {
    // 强制触发一次点击事件，以确保样式按钮和初始渲染状态正确
    const initialStyleButton = document.querySelector(`.style-button[data-style="${currentStyle}"]`);
    if (initialStyleButton) {
        initialStyleButton.click();
    }
});
