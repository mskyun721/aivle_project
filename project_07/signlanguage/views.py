from django.shortcuts import render
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
import numpy as np
import cv2
import string
from keras.models import load_model
from django.db import connection
import joblib
import pickle
import xgboost as xgb


# from pybo.model import Result
from .models import *
import os

# Create your views here.

logger = logging.getLogger('mylogger')

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

def index(request):
    
    return render(request, 'language/index.html')

def chart(request):
    sql = '''
        SELECT r.model_id, a.model, a.version, count(a.id) as total, sum(predict) as collect, sum(predict)*100/count(a.id) as percent
        FROM signlanguage_result r, signlanguage_ai_model a 
        WHERE r.model_id = a.id
        GROUP BY r.model_id;
        '''
    r_bool, result = Sql(sql)
    print(f'result : {result}')
    return render(request, 'language/model_chart.html', result)

def upload(request):
    if request.method == 'POST' and request.FILES['files']:

        list_file = request.FILES.getlist('files')
        list_answer = request.POST.getlist('answer')

        ai_model = AI_model.objects.get(use_type=True)
        model_path = ai_model.model.path
        
        if model_path[-3:] == 'pkl':
            model = joblib.load(model_path)

            context_result = []
            for i in range(len(list_file)):
                #form?????? ????????? ????????? ????????????. 
                file = list_file[i]
                # logger.error('file', file)
                # class names ??????
                class_names = list(string.ascii_lowercase)
                class_names = np.array(class_names)

                # history ????????? ?????? ????????? ????????? DB??? ????????????.
                # ?????? ?????????????????? ????????? ??????.
                result = Result()
                result.answer = list_answer[i]
                result.image = file
                result.pub_date = timezone.datetime.now()
                
                result.save()


                # ???????????? ??????
                img = cv2.imread(result.image.path, cv2.IMREAD_GRAYSCALE)

                # ?????? ??????
                img = cv2.resize(img, (28, 28))
                
                img = img.flatten()
                
                test_sign = img.reshape((1, img.shape[0]))
                
                pred = model.predict(test_sign)
                
                #????????? DB??? ????????????.
                result.result = class_names[int(pred)]
                result.model = ai_model
                
                # ?????? ?????? ??????
                ai_model.total_cnt += 1
                if result.result == result.answer:
                    ai_model.predict_cnt += 1

                result.save()
                
                context_result.append(result)      
        
        else:
            model = load_model(model_path)

            context_result = []
            for i in range(len(list_file)):
                #form?????? ????????? ????????? ????????????. 
                file = list_file[i]
                # logger.error('file', file)
                # class names ??????
                class_names = list(string.ascii_lowercase)
                class_names = np.array(class_names)

                # history ????????? ?????? ????????? ????????? DB??? ????????????.
                # ?????? ?????????????????? ????????? ??????.
                result = Result()
                result.answer = list_answer[i]
                result.image = file
                result.pub_date = timezone.datetime.now()
                
                result.save()


                # ???????????? ??????
                img = cv2.imread(result.image.path, cv2.IMREAD_GRAYSCALE)

                # ?????? ??????
                img = cv2.resize(img, (28, 28))

                # input shape ?????????
                test_sign = img.reshape(1, 28, 28, 1)

                # ????????????
                test_sign = test_sign / 255.

                # ?????? : ?????? ??? ????????? ?????? ?????? ?????? ?????? ??????.
                pred = model.predict(test_sign)
                pred_1 = pred.argmax(axis=1)


                #????????? DB??? ????????????.
                result.result = class_names[pred_1][0]
                result.model = ai_model
                
                # ?????? ?????? ??????
                ai_model.total_cnt += 1
                if result.result == result.answer:
                    ai_model.predict_cnt += 1

                result.save()
                
                context_result.append(result)

        ai_model.save()
        context = {
            'result': context_result,
        }


    # http method??? GET??? ???????????? ?????????. ????????? ?????????????????? ?????????
    else:
        test = request.GET['test']
        logger.error(('Something went wrong!!',test))

    return render(request, 'language/result.html', context)    

