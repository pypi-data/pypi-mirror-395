"""
Permissões customizadas para DRF
"""

from rest_framework import permissions

from shared_auth.middleware import get_member
from shared_auth.utils import get_organization_model


class IsAuthenticated(permissions.BasePermission):
    """
    Verifica se usuário está autenticado via SharedToken
    """

    message = "Autenticação necessária."

    def has_permission(self, request, view):
        return bool(
            request.user and hasattr(request.user, "pk") and request.user.is_active
        )


class HasActiveOrganization(permissions.BasePermission):
    """
    Verifica se usuário tem organização ativa
    """

    message = "Organização ativa necessária."

    def has_permission(self, request, view):
        if not request.user or not hasattr(request, "organization_id"):
            return False

        if not request.organization_id:
            return False

        # Verificar se organização está ativa
        Organization = get_organization_model()

        try:
            org = Organization.objects.get(pk=request.organization_id)
            return org.is_active()
        except Organization.DoesNotExist:
            return False


class IsSameOrganization(permissions.BasePermission):
    """
    Verifica se o objeto pertence à mesma organização do usuário

    O model deve ter organization_id
    """

    message = "Você não tem permissão para acessar este recurso."

    def has_object_permission(self, request, view, obj):
        if not hasattr(request, "organization_id"):
            return False

        if not hasattr(obj, "organization_id"):
            return True  # Se objeto não tem org, permite

        # Verifica se o usuário é membro da organização do objeto
        if not get_member(request.user.pk, obj.organization_id):
            return False

        return obj.organization_id == request.organization_id


class IsOwnerOrSameOrganization(permissions.BasePermission):
    """
    Verifica se é o dono do objeto OU da mesma organização

    O model deve ter user_id e/ou organization_id
    """

    message = "Você não tem permissão para acessar este recurso."

    def has_object_permission(self, request, view, obj):
        # Verificar se é o dono
        if hasattr(obj, "user_id") and obj.user_id == request.user.pk:
            return True

        # Verificar se é da mesma organização
        if hasattr(obj, "organization_id") and hasattr(request, "organization_id"):
            # Verifica se o usuário é membro da organização do objeto
            if get_member(request.user.pk, obj.organization_id):
                return obj.organization_id == request.organization_id

        return False


class HasSystemPermission(permissions.BasePermission):
    """
    Verifica se usuário tem permissão específica no sistema.
    
    Usage:
        class MyViewSet(viewsets.ModelViewSet):
            permission_classes = [HasSystemPermission]
            required_permission = 'create_invoices'
    """
    
    message = "Você não tem permissão para realizar esta ação."
    
    def has_permission(self, request, view):
        """Verifica permissão no nível da view"""
        from django.conf import settings
        from shared_auth.permissions_helpers import user_has_permission
        
        # Pegar permissão requerida
        permission_codename = getattr(view, 'required_permission', None)
        
        if not permission_codename:
            # Se não tem permissão definida, permite
            return True
        
        # Verificar autenticação
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Pegar organização
        organization_id = getattr(request, 'organization_id', None)
        if not organization_id:
            return False
        
        # Pegar sistema
        system_id = getattr(settings, 'SYSTEM_ID', None)
        if not system_id:
            # Tentar pegar do header
            header_value = request.headers.get('X-System-ID')
            if header_value:
                try:
                    system_id = int(header_value)
                except (ValueError, TypeError):
                    return False
            else:
                return False
        
        # Verificar permissão
        return user_has_permission(
            request.user.id,
            organization_id,
            permission_codename,
            system_id,
            request=request
        )


class HasAnyPermission(permissions.BasePermission):
    """
    Verifica se usuário tem pelo menos uma das permissões.
    
    Usage:
        class MyViewSet(viewsets.ModelViewSet):
            permission_classes = [HasAnyPermission]
            required_permissions = ['view_reports', 'create_reports']
    """
    
    message = "Você não tem nenhuma das permissões necessárias."
    
    def has_permission(self, request, view):
        """Verifica se tem pelo menos uma permissão"""
        from django.conf import settings
        from shared_auth.permissions_helpers import user_has_permission
        
        # Pegar permissões requeridas
        permission_codenames = getattr(view, 'required_permissions', [])
        
        if not permission_codenames:
            # Se não tem permissões definidas, permite
            return True
        
        # Verificar autenticação
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Pegar organização
        organization_id = getattr(request, 'organization_id', None)
        if not organization_id:
            return False
        
        # Pegar sistema
        system_id = getattr(settings, 'SYSTEM_ID', None)
        if not system_id:
            # Tentar pegar do header
            header_value = request.headers.get('X-System-ID')
            if header_value:
                try:
                    system_id = int(header_value)
                except (ValueError, TypeError):
                    return False
            else:
                return False
        
        # Verificar se tem pelo menos uma permissão
        return any(
            user_has_permission(
                request.user.id,
                organization_id,
                perm,
                system_id,
                request=request
            )
            for perm in permission_codenames
        )


class HasAllPermissions(permissions.BasePermission):
    """
    Verifica se usuário tem todas as permissões.
    
    Usage:
        class MyViewSet(viewsets.ModelViewSet):
            permission_classes = [HasAllPermissions]
            required_permissions = ['create_invoices', 'edit_invoices']
    """
    
    message = "Você não tem todas as permissões necessárias."
    
    def has_permission(self, request, view):
        """Verifica se tem todas as permissões"""
        from django.conf import settings
        from shared_auth.permissions_helpers import user_has_permission
        
        # Pegar permissões requeridas
        permission_codenames = getattr(view, 'required_permissions', [])
        
        if not permission_codenames:
            # Se não tem permissões definidas, permite
            return True
        
        # Verificar autenticação
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Pegar organização
        organization_id = getattr(request, 'organization_id', None)
        if not organization_id:
            return False
        
        # Pegar sistema
        system_id = getattr(settings, 'SYSTEM_ID', None)
        if not system_id:
            # Tentar pegar do header
            header_value = request.headers.get('X-System-ID')
            if header_value:
                try:
                    system_id = int(header_value)
                except (ValueError, TypeError):
                    return False
            else:
                return False
        
        # Verificar se tem todas as permissões
        return all(
            user_has_permission(
                request.user.id,
                organization_id,
                perm,
                system_id,
                request=request
            )
            for perm in permission_codenames
        )

