from rest_framework.pagination import PageNumberPagination


class APIPagination(PageNumberPagination):
    """
    Пагинация для отзывов и комментариев.
    Размер страницы: 10 объектов.
    """
    page_size = 10