from abc import ABCMeta

from tdm.abstract.datamodel import AbstractMarkup
from tdm.datamodel.nodes import TableNode
from tdm.wrapper.node import AbstractNodeWrapper, composite_markup, generate_wrapper

from .abstract import AbstractTIETableNode
from .markup import TIETableNodeMarkup


@composite_markup(tab=TIETableNodeMarkup)
class _CompositeTableMarkup(AbstractMarkup, AbstractTIETableNode, metaclass=ABCMeta):
    pass


@generate_wrapper(_CompositeTableMarkup)
class TIETableNode(TableNode, AbstractTIETableNode, AbstractNodeWrapper[TableNode], metaclass=ABCMeta):
    pass
