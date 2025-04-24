<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0" xpath-default-namespace="http://www.tei-c.org/ns/1.0">
    
    <xsl:output method="text" encoding="UTF-8"/>
    
    <xsl:template match="teiHeader"/>
    <xsl:template match="sourceDoc"/>
    <xsl:template match="fw"/>
    <xsl:template match="lb">
        <xsl:text>&#10;</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>