"""
Models abstratos para customização
Estes models podem ser herdados nos apps clientes para adicionar campos e métodos customizados
"""

import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from shared_auth.conf import (
    GROUP_ORG_PERMISSIONS_PERMISSIONS_TABLE,
    GROUP_ORG_PERMISSIONS_TABLE,
    GROUP_PERMISSIONS_PERMISSIONS_TABLE,
    GROUP_PERMISSIONS_TABLE,
    PERMISSION_TABLE,
    PLAN_GROUP_PERMISSIONS_TABLE,
    PLAN_TABLE,
    SUBSCRIPTION_TABLE,
    SYSTEM_TABLE,
)

from .conf import MEMBER_TABLE, ORGANIZATION_TABLE, TOKEN_TABLE, USER_TABLE
from .exceptions import OrganizationNotFoundError
from .managers import SharedMemberManager, SharedOrganizationManager, UserManager
from .storage_backend import Storage


def organization_image_path(instance, filename):
    return os.path.join(
        "organization",
        str(instance.pk),
        "images",
        filename,
    )


class AbstractSharedToken(models.Model):
    """
    Model abstrato READ-ONLY da tabela authtoken_token
    Usado para validar tokens em outros sistemas

    Para customizar, crie um model no seu app:

    from shared_auth.abstract_models import AbstractSharedToken

    class CustomToken(AbstractSharedToken):
        # Adicione campos customizados
        custom_field = models.CharField(max_length=100)

        class Meta(AbstractSharedToken.Meta):
            pass

    E configure no settings.py:
    SHARED_AUTH_TOKEN_MODEL = 'seu_app.CustomToken'
    """

    key = models.CharField(max_length=40, primary_key=True)
    user_id = models.IntegerField()
    created = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        abstract = True
        managed = False
        db_table = TOKEN_TABLE

    def __str__(self):
        return self.key

    @property
    def user(self):
        """Acessa usuário do token"""
        from .utils import get_user_model

        if not hasattr(self, "_cached_user"):
            User = get_user_model()
            self._cached_user = User.objects.get_or_fail(self.user_id)
        return self._cached_user

    def is_valid(self):
        """Verifica se token ainda é válido"""
        # Implementar lógica de expiração se necessário
        return True


