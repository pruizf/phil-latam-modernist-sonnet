header_prosopography = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="../schema/constrictions-prosopography.sch" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
   <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Prosopografía</title>
            <respStmt>
               <resp>Recolección de datos y codificación</resp>
               <name xml:id="prf">Pablo Ruiz Fabo</name>
               <name xml:id="heb">Helena Bermúdez Sabel</name>
               <name xml:id="cimc">Clara Isabel Martínez Cantón</name>
               <name xml:id="jct">José Calvo Tello</name>
            </respStmt>
         </titleStmt>
         <publicationStmt>
            <publisher>Diachronic Spanish Sonnet Corpus</publisher>
            <availability>
               <licence>
                  <ref target="http://creativecommons.org/licenses/by/4.0/">Creative Commons
                     Attribution 4.0 International</ref>
               </licence>
            </availability>
         </publicationStmt>
         <sourceDesc>
            <p>Born digital</p>
         </sourceDesc>
         <encodingDesc>
            <listPrefixDef>
               <prefixDef ident="foaf" matchPattern="([A-Za-z]+)"
                  replacementPattern="http://xmlns.com/foaf/0.1/$1"/>
               <prefixDef ident="dc" matchPattern="([A-Za-z]+)"
                  replacementPattern="http://purl.org/dc/terms/$1"/>
               <prefixDef ident="schema" matchPattern="([A-Za-z]+)"
                  replacementPattern="http://schema.org/$1"/>
               <prefixDef ident="rdfs" matchPattern="([A-Za-z]+)"
                  replacementPattern="http://www.w3.org/2000/01/rdf-schema#$1"/>
            </listPrefixDef>
         </encodingDesc>
      </fileDesc>
   </teiHeader>
   <text>
      <body>
         <listPerson>
             """

prosopography_end_tags = """
         </listPerson>
      </body>
   </text>
</TEI>
"""