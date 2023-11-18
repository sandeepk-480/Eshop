from django.contrib import admin
from app.models import Category, Sub_category,Product,Contact,Order,Brand
from django.db.migrations.recorder import MigrationRecorder

# Register your models here.
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(Brand)


admin.site.register(MigrationRecorder.Migration)