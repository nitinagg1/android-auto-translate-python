import xml
import os
import copy
import logging
import xml.etree.ElementTree as ET
from google_translate_api import translate_strings
from io import BytesIO
import argparse
import constants


parser = argparse.ArgumentParser(description='generates strings translations for android applications using google translate APIs')
parser.add_argument('--source',
                    help='path to the source strings.xml file , for example PATH_TO_RES_FOLDER/values/strings.xml')
parser.add_argument('--lang',
                    help='accepts comma separated list of langs codes to generate automatic translations')

source_file = None

lang_list = []

def parse_xml_document():
    logging.info("parse_xml_document start")
    tree = ET.parse(source_file)

    root = tree.getroot()
    child_list = root._children

    required_translations = dict()

    for child in child_list:
        key = child.attrib['name']
        value = child.text
        required_translations[key] = value

    translated_strings_dict_copy = copy.deepcopy(required_translations)

    required_translations_list = []

    for key, value in required_translations.iteritems():
        required_translations_list.append(value)

    for lang_code in lang_list:
        translated_strings = translate_strings(required_translations_list, lang_code)

        counter = 0
        for key, value in translated_strings_dict_copy.iteritems():
            translated_strings_dict_copy[key] = translated_strings['translations'][counter]['translatedText']
            counter += 1

        print 'the translated strings are'
        create_xml_from_dict(translated_strings_dict_copy, lang_code)


def create_xml_from_dict(translated_string_dict, lang_code):
    logging.info('create_xml_from_dict start')
    root = ET.Element("resources")
    root.set('xmlns:tools','http://schemas.android.com/tools')
    root.tail = "\n"
    for key, value in translated_string_dict.iteritems():
        f = ET.SubElement(root, "string", name=key).text = value
    tree = ET.ElementTree(root)

    dst_string_file = '{}/values-{}'.format(os.path.dirname(os.path.dirname(source_file)), lang_code)
    if not os.path.exists(dst_string_file):
        os.makedirs(dst_string_file)
    file_path = '{}/strings.xml'.format(dst_string_file)
    tree.write(file_path, encoding='utf8', method='xml')

if __name__ == '__main__':
    args = parser.parse_args()
    if not (args.source and\
                args.lang):
        raise AttributeError('No source file or lang list specified, do --help to check arguments.')

    source_file = args.source
    lang_list = args.lang.split(',')
    if not os.path.isfile(source_file):
        raise AttributeError('source file specified is incorrect')

    for lang_code in lang_list:
        if lang_code not in constants.SUPPORTED_LANG_CODES:
            raise AttributeError('lang code provided not supported, check ISO-639-1 Code, #lang code is case sensitive')

    parse_xml_document()
