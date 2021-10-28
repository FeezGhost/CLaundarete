from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsCreatorOrIsAdmin(permissions.BasePermission):

    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.groups.filter(name='launderer').exists():
            appUser = user.launderer
            return bool(appUser and obj.launderer == appUser)
        elif user.groups.filter(name='client').exists():
            appUser = user.client
            return bool(appUser and obj.client == appUser)
        else:
            return bool(user and user.is_staff)

class IsCreatorLaunderetteOrIsAdmin(permissions.BasePermission):

    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.groups.filter(name='launderer').exists():
            appUser = user.launderer
            if appUser.launderette.set_all().count() > 0:
                launderette = appUser.launderette.set_all()[0]
                return bool(launderette and obj.launderette == launderette)
            else:
                return False
        elif user.groups.filter(name='client').exists():
            appUser = user.client
            return bool(appUser and obj.client == appUser)
        else:
            return bool(user and user.is_staff)