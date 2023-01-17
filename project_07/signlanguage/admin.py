from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Result, AI_model
from django.db import connection
# Register your models here.


# 관리에서 Result 객체에 대해  기본 CRUD 관리를 한다. 
admin.site.register(Result)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"

    columns = [col[0] for col in cursor.description]
    result = cursor.fetchall()
    dict_result = {key:[] for key in columns}
    for row in result:
        tmp = zip(columns, row)
        for key, value in tmp:
            dict_result[key].append(value)

    return dict_result

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

@admin.register(AI_model)
class AI_modelAdmin(admin.ModelAdmin):
    list_display = ("id", "model", "version", "use_type") # display these table columns in the list view
    ordering = ("-pub_date",)

    def changelist_view(self, request, extra_context=None):
        sql = '''
        SELECT r.model_id, a.model, a.version, a.total_cnt, a.predict_cnt, a.predict_cnt*100/a.total_cnt as percent
        FROM signlanguage_result r, signlanguage_ai_model a 
        WHERE r.model_id = a.id
        GROUP BY r.model_id;
        '''
        r_bool, result = Sql(sql)
        print(result)
        as_json = json.dumps(list(result), cls=DjangoJSONEncoder)
        extra_context = {"chart_data": result}
        print(as_json)

        return super().changelist_view(request, extra_context=extra_context)