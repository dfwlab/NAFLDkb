from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from models.models import News, Publications, Updates
import sqlite3
import os.path
import re
import numpy as np
import pandas as pd


def index(request):
    return render(request, 'index.html')


def strategies(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    searchterm = ''
    limit = 10
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        SQL = "SELECT * from Therapy_Strategies"
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            # rows.append(row)
            rows.append([row[0], row[1], row[2], row[3], row[4]])
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Therapy strategies' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Therapy_Strategies where Strategy_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[2], row1[3], row1[4]])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    return render(request, 'strategies.html', result)


def targets(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    searchterm = ''
    graphsearch = ''
    limit = 20
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if request.GET.get('graphsearch') is not None:
        graphsearch = request.GET.get('graphsearch')
    graphsearch = graphsearch.strip()
    if graphsearch == '' and searchterm == '':
        SQL = "SELECT * from Therapy_Targets"
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            rows.append([row[0], row[1], row[3], row[4], row[5], row[7], row[8]])
    elif graphsearch == '':
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Therapy targets' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Therapy_Targets where Target_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[3], row1[4], row1[5], row1[7], row1[8]])
    else:
        SQL = "SELECT * from Therapy_Targets where "+{'action':'Target_Action', 'class':'Target_Class'}.get(graphsearch.strip(), 'Target_ID')+"=?"
        cursor.execute(SQL, (searchterm, ))
        for row in cursor:
            num = num + 1
            rows.append([row[0], row[1], row[3], row[4], row[5], row[7], row[8]])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['graphsearch'] = graphsearch
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    stats_action = [i[3] for i in rows]
    result['stats_action'] = ','.join(["{name:'"+i+"',y:"+str(stats_action.count(i))+"}" for i in set(stats_action)])
    stats_class = [i[4] for i in rows]
    result['stats_class'] = ','.join(["{name:'"+i+"',y:"+str(stats_class.count(i))+"}" for i in set(stats_class)])
    return render(request, 'targets.html', result)


def drugs(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    filterstr = ''
    rows = []
    searchterm = ''
    limit = 50
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        if request.GET.get('type') is not None:
            if request.GET.get('type') != 'All' and request.GET.get('type') != '':
                result['type'] = request.GET.get('type')
                if filterstr == '':
                    filterstr = " where Drug_Type='" + request.GET.get('type') + "'"
        if request.GET.get('reposition') is not None:
            if request.GET.get('reposition') != 'All' and request.GET.get('reposition') != '':
                result['reposition'] = request.GET.get('reposition')
                if request.GET.get('reposition') == 'Yes':
                    if filterstr == '':
                        filterstr = " where [Repositioning for NAFLD]=1"
                    else:
                        filterstr = filterstr + " and [Repositioning for NAFLD]=1"
                else:
                    if filterstr == '':
                        filterstr = " where [Repositioning for NAFLD]=0"
                    else:
                        filterstr = filterstr + " and [Repositioning for NAFLD]=0"
        if request.GET.get('trial') is not None:
            if request.GET.get('trial') != 'All' and request.GET.get('trial') != '':
                result['trial'] = request.GET.get('trial')
                if filterstr == '':
                    filterstr = " where [Clinical_Trial_Progress] like '%" + request.GET.get('trial') + "%'"
                else:
                    filterstr = filterstr + " and [Clinical_Trial_Progress] like '%" + request.GET.get('trial') + "%'"
        if request.GET.get('progress') is not None:
            if request.GET.get('progress') != 'All' and request.GET.get('progress') != '':
                result['progress'] = request.GET.get('progress')
                if filterstr == '':
                    filterstr = " where Latest_Progress like '%" + request.GET.get('progress') + "%'"
                else:
                    filterstr = filterstr + " and Latest_Progress like '%" + request.GET.get('progress') + "%'"

        if filterstr == '':
            SQL = "SELECT * from Drugs"
        else:
            SQL = "SELECT * from Drugs" + filterstr
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            # rows.append(row)
            rows.append([row[0], row[1], row[3], row[4], row[16], row[17], row[19]])
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Drugs' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Drugs where Drug_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[3], row1[4], row1[16], row1[17], row1[19]])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    stats_type = [i[2] for i in rows]
    result['stats_type'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_type.count(i))+"}" for i in set(stats_type)])
    stats_category = []
    for i in rows:
        stats_category.extend([j.strip() for j in str(i[5]).split('; ') if j.strip()!='' and j.strip()!='--' and j.strip()!='None'])
    result['stats_category'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_category.count(i))+"}" for i in set(stats_category)])
    return render(request, 'drugs.html', result)


