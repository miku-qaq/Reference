from antlr4 import ParseTreeListener
from gen.dataDefinition import Reference, extract_doi, extract_url, extract_year,Author

class CitationCustomListener(ParseTreeListener):
    def __init__(self, auto_doi=True):
        self.auto_doi = auto_doi
        self.reference = None

    # 进入 citation 时，创建 Reference
    def enterCitation(self, ctx):
        self.reference = Reference(raw=ctx.getText())

    # 退出 citation 时，执行 DOI/URL 补全
    def exitCitation(self, ctx):
        r = self.reference
        if r is None:
            return
        if self.auto_doi and not r.doi:
            r.doi = extract_doi(r.raw)
        if not r.url:
            r.url = extract_url(r.raw)

    # ===== Common author exits =====
    def exitApaAuthors(self, ctx):
        if self.reference is None: return
        for author_ctx in ctx.apaAuthor():
            if author_ctx.chineseName():
                full_name = author_ctx.chineseName().getText().strip()
                author = Author(country='CN', firstName=full_name, lastName='')
            elif author_ctx.englishNameApa():
                en_name_ctx = author_ctx.englishNameApa()
                first_name = en_name_ctx.firstName().getText().strip()
                last_name = en_name_ctx.lastName().getText().strip()
                author = Author(country='NCN', firstName=first_name, lastName=last_name)
            self.reference.authors.append(author)

    def exitIeeeAuthors(self, ctx):
        if self.reference is None: return
        for author_ctx in ctx.ieeeAuthor():
            if author_ctx.chineseName():
                full_name = author_ctx.chineseName().getText().strip()
                author = Author(country='CN', firstName=full_name, lastName='')
            elif author_ctx.englishNameIeee():
                en_name_ctx = author_ctx.englishNameIeee()
                first_name = en_name_ctx.firstName().getText().strip()
                last_name = en_name_ctx.lastName().getText().strip()
                author = Author(country='NCN', firstName=first_name, lastName=last_name)
            self.reference.authors.append(author)

    def exitGbtAuthors(self, ctx):
        if self.reference is None: return
        for author_ctx in ctx.gbtAuthor():
            if author_ctx.chineseName():
                full_name = author_ctx.chineseName().getText().strip()
                author = Author(country='CN', firstName=full_name, lastName='')
            elif author_ctx.englishNameApa():
                en_name_ctx = author_ctx.englishNameApa()
                first_name = en_name_ctx.firstName().getText().strip()
                last_name = en_name_ctx.lastName().getText().strip()
                author = Author(country='NCN', firstName=first_name, lastName=last_name)
            self.reference.authors.append(author)

    # ===== APA =====
    def exitApaBook(self, ctx):
        r = self.reference
        if r is None: return
        r.year = extract_year(ctx.year().getText())
        r.title = ctx.title().getText().strip()
        r.publisher = ctx.publisher().getText().strip()
        r.ref_type = 'book'

    def exitApaJournal(self, ctx):
        r = self.reference
        if r is None: return
        r.year = extract_year(ctx.year().getText())
        r.title = ctx.title().getText().strip()
        r.venue = ctx.venue().getText().strip()
        r.volume = ctx.volume().getText().strip()
        if ctx.issue():
            r.issue = ctx.issue().getText().strip()
        r.pages = ctx.pages().getText().strip()
        r.ref_type = 'journal'

    def exitApaConference(self, ctx):
        r = self.reference
        if r is None: return
        # 第一个 year() 为出版年
        r.year = extract_year(ctx.year(0).getText())
        r.title = ctx.title().getText().strip()
        r.venue = ctx.venue().getText().strip()
        r.pages = ctx.pages().getText().strip()
        r.ref_type = 'conference'

    def exitApaWeb(self, ctx):
        r = self.reference
        if r is None: return
        r.year = extract_year(ctx.year().getText())
        r.title = ctx.title().getText().strip()
        r.url = ctx.url().getText().strip()
        r.ref_type = 'web'

    # ===== IEEE =====
    def exitIeeeBook(self, ctx):
        r = self.reference
        if r is None: return
        r.title = ctx.title().getText().strip()
        r.pubplace = ctx.place().getText().strip()
        r.publisher = ctx.publisher().getText().strip()
        r.year = ctx.year().getText().strip()
        r.ref_type = 'book'

    def exitIeeeJournal(self, ctx):
        r = self.reference
        if r is None: return
        r.title = ctx.title().getText().strip()
        r.venue = ctx.venue().getText().strip()
        r.volume = ctx.volume().getText().strip()
        r.issue = ctx.issue().getText().strip()
        r.pages = ctx.pages().getText().strip()
        r.year = ctx.year().getText().strip()
        r.ref_type = 'journal'

    def exitIeeeConference(self, ctx):
        r = self.reference
        if r is None: return
        r.title = ctx.title().getText().strip()
        r.venue = ctx.venue().getText().strip()
        r.pages = ctx.pages().getText().strip()
        r.year = ctx.year().getText().strip()
        r.ref_type = 'conference'

    def exitIeeeWeb(self, ctx):
        r = self.reference
        if r is None: return
        r.title = ctx.title().getText().strip()
        r.url = ctx.url().getText().strip()
        r.ref_type = 'web'

    # ===== GB/T =====
    def exitGbtBook(self, ctx):
        r = self.reference
        if r is None: return
        r.title = ctx.title().getText().strip()
        r.pubplace = ctx.place().getText().strip()
        r.publisher = ctx.publisher().getText().strip()
        r.year = ctx.year().getText().strip()
        r.ref_type = 'book'

    def exitGbtJournal(self, ctx):
        r = self.reference
        if r is None: return
        r.title = ctx.title().getText().strip()
        r.venue = ctx.venue().getText().strip()
        r.year = ctx.year().getText().strip()
        r.volume = ctx.volume().getText().strip()
        r.issue = ctx.issue().getText().strip()
        r.pages = ctx.pages().getText().strip()
        r.year = ctx.year().getText().strip()
        r.ref_type = 'journal'

    def exitGbtConference(self, ctx):
        r = self.reference
        if r is None: return
        r.title = ctx.title().getText().strip()
        r.venue = ctx.venue().getText().strip()
        # publication year 为第二个 year()
        r.year = ctx.year(1).getText().strip() if len(ctx.year()) > 1 else ''
        r.pubplace = ctx.place().getText().strip()
        r.publisher = ctx.publisher().getText().strip()
        r.pages = ctx.pages().getText().strip()
        r.ref_type = 'conference'

    def exitGbtWeb(self, ctx):
        r = self.reference
        if r is None: return
        r.title = ctx.title().getText().strip()
        r.access_date = ctx.dates().getText().strip()
        r.url = ctx.url().getText().strip()
        r.year = r.access_date.split('-')[0]
        r.ref_type = 'web'
