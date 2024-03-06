from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

class CustomPagination(PageNumberPagination):
    default_page_size = 10
    max_page_size = 100

    def get_page_size(self, request):
        if 'page_size' in request.query_params:
            try:
                page_size = int(request.query_params['page_size'])
                return min(page_size, self.max_page_size)
            except ValueError:
                raise ValidationError(detail="Invalid page size format. It should be an integer.")
        return self.default_page_size