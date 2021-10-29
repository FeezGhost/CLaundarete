from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsCreatorOrIsAdmin(permissions.BasePermission):

    message = 'You must be the creator of this object.'
    print('check 1')
        

    def has_object_permission(self, request, view, obj):
        print('check 2')
        if request.method in permissions.SAFE_METHODS:
            print('check 3')
            return True
        if request.method == 'GET':
            print('get')
            return True
        user = request.user
        if user.groups.filter(name='launderer').exists():
            print('check 4 launderer')
            appUser = user.launderer
            return bool(appUser and obj.launderer == appUser)
        elif user.groups.filter(name='client').exists():
            print('check 5 client')
            appUser = user.client
            return bool(appUser and obj.client == appUser)
        else:
            print('check 6 admin')
            return bool(user and user.is_staff)

class IsCreatorLaunderetteOrIsAdmin(permissions.BasePermission):
    print('check 1 in api')
    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        print('check 2 in api function')
        if request.method in permissions.SAFE_METHODS:
            print('check 3 in get api function')
            return True
        user = request.user
        if user.groups.filter(name='launderer').exists():
            print('check 4 in launderer')
            appUser = user.launderer
            if appUser.launderette_set.all().count() > 0:
                print('check 5 in launderette')
                launderette = appUser.launderette_set.all()[0]
                print(launderette)
                return bool(obj.launderette.id == launderette.id)
            return False
        elif user.groups.filter(name='client').exists():
            print('check 6 in client')
            appUser = user.client
            return bool(appUser and obj.client.id == appUser.id)
        else:
            print('check 7 in admin')
            return bool(user and user.is_staff)