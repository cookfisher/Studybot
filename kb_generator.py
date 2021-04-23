from rdflib import URIRef, Literal, Namespace, Graph
from rdflib.namespace import XSD, RDF, RDFS
from pathlib import Path
from os import getcwd
import pandas as pd
from os import walk
import pdfplumber
import requests


g = Graph()

FC = Namespace('http://focu.io/schema#')
FCD = Namespace('http://focu.io/data#')
DBR = Namespace('http://dbpedia.org/resource/')
VIVO = Namespace('http://vivoweb.org/ontology/core#')
AIISO = Namespace('http://purl.org/vocab/aiiso/schema#')
TEACH = Namespace('http://linkedscience.org/teach/ns#')

g.bind('focu', FC)
g.bind('focudata', FCD)
g.bind('dbr', DBR)
g.bind('vivo', VIVO)
g.bind('aiiso', AIISO)
g.bind('teach', TEACH)


# Class and Property
lab = FC['Lab']
g.add((lab, RDF.type, RDFS.Class))
g.add((lab, RDFS['subClassOf'], TEACH['Lecture']))
g.add((lab, RDFS.label, Literal('Lab', lang='en')))
g.add((lab, RDFS.comment, Literal('Lab Class', lang='en')))

tut = FC['Tutorial']
g.add((tut, RDF.type, RDFS.Class))
g.add((tut, RDFS['subClassOf'], TEACH['Lecture']))
g.add((tut, RDFS.label, Literal('Tutorial', lang='en')))
g.add((tut, RDFS.comment, Literal('Tutorial Class', lang='en')))

topic = FC['Topic']
g.add((topic, RDF.type, RDFS.Class))
g.add((topic, RDFS.label, Literal('Topic', lang='en')))
g.add((topic, RDFS.comment, Literal('Topic Class', lang='en')))

slide = FC['Slide']
g.add((slide, RDF.type, RDFS.Class))
g.add((slide, RDFS.label, Literal('Slide', lang='en')))
g.add((slide, RDFS.comment, Literal('Slide', lang='en')))

worksheet = FC['Worksheet']
g.add((worksheet, RDF.type, RDFS.Class))
g.add((worksheet, RDFS.label, Literal('Worksheet', lang='en')))
g.add((worksheet, RDFS.comment, Literal('Worksheet', lang='en')))

reading = FC['Reading']
g.add((reading, RDF.type, RDFS.Class))
g.add((reading, RDFS.label, Literal('Reading', lang='en')))
g.add((reading, RDFS.comment, Literal('Reading', lang='en')))

course_outline = FC['CourseOutline']
g.add((course_outline, RDF.type, RDFS.Class))
g.add((course_outline, RDFS.label, Literal('Course Outline', lang='en')))
g.add((course_outline, RDFS.comment, Literal('Course Outline', lang='en')))

subj = FC['Subject']
g.add((subj, RDF.type, RDFS.Class))
g.add((subj, RDFS.label, Literal('Subject', lang='en')))
g.add((subj, RDFS.comment, Literal('Subject Class', lang='en')))

subject_pro = FC['subject']
g.add((subject_pro, RDF.type, RDF.Property))
g.add((subject_pro, RDFS.label, Literal('subject', lang='en')))
g.add((subject_pro, RDFS.comment, Literal('Course subject.', lang='en')))
g.add((subject_pro, RDFS.domain, TEACH['Course']))
g.add((subject_pro, RDFS.range, FC['Subject']))

outline = FC['outline']
g.add((outline, RDF.type, RDF.Property))
g.add((outline, RDFS.label, Literal('outline', lang='en')))
g.add((outline, RDFS.comment, Literal('Course outline.', lang='en')))
g.add((outline, RDFS.domain, TEACH['Course']))
g.add((outline, RDFS.range, FC['CourseOutline']))

content = FC['content']
g.add((content, RDF.type, RDF.Property))
g.add((content, RDFS.label, Literal('content', lang='en')))
g.add((content, RDFS.comment, Literal('Lab content or tutorial content.', lang='en')))
g.add((content, RDFS.domain, FC['Lab']))
g.add((content, RDFS.domain, FC['Tutorial']))
g.add((content, RDFS.range, FC['Slide']))
g.add((content, RDFS.range, FC['Worksheet']))
g.add((content, RDFS.range, FC['Reading']))
g.add((content, RDFS.range, VIVO['Video']))

