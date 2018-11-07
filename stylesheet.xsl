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

          video {
            display: block;
            max-width: 100%;
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

  <xsl:attribute-set name="media-params">
    <xsl:attribute name="src">  
      <xsl:value-of select="enclosure/@url"/>
    </xsl:attribute>
    <xsl:attribute name="controls"/>
  </xsl:attribute-set>

  <xsl:template match="item">
    <div class="item">
      <xsl:element name="a">
        <xsl:attribute name="href">
          <xsl:value-of select="enclosure/@url"/>
        </xsl:attribute>
        <xsl:value-of select="title"/>
      </xsl:element>
      <xsl:if test="enclosure[contains(@url, 'mp4')]">
        <xsl:element name="video" use-attribute-sets="media-params">
        </xsl:element>
      </xsl:if>
    </div>
  </xsl:template>

</xsl:stylesheet>

