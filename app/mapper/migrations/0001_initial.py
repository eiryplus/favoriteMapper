# Generated by Django 3.0.7 on 2020-06-13 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Mapper",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="登録日"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="登録日")),
                (
                    "id",
                    models.CharField(
                        max_length=31,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Mapper ID",
                    ),
                ),
                (
                    "username",
                    models.CharField(max_length=255, null=True, verbose_name="ユーザー名"),
                ),
                (
                    "latest_uploaded",
                    models.DateTimeField(
                        db_index=True, null=True, verbose_name="最終アップロード日"
                    ),
                ),
                (
                    "latest_processed",
                    models.DateTimeField(
                        db_index=True, null=True, verbose_name="最終処理日"
                    ),
                ),
            ],
            options={"db_table": "mapper",},
        ),
        migrations.CreateModel(
            name="Map",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="登録日"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="登録日")),
                (
                    "id",
                    models.CharField(
                        max_length=7,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Map ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="曲名")),
                (
                    "uploaded",
                    models.DateTimeField(db_index=True, verbose_name="アップロード日"),
                ),
                ("duration", models.FloatField(default=0, verbose_name="曲の長さ")),
                ("origin", models.TextField(verbose_name="オリジナルデータ")),
                (
                    "mapper",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mapper.Mapper"
                    ),
                ),
            ],
            options={"db_table": "map",},
        ),
        migrations.CreateModel(
            name="Difficulty",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="登録日"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="登録日")),
                ("level", models.IntegerField(verbose_name="難易度")),
                ("notes_count", models.IntegerField(verbose_name="ノーツ数")),
                ("notes_per_sec", models.FloatField(verbose_name="NPS")),
                (
                    "distance_per_sec",
                    models.FloatField(default=0.0, verbose_name="セイバーの移動距離"),
                ),
                (
                    "map",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="mapper.Map"
                    ),
                ),
            ],
            options={"db_table": "difficulty",},
        ),
    ]
