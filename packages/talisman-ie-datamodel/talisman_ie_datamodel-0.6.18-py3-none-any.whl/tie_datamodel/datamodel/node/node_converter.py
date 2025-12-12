import inspect
from functools import partial, wraps
from typing import Callable, Iterable, Mapping, Type, Union

from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractNode
from tdm.wrapper.node import AbstractNodeWrapper


def _find_appropriate_type(node: AbstractNode, mapping: Mapping[Type[AbstractNode], Type[AbstractNodeWrapper]]) -> AbstractNode:
    for source_type, target_type in mapping.items():
        if isinstance(node, source_type):
            return target_type.wrap(node)
    return node


def _convert_nodes(
        nodes: Iterable[AbstractNode], mapping: Mapping[Type[AbstractNode], Type[AbstractNodeWrapper]]
) -> Iterable[AbstractNode]:
    converted_nodes = [mapping[type(node)].wrap(node) if type(node) in mapping else _find_appropriate_type(node, mapping) for node in nodes]
    return converted_nodes


def _convert_documents(
        documents: Iterable[TalismanDocument],
        mapping: Mapping[Type[AbstractNode], Type[AbstractNodeWrapper]]
) -> Iterable[TalismanDocument]:
    types = Union[tuple(mapping)]
    return [doc.with_nodes(_convert_nodes(doc.get_nodes(types), mapping)) for doc in documents]


def _check_param_annotation(annotation, type_: Type[AbstractNode] | Type[TalismanDocument]) -> bool:
    if annotation is inspect.Signature.empty:
        return False
    try:
        if hasattr(annotation, "__origin__"):  # looks like it is some generic
            return issubclass(annotation.__origin__, Iterable) and issubclass(annotation.__args__[0], type_)
        else:  # hope it is regular class
            return issubclass(annotation, type_)
    except Exception:
        return False


def _convert_document_nodes(
        types: Type[AbstractNodeWrapper] | Iterable[Type[AbstractNodeWrapper]],
        mode: Type[AbstractNode] | Type[TalismanDocument],
        args: tuple[str, ...] | None = None
):
    if isinstance(types, type):
        types = (types,)

    mapping = {}
    for type_ in types:
        # Actually it is some kind of magic. But if wrapper type is built with @generate_wrapper decorator, this code should work properly
        source_type = type_.__orig_bases__[0].__args__[0]
        if source_type in mapping:
            raise ValueError(f"wrapping types collision: {type_} and {mapping[source_type]} wraps the same nodes")
        mapping[source_type] = type_

    if mode is TalismanDocument:
        mapper = partial(_convert_documents, mapping=mapping)
    elif mode is AbstractNode:
        mapper = partial(_convert_nodes, mapping=mapping)
    else:
        raise ValueError

    def decorator(f: Callable):
        signature = inspect.signature(f)
        if args:
            params = args
        else:  # try to determine arguments from method typing (if exists)
            params = [arg for arg, param in signature.parameters.items() if _check_param_annotation(param.annotation, mode)]

        if not params:
            raise ValueError(f"Unable to get appropriate arguments for nodes wrapping from method signature {signature}")

        def maybe_wrap(x):
            if not isinstance(x, Iterable):
                return [x], lambda a: next(iter(a))
            return x, lambda a: a

        @wraps(f)
        def convert(*args, **kwargs):
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            named_args = bound_args.arguments

            for param in params:
                objs, resolver = maybe_wrap(named_args[param])
                converted = mapper(objs)
                named_args[param] = resolver(converted)

            return f(**named_args)

        return convert

    return decorator


def wrap_nodes(types: Type[AbstractNodeWrapper] | Iterable[Type[AbstractNodeWrapper]], *, args: tuple[str, ...] | None = None):
    """
    A decorator that attempts to convert incoming document nodes into wrappers based on specified wrapper types.
    It can convert either individual nodes passed to the decorated function or iterables of nodes.

    NOTE: if Sequence of nodes is passed, it will be converted to an Iterator of nodes.

    @param types: Wrapper types to be used for nodes wrapping.
    @param args: Names of the decorated function parameters to be converted.
    If this parameter is not specified, the decorator will attempt to determine args with respect to typing annotations.
    """
    return _convert_document_nodes(types, AbstractNode, args)


def wrap_document_nodes(types: Type[AbstractNodeWrapper] | Iterable[Type[AbstractNodeWrapper]], *, args: tuple[str, ...] | None = None):
    """
    A decorator that attempts to convert incoming Talisman documents or nodes into wrappers based on specified wrapper types.

    It can convert either individual documents passed to the decorated function or iterables of them.
    NOTE: If a sequence of documents is passed, it will be converted to an Iterator of nodes.

    @param types: Wrapper types to be used for document wrapping.
    @param args: Names of the decorated function parameters to be converted.
    If this parameter is not specified, the decorator will attempt to determine args with respect to typing annotations.
    """
    return _convert_document_nodes(types, TalismanDocument, args)
