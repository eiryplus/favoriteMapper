import os
import json
import requests
import zipfile

from django.db import models
from common.models import ModelBase
from mapper import consts


# https://beatsaver.com/api/users/find/5cff0b7598cc5a672c851d38
# {"_id":"5cff0b7598cc5a672c851d38","username":"coolingcloset"}
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
        except:
            os.rmdir(self.extract_path)


class Difficulty(ModelBase):
    map = models.ForeignKey(Map, on_delete=models.CASCADE, db_index=True)
    level = models.IntegerField("難易度")
    notes_count = models.IntegerField("ノーツ数")
    notes_per_sec = models.FloatField("NPS", 0.0)
    distance_per_sec = models.FloatField("セイバーの移動距離", default=0.0)

    class Meta:
        db_table = "difficulty"
