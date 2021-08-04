from django.urls import path

from . import views

urlpatterns = [
    path("account", views.AccountCreate.as_view()),
    path("account/<uuid:id>", views.AccountRetrieve.as_view()),
    path("account/<uuid:account_id>/equity", views.EquityHoldingListCreate.as_view()),
    path(
        "account/<uuid:account_id>/equity/<uuid:id>",
        views.EquityHoldingRetrieve.as_view(),
    ),
]
