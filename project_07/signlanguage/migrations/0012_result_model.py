# Generated by Django 4.1.3 on 2022-11-23 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("signlanguage", "0011_remove_result_model_ai_model_predict_cnt_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="model",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="signlanguage.ai_model",
            ),
        ),
    ]
