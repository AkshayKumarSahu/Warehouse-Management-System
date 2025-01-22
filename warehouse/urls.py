from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.AdminView.as_view(), name='admin_dashboard'),
    path('building_manager_dashboard/', views.BuildingManagerView.as_view(), name='building_manager_dashboard'),
    path('warehouse_keeper_dashboard/', views.WarehouseKeeperView.as_view(), name='warehouse_keeper_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('inventory/', views.view_all_inventory, name='view_all_inventory'),
    path('add_material/', views.add_material, name='add_material'),
    path('inward/', views.inward_material, name='inward_material'),
    path('add_building/', views.add_building, name='add_building'),
    path('assign_material/', views.assign_material, name='assign_material'),
    path('building_material_list/', views.building_material_list, name='building_material_list'),
    path('buildings/', views.building_list, name='building_list'),
    path('building_materials/<str:building_name>/', views.building_material_list, name='building_materials'),
    path('issue_material/', views.issue_material, name='issue_material'),

    # Other URL patterns
    path('get_material_details/', views.get_material_details, name='get_material_details'),
    path('search_materials/', views.search_materials, name='search_materials'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('get_materials_for_building/<int:building_id>/', views.get_materials_for_building, name='get_materials_for_building'),
    path('get_building_materials/', views.get_building_materials, name='get_building_materials'),
    path('get_material_quantity/', views.get_material_quantity, name='get_material_quantity'),
    
    
    
    #hidden urls
    path('record_consumption/', views.record_consumption, name='record_consumption'),
    path('consumption_report/', views.consumption_report, name='consumption_report'),
    path('loan_material/', views.loan_material, name='loan_material'),
    path('repay_material/', views.repay_material, name='repay_material'),
    path('loan_list/', views.loan_list, name='loan_list'),  # Add a loan list view
    path('reports/total-usage/', views.total_inventory_usage, name='total_inventory_usage'),
    path('reports/loan-history/', views.loan_repayment_history, name='loan_repayment_history'),

    # path('material_list/', views.material_list, name='material_list'),
    # path('loan_history/', views.loan_history, name='loan_history'),
]
