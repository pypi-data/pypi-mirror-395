from dlt._workspace.exceptions import WorkspaceException
from dlt.common.runtime.exceptions import RuntimeException


class RuntimeNotAuthenticated(RuntimeException):
    pass


class RuntimeOperationNotAuthorized(WorkspaceException, RuntimeException):
    pass


class WorkspaceIdMismatch(RuntimeOperationNotAuthorized):
    def __init__(self, local_workspace_id: str, remote_workspace_id: str):
        self.local_workspace_id = local_workspace_id
        self.remote_workspace_id = remote_workspace_id
        super().__init__(local_workspace_id, remote_workspace_id)


class LocalWorkspaceIdNotSet(RuntimeOperationNotAuthorized):
    def __init__(self, remote_workspace_id: str):
        self.remote_workspace_id = remote_workspace_id
        super().__init__(remote_workspace_id)
