<?xml version="1.0"?>

<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html"/>

  <xsl:template match="/">
    <html>
      <head>
        <style>
          * {
            font-family: sans-serif;
          }

          .item {
            margin-bottom: 20px;
          }
        </style>
      </head>
      <body>
        <h1>
          <xsl:value-of select="//channel/title"/>
        </h1>
        <p>
          <xsl:value-of select="//channel/description"/>
        </p>
        <div>
          <xsl:apply-templates select="//item"/>
        </div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="item">
    <div class="item">
      <xsl:element name="a">
        <xsl:attribute name="href">
          <xsl:value-of select="enclosure/@url"/>
        </xsl:attribute>
        <xsl:value-of select="title"/>
      </xsl:element>
    </div>
  </xsl:template>

</xsl:stylesheet>

