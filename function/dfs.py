from xml.parsers.expat import ParserCreate

time=[]

class DefaultSaxHandler(object):

    def start_element(self, name, attrs):
        global time
        time.append(attrs)
        print('sax:start_element: %s, attrs: %s' % (name, str(attrs)))

    def end_element(self, name):
        print('sax:end_element: %s' % name)

    def char_data(self, text):
        print('sax:char_data: %s' % text)

xml = r'''<?xml version="1.0"?>
<ol>
<d p="6.2030000686646,1,25,0,1498230761,0,42942a9d,3485082149">20秒</d>
<d p="0.67799997329712,1,25,0,1498230749,0,623c3508,3485082211">刚刚</d>
</ol>
'''

handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)
