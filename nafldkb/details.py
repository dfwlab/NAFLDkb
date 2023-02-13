from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import sqlite3
import os.path
import re
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import Draw
from base64 import b64encode
from io import BytesIO


def strategy_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows1 = []
    rows2 = []
    rows3 = []
    rows4 = []
    links = []
    nodes = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Therapy_Strategies where Strategy_ID=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    result['Strategy_ID'] = row[0]
    result['Therapy_strategy'] = row[1]
    result['Synonyms'] = row[2]
    result['Therapy_Targets'] = row[3]
    result['Therapy_Drugs'] = row[4]
    result['Mechanism'] = row[5]
    result['knowledge_points'] = row[6]
    result['Medical_Therapy'] = row[8]
    nodes.append("{id: '" + str(row[1]) + "', color:'#2f7ed8', marker: {radius: 20}, dataLabels: 'strategy'}, ")
    pmlink = ''
    pmids = row[7].split("; ")
    for pmid in pmids:
        if pmlink == '':
            pmlink = '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
        else:
            pmlink = pmlink + '; ' + '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
    result['pmlink'] = pmlink
    if row[8] != 0:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Therapy targets' group by class_id"
        cursor1.execute(SQL, ('%' + row[6] + '%',))
        num = 0
        for row1 in cursor1:
            num = num + 1
            SQL = "SELECT * from Therapy_Targets where Target_ID=?"
            cursor2.execute(SQL, (row1[0],))
            row2 = cursor2.fetchone()
            rows1.append([row2[0], row2[1], row2[3], row2[4], row2[5], row2[7], row2[8]])
            nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#8bbc21', marker: {symbol: 'square', radius: 10}, datatype: 'targets'},")
            links.append("{from: '" + str(row[1]) + "', to: '" + str(row2[1]).replace("'", "") + "'},")
        result['rows1'] = rows1
        result['num1'] = num

    if row[8] != 0:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Drugs' group by class_id"  # limit 10
        cursor1.execute(SQL, ('%' + row[6] + '%',))
        num = 0
        for row1 in cursor1:
            num = num + 1
            SQL = "SELECT * from Drugs where Drug_ID=?"
            cursor2.execute(SQL, (row1[0],))
            row2 = cursor2.fetchone()
            if num < 11:
                rows2.append([row2[0], row2[1], row2[3], row2[4], row2[16], row2[17], row2[19]])
                nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#910000', marker: {symbol: 'triangle', radius: 10}, datatype: 'drugs'},")
                links.append("{from: '" + str(row[1]) + "', to: '" + str(row2[1]).replace("'", "") + "'},")
        result['rows2'] = rows2
        result['num2'] = num

    if row[8] != 0:
        SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Candidates' group by class_id"  # limit 10
        cursor1.execute(SQL, ('%' + row[6] + '%',))
        num = 0
        for row1 in cursor1:
            num = num + 1
            SQL = "SELECT * from Candidates where Candidate_ID=?"
            cursor2.execute(SQL, (row1[0],))
            row2 = cursor2.fetchone()
            if num < 11:
                rows3.append([row2[0], row2[1], row2[2], row2[3], row2[4], row2[15]])
                nodes.append("{id: '" + str(row2[4]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#1aadce', marker: {symbol: 'triangle-down', radius: 10}, datatype: 'candidates'},")
                links.append("{from: '" + str(row[1]) + "', to: '" + str(row2[4]).replace("'", "") + "'},")
        result['rows3'] = rows3
        result['num3'] = num

    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Research articles' group by class_id"
    cursor1.execute(SQL, ('%' + row[6] + '%',))
    num = 0
    for row1 in cursor1:
        num = num+1
        if num < 21:
            SQL = "SELECT * from Research_Articles where Article_id=?"
            cursor2.execute(SQL, (row1[0],))
            row2 = cursor2.fetchone()
            rows4.append([row2[0], row2[1], row2[2], row2[4]])
    result['rows4'] = rows4
    result['num4'] = num
    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'strategy_details.html', result)


def target_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    rows2 = []
    rows3 = []
    rows4 = []
    links = []
    nodes = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Therapy_Targets where Target_ID=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    rows0.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
    result['rows0'] = rows0
    nodes.append("{id: '" + str(row[1]).replace("'", "") + "', color:'#8bbc21', marker: {symbol: 'square', radius: 20}, dataLabels: 'target'}, ")
    pmlink = ''
    pmids = row[10].split("; ")
    for pmid in pmids:
        if pmlink == '':
            pmlink = '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
        else:
            pmlink = pmlink + '; ' + '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
    result['pmlink'] = pmlink

    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Drugs' group by class_id"
    cursor1.execute(SQL, ('%' + row[1] + '%',))
    num = 0
    for row1 in cursor1:
        num = num + 1
        SQL = "SELECT * from Drugs where Drug_ID=?"
        cursor2.execute(SQL, (row1[0],))
        row2 = cursor2.fetchone()
        if num < 11:
            rows1.append([row2[0], row2[1], row2[3], row2[4], row2[16], row2[17], row2[19]])
            nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#910000', marker: {symbol: 'triangle', radius: 10}, datatype: 'drugs'},")
            links.append("{from: '" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows1'] = rows1
    result['num1'] = num

    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Candidates' group by class_id"
    cursor1.execute(SQL, ('%' + row[1] + '%',))
    num = 0
    for row1 in cursor1:
        num = num + 1
        SQL = "SELECT * from Candidates where Candidate_ID=?"
        cursor2.execute(SQL, (row1[0],))
        row2 = cursor2.fetchone()
        if num < 11:
            rows2.append([row2[0], row2[1], row2[2], row2[3], row2[4], row2[15]])
            nodes.append("{id: '" + str(row2[4]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#1aadce', marker: {symbol: 'triangle-down', radius: 10}, datatype: 'candidates'},")
            links.append("{from: '" + str(row[1]).replace("'", "") + "', to: '" + str(row2[4]).replace("'", "") + "'},")
    result['rows2'] = rows2
    result['num2'] = num

    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Research articles' group by class_id"
    cursor1.execute(SQL, ('%' + row[1] + '%',))
    num = 0
    for row1 in cursor1:
        num = num + 1
        if num < 21:
            SQL = "SELECT * from Research_Articles where Article_id=?"
            cursor2.execute(SQL, (row1[0],))
            row2 = cursor2.fetchone()
            rows3.append([row2[0], row2[1], row2[2], row2[4]])
    result['rows3'] = rows3
    result['num3'] = num
    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Bioactive Compounds' group by class_id"
    cursor1.execute(SQL, ('%' + row[1] + '%',))
    num = 0
    for row1 in cursor1:
        num = num + 1
        if num < 11:
            SQL = "SELECT * from Bioactive_Compounds where compound_id=?"
            cursor2.execute(SQL, (row1[0],))
            row2 = cursor2.fetchone()
            rows4.append([row2[0], row2[1], row2[4], row2[2], row2[5], row2[6], row2[32]])
    result['rows4'] = rows4
    result['num4'] = num
    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'target_details.html', result)


def drug_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    rows2 = []
    rows3 = []
    rows4 = []
    links = []
    nodes = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Drugs where Drug_ID=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    rows0.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                  row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19]])
    result['rows0'] = rows0
    if row[9] is not None:
        try:
            smi = row[9]
            m = Chem.MolFromSmiles(smi)
            image_io = BytesIO()
            img = Draw.MolToImage(m)
            img.save(image_io, 'PNG')
            dataurl = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
            result['img'] = dataurl
        except:
            pass
    nodes.append("{id: '" + str(row[1]).replace("'", "") + "', color:'#910000', marker: {symbol: 'triangle', radius: 20}, dataLabels: 'drug'}, ")
    num = 0
    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Clinical trials' group by class_id"
    cursor1.execute(SQL, ('%' + row[1] + '%',))
    for row1 in cursor1:
        num = num + 1
        SQL = "SELECT * from Clinical_Trials where Trial_ID=? and Trial_ID is not null"
        cursor2.execute(SQL, (row1[0],))
        row2 = cursor2.fetchone()
        rows1.append([row2[0], row2[1], row2[15], row2[6], row2[7], row2[19], row2[22], row2[24]])
        nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#1aadce', marker: {symbol: 'diamond', radius: 10}, datatype: 'trials'},")
        links.append("{from: '" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows1'] = rows1
    result['num1'] = num
    num = 0
    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Research articles' group by class_id"
    cursor1.execute(SQL, ('%' + row[1] + '%',))
    for row1 in cursor1:
        num = num + 1
        if num < 21:
            SQL = "SELECT * from Research_Articles where Article_id=?"
            cursor2.execute(SQL, (row1[0],))
            row2 = cursor2.fetchone()
            rows2.append([row2[0], row2[1], row2[2], row2[4]])
    result['rows2'] = rows2
    result['num2'] = num

    targetids = []
    cursor1.execute("SELECT * from Therapy_Targets")
    for row1 in cursor1:
        targets = row1[1]
        if row1[2] is not None:
            targets = targets + "; " + row1[2]
        targets = targets.split('; ')
        for target in targets:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Drugs' and class_id=?"
            cursor2.execute(SQL, ('%' + target.replace("'", "") + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    targetids.append(row1[0])
    targetids = list(set(targetids))
    num = 0
    for targetid in targetids:
        num = num + 1
        SQL = "SELECT * from Therapy_Targets where Target_ID=?"
        cursor2.execute(SQL, (targetid,))
        row2 = cursor2.fetchone()
        rows3.append([row2[0], row2[1], row2[3], row2[4], row2[5], row2[7], row2[8]])
        nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#8bbc21', marker: {symbol: 'square', radius: 10}, datatype: 'targets'},")
        links.append("{from: '" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows3'] = rows3
    result['num3'] = num

    stragyids = []
    cursor1.execute("SELECT * from Therapy_Strategies")
    for row1 in cursor1:
        strategies = row1[1]
        if row1[2] is not None:
            strategies = strategies + "; " + row1[2]
        strategies = strategies.split('; ')
        for strategy in strategies:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Drugs' and class_id=?"
            cursor2.execute(SQL, ('%' + strategy + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    stragyids.append(row1[0])
    stragyids = list(set(stragyids))
    num = 0
    for stragyid in stragyids:
        num = num + 1
        SQL = "SELECT * from Therapy_Strategies where Strategy_ID=?"
        cursor2.execute(SQL, (stragyid,))
        row2 = cursor2.fetchone()
        rows4.append([row2[0], row2[1], row2[2], row2[3], row2[4]])
        nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#2f7ed8', marker: {symbol: 'circle', radius: 10}, datatype: 'strategies'},")
        links.append("{from: '" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows4'] = rows4
    result['num4'] = num
    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'drug_details.html', result)


def trial_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    links = []
    nodes = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Clinical_Trials where Trial_ID=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    rows0.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                  row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22]
                  , row[23], row[24]])
    result['rows0'] = rows0
    nodes.append("{id: '" + str(row[1]).replace("'", "") + "', color:'#1aadce', marker: {symbol: 'diamond', radius: 20}, dataLabels: 'trial'}, ")
    num = 0
    if row[3] is not None:
        drugids = row[3].split("; ")
        for drugid in drugids:
            num = num + 1
            SQL = "SELECT * from Drugs where Drug_ID=?"
            cursor2.execute(SQL, (drugid,))
            row2 = cursor2.fetchone()
            if num < 11:
                rows1.append([row2[0], row2[1], row2[3], row2[4], row2[16], row2[17], row2[19]])
            nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#910000', marker: {symbol: 'triangle', radius: 10}, datatype: 'drugs'},")
            links.append("{from: '" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
        result['rows1'] = rows1
        result['num1'] = num
    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'trial_details.html', result)


def disease_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    rows2 = []
    rows3 = []
    links = []
    nodes = []
    str1 = ''
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Associated_Diseases where Disease_ID=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    str1 = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', row[3])
    rows0.append([row[0], row[1], row[2], str1, row[4], row[5], row[6], row[7], row[8], row[9]])
    result['rows0'] = rows0
    nodes.append("{id: '" + str(row[2]).replace("'", "") + "', color:'#f28f43', marker: {symbol: 'triangle', radius: 20}, dataLabels: 'target'}, ")
    pmlink = ''
    pmids = row[8].split("; ")
    for pmid in pmids:
        if pmlink == '':
            pmlink = '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
        else:
            pmlink = pmlink + '; ' + '<a href="https://pubmed.ncbi.nlm.nih.gov/' + pmid + '" target="_blank">' + pmid + '</a>'
    result['pmlink'] = pmlink

    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Drugs' group by class_id"
    cursor1.execute(SQL, ('%' + row[9] + '%',))
    num = 0
    for row1 in cursor1:
        num = num + 1
        SQL = "SELECT * from Drugs where Drug_ID=?"
        cursor2.execute(SQL, (row1[0],))
        row2 = cursor2.fetchone()
        if num < 11:
            rows1.append([row2[0], row2[1], row2[3], row2[4], row2[16], row2[17], row2[19]])
            nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#910000', marker: {symbol: 'triangle', radius: 10}, datatype: 'drugs'},")
            links.append("{from: '" + str(row[2]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows1'] = rows1
    result['num1'] = num

    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Candidates' group by class_id"
    cursor1.execute(SQL, ('%' + row[9] + '%',))
    num = 0
    for row1 in cursor1:
        num = num + 1
        SQL = "SELECT * from Candidates where Candidate_ID=?"
        cursor2.execute(SQL, (row1[0],))
        row2 = cursor2.fetchone()
        if num < 11:
            rows2.append([row2[0], row2[1], row2[2], row2[3], row2[4], row2[15]])
            nodes.append("{id: '" + str(row2[4]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#1aadce', marker: {symbol: 'triangle-down', radius: 10}, datatype: 'candidates'},")
            links.append("{from: '" + str(row[2]).replace("'", "") + "', to: '" + str(row2[4]).replace("'", "") + "'},")
    result['rows2'] = rows2
    result['num2'] = num

    SQL = "SELECT class_id from NAFLDdb where knowledge_points like ? and class='Research articles' group by class_id"
    cursor1.execute(SQL, ('%' + row[9] + '%',))
    num = 0

    for row1 in cursor1:
        num = num + 1
        if num < 21:
            SQL = "SELECT * from Research_Articles where Article_id=?"
            cursor2.execute(SQL, (row1[0],))
            row2 = cursor2.fetchone()
            rows3.append([row2[0], row2[1], row2[2], row2[4]])
    result['rows3'] = rows3
    result['num3'] = num
    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'disease_details.html', result)


def candidate_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    rows2 = []
    rows3 = []
    links = []
    nodes = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Candidates where Candidate_ID=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    rows0.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                  row[12], row[13], row[14], row[15]])
    result['rows0'] = rows0
    if row[7] is not None:
        try:
            smi = row[7]
            m = Chem.MolFromSmiles(smi)
            image_io = BytesIO()
            img = Draw.MolToImage(m)
            img.save(image_io, 'PNG')
            dataurl = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
            result['img'] = dataurl
        except:
            pass
    nodes.append("{id: '" + str(row[4]).replace("'", "") + "', color:'#1aadce', marker: {symbol: 'triangle-down', radius: 20}, dataLabels: 'candidate'}, ")

    stragyids = []
    cursor1.execute("SELECT * from Therapy_Strategies")
    for row1 in cursor1:
        strategies = row1[1]
        if row1[2] is not None:
            strategies = strategies + "; " + row1[2]
        strategies = strategies.split('; ')
        for strategy in strategies:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Candidates' and class_id=?"
            cursor2.execute(SQL, ('%' + strategy + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    stragyids.append(row1[0])
    stragyids = list(set(stragyids))
    num = 0
    for stragyid in stragyids:
        num = num + 1
        SQL = "SELECT * from Therapy_Strategies where Strategy_ID=?"
        cursor2.execute(SQL, (stragyid,))
        row2 = cursor2.fetchone()
        rows1.append([row2[0], row2[1], row2[2], row2[3], row2[4]])
        nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#2f7ed8', marker: {symbol: 'circle', radius: 10}, datatype: 'strategies'},")
        links.append("{from: '" + str(row[4]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows1'] = rows1
    result['num1'] = num

    targetids = []
    cursor1.execute("SELECT * from Therapy_Targets")
    for row1 in cursor1:
        targets = row1[1]
        if row1[2] is not None:
            targets = targets + "; " + row1[2]
        targets = targets.split('; ')
        for target in targets:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Candidates' and class_id=?"
            cursor2.execute(SQL, ('%' + target.replace("'", "") + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    targetids.append(row1[0])
    targetids = list(set(targetids))
    num = 0
    for targetid in targetids:
        num = num + 1
        SQL = "SELECT * from Therapy_Targets where Target_ID=?"
        cursor2.execute(SQL, (targetid,))
        row2 = cursor2.fetchone()
        rows2.append([row2[0], row2[1], row2[3], row2[4], row2[5], row2[7], row2[8]])
        nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#8bbc21', marker: {symbol: 'square', radius: 10}, datatype: 'targets'},")
        links.append("{from: '" + str(row[4]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows2'] = rows2
    result['num2'] = num

    diseaseids = []
    cursor1.execute("SELECT * from Associated_Diseases")
    for row1 in cursor1:
        diseases = row1[2]
        if row1[4] is not None:
            diseases = diseases + "; " + row1[4]
        diseases = diseases.split('; ')
        for disease in diseases:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Candidates' and class_id=?"
            cursor2.execute(SQL, ('%' + disease.replace("'", "") + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    diseaseids.append(row1[0])
    diseaseids = list(set(diseaseids))
    num = 0
    for diseaseid in diseaseids:
        num = num + 1
        SQL = "SELECT * from Associated_Diseases where Disease_ID=?"
        cursor2.execute(SQL, (diseaseid,))
        row2 = cursor2.fetchone()
        rows3.append([row2[0], row2[1], row2[2], row2[3], row2[5]])
        nodes.append("{id: '" + str(row2[2]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#f28f43', marker: {symbol: 'triangle', radius: 10}, datatype: 'diseases'},")
        links.append("{from: '" + str(row[4]).replace("'", "") + "', to: '" + str(row2[2]).replace("'", "") + "'},")
    result['rows3'] = rows3
    result['num3'] = num

    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'candidate_details.html', result)


def compound_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    links = []
    nodes = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Bioactive_Compounds where compound_id=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    rows0.append([row[0], row[1], row[4], row[2], row[3], row[6], row[7], row[32], row[8]])
    result['rows0'] = rows0
    nodes.append("{id: '" + str(row[1]).replace("'", "") + "', color:'#D8BFD8', marker: {symbol: 'circle', radius: 20}},")
    targets = row[8]
    targets = targets.split('; ')
    num = 0
    for target in targets:
        num = num + 1
        SQL = "SELECT * from Therapy_Targets where Target_Name like ?"
        cursor2.execute(SQL, ('%' + target + '%',))
        row2 = cursor2.fetchone()
        rows1.append([row2[0], row2[1], row2[3], row2[4], row2[5], row2[7], row2[8]])
        nodes.append(
            "{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#8bbc21', marker: {symbol: 'square', radius: 10}, datatype: 'targets'},")
        links.append("{from: '" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows1'] = rows1
    result['num1'] = num
    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'compound_details.html', result)


def cmap_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from CMap where CMap_id=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    rows0.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
    result['rows0'] = rows0
    if row[5] is not None:
        try:
            smi = row[5]
            m = Chem.MolFromSmiles(smi)
            image_io = BytesIO()
            img = Draw.MolToImage(m)
            img.save(image_io, 'PNG')
            dataurl = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
            result['img'] = dataurl
        except:
            pass
    SQL1 = "SELECT * from CMap_Scores where pert_id=?"
    cursor1.execute(SQL1, (row[1], ))
    for row1 in cursor1:
        rows1.append([row1[0], row1[1], row1[2], row1[3], row1[4], row1[5], row1[6], row1[7], row1[8], row1[9], row1[10]])
    result['rows1'] = rows1

    return render(request, 'cmap_details.html', result)


def product_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    links = []
    nodes = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Natural_Products where Product_ID=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    rows0.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
    result['rows0'] = rows0
    if row[4] is not None:
        try:
            smi = row[4]
            m = Chem.MolFromSmiles(smi)
            image_io = BytesIO()
            img = Draw.MolToImage(m)
            img.save(image_io, 'PNG')
            dataurl = 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
            result['img'] = dataurl
        except:
            pass
    if row[1] is not None:
        nodes.append("{id: '" + str(row[1]).replace("'", "") + "', color:'#00FF00', marker: {symbol: 'circle', radius: 20}},")
    else:
        nodes.append("{id: '" + str(row[0]).replace("'", "") + "', color:'#00FF00', marker: {symbol: 'circle', radius: 20}},")
    SQL = "SELECT Drug_ID from Natural_Products where Source_ID=? group by Drug_ID order by Drug_ID"
    cursor1.execute(SQL, (row[8], ))
    num = 0
    for row1 in cursor1:
        num = num + 1
        SQL = "SELECT * from Drugs where Drug_ID=?"
        cursor2.execute(SQL, (row1[0],))
        row2 = cursor2.fetchone()
        rows1.append([row2[0], row2[1], row2[3], row2[4], row2[16], row2[17], row2[19]])
        if row[1] is not None:
            nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#910000', marker: {symbol: 'triangle', radius: 10}, datatype: 'drugs'},")
            links.append("{from: '" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
        else:
            nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#910000', marker: {symbol: 'triangle', radius: 10}, datatype: 'drugs'},")
            links.append("{from: '" + str(row[0]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows1'] = rows1
    result['num1'] = num
    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'product_details.html', result)


def article_details(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    rows0 = []
    rows1 = []
    rows2 = []
    rows3 = []
    rows4 = []
    links = []
    nodes = []
    if request.GET.get('id') is not None:
        id = request.GET.get('id')
    else:
        return render(request, 'index.html')

    SQL = "SELECT * from Research_Articles where Article_ID=?"
    cursor.execute(SQL, (id, ))
    row = cursor.fetchone()
    rows0.append([row[0], row[1], row[2], row[3], row[4], row[5]])
    result['rows0'] = rows0
    nodes.append("{id: 'PMID" + str(row[1]).replace("'", "") + "', color:'#1aadce', marker: {symbol: 'triangle-down', radius: 20}, dataLabels: 'candidate'}, ")

    stragyids = []
    cursor1.execute("SELECT * from Therapy_Strategies")
    for row1 in cursor1:
        strategies = row1[1]
        if row1[2] is not None:
            strategies = strategies + "; " + row1[2]
        strategies = strategies.split('; ')
        for strategy in strategies:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Research articles' and class_id=?"
            cursor2.execute(SQL, ('%' + strategy + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    stragyids.append(row1[0])
    stragyids = list(set(stragyids))
    num = 0
    for stragyid in stragyids:
        num = num + 1
        SQL = "SELECT * from Therapy_Strategies where Strategy_ID=?"
        cursor2.execute(SQL, (stragyid,))
        row2 = cursor2.fetchone()
        rows1.append([row2[0], row2[1], row2[2], row2[3], row2[4]])
        nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#2f7ed8', marker: {symbol: 'circle', radius: 10}, datatype: 'strategies'},")
        links.append("{from: 'PMID" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows1'] = rows1
    result['num1'] = num

    targetids = []
    cursor1.execute("SELECT * from Therapy_Targets")
    for row1 in cursor1:
        targets = row1[1]
        if row1[2] is not None:
            targets = targets + "; " + row1[2]
        targets = targets.split('; ')
        for target in targets:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Research articles' and class_id=?"
            cursor2.execute(SQL, ('%' + target.replace("'", "") + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    targetids.append(row1[0])
    targetids = list(set(targetids))
    num = 0
    for targetid in targetids:
        num = num + 1
        SQL = "SELECT * from Therapy_Targets where Target_ID=?"
        cursor2.execute(SQL, (targetid,))
        row2 = cursor2.fetchone()
        rows2.append([row2[0], row2[1], row2[3], row2[4], row2[5], row2[7], row2[8]])
        nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#8bbc21', marker: {symbol: 'square', radius: 10}, datatype: 'targets'},")
        links.append("{from: 'PMID" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows2'] = rows2
    result['num2'] = num

    diseaseids = []
    cursor1.execute("SELECT * from Associated_Diseases")
    for row1 in cursor1:
        diseases = row1[2]
        if row1[4] is not None:
            diseases = diseases + "; " + row1[4]
        diseases = diseases.split('; ')
        for disease in diseases:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Research articles' and class_id=?"
            cursor2.execute(SQL, ('%' + disease.replace("'", "") + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    diseaseids.append(row1[0])
    diseaseids = list(set(diseaseids))
    num = 0
    for diseaseid in diseaseids:
        num = num + 1
        SQL = "SELECT * from Associated_Diseases where Disease_ID=?"
        cursor2.execute(SQL, (diseaseid,))
        row2 = cursor2.fetchone()
        rows3.append([row2[0], row2[1], row2[2], row2[3], row2[5]])
        nodes.append("{id: '" + str(row2[2]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#f28f43', marker: {symbol: 'triangle', radius: 10}, datatype: 'diseases'},")
        links.append("{from: 'PMID" + str(row[1]).replace("'", "") + "', to: '" + str(row2[2]).replace("'", "") + "'},")
    result['rows3'] = rows3
    result['num3'] = num

    drugids = []
    cursor1.execute("SELECT * from Drugs")
    for row1 in cursor1:
        drugs = row1[1]
        if row1[2] is not None:
            drugs = drugs + "; " + row1[2]
        drugs = drugs.split('; ')
        for drug in drugs:
            SQL = "SELECT count(distinct class_id) from NAFLDdb where knowledge_points like ? and class='Research articles' and class_id=?"
            cursor2.execute(SQL, ('%' + drug.replace("'", "") + '%', row[0]))
            for row2 in cursor2:
                if row2[0] > 0:
                    drugids.append(row1[0])
    drugids = list(set(drugids))
    num = 0
    for drugid in drugids:
        num = num + 1
        SQL = "SELECT * from Drugs where Drug_ID=?"
        cursor2.execute(SQL, (drugid,))
        row2 = cursor2.fetchone()
        rows4.append([row2[0], row2[1], row2[3], row2[4], row2[16], row2[17], row2[19]])
        nodes.append("{id: '" + str(row2[1]).replace("'", "") + "', cid:'"+str(row2[0])+"', color:'#77a1e5', marker: {symbol: 'diamond', radius: 10}, datatype: 'drugs'},")
        links.append("{from: 'PMID" + str(row[1]).replace("'", "") + "', to: '" + str(row2[1]).replace("'", "") + "'},")
    result['rows4'] = rows4
    result['num4'] = num

    links = '\n'.join(links)
    nodes = '\n'.join(nodes)
    result['nodes'] = nodes
    result['links'] = links
    return render(request, 'article_details.html', result)

