from django.shortcuts import render
from django.views.decorators import csrf
from django.http import HttpResponse, JsonResponse
from rdkit import Chem
import sqlite3
import os.path
from rdkit import DataStructs
from rdkit.Chem import MACCSkeys
from rdkit.Chem import AllChem, Descriptors


def screen(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    result = {}
    rows = []
    mw = 0
    tpsa = 0
    hbd = 0
    hba = 0
    rbs = 0
    alogp = 0
    ant = 0
    qed = 0
    numall = 0
    field = ''
    num = 0
    if request.method == 'GET':
        field = request.GET['fd']
        mw = request.GET['mw']
        tpsa = request.GET['tpsa']
        hbd = request.GET['hbd']
        hba = request.GET['hba']
        rbs = request.GET['rbs']
        alogp = request.GET['alogp']
        ant = request.GET['ant']
        qed = request.GET['qed']
        numall = int(request.GET['screennum'])
        if mw == '0':
            c_mw = '[Molecular Weight] <=200'
        elif mw == '200':
            c_mw = '[Molecular Weight]>200 and [Molecular Weight]<=500'
        elif mw == '500':
            c_mw = '[Molecular Weight]>500 and [Molecular Weight]<=800'
        elif mw == '800':
            c_mw = '[Molecular Weight]>800 and [Molecular Weight]<=1000'
        elif mw == '1000':
            c_mw = '[Molecular Weight]>1000'

        if tpsa == '0':
            c_tpsa = '[Polar Surface Area]<=25'
        elif tpsa == '25':
            c_tpsa = '[Polar Surface Area]>25 and [Polar Surface Area]<=50'
        elif tpsa == '50':
            c_tpsa = '[Polar Surface Area]>50 and [Polar Surface Area]<=75'
        elif tpsa == '75':
            c_tpsa = '[Polar Surface Area]>75 and [Polar Surface Area]<=100'
        elif tpsa == '100':
            c_tpsa = '[Polar Surface Area]>100'

        if hbd == '0':
            c_hbd = '[HBD]=0'
        elif hbd == '1':
            c_hbd = '[HBD]>=1 and [HBD]<=5'
        elif hbd == '6':
            c_hbd = '[HBD]>5 and [HBD]<=10'
        elif hbd == '10':
            c_hbd = '[HBD]>10'

        if hba == '0':
            c_hba = '[HBA]=0'
        elif hba == '1':
            c_hba = '[HBA]>=1 and [HBA]<=5'
        elif hba == '6':
            c_hba = '[HBA]>5 and [HBA]<=10'
        elif hba == '10':
            c_hba = '[HBA]>10'

        if rbs == '0':
            c_rbs = '[#Rotatable Bonds]=0'
        elif rbs == '1':
            c_rbs = '[#Rotatable Bonds]>=1 and [#Rotatable Bonds]<=5'
        elif rbs == '6':
            c_rbs = '[#Rotatable Bonds]>5 and [#Rotatable Bonds]<=10'
        elif rbs == '10':
            c_rbs = '[#Rotatable Bonds]>10'

        if alogp == '0':
            c_alogp = '[AlogP]<=0'
        elif alogp == '2':
            c_alogp = '[AlogP]>0 and [AlogP]<=2'
        elif alogp == '4':
            c_alogp = '[AlogP]>2 and [AlogP]<=4'
        elif alogp == '5':
            c_alogp = '[AlogP]>4 and [AlogP]<=5'
        elif alogp == '6':
            c_alogp = '[AlogP]>5'

    if field == 'Bioactive Compounds':
        SQL = "SELECT * from Bioactive_Compounds where "
        SQL = SQL + c_mw + " and " + c_tpsa + " and " + c_hbd + " and " + c_hba + " and " + c_rbs + " and " + c_alogp + " and " + ant + " and [QED Weighted]>=" + qed
        cursor.execute(SQL, )
        for row in cursor:
            rows.append([row[0], row[1], row[4], row[2], row[5], row[6], row[32]])
            num = num + 1
            if num > numall:
                break
        result['rows'] = rows
        result['num'] = num
    elif field == 'Natural Products':
        SQL = "SELECT * from Natural_Products where "
        SQL = SQL + c_mw.replace("Molecular Weight", "MW") + " and " + c_tpsa.replace("Polar Surface Area", "TPSA") + " and " + c_hbd + " and " + c_hba + " and " + c_rbs.replace("#Rotatable Bonds", "RB") + " and " + c_alogp + " and " + ant.replace("NAFLDTargets", "NAFLDTherapies") + " and [QED]>=" + qed
        cursor.execute(SQL, )
        for row in cursor:
            rows.append([row[0], row[1], row[2], row[6], row[7], row[10]])
            num = num + 1
            if num > numall:
                break
        result['rows'] = rows
        result['num'] = num
    return JsonResponse(result)

