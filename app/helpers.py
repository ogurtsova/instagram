from django.core.paginator import Paginator


def pagination(request, items, per_page=3):
    p = Paginator(items, per_page)
    page_number = 1
    if request.GET.get("page"):
        page_number = request.GET.get("page")
    page = p.page(page_number)
    return page


class Pager():
    query_set = []
    items = []
    page = 0
    per_page = 0

    def start(self, qs, pp):
        self.query_set = qs
        self.per_page = pp

    def set_page(self, p):
        self.page = p

    def get_items(self):
        return self.items