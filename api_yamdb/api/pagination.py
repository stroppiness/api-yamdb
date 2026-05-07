from rest_framework.pagination import PageNumberPagination

class APIPagination(PageNumberPagination):
    page_size = 10