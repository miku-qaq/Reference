grammar Citation;
options { language=Python3; }

// ====================== Parser Rules ======================

// 顶级引用规则，匹配任意类型的引用
citation: bookCitation | journalCitation | conferenceCitation | webCitation;

/* 书籍引用规则 */
bookCitation: apaBook | ieeeBook | gbtBook;
// APA 格式: 作者 (年份). 书名. 出版社.
apaBook: apaAuthors ('(' | '（') year (')' | '）') '.' title ('('  ')')? '.' publisher'.';
// IEEE 格式: 作者, "书名", 出版社, 年份.
ieeeBook: ieeeAuthors ',' ' '* '"' title'"' ' '* ',' (place ':')? publisher ',' year '.';
// GB/T 7714: 作者. 书名[M]. 出版地: 出版社, 出版年: 页码.
gbtBook: gbtAuthors '.' title '[M]' ' '* '.' (place':')?  publisher',' year '.';

/* 期刊引用规则 */
journalCitation: apaJournal | ieeeJournal | gbtJournal;
// APA: 作者 (年份). 文章标题. 期刊名, 卷号(期号), 页码.
apaJournal: apaAuthors ' '* ('(' | '（') year (')' | '）') ' '* '.' title '.' venue ',' volume ('(' issue ')')? ':' pages '.'?;
// IEEE: 作者, "文章标题", 期刊名, vol. 卷号, no. 期号, pp. 页码, 年份.
ieeeJournal: ieeeAuthors ',' ' '* '"' title ',' '"' ' '*  venue ',' ' '* 'vol.' volume ',' ' '* 'no.' issue ','  ' '* 'pp.' pages ',' year '.';
// GB/T 7714: 作者. 文章标题[J]. 期刊名, 年, 卷号(期号): 页码.
gbtJournal: gbtAuthors '.' title '[J]' ' '* '.' venue ',' year ',' volume '(' issue ')' ':' pages'.';

/* 会议引用规则 */
conferenceCitation: apaConference | ieeeConference | gbtConference;
// APA 会议：作者 (年份). 标题. In 会议名称, 年份: 页码.
apaConference: apaAuthors ('(' | '“') year (')' | '”') '.' title '.' ('In' | 'in') venue ',' year ':' pages '.'?;
// IEEE 会议：作者, "标题", In 会议名称, 年份: 页码.
ieeeConference: ieeeAuthors ',' ' '* '"' title ','  '"' ' '* ('In' | 'in') venue ',' year ':' pages '.';
// GB/T 7714 会议：作者. 标题[C]. 会议名称(年份). 地点: 出版社, 年份 (会议论文集)?: 页码.
gbtConference: gbtAuthors '.' title '[C]' ' '* '//' venue ('(' year ')')? '.' place ':' publisher ',' year ':' pages '.';

/* 网页引用规则 */
webCitation: apaWeb | ieeeWeb | gbtWeb;
// APA Web：作者 (年份). 标题. Retrieved from URL
apaWeb: apaAuthors ('(' | '“') year (')' | '”') '.' title '.' 'Retrieved from' url;
// IEEE Web：作者, "标题", [Online]. Available: URL
ieeeWeb: ieeeAuthors ',' '"' title ',''"'  '[Online].' 'Available:' url;
// GB/T 7714 Web：作者. 标题[EB/OL]. [访问日期]. URL
gbtWeb: gbtAuthors '.' title '[EB/OL]' '.' '[' dates ']' '.' url;

/* 作者格式规则 */
// APA格式作者 (姓, 名)
apaAuthors: apaAuthor (',' apaAuthor)* ( ','? ' '* '&' apaAuthor)?;
apaAuthor:  englishNameApa | chineseName;

// IEEE格式作者 (全名)
ieeeAuthors: ieeeAuthor (',' ieeeAuthor)* ( ','? ' '* 'and' ieeeAuthor)? ;
ieeeAuthor: englishNameIeee | chineseName;

// GB/T格式作者 (全名)
gbtAuthors: gbtAuthor (',' gbtAuthor)* ( ','? ' '* ('和' | 'and') gbtAuthor)?;
gbtAuthor: chineseName | englishNameApa;

chineseName: string;
englishNameIeee: lastName '.' firstName;
englishNameApa: firstName ',' lastName '.';
firstName: string;
lastName: string;

volume: ' '* DIGIT ' '*;
issue: ' '* DIGIT ' '*;
pages: ' '* DIGIT '–' DIGIT ' '*;
url: string;
venue: ( string '.')+;
place: string;
title: string ( string | ':' | '-')* string;
publisher: string;
string: ' '* (LETTERS | DIGIT) ( LETTERS | DIGIT | ' ' )* ' '*;
year: ' '* LETTERS? ' '* DIGIT ' '* ;
dates:  year '-' ' '* DIGIT ' '* '-' ' '* DIGIT ' '*;

// ====================== Lexer Rules ======================
// 基础字符定义
LETTERS: [A-Za-z\u4e00-\u9fa5]+;  // 支持中英文字符
DIGIT: [0-9]+;

// 空白字符忽略
WS: [\t\r\n]+ -> skip;