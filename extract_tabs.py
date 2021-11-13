import re


TAGS_RE = re.compile(r"<(?P<tag>\w+)(?P<attributes>[^>]*?)/?>")
ATTRIBUTE_RE = re.compile(r"""
                          (?P<attribute>[-\w]+)=
                          (?P<quote>(?P<single>')|(?P<duble>"))?
                          (?P<value>(?(single)[^'])+?|(?(duble)[^"])+?|\S+?)
                          (?(quote)(?P=quote))
                          """, re.X)


def main():
    filename = input("Enter filename: ")
    try:
        with open(filename, 'r', encoding='utf8') as fh:
            xml_text = fh.read()
            for tag, attributes in TAGS_RE.findall(xml_text):
                print(tag)
                for attribute, q, s, d, value in ATTRIBUTE_RE.findall(attributes):
                    print(f'    {attribute} = {value}')
    except EnvironmentError as err:
        print(err)

main()
