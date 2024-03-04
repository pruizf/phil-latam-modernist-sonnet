<?xml version="1.0" encoding="UTF-8"?>
<!-- Author: Helena Bermúdez Sabel -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs"
    version="3.0">
    <xsl:output method="text"/>
    <xsl:param name="dir" select="'per-sonnet/'"/>
    <xsl:template match="/">
        <!-- 
           Example of command java -jar ../../../../saxon.jar -s:18th/per-sonnet -o:../test/18th/per-sonnet -xsl:../../xslt/tei2txt_per-sonnet.xsl-->
        
        <xsl:variable name="fileName" select="document-uri(current()) => substring-after($dir) => substring-before('xml')"/>
        <xsl:result-document href="{$fileName}txt">
            <xsl:apply-templates select="descendant::lg[@type eq 'sonnet']/lg"/>
        </xsl:result-document>
    </xsl:template>
    <xsl:template match="lg">
        <xsl:apply-templates select="l"></xsl:apply-templates>
<xsl:text>
</xsl:text>
    </xsl:template>
<xsl:template match="l">
    <xsl:value-of select="current() => normalize-space()"/>
<xsl:text>
</xsl:text>
</xsl:template>
</xsl:stylesheet>