def trials(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    searchterm = ''
    filterstr = ''
    limit = 100
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        if request.GET.get('phases') is not None:
            if request.GET.get('phases') != 'All' and request.GET.get('phases') != '':
                result['phases'] = request.GET.get('phases')
                if filterstr == '':
                    filterstr = " where Phases like '%" + request.GET.get('phases') + "%'"
        if request.GET.get('status') is not None:
            if request.GET.get('status') != 'All' and request.GET.get('status') != '':
                result['status'] = request.GET.get('status')
                if filterstr == '':
                    filterstr = " where Status='" + request.GET.get('status') + "'"
                else:
                    filterstr = filterstr + " and Status='" + request.GET.get('status') + "'"
        if request.GET.get('gender') is not None:
            if request.GET.get('gender') != 'All' and request.GET.get('gender') != '':
                result['gender'] = request.GET.get('gender')
                if filterstr == '':
                    filterstr = " where Gender like '%" + request.GET.get('gender') + "%'"
                else:
                    filterstr = filterstr + " and Gender like '%" + request.GET.get('gender') + "%'"
        if request.GET.get('age') is not None:
            if request.GET.get('age') != 'All' and request.GET.get('age') != '':
                result['age'] = request.GET.get('age')
                if filterstr == '':
                    filterstr = " where Age like '%" + request.GET.get('age') + "%'"
                else:
                    filterstr = filterstr + " and Age like '%" + request.GET.get('age') + "%'"
        if request.GET.get('locations') is not None:
            if request.GET.get('locations') != 'All' and request.GET.get('locations') != '':
                result['locations'] = request.GET.get('locations')
                if filterstr == '':
                    filterstr = " where Locations like '%" + request.GET.get('locations') + "%'"
                else:
                    filterstr = filterstr + " and Locations like '%" + request.GET.get('locations') + "%'"

        if filterstr == '':
            SQL = "SELECT * from Clinical_Trials"
        else:
            SQL = "SELECT * from Clinical_Trials" + filterstr
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            # rows.append(row)
            rows.append([row[0], row[1], row[15], row[6], row[7], row[19], row[22], row[24]])
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Clinical trials' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Clinical_Trials where Trial_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[15], row1[6], row1[7], row1[19], row1[22], row1[24]])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    stats_phase = [i[2] for i in rows]
    result['stats_phase'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_phase.count(i))+"}" for i in set(stats_phase)])
    stats_status = [i[3] for i in rows]
    result['stats_status'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_status.count(i))+"}" for i in set(stats_status)])
    return render(request, 'trials.html', result)


def diseases(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    searchterm = ''
    limit = 10
    num = 0
    str = ''
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        SQL = "SELECT * from Associated_Diseases"
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            # rows.append(row)
            str = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', row[3])
            rows.append([row[0], row[1], row[2], str, row[5]])
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Associated diseases' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Associated_Diseases where Disease_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            str = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', row1[3])
            rows.append([row1[0], row1[1], row1[2], str, row1[5]])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    return render(request, 'diseases.html', result)


