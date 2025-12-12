"""
Mixins para facilitar a criação de models com referências ao sistema de auth
"""

from django.db import models
from rest_framework import status, viewsets
from rest_framework.response import Response

from shared_auth.managers import BaseAuthManager


class OrganizationMixin(models.Model):
    """
    Mixin para models que pertencem a uma organização

    Adiciona:
    - Campo organization_id
    - Property organization (lazy loading)
    - Métodos úteis

    Usage:
        class Rascunho(OrganizationMixin):
            titulo = models.CharField(max_length=200)

        # Uso
        rascunho.organization  # Acessa organização automaticamente
        rascunho.organization_members  # Acessa membros
    """

    organization_id = models.IntegerField(
        db_index=True,
        help_text="ID da organização no sistema de autenticação",
        null=True,
        default=None,
    )
    objects = BaseAuthManager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["organization_id"]),
        ]

    @classmethod
    def prefetch_organizations(cls, queryset, request, org_ids=None):
        if not hasattr(request, "_orgs_dict"):
            from shared_auth.utils import get_organization_model

            Organization = get_organization_model()
            if org_ids is None:
                org_ids = list(
                    queryset.values_list("organization_id", flat=True).distinct()
                )
            if not org_ids:
                request._orgs_dict = {}
                return queryset

            orgs_qs = Organization.objects.filter(pk__in=org_ids)
            request._orgs_dict = {org.pk: org for org in orgs_qs}

        return queryset

    @property
    def organization(self):
        if not hasattr(self, "_cached_organization"):
            from shared_auth.utils import get_organization_model

            Organization = get_organization_model()
            self._cached_organization = Organization.objects.get_or_fail(
                self.organization_id
            )
        return self._cached_organization

    @property
    def organization_members(self):
        """Retorna membros da organização"""
        return self.organization.members

    @property
    def organization_users(self):
        """Retorna usuários da organização"""
        return self.organization.users

    def is_organization_active(self):
        """Verifica se a organização está ativa"""
        return self.organization.is_active()

    def get_organization_name(self):
        """Retorna nome da organização (safe)"""
        try:
            return self.organization.name
        except Exception:
            return None


class UserMixin(models.Model):
    """
    Mixin para models que pertencem a um usuário

    Adiciona:
    - Campo user_id
    - Property user (lazy loading)
    - Métodos úteis

    Usage:
        class Rascunho(UserMixin):
            titulo = models.CharField(max_length=200)

        # Uso
        rascunho.user  # Acessa usuário automaticamente
        rascunho.user_email  # Acessa email
    """

    user_id = models.IntegerField(
        db_index=True,
        help_text="ID do usuário no sistema de autenticação",
        null=True,
        default=None,
    )
    objects = BaseAuthManager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["user_id"]),
        ]

    @property
    def user(self):
        """
        Acessa usuário do banco de auth (lazy loading com cache)
        """
        if not hasattr(self, "_cached_user"):
            from shared_auth.utils import get_user_model

            User = get_user_model()
            self._cached_user = User.objects.get_or_fail(self.user_id)
        return self._cached_user

    @property
    def user_email(self):
        """Retorna email do usuário (safe)"""
        try:
            return self.user.email
        except Exception:
            return None

    @property
    def user_full_name(self):
        """Retorna nome completo do usuário (safe)"""
        try:
            return self.user.get_full_name()
        except Exception:
            return None

    @property
    def user_organizations(self):
        """Retorna organizações do usuário"""
        return self.user.organizations

    def is_user_active(self):
        """Verifica se o usuário está ativo"""
        try:
            return self.user.is_active and self.user.deleted_at is None
        except Exception:
            return False


class OrganizationUserMixin(OrganizationMixin, UserMixin):
    """
    Mixin combinado para models que pertencem a organização E usuário

    Adiciona tudo dos dois mixins + validações

    Usage:
        class Rascunho(OrganizationUserMixin):
            titulo = models.CharField(max_length=200)

        # Uso
        rascunho.organization  # Organização
        rascunho.user  # Usuário
        rascunho.validate_user_belongs_to_organization()  # Validação
    """

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["organization_id", "user_id"]),
        ]

    def validate_user_belongs_to_organization(self):
        """
        Valida se o usuário pertence à organização

        Returns:
            bool: True se pertence, False caso contrário
        """
        from shared_auth.utils import get_member_model

        Member = get_member_model()
        return Member.objects.filter(
            user_id=self.user_id, organization_id=self.organization_id
        ).exists()

    def user_can_access(self, user_id):
        """
        Verifica se um usuário pode acessar este registro
        (se pertence à mesma organização)
        """
        from shared_auth.utils import get_member_model

        Member = get_member_model()
        return Member.objects.filter(
            user_id=user_id, organization_id=self.organization_id
        ).exists()
        
