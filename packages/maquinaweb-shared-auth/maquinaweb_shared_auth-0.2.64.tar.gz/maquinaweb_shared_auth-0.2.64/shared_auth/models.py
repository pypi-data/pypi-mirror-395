"""
Models READ-ONLY para acesso aos dados de autenticação
ATENÇÃO: Estes models NÃO devem ser usados para criar migrations

Para customizar estes models, herde dos models abstratos em shared_auth.abstract_models
e configure no settings.py. Veja a documentação em abstract_models.py
"""

from .abstract_models import (
    AbstractGroupOrganizationPermissions,
    AbstractGroupPermissions,
    AbstractMemberSystemGroup,
    AbstractOrganizationGroup,
    AbstractPermission,
    AbstractPlan,
    AbstractSharedMember,
    AbstractSharedOrganization,
    AbstractSharedToken,
    AbstractSubscription,
    AbstractSystem,
    AbstractUser,
)
from .conf import (
    GROUP_ORG_PERMISSIONS_TABLE,
    GROUP_PERMISSIONS_TABLE,
    MEMBER_SYSTEM_GROUP_TABLE,
    ORGANIZATION_GROUP_TABLE,
    PERMISSION_TABLE,
    PLAN_TABLE,
    SUBSCRIPTION_TABLE,
    SYSTEM_TABLE,
)
from .managers import (
    GroupOrganizationPermissionsManager,
    MemberSystemGroupManager,
    PermissionManager,
    SubscriptionManager,
    SystemManager,
)


class SharedToken(AbstractSharedToken):
    """
    Model READ-ONLY padrão da tabela authtoken_token
    
    Para customizar, crie seu próprio model herdando de AbstractSharedToken
    """
    
    class Meta(AbstractSharedToken.Meta):
        pass


class SharedOrganization(AbstractSharedOrganization):
    """
    Model READ-ONLY padrão da tabela organization
    
    Para customizar, crie seu próprio model herdando de AbstractSharedOrganization
    """
    
    class Meta(AbstractSharedOrganization.Meta):
        pass


class User(AbstractUser):
    """
    Model READ-ONLY padrão da tabela auth_user
    
    Para customizar, crie seu próprio model herdando de AbstractUser
    """
    
    class Meta(AbstractUser.Meta):
        pass


class SharedMember(AbstractSharedMember):
    """
    Model READ-ONLY padrão da tabela organization_member
    
    Para customizar, crie seu próprio model herdando de AbstractSharedMember
    """
    
    class Meta(AbstractSharedMember.Meta):
        pass


class OrganizationGroup(AbstractOrganizationGroup):
    """
    Model READ-ONLY padrão da tabela organization_organizationgroup
    Representa um grupo de organizações com assinatura compartilhada
    
    Para customizar, crie seu próprio model herdando de AbstractOrganizationGroup
    """
    
    class Meta(AbstractOrganizationGroup.Meta):
        db_table = ORGANIZATION_GROUP_TABLE



class System(AbstractSystem):
    """
    Model READ-ONLY padrão da tabela plans_system
    Representa um sistema externo que usa este serviço de autenticação
    
    Para customizar, crie seu próprio model herdando de AbstractSystem
    """
    
    objects = SystemManager()
    
    class Meta(AbstractSystem.Meta):
        db_table = SYSTEM_TABLE


class Permission(AbstractPermission):
    """
    Model READ-ONLY padrão da tabela organization_permissions
    Define permissões específicas de cada sistema
    
    Para customizar, crie seu próprio model herdando de AbstractPermission
    """
    
    objects = PermissionManager()
    
    class Meta(AbstractPermission.Meta):
        db_table = PERMISSION_TABLE


class GroupPermissions(AbstractGroupPermissions):
    """
    Model READ-ONLY padrão da tabela organization_grouppermissions
    Grupos base de permissões (usados nos planos)
    
    Para customizar, crie seu próprio model herdando de AbstractGroupPermissions
    """
    
    class Meta(AbstractGroupPermissions.Meta):
        db_table = GROUP_PERMISSIONS_TABLE


class Plan(AbstractPlan):
    """
    Model READ-ONLY padrão da tabela plans_plan
    Planos oferecidos por cada sistema, com conjunto de permissões
    
    Para customizar, crie seu próprio model herdando de AbstractPlan
    """
    
    class Meta(AbstractPlan.Meta):
        db_table = PLAN_TABLE


class Subscription(AbstractSubscription):
    """
    Model READ-ONLY padrão da tabela plans_subscription
    Assinatura de uma organização a um plano
    
    Para customizar, crie seu próprio model herdando de AbstractSubscription
    """
    
    objects = SubscriptionManager()
    
    class Meta(AbstractSubscription.Meta):
        db_table = SUBSCRIPTION_TABLE


class GroupOrganizationPermissions(AbstractGroupOrganizationPermissions):
    """
    Model READ-ONLY padrão da tabela organization_grouporganizationpermissions
    Grupos de permissões criados pela organização para distribuir aos usuários
    
    Para customizar, crie seu próprio model herdando de AbstractGroupOrganizationPermissions
    """
    
    objects = GroupOrganizationPermissionsManager()
    
    class Meta(AbstractGroupOrganizationPermissions.Meta):
        db_table = GROUP_ORG_PERMISSIONS_TABLE


class MemberSystemGroup(AbstractMemberSystemGroup):
    """
    Model READ-ONLY padrão da tabela organization_membersystemgroup
    Relaciona um membro a um grupo de permissões em um sistema específico
    
    Para customizar, crie seu próprio model herdando de AbstractMemberSystemGroup
    """
    
    objects = MemberSystemGroupManager()
    
    class Meta(AbstractMemberSystemGroup.Meta):
        db_table = MEMBER_SYSTEM_GROUP_TABLE

