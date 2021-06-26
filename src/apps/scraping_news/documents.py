from django_elasticsearch_dsl import (
    Document ,
    fields,
    Index,
)
from django_elasticsearch_dsl.registries import registry 

from .models import News_s
news = Index('news')

news.settings(
    number_of_shards=1,
    number_of_replicas=1
)

@news.doc_type
class NewsDocument(Document):
    class Django:
        model = News_s
        fields= ['title','resume','description','image','date','thematic','fake_flag']