class RequirePermissionMixin:
    required_permission = None
    required_permissions = None
    base_permission = None
    translate_action_to_perm = {
        'list': 'view',
        'retrieve': 'view',
        'create': 'add',
        'update': 'change',
        'partial_update': 'change',
        'destroy': 'delete',
    }
    
    def check_permissions(self, request):
        if hasattr(super(), 'check_permissions'):
            super().check_permissions(request)
        
        if self.base_permission and self.action in self.translate_action_to_perm:
            perm = f"{self.translate_action_to_perm.get(self.action)}_{self.base_permission}"
            if not self.check_permission(perm):
                self.permission_denied(
                    request,
                    message=f"Permissão '{perm}' necessária."
                )
        if self.required_permission:
            if not self.check_permission(self.required_permission):
                self.permission_denied(
                    request,
                    message=f"Permissão '{self.required_permission}' necessária."
                )
        if self.required_permissions:
            has_any = any(
                self.check_permission(perm) 
                for perm in self.required_permissions
            )
            if not has_any:
                self.permission_denied(
                    request,
                    message=f"Uma das permissões necessárias: {', '.join(self.required_permissions)}"
                )
    
    def check_permission(self, permission_codename):
        """
        Verifica se usuário tem permissão específica.
        
        OTIMIZADO: Passa request para habilitar cache de permissões.
        
        Args:
            permission_codename: Código da permissão (ex: 'create_invoices')
        
        Returns:
            bool: True se tem permissão
        
        Usage:
            if self.check_permission('create_invoices'):
                # Usuário pode criar faturas
                pass
        """
        from shared_auth.permissions_helpers import user_has_permission
        
        system_id = self.get_system_id()
        if not system_id:
            return False
        
        organization_id = self.get_organization_id()
        if not organization_id:
            return False
        
        user = self.get_user()
        if not user or not user.is_authenticated:
            return False
        
        return user_has_permission(
            user.id,
            organization_id,
            permission_codename,
            system_id,
            request=getattr(self, 'request', None)
        )

    def require_permission(self, permission_codename):
        """
        Retorna erro se usuário não tiver permissão.
        
        Args:
            permission_codename: Código da permissão
        
        Returns:
            Response com erro 403 ou None se tem permissão
        
        Usage:
            response = self.require_permission('create_invoices')
            if response:
                return response
        """
        if not self.check_permission(permission_codename):
            return Response(
                {"detail": f"Permissão '{permission_codename}' necessária."},
                status=status.HTTP_403_FORBIDDEN
            )
        return None

    def get_user_permissions(self):
        """
        Lista todas as permissões do usuário no sistema atual.
        
        Returns:
            list[Permission]: Permissões do usuário
        
        Usage:
            perms = self.get_user_permissions()
            for perm in perms:
                print(perm.codename)
        """
        from shared_auth.permissions_helpers import get_user_permissions
        
        system_id = self.get_system_id()
        if not system_id:
            return []
        
        organization_id = self.get_organization_id()
        if not organization_id:
            return []
        
        user = self.get_user()
        if not user or not user.is_authenticated:
            return []
        
        return get_user_permissions(
            user.id,
            organization_id,
            system_id,
            request=getattr(self, 'request', None)
        )

    def get_user_permission_codenames(self):
        """
        Lista codenames das permissões do usuário.
        
        Returns:
            List[str]: Lista de codenames
        
        Usage:
            codenames = self.get_user_permission_codenames()
            # ['create_invoices', 'edit_invoices']
        """
        return [perm.codename for perm in self.get_user_permissions()]



class LoggedOrganizationPermMixin:
    """
    Mixin para ViewSets que dependem de uma organização logada.
    Integra com a lib maquinaweb-shared-auth.
    
    NÃO use diretamente. Use LoggedOrganizationViewSet.
    """

    def get_organization_id(self):
        """Obtém o ID da organização logada via maquinaweb-shared-auth"""
        return getattr(self.request, 'organization_id', None)

    def get_organization_ids(self):
        """Obtém os IDs das organizações permitidas via maquinaweb-shared-auth"""
        return getattr(self.request, 'organization_ids', [])

    def get_user(self):
        """Obtém o usuário atual autenticado"""
        return self.request.user

    def get_system_id(self):
        """
        Obtém o ID do sistema.
        
        Busca em:
        1. Settings SYSTEM_ID
        2. Header X-System-ID
        """
        from django.conf import settings
        
        system_id = getattr(settings, 'SYSTEM_ID', None)
        if system_id:
            return system_id
        
        # Tentar pegar do header
        header_value = self.request.headers.get('X-System-ID')
        if header_value:
            try:
                return int(header_value)
            except (ValueError, TypeError):
                pass
        
        return None

    def check_logged_organization(self):
        """Verifica se há uma organização logada"""
        return self.get_organization_id() is not None

    def require_logged_organization(self):
        """Retorna erro se não houver organização logada"""
        if not self.check_logged_organization():
            return Response(
                {
                    "detail": "Nenhuma organização logada. Defina uma organização antes de continuar."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return None

    def get_queryset(self):
        """Filtra os objetos pela organização logada, se aplicável"""
        queryset = super().get_queryset()

        response = self.require_logged_organization()
        if response:
            return queryset.none()

        organization_id = self.get_organization_id()
        if hasattr(queryset.model, "organization_id"):
            return queryset.filter(organization_id=organization_id)
        elif hasattr(queryset.model, "organization"):
            return queryset.filter(organization_id=organization_id)
        return queryset

    def perform_create(self, serializer):
        """Define a organização automaticamente ao criar um objeto"""
        response = self.require_logged_organization()
        if response:
            # CORRIGIDO: Lançar exceção em vez de retornar Response
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Nenhuma organização logada.")

        organization_id = self.get_organization_id()

        if "organization" in serializer.fields:
            serializer.save(organization_id=organization_id)
        else:
            serializer.save()

class LoggedOrganizationMixin(RequirePermissionMixin, LoggedOrganizationPermMixin, viewsets.ModelViewSet):
    pass


class PrefetchOrganizationsMixin(LoggedOrganizationMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        return OrganizationMixin.prefetch_organizations(queryset, self.request)


class TimestampedMixin(models.Model):
    """
    Mixin para adicionar timestamps
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