def candidates(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    filterstr = ''
    searchterm = ''
    limit = 100
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        if request.GET.get('type1') is not None:
            if request.GET.get('type1') != 'All' and request.GET.get('type1') != '':
                result['type1'] = request.GET.get('type1')
                if filterstr == '':
                    filterstr = " where Source_Type like '%" + request.GET.get('type1') + "%'"
        if request.GET.get('type2') is not None:
            if request.GET.get('type2') != 'All' and request.GET.get('type2') != '':
                result['type2'] = request.GET.get('type2')
                if filterstr == '':
                    filterstr = " where Compound_Type like '%" + request.GET.get('type2') + "%'"
                else:
                    filterstr = filterstr + " and Compound_Type like '%" + request.GET.get('type2') + "%'"
        if request.GET.get('criteria') is not None:
            if request.GET.get('criteria') != 'All' and request.GET.get('criteria') != '':
                result['criteria'] = request.GET.get('criteria')
                if filterstr == '':
                    filterstr = " where Inclusion_Criteria like '%" + request.GET.get('criteria') + "%'"
                else:
                    filterstr = filterstr + " and Inclusion_Criteria like '%" + request.GET.get('criteria') + "%'"

        if filterstr == '':
            SQL = "SELECT * from Candidates"
        else:
            SQL = "SELECT * from Candidates" + filterstr
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            # rows.append(row)
            rows.append([row[0], row[1], row[2], row[3], row[4], row[15]])
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Candidates' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Candidates where Candidate_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[2], row1[3], row1[4], row1[15]])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    stats_source = []
    for i in rows:
        stats_source.extend([j.strip() for j in str(i[2]).split('; ') if j.strip()!='' and j.strip()!='--' and j.strip()!='None'])
    result['stats_source'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_source.count(i))+"}" for i in set(stats_source)])
    stats_compound = [i[3] for i in rows]
    result['stats_compound'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_compound.count(i))+"}" for i in set(stats_compound)])
    stats_inclusion = [i[5] for i in rows]
    result['stats_inclusion'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_inclusion.count(i))+"}" for i in set(stats_inclusion)])
    return render(request, 'candidates.html', result)


def compounds(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    rows1 = []
    stats_ro5s = []
    stats_targets = []
    filterstr = ''
    searchterm = ''
    ant = ''
    limit = 100
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        if request.GET.get('type') is not None:
            if request.GET.get('type') != 'All' and request.GET.get('type') != '':
                result['type'] = request.GET.get('type')
                if filterstr == '':
                    filterstr = " where Type like '%" + request.GET.get('type') + "%'"
        if request.GET.get('species') is not None:
            if request.GET.get('species') != 'All' and request.GET.get('species') != '':
                result['species'] = request.GET.get('species')
                if filterstr == '':
                    filterstr = " where [Molecular Species] like '%" + request.GET.get('species') + "%'"
                else:
                    filterstr = filterstr + " and [Molecular Species] like '%" + request.GET.get('species') + "%'"
        if request.GET.get('ro5') is not None:
            if request.GET.get('ro5') != 'All' and request.GET.get('ro5') != '':
                result['ro5'] = request.GET.get('ro5')
                if filterstr == '':
                    filterstr = " where [#RO5 Violations (Lipinski)]=" + request.GET.get('ro5')
                else:
                    filterstr = filterstr + " and [#RO5 Violations (Lipinski)]=" + request.GET.get('ro5')
        if request.GET.get('ant') is not None:
            if request.GET.get('ant') != 'All' and request.GET.get('ant') != '':
                result['ant'] = request.GET.get('ant')
                ant = request.GET.get('ant')
                ant = ant.replace("'", "''")
                ant = ant.replace("/", "_")
                if filterstr == '':
                    filterstr = " where [Targets] like '%" + ant + "%'"
                else:
                    filterstr = filterstr + " and [Targets] like '%" + ant + "%'"
        if filterstr == '':
            SQL = "SELECT * from Bioactive_Compounds"
        else:
            SQL = "SELECT * from Bioactive_Compounds" + filterstr
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            # rows.append(row)
            rows.append([row[0], row[1], row[4], row[2], row[5], row[6], row[32]])
            stats_ro5s.append(row[30])
            stats_targets.extend([k.strip() for k in str(row[8]).split('; ') if k.strip()!='' and k.strip()!='None'])
        SQL = "SELECT [Target_Name] from Therapy_Targets where [Target_Name] is not null order by Target_Name"
        cursor1.execute(SQL, )
        for row1 in cursor1:
            rows1.append([row1[0]])
        result['rows1'] = rows1
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Bioactive Compounds' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Bioactive_Compounds where compound_id=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[4], row1[2], row1[5], row1[6], row1[32]])
            stats_ro5s.append(row1[30])
            stats_targets.extend([k.strip() for k in str(row1[8]).split('; ') if k.strip()!='' and k.strip()!='None'])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    result['stats_ro5s'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_ro5s.count(i))+"}" for i in [0, 1, 2, 3, 4]])
    stats_targets_ = []
    for i in set(stats_targets):
        SQL = "SELECT * from Therapy_Targets where Target_Name like ?"
        cursor.execute(SQL, ('%' + i + '%',))
        row = cursor.fetchone()
        gene = str(row[3]).strip()
        stats_targets_.append("{name:\""+str(gene)+"\",weight:"+str(np.log(stats_targets.count(i)))+",raw:"+str(stats_targets.count(i))+",target:\""+str(i)+"\"}")
    result['stats_targets'] = ','.join(stats_targets_)
    return render(request, 'compounds.html', result)


