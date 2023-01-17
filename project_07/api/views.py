from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
import logging
from django.conf import settings
from django.core.files.storage import default_storage
from signlanguage.models import *
from django.db.models import Sum, Count
from django.db import connection

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"

    columns = [col[0] for col in cursor.description]
    result = cursor.fetchall()
    dict_result = {key:[] for key in columns}
    for row in result:
        tmp = zip(columns, row)
        for key, value in tmp:
            dict_result[key].append(value)

    # return [dict(zip(columns, row)) for row in cursor.fetchall()]
    return dict_result


def Procedure(name, *param):
    try:
        # close_old_connections()
        cursor = connection.cursor()
        str_param = ''
        for i, v in enumerate(param):
            str_param += "'" + v + "'"

            if i < (len(param)-1):
                str_param += ", "
        
        sql = f"CALL {name}({str_param});"
        cursor.execute(sql)
        result = dictfetchall(cursor)

    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()

    return True, result


def Sql(sql):
    try:
        # close_old_connections()
        cursor = connection.cursor()
        cursor.execute(sql)
        result = dictfetchall(cursor)

    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()

    return True, result

def chartAll(request):
    sql = '''
        SELECT r.model_id, a.model, a.version, count(a.id) as total, sum(predict) as collect, sum(predict)*100/count(a.id) as percent
        FROM signlanguage_result r, signlanguage_ai_model a 
        WHERE r.model_id = a.id
        GROUP BY r.model_id;
        '''
    r_bool, result = Sql(sql)
    message = ''
    
    if not r_bool:
        message = 'Failed mysql'
    else:
        message = 'Success mysql'

    jsonData = {
        'model_predict' : result
    }
    # print(jsonData)
    return JsonResponse(data=result, safe=True, status=200)