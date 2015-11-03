@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix dcterms: <http://www.purl.org/dc/terms/>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix skos: <http://www.w3.org/2004/02/skos/core#>.

@prefix doco: <http://purl.org/spar/doco/>.
@prefix deo: <http://purl.org/spar/deo/>.
@prefix sro:
<http://salt.semanticauthoring.org/ontologies/sro#>.
@prefix bibo: <http://purl.org/ontology/bibo/>.
@prefix bibtex: <http://purl.org/net/nknouf/ns/bibtex#>.
@prefix pattern:
<http://www.essepuntato.it/2008/12/pattern#>.

@prefix pub:
<http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/>.
@prefix : <http://example.org/>.

# Triple-classing a pub:Publication instance, remember to
satisfy constraints on bibtex:Article!
:publication1 a pub:Publication, bibtex:Article,
bibo:Document;
    bibtex:hasTitle "..."; # this and the following triples
are asserted to satisfy constraints on bibtex:Article
    bibtex:hasYear "2015"^^xsd:nonNegativeInteger;
    bibtex:hasJournal "...";
    bibtex:hasAuthor "...".

# Double-classing a pub:Chapter instance.
:chapter4 a pub:Chapter, doco:Chapter;
    rdfs:label "Chapter 4";
    pub:caption "Energy Supply and Use";
    pub:inPublication :publication2; # this chapter is in a
publication
    pub:hasSection :section1; # it has a section in it
    pub:hasFigure :figure1; # it has a figure in it
    pub:hasTable :table1; # it has a table in it
    pattern:contains :paragraph1. # use a property in DoCO
to reach down to the paragraph level

# Double-classing a pub:Section instance.
:section1 a pub:Section, doco:Section;
    rdfs:label "Section 4.1";
    pub:caption "Disruptions from Extreme Weather";
    pub:inPublication :publication1; # this section is in a
publication
    pub:inChapter :chapter4; # this section is in a chapter
    pub:hasSection :section1_1; # it has a subsection
    pub:hasFigure :figure1; # it has a figure in it
    pub:hasTable :table1; # it has a table in it
    pattern:contains :paragraph1. # use a property in DoCO
to reach down to the paragraph level

# Figure
:figure1 a pub:Figure; # Benefit of double-classing with
doco:Figure is unclear, so no double-classing here.
    rdfs:label "Figure 4.1";
    pub:caption "Paths of Hurricanes Katrina and Rita
Relative to Oil and Gas Production Facilities";
    pub:inSection :section1; # the figure is in a section
    pub:inChapter :chapter4; # the figure is in a chapter
    pub:inPublication :publication1. # the figure is in a
publication

# Table
:table1 a pub:Table; # No double-classing with doco:Table
here because the benefit is unclear.
    rdfs:label "Table 4.1";
    pub:caption "Changing Energy Use for Heating and
Cooling Will Vary by Region";
    pub:inSection :section1; # the table is in a section
    pub:inChapter :chapter4; # it is in a chapter
    pub:inPublication :publication1. # it is in a
publication

# Result in the form of a list
:list1 a pub:List;
    rdfs:label "The list at the beginning of Chapter 4"; #
give location information to help identify the list
    pub:inChapter :chapter4; # the list is in a chapter
    pub:inPublication :publication1. # it is in a
publication

# Textually described result
:text1 a pub:Text;
    rdfs:label "The sentence in the last paragraph of page
115 saying that coal produced 42% of U.S. electricity in
2011";
    pub:inSection :section1; # the text is found in a
section
    pub:inChapter :chapter4; # it is in a chapter
    pub:inPublication :publication1. # it is in a
publication