def articles(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows = []
    searchterm = ''
    graphsearch = ''
    filterstr = ''
    limit = 100
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm').strip()
    if request.GET.get('graphsearch') is not None:
        graphsearch = request.GET.get('graphsearch').strip()
    if graphsearch == '' and searchterm == '':
        if request.GET.get('type') is not None:
            if request.GET.get('type') != 'All' and request.GET.get('type') != '':
                result['type'] = request.GET.get('type')
                if filterstr == '':
                    filterstr = " where PublicationType like '%" + request.GET.get('type') + "%'"
        if request.GET.get('source') is not None:
            if request.GET.get('source') != 'All' and request.GET.get('source') != '':
                result['source'] = request.GET.get('source')
                if filterstr == '':
                    filterstr = " where Source = '" + request.GET.get('source') + "'"
                else:
                    filterstr = filterstr + " and Source = '" + request.GET.get('source') + "'"
        if request.GET.get('year') is not None:
            if request.GET.get('year') != 'All' and request.GET.get('year') != '':
                result['year'] = request.GET.get('year')
                if request.GET.get('year') == '1 Year':
                    if filterstr == '':
                        filterstr = " where PubYear>=2021"
                    else:
                        filterstr = filterstr + " and PubYear>=2021"
                elif request.GET.get('year') == '3 Years':
                    if filterstr == '':
                        filterstr = " where PubYear>=2019"
                    else:
                        filterstr = filterstr + " and PubYear>=2019"
                elif request.GET.get('year') == '5 Years':
                    if filterstr == '':
                        filterstr = " where PubYear>=2017"
                    else:
                        filterstr = filterstr + " and PubYear>=2017"
                elif request.GET.get('year') == '10 Years':
                    if filterstr == '':
                        filterstr = " where PubYear>=2012"
                    else:
                        filterstr = filterstr + " and PubYear>=2012"
        if request.GET.get('topic') is not None:
            if request.GET.get('topic') != 'All' and request.GET.get('topic') != '':
                result['topic'] = request.GET.get('topic')
                if filterstr == '':
                    filterstr = " where MeshHeading like '%" + request.GET.get('topic') + "%'"
                else:
                    filterstr = filterstr + " and MeshHeading like '%" + request.GET.get('topic') + "%'"
        if filterstr == '':
            SQL = "SELECT * from Research_Articles"
        else:
            SQL = "SELECT * from Research_Articles" + filterstr
        # SQL = "SELECT * from Research_Articles"
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            # rows.append(row)
            rows.append([row[0], row[1], row[2], row[4], row[10]])
    elif graphsearch != '' and searchterm != '':
        # article2keywords = pd.read_csv('./static/data/Research_Articles_NLP.tsv', sep='\t', index_col=0)
        # temp = article2keywords.loc[(article2keywords['Type']==graphsearch)&(article2keywords['Keyword_in_KB']==searchterm), :]
        # for tid in set(temp['Tid']):
        SQL = "SELECT distinct Aid from Research_Articles_NLP where Type=? and [Keyword_in_KB]=?"
        cursor2.execute(SQL, (graphsearch, searchterm))
        for row2 in cursor2:
            SQL = "SELECT * from Research_Articles where Article_ID=?"
            cursor1.execute(SQL, (row2[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[2], row1[4], row1[10]])
            num += 1
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Research articles' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Research_Articles where Article_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[2], row1[4], row1[10]])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num

    # #######
    # article2keywords = pd.read_csv('./static/data/Research_Articles_NLP.tsv', sep='\t', index_col=0)
    # #print(article2keywords.head())
    # # strategy
    # temp = article2keywords.loc[article2keywords['Type']=='strategy_details', :]
    # stats_temp = []
    # for i in set(temp['Keyword_in_KB']):
    #     stats_temp.append([i, len(set(temp.loc[temp['Keyword_in_KB']==i, 'Aid']))])
    stats_temp = []
    SQL = "SELECT Keyword_in_KB, count(distinct Aid) from Research_Articles_NLP where Type='strategy_details' group by Keyword_in_KB"
    cursor2.execute(SQL,)
    for row2 in cursor2:
        stats_temp.append([row2[0], row2[1]])
    result['stats_strategy'] = ','.join(["{name:\""+str(i)+"\",weight:"+str(j)+"}" for i, j in stats_temp])

    # target
    # temp = article2keywords.loc[article2keywords['Type']=='target_details', :]
    # stats_temp = []
    # for i in set(temp['Keyword_in_KB']):
    #     stats_temp.append([i, len(set(temp.loc[temp['Keyword_in_KB']==i, 'Aid']))])

    stats_temp = []
    SQL = "SELECT Keyword_in_KB, count(distinct Aid) from Research_Articles_NLP where Type='target_details' group by Keyword_in_KB"
    cursor2.execute(SQL,)
    for row2 in cursor2:
        stats_temp.append([row2[0], row2[1]])
    result['stats_target'] = ','.join(["{name:\""+str(i)+"\",weight:"+str(j)+"}" for i, j in stats_temp])

    # disease
    # temp = article2keywords.loc[article2keywords['Type']=='disease_details', :]
    # stats_temp = []
    # for i in set(temp['Keyword_in_KB']):
    #     stats_temp.append([i, len(set(temp.loc[temp['Keyword_in_KB']==i, 'Aid']))])

    stats_temp = []
    SQL = "SELECT Keyword_in_KB, count(distinct Aid) from Research_Articles_NLP where Type='disease_details' group by Keyword_in_KB"
    cursor2.execute(SQL,)
    for row2 in cursor2:
        stats_temp.append([row2[0], row2[1]])
    result['stats_disease'] = ','.join(["{name:\""+str(i)+"\",weight:"+str(j)+"}" for i, j in stats_temp])

    # drug
    # temp = article2keywords.loc[article2keywords['Type']=='drug_details', :]
    # stats_temp = []
    # for i in set(temp['Keyword_in_KB']):
    #     stats_temp.append([i, len(set(temp.loc[temp['Keyword_in_KB']==i, 'Aid']))])

    stats_temp = []
    SQL = "SELECT Keyword_in_KB, count(distinct Aid) from Research_Articles_NLP where Type='drug_details' group by Keyword_in_KB"
    cursor2.execute(SQL,)
    for row2 in cursor2:
        stats_temp.append([row2[0], row2[1]])
    result['stats_drug'] = ','.join(["{name:\""+str(i)+"\",weight:"+str(j)+"}" for i, j in stats_temp])
    
    return render(request, 'articles.html', result)


def models(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    searchterm = ''
    filterstr = ''
    limit = 20
    num = 0
    str = ''
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        if request.GET.get('Category') is not None:
            if request.GET.get('Category') != 'All' and request.GET.get('Category') != '':
                result['Category'] = request.GET.get('Category')
                if filterstr == '':
                    filterstr = " where Category='" + request.GET.get('Category') + "'"
        if request.GET.get('Class') is not None:
            if request.GET.get('Class') != 'All' and request.GET.get('Class') != '':
                result['Class'] = request.GET.get('Class')
                if filterstr == '':
                    filterstr = " where Class='" + request.GET.get('Class') + "'"
                else:
                    filterstr = filterstr + " and Class='" + request.GET.get('Class') + "'"
        if request.GET.get('Source') is not None:
            if request.GET.get('Source') != 'All' and request.GET.get('Source') != '':
                result['Source'] = request.GET.get('Source')
                if filterstr == '':
                    filterstr = " where Source like '%" + request.GET.get('Source') + "%'"
                else:
                    filterstr = filterstr + " and Source like '%" + request.GET.get('Source') + "%'"
        if filterstr == '':
            SQL = "SELECT * from NAFLD_Models"
        else:
            SQL = "SELECT * from NAFLD_Models" + filterstr
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            pmlink = ''
            pmids = row[7].split("; ")
            for pmid in pmids:
                if pmlink == '':
                    pmlink = '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
                else:
                    pmlink = pmlink + '; ' + '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
            rows.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], pmlink])
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='NAFLD Models' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from NAFLD_Models where Model_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            pmlink = ''
            pmids = row1[7].split("; ")
            for pmid in pmids:
                if pmlink == '':
                    pmlink = '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
                else:
                    pmlink = pmlink + '; ' + '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
            rows.append([row1[0], row1[1], row1[2], row1[3], row1[4], row1[5], row1[6], pmlink])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    return render(request, 'models.html', result)


