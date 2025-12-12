from greyhorse.error import Error, ErrorCase


class BorrowError(Error):
    namespace = 'greyhorse.app'

    Empty = ErrorCase(
        msg='Cannot borrow "{name}" as immutable because the value is not available', name=str
    )

    # MovedOut = ErrorCase(
    #     msg='Cannot borrow "{name}" as immutable because the value was moved out', name=str
    # )

    BorrowedAsMutable = ErrorCase(
        msg='Cannot borrow "{name}" as immutable because it is also borrowed as mutable',
        name=str,
    )

    Unexpected = ErrorCase(
        msg='Cannot borrow "{name}" as immutable because an unexpected '
        'error occurred: "{details}"',
        name=str,
        details=str,
    )


class BorrowMutError(Error):
    namespace = 'greyhorse.app'

    Empty = ErrorCase(
        msg='Cannot borrow "{name}" as mutable because the value is not available', name=str
    )

    # MovedOut = ErrorCase(
    #     msg='Cannot borrow "{name}" as mutable because the value was moved out', name=str
    # )

    AlreadyBorrowed = ErrorCase(
        msg='Cannot borrow "{name}" as mutable more than once at a time', name=str
    )

    BorrowedAsImmutable = ErrorCase(
        msg='Cannot borrow "{name}" as mutable because it is also borrowed as immutable',
        name=str,
    )

    Unexpected = ErrorCase(
        msg='Cannot borrow "{name}" as mutable because an unexpected '
        'error occurred: "{details}"',
        name=str,
        details=str,
    )
