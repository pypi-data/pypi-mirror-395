class VaultOperationError(Exception):
    pass


class VaultTimeoutError(VaultOperationError):
    pass


class VaultAuthenticationError(VaultOperationError):
    pass


class VaultSecretNotFoundError(VaultOperationError):
    pass


class VaultSecretVersionDeletedError(VaultOperationError):
    pass


class VaultSecretVersionDestroyedError(VaultOperationError):
    pass


