from django.contrib import admin
from .models import Inward, Material, Building, BuildingMaterial, Loan, InventoryTransaction, StockAlert, BuildingReport
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


#Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add custom fields here
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role')


# Inline for the BuildingMaterial model (because of the ManyToMany relationship with Material)
class BuildingMaterialInline(admin.TabularInline):
    model = BuildingMaterial
    extra = 1  # Number of empty forms to display by default

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'material_type', 'material_code','hsn_code')
    search_fields = ('name', 'material_type', 'material_code','hsn_code')
    list_filter = ('material_type',)

class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'project_manager', 'date_added')
    search_fields = ('name', 'location', 'project_manager')
    inlines = [BuildingMaterialInline]  # To show the building-material relation

# class BuildingMaterialAdmin(admin.ModelAdmin):
#     list_display = ('building', 'material', 'quantity', 'date_added')
#     search_fields = ('building__name', 'material__name')
#     list_filter = ('building', 'material')

class LoanAdmin(admin.ModelAdmin):
    list_display = ('from_building', 'to_building', 'material', 'quantity', 'loan_date', 'repayment_date')
    search_fields = ('from_building__name', 'to_building__name', 'material__name')
    list_filter = ('from_building', 'to_building', 'material')

# class InventoryTransactionAdmin(admin.ModelAdmin):
#     list_display = ('transaction_type', 'material', 'building', 'quantity', 'date')
#     list_filter = ('transaction_type', 'material', 'building')

class StockAlertAdmin(admin.ModelAdmin):
    list_display = ('material', 'threshold', 'alert_date')
    list_filter = ('material',)

class BuildingReportAdmin(admin.ModelAdmin):
    list_display = ('building', 'report_type', 'generated_on')
    list_filter = ('building', 'report_type')

class InwardAdmin(admin.ModelAdmin):
    list_display = ('material','supplier','po_number', 'building', 'quantity', 'date_inward','expiration_date')
    list_filter = ('material', 'building')

# Register all models
admin.site.register(Material, MaterialAdmin)
admin.site.register(Building, BuildingAdmin)
# admin.site.register(BuildingMaterial, BuildingMaterialAdmin)
# admin.site.register(Loan, LoanAdmin)
# admin.site.register(InventoryTransaction, InventoryTransactionAdmin)
# admin.site.register(StockAlert, StockAlertAdmin)
# admin.site.register(BuildingReport, BuildingReportAdmin)
admin.site.register(Inward, InwardAdmin)
