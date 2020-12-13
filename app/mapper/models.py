import os
import json
import requests
import zipfile

from django.db import models
from django.utils.functional import cached_property
import pygame

from common.models import ModelBase
from mapper import consts

pygame.mixer.init()


class Mapper(ModelBase):
    # 取り込みデータ
    id = models.CharField(verbose_name="Mapper ID", max_length=31, primary_key=True)
    username = models.CharField(
        verbose_name="ユーザー名", max_length=255, null=True
    )  # 後で自動取得
    latest_uploaded = models.DateTimeField(
        verbose_name="最終アップロード日", db_index=True, null=True
    )
    # 内部処理用
    latest_processed = models.DateTimeField(
        verbose_name="最終処理日", db_index=True, null=True
    )

    class Meta:
        db_table = "mapper"

    def update_latest_uploaded(self):
        aggregated = self.map_set.aggregate(models.Max("uploaded"))
        self.latest_uploaded = aggregated.get("uploaded__max")
        self.save()


class Map(ModelBase):
    id = models.CharField(verbose_name="Map ID", max_length=7, primary_key=True)
    name = models.CharField(verbose_name="曲名", max_length=255)
    uploaded = models.DateTimeField(verbose_name="アップロード日", db_index=True)
    duration = models.FloatField(verbose_name="曲の長さ", default=0)
    origin = models.TextField(verbose_name="オリジナルデータ")
    downloaded = models.BooleanField("ダウンロード完了フラグ", default=False)

    mapper = models.ForeignKey(Mapper, on_delete=models.CASCADE)

    class Meta:
        db_table = "map"

    @property
    def display_duration(self):
        return "{}:{}".format(int(self.duration / 60), int(self.duration) % 60)

    @property
    def download_file_path(self):
        return os.path.join(consts.DOWNLOAD_DIR, self.id + ".zip")

    @property
    def extract_path(self):
        return os.path.join(consts.EXTRACT_DIR, self.id)

    @property
    def origin_data(self):
        return json.loads(self.origin)

    @property
    def download_url(self):
        return consts.BASE_URL + self.origin_data.get("directDownload")

    @cached_property
    def info_dat(self):
        info_path = os.path.join(self.extract_path, "info.dat")
        if not os.path.isfile(info_path):
            return
        with open(info_path, "r", encoding="utf-8") as fp:
            dat = json.load(fp)
        return dat

    @cached_property
    def music_file_duration(self):
        sonf_file = os.path.join(self.extract_path, self.info_dat.get("_songFilename"))
        sc = pygame.mixer.Sound(sonf_file)
        return sc.get_length()

    def download(self):
        if self.downloaded:
            return
        response = requests.get(self.download_url, headers=consts.headers)
        with open(self.download_file_path, "wb") as fp:
            fp.write(response.content)
        self.downloaded = True
        self.save()

    def extract_zip(self):
        if not os.path.isfile(self.download_file_path):
            raise FileNotFoundError()
        if os.path.isdir(self.extract_path):
            return
        try:
            os.makedirs(self.extract_path, 755, exist_ok=True)
            with zipfile.ZipFile(self.download_file_path) as fp:
                fp.extractall(self.extract_path)
        except zipfile.BadZipFile as e:
            os.rmdir(self.extract_path)
            raise e


DIFFICULTY_CHOICES = (
    (0, "Easy"),
    (1, "Normal"),
    (2, "Hard"),
    (3, "Expert"),
    (4, "ExpertPlus"),
)
DIFFICULTY_DICT = {t[1]: t[0] for t in DIFFICULTY_CHOICES}


class Difficulty(ModelBase):
    map = models.ForeignKey(Map, on_delete=models.CASCADE, db_index=True)
    code = models.IntegerField("難易度", choices=DIFFICULTY_CHOICES)
    notes_count = models.IntegerField("ノーツ数")
    notes_per_sec = models.FloatField("NPS", default=0.0)
    speed = models.IntegerField(verbose_name="スピード")
    obstacles = models.IntegerField(verbose_name="壁の数")
    bombs = models.IntegerField(verbose_name="ボムの数")
    distance_per_sec = models.FloatField("セイバーの移動距離", default=0.0)

    class Meta:
        db_table = "difficulty"
