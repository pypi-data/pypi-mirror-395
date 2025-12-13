"""
Middlewares para autenticação compartilhada
"""

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from .authentication import SharedTokenAuthentication
from .utils import (
    get_member_model,
    get_organization_model,
    get_token_model,
    get_user_model,
)


class SharedAuthMiddleware(MiddlewareMixin):
    """
    Middleware que autentica usuário baseado no token do header

    Usage em settings.py:
        MIDDLEWARE = [
            ...
            'shared_auth.middleware.SharedAuthMiddleware',
        ]

    O middleware busca o token em:
    - Header: Authorization: Token <token>
    - Header: X-Auth-Token: <token>
    - Cookie: auth_token
    """

    def process_request(self, request):
        from .permissions_cache import init_permissions_cache

        init_permissions_cache(request)

        # Caminhos que não precisam de autenticação
        exempt_paths = getattr(
            request,
            "auth_exempt_paths",
            [
                "/api/auth/login/",
                "/api/auth/register/",
                "/health/",
                "/static/",
            ],
        )

        if any(request.path.startswith(path) for path in exempt_paths):
            return None

        # Extrair token
        token = self._get_token_from_request(request)

        if not token:
            # request.user = None
            request.auth = None
            return None

        # Validar token e buscar usuário
        Token = get_token_model()
        User = get_user_model()

        try:
            token_obj = Token.objects.get(key=token)
            user = User.objects.get(pk=token_obj.user_id)

            if not user.is_active or user.deleted_at is not None:
                # request.user = None
                request.auth = None
                return None

            # Adicionar ao request
            if user:
                request.user = user
                request.auth = token_obj

        except (Token.DoesNotExist, User.DoesNotExist):
            # request.user = None
            request.auth = None

        return None

    def _get_token_from_request(self, request):
        """Extrai token do request"""
        # Header: Authorization: Token <token>
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Token "):
            return auth_header.split(" ")[1]

        # Header: X-Auth-Token
        token = request.META.get("HTTP_X_AUTH_TOKEN")
        if token:
            return token

        # Cookie
        token = request.COOKIES.get("auth_token")
        if token:
            return token

        return None


class RequireAuthMiddleware(MiddlewareMixin):
    """
    Middleware que FORÇA autenticação em todas as rotas
    Retorna 401 se não estiver autenticado

    Usage em settings.py:
        MIDDLEWARE = [
            'shared_auth.middleware.SharedAuthMiddleware',
            'shared_auth.middleware.RequireAuthMiddleware',
        ]
    """

    def process_request(self, request):
        # Caminhos públicos
        public_paths = getattr(
            request,
            "public_paths",
            [
                "/api/auth/",
                "/health/",
                "/docs/",
                "/static/",
            ],
        )

        if any(request.path.startswith(path) for path in public_paths):
            return None

        # Verificar se está autenticado
        if not hasattr(request, "user") or request.user is None:
            return JsonResponse(
                {
                    "error": "Autenticação necessária",
                    "detail": "Token não fornecido ou inválido",
                },
                status=401,
            )

        return None


