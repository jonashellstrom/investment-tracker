from django.urls import path

from . import views

urlpatterns = [
    path("account/<uuid:account_id>/equity", views.EquityHoldingList.as_view()),
    path(
        "account/<uuid:account_id>/equity/<uuid:id>",
        views.EquityHoldingRetrieve.as_view(),
    ),
]
