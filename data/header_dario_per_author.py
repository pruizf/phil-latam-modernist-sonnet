header_dario_pa = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://raw.githubusercontent.com/pruizf/disco/master/schema/tei_all_DISCO.rnc" type="application/relax-ng-compact-syntax"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
   <teiHeader>
      <fileDesc>
         <titleStmt about="disco:au_694n">
            <title property="dc:title">Sonetos de Rubén Darío</title>
            <author property="dc:creator" resource="disco:694n" corresp="#disco_694n">
              Rubén Darío</author>
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
            <idno type="#disco" xml:id="file_au_694n"/>
         </publicationStmt>
         <sourceDesc><p>Transcripción de sonetos seleccionados a partir de
            <bibl type="print-source">Madrid: Visor
              <hi rend="italics">Rubén Darío Sonetos Completos ;
              edición de Ricardo Llopesa</hi>, <date>2010</date>, <ref 
              target="https://www.visor-libros.com/tienda/sonetos-completos.html"/>.</bibl>
            </p>  
         </sourceDesc>
      </fileDesc>
      <profileDesc>
         <langUsage>
            <language ident="es" about="disco:au_694n" property="dc:language"
               resource="dbpedia:Idioma_español">Spanish</language>
         </langUsage>
         <particDesc>
            <listPerson>
               <person xml:id="disco_694n" about="disco:694n" typeOf="foaf:Person">
                  <idno cert="high" property="rdfs:seeAlso"
                     resource="https://viaf.org/viaf/177755002"/>
                  <persName type="short">Darío</persName>
                  <persName type="full">
                     <forename property="foaf:givenName">Rubén</forename>
                     <surname property="foaf:familyName">Darío</surname>
                  </persName>
                  <persName type="source" property="foaf:name">Rubén Darío</persName>
                  <sex property="foaf:gender" content="M"/>
                  <birth>
                     <location>
                        <placeName>
                           <settlement property="schema:birthPlace" inlist="">Metapa</settlement>
                           <country property="schema:birthPlace" inlist="">Nicaragua</country>
                           <bloc property="schema:birthPlace" inlist="">America</bloc>
                        </placeName>
                     </location>
                     <date type="century">19</date>
                  </birth>
                  <death>
                     <location>
                        <placeName>
                           <settlement property="schema:birthPlace" inlist="">León</settlement>
                           <country property="schema:birthPlace" inlist="">Nicaragua</country>
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
         <change when="2023-01-20" who="#prf">Initial TEI version </change>
      </revisionDesc>
   </teiHeader>
   <text>
      <front>
         <div>
            <head>Rubén Darío</head>
            <p>Metapa (Nicaragua). 1867 - 1916</p>
         </div>
      </front>
   """