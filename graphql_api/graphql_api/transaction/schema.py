from datetime import datetime
import graphene
from graphql_api.transaction.models import Transaction
from graphene import Node
from graphene_django.types import DjangoObjectType
from .repository import transform
from django.db.models import Sum, DateField, DateTimeField, F
from django.db.models.functions import Trunc, TruncMonth
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import JsonResponse

class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = []

    pk = graphene.String()

class TransactionSeries(graphene.ObjectType):
    key = graphene.String()
    amount = graphene.Int()



class TransactionQueries(graphene.ObjectType):
    transactions = graphene.List(TransactionNode)
    transactionStats = graphene.List(TransactionNode, presetRange = graphene.String())
    transactionSeries = graphene.List(TransactionSeries, presetRange = graphene.String())

    def resolve_transactions(self, info):
        return Transaction.objects.all().order_by("-created_at")
    
    def resolve_transactionStats(self, info, presetRange):
        filter_date = transform.transform_type(self, presetRange)    
        return Transaction.objects.filter(created_at__gte=filter_date).order_by("-category")

    def resolve_transactionSeries(self, info, presetRange):
        data = []
        filter_date = transform.transform_type(self, presetRange)
        type = presetRange[7:-1].lower() 
        results = Transaction.objects.filter(created_at__gte=filter_date).annotate(key=Trunc("created_at", type)).values("key").annotate(amount = Sum("amount")).order_by("-amount")
        for result in results:
            x = {
                "key":result["key"].strftime("%Y-%m") if presetRange == "LAST_7_MONTHS" else result["key"].strftime("%Y-%m-%d"),
                "amount":result["amount"]
            }
            data.append(x)
        return data
