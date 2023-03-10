# Generated by Django 4.1.3 on 2022-11-22 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("signlanguage", "0009_ai_model_predict_cnt_ai_model_total_cnt_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="ai_model", name="predict_cnt",),
        migrations.RemoveField(model_name="ai_model", name="total_cnt",),
        migrations.AddField(
            model_name="result",
            name="model",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="signlanguage.ai_model",
            ),
        ),
        migrations.AddField(
            model_name="result",
            name="predict",
            field=models.BooleanField(default=True),
        ),
    ]
