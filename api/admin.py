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
    filter_horizontal = ('wishlist',)
    


# class ProductImageInline(GrappelliSortableHiddenMixin, admin.TabularInline):
class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    # sortable_field_name = 'order'

# class ProductOptionInline(GrappelliSortableHiddenMixin, admin.TabularInline):
class ProductOptionInline(admin.TabularInline):
    model = models.ProductOption
    # sortable_field_name = 'order'

# class ReviewInline(GrappelliSortableHiddenMixin, admin.TabularInline):
class ReviewInline(admin.TabularInline):
    model = models.Review
    # sortable_field_name = 'order'

@admin.register(models.Product)
class Product(BaseAdmin):
    list_filter = ('seller', 'category', 'is_hide', 'created', 'updated')
    list_display = ('seller', 'category', 'name', 'address', 'price', 'view_count', 'description', 'is_hide', 'created', 'updated')
    inlines = [ProductImageInline, ProductOptionInline, ReviewInline]

@admin.register(models.Review)
class Review(BaseAdmin):
    list_filter = ('product__name', )

@admin.register(models.Purchase)
class Purchase(BaseAdmin):
    list_filter = ('buyer','product_option','qty','amount','payment_type','status','imp_id','merchant_uid','created','updated',)


