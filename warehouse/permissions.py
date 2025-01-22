from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsBuildingManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'building_manager'

class IsWarehouseKeeper(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'warehouse_keeper'
