import xml.etree.ElementTree as ET
import zipfile

class Mnemosyne2Cards(object):
    @staticmethod
    def read(raw_file):
        with zipfile.ZipFile(raw_file, "r") as zip_file:
            # Extract cards XML file
            cards_file = zip_file.open("cards.xml")

            # Parse XML
            cards = ET.parse(cards_file).getroot()
            return ((log.find('b').text, log.find('f').text)
                    for log in cards.findall('log')
                    if str(log.get('type')) == '16')
