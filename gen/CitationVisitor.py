# Generated from C:/Users/bochi/PycharmProjects/FlaskProject/antlr/Citation.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CitationParser import CitationParser
else:
    from CitationParser import CitationParser

# This class defines a complete generic visitor for a parse tree produced by CitationParser.

class CitationVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CitationParser#citation.
    def visitCitation(self, ctx:CitationParser.CitationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#bookCitation.
    def visitBookCitation(self, ctx:CitationParser.BookCitationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#apaBook.
    def visitApaBook(self, ctx:CitationParser.ApaBookContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#ieeeBook.
    def visitIeeeBook(self, ctx:CitationParser.IeeeBookContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#gbtBook.
    def visitGbtBook(self, ctx:CitationParser.GbtBookContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#journalCitation.
    def visitJournalCitation(self, ctx:CitationParser.JournalCitationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#apaJournal.
    def visitApaJournal(self, ctx:CitationParser.ApaJournalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#ieeeJournal.
    def visitIeeeJournal(self, ctx:CitationParser.IeeeJournalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#gbtJournal.
    def visitGbtJournal(self, ctx:CitationParser.GbtJournalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#conferenceCitation.
    def visitConferenceCitation(self, ctx:CitationParser.ConferenceCitationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#apaConference.
    def visitApaConference(self, ctx:CitationParser.ApaConferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#ieeeConference.
    def visitIeeeConference(self, ctx:CitationParser.IeeeConferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#gbtConference.
    def visitGbtConference(self, ctx:CitationParser.GbtConferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#webCitation.
    def visitWebCitation(self, ctx:CitationParser.WebCitationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#apaWeb.
    def visitApaWeb(self, ctx:CitationParser.ApaWebContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#ieeeWeb.
    def visitIeeeWeb(self, ctx:CitationParser.IeeeWebContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#gbtWeb.
    def visitGbtWeb(self, ctx:CitationParser.GbtWebContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#apaAuthors.
    def visitApaAuthors(self, ctx:CitationParser.ApaAuthorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#apaAuthor.
    def visitApaAuthor(self, ctx:CitationParser.ApaAuthorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#ieeeAuthors.
    def visitIeeeAuthors(self, ctx:CitationParser.IeeeAuthorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#ieeeAuthor.
    def visitIeeeAuthor(self, ctx:CitationParser.IeeeAuthorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#gbtAuthors.
    def visitGbtAuthors(self, ctx:CitationParser.GbtAuthorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#gbtAuthor.
    def visitGbtAuthor(self, ctx:CitationParser.GbtAuthorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#chineseName.
    def visitChineseName(self, ctx:CitationParser.ChineseNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#englishNameIeee.
    def visitEnglishNameIeee(self, ctx:CitationParser.EnglishNameIeeeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#englishNameApa.
    def visitEnglishNameApa(self, ctx:CitationParser.EnglishNameApaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#firstName.
    def visitFirstName(self, ctx:CitationParser.FirstNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#lastName.
    def visitLastName(self, ctx:CitationParser.LastNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#volume.
    def visitVolume(self, ctx:CitationParser.VolumeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#issue.
    def visitIssue(self, ctx:CitationParser.IssueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#pages.
    def visitPages(self, ctx:CitationParser.PagesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#url.
    def visitUrl(self, ctx:CitationParser.UrlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#venue.
    def visitVenue(self, ctx:CitationParser.VenueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#place.
    def visitPlace(self, ctx:CitationParser.PlaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#title.
    def visitTitle(self, ctx:CitationParser.TitleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#publisher.
    def visitPublisher(self, ctx:CitationParser.PublisherContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#string.
    def visitString(self, ctx:CitationParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#year.
    def visitYear(self, ctx:CitationParser.YearContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CitationParser#dates.
    def visitDates(self, ctx:CitationParser.DatesContext):
        return self.visitChildren(ctx)



del CitationParser