class OrganizationMiddleware(MiddlewareMixin):
    """
    Middleware que adiciona organização logada ao request

    Adiciona:
    - request.organization (objeto SharedOrganization)
    """

    def process_request(self, request) -> None:
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            ip = ip.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        organization_id = self._determine_organization_id(request)
        user = self._authenticate_user(request)

        if not organization_id and not user:
            return

        if organization_id and user:
            organization_id = self._validate_organization_membership(
                user, organization_id
            )
            if not organization_id:
                return

        organization_ids = self._determine_organization_ids(request)

        request.organization_id = organization_id
        request.organization_ids = organization_ids
        Organization = get_organization_model()
        request.organization = Organization.objects.filter(pk=organization_id).first()

        if user and organization_id:
            system_id = self._get_system_id(request)
            if system_id:
                from .permissions_cache import warmup_permissions_cache

                warmup_permissions_cache(user.id, organization_id, system_id, request)

    @staticmethod
    def _authenticate_user(request):
        try:
            data = SharedTokenAuthentication().authenticate(request)
        except Exception:
            return None

        return data[0] if data else None

    def _determine_organization_id(self, request):
        org_id = self._get_organization_from_header(request)
        if org_id:
            return org_id

        return self._get_organization_from_user(request)

    def _determine_organization_ids(self, request):
        return self._get_organization_ids_from_user(request)

    @staticmethod
    def _get_organization_from_header(request):
        if header_value := request.headers.get("X-Organization"):
            try:
                return int(header_value)
            except (ValueError, TypeError):
                pass
        return None

    @staticmethod
    def _get_organization_from_user(request):
        """
        Retorna a primeira organização do usuário autenticado
        """
        if not request.user.is_authenticated:
            return None

        # Buscar a primeira organização que o usuário pertence
        Member = get_member_model()
        member = Member.objects.filter(user_id=request.user.pk).first()

        return member.organization_id if member else None

    @staticmethod
    def _get_organization_ids_from_user(request):
        if not request.user.is_authenticated:
            return None

        Member = get_member_model()
        member = Member.objects.filter(user_id=request.user.pk)

        return (
            list(member.values_list("organization_id", flat=True)) if member else None
        )

    @staticmethod
    def _validate_organization_membership(user, organization_id):
        try:
            member = get_member(user.pk, organization_id)
            if not member and not user.is_superuser:
                return None
            return organization_id
        except Exception:
            return None

    @staticmethod
    def _get_system_id(request):
        """
        Obtém o system_id para warm-up de permissões.

        Busca em:
        1. Settings SYSTEM_ID
        2. Header X-System-ID
        """
        from django.conf import settings

        system_id = getattr(settings, "SYSTEM_ID", None)
        if system_id:
            return system_id

        # Tentar pegar do header
        header_value = request.headers.get("X-System-ID")
        if header_value:
            try:
                return int(header_value)
            except (ValueError, TypeError):
                pass

        return None


def get_member(user_id, organization_id):
    """Busca membro usando o model configurado"""
    Member = get_member_model()
    return Member.objects.filter(
        user_id=user_id, organization_id=organization_id
    ).first()


class PaymentVerificationMiddleware(MiddlewareMixin):
    """
    Middleware que verifica se a organização possui assinatura ativa.

    Bloqueia acesso se:
    - Usuário não está em OrganizationGroup
    - OrganizationGroup não tem subscription ativa e paga

    Usage em settings.py:
        MIDDLEWARE = [
            'shared_auth.middleware.SharedAuthMiddleware',
            'shared_auth.middleware.OrganizationMiddleware',
            'shared_auth.middleware.PaymentVerificationMiddleware',  # Adicionar por último
        ]

        # Caminhos permitidos sem pagamento
        PAYMENT_EXEMPT_PATHS = [
            '/api/auth/',
            '/api/checkout/',
            '/admin/',
        ]
    """

    # Caminhos padrão permitidos sem verificação de pagamento
    DEFAULT_ALLOWED_PATHS = [
        "/api/auth/",
        "/api/checkout/",
        "/admin/",
        "/health/",
        "/docs/",
        "/static/",
        "/api/schema/",
    ]

    def process_request(self, request):
        from django.conf import settings

        # Ignora se não autenticado
        if not hasattr(request, "user") or not request.user.is_authenticated:
            return None

        # Ignora superusers
        if request.user.is_superuser:
            return None

        # Pega caminhos permitidos do settings ou usa padrão
        allowed_paths = getattr(
            settings, "PAYMENT_EXEMPT_PATHS", self.DEFAULT_ALLOWED_PATHS
        )

        # Verifica se path é permitido
        if any(request.path.startswith(path) for path in allowed_paths):
            return None

        # Busca OrganizationGroup do usuário
        from .utils import get_organization_group_model, get_subscription_model

        OrganizationGroup = get_organization_group_model()
        Subscription = get_subscription_model()

        # Tenta encontrar OrganizationGroup onde usuário é owner
        organization_group = OrganizationGroup.objects.filter(
            owner_id=request.user.id
        ).first()

        if not organization_group:
            return JsonResponse(
                {
                    "error": "no_organization_group",
                    "message": "Usuário não possui grupo de organização. Complete o onboarding.",
                    "redirect": "/onboarding/",
                },
                status=403,
            )

        # Verifica se tem subscription ativa e paga
        has_active_subscription = Subscription.objects.filter(
            organization_group_id=organization_group.pk, active=True, paid=True
        ).exists()

        if not has_active_subscription:
            return JsonResponse(
                {
                    "error": "no_active_subscription",
                    "message": "Não há assinatura ativa. Realize o pagamento para continuar.",
                    "redirect": "/checkout/",
                },
                status=402,  # Payment Required
            )

        return None
