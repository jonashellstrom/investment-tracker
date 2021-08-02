from rest_framework import pagination


class HoldingPagination(pagination.CursorPagination):
    ordering = "-first_added_at"
    page_size_query_param = "page_size"