labAssociat = FC['labAssociateWith']
g.add((labAssociat, RDF.type, RDF.Property))
g.add((labAssociat, RDFS.label, Literal('lab associated with a specific lecture', lang='en')))
g.add((labAssociat, RDFS.comment, Literal('lab associated with a specific lecture', lang='en')))
g.add((labAssociat, RDFS.domain, FC['Lab']))
g.add((labAssociat, RDFS.range, TEACH['Lecture']))

tutAssociat = FC['tutorialAssociateWith']
g.add((tutAssociat, RDF.type, RDF.Property))
g.add((tutAssociat, RDFS.label, Literal('tutorial associated with a specific lecture', lang='en')))
g.add((tutAssociat, RDFS.comment, Literal('tutorial associated with a specific lecture', lang='en')))
g.add((tutAssociat, RDFS.domain, FC['Tutorial']))
g.add((tutAssociat, RDFS.range, TEACH['Lecture']))

topicAssociat = FC['topicAssociateWith']
g.add((topicAssociat, RDF.type, RDF.Property))
g.add((topicAssociat, RDFS.label, Literal('topics', lang='en')))
g.add((topicAssociat, RDFS.comment, Literal('topics that are covered in a course or a lecture in a course.', lang='en')))
g.add((topicAssociat, RDFS.domain, FC['Topic']))
g.add((topicAssociat, RDFS.range, TEACH['Lecture']))
g.add((topicAssociat, RDFS.range, TEACH['Course']))
g.add((topicAssociat, RDFS.range, FC['Slide']))
g.add((topicAssociat, RDFS.range, FC['Worksheet']))
g.add((topicAssociat, RDFS.range, FC['Reading']))
g.add((topicAssociat, RDFS.range, FC['Lab']))
g.add((topicAssociat, RDFS.range, FC['Tutorial']))

offeredAt = FC['offeredAt']
g.add((offeredAt, RDF.type, RDF.Property))
g.add((offeredAt, RDFS.label, Literal('offered in', lang='en')))
g.add((offeredAt, RDFS.comment, Literal('a course is offered at a univeristy.', lang='en')))
g.add((offeredAt, RDFS.domain, TEACH['Course']))
g.add((offeredAt, RDFS.range, VIVO['University']))

offeredIn = FC['offeredIn']
g.add((offeredIn, RDF.type, RDF.Property))
g.add((offeredIn, RDFS.label, Literal('lecture in', lang='en')))
g.add((offeredIn, RDFS.comment, Literal('a lecture is in a course.', lang='en')))
g.add((offeredIn, RDFS.domain, TEACH['Lecture']))
g.add((offeredIn, RDFS.range, TEACH['Course']))


def add_topics(text, course_name, lec, slide):
    # print(text)
    spot_light_url = f'https://api.dbpedia-spotlight.org/en/annotate?text={text}'
    headers = {'accept': 'application/json'}
    if requests.get(url=spot_light_url, headers=headers).status_code == 200:
        response = requests.get(url=spot_light_url, headers=headers).json()
        response = response.get('Resources')
        if response is not None:
            for item in response:
                dbr_link = item['@URI']
                dbr_name = dbr_link[28:]
                # print(dbr_name)

                topic = FCD[dbr_name]
                g.add((topic, RDF.type, FC['Topic']))
                g.add((topic, RDFS.label, Literal(dbr_name, lang='en')))
                g.add((topic, AIISO['name'], Literal(dbr_name)))
                g.add((topic, FC['topicAssociateWith'], FCD[course_name]))
                if lec is not None:
                    g.add((topic, FC['topicAssociateWith'], lec))
                if slide is not None:
                    g.add((topic, FC['topicAssociateWith'], slide))
                g.add((topic, RDFS.seeAlso, DBR[dbr_name]))


def add_topics_file(file_name, course_name, lec, slide):
    print(file_name)
    pdf = pdfplumber.open(file_name)
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text = page.extract_text()
        add_topics(text, course_name, lec, slide)
    pdf.close()


