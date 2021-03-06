@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix dcterms: <http://www.purl.org/dc/terms/>.
@prefix skos: <http://www.w3.org/2004/02/skos/core#>.
@prefix prov: <http://www.w3.org/ns/prov#>.

@prefix pub:
<http://orion.tw.rpi.edu/~fulinyun/ontology/prov-pub/>.
@prefix : <http://example.org/>.

# In-memory data description
:csv_content a pub:InMemoryData;
    dcterms:description "Data held by the csv_content
variable.".

# On-disk data description
:csv_file a pub:OnDiskData;
    pub:format "CSV";
    dcterms:description "Data in the data.csv file.".
    
# Library description
:pandas a pub:Library;
        dcterms:description "The pandas Python library.".
    
# Published result description
:figure4_2 a pub:Figure;
    rdfs:label "Figure 4.2";
    pub:caption "Increase in Cooling Demand and Decrease in
Heating Demand";
    pub:inSection :section1.

# A physical change of data --- download
:download_data a pub:PhysicalChange;
    pub:language "Bash";
    pub:code "wget
http://www1.ncdc.noaa.gov/pub/orders/CDODiv2177686828992.tx
t";
    dcterms:description "Downloaded a CSV file from a
NOAA/NCDC download link with the wget utility.";
    prov:used :wget;
    prov:generated :csv_file_1.
:wget a pub:Library;
    dcterms:description "The wget utility.".
:csv_file_1 a pub:OnDiskData;
    pub:format "CSV";
    dcterms:description "Data in the
CDODiv2177686828992.txt file.".

# A syntactical change of data --- format conversion
:convert_data a pub:SyntacticalChange;
    dcterms:description "Used the online converter at
http://www.easyrdf.org/converter with the \"Raw output\"
option clicked.";
    prov:used :converter;
    prov:used :xml_data;
    prov:generated :ttl_data.
:converter a pub:Library;
    dcterms:description "The easyrdf online converter.".
:xml_data a pub:OnDiskData;
    pub:format "RDF/XML";
    dcterms:description "The bibtex ontology in RDF/XML.".
:ttl_data a pub:OnDiskData;
    pub:format "Turtle";
    dcterms:description "The bibtex ontology in Turtle.".

# A semantical change of data --- transformation for
plotting
:transform_data a pub:SemanticalChange;
    dcterms:description "Used Python scripts to transform
data held by the variable csv_content into data held by
variable percent for matplotlib.";
    pub:language "Python";
    pub:code """
    import pandas as pd
    dd_agg=dd.groupby(dd['YearMonth'] // 100).sum()
    dd_agg.index.name=u'Year'
    cdd_avg, hdd_avg = sum(dd_agg['CDD'][0:31])/31,
sum(dd_agg['HDD'][0:31])/31
    to_percent = lambda x, y: (x-y)/y*100
    cdd_percent, hdd_percent = to_percent(dd_agg['CDD'][:],
cdd_avg), to_percent(dd_agg['HDD'][:], hdd_avg)
    percent = pd.concat([hdd_percent, cdd_percent], axis=1)
    """;
    prov:used :pandas;
    pub:transformed :csv_content;
    prov:generated :percent.
:percent a pub:InMemoryData;
    dcterms:description "Data held by the \"percent\"
variable.".

# Data obtaining
:obtain_data a pub:Obtaining;
    dcterms:description "Filled out the data request form
at http://www7.ncdc.noaa.gov/CDO/CDODivisionalSelect.jsp#
with period: 1970.1--2010.12, and downloaded the requested
data.";
    prov:generated :csv_file_1.

# Data loading
:load_data a pub:Loading;
    dcterms:description "Loaded data from the data.csv file
to the csv_content variable.";
    pub:language "Python";
    pub:code """
    import pandas as pd
    csv_content = pd.read_csv("data.csv", delimiter=' ',
skipinitialspace=True)        
    """;
    pub:loaded :csv_file;
    prov:used :pandas;
    pub:generated :csv_content.

# Data saving
:save_data a pub:Saving;
    dcterms:description "Saved data held by the csv_content
varialbe to the data.csv file.";
    pub:language "R";
    pub:code "write.csv(csv_content, \"data1.csv\")";
    pub:saved :csv_content;
    prov:generated :csv_file_2.
:csv_file_2 a pub:OnDiskData;
    pub:format "CSV";
    dcterms:description "Data in the data1.csv file.".

# Data transformation
:transform_data_1 a pub:Transformation;
    dcterms:description "Used Python scripts to transform
data held by the variable csv_content into data held by
variable percent for matplotlib.";
    pub:language "Python";
    pub:code """
    import pandas as pd
    dd_agg=dd.groupby(dd['YearMonth'] // 100).sum()
    dd_agg.index.name=u'Year'
    cdd_avg, hdd_avg = sum(dd_agg['CDD'][0:31])/31,
sum(dd_agg['HDD'][0:31])/31
    to_percent = lambda x, y: (x-y)/y*100
    cdd_percent, hdd_percent = to_percent(dd_agg['CDD'][:],
cdd_avg), to_percent(dd_agg['HDD'][:], hdd_avg)
    percent = pd.concat([hdd_percent, cdd_percent], axis=1)
    """;
    prov:used :pandas;
    pub:transformed :csv_content;
    prov:generated :percent.

# Data visualization
:plot_data a pub:Visualization;
    dcterms:description "Plotted data held by the percent
variable with matplotlib to generate Figure 4.2.";
    pub:language "Python";
    pub:code """
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    percent.plot(kind='bar', figsize=(20,10))
    """;
    pub:visualized :percent;
    prov:used :matplotlib;
    prov:generated :figure4_2.
:matplotlib a pub:Library;
    dcterms:description "The matplotlib Python library.".

# Data analysis
:analyze_data a pub:Analysis;
    dcterms:description "Analyzed data about U.S.
electricity generation in 2011";
    pub:analyzed :us_electricity_data_2011;
    prov:generated :text.
:us_electricity_data_2011 a pub:Data.
:text a pub:Text;
    rdfs:label "The sentence in the last paragraph of page
115 saying that coal produced 42% of U.S. electricity in
2011";
    pub:inSection :section1.

# Result reuse
:reuse_figure a pub:Reuse;
    dcterms:description "Reused Figure 19 in the
osti-1026811 report as Figure 4.5.";
    pub:reused :figure19;
    prov:generated :figure4_5.
:figure19 a pub:Figure.
:figure4_5 a pub:Figure;
    rdfs:label "Figure 4.5";
    pub:caption "California Power Plants Potentially at
Risk from Sea Level Rise";
    pub:inSection :section1.
    
