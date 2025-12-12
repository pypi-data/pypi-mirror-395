<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:owl="http://www.w3.org/2002/07/owl#"
                xmlns:dct="http://purl.org/dc/terms/"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
>
    <xsl:template match="/">
        <html>
            <head>
                <style>
                    dl dt {
                    margin-top:2em;
                    margin-bottom:.5em;
                    }
                    dl dt .label {
                    font-weight:bold;
                    font-size:130%;
                    font-family:monospace;
                    color:#333;
                    }
                    span.attr {
                    display:inline-block;
                    border-radius:3px;
                    background:#ccc;
                    padding:.2em;
                    margin-right:.5em;
                    margin-bottom:.2em;
                    font-family:monospace;
                    text-transform:capitalize;
                    font-size:110%;
                    }
                    body {
                    max-width:900px;
                    margin:0 auto;
                    font-family:roboto,sans;
                    }
                    .anchor {
                    font-weight:bold;
                    font-size:120%;
                    }
                    a:link {
                    text-decoration:none;
                    color:#284185;
                    }
                    p.warning {
                    font-style:italic;
                    }
                    p.comment {
                    text-align:justify;
                    }
                </style>
            </head>
            <body>
                <h1>
                    <xsl:value-of select="rdf:RDF/owl:Ontology/dct:title"/>
                </h1>
                <h2>Paralex OWL ontology</h2>

                <p class="warning">Please see the <a href="https://www.paralex-standard.org/">documentation for
                    Paralex</a>.
                </p>

                <p class="warning">This HTML is meant to show a simple browser introduction to the ontology and has been
                    automatically created using XSLT. To see the
                    source OWL as RDF/XML, either use "Save As" or "View Source".
                </p>

                <p class="comment">
                    <xsl:apply-templates select="rdf:RDF/owl:Ontology/rdfs:comment"/>
                </p>

                <h3>Classes</h3>
                <dl>
                    <xsl:apply-templates select="//owl:Class"/>
                </dl>
                <h3>Object properties</h3>
                <dl>
                    <xsl:apply-templates select="//owl:ObjectProperty"/>
                </dl>


                <h3>Data type properties</h3>
                <dl>
                    <xsl:apply-templates select="//owl:DatatypeProperty"/>
                </dl>

            </body>
        </html>
    </xsl:template>
    <xsl:template match="//owl:ObjectProperty | //owl:DatatypeProperty | //owl:Class">
        <dt class="property" id="{substring-after(@rdf:about, '#')}">
            <span class="anchor">
                <a href="{@rdf:about}"># </a>
            </span>
            <span class="label">
                <xsl:choose>
                    <xsl:when test="rdfs:label">
                        <xsl:value-of select="rdfs:label"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:choose>
                            <xsl:when test="contains(@rdf:about,'#')">
                                <xsl:value-of select="substring-after(@rdf:about, '#')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:choose>
                                    <xsl:when test="contains(@rdf:about,'/gold/')">
                                        <xsl:value-of select="substring-after(@rdf:about, '/gold/')"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="@rdf:about"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:otherwise>
                </xsl:choose>
            </span>
            (
            <span class="ref">
                <a href="{@rdf:about}">
                    <code>
                        <xsl:value-of select="@rdf:about"/>
                    </code>
                </a>
            </span>
            )
            &#xa0;
        </dt>
        <dd>
            <xsl:apply-templates select="rdfs:range | rdfs:domain | rdfs:subPropertyOf | rdfs:subClassOf"/>
            <xsl:apply-templates select="rdfs:comment"/>
        </dd>
    </xsl:template>
    <xsl:template match="rdfs:range | rdfs:domain | rdfs:subPropertyOf  | rdfs:subClassOf">
        <span class="attr" ><xsl:value-of select="local-name(.)"/>:
        </span>
        <a href="{@rdf:resource}">
            <code>
                <xsl:value-of select="@rdf:resource"/>
            </code>
        </a>
        <br/>
    </xsl:template>
    <xsl:template match="rdfs:comment">
        <xsl:value-of select="."/>
        <br/>
    </xsl:template>
</xsl:stylesheet>

