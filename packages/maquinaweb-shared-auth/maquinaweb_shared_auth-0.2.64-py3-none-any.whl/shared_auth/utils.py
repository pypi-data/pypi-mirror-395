"""
Utilitários para obter os models configurados
Similar ao get_user_model() do Django
"""

from django.apps import apps
from django.conf import importlib
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers

from .conf import get_setting


def get_token_model():
    """
    Retorna o model de Token configurado ou o padrão.

    Usage:
        from shared_auth.utils import get_token_model

        Token = get_token_model()
        token = Token.objects.get(key='abc123')
    """
    model_string = get_setting("SHARED_AUTH_TOKEN_MODEL", "shared_auth.SharedToken")

    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_TOKEN_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_TOKEN_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_organization_model():
    """
    Retorna o model de Organization configurado ou o padrão.

    Usage:
        from shared_auth.utils import get_organization_model

        Organization = get_organization_model()
        org = Organization.objects.get(id=1)
    """
    model_string = get_setting(
        "SHARED_AUTH_ORGANIZATION_MODEL", "shared_auth.SharedOrganization"
    )

    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_ORGANIZATION_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_ORGANIZATION_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_user_model():
    """
    Retorna o model de User configurado ou o padrão.

    Usage:
        from shared_auth.utils import get_user_model

        User = get_user_model()
        user = User.objects.get(id=1)
    """
    model_string = get_setting("SHARED_AUTH_USER_MODEL", "shared_auth.User")

    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_USER_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_USER_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_member_model():
    """
    Retorna o model de Member configurado ou o padrão.

    Usage:
        from shared_auth.utils import get_member_model

        Member = get_member_model()
        member = Member.objects.get(id=1)
    """
    model_string = get_setting("SHARED_AUTH_MEMBER_MODEL", "shared_auth.SharedMember")

    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_MEMBER_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_MEMBER_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_organization_serializer():
    import_path_serializer = get_setting("SHARED_AUTH_ORGANIZATION_SERIALIZER", None)

    if not import_path_serializer:
        return serializers.ModelSerializer

    try:
        module_path, class_name = import_path_serializer.rsplit(".", 1)
        module = importlib.import_module(module_path)
        serializer_class = getattr(module, class_name)
        return serializer_class
    except Exception as e:
        print(f"Erro ao importar serializer: {import_path_serializer}: {e}")
        return serializers.ModelSerializer


def get_organization_group_model():
    """
    Retorna o model de OrganizationGroup configurado ou o padrão.

    Usage:
        from shared_auth.utils import get_organization_group_model

        OrganizationGroup = get_organization_group_model()
        group = OrganizationGroup.objects.get(id=1)
    """
    model_string = get_setting(
        "SHARED_AUTH_ORGANIZATION_GROUP_MODEL", "shared_auth.OrganizationGroup"
    )

    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_ORGANIZATION_GROUP_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_ORGANIZATION_GROUP_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )



# ============================================================================
# PERMISSION SYSTEM MODEL GETTERS
# ============================================================================


def get_system_model():
    """
    Retorna o model de System configurado ou o padrão.
    
    Usage:
        from shared_auth.utils import get_system_model
        
        System = get_system_model()
        system = System.objects.get(id=1)
    """
    model_string = get_setting("SHARED_AUTH_SYSTEM_MODEL", "shared_auth.System")
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_SYSTEM_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_SYSTEM_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_permission_model():
    """
    Retorna o model de Permission configurado ou o padrão.
    
    Usage:
        from shared_auth.utils import get_permission_model
        
        Permission = get_permission_model()
        perm = Permission.objects.get(id=1)
    """
    model_string = get_setting("SHARED_AUTH_PERMISSION_MODEL", "shared_auth.Permission")
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_PERMISSION_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_PERMISSION_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_plan_model():
    """
    Retorna o model de Plan configurado ou o padrão.
    
    Usage:
        from shared_auth.utils import get_plan_model
        
        Plan = get_plan_model()
        plan = Plan.objects.get(id=1)
    """
    model_string = get_setting("SHARED_AUTH_PLAN_MODEL", "shared_auth.Plan")
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_PLAN_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_PLAN_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_subscription_model():
    """
    Retorna o model de Subscription configurado ou o padrão.
    
    Usage:
        from shared_auth.utils import get_subscription_model
        
        Subscription = get_subscription_model()
        sub = Subscription.objects.get(id=1)
    """
    model_string = get_setting("SHARED_AUTH_SUBSCRIPTION_MODEL", "shared_auth.Subscription")
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_SUBSCRIPTION_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_SUBSCRIPTION_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_group_permissions_model():
    """
    Retorna o model de GroupPermissions configurado ou o padrão.
    
    Usage:
        from shared_auth.utils import get_group_permissions_model
        
        GroupPermissions = get_group_permissions_model()
        group = GroupPermissions.objects.get(id=1)
    """
    model_string = get_setting("SHARED_AUTH_GROUP_PERMISSIONS_MODEL", "shared_auth.GroupPermissions")
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_GROUP_PERMISSIONS_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_GROUP_PERMISSIONS_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_group_organization_permissions_model():
    """
    Retorna o model de GroupOrganizationPermissions configurado ou o padrão.
    
    Usage:
        from shared_auth.utils import get_group_organization_permissions_model
        
        GroupOrgPermissions = get_group_organization_permissions_model()
        group = GroupOrgPermissions.objects.get(id=1)
    """
    model_string = get_setting(
        "SHARED_AUTH_GROUP_ORG_PERMISSIONS_MODEL", 
        "shared_auth.GroupOrganizationPermissions"
    )
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_GROUP_ORG_PERMISSIONS_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_GROUP_ORG_PERMISSIONS_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )


def get_member_system_group_model():
    """
    Retorna o model de MemberSystemGroup configurado ou o padrão.
    
    Usage:
        from shared_auth.utils import get_member_system_group_model
        
        MemberSystemGroup = get_member_system_group_model()
        assignment = MemberSystemGroup.objects.get(id=1)
    """
    model_string = get_setting(
        "SHARED_AUTH_MEMBER_SYSTEM_GROUP_MODEL", 
        "shared_auth.MemberSystemGroup"
    )
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_MEMBER_SYSTEM_GROUP_MODEL deve estar no formato 'app_label.model_name'. "
            f"Recebido: '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"SHARED_AUTH_MEMBER_SYSTEM_GROUP_MODEL refere-se ao model '{model_string}' "
            f"que não foi instalado ou é inválido."
        )

