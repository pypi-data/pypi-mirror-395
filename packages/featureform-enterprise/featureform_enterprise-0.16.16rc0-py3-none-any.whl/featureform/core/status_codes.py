"""
gRPC status codes used by Featureform.

These constants correspond to the gRPC status codes defined in the gRPC specification
and used by the Go server (google.golang.org/grpc/codes). They are used to identify
error types returned from the server without relying on error message strings.

Reference: https://grpc.github.io/grpc/core/md_doc_statuscodes.html
"""

# The operation completed successfully.
OK = 0

# The operation was cancelled, typically by the caller.
CANCELLED = 1

# Unknown error. This may be returned when a Status value received from another
# address space belongs to an error space that is not known in this address space.
UNKNOWN = 2

# The client specified an invalid argument.
INVALID_ARGUMENT = 3

# The deadline expired before the operation could complete.
DEADLINE_EXCEEDED = 4

# Some requested entity (e.g., file or directory) was not found.
NOT_FOUND = 5

# The entity that a client attempted to create already exists.
ALREADY_EXISTS = 6

# The caller does not have permission to execute the specified operation.
PERMISSION_DENIED = 7

# Some resource has been exhausted (e.g., per-user quota, file system space).
RESOURCE_EXHAUSTED = 8

# The operation was rejected because the system is not in a state required
# for the operation's execution.
FAILED_PRECONDITION = 9

# The operation was aborted, typically due to a concurrency issue.
ABORTED = 10

# The operation was attempted past the valid range.
OUT_OF_RANGE = 11

# The operation is not implemented or is not supported/enabled in this service.
UNIMPLEMENTED = 12

# Internal error.
INTERNAL = 13

# The service is currently unavailable.
UNAVAILABLE = 14

# Unrecoverable data loss or corruption.
DATA_LOSS = 15

# The request does not have valid authentication credentials.
UNAUTHENTICATED = 16
