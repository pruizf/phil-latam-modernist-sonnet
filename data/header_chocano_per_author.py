header_chocano_pa = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://raw.githubusercontent.com/pruizf/disco/master/schema/tei_all_DISCO.rnc" type="application/relax-ng-compact-syntax"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
   <teiHeader>
      <fileDesc>
         <titleStmt about="disco:au_592n">
            <title property="dc:title">Sonetos de José Santos Chocano</title>
            <author property="dc:creator" resource="disco:592n" corresp="#disco_592n">
              José Santos Chocano</author>
            <principal xml:id="prf">Pablo Ruiz Fabo</principal>
            <principal xml:id="heb">Helena Bermúdez Sabel</principal>
            <principal xml:id="cimc">Clara Isabel Martínez Cantón</principal>
            <respStmt>
               <resp>Metrical annotation done with <ref target="https://github.com/linhd-postdata/rantanplan">Rantanplan</ref>, developed by</resp>
               <name>Javier de la Rosa et al.</name>
            </respStmt>
            <respStmt>
               <resp>Rhyme annotation done with <ref
                     target="https://github.com/versotym/rhymeTagger">RhymeTagger</ref>, developed
                  by</resp>
               <name xml:id="pp">Petr Plecháč</name>
            </respStmt>
         </titleStmt>
         <extent>
            <measure unit="sonnets">{nbr_of_sonnets}</measure>
            <measure unit="tokens">{nbr_of_tokens}</measure>
            <measure unit="line">{nbr_of_lines}</measure>
         </extent>
         <publicationStmt>
            <publisher>Diachronic Spanish Sonnet Corpus</publisher>
            <availability status="free">
               <p>The text is freely available</p>
            </availability>
            <date when="2023">2023</date>
            <idno type="#disco" xml:id="file_au_592n"/>
         </publicationStmt>
         <sourceDesc>
           <listBibl>
            <bibl xml:id="antologia" type="digital-source">Biblioteca Cervantes Virtual, <hi rend="italics">Sonetos del
                  siglo XIX</hi> / editados por Ramón García González, <date when="2006"
               >2006</date>, <ref target="http://www.cervantesvirtual.com/nd/ark:/59851/bmc4q861"/>,
                  <ref target="http://www.cervantesvirtual.com/obra/sonetos-del-siglo-xix--0/"
               />.</bibl>
            <bibl xml:id="completas-I" type="digital-source">Alicante: Biblioteca Virtual Miguel de Cervantes
              <hi rend="italics">Poesías completas. Tomo Primero: Iras santas; En la aldea;
              Azahares; Selva virgen; Poemas / José Santos Chocano (formato PDF)</hi>,
              <date>2015</date>, <ref 
              target="https://www.cervantesvirtual.com/nd/ark:/59851/bmcpg3m2"/>.
            </bibl>
            <bibl xml:id="completas-II" type="digital-source">Alicante: Biblioteca Virtual Miguel de Cervantes
              <hi rend="italics">Poesías completas. Tomo Segundo: Iras santas; En la aldea;
              Azahares; Selva virgen; Poemas / José Santos Chocano (formato PDF)</hi>,
              <date>2015</date>, <ref 
              target="https://www.cervantesvirtual.com/nd/ark:/59851/bmcjq2w2"/>.
            </bibl>
           </listBibl>
         </sourceDesc>
      </fileDesc>
      <profileDesc>
         <langUsage>
            <language ident="es" about="disco:au_592n" property="dc:language"
               resource="dbpedia:Idioma_español">Spanish</language>
         </langUsage>
         <particDesc>
            <listPerson>
               <person xml:id="disco_592n" about="disco:592n" typeOf="foaf:Person">
                  <idno cert="high" property="rdfs:seeAlso"
                     resource="https://viaf.org/viaf/71504072"/>
                  <persName type="short">Chocano</persName>
                  <persName type="full">
                     <forename property="foaf:givenName">José Santos</forename>
                     <surname property="foaf:familyName">Chocano</surname>
                  </persName>
                  <persName type="source" property="foaf:name">José Santos Chocano</persName>
                  <sex property="foaf:gender" content="M"/>
                  <birth>
                     <location>
                        <placeName>
                           <settlement property="schema:birthPlace" inlist="">Lima</settlement>
                           <country property="schema:birthPlace" inlist="">Perú</country>
                           <bloc property="schema:birthPlace" inlist="">America</bloc>
                        </placeName>
                     </location>
                     <date type="century">19</date>
                  </birth>
                  <death>
                     <location>
                        <placeName>
                           <settlement property="schema:birthPlace" inlist="">Santiago</settlement>
                           <country property="schema:birthPlace" inlist="">Chile</country>
                           <bloc property="schema:birthPlace" inlist="">America</bloc>
                        </placeName>
                     </location>
                     <date type="century">20</date>
                  </death>
                  <listBibl inlist="" rel="blterms:hasCreated" typeOf="schema:CreativeWork">{list_bibl}
                  </listBibl>
               </person>
            </listPerson>
         </particDesc>
      </profileDesc>
      <encodingDesc>
         <listPrefixDef>
            <prefixDef ident="foaf" matchPattern="([A-Za-z]+)"
               replacementPattern="http://xmlns.com/foaf/0.1/$1"/>
            <prefixDef ident="dc" matchPattern="([A-Za-z]+)"
               replacementPattern="http://purl.org/dc/terms/$1"/>
            <prefixDef ident="schema" matchPattern="([A-Za-z]+)"
               replacementPattern="http://schema.org/$1"/>
            <prefixDef ident="dbpedia" matchPattern="([A-Za-z]+(_[A-Za-z])*)"
               replacementPattern="http://es.dbpedia.org/page/"/>
            <prefixDef ident="blterms" matchPattern="([A-Za-z]+)"
               replacementPattern="http://www.bl.uk/schemas/bibliographic/blterms#$1"/>
            <prefixDef ident="rdfs" matchPattern="([A-Za-z]+)"
               replacementPattern="http://www.w3.org/2000/01/rdf-schema#$1"/>
         </listPrefixDef>
         <metDecl type="met" pattern="((\+|\-)+)*">
            <metSym value="+">stressed syllable</metSym>
            <metSym value="-">unstressed syllable</metSym>
         </metDecl>
         <metDecl type="met">
            <p>The metrical patterns were extracted automatically using the <ref
                  target="https://github.com/bncolorado/adsoScansionSystem">ADSO</ref> tool.</p>
         </metDecl>
         <metDecl type="enjamb">
            <p>The values of the <att>enjamb</att> atributes were extracted automatically using the
                  <ref target="https://sites.google.com/site/spanishenjambment/">ANJA (Automatic
                  eNJambment Analysis)</ref> tool. For more information about the types of
               enjambment as defined in this corpus, read the <ref
                  target="https://sites.google.com/site/spanishenjambment/enjambment-types"
                  >documentation</ref>. In addition, a <att>cert</att> was added to express the
               degree of certainty concerning the characterisation of the enjambment. The following
                  <ref target="https://sites.google.com/site/spanishenjambment/tei-certitude-values"
                  >report</ref> covers this feature in deep detail.</p>
         </metDecl>
      </encodingDesc>
      <revisionDesc>
         <change when="2017-11-02" who="#prf">Initial TEI version </change>
         <change when="2017-11-27" who="#prf">Addition of metrical annotation</change>
         <change when="2017-11-27" who="#heb">Review of authors’ metadata</change>
         <change when="2017-12-01" who="#prf">Encoding of enjambment</change>
         <change when="2017-12-01" who="#heb">Publication of 19th, 18th and Golden Age
            version</change>
         <change when="2018-05-16" who="#heb">Revision of RDFa attributes</change>
         <change when="2019-03-14" who="#heb">Added rhyme schemes aided by <name corresp="#pp"
               >Plecháč</name></change>
         <change when="2019-03-16" who="#cimc #heb">Rhyme review and additional analyses</change>
         <change when="2021-12-12" who="#prf #heb">New release</change>
         <change when="2023-01-20" who="#prf">Adds sonnets from
           <bibl corresp="#completas-I #completas-II">Poesías completas</bibl>
         </change>
         <change when="2023-01-20" who="#prf">Metrics for sonnets in earlier source
         (<bibl corresp="#antologia">García González, 2006</bibl>) reannotated with Rantanplan</change>
      </revisionDesc>
   </teiHeader>
   <text>
      <front>
         <div>
            <head>José Santos Chocano</head>
            <p>Lima (Perú). 1875 - 1934</p>
         </div>
      </front>
   """
