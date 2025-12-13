from django.conf import settings

def get_setting(name, default):
    """Retorna valor configurado no settings ou o padrão"""
    return getattr(settings, name, default)


# Auth tables
ORGANIZATION_TABLE = get_setting("SHARED_AUTH_ORGANIZATION_TABLE", "organization_organization")
ORGANIZATION_GROUP_TABLE = get_setting("SHARED_AUTH_ORGANIZATION_GROUP_TABLE", "organization_organizationgroup")
USER_TABLE = get_setting("SHARED_AUTH_USER_TABLE", "auth_user")
MEMBER_TABLE = get_setting("SHARED_AUTH_MEMBER_TABLE", "organization_member")
TOKEN_TABLE = get_setting("SHARED_AUTH_TOKEN_TABLE", "organization_multitoken")

# Permission system tables
SYSTEM_TABLE = get_setting("SHARED_AUTH_SYSTEM_TABLE", "plans_system")
PERMISSION_TABLE = get_setting("SHARED_AUTH_PERMISSION_TABLE", "organization_permissions")
PLAN_TABLE = get_setting("SHARED_AUTH_PLAN_TABLE", "plans_plan")
SUBSCRIPTION_TABLE = get_setting("SHARED_AUTH_SUBSCRIPTION_TABLE", "plans_subscription")
GROUP_PERMISSIONS_TABLE = get_setting("SHARED_AUTH_GROUP_PERMISSIONS_TABLE", "organization_grouppermissions")
GROUP_ORG_PERMISSIONS_TABLE = get_setting("SHARED_AUTH_GROUP_ORG_PERMISSIONS_TABLE", "organization_grouporganizationpermissions")
MEMBER_SYSTEM_GROUP_TABLE = get_setting("SHARED_AUTH_MEMBER_SYSTEM_GROUP_TABLE", "organization_membersystemgroup")

# и т.д.
# ManyToMany tables
PLAN_GROUP_PERMISSIONS_TABLE = get_setting("SHARED_AUTH_PLAN_GROUP_PERMISSIONS_TABLE", "plans_plan_group_permissions")
GROUP_PERMISSIONS_PERMISSIONS_TABLE = get_setting("SHARED_AUTH_GROUP_PERMISSIONS_PERMISSIONS_TABLE", "organization_grouppermissions_permissions")
GROUP_ORG_PERMISSIONS_PERMISSIONS_TABLE = get_setting("SHARED_AUTH_GROUP_ORG_PERMISSIONS_PERMISSIONS_TABLE", "organization_grouporganizationpermissions_permissions")

# Other settings
CLOUDFRONT_DOMAIN = get_setting("CLOUDFRONT_DOMAIN", "")
CUSTOM_DOMAIN_AUTH = get_setting("CUSTOM_DOMAIN_AUTH", CLOUDFRONT_DOMAIN)
SYSTEM_ID = get_setting("SYSTEM_ID", None)