def add_lecture_name_comp472(file_name):
    pdf = pdfplumber.open(file_name)
    page = pdf.pages[0]
    text = page.extract_text().strip()
    text = text.split('Russell')[0][26:].strip()
    text = text.split('\uf0a7')[0].strip()
    text = text.split('(')[0].strip()
    pdf.close()
    return text


def add_lectures(course_name):
    folder_name = '.\\' + course_name + '\Lectures'
    _, _, file_names = next(walk(folder_name))

    for i in range(len(file_names)):
        slide = URIRef(Path(getcwd() + folder_name[1:] + '\\' + file_names[i]).as_uri())
        g.add((slide, RDF.type, FC['Slide']))

        lec = FCD[course_name + '_lecture' + str(i + 1)]
        g.add((lec, RDF.type, TEACH['Lecture']))
        if course_name == 'COMP472':
            g.add((lec, AIISO['name'], Literal(add_lecture_name_comp472(getcwd() + folder_name[1:] + '\\' + file_names[i]))))
        # elif course_name == 'COMP474':
        #     g.add((lec, AIISO['name'], Literal(add_lecture_name_comp474(getcwd() + folder_name[1:] + '\\' + file_names[i]))))
        g.add((lec, AIISO['code'], Literal(str(i + 1), datatype=XSD['integer'])))
        g.add((lec, FC['content'], slide))
        g.add((lec, FC['offeredIn'], FCD[course_name]))

        add_topics_file(getcwd() + folder_name[1:] + '\\' + file_names[i], course_name, lec, slide)


def add_labs(course_name):
    folder_name = '.\\' + course_name + '\Labs'
    _, _, file_names = next(walk(folder_name))

    for i in range(len(file_names)):
        slide = URIRef(Path(getcwd() + folder_name[1:] + '\\' + file_names[i]).as_uri())
        g.add((slide, RDF.type, FC['Slide']))

        lab = FCD[course_name + '_lab' + str(i + 1)]
        g.add((lab, RDF.type, FC['Lab']))
        g.add((lab, AIISO['name'], Literal(course_name + '_lab' + str(i + 1))))
        g.add((lab, AIISO['code'], Literal(str(i + 1), datatype=XSD['integer'])))
        g.add((lab, FC['content'], slide))
        g.add((lab, FC['labAssociatedWith'], FCD[course_name + '_lecture' + str(i + 1)]))
        # g.add((lab2, RDFS.seeAlso, URIRef('https://rdflib.readthedocs.io/en/stable/index.html')))

        add_topics_file(getcwd() + folder_name[1:] + '\\' + file_names[i], course_name, lab, slide)


def add_worksheets(course_name):
    folder_name = '.\\' + course_name + '\Worksheets'
    _, _, file_names = next(walk(folder_name))

    for i in range(len(file_names)):
        worksheet = URIRef(Path(getcwd() + folder_name[1:] + '\\' + file_names[i]).as_uri())
        g.add((worksheet, RDF.type, FC['Worksheet']))

        lec = FCD[course_name + '_lecture' + str(i + 2)]
        g.add((lec, FC['content'], worksheet))

        add_topics_file(getcwd() + folder_name[1:] + '\\' + file_names[i], course_name, lec, worksheet)


def add_course_outline(course_name):
    folder_name = '.\\' + course_name + '\Course_Outline'
    _, _, file_names = next(walk(folder_name))

    for i in range(len(file_names)):
        outline = URIRef(Path(getcwd() + folder_name[1:] + '\\' + file_names[i]).as_uri())
        g.add((outline, RDF.type, FC['CourseOutline']))

        g.add((FCD[course_name], FC['outline'], outline))

        add_topics_file(getcwd() + folder_name[1:] + '\\' + file_names[i], course_name, None, None)


def add_readings(course_name):
    folder_name = '.\\' + course_name + '\Readings'
    _, _, file_names = next(walk(folder_name))

    for i in range(len(file_names)):
        reading = URIRef(Path(getcwd() + folder_name[1:] + '\\' + file_names[i]).as_uri())
        g.add((reading, RDF.type, FC['Reading']))
        lec = FCD[course_name + '_lecture' + str(int(file_names[i][3:5]))]
        g.add((lec, FC['content'], reading))

        add_topics_file(getcwd() + folder_name[1:] + '\\' + file_names[i], course_name, lec, reading)