class AbstractSharedOrganization(models.Model):
    """
    Model abstrato READ-ONLY da tabela organization
    Usado para acessar dados de organizações em outros sistemas

    Para customizar, crie um model no seu app:

    from shared_auth.abstract_models import AbstractSharedOrganization

    class CustomOrganization(AbstractSharedOrganization):
        # Adicione campos customizados
        custom_field = models.CharField(max_length=100)

        class Meta(AbstractSharedOrganization.Meta):
            pass

    E configure no settings.py:
    SHARED_AUTH_ORGANIZATION_MODEL = 'seu_app.CustomOrganization'
    """

    # Campos principais
    name = models.CharField(max_length=255)
    fantasy_name = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    cellphone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image_organization = models.ImageField(
        storage=Storage, upload_to=organization_image_path, null=True
    )
    logo = models.ImageField(
        storage=Storage, upload_to=organization_image_path, null=True
    )

    # Relacionamentos
    organization_group_id = models.IntegerField(null=True, blank=True)
    main_organization_id = models.IntegerField(null=True, blank=True)
    is_branch = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict)

    # Metadados
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SharedOrganizationManager()

    class Meta:
        abstract = True
        managed = False
        db_table = ORGANIZATION_TABLE

    def __str__(self):
        return self.fantasy_name or self.name or f"Org #{self.pk}"

    @property
    def organization_group(self):
        """
        Acessa grupo de organização (lazy loading)

        Usage:
            if org.organization_group:
                print(org.organization_group.name)
        """
        from .utils import get_organization_group_model

        if self.organization_group_id:
            OrganizationGroup = get_organization_group_model()
            return OrganizationGroup.objects.get_or_fail(self.organization_group_id)
        return None

    @property
    def main_organization(self):
        """
        Acessa organização principal (lazy loading)

        Usage:
            if org.is_branch:
                main = org.main_organization
        """
        from .utils import get_organization_model

        if self.main_organization_id:
            Organization = get_organization_model()
            return Organization.objects.get_or_fail(self.main_organization_id)
        return None

    @property
    def branches(self):
        """
        Retorna filiais desta organização

        Usage:
            branches = org.branches
        """
        from .utils import get_organization_model

        Organization = get_organization_model()
        return Organization.objects.filter(main_organization_id=self.pk)

    @property
    def members(self):
        """
        Retorna membros desta organização

        Usage:
            members = org.members
            for member in members:
                print(member.user.email)
        """
        from .utils import get_member_model

        Member = get_member_model()
        return Member.objects.for_organization(self.pk)

    @property
    def users(self):
        """
        Retorna usuários desta organização

        Usage:
            users = org.users
        """
        from .utils import get_user_model

        User = get_user_model()
        return User.objects.filter(
            id__in=self.members.values_list("user_id", flat=True)
        )

    def is_active(self):
        """Verifica se organização está ativa"""
        return self.deleted_at is None

    def get_permissions_for_system(self, system):
        """
        Retorna permissões do sistema baseado na assinatura do grupo de organizações.
        Se a organização não pertence a um grupo, retorna vazio.

        Args:
            system: Instance do System model ou system_id (int)

        Returns:
            QuerySet de Permission objects

        Usage:
            from shared_auth.utils import get_system_model

            System = get_system_model()
            system = System.objects.get(name='MeuSistema')
            permissions = organization.get_permissions_for_system(system)
        """
        from .utils import get_permission_model, get_subscription_model

        # Se não pertence a um grupo, sem permissões
        if not self.organization_group_id:
            Permission = get_permission_model()
            return Permission.objects.none()

        # Extrai system_id se foi passado um objeto
        system_id = system.id if hasattr(system, "id") else system

        Subscription = get_subscription_model()
        Permission = get_permission_model()

        # Busca assinatura ativa do grupo
        subscription = (
            Subscription.objects.filter(
                organization_group_id=self.organization_group_id,
                plan__system_id=system_id,
                active=True,
                paid=True,
            )
            .select_related("plan")
            .order_by("-started_at")
            .first()
        )

        if not subscription:
            return Permission.objects.none()

        # Coleta todas as permissões dos grupos de permissões do plano
        permission_ids = set()
        for group in subscription.plan.group_permissions.all():
            permission_ids.update(group.permissions.values_list("id", flat=True))

        return Permission.objects.filter(id__in=permission_ids, system_id=system_id)


class AbstractUser(AbstractUser):
    """
    Model abstrato READ-ONLY da tabela auth_user

    Para customizar, crie um model no seu app:

    from shared_auth.abstract_models import AbstractUser

    class CustomUser(AbstractUser):
        # Adicione campos customizados
        custom_field = models.CharField(max_length=100)

        class Meta(AbstractUser.Meta):
            pass

    E configure no settings.py:
    SHARED_AUTH_USER_MODEL = 'seu_app.CustomUser'
    """

    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(storage=Storage, blank=True, null=True)

    # Campos customizados
    createdat = models.DateTimeField()
    updatedat = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    class Meta:
        abstract = True
        managed = False
        db_table = USER_TABLE

    @property
    def organizations(self):
        """
        Retorna todas as organizações associadas ao usuário.
        """
        from .utils import get_member_model, get_organization_model

        Organization = get_organization_model()
        Member = get_member_model()

        return Organization.objects.filter(
            id__in=Member.objects.filter(user_id=self.id).values_list(
                "organization_id", flat=True
            )
        )

    def get_org(self, organization_id):
        """
        Retorna a organização especificada pelo ID, se o usuário for membro.
        """
        from .utils import get_member_model, get_organization_model

        Organization = get_organization_model()
        Member = get_member_model()

        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            raise OrganizationNotFoundError(
                f"Organização com ID {organization_id} não encontrada."
            )

        if not Member.objects.filter(
            user_id=self.id, organization_id=organization.id
        ).exists():
            raise OrganizationNotFoundError("Usuário não é membro desta organização.")

        return organization