def pathogenesis(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    searchterm = ''
    limit = 10
    num = 0
    str = ''
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        SQL = "SELECT * from Pathogenesis"
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            pmlink = ''
            pmids = row[4].split("; ")
            for pmid in pmids:
                if pmlink == '':
                    pmlink = '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
                else:
                    pmlink = pmlink + '; ' + '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
            rows.append([row[0], row[1], row[2], row[3], pmlink])
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Pathogenesis' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Pathogenesis where [Path_ID]=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            pmlink = ''
            pmids = row1[4].split("; ")
            for pmid in pmids:
                if pmlink == '':
                    pmlink = '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
                else:
                    pmlink = pmlink + '; ' + '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
            rows.append([row1[0], row1[1], row1[2], row1[3], pmlink])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    return render(request, 'pathogenesis.html', result)


def casestudy(request):
    return render(request, 'casestudy.html')


def downloads(request):
    return render(request, 'downloads.html')


def about(request):
    return render(request, 'about.html')


def structure(request):
    return render(request, 'structure.html')


def screening(request):
    return render(request, 'screening.html')


def reposition(request):
    return render(request, 'reposition.html')

def annotation(request):
    return render(request, 'annotation.html')

def cmap(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    rows1 = []
    stats_targets = []
    stats_moa = []
    filterstr = ''
    searchterm = ''
    limit = 100
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        if request.GET.get('ant') is not None:
            if request.GET.get('ant') != 0 and request.GET.get('ant') != '' and str(request.GET.get('ant')).strip()!='0':
                result['antid'] = request.GET.get('ant')
                SQL = "SELECT * from Therapy_Targets where [Target_id]=?"
                cursor1.execute(SQL, (request.GET.get('ant'),))
                row = cursor1.fetchone()
                result['ant'] = row[1]
                ant = row[3]
                if filterstr == '':
                    filterstr = " where [Targets] like '%" + ant + "%'"
                else:
                    filterstr = filterstr + " and [Targets] like '%" + ant + "%'"
        if filterstr == '':
            SQL = "SELECT * from CMap where pert_id like '%BRD-%' order by CMap_id"
        else:
            SQL = "SELECT * from CMap" + filterstr
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            rows.append([row[0], row[1], row[2], row[3], row[4], row[7]])
            stats_targets.extend([k.strip() for k in str(row[3]).split('; ') if k.strip()!='' and k.strip()!='None'])
            stats_moa.extend([k.strip() for k in str(row[4]).split('; ') if k.strip()!='' and k.strip()!='None'])
        SQL = "SELECT * from Therapy_Targets where [Target_Name] is not null order by Target_Name"
        cursor1.execute(SQL, )
        for row1 in cursor1:
            rows1.append([row1[0], row1[1]])
        result['rows1'] = rows1
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='CMap' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from CMap where CMap_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[2], row1[3], row1[4], row1[7]])
            stats_targets.extend([k.strip() for k in str(row1[3]).split('; ') if k.strip()!='' and k.strip()!='None'])
            stats_moa.extend([k.strip() for k in str(row1[4]).split('; ') if k.strip()!='' and k.strip()!='None'])
    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    stats_targets_ = []
    for i in set(stats_targets):
        stats_targets_.append("{name:\""+str(i)+"\",weight:"+str(stats_targets.count(i))+",raw:"+str(stats_targets.count(i))+",target:\""+str(i)+"\"}")
    result['stats_targets'] = ','.join(stats_targets_)
    stats_moa_ = []
    for i in set(stats_moa):
        stats_moa_.append("{name:\""+str(i)+"\",weight:"+str(stats_moa.count(i))+",raw:"+str(stats_moa.count(i))+",target:\""+str(i)+"\"}")
    result['stats_moa'] = ','.join(stats_moa_)
    return render(request, 'cmap.html', result)


