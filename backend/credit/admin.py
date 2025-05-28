from django.contrib import admin

from backend.credit.models import CreditPlan, CreditRequest, Transaction


@admin.register(Transaction)
class TransactionModel(admin.ModelAdmin):
    list_display = ("balance", "type", "amount", "created_at")
    ordering = ("-created_at",)


@admin.register(CreditPlan)
class CreditPlanModel(admin.ModelAdmin):
    # list_display = ("balance", "type", "amount", "created_at")
    # ordering = ("-created_at",)
    pass


@admin.register(CreditRequest)
class CreditRequestModel(admin.ModelAdmin):
    # list_display = ("balance", "type", "amount", "created_at")
    # ordering = ("-created_at",)
    pass
