#!/usr/bin/env python
################################################################
import inspect

import transaction
from ZODB.POSException import ConflictError

from . import bdlogging

################################################################
print = bdlogging.invalidPrint
logger = bdlogging.getLogger(__name__)
################################################################


def explain_conflict(e, obj):

    if hasattr(obj, "connection"):
        conn = obj.connection
    elif hasattr(obj, "base"):
        conn = obj.base.connection
    else:
        conn = None

    if conn:
        oid = e.oid
        obj = conn.get(oid)  # fetch the actual BTree
        logger.warning(f"Conflicted object: {obj} {type(obj)}")
        import BTrees.OOBTree

        if isinstance(obj, BTrees.OOBTree.OOBTree):
            logger.warning([e for e in obj.items()])
            if "id" in obj.keys():
                logger.warning(f"id: {obj['id']}")

    import traceback

    logger.warning("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    logger.warning("".join(traceback.format_stack()))


################################################################


def execute_generator_func(foo, *args, **kwargs):
    name = foo.__name__
    logger.debug(f"Execute generator {name}")
    gen = foo(*args, **kwargs)
    return execute_generator(name, gen)


################################################################


def execute_func(foo, *args, **kwargs):
    name = foo.__name__
    logger.debug(f"Execute normal function {name}")
    return foo(*args, **kwargs)


################################################################


def execute_generator(name, gen, commit=True):
    step = 0

    while True:
        try:
            logger.debug(f"Running step {name}:{step}")
            temp_res = next(gen)
            if commit:
                transaction.commit()
            if temp_res is None:
                logger.debug(f"Done step {name}:{step}")
            elif inspect.isgenerator(temp_res):
                temp_res = execute_generator(f"{name}:{step}", temp_res)
                logger.debug(f"Done step {name}:{step} => temp_res")
            else:
                logger.debug(f"Done step {name}:{step} => temp_res")
            step += 1

        except StopIteration as e:
            logger.debug(f"Done generator {name}:{step} => {e.value}")
            return e.value


################################################################


def decorator_transaction(foo, retries=10, verbose=False, stop_on_conflict=True):
    verbose = True
    logger.debug(
        f"Decorate {foo.__name__} {type(foo)} {inspect.isgeneratorfunction(foo)} {foo}"
    )

    executor = execute_func
    if inspect.isgeneratorfunction(foo):
        executor = execute_generator_func

    def _protected_function(self, *args, commit=True, **kwargs):

        logger.debug(
            f"Run decorated {foo.__name__}: commit={commit} transaction={transaction.get()}"
        )

        if verbose:
            logger.debug(
                "Start transaction %s",
                foo.__name__,
            )
        attempts = 0

        try:
            if commit:
                transaction.commit()
                logger.debug(
                    f"Run decorated {foo.__name__}: commit={commit} (after-commit):transaction={transaction.get()}"
                )

        except ConflictError as e:
            explain_conflict(e, self)
            raise e

        while 1:
            try:
                sig = inspect.signature(foo)
                params = sig.parameters
                # Check if "commit" exists and has default value False
                if "commit" in params:
                    kwargs["commit"] = commit
                ret = executor(foo, self, *args, **kwargs)
                if commit:
                    transaction.commit()
                if verbose:
                    logger.debug("End transaction %s", foo.__name__)
                return ret
            except ConflictError as e:
                if verbose:
                    explain_conflict(e, self)
                if verbose:
                    logger.debug("Abort transaction %s", foo.__name__)
                transaction.abort()
                attempts += 1
                if attempts >= retries:
                    if not stop_on_conflict:
                        return None
                    raise e
        logger.debug(f"End decorated {foo.__name__}: commit={commit}")

    return _protected_function


################################################################


def _transaction(func=None, retries=10, verbose=False, stop_on_conflict=True):
    if func is not None:
        return decorator_transaction(
            func, retries=retries, verbose=verbose, stop_on_conflict=stop_on_conflict
        )
    return lambda x: decorator_transaction(
        x, retries=retries, verbose=verbose, stop_on_conflict=stop_on_conflict
    )