class AbstractSharedMember(models.Model):
    """
    Model abstrato READ-ONLY da tabela organization_member
    Relacionamento entre User e Organization

    Para customizar, crie um model no seu app:

    from shared_auth.abstract_models import AbstractSharedMember

    class CustomMember(AbstractSharedMember):
        # Adicione campos customizados
        custom_field = models.CharField(max_length=100)

        class Meta(AbstractSharedMember.Meta):
            pass

    E configure no settings.py:
    SHARED_AUTH_MEMBER_MODEL = 'seu_app.CustomMember'
    """

    user_id = models.IntegerField()
    organization_id = models.IntegerField()
    metadata = models.JSONField(default=dict)

    objects = SharedMemberManager()

    class Meta:
        abstract = True
        managed = False
        db_table = MEMBER_TABLE

    def __str__(self):
        return f"Member: User {self.user_id} - Org {self.organization_id}"

    @property
    def user(self):
        """
        Acessa usuário (lazy loading)

        Usage:
            member = SharedMember.objects.first()
            user = member.user
            print(user.email)
        """
        from .utils import get_user_model

        User = get_user_model()
        return User.objects.get_or_fail(self.user_id)

    @property
    def organization(self):
        """
        Acessa organização (lazy loading)

        Usage:
            member = SharedMember.objects.first()
            org = member.organization
            print(org.name)
        """
        from .utils import get_organization_model

        Organization = get_organization_model()
        return Organization.objects.get_or_fail(self.organization_id)


class GroupPermissionsPermission(models.Model):
    grouppermissions_id = models.BigIntegerField()
    permissions_id = models.BigIntegerField()

    class Meta:
        db_table = GROUP_PERMISSIONS_PERMISSIONS_TABLE
        managed = False
        unique_together = ("grouppermissions_id", "permissions_id")
        app_label = "shared_auth"

    def __str__(self):
        return f"GroupPerm {self.grouppermissions_id} → Perm {self.permissions_id}"


class PlanGroupPermission(models.Model):
    plan_id = models.BigIntegerField()
    grouppermissions_id = models.BigIntegerField()

    class Meta:
        db_table = PLAN_GROUP_PERMISSIONS_TABLE
        managed = False
        unique_together = ("plan_id", "grouppermissions_id")
        app_label = "shared_auth"

    def __str__(self):
        return f"Plan {self.plan_id} → GroupPerm {self.grouppermissions_id}"


class GroupOrgPermissionsPermission(models.Model):
    grouporganizationpermissions_id = models.BigIntegerField()
    permissions_id = models.BigIntegerField()

    class Meta:
        db_table = GROUP_ORG_PERMISSIONS_PERMISSIONS_TABLE
        managed = False
        unique_together = ("grouporganizationpermissions_id", "permissions_id")
        app_label = "shared_auth"

    def __str__(self):
        return f"OrgGroup {self.grouporganizationpermissions_id} → Perm {self.permissions_id}"


class AbstractSystem(models.Model):
    """
    Model abstrato READ-ONLY da tabela plans_system
    Representa um sistema externo que usa este serviço de autenticação

    Para customizar, crie um model no seu app:

    from shared_auth.abstract_models import AbstractSystem

    class CustomSystem(AbstractSystem):
        custom_field = models.CharField(max_length=100)

        class Meta(AbstractSystem.Meta):
            pass

    E configure no settings.py:
    SHARED_AUTH_SYSTEM_MODEL = 'seu_app.CustomSystem'
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = models.Manager()  # Will be replaced by SystemManager in concrete model

    class Meta:
        abstract = True
        managed = False
        db_table = SYSTEM_TABLE

    def __str__(self):
        return self.name


class AbstractPermission(models.Model):
    """
    Model abstrato READ-ONLY da tabela organization_permissions
    Define permissões específicas de cada sistema

    Para customizar, crie um model no seu app e configure:
    SHARED_AUTH_PERMISSION_MODEL = 'seu_app.CustomPermission'
    """

    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    scope = models.CharField(max_length=100, blank=True, default="")
    scope_label = models.CharField(max_length=100, blank=True, default="")
    model = models.CharField(max_length=100, blank=True, default="")
    model_label = models.CharField(max_length=100, blank=True, default="")
    system_id = models.IntegerField()

    objects = models.Manager()

    class Meta:
        abstract = True
        managed = False
        db_table = PERMISSION_TABLE

    def __str__(self):
        return f"{self.codename} ({self.name})"

    @property
    def system(self):
        """Acessa sistema (lazy loading)"""
        from .utils import get_system_model

        if not hasattr(self, "_cached_system"):
            System = get_system_model()
            self._cached_system = System.objects.get_or_fail(self.system_id)
        return self._cached_system


class AbstractGroupPermissions(models.Model):
    """
    Model abstrato READ-ONLY da tabela organization_grouppermissions
    Grupos base de permissões (usados nos planos)

    Para customizar, configure:
    SHARED_AUTH_GROUP_PERMISSIONS_MODEL = 'seu_app.CustomGroupPermissions'
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    system_id = models.IntegerField()

    objects = models.Manager()

    class Meta:
        abstract = True
        managed = False
        db_table = GROUP_PERMISSIONS_TABLE

    def __str__(self):
        return self.name

    @property
    def system(self):
        """Acessa sistema (lazy loading)"""
        from .utils import get_system_model

        if not hasattr(self, "_cached_system"):
            System = get_system_model()
            self._cached_system = System.objects.get_or_fail(self.system_id)
        return self._cached_system

    @property
    def permissions(self):
        from .utils import get_permission_model

        Permission = get_permission_model()

        perm_ids = (
            GroupPermissionsPermission.objects.using("auth_db")
            .filter(grouppermissions_id=self.pk)
            .values_list("permissions_id", flat=True)
        )

        return Permission.objects.using("auth_db").filter(id__in=perm_ids)


