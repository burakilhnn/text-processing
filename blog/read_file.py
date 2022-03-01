import re
from datetime import datetime
import datefinder
import fitz
from .models import Pdf


def read_pdf(pathname,file_id):
    all_pdf = []
    with fitz.open(pathname) as doc:
        text = ""
        for page in doc:
            text = page.get_text()   
            all_pdf.append(text)

    all_pdf[0] = all_pdf[0].replace('\n','')
    all_pdf[0] = all_pdf[0].replace("..","")
    all_pdf[0] = all_pdf[0].split("  ")
    str_list = list(filter(None, all_pdf[0]))
    for i in range (0,len(str_list)):
        str_list[i] = str_list[i].strip()
    lesson = str_list[3]
    title = str_list[4]
    student_name = str_list[5]

    supervisor = ""
    judges = []

    for i in range(len(str_list)):
        if "Danışman" in str_list[i]:
            str_list[i] = str_list[i].replace("Danışman","")
            name = str_list[i].split(",")
            supervisor = name[0].strip()
        if "Jüri" in str_list[i]:
            str_list[i] = str_list[i].replace("Jüri Üyesi","")
            name = str_list[i].split(",")
            judges.append(name[0].strip())

    matches = list(datefinder.find_dates(str_list[-1]))

    if len(matches) > 0:
        date = matches[0]
    else:
        print('No dates found')

    if date.day > 1 and date.day < 9:
        delivery_date = str(date.year - 1) + "-" + str(date.year) + " Bahar"
    else:
        delivery_date = str(date.year) + "-" + str(date.year+1) + " Güz"
    idx  = 0
    for i in range(len(all_pdf)):
        if "ÖZET" in all_pdf[i]:
            idx = i

    all_pdf[idx] = all_pdf[idx].replace('\n','')
    all_pdf[idx] = all_pdf[idx].replace("..","")
    all_pdf[idx] = all_pdf[idx].split("  ")
    str_list2 = list(filter(None, all_pdf[idx]))
    for i in range (0,len(str_list2)):
        str_list2[i] = str_list2[i].strip()

    key = len(str_list2) - 1

    keyword_idx = str_list2[key].index('Anahtar')
    summary = str_list2[key][:keyword_idx]
    summary = str_list2[key] + summary
    summary = summary.replace("ÖZET","").strip()

    keywords = str_list2[key][keyword_idx:]
    keywords = keywords.replace("Anahtar kelimeler:","").strip()
    keywords_list = keywords.split(",")
    for i in range(len(keywords_list)):
        keywords_list[i] = keywords_list[i].strip()

    all_pdf[2] = all_pdf[2].replace('\n','')
    all_pdf[2] = all_pdf[2].split("  ")
    str_list3 = list(filter(None, all_pdf[2]))
    for i in range (0,len(str_list3)):
        str_list3[i] = str_list3[i].strip()

    student_no = re.findall(r'\d+', str_list3[-1])
    student_no = str(student_no[0])

    type_of_edu = ""

    if(student_no[5] == "2"):
        type_of_edu = "Gece"
    else:
        type_of_edu = "Örgün"

    student_no = int(student_no)

    obj = Pdf.objects.get(id=file_id)
    obj.title=title
    obj.student=student_name
    obj.lesson=lesson
    obj.season=delivery_date
    obj.keywords=keywords_list
    obj.judges=judges
    obj.supervisor=supervisor
    obj.summary=summary
    obj.student_no = student_no
    obj.type_of_edu = type_of_edu
    obj.save()
    

    
    
