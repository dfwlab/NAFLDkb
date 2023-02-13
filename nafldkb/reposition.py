from django.http import HttpResponse, JsonResponse
from rdkit import Chem
import sqlite3
import os.path


def getnodename(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    rows0 = []
    num = 0
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    result = {}
    if request.method == 'GET':
        type = request.GET['type']
    if type == "targets":
        SQL = "SELECT * from Therapy_Targets order by Target_Name"
        cursor1.execute(SQL, )
        for row1 in cursor1:
            rows0.append([row1[0], row1[1]])
            num = num + 1
    elif type == "strategies":
        SQL = "SELECT * from Therapy_Strategies order by Therapy_Strategy"
        cursor1.execute(SQL, )
        for row1 in cursor1:
            rows0.append([row1[0], row1[1]])
            num = num + 1
    elif type == "indication":
        SQL = "SELECT * from Associated_Diseases order by Disease_Name"
        cursor1.execute(SQL, )
        for row1 in cursor1:
            rows0.append([row1[0], row1[2]])
            num = num + 1
    result['rows0'] = rows0
    result['num'] = num
    return JsonResponse(result)

def reposition(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    rows0 = []
    drug_type = ""
    targets = ""
    sql = ""
    strategies = ""
    indication = ""
    num = 0
    links1 = []
    links2 = []
    links3 = []
    links = []
    nodes = []
    cursor = conn.cursor()
    cursor2 = conn.cursor()
    result = {}
    if request.method == 'GET':
        drug_type = request.GET['type']
        targets = request.GET['targets']
        strategies = request.GET['strategies']
        indication = request.GET['indication']
    if targets != "":
        target_ids = targets.split(";")
        target_ids = list(set(target_ids))
        for target_id in target_ids:
            if sql == "":
                sql = "SELECT * from DrugBank where NAFLD_links like '%1-" + target_id + ";%'"
            else:
                sql = sql + " and NAFLD_links like '%1-" + target_id + ";%'"
            SQL = "SELECT * from Therapy_Targets where Target_ID=?"
            cursor2.execute(SQL, (target_id,))
            row2 = cursor2.fetchone()
            nodes.append({"id":  str(row2[1]).replace("'", ""), "cid": str(row2[0]), "color": '#8bbc21', "marker": {"symbol": 'square', "radius": 10}, "datatype": 'targets'})
            links1.append(str(row2[1]).replace("'", ""))
    if strategies != "":
        strategy_ids = strategies.split(";")
        strategy_ids = list(set(strategy_ids))
        for strategy_id in strategy_ids:
            if sql == "":
                sql = "SELECT * from DrugBank where NAFLD_links like '%2-" + strategy_id + ";%'"
            else:
                sql = sql + " and NAFLD_links like '%2-" + strategy_id + ";%'"
            SQL = "SELECT * from Therapy_Strategies where Strategy_ID=?"
            cursor2.execute(SQL, (strategy_id,))
            row2 = cursor2.fetchone()
            nodes.append({"id": str(row2[1]).replace("'", ""), "cid": str(row2[0]), "color": '#2f7ed8', "marker": {"symbol": 'circle', "radius": 10}, "datatype": 'strategies'})
            links2.append(str(row2[1]).replace("'", ""))
    if indication != "":
        indication_ids = indication.split(";")
        indication_ids = list(set(indication_ids))
        for indication_id in indication_ids:
            if sql == "":
                sql = "SELECT * from DrugBank where NAFLD_links like '%3-" + indication_id + ";%'"
            else:
                sql = sql + " and NAFLD_links like '%3-" + indication_id + ";%'"
            SQL = "SELECT * from Associated_Diseases where Disease_ID=?"
            cursor2.execute(SQL, (indication_id,))
            row2 = cursor2.fetchone()
            nodes.append({"id": str(row2[2]).replace("'", ""), "cid": str(row2[0]), "color": '#f28f43', "marker": {"symbol": 'triangle', "radius": 10}, "datatype": 'diseases'})
            links3.append(str(row2[2]).replace("'", ""))
    if drug_type != "all":
        sql = sql + " and groups like '%" + drug_type + "%'"
    cursor.execute(sql, )
    for row1 in cursor:
        candidate_id = None
        if row1[2] is None:
            cursor2.execute("select Candidate_ID from Candidates where Source_ID=?", (row1[1], ))
            for row2 in cursor2:
                candidate_id = row2[0]
        rows0.append([row1[1], row1[3], row1[4], row1[6], row1[10], row1[2], candidate_id])
        num = num + 1
        nodes.append({"id": str(row1[4]), "cid": str(candidate_id), "did": str(row1[2]), "color": '#1aadce', "marker": {"symbol": 'triangle-down', "radius": 10}, "datatype": 'candidates'})
        for i in links1:
            links.append({"from": i, "to": str(row1[4]).replace("'", "")})
        for i in links2:
            links.append({"from": i, "to": str(row1[4]).replace("'", "")})
        for i in links3:
            links.append({"from": i, "to": str(row1[4]).replace("'", "")})
    result['rows'] = rows0
    result['num'] = num
    result['nodes'] = nodes
    if num > 0:
        result['links'] = links
    return JsonResponse(result, safe=False)