class AbstractPlan(models.Model):
    """
    Model abstrato READ-ONLY da tabela plans_plan
    Planos oferecidos por cada sistema, com conjunto de permissões

    Para customizar, configure:
    SHARED_AUTH_PLAN_MODEL = 'seu_app.CustomPlan'
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    system_id = models.IntegerField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    recurrence = models.CharField(max_length=10)

    # Campos de desconto - aplicados nas primeiras recorrências
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Valor de desconto aplicado nas primeiras recorrências",
    )
    discount_duration = models.PositiveIntegerField(
        null=True, blank=True, help_text="Número de recorrências com desconto"
    )

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        abstract = True
        managed = False
        db_table = PLAN_TABLE

    def __str__(self):
        return f"{self.name} - {self.system.name if hasattr(self, 'system') else self.system_id}"

    @property
    def system(self):
        """Acessa sistema (lazy loading)"""
        from .utils import get_system_model

        if not hasattr(self, "_cached_system"):
            System = get_system_model()
            self._cached_system = System.objects.get_or_fail(self.system_id)
        return self._cached_system

    @property
    def group_permissions(self):
        from .utils import get_group_permissions_model

        GroupPermissions = get_group_permissions_model()

        group_ids = (
            PlanGroupPermission.objects.using("auth_db")
            .filter(plan_id=self.pk)
            .values_list("grouppermissions_id", flat=True)
        )

        return GroupPermissions.objects.using("auth_db").filter(id__in=group_ids)

    def get_price_for_subscription(self, payment_count=0):
        """
        Calcula o preço considerando desconto aplicado.

        Args:
            payment_count: Número de pagamentos já realizados para esta subscription.
                          Se for o primeiro pagamento (count=0), aplica desconto se houver.

        Returns:
            Decimal: Preço do plano, com desconto se aplicável.
        """
        if self.discount_amount and self.discount_duration:
            if payment_count < self.discount_duration:
                return self.price - self.discount_amount
        return self.price


class AbstractOrganizationGroup(models.Model):
    """
    Model abstrato READ-ONLY da tabela organization_organizationgroup
    Representa um grupo de organizações com assinatura compartilhada

    Para customizar, crie um model no seu app:

    from shared_auth.abstract_models import AbstractOrganizationGroup

    class CustomOrganizationGroup(AbstractOrganizationGroup):
        custom_field = models.CharField(max_length=100)

        class Meta(AbstractOrganizationGroup.Meta):
            pass

    E configure no settings.py:
    SHARED_AUTH_ORGANIZATION_GROUP_MODEL = 'seu_app.CustomOrganizationGroup'
    """

    owner_id = models.IntegerField()
    name = models.CharField(
        max_length=255, help_text="Nome do grupo (ex: 'Empresas do João', 'Grupo Acme')"
    )

    # Campos de billing (usados para pagamentos)
    document = models.CharField(
        max_length=20, blank=True, null=True, help_text="CPF/CNPJ"
    )
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    # Organização padrão do grupo
    default_organization_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = models.Manager()

    class Meta:
        abstract = True
        managed = False
        db_table = "organization_organizationgroup"  # Will be imported from conf in concrete model

    def __str__(self):
        return f"{self.name} (Owner: {self.owner_id})"

    @property
    def owner(self):
        """Acessa usuário (lazy loading)"""
        from .utils import get_user_model

        if not hasattr(self, "_cached_owner"):
            User = get_user_model()
            self._cached_owner = User.objects.get_or_fail(self.owner_id)
        return self._cached_owner

    @property
    def default_organization(self):
        """Acessa organização padrão (lazy loading)"""
        from .utils import get_organization_model

        if not self.default_organization_id:
            return None

        if not hasattr(self, "_cached_default_organization"):
            Organization = get_organization_model()
            try:
                self._cached_default_organization = Organization.objects.get(
                    pk=self.default_organization_id
                )
            except Organization.DoesNotExist:
                self._cached_default_organization = None
        return self._cached_default_organization

    @property
    def organizations(self):
        """Retorna organizações pertencentes a este grupo"""
        from .utils import get_organization_model

        Organization = get_organization_model()
        return Organization.objects.filter(organization_group_id=self.pk)

    @property
    def subscriptions(self):
        """Retorna assinaturas ativas deste grupo"""
        from .utils import get_subscription_model

        Subscription = get_subscription_model()
        return Subscription.objects.filter(organization_group_id=self.pk)

    def has_active_subscription(self, system_id=None):
        """
        Verifica se o grupo tem assinatura ativa.

        Args:
            system_id: Opcional. ID do sistema para verificar assinatura específica.
        """
        from .utils import get_subscription_model

        Subscription = get_subscription_model()
        qs = Subscription.objects.filter(
            organization_group_id=self.pk, active=True, paid=True
        )

        if system_id:
            qs = qs.filter(plan__system_id=system_id)

        return qs.exists()


class AbstractSubscription(models.Model):
    """
    Model abstrato READ-ONLY da tabela plans_subscription
    Assinatura de plano por grupo de organizações.
    Uma assinatura cobre TODAS as organizações do grupo.

    Modelo simplificado: 1 subscription por plano que renova continuamente.
    Histórico de pagamentos é mantido no model Payment.

    Para customizar, configure:
    SHARED_AUTH_SUBSCRIPTION_MODEL = 'seu_app.CustomSubscription'
    """

    organization_group_id = models.IntegerField(
        help_text="Grupo de organizações cobertas por esta assinatura"
    )
    plan_id = models.IntegerField()
    payment_date = models.DateTimeField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)
    started_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    objects = models.Manager()  # Will be replaced by SubscriptionManager

    class Meta:
        abstract = True
        managed = False
        db_table = SUBSCRIPTION_TABLE

    def __str__(self):
        return f"Subscription {self.pk} - Group {self.organization_group_id}"

    @property
    def organization_group(self):
        """Acessa grupo de organizações (lazy loading)"""
        from .utils import get_organization_group_model

        if not hasattr(self, "_cached_organization_group"):
            OrganizationGroup = get_organization_group_model()
            try:
                self._cached_organization_group = OrganizationGroup.objects.get(
                    pk=self.organization_group_id
                )
            except OrganizationGroup.DoesNotExist:
                self._cached_organization_group = None
        return self._cached_organization_group

    @property
    def plan(self):
        """Acessa plano (lazy loading)"""
        from .utils import get_plan_model

        if not hasattr(self, "_cached_plan"):
            Plan = get_plan_model()
            try:
                self._cached_plan = Plan.objects.get(pk=self.plan_id)
            except Plan.DoesNotExist:
                self._cached_plan = None
        return self._cached_plan

    def is_valid(self):
        """Verifica se assinatura está ativa, paga e não expirada (DEPRECATED: use is_active_and_valid)"""
        return self.is_active_and_valid()

    def is_active_and_valid(self):
        """
        Verifica se subscription está ativa, paga e dentro do prazo.
        Considera também se foi cancelada.
        """
        if not self.active or not self.paid:
            return False

        if self.canceled_at:
            # Se cancelada, ainda é válida até expirar
            if self.expires_at and self.expires_at < timezone.now():
                return False
            return True

        if self.expires_at and self.expires_at < timezone.now():
            return False

        return True

    def is_expired(self):
        """Verifica se a assinatura está expirada"""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    def needs_renewal(self):
        """
        Verifica se a subscription precisa de renovação.
        Retorna True se auto_renew ativo e expiração atingida/próxima.
        """
        if not self.auto_renew:
            return False
        if not self.expires_at:
            return False
        return timezone.now() >= self.expires_at

    def set_paid(self):
        """Marca assinatura como paga (apenas para referência, não salva)"""
        self.paid = True
        self.payment_date = timezone.now()

    def cancel(self):
        """Cancela assinatura - mantém ativa até expirar (apenas para referência, não salva)"""
        self.auto_renew = False
        self.canceled_at = timezone.now()


class AbstractGroupOrganizationPermissions(models.Model):
    """
    Model abstrato READ-ONLY da tabela organization_grouporganizationpermissions
    Grupos de permissões criados pela organização para distribuir aos usuários

    Para customizar, configure:
    SHARED_AUTH_GROUP_ORG_PERMISSIONS_MODEL = 'seu_app.CustomGroupOrgPermissions'
    """

    organization_id = models.IntegerField()
    system_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    objects = (
        models.Manager()
    )  # Will be replaced by GroupOrganizationPermissionsManager

    class Meta:
        abstract = True
        managed = False
        db_table = GROUP_ORG_PERMISSIONS_TABLE

    def __str__(self):
        return f"{self.name} (Org {self.organization_id})"

    @property
    def organization(self):
        """Acessa organização (lazy loading)"""
        from .utils import get_organization_model

        if not hasattr(self, "_cached_organization"):
            Organization = get_organization_model()
            self._cached_organization = Organization.objects.get_or_fail(
                self.organization_id
            )
        return self._cached_organization

    @property
    def system(self):
        """Acessa sistema (lazy loading)"""
        from .utils import get_system_model

        if not hasattr(self, "_cached_system"):
            System = get_system_model()
            self._cached_system = System.objects.get_or_fail(self.system_id)
        return self._cached_system

    @property
    def permissions(self):
        from .utils import get_permission_model

        Permission = get_permission_model()

        perm_ids = (
            GroupOrgPermissionsPermission.objects.using("auth_db")
            .filter(grouporganizationpermissions_id=self.pk)
            .values_list("permissions_id", flat=True)
        )

        return Permission.objects.using("auth_db").filter(id__in=perm_ids)


class AbstractMemberSystemGroup(models.Model):
    """
    Model abstrato READ-ONLY da tabela organization_membersystemgroup
    Relaciona um membro a um grupo de permissões em um sistema específico

    Para customizar, configure:
    SHARED_AUTH_MEMBER_SYSTEM_GROUP_MODEL = 'seu_app.CustomMemberSystemGroup'
    """

    member_id = models.IntegerField()
    group_id = models.IntegerField()
    system_id = models.IntegerField()
    created_at = models.DateTimeField()

    objects = models.Manager()  # Will be replaced by MemberSystemGroupManager

    class Meta:
        abstract = True
        managed = False
        db_table = GROUP_ORG_PERMISSIONS_TABLE

    def __str__(self):
        return (
            f"Member {self.member_id} - Group {self.group_id} - System {self.system_id}"
        )

    @property
    def member(self):
        """Acessa membro (lazy loading)"""
        from .utils import get_member_model

        if not hasattr(self, "_cached_member"):
            Member = get_member_model()
            try:
                self._cached_member = Member.objects.get(pk=self.member_id)
            except Member.DoesNotExist:
                self._cached_member = None
        return self._cached_member

    @property
    def group(self):
        """Acessa grupo (lazy loading)"""
        from .utils import get_group_organization_permissions_model

        if not hasattr(self, "_cached_group"):
            GroupOrgPermissions = get_group_organization_permissions_model()
            try:
                self._cached_group = GroupOrgPermissions.objects.get(pk=self.group_id)
            except GroupOrgPermissions.DoesNotExist:
                self._cached_group = None
        return self._cached_group

    @property
    def system(self):
        """Acessa sistema (lazy loading)"""
        from .utils import get_system_model

        if not hasattr(self, "_cached_system"):
            System = get_system_model()
            self._cached_system = System.objects.get_or_fail(self.system_id)
        return self._cached_system