def subject_generator(subject_name):
    subject = FCD[subject_name]
    g.add((subject, RDF.type, FC['Subject']))
    g.add((subject, AIISO['name'], Literal(subject_name)))


def course_generator(subject, catalog, long_title, units, description):
    class1 = FCD[subject + catalog]
    g.add((class1, RDF.type, TEACH['Course']))
    g.add((class1, TEACH['courseTitle'], Literal(long_title)))
    g.add((class1, VIVO['courseCredits'], Literal(units, datatype=XSD['decimal'])))
    g.add((class1, FC['subject'], FCD[subject]))
    g.add((class1, AIISO['code'], Literal(catalog, datatype=XSD['integer'])))
    g.add((class1, TEACH['courseDescription'], Literal(description)))
    # g.add((class1, RDFS.seeAlso, DBR['Concordia_University']))
    g.add((class1, FC['offeredAt'], FCD['Concordia_University']))
    # g.add((class1, FC['outline'], Literal('utline.....Intelligent Systems')))


table1 = pd.read_csv("CU_SR_OPEN_DATA_CATALOG_DESC.csv", header=0)
table2 = pd.read_csv("CU_SR_OPEN_DATA_CATALOG-37272173.csv", header=0)

table_merged = pd.merge(table1, table2, on='Course ID', how='inner')

subjects = []
course_ids = []

for index, row in table_merged.iterrows():
    if row['Subject'] not in subjects:
        subjects.append(row['Subject'])
    if row['Course ID'] not in course_ids:
        course_ids.append(row['Course ID'])
        course_generator(row['Subject'], row['Catalog'], row['Long Title'], row['Class Units'], row['Descr'])
        if not ('Please see GRAD Calendar' in str(row['Descr'])
                or 'Please see UGRD Calendar' in str(row['Descr'])
                or 'Please see Graduate Calendar' in str(row['Descr'])
                or 'Please see Undergraduate Calendar' in str(row['Descr'])
                or 'nan' == str(row['Descr'])):
            add_topics(row['Descr'], row['Subject']+row['Catalog'], None, None)

for item in subjects:
    subject_generator(item)

course_name = 'COMP472'
add_lectures(course_name)
add_labs(course_name)

course_name = 'COMP474'
add_lectures(course_name)
add_labs(course_name)
add_worksheets(course_name)
add_course_outline(course_name)
add_readings(course_name)

# data
concordia = FCD['Concordia_University']
g.add((concordia, RDF.type, VIVO['University']))
g.add((concordia, AIISO['name'], Literal('Concordia University')))
g.add((concordia, RDFS.seeAlso, DBR['Concordia_University']))

video1 = URIRef('https://www.youtube.com/watch?v=P18EdAKuC1U')
g.add((video1, RDF.type, VIVO['Video']))

lec1 = FCD['COMP474_lecture1']
g.add((lec1, FC['content'], video1))

g.add((FCD['COMP474_lecture1'], AIISO['name'], Literal('Intelligent Systems Introduction')))
g.add((FCD['COMP474_lecture2'], AIISO['name'], Literal('Knowledge Graphs')))
g.add((FCD['COMP474_lecture3'], AIISO['name'], Literal('Vocabularies & Ontologies')))
g.add((FCD['COMP474_lecture4'], AIISO['name'], Literal('Knowledge Base Queries & SPARQL')))
g.add((FCD['COMP474_lecture5'], AIISO['name'], Literal('Knowledge Base Design & Applications')))
g.add((FCD['COMP474_lecture6'], AIISO['name'], Literal('Recommender Systems')))
g.add((FCD['COMP474_lecture7'], AIISO['name'], Literal('Machine Learning for Intelligent Systems')))
g.add((FCD['COMP474_lecture8'], AIISO['name'], Literal('Intelligent Agents')))
g.add((FCD['COMP474_lecture9'], AIISO['name'], Literal('Text Mining')))
g.add((FCD['COMP474_lecture10'], AIISO['name'], Literal('Neural Networks & Word Embeddings')))
g.add((FCD['COMP474_lecture11'], AIISO['name'], Literal('Introduction to Deep Learning')))
g.add((FCD['COMP474_lecture12'], AIISO['name'], Literal('Deep Learning for Intelligent Systems')))


g.serialize(format='nt', destination="school.nt")
g.serialize(format='ttl', destination="school.ttl")

