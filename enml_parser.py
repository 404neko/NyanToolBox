import lxml.html
from lxml import etree

permitted_elements = ['a', 'abbr', 'acronym', 'address',
    'area', 'b', 'bdo', 'big', 'blockquote', 'br', 'caption',
    'center', 'cite', 'code', 'col', 'colgroup', 'dd', 'del',
    'dfn', 'div', 'dl', 'dt', 'em', 'font', 'h1', 'h2', 'h3',
    'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'kbd', 'li',
    'map', 'ol', 'p', 'pre', 'q', 's', 'samp', 'small', 'span',
    'strike', 'strong', 'sub', 'sup', 'table', 'tbody', 'td',
    'tfoot', 'th', 'tfoot', 'th', 'thead', 'title', 'tr', 'tt',
    'u', 'var', 'xmp'
]

permitted_attrs = ['href', 'src']

def load(content):
    parser = lxml.html.HTMLParser(encoding='UTF-8')
    return lxml.html.document_fromstring(content, parser=parser)

def parse(lxml_):
    if not lxml_.tag in permitted_elements:
        lxml_.tag = 'div'

    for elem in lxml_.xpath('//*'):
        if not etree.iselement(elem):
            elem.drop_tree()
        elif not elem.tag in permitted_elements:
            elem.drop_tag()
        elif elem.tag == 'a' and 'href' in elem.attrib and elem.attrib['href'].startswith('javascript:'):
            elem.drop_tag()
        
        for key in elem.attrib:
            if not key in permitted_attrs:
                elem.attrib.pop(key)

    return etree.tostring(
        lxml_, method='xml',
        encoding='UTF-8', xml_declaration=None,
        pretty_print=False, with_tail=True,
        standalone=None
    )

def load_images(html):
    pass

def format(html):
    pass