import graphene
from graphene import Node
from graphene.types import field
from graphene_django import DjangoObjectType
from graphene_elastic import (
    ElasticsearchObjectType,
    ElasticsearchConnectionField,
)
from graphene_elastic.filter_backends import FilteringFilterBackend, SearchFilterBackend
from graphene_elastic.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_TERM,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_IN,
)

from .documents import NewsDocument

from .models import News_s, Nlp
from .nlp import *
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

class News_sType(DjangoObjectType):
    class Meta:
        model = News_s
        field = "__all__"


class New_sTypeSearch(ElasticsearchObjectType):
    class Meta:
        document = NewsDocument
        interfaces = (Node,)
        filter_backends = [
            FilteringFilterBackend,
            SearchFilterBackend,
        ]
        filter_fields = {
            "title": {
                "field": "title.raw",
                "lookups": [
                    LOOKUP_FILTER_TERM,
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
                "default_lookup": LOOKUP_FILTER_TERM,
            },
            "description": "description.raw",
        }
        search_fields = {
            "title": {"boost": 4},
            "description": {"boost": 2},
        }
        ordering_fields = {
            "id": None,
            "title": "title.raw",
            "description": "description.raw",
        }


class Query(object):
    allnews = graphene.List(News_sType)
    new = graphene.Field(News_sType, new_id=graphene.Int())
    all_post_documents = ElasticsearchConnectionField(New_sTypeSearch)

    def resolve_allnews(self, info, **kwargs):
        return News_s.objects.all()

    def resolve_new(self, info, new_id):
        return News_s.objects.get(pk=new_id)


# class CheckNewsInput(graphene.InputObjectType):
#     title = graphene.String()
#     fake_flag = graphene.Int()


class CheckNews(graphene.Mutation):
    class Arguments:
        title = graphene.String()

    news = graphene.Field(News_sType)

    @staticmethod
    def mutate(root, info, title=None):
        new = News_s(title=title)
        print(new.title)
        return CheckNews(news=new)


class NlpType(DjangoObjectType):
    class Meta:
        model = Nlp
        field = "__all__"


class NlpMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        method = graphene.String()

    nlp_process = graphene.Field(NlpType)

    @staticmethod
    def mutate(root, info, title=None, method=None):
        nlp = Nlp(title=title, method=method)
        if method == "Tokenization":
            result = tokenize(title)
        if method == "Stop words":
            result = stopword(title)
        if method == "Lemmatization":
            result = lemmatize(title)
        if method == "Stemming":
            result = stem(title)
        if method == "Pos Tagging":
            result = postag(title)
        if method == "Bag of words":
            result = bagofwords(title)
        # if method == "TF-IDF":
        #     result = tfidf(title)
        # if method == "Word2Vec":
        #     pass
        nlp = Nlp(title=title, method=method, result=result)
        return NlpMutation(nlp_process=nlp)


class NewsDetection(graphene.Mutation):
    class Arguments:
        title = graphene.String()
    result_check  = graphene.Field(NlpType)
    @staticmethod
    def mutate(root, info, title=None):
        
        pred = news_model.predict(word_vect.transform([title]))
        prediction=pd.DataFrame(pred, columns=['fake_flag']) 
        if prediction['fake_flag']==0:
            res= "fake"
        else :
            res = "Not fake"
        check_new = Nlp(title=title,result=res)
        return NewsDetection(result_check= check_new)


class Mutation(graphene.ObjectType):
    CheckNews = CheckNews.Field()
    nlp_mutation = NlpMutation.Field()
    newsDetection = NewsDetection.Field()


