from __future__ import annotations

import inspect
import typing
import weakref
from collections import defaultdict
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum
from itertools import accumulate
from types import NoneType
from typing import Any, cast, override

# import networkx as nx
# from matplotlib.pyplot import plot
from greyhorse.app.abc.collections.registries import Registry
from greyhorse.app.abc.collections.selectors import Selector, SelectorCombiner
from greyhorse.app.abc.resources.common import ResourceEventKind
from greyhorse.app.abc.resources.providers import ProviderListenerFn, ProviderSubscription
from greyhorse.app.private.collections.registries import DictRegistry, MutDictRegistry
from greyhorse.app.private.runtime.invoke import invoke_sync
from greyhorse.factory import CachePolicy, Factory, into_factory
from greyhorse.maybe import Just, Maybe, Nothing
from greyhorse.utils.types import is_maybe, is_optional, unwrap_maybe, unwrap_optional


def test_domain_service_factory() -> None:
    ...
    # def f1(a: int)->float:
    #     return float(a)
    #
    # def f11(a0: int)->float:
    #     return float(a0) + 10
    #
    # def f2(a: float)->Decimal:
    #     return Decimal(a)
    #
    # def f3(a: int)->str:
    #     return str(a)
    #
    # f1f = into_factory(f1)
    # f2f = into_factory(f2)
    # f3f = into_factory(f3)
    #
    # assert compositor.add(float, f1f, domain='1', scope=TestLifetime.DOMAIN)
    # assert compositor.add(float, into_factory(f11), domain='1', scope=TestLifetime.OPERATION)
    # assert compositor.add(Decimal, f2f, domain='1', scope=TestLifetime.DOMAIN)
    # assert compositor.add(Decimal, f2f, domain='2', scope=TestLifetime.DOMAIN)
    # assert compositor.add(str, f3f, domain='1', scope=TestLifetime.DOMAIN)
    # assert compositor.add(int, into_factory(lambda: 999, int), domain='1', scope=TestLifetime.DOMAIN)
    # assert compositor.add(int, into_factory(lambda: 999, int), domain='2', scope=TestLifetime.OPERATION)
    #
    # assert compositor.has_provider_signature(Callable[[float], Decimal], domain='1', scope=TestLifetime.DOMAIN)
    # assert compositor.has_provider_signature(Callable[[int], Decimal], domain='1', scope=TestLifetime.DOMAIN)
    # assert compositor.has_provider_signature(Callable[[int], Decimal], domain='2', scope=TestLifetime.OPERATION)

    # fff = compositor.get_provider(Decimal, domain='2', scope=TestLifetime.DOMAIN).unwrap()
    # vvv = fff(123.0)

    # state_ctx = StateContext(TestLifetime, compositor, domain='1')
    #
    # with state_ctx as sel:
    #     assert sel.has(float)
    #     res1 = sel.get(float).unwrap()
    #
    #     with state_ctx as sel1:
    #         assert sel1.has(float)
    #         res2 = sel1.get(float).unwrap()
    #
    #         with state_ctx as sel2:
    #             assert sel2.has(float)
    #             res3 = sel2.get(float).unwrap()
    #
    # assert compositor.remove(float, f1f, domain='1')
    # assert compositor.remove(Decimal, f2f, domain='2')
    # assert compositor.remove(str, f3f, domain='1')

    # assert fragment.add_provider(Decimal, into_factory(Decimal(123)), scope=ModuleScope.MODULE)

    # def decimal_op(value: Decimal) -> int:
    #     return int(value.to_integral_value())

    # assert fragment.add_provider(int, into_factory(decimal_op))

    # frag_ctx = fragment.get_context()

    # assert fragment.has_factory(float)

    # ctx = domain.get_factory_ctx(float).unwrap()
    #
    # with ctx as fn:
    #     assert fn.check_signature(Callable[[], float])
    #     assert fn.check_signature(Callable[[Decimal], float])
    #     fff = fn()
    #     assert float(7890.0) == fff
    #     fn.destroy(fff)
    #
    # ctx = domain.get_factory_ctx(str).unwrap()
    #
    # with ctx as fn:
    #     assert fn.check_signature(Callable[[], str])
    #     assert fn.check_signature(Callable[[Decimal], str])
    #     assert fn.check_signature(Callable[[float], str])
    #     assert fn.check_signature(Callable[[float, Decimal], str])
    #     fff = fn()
    #     assert '579' == fff
    #     fn.destroy(fff)

    # builder = ContextBuilder[SyncContext, TestDataClass](TestDataClass)
    # op = domain.get_provider(float).unwrap()
    # builder.add_param('f1', op)
    # op = domain.get_provider(str).unwrap()
    # builder.add_param('f2', op)
    # ctx = builder.build()
    #
    # with ctx as ddd:
    #     assert ddd.f1.check_signature(Callable[[], float])
    #     assert ddd.f2.check_signature(Callable[[float], str])
    #     composite_f = SyncCompositeFactory[str](ddd.f1, ddd.f2, scoped=True)
    #     assert composite_f.check_signature(Callable[[], str])
    #     v = composite_f()
    #     composite_f.destroy(v)


