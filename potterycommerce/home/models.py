from django.db import models

from wagtail.models import Page

from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


class Product(Page):
    sku = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('sku'),
        FieldPanel('price'),
        FieldPanel('image'),
        FieldPanel('short_description'),
        InlinePanel('custom_fields', label='Custom fields'),
    ]

class ProductCustomField(Orderable):
    product = ParentalKey(Product, on_delete=models.CASCADE, related_name='custom_fields')
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('options')
    ]
    def get_context(self, request):
        context = super().get_context(request)
        fields = []
        for f in self.custom_fields.get_object_list():
            if f.options:
                f.options_array = f.options.split('|')
                fields.append(f)
            else:
                fields.append(f)

        context['custom_fields'] = fields

        return context


class HomePage(Page):
    def get_context(self, request):
        
        context = super().get_context(request)

        #context['products'] = Product.objects.child_of(self).live()
        products =  Product.objects.child_of(self.get_descendants()[0]).live()
        #products = ['a','bb']
        context['products'] = products
        return context
    

    

# Defining a new model called ShopPage that inherits from the Page model
class ShopPage(Page):
    # Overriding the get_context method to add additional context
    def get_context(self, request):
        # Getting all sibling pages of the current page
        siblings = Page.objects.sibling_of(self)
        # Getting the context from the parent class
        context = super().get_context(request)

        # Getting all live child pages of the first sibling that are instances of the Product model
        products =  Product.objects.child_of(siblings[0]).live()

        context['products'] = products
        return context
    



@register_setting
class SnipcartSettings(BaseSiteSetting):
    api_key = models.CharField(
        max_length=255,
        help_text='Your Snipcart public API key'
    )
