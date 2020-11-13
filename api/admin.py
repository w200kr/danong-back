from django.contrib import admin

from grappelli.forms import GrappelliSortableHiddenMixin

from api import models

class BaseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SmallCategory)
class SmallCategoryAdmin(admin.ModelAdmin):
    list_display = ('large_category', 'name')
    list_filter = ('large_category', )

@admin.register(models.Profile)
class Profile(BaseAdmin):
    list_display = ('get_username','category','name','address',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'ID'


class ProductImageInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = models.ProductImage
    sortable_field_name = 'order'

class ProductOptionInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = models.ProductOption
    sortable_field_name = 'order'

class ReviewInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = models.Review
    sortable_field_name = 'order'

@admin.register(models.Product)
class Product(BaseAdmin):
    inlines = [ProductImageInline, ProductOptionInline, ReviewInline]

@admin.register(models.Review)
class Review(BaseAdmin):
    list_filter = ('product__name', )

@admin.register(models.Purchase)
class Purchase(BaseAdmin):
    list_filter = ('buyer','product_option','qty','amount','payment_type','status','imp_id','merchant_id','created','updated',)