_Source = typing.NewType('Source', NoneType)
_Sink = typing.NewType('Sink', NoneType)


@dataclass(slots=True, frozen=True, kw_only=True)
class _FactorySchedule[S: IntEnum]:
    factory: Factory[Any]
    policy: CachePolicy
    scoped: bool
    is_async: bool
    scope: S | None


class FactoryCompositor(MutFactoryRegistry, ProviderSubscription):
    __slots__ = ('_deps', '_graph', '_listeners')

    def __init__(self) -> None:
        self._graph = nx.MultiDiGraph()
        self._deps: dict[str, set[type]] = defaultdict(set)
        self._listeners = MutDictRegistry[type, ProviderListenerFn](allow_many=True)

    def clear(self) -> None:
        self._deps.clear()
        self._graph.clear()

    @override
    def has_factory[T, S: IntEnum](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        object_selector: Selector[type, Any] | None = None,
        domain: str = '',
        scope: S | None = None,
        **filters: Any,
    ) -> bool:
        view = self._get_search_view(domain, scope)

        if target_type is None:
            sig_ret_type = signature.__args__[-1]
            for ret_type in view.nodes:
                if ret_type in (_Source, _Sink):
                    continue
                if issubclass(ret_type, sig_ret_type):
                    target_type = ret_type
                    break
            else:
                return False

        if not view.has_node(target_type):
            return False

        schedule = self._schedule(view, target_type, scope)

        if not schedule:
            return False
        if len(schedule) == 1:
            if signature is None:
                return True
            return schedule[0].factory.check_signature(signature)
        factories: list[Factory[Any]] = [f.factory for f in schedule]
        return self._check_signature(factories, signature, object_selector)

    @override
    def get_factory[T, S: IntEnum](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        object_cache: Registry[type, Any] | None = None,
        domain: str = '',
        scope: S | None = None,
        **filters: Any,
    ) -> Maybe[Factory[T]]:
        view = self._get_search_view(domain, scope)

        if target_type is None:
            sig_ret_type = signature.__args__[-1]
            for ret_type in view.nodes:
                if ret_type in (_Source, _Sink):
                    continue
                if issubclass(ret_type, sig_ret_type):
                    target_type = ret_type
                    break
            else:
                return Nothing

        if not view.has_node(target_type):
            return Nothing

        schedule = self._schedule(view, target_type, scope)

        if not schedule:
            return Nothing
        if len(schedule) == 1:
            if signature is None or schedule[0].factory.check_signature(signature):
                return Just(schedule[0].factory.clone())
            return Nothing

        factories: list[Factory[Any]] = [f.factory for f in schedule]

        if signature is not None and not self._check_signature(
            factories, signature, object_cache
        ):
            return Nothing

        cache_policy = max(CachePolicy.STATIC, *[f.policy for f in schedule])
        scoped: bool = any([f.scoped for f in schedule])
        # is_async: bool = any([f.is_async for f in schedule])

        factory = SyncCompositeFactory[target_type](
            *factories, scoped=scoped, object_cache=object_cache, cache_policy=cache_policy
        )

        return Just(factory)

    @override
    def get_factory_with_metadata[T, S: IntEnum](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        object_cache: Registry[type, Any] | None = None,
        domain: str = '',
        scope: S | None = None,
        **filters: Any,
    ) -> Maybe[tuple[Factory[T], Mapping[str, Any]]]:
        return self.get_factory(
            target_type=target_type,
            signature=signature,
            object_cache=object_cache,
            domain=domain,
            scope=scope,
            **filters,
        ).map(lambda f: (f, {}))

    @override
    def add_factory[T, S: IntEnum](
        self,
        target_type: type[T],
        factory: Factory[T],
        domain: str = '',
        scope: S | None = None,
        **metadata: Any,
    ) -> bool:
        if not issubclass(factory.return_type, target_type):
            return False

        node_metadata = {'domains': {domain}}
        edge_metadata = {'domains': {domain}, 'scope': scope}

        if target_type is None:
            self._graph.add_node(_Sink)
            target_type = _Sink

        elif self._graph.has_node(target_type):
            data = self._graph.nodes[target_type]
            if 'domains' not in data:
                data['domains'] = set()
            data['domains'].add(domain)
        else:
            self._graph.add_node(target_type, **node_metadata)

        if target_type in self._deps[domain]:
            self._deps[domain].remove(target_type)

        if not factory.actual_params:
            self._graph.add_edge(_Source, target_type, factory=factory, **edge_metadata)
        else:
            for param_type in factory.actual_params.values():
                stripped_param_type = unwrap_maybe(unwrap_optional(param_type))
                if not self._graph.has_node(stripped_param_type):
                    self._deps[domain].add(stripped_param_type)

                self._graph.add_edge(
                    stripped_param_type, target_type, factory=factory, **edge_metadata
                )

        event = ProviderEvent(
            kind=ResourceEventKind.SETUP, target=factory, type=target_type, metadata=metadata
        )
        filter = _CovariantListenersFilter(kind=ResourceEventKind.SETUP, key=target_type)

        for _, listener, __ in self._listeners.filter(filter):
            listener(event)

        return True

    @override
    def remove_factory[T, S: IntEnum](
        self,
        target_type: type[T],
        factory: Factory[T] | None = None,
        domain: str = '',
        scope: S | None = None,
        **metadata: Any,
    ) -> bool:
        def filter_nodes(in_type: type) -> bool:
            data = self._graph.nodes[in_type]
            return domain in data['domains'] if 'domains' in data else True

        if factory is None:

            def filter_edges(in_type: type, out_type: type, k: int) -> bool:
                data = self._graph[in_type][out_type][k]
                res = domain in data['domains']
                if scope is None:
                    res &= data['scope'] is None
                else:
                    res &= (data['scope'] or 0) <= scope
                return res and out_type is target_type

        else:

            def filter_edges(in_type: type, out_type: type, k: int) -> bool:
                data = self._graph[in_type][out_type][k]
                res = domain in data['domains']
                if scope is None:
                    res &= data['scope'] is None
                else:
                    res &= (data['scope'] or 0) <= scope
                return res and data.get('factory') == factory

        view = cast(
            nx.MultiDiGraph,
            nx.subgraph_view(self._graph, filter_node=filter_nodes, filter_edge=filter_edges),
        )

        if not view.has_node(target_type):
            return Nothing

        old_predecessors = list(view.pred[target_type])
        edges_to_remove = list(view.edges.data('factory', keys=True))
        factories_to_remove = {f for _1, _2, _3, f in edges_to_remove}
        self._graph.remove_edges_from(edges_to_remove)
        has_successors = len(view.succ[target_type]) > 0

        if has_successors:
            self._deps[domain].add(target_type)
        else:
            domains = self._graph.nodes[target_type]['domains']
            domains.remove(domain)
            if not domains:
                self._graph.remove_node(target_type)
            if target_type in self._deps[domain]:
                self._deps[domain].remove(target_type)

        for pred_type in old_predecessors:
            if len(view.succ[pred_type]) == 0:
                self._graph.remove_node(pred_type)
                if pred_type in self._deps[domain]:
                    self._deps[domain].remove(pred_type)

        filter = _CovariantListenersFilter(kind=ResourceEventKind.TEARDOWN, key=target_type)

        for orig_fn in factories_to_remove:
            event = ProviderEvent(
                kind=ResourceEventKind.TEARDOWN,
                target=orig_fn,
                type=target_type,
                metadata=metadata,
            )

            for _, listener, __ in self._prov_listeners.filter(filter):
                listener(event)

        return True

    @override
    def add_provider_listener[T](
        self,
        key: type[T],
        fn: ProviderListenerFn,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool:
        return self._listeners.add(key, fn, kind=kind)

    @override
    def remove_provider_listener[T](
        self,
        key: type[T],
        fn: ProviderListenerFn | None = None,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool:
        filter = _CovariantListenersFilter(kind=kind, key=key)
        to_remove = []

        for t, orig_fn, metadata in self._listeners.filter(filter):
            if fn is None or fn == orig_fn:
                to_remove.append((t, orig_fn, metadata['kind']))

        res = False

        for key, orig_fn, orig_kind in to_remove:
            new_kind = orig_kind & ~kind
            res |= self._listeners.remove(key, orig_fn)
            if new_kind != ResourceEventKind(0):
                self._listeners.add(key, orig_fn, kind=new_kind)

        return res

    def _get_search_view[S: IntEnum](
        self, domain: str = '', scope: S | None = None
    ) -> nx.MultiDiGraph:
        def filter_nodes(in_type: type) -> bool:
            data = self._graph.nodes[in_type]
            return domain in data['domains'] if 'domains' in data else True

        def filter_edges(in_type: type, out_type: type, k: int) -> bool:
            data = self._graph[in_type][out_type][k]
            res = domain in data['domains']
            if scope is None:
                res &= data['scope'] is None
            else:
                res &= (data['scope'] or 0) <= scope
            return res

        return cast(
            nx.MultiDiGraph,
            nx.subgraph_view(self._graph, filter_node=filter_nodes, filter_edge=filter_edges),
        )

    @staticmethod
    def _schedule[T, S: IntEnum](
        view: nx.MultiDiGraph, target_type: type[T], scope: S | None = None
    ) -> list[_FactorySchedule]:
        factories: dict[type, list[_FactorySchedule]] = defaultdict(list)
        type_schedule: list[type] = []
        result: list[_FactorySchedule] = []

        for in_type, out_type, k, _ in nx.edge_bfs(view, target_type, orientation='reverse'):
            data = view.get_edge_data(in_type, out_type, k)
            factory = data['factory']
            factory_scope: S | None = data.get('scope')

            factories[out_type].append(
                _FactorySchedule(
                    factory=factory,
                    policy=factory.cache_policy,
                    scoped=factory.scoped,
                    is_async=factory.is_async,
                    scope=factory_scope,
                )
            )
            if not type_schedule or type_schedule[-1] is not out_type:
                type_schedule.append(out_type)

        for out_type in type_schedule:
            matched: _FactorySchedule | None = None

            for item in factories[out_type]:
                if scope is None and item.scope is None:
                    matched = item
                    break
                if scope is None:
                    if item.scope != 0:
                        continue
                    matched = item
                    break
                if item.scope is None:
                    if scope != 0:
                        continue
                    matched = item
                    break

                if (matched is None and item.scope <= scope) or (
                    matched is not None and min(item.scope, scope) > matched.scope
                ):
                    matched = item

            if matched is None:
                return []
            result.append(matched)

        return result

    @staticmethod
    def _check_signature(
        factories: list[Factory[Any]],
        signature: type[Callable],
        object_selector: Selector[type, Any] | None = None,
    ) -> bool:
        combined_params = []
        has_types = set([f.return_type for f in factories])
        sig_params = signature.__args__[0 : len(signature.__args__) - 1]

        for fn_params in (f.actual_params.values() for f in factories):
            for pt in fn_params:
                if object_selector is not None and object_selector.has(pt):
                    continue
                if pt in has_types and pt not in sig_params:
                    continue
                combined_params.append(pt)

        sig_params_idx = 0

        for param_type in combined_params:
            if sig_params_idx < len(sig_params):
                sig_param_type = sig_params[sig_params_idx]

                if is_maybe(param_type):
                    fit = issubclass(unwrap_maybe(sig_param_type), param_type)
                elif is_optional(param_type):
                    fit = issubclass(unwrap_optional(sig_param_type), param_type)
                elif inspect.isclass(sig_param_type):
                    fit = issubclass(sig_param_type, param_type)
                else:
                    fit = sig_param_type is param_type

                if fit:
                    sig_params_idx += 1
                    continue

            if not is_optional(param_type) and not is_maybe(param_type):
                return False

        return sig_params_idx == len(sig_params)


class SyncCompositeFactory[T](Factory[T]):
    __slots__ = ('_finalizers', '_object_cache', '_schedule', '_scoped')

    def __init__(
        self,
        *factories: Factory[Any],
        scoped: bool,
        args: Mapping[str, Any] | None = None,
        object_cache: DictRegistry[type, Any] | None = None,
        cache_policy: CachePolicy = CachePolicy.VOLATILE,
    ) -> None:
        combined_params = {}
        args = args if args else {}
        has_types = set([f.return_type for f in factories])

        for fn_params in (f._params for f in factories):
            combined_params.update({
                p.name: p.type for p in fn_params if p.type not in has_types
            })
            args.update({
                p.name: p.value
                for p in fn_params
                if p.type not in has_types and p.value is not None
            })

        super().__init__(combined_params, args, cache_policy)
        self._schedule = factories
        self._scoped = scoped
        self._object_cache = object_cache
        self._finalizers: dict[int, list[tuple[Factory[Any], Any]]] = {}

    @property
    def scoped(self) -> bool:
        return self._scoped

    @override
    def create[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        actual_args = DictRegistry[type, Any]()

        for param_name, param_value in self._prepare_kwargs(*args, **kwargs).items():
            pd = self._params[self._name_map[param_name]]
            if pd.is_required or param_value is not None:
                actual_args.add(pd.type, param_value)

        factory_cache = DictRegistry[type, Factory[Any]]()
        object_cache = MutDictRegistry[type, Any]()
        selectors = (
            [actual_args, object_cache]
            if self._object_cache is None
            else [actual_args, object_cache, self._object_cache]
        )
        cache_selector = SelectorCombiner[type, Any](*selectors)
        finalizers: list[tuple[Factory[Any], Any | weakref.ref]] = []

        res: T = None

        for i, factory in enumerate(self._schedule):
            last_factory = i == len(self._schedule) - 1
            res_type = factory.return_type

            if actual_args.has(res_type):
                continue

            kwargs: dict[str, Any] = {}

            for param_name, param_type in factory.actual_params.items():
                stripped_param_type = unwrap_maybe(unwrap_optional(param_type))

                if param_value := cache_selector.get(stripped_param_type):
                    kwargs[param_name] = (
                        param_value if is_maybe(param_type) else param_value.unwrap()
                    )

                elif factory_cache.has(stripped_param_type):
                    param_factory, param_kwargs = factory_cache.get_with_metadata(
                        stripped_param_type
                    ).unwrap()
                    param_value = invoke_sync(param_factory.create, **param_kwargs)

                    if param_factory.scoped:
                        finalizers.append(self._create_finalizer(param_factory, param_value))
                    if param_factory.cache_policy < CachePolicy.VOLATILE:
                        object_cache.add(stripped_param_type, param_value)
                    if (
                        param_factory.cache_policy < CachePolicy.SCOPED
                        and self._object_cache is not None
                    ):
                        self._object_cache.add(stripped_param_type, param_value)

                    kwargs[param_name] = (
                        Just(param_value) if is_maybe(param_type) else param_value
                    )

                elif is_maybe(param_type):
                    kwargs[param_name] = Nothing
                elif is_optional(param_type):
                    kwargs[param_name] = None

            if not last_factory:
                factory_cache.add(res_type, factory, **kwargs)
                continue

            res = invoke_sync(factory.create, **kwargs)

            if factory.scoped:
                finalizers.append(self._create_finalizer(factory, res))
            if factory.cache_policy < CachePolicy.SCOPED and self._object_cache is not None:
                self._object_cache.add(res_type, res)

        self._finalizers[id(res)] = finalizers
        return res

    @override
    def destroy(self, instance: T) -> None:
        key = id(instance)

        if finalizers := self._finalizers.get(key):
            for factory, instance in reversed(finalizers):
                if isinstance(instance, weakref.ref):
                    instance = instance()
                invoke_sync(factory.destroy, instance)

            del self._finalizers[key]

    @override
    def clone(self) -> Factory[T]:
        instance = type(self)(self._schedule, self._scoped, self._cacheable, {})
        self._clone_into(instance)
        return instance

    @override
    def __eq__(self, other: Factory[T]) -> bool:
        return isinstance(other, SyncCompositeFactory) and self._schedule == other._schedule

    def _create_finalizer(self, factory: Factory, instance: Any) -> tuple[Factory[Any], Any]:
        if hasattr(instance, '__weakref__'):
            return factory, weakref.ref(instance)
        return factory, instance


if __name__ == '__main__':
    compositor = FactoryCompositor()

    def f1(a: int) -> float:
        return float(a)

    def f11(a0: int) -> float:
        return float(a0) + 10

    def f2(a: float) -> Decimal:
        return Decimal(a)

    def f3(a: int) -> str:
        return str(a)

    f1f = into_factory(f1)
    f2f = into_factory(f2)
    f3f = into_factory(f3)

    assert compositor.add(float, f1f, domain='Домен А', scope=TestLifetime.DOMAIN)
    assert compositor.add(
        float, into_factory(f11), domain='Домен Б', scope=TestLifetime.OPERATION
    )
    assert compositor.add(Decimal, f2f, domain='Домен А', scope=TestLifetime.DOMAIN)
    assert compositor.add(Decimal, f2f, domain='Домен Б', scope=TestLifetime.OPERATION)
    assert compositor.add(str, f3f, domain='Домен А', scope=TestLifetime.DOMAIN)

    import matplotlib.pyplot as plt

    # limits = plt.axis("off")
    # plt.autoscale(True)

    G = compositor._graph
    # pos = nx.nx_agraph.graphviz_layout(G)
    pos = nx.bfs_layout(G, int, align='horizontal')
    # pos = nx.multipartite_layout(G, subset_key="domains")
    # pos = nx.spring_layout(G)

    # nx.nx_agraph.view_pygraphviz(G, edgelabel=lambda d: d['scope'].name)

    connectionstyle = [f'arc3,rad={r}' for r in accumulate([0.15] * 4)]
    connectionstyle2 = [f'arc3,rad={r}' for r in accumulate([0.35] * 4)]

    elarge = [
        tuple(edge) for *edge, d in G.edges(data=True) if d['scope'] == TestLifetime.DOMAIN
    ]
    esmall = [
        tuple(edge) for *edge, d in G.edges(data=True) if d['scope'] == TestLifetime.OPERATION
    ]

    plot()
    nx.draw_networkx_nodes(G, pos=pos, node_size=1900)
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=4, connectionstyle=connectionstyle)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=esmall,
        width=4,
        alpha=0.5,
        edge_color='b',
        style='dashed',
        connectionstyle=connectionstyle2,
    )
    nx.draw_networkx_labels(
        G, pos, labels={n: n.__name__ for n in G}, font_size=10, font_family='sans-serif'
    )
    nx.draw_networkx_edge_labels(
        G,
        pos=pos,
        connectionstyle=connectionstyle,
        edge_labels={
            tuple(edge): f'{",".join(d["domains"])}, {d["scope"].name}'
            for *edge, d in G.edges(keys=True, data=True)
        },
        # bbox={"alpha": 0},
        # label_pos=1.3,
        # font_color="blue",
    )

    ax = plt.gca()
    ax.margins(0.20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
