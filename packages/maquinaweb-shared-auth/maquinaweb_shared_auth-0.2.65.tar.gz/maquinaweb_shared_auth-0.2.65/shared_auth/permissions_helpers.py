"""
Helper functions para checagem e listagem de permissões
Funções principais para o sistema de permissões multi-sistema
"""


def user_has_permission(user_id, organization_id, permission_codename, system_id, request=None):
    """
    Verifica se um usuário tem uma permissão específica.
    
    OTIMIZADO: Usa cache por request para eliminar queries duplicadas.
    
    Fluxo:
    1. Busca Member (user + organization) - COM CACHE
    2. Busca MemberSystemGroup (member + system) - COM CACHE
    3. Busca GroupOrganizationPermissions - COM CACHE
    4. Verifica se permission_codename está no grupo - COM CACHE
    
    Args:
        user_id: ID do usuário
        organization_id: ID da organização
        permission_codename: Código da permissão (ex: 'create_invoices')
        system_id: ID do sistema
        request: Request object (opcional, para cache)
    
    Returns:
        bool: True se usuário tem a permissão, False caso contrário
    
    Usage:
        from shared_auth.permissions_helpers import user_has_permission
        
        if user_has_permission(5, 1, 'create_invoices', 2, request):
            # Usuário pode criar faturas
            pass
    """
    from .permissions_cache import (
        get_cached_member,
        get_cached_member_group,
        get_cached_permission_codenames,
    )
    
    # 1. Buscar membro (COM CACHE)
    member = get_cached_member(user_id, organization_id, request)
    if not member:
        return False
    
    # 2. Buscar grupo do membro no sistema (COM CACHE)
    member_group = get_cached_member_group(member.id, system_id, request)
    if not member_group:
        return False
    
    # 3. Buscar codenames de permissões do grupo (COM CACHE)
    codenames = get_cached_permission_codenames(member_group.group_id, system_id, request)
    
    # 4. Verificar se permissão está no set (O(1) lookup)
    return permission_codename in codenames


def get_user_permissions(user_id, organization_id, system_id, request=None):
    """
    Retorna todas as permissões do usuário em um sistema.
    
    OTIMIZADO: Usa cache por request para eliminar queries duplicadas.
    
    Args:
        user_id: ID do usuário
        organization_id: ID da organização
        system_id: ID do sistema
        request: Request object (opcional, para cache)
    
    Returns:
        list[Permission]: Lista de permissões do usuário
    
    Usage:
        from shared_auth.permissions_helpers import get_user_permissions
        
        perms = get_user_permissions(5, 1, 2, request)
        for perm in perms:
            print(perm.codename)
    """
    from .permissions_cache import (
        get_cached_all_permissions,
        get_cached_member,
        get_cached_member_group,
    )
    
    # 1. Buscar membro (COM CACHE)
    member = get_cached_member(user_id, organization_id, request)
    if not member:
        return []
    
    # 2. Buscar grupo do membro no sistema (COM CACHE)
    member_group = get_cached_member_group(member.id, system_id, request)
    if not member_group:
        return []
    
    # 3. Buscar todas as permissões (COM CACHE)
    return get_cached_all_permissions(member_group.group_id, system_id, request)


def get_user_permission_codenames(user_id, organization_id, system_id, request=None):
    """
    Retorna lista de codenames de permissões do usuário.
    
    OTIMIZADO: Usa cache por request.
    
    Args:
        user_id: ID do usuário
        organization_id: ID da organização
        system_id: ID do sistema
        request: Request object (opcional, para cache)
    
    Returns:
        List[str]: Lista de codenames
    
    Usage:
        from shared_auth.permissions_helpers import get_user_permission_codenames
        
        codenames = get_user_permission_codenames(5, 1, 2, request)
        # ['create_invoices', 'edit_invoices', 'view_reports']
    """
    permissions = get_user_permissions(user_id, organization_id, system_id, request)
    return [perm.codename for perm in permissions]


def get_organization_permissions(organization_id, system_id):
    """
    Retorna permissões disponíveis no plano da organização.
    
    Fluxo:
    1. Busca Subscription ativa
    2. Busca Plan
    3. Retorna permissões dos GroupPermissions do plano
    
    Args:
        organization_id: ID da organização
        system_id: ID do sistema
    
    Returns:
        QuerySet[Permission]: Permissões do plano
    
    Usage:
        from shared_auth.permissions_helpers import get_organization_permissions
        
        perms = get_organization_permissions(1, 2)
        for perm in perms:
            print(perm.codename)
    """
    from .utils import get_permission_model, get_subscription_model
    
    Permission = get_permission_model()
    
    # 1. Buscar assinatura ativa
    Subscription = get_subscription_model()
    subscription = Subscription.objects.valid_for_organization_and_system(
        organization_id,
        system_id
    )
    
    if not subscription:
        return Permission.objects.none()
    
    # 2. Buscar plano
    plan = subscription.plan
    if not plan:
        return Permission.objects.none()
    
    # 3. Buscar grupos de permissões do plano
    group_permissions = plan.group_permissions.all()
    
    # 4. Coletar todas as permissões dos grupos
    permission_ids = []
    for group in group_permissions:
        permission_ids.extend(
            group.permissions.values_list('id', flat=True)
        )
    
    # 5. Retornar permissões únicas
    return Permission.objects.filter(id__in=set(permission_ids))


def get_organization_permission_codenames(organization_id, system_id):
    """
    Retorna lista de codenames de permissões do plano da organização.
    
    Args:
        organization_id: ID da organização
        system_id: ID do sistema
    
    Returns:
        List[str]: Lista de codenames
    
    Usage:
        from shared_auth.permissions_helpers import get_organization_permission_codenames
        
        codenames = get_organization_permission_codenames(1, 2)
    """
    permissions = get_organization_permissions(organization_id, system_id)
    return list(permissions.values_list('codename', flat=True))


def user_has_any_permission(user_id, organization_id, permission_codenames, system_id):
    """
    Verifica se usuário tem pelo menos uma das permissões.
    
    Args:
        user_id: ID do usuário
        organization_id: ID da organização
        permission_codenames: Lista de codenames
        system_id: ID do sistema
    
    Returns:
        bool: True se tem pelo menos uma permissão
    
    Usage:
        from shared_auth.permissions_helpers import user_has_any_permission
        
        if user_has_any_permission(5, 1, ['view_reports', 'create_reports'], 2):
            # Usuário pode ver ou criar relatórios
            pass
    """
    for codename in permission_codenames:
        if user_has_permission(user_id, organization_id, codename, system_id):
            return True
    return False


def user_has_all_permissions(user_id, organization_id, permission_codenames, system_id):
    """
    Verifica se usuário tem todas as permissões.
    
    Args:
        user_id: ID do usuário
        organization_id: ID da organização
        permission_codenames: Lista de codenames
        system_id: ID do sistema
    
    Returns:
        bool: True se tem todas as permissões
    
    Usage:
        from shared_auth.permissions_helpers import user_has_all_permissions
        
        if user_has_all_permissions(5, 1, ['create_invoices', 'edit_invoices'], 2):
            # Usuário pode criar E editar faturas
            pass
    """
    for codename in permission_codenames:
        if not user_has_permission(user_id, organization_id, codename, system_id):
            return False
    return True
