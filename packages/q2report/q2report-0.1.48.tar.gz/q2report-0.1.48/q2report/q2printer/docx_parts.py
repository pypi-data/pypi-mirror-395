#    Copyright © 2021 Andrei Puchko
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

docx_parts = {}
docx_parts[
    "doc_start"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document
    xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    xmlns:w10="urn:schemas-microsoft-com:office:word"
    xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    xmlns:v="urn:schemas-microsoft-com:vml"
    xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:o="urn:schemas-microsoft-com:office:office"
    xmlns:ve="http://schemas.openxmlformats.org/markup-compatibility/2006">
<w:body>

"""

docx_parts[
    "image"
] = """
    <w:r>
    <w:drawing>
        <wp:inline distT="0" distB="0" distL="0" distR="0">
            <wp:extent cx="%(width)s" cy="%(height)s"/>
            <wp:effectExtent l="0" t="0" r="0" b="0"/>
            <wp:docPr id="%(imageIndex)s" name="image%(imageIndex)s"/>
            <wp:cNvGraphicFramePr>
                <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                    noChangeAspect="1"/>
            </wp:cNvGraphicFramePr>
            <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                    <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
                        <pic:nvPicPr>
                        <pic:cNvPr id="%(imageIndex)s"
                                name="image%(imageIndex)s.png"/>
                        <pic:cNvPicPr/>
                    </pic:nvPicPr>                    
                        <pic:blipFill>
                            <a:blip r:embed="rId%(imageIndex)s">
                                </a:blip>
                            <a:stretch>
                                <a:fillRect/>
                            </a:stretch>
                        </pic:blipFill>
                        <pic:spPr bwMode="auto">
                            <a:xfrm>
                                <a:off
                                    x="0"
                                    y="0"/>
                                <a:ext
                                    cx="%(width)s"
                                    cy="%(height)s"/>
                            </a:xfrm>
                            <a:prstGeom prst="rect">
                                <a:avLst/>
                            </a:prstGeom>
                        </pic:spPr>
                    </pic:pic>
                </a:graphicData>
            </a:graphic>
        </wp:inline>
    </w:drawing>
    </w:r>
    """

docx_parts[
    "rels"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1"
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
        Target="word/document.xml"/>
    </Relationships>"""
docx_parts[
    "content_type"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="jpg" ContentType="image/jpg"/>
    <Default Extension="png" ContentType="image/png"/>
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Override PartName="/word/document.xml"
        ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    %s
    </Types>"""
docx_parts["headers_footers_content_type"] = """
            <Override PartName="/word/%s%s.xml"
                ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.%s+xml"/>
"""
docx_parts[
    "word_rels"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    %s
    </Relationships>"""
docx_parts[
    "images"
] = """<Relationship Id="rId%s"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    Target="media/image%s.png"/>"""

docx_parts[
    "headers"
] = """	<Relationship Id="rId%s"
                Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header"
                Target="header%s.xml"/>
"""

docx_parts[
    "footers"
] = """	<Relationship Id="rId%s"
                Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
                Target="footer%s.xml"/>
"""

docx_parts[
    "header"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <w:hdr xmlns:o="urn:schemas-microsoft-com:office:office"
                    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                    xmlns:v="urn:schemas-microsoft-com:vml"
                    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                    xmlns:w10="urn:schemas-microsoft-com:office:word"
                    xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                    xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
                    xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
                    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                    xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
                    xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
                    xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
                    mc:Ignorable="w14 wp14 w15">
                    %s
                </w:hdr>
                    """

docx_parts[
    "footer"
] = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <w:ftr xmlns:o="urn:schemas-microsoft-com:office:office"
                    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                    xmlns:v="urn:schemas-microsoft-com:vml"
                    xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                    xmlns:w10="urn:schemas-microsoft-com:office:word"
                    xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
                    xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
                    xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
                    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                    xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
                    xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
                    xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
                    mc:Ignorable="w14 wp14 w15">
                    %s
                </w:ftr>
                    """
