from django.http import HttpResponse, JsonResponse
from rdkit import Chem
import sqlite3
import os.path
import re, os
import time
import urllib
import multiprocessing as mp
#os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'

def get_message_from_pmid(pmid):
    requestURL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=text&rettype=abstract&id="+str(pmid)
    response = urllib.request.urlopen(requestURL, {}, 10)
    responseBody = response.read()
    return responseBody

def get_message_from_pmid_retry(pmid):
    for t in range(5):
        try:
            response = get_message_from_pmid(pmid).decode('utf-8','ignore')
            if len(response.strip())>100:
                return response.strip()
        except:
            pass
    return 'Error! Check your input'

def re_by_keyword(keys, abstract, nlp_type, key_id):
    del_keywords = ['same', 'FAs']
    result = set()
    for key in keys:
        key_ = '[ -,\.]('+key.replace('(', '\(').replace(')', '\)').replace('+', '\+').replace('*', '\*').replace('.', '\.').replace('?', '\?').replace('^', '\^').replace('$', '\$').replace('=', '\=').replace('|', '\|').replace('[', '\[').replace(']', '\]').replace('<', '\<').replace('>', '\>')+')[ \.,-]'
        pattern = re.compile(key_, re.IGNORECASE)
        res = pattern.findall(abstract)
        for i in res:
            if i not in del_keywords:
                result.add((nlp_type, key_id, i, key))
    return result

def article_decode(abstract):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    result = set()
    links = []
    nodes = []
    stragyids = []
    ### Therapy_Strategies
    cursor.execute("SELECT * from Therapy_Strategies")
    for row in cursor:
        strategies = str(row[1]).split('; ')+str(row[2]).split('; ') if row[2] is not None else str(row[1]).split('; ')
        result.update(re_by_keyword(strategies, abstract, 'strategy_details', row[0]))
        
    ### Therapy_Targets
    cursor.execute("SELECT * from Therapy_Targets")
    for row in cursor:
        targets = str(row[1]).split('; ')+str(row[2]).split('; ') if row[2] is not None else str(row[1]).split('; ')
        result.update(re_by_keyword(targets, abstract, 'target_details', row[0]))
        
    ### Associated_Diseases
    cursor.execute("SELECT * from Associated_Diseases")
    for row in cursor:
        diseases = str(row[2]).split('; ')+str(row[4]).split('; ') if row[4] is not None else str(row[2]).split('; ')
        result.update(re_by_keyword(diseases, abstract, 'disease_details', row[0]))
        
    ### Drugs
    cursor.execute("SELECT * from Drugs")
    for row in cursor:
        drugs = str(row[1]).split('; ')+str(row[2]).split('; ') if row[2] is not None else str(row[1]).split('; ')
        result.update(re_by_keyword(drugs, abstract, 'drug_details', row[0]))
        
    return result

def article_decode_mp(abstract, core=5):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DBfile = os.path.join(BASE_DIR, 'NAFLDdb.db')
    conn = sqlite3.connect(DBfile)
    cursor = conn.cursor()
    result = set()
    links = []
    nodes = []
    stragyids = []
    params_list = []
    pool = mp.Pool(processes=core)
    ### Therapy_Strategies
    cursor.execute("SELECT * from Therapy_Strategies")
    for row in cursor:
        strategies = str(row[1]).split('; ')+str(row[2]).split('; ') if row[2] is not None else str(row[1]).split('; ')
        params_list.append([strategies, abstract, 'strategy_details', row[0], ])
        #result.update(re_by_keyword(strategies, abstract, 'strategy_details', row[0]))
        
    ### Therapy_Targets
    cursor.execute("SELECT * from Therapy_Targets")
    for row in cursor:
        targets = str(row[1]).split('; ')+str(row[2]).split('; ') if row[2] is not None else str(row[1]).split('; ')
        params_list.append([targets, abstract, 'target_details', row[0], ])
        #result.update(re_by_keyword(targets, abstract, 'target_details', row[0]))
        
    ### Associated_Diseases
    cursor.execute("SELECT * from Associated_Diseases")
    for row in cursor:
        diseases = str(row[2]).split('; ')+str(row[4]).split('; ') if row[4] is not None else str(row[2]).split('; ')
        params_list.append([diseases, abstract, 'disease_details', row[0], ])
        #result.update(re_by_keyword(diseases, abstract, 'disease_details', row[0]))
        
    ### Drugs
    cursor.execute("SELECT * from Drugs")
    for row in cursor:
        drugs = str(row[1]).split('; ')+str(row[2]).split('; ') if row[2] is not None else str(row[1]).split('; ')
        params_list.append([drugs, abstract, 'drug_details', row[0], ])
        #result.update(re_by_keyword(drugs, abstract, 'drug_details', row[0]))
    mp_results = pool.starmap(re_by_keyword, params_list)
    for res in mp_results:
        result.update(res)
    return result

def article_style(abstract, keywords):
    new_abstract = abstract
    colors = {'strategy_details':'green', 'target_details':'red', 'disease_details':'blue', 'drug_details':'purple'}
    keywords = sorted(keywords, key=lambda x:len(x[2]), reverse=True)
    for ctype, id, map_term, raw_term in keywords:
        new_abstract = new_abstract.replace(raw_term, "<a href='/nafldkb/"+ctype+"?id="+str(id)+"' style='color:"+colors.get(ctype, 'gray')+"'>"+map_term+'</a>')
    return new_abstract

def annotation_search(request):
    result = {}
    input = ''
    if request.method == 'GET':
        input = request.GET['input']
    abstract = get_message_from_pmid_retry(input.strip())
    result['abstract'] = abstract
    keywords = article_decode(abstract)
    mapping = article_style(abstract, keywords)
    result['mapping'] = mapping
    return JsonResponse(result, safe=False)



