from isapilib.api.models import BranchAPI
from isapilib.core.exceptions import PermissionDenied


def add_conn(user, branch: BranchAPI):
    name = branch.connection.create_connection()
    if not branch.check_permissions(user):
        raise PermissionDenied(f'You do not have permissions on this connection [{user.username}, {branch.pk}]')
    return name
