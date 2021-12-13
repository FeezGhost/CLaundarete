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

        if request.method == 'GET':
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
        if request.user.is_anonymous == False:
            user = request.user
            if user.groups.filter(name='launderer').exists():
                appUser = user.launderer
                if appUser.launderette_set.all().count() > 0:
                    launderette = appUser.launderette_set.all()[0]
                    return bool(obj.launderette.id == launderette.id)
                
                return False
            
            elif user.user.is_staff:
                return bool(user and user.is_staff)
            
            elif user.exists():
                appUser = user.client
                return bool(appUser and obj.client.id == appUser.id)
            
        else:
            return bool(False)
