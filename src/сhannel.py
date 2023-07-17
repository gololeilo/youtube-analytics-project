from googleapiclient.discovery import build
import json
import os


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        id канала
        название канала
        описание канала
        ссылка на канал
        количество подписчиков
        количество видео
        общее количество просмотров"""
        self._channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscribers_count = None
        self.video_count = None
        self.view_count = None
        self._get_channel_info()

    def __str__(self):
        """
        метод для возвращения в строковом варианте название канала
        и ссылки на него по указанному шаблону
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        магический метод для сложения  (в данном случие по числу подписчиков)
        """
        return int(self.subscribers_count) + int(other.subscribers_count)

    def __sub__(self, other):
        """
        магический метод для вычитания (в данном случие по числу подписчиков)
        """
        return int(self.subscribers_count) - int(other.subscribers_count)

    def __gt__(self, other):
        """
        магический метод для сравнения по параметру больше/меньше
        """
        return int(self.subscribers_count) > int(other.subscribers_count)

    def __ge__(self, other):
        """
        магический метод для сравнения по параметру больше или равно/меньше или равно
        """
        return int(self.subscribers_count) >= int(other.subscribers_count)

    @property
    def channel_id(self):
        """
        метод, делающий свойство channel_id доступным только для чтения
        """
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value):
        """
        метод для генерации исключения и получения ожидаемого поведения от main.py
        @param value:
        @return:
        """
        return AttributeError

    @classmethod
    def get_service(cls):
        """
        метод для получения объекта с работой API вне класса
        """
        api_key = os.environ.get('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube  # <googleapiclient.discovery.Resource object at 0x000001FD9EC38510>

    def _get_channel_info(self):
        """
        метод приватный и используется только внутри класса для получения инфы
        """
        youtube = self.get_service()
        channel = youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()  # запрос к API и получение данных в json-подобном формате

        channel_info = channel['items'][0]['snippet']  # для хранения общей инфы о канале
        statistics = channel['items'][0]['statistics']  # для хранения статистической инфы

        self.title = channel_info['title']
        self.description = channel_info['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscribers_count = statistics['subscriberCount']
        self.video_count = statistics['videoCount']
        self.view_count = statistics['viewCount']

    def to_json(self, file_name):
        """
        метод, сохраняющий в файл значения атрибутов экземпляра Channel
        """
        data = {'id': self.channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscribers_count': self.subscribers_count,
                'video_count': self.video_count,
                'view_count': self.view_count,
                }
        with open(file_name, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)  # для корректного вывода в json-формате
