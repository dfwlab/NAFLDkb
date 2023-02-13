from django.shortcuts import render
from django.views.decorators import csrf
from django.http import HttpResponse
import sqlite3
import os.path


def search(request):
    result = {}
    searchterm = ''
    if request.GET != '':
        searchterm = request.GET['searchterm']
    if searchterm == '':
        return render(request, 'index.html')
    elif len(searchterm) < 3:
        return HttpResponse('Please input 3 characters at least!')
    else:
        searchterm = searchterm.strip()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
        conn = sqlite3.connect(DBfile)
        cursor = conn.cursor()
        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Associated diseases'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['Associated_diseases'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Candidates'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['Candidates'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Bioactive Compounds'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['compounds'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='CMap'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['cmap'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Natural Products'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['products'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Clinical trials'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['Clinical_trials'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Drugs'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['Drugs'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Research articles'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['Research_articles'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Therapy targets'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['Targets'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Therapy strategies'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        # row = cursor.fetchone()
        for row in cursor:
            result['Therapy_strategies'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='NAFLD Models'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            result['models'] = row[0]

        SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Pathogenesis'"
        cursor.execute(SQL, ('%' + searchterm + '%',))
        for row in cursor:
            result['pathogenesis'] = row[0]

        if result == {}:
            return HttpResponse('No result. Please try again!')
        else:
            result['searchterm'] = searchterm
            return render(request, "search.html", result)

