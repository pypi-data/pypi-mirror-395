from mypy.mro import calculate_mro
from mypy.nodes import GDEF, Block, ClassDef, SymbolTable, SymbolTableNode, TypeInfo
from mypy.plugin import AttributeContext, ClassDefContext, DynamicClassDefContext, Plugin
from mypy.types import Instance, Type


def _base_cls_hook(ctx: ClassDefContext) -> None:
    if ctx.cls.fullname == 'greyhorse.error.ErrorCase':
        pass


def _dynamic_class_hook(ctx: DynamicClassDefContext) -> None:
    cls = ClassDef(ctx.name, Block([]))
    cls.fullname = ctx.api.qualified_name(ctx.name)
    sym = ctx.api.lookup_fully_qualified_or_none(ctx.api.type.fullname)
    base = Instance(sym.node, [])

    info = TypeInfo(SymbolTable(), cls, ctx.api.cur_mod_id)
    info.bases = [base]
    cls.info = info
    calculate_mro(info)
    ctx.api.add_symbol_table_node(ctx.name, SymbolTableNode(GDEF, info))


def _class_attribute_hook(ctx: AttributeContext) -> Type:
    return ctx.type


class APIClientPlugin(Plugin):
    def get_base_class_hook(self, fullname: str):
        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo) and fullname.startswith('greyhorse'):
            print(f'base_class: {fullname}')
            return _base_cls_hook
        return None

    def get_dynamic_class_hook(self, fullname: str):
        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo):
            for name in ('greyhorse.enum', 'greyhorse.result'):
                if fullname.startswith(name):
                    print(f'dynamic_class: {fullname}')
                    return _dynamic_class_hook
        return None

    # def get_class_attribute_hook(self, fullname: str) -> Callable[[AttributeContext], Type] | None:
    #     sym = self.lookup_fully_qualified(fullname)
    #     if sym and isinstance(sym.node, TypeInfo):
    #         if fullname.startswith('greyhorse'):
    #             print(f'class_attribute: {fullname}')
    #             return _class_attribute_hook


def plugin(version: str):
    return APIClientPlugin
