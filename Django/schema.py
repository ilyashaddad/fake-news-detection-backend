import graphene
import src.apps.scraping_news.schema
import src.apps.fake.schema


class Query(
    src.apps.scraping_news.schema.Query,
    graphene.ObjectType
    ):
    pass
   
class Mutation(
    src.apps.scraping_news.schema.Mutation,
    
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)