def products(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows = []
    rows1 = []
    rows2 = []
    filterstr = ''
    searchterm = ''
    limit = 100
    num = 0
    if request.GET.get('searchterm') is not None:
        searchterm = request.GET.get('searchterm')
    searchterm = searchterm.strip()
    if searchterm == '':
        if request.GET.get('type') != 'All' and request.GET.get('type') is not None and request.GET.get('type') != '':
            result['type'] = request.GET.get('type')
            type = request.GET.get('type')
            if filterstr == '':
                filterstr = " where Pathway like '%" + type + "%'"
            else:
                filterstr = filterstr + " and Pathway like '%" + type + "%'"
        if request.GET.get('source') != 'All' and request.GET.get('source') is not None and request.GET.get('source') != '':
            result['source'] = request.GET.get('source')
            source = request.GET.get('source')
            if filterstr == '':
                filterstr = " where Biological_Source like '%" + source + "%'"
            else:
                filterstr = filterstr + " and Biological_Source like '%" + source + "%'"
        if request.GET.get('drug') != 'All' and request.GET.get('drug') is not None and request.GET.get('drug') != '':
            result['drug'] = request.GET.get('drug')
            drug = request.GET.get('drug')
            if filterstr == '':
                filterstr = " where Drug_Name like '%" + drug + "%'"
            else:
                filterstr = filterstr + " and Drug_Name like '%" + drug + "%'"
        if filterstr == '':
            SQL = "SELECT * from Natural_Products order by Product_ID"
        else:
            SQL = "SELECT * from Natural_Products" + filterstr
        cursor.execute(SQL)
        for row in cursor:
            num = num + 1
            rows.append([row[0], row[1], row[2], row[6], row[7], row[10], row[9]])
        SQL = "SELECT Biological_Source from Natural_Products where Biological_Source is not null group by Biological_Source order by Biological_Source"
        cursor1.execute(SQL, )
        for row1 in cursor1:
            rows1.append([row1[0]])
        result['rows1'] = rows1
        SQL = "SELECT Drug_Name from Natural_Products where Drug_Name is not null group by Drug_Name order by Drug_Name"
        cursor1.execute(SQL, )
        for row1 in cursor1:
            rows2.append([row1[0]])
        result['rows2'] = rows2
    else:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Natural Products' group by class_id"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            num = num + 1
            SQL = "SELECT * from Natural_Products where Product_ID=?"
            cursor1.execute(SQL, (row[0], ))
            row1 = cursor1.fetchone()
            rows.append([row1[0], row1[1], row1[2], row1[6], row1[7], row1[10], row1[9]])

    p = Paginator(rows, limit)
    page = request.GET.get('page')
    if page:
        pass
    else:
        page = 1
    try:
        a_a = p.page(page)
        page1 = p.page(page)
        page_list = page1.object_list
    except PageNotAnInteger:
        a_a = p.page(1)
    except EmptyPage:
        a_a = p.page(p.num_pages)
    result['searchterm'] = searchterm
    result['page_list'] = page_list
    result['second_list_obj'] = a_a
    result['p'] = p
    result['num'] = num
    stats_category = [i[3] for i in rows]
    stats_category_ = []
    for i in stats_category:
        stats_category_.extend([j.strip() for j in str(i).split('/') if j.strip()!='None' and j.strip()!=''])
    result['stats_category'] = ','.join(["{name:'"+str(i)+"',y:"+str(stats_category_.count(i))+"}" for i in set(stats_category_)])
    stats_source = [i[4] for i in rows]
    stats_source_ = []
    for i in set(stats_source):
        stats_source_.append("{name:\""+str(i)+"\",weight:"+str(stats_source.count(i))+",raw:"+str(stats_source.count(i))+",target:\""+str(i)+"\"}")
    result['stats_source'] = ','.join(stats_source_)
    return render(request, 'products.html', result)


def file_iterator(file_name, chunk_size=1024):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def download(request):
    filename = request.GET['file']
    file = open('./static/data/'+filename, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename='+filename
    return response


def tutorial(request):
    return render(request, 'tutorial.html')


