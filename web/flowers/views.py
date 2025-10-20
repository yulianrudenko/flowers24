from django.views.generic import DetailView, ListView

from flowers.models import Bouquet, BouquetCategory


class BouquetListView(ListView):
    model = Bouquet
    template_name = "bouquet_list.html"
    context_object_name = "flowers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = BouquetCategory.objects.all()
        return context


class BouquetCategoryDetailView(DetailView):
    model = BouquetCategory
    template_name = "bouquet_category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bouquets"] = Bouquet.objects.filter(categories=self.object)
        context["categories"] = BouquetCategory.objects.all()
        return context
