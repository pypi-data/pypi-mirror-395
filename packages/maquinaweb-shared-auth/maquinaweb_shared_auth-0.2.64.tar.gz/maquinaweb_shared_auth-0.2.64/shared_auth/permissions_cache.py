"""
Sistema de cache de permissões por request.
Elimina queries duplicadas durante verificação de permissões.
"""

from threading import local

# Thread-local storage para cache quando não há request disponível
_thread_local = local()


def _get_cache_dict(request=None):
    """
    Obtém o dicionário de cache de permissões.
    
    Args:
        request: Request object (opcional)
        
    Returns:
        dict: Dicionário de cache
    """
    if request and hasattr(request, '_permissions_cache'):
        return request._permissions_cache
    
    # Fallback para thread-local (útil em contextos sem request)
    if not hasattr(_thread_local, 'permissions_cache'):
        _thread_local.permissions_cache = {}
    return _thread_local.permissions_cache


def get_cached_member(user_id, organization_id, request=None):
    """
    Busca e cacheia Member para o par (user_id, organization_id).
    
    Args:
        user_id: ID do usuário
        organization_id: ID da organização
        request: Request object (opcional)
        
    Returns:
        Member instance ou None
    """
    from .utils import get_member_model
    
    cache = _get_cache_dict(request)
    cache_key = f'member_{user_id}_{organization_id}'
    
    if cache_key in cache:
        return cache[cache_key]
    
    Member = get_member_model()
    member = Member.objects.filter(
        user_id=user_id,
        organization_id=organization_id
    ).first()
    
    cache[cache_key] = member
    return member


def get_cached_member_group(member_id, system_id, request=None):
    """
    Busca e cacheia MemberSystemGroup para o par (member_id, system_id).
    
    Args:
        member_id: ID do membro
        system_id: ID do sistema
        request: Request object (opcional)
        
    Returns:
        MemberSystemGroup instance ou None
    """
    from .utils import get_member_system_group_model
    
    cache = _get_cache_dict(request)
    cache_key = f'member_group_{member_id}_{system_id}'
    
    if cache_key in cache:
        return cache[cache_key]
    
    MemberSystemGroup = get_member_system_group_model()
    member_group = MemberSystemGroup.objects.get_group_for_member_and_system(
        member_id,
        system_id
    )
    
    cache[cache_key] = member_group
    return member_group


def get_cached_group_permissions(group_id, system_id, request=None):
    """
    Busca e cacheia GroupOrganizationPermissions com suas permissões.
    
    Args:
        group_id: ID do grupo de permissões
        system_id: ID do sistema
        request: Request object (opcional)
        
    Returns:
        GroupOrganizationPermissions instance ou None
    """
    from .utils import get_group_organization_permissions_model
    
    cache = _get_cache_dict(request)
    cache_key = f'group_perms_{group_id}_{system_id}'
    
    if cache_key in cache:
        return cache[cache_key]
    
    GroupOrgPermissions = get_group_organization_permissions_model()
    try:
        # Busca o grupo sem prefetch ainda
        group = GroupOrgPermissions.objects.get(pk=group_id)
    except GroupOrgPermissions.DoesNotExist:
        cache[cache_key] = None
        return None
    
    cache[cache_key] = group
    return group


def get_cached_permission_codenames(group_id, system_id, request=None):
    """
    Busca e cacheia SET de codenames de permissões do grupo.
    
    Args:
        group_id: ID do grupo de permissões
        system_id: ID do sistema
        request: Request object (opcional)
        
    Returns:
        set: Set de codenames de permissões
    """
    cache = _get_cache_dict(request)
    cache_key = f'perm_codenames_{group_id}_{system_id}'
    
    if cache_key in cache:
        return cache[cache_key]
    
    group = get_cached_group_permissions(group_id, system_id, request)
    if not group:
        cache[cache_key] = set()
        return set()
    
    # Buscar todos os codenames de uma vez
    codenames = set(
        group.permissions.filter(system_id=system_id)
        .values_list('codename', flat=True)
    )
    
    cache[cache_key] = codenames
    return codenames


def get_cached_all_permissions(group_id, system_id, request=None):
    """
    Busca e cacheia lista de Permission objects do grupo.
    
    Args:
        group_id: ID do grupo de permissões
        system_id: ID do sistema
        request: Request object (opcional)
        
    Returns:
        list: Lista de Permission objects
    """
    cache = _get_cache_dict(request)
    cache_key = f'all_perms_{group_id}_{system_id}'
    
    if cache_key in cache:
        return cache[cache_key]
    
    group = get_cached_group_permissions(group_id, system_id, request)
    if not group:
        cache[cache_key] = []
        return []
    
    # Buscar todas as permissões de uma vez e converter para lista
    permissions = list(group.permissions.filter(system_id=system_id))
    
    cache[cache_key] = permissions
    return permissions


def warmup_permissions_cache(user_id, organization_id, system_id, request=None):
    """
    Pré-carrega (warm-up) todas as permissões do usuário no cache.
    Reduz 4 queries para apenas as necessárias no início da request.
    
    Esta função deve ser chamada pelo middleware após autenticação.
    
    Args:
        user_id: ID do usuário
        organization_id: ID da organização
        system_id: ID do sistema
        request: Request object
        
    Returns:
        bool: True se conseguiu fazer warm-up, False caso contrário
    """
    # 1. Buscar e cachear member
    member = get_cached_member(user_id, organization_id, request)
    if not member:
        return False
    
    # 2. Buscar e cachear member group
    member_group = get_cached_member_group(member.id, system_id, request)
    if not member_group:
        return False
    
    # 3. Buscar e cachear group permissions
    group = get_cached_group_permissions(member_group.group_id, system_id, request)
    if not group:
        return False
    
    # 4. OTIMIZAÇÃO PRINCIPAL: Carregar TODAS as permissões e codenames de uma vez
    # Isso faz com que verificações subsequentes sejam O(1) em memória
    get_cached_permission_codenames(member_group.group_id, system_id, request)
    get_cached_all_permissions(member_group.group_id, system_id, request)
    
    return True


def clear_permissions_cache(request=None):
    """
    Limpa o cache de permissões.
    Útil para testes ou quando necessário forçar reload.
    
    Args:
        request: Request object (opcional)
    """
    if request and hasattr(request, '_permissions_cache'):
        request._permissions_cache.clear()
    
    if hasattr(_thread_local, 'permissions_cache'):
        _thread_local.permissions_cache.clear()


def init_permissions_cache(request):
    """
    Inicializa o cache de permissões no request.
    Chamado pelo middleware no início de cada request.
    
    Args:
        request: Request object
    """
    if not hasattr(request, '_permissions_cache'):
        request._permissions_cache = {}
