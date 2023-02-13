from django.shortcuts import render
from django.views.decorators import csrf
from django.http import HttpResponse, JsonResponse
from rdkit import Chem
import sqlite3
import os.path
from rdkit import DataStructs
from rdkit.Chem import MACCSkeys
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem.Pharm2D import Gobbi_Pharm2D, Generate

def search(request):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    result = {}
    rows = []
    smi = ''
    type = ''
    num = 0
    field = ''
    similarity = 0.01
    if request.method == 'GET':
        smi = request.GET['smi']
        type = request.GET['type']
        field = request.GET['fd']
    m = Chem.MolFromSmiles(smi)
    mw = Descriptors.MolWt(m)
    InchiKey = Chem.MolToInchiKey(m)
    if field == 'NAFLD Therapy Agents':
        if type == 'exact':
            SQL = "SELECT * from Drugs where InchiKey=?"
            cursor.execute(SQL, (InchiKey,))
            for row in cursor:
                rows.append([row[0], row[1], row[3], row[4], row[16], row[17], row[19]])
                num = num + 1
                if num > 100:
                    break
            result['rows'] = rows
            result['num'] = num
        elif type == 'substructure':
            SQL = "SELECT * from Drugs where SMILES is not null"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[9])
                    if m1.HasSubstructMatch(m):
                        rows.append([row[0], row[1], row[3], row[4], row[16], row[17], row[19]])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
        elif type == 'similarity':
            fp = request.GET['fp']
            mt = request.GET['mt']
            si = float(request.GET['si'])
            if fp == 'MACCS Keys':
                f = MACCSkeys.GenMACCSKeys(m)
            elif fp == 'Morgan Fingerprints':
                f = AllChem.GetMorganFingerprint(m, 2)
            else:
                f = Chem.RDKFingerprint(m)
            SQL = "SELECT * from Drugs where SMILES is not null"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[9])
                    if fp == 'MACCS Keys':
                        f1 = MACCSkeys.GenMACCSKeys(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    elif fp == 'Morgan Fingerprints':
                        f1 = AllChem.GetMorganFingerprint(m1, 2)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    else:
                        f1 = Chem.RDKFingerprint(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    similarity = round(similarity, 2)
                    if similarity >= si:
                        rows.append([row[0], row[1], row[3], row[4], row[16], row[17], row[19], similarity])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
    elif field == 'Drug Candidates':
        if type == 'exact':
            SQL = "SELECT * from Candidates where InchiKey=?"
            cursor.execute(SQL, (InchiKey,))
            for row in cursor:
                rows.append([row[0], row[1], row[2], row[3], row[4], row[15]])
                num = num + 1
                if num > 100:
                    break
            result['rows'] = rows
            result['num'] = num
        elif type == 'substructure':
            SQL = "SELECT * from Candidates where SMILES is not null"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[7])
                    if m1.HasSubstructMatch(m):
                        rows.append([row[0], row[1], row[2], row[3], row[4], row[15]])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
        elif type == 'similarity':
            fp = request.GET['fp']
            mt = request.GET['mt']
            si = float(request.GET['si'])
            if fp == 'MACCS Keys':
                f = MACCSkeys.GenMACCSKeys(m)
            elif fp == 'Morgan Fingerprints':
                f = AllChem.GetMorganFingerprint(m, 2)
            else:
                f = Chem.RDKFingerprint(m)
            SQL = "SELECT * from Candidates where SMILES is not null"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[7])
                    if fp == 'MACCS Keys':
                        f1 = MACCSkeys.GenMACCSKeys(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    elif fp == 'Morgan Fingerprints':
                        f1 = AllChem.GetMorganFingerprint(m1, 2)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    else:
                        f1 = Chem.RDKFingerprint(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    similarity = round(similarity, 2)
                    if similarity >= si:
                        rows.append([row[0], row[1], row[2], row[3], row[4], row[15], similarity])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
    elif field == 'Bioactive Compounds':
        if type == 'exact':
            SQL = "SELECT * from Bioactive_Compounds where InchiKey=?"
            cursor.execute(SQL, (InchiKey,))
            for row in cursor:
                rows.append([row[0], row[1], row[4], row[2], row[5], row[6], row[32]])
                num = num + 1
                if num > 100:
                    break
            result['rows'] = rows
            result['num'] = num
        elif type == 'substructure':
            SQL = "SELECT * from Bioactive_Compounds where SMILES is not null and type='Small molecule'"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[7])
                    if m1.HasSubstructMatch(m):
                        rows.append([row[0], row[1], row[4], row[2], row[5], row[6], row[32]])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
        elif type == 'similarity':
            fp = request.GET['fp']
            mt = request.GET['mt']
            si = float(request.GET['si'])
            if fp == 'MACCS Keys':
                f = MACCSkeys.GenMACCSKeys(m)
            elif fp == 'Morgan Fingerprints':
                f = AllChem.GetMorganFingerprint(m, 2)
            else:
                f = Chem.RDKFingerprint(m)
            if mw <= 100:
                sql1 = " and [Molecular Weight]<150 and [Molecular Weight]>10"
            else:
                sql1 = " and [Molecular Weight]<" + str(mw+100) + " and [Molecular Weight]>" + str(mw-100)
            SQL = "SELECT * from Bioactive_Compounds where SMILES is not null and type='Small molecule'" +sql1
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[7])
                    if fp == 'MACCS Keys':
                        f1 = MACCSkeys.GenMACCSKeys(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    elif fp == 'Morgan Fingerprints':
                        f1 = AllChem.GetMorganFingerprint(m1, 2)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    else:
                        f1 = Chem.RDKFingerprint(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    similarity = round(similarity, 2)
                    if similarity >= si:
                        rows.append([row[0], row[1], row[4], row[2], row[5], row[6], row[32], similarity])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
    elif field == 'CMap Candidates':
        if type == 'exact':
            SQL = "SELECT * from CMap where inchi_key=?"
            cursor.execute(SQL, (InchiKey,))
            for row in cursor:
                rows.append([row[0], row[1], row[2], row[3], row[4], row[7]])
                num = num + 1
                if num > 100:
                    break
            result['rows'] = rows
            result['num'] = num
        elif type == 'substructure':
            SQL = "SELECT * from CMap where canonical_smiles is not null"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[5])
                    if m1.HasSubstructMatch(m):
                        rows.append([row[0], row[1], row[2], row[3], row[4], row[7]])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
        elif type == 'similarity':
            fp = request.GET['fp']
            mt = request.GET['mt']
            si = float(request.GET['si'])
            if fp == 'MACCS Keys':
                f = MACCSkeys.GenMACCSKeys(m)
            elif fp == 'Morgan Fingerprints':
                f = AllChem.GetMorganFingerprint(m, 2)
            else:
                f = Chem.RDKFingerprint(m)
            SQL = "SELECT * from CMap where canonical_smiles is not null"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[5])
                    if fp == 'MACCS Keys':
                        f1 = MACCSkeys.GenMACCSKeys(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    elif fp == 'Morgan Fingerprints':
                        f1 = AllChem.GetMorganFingerprint(m1, 2)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    else:
                        f1 = Chem.RDKFingerprint(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    similarity = round(similarity, 2)
                    if similarity >= si:
                        rows.append([row[0], row[1], row[2], row[3], row[4], row[7], similarity])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
    elif field == 'Natural Products':
        if type == 'exact':
            SQL = "SELECT * from Natural_Products where InchiKey=?"
            cursor.execute(SQL, (InchiKey,))
            for row in cursor:
                rows.append([row[0], row[1], row[2], row[6], row[7], row[10]])
                num = num + 1
                if num > 100:
                    break
            result['rows'] = rows
            result['num'] = num
        elif type == 'substructure':
            SQL = "SELECT * from Natural_Products where SMI is not null"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[4])
                    if m1.HasSubstructMatch(m):
                        rows.append([row[0], row[1], row[2], row[6], row[7], row[10]])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
        elif type == 'similarity':
            fp = request.GET['fp']
            mt = request.GET['mt']
            si = float(request.GET['si'])
            if fp == 'MACCS Keys':
                f = MACCSkeys.GenMACCSKeys(m)
            elif fp == 'Morgan Fingerprints':
                f = AllChem.GetMorganFingerprint(m, 2)
            else:
                f = Chem.RDKFingerprint(m)
            SQL = "SELECT * from Natural_Products where SMI is not null"
            cursor.execute(SQL)
            for row in cursor:
                try:
                    m1 = Chem.MolFromSmiles(row[4])
                    if fp == 'MACCS Keys':
                        f1 = MACCSkeys.GenMACCSKeys(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    elif fp == 'Morgan Fingerprints':
                        f1 = AllChem.GetMorganFingerprint(m1, 2)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    else:
                        f1 = Chem.RDKFingerprint(m1)
                        if mt == 'Tanimoto Similarity':
                            similarity = DataStructs.FingerprintSimilarity(f, f1)
                        else:
                            similarity = DataStructs.DiceSimilarity(f, f1)
                    similarity = round(similarity, 2)
                    if similarity >= si:
                        rows.append([row[0], row[1], row[2], row[6], row[7], row[10], similarity])
                        num = num + 1
                        if num > 100:
                            break
                except:
                    pass
                result['rows'] = rows
                result['num'] = num
    return JsonResponse(result)

