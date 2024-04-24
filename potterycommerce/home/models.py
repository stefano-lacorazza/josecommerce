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

    collection = models.ForeignKey(
        "ProductCollection",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    content_panels = Page.content_panels + [
        FieldPanel("sku"),
        FieldPanel("price"),
        FieldPanel("collection"),
        FieldPanel("short_description"),
        InlinePanel("custom_fields", label="Custom fields"),
        InlinePanel("images", label="Product Images"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        product_images = ProductImage.objects.all()
        cntx_product_images = []
        for product_image in product_images:
            if product_image.product == self:
                cntx_product_images.append(product_image)
        context["product_images"] = cntx_product_images
        return context


class ShopPage(Page):
    def get_context(self, request):
        context = super().get_context(request)

        siblings = Page.objects.sibling_of(self)
        products = Product.objects.child_of(siblings[0]).live()
        collections = ProductCollection.objects.child_of(siblings[0]).live()

        # Query all ProductImage objects related to the products
        product_images = ProductImage.objects.all()
        for product in products:
            for product_image in product_images:
                if product_image.product == product:
                    product.image = product_image.image

        context["products"] = products
        context["collections"] = collections
        context["product_images"] = product_images

        return context


class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)

        products = Product.objects.child_of(self.get_descendants()[0]).live()
        collections = ProductCollection.objects.child_of(
            self.get_descendants()[0]
        ).live()

        # Query all ProductImage objects related to the products
        # product_images = ProductImage.objects.filter(product__in=products)

        context["products"] = products
        context["collections"] = collections
        # context["product_images"] = product_images

        return context


class ProductCustomField(Orderable):
    product = ParentalKey(
        Product, on_delete=models.CASCADE, related_name="custom_fields"
    )
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [FieldPanel("name"), FieldPanel("options")]

    def get_context(self, request):
        context = super().get_context(request)
        fields = []
        for f in self.custom_fields.get_object_list():
            if f.options:
                f.options_array = f.options.split("|")
                fields.append(f)
            else:
                fields.append(f)

        context["custom_fields"] = fields

        return context


class ProductImage(models.Model):
    # The product that this image belongs to
    product = ParentalKey("Product", related_name="images", on_delete=models.CASCADE)

    # The image
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("image"),
    ]


class ProductCollection(Page):
    # The name of the collection
    name = models.CharField(max_length=255, unique=True)

    description = models.TextField(blank=True, null=True)
    # The panels for the admin interface
    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("description"),
        InlinePanel("images", label="Collection Images"),
    ]


class ProductCollectionCustomField(Orderable):
    ProductCollection = ParentalKey(
        ProductCollection, on_delete=models.CASCADE, related_name="custom_fields"
    )
    name = models.CharField(max_length=255)
    options = models.CharField(max_length=500, null=True, blank=True)

    panels = [FieldPanel("name"), FieldPanel("options")]

    def get_context(self, request):
        context = super().get_context(request)
        fields = []
        for f in self.custom_fields.get_object_list():
            if f.options:
                f.options_array = f.options.split("|")
                fields.append(f)
            else:
                fields.append(f)

        context["custom_fields"] = fields

        return context


class CollectionImage(models.Model):
    # The collection that this image belongs to
    collection = ParentalKey(
        "ProductCollection", related_name="images", on_delete=models.CASCADE
    )

    # The image
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("image"),
    ]


@register_setting
class SnipcartSettings(BaseSiteSetting):
    api_key = models.CharField(max_length=255, help_text="Your Snipcart public API key")
