import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cml_parser.cml_objects import (
    Parameter, Operation, Attribute, Entity, ValueObject, DomainEvent,
    Enum, Subdomain, SubdomainType, Domain, Aggregate, Service, Repository,
    Context, ContextMap, Relationship, UseCase, UserStory, Stakeholder,
    StakeholderGroup, Value, ValueCluster, ValueRegister, Command, FlowStep,
    Flow, Coordination, Application, CommandEvent, DataTransferObject, Module,
    CML, Diagnostic, ParseResult
)

def test_object_reprs_and_methods():
    # Diagnostic and ParseResult
    d = Diagnostic(message="Msg", line=1, col=2, filename="f.cml", expected=["A", "B"])
    assert "f.cml:1:2" in d.pretty()
    assert "expected: A, B" in d.pretty()
    
    d2 = Diagnostic(message="Msg")
    assert d2.pretty() == "Msg"

    d3 = Diagnostic(message="Msg", line=1)
    assert "f.cml:1" in d.pretty() or ":1" in d3.pretty()
    
    pr = ParseResult(model=None, errors=[d], warnings=[d], filename="test.cml")
    assert pr.ok is False
    assert "errors=1" in repr(pr)
    assert pr.to_dict()["filename"] == "test.cml"
    
    pr_ok = ParseResult(model="M", errors=[], warnings=[])
    assert pr_ok.ok is True
    assert "OK" in repr(pr_ok)

    # Parameter
    p = Parameter(name="p", type="String", is_reference=True)
    assert "@String p" in repr(p)

    # Operation
    op = Operation(name="op", return_type="void", parameters=[p])
    assert "op(@String p) -> void" in repr(op)

    # Attribute
    attr = Attribute(name="a", type="int", is_reference=True, is_key=True)
    assert "-int a key" in repr(attr)

    # Entity
    ent = Entity(name="E", is_aggregate_root=True)
    ent.attributes.append(attr)
    ent.operations.append(op)
    assert "E (root)" in repr(ent)
    assert ent.get_attribute("a") == attr
    assert ent.get_attribute("missing") is None
    assert ent.get_operation("op") == op
    assert ent.get_operation("missing") is None

    # ValueObject
    vo = ValueObject(name="VO")
    vo.attributes.append(attr)
    vo.operations.append(op)
    assert "VO" in repr(vo)
    assert vo.get_attribute("a") == attr
    assert vo.get_operation("op") == op

    # DomainEvent
    de = DomainEvent(name="DE")
    de.attributes.append(attr)
    de.operations.append(op)
    assert "DE" in repr(de)
    assert de.get_attribute("a") == attr
    assert de.get_operation("op") == op

    # Enum
    en = Enum(name="S", is_aggregate_lifecycle=True)
    assert "S (lifecycle)" in repr(en)

    # Subdomain
    sd = Subdomain(name="SD", type=SubdomainType.CORE, vision="V")
    assert "SD" in repr(sd)
    sd.entities.append(ent)
    assert sd.get_entity("E") == ent
    assert sd.get_entity("missing") is None
    
    ctx_impl = Context(name="Impl")
    sd.implementations.append(ctx_impl)
    assert sd.get_implementation("Impl") == ctx_impl
    assert sd.get_implementation("missing") is None

    # Domain
    dom = Domain(name="D", vision="V")
    dom.subdomains.append(sd)
    assert "D" in repr(dom)
    assert dom.core == [sd]
    assert dom.supporting == []
    assert dom.generic == []
    assert dom.get_subdomain("SD") == sd
    assert dom.get_subdomain("missing") is None

    # Service
    svc = Service(name="Svc")
    svc.operations.append(op)
    assert "Svc" in repr(svc)
    assert svc.get_operation("op") == op
    assert svc.get_operation("missing") is None

    # Repository
    repo = Repository(name="Repo")
    repo.operations.append(op)
    assert "Repo" in repr(repo)
    assert repo.get_operation("op") == op

    # CommandEvent
    ce = CommandEvent(name="CE")
    ce.attributes.append(attr)
    assert "CE" in repr(ce)
    assert ce.get_attribute("a") == attr

    # DataTransferObject
    dto = DataTransferObject(name="DTO")
    dto.attributes.append(attr)
    assert "DTO" in repr(dto)
    assert dto.get_attribute("a") == attr

    # Aggregate
    agg = Aggregate(name="Agg")
    agg.entities.append(ent)
    agg.value_objects.append(vo)
    agg.domain_events.append(de)
    agg.services.append(svc)
    agg.repositories.append(repo)
    agg.enums.append(en)
    assert "Agg" in repr(agg)
    assert agg.get_entity("E") == ent
    assert agg.get_value_object("VO") == vo
    assert agg.get_domain_event("DE") == de
    assert agg.get_service("Svc") == svc
    assert agg.get_repository("Repo") == repo
    assert agg.get_enum("S") == en
    
    assert agg.get_entity("missing") is None
    assert agg.get_value_object("missing") is None
    # ... assert missing for others

    # Context
    ctx = Context(name="Ctx")
    ctx.aggregates.append(agg)
    ctx.services.append(svc)
    ctx.implements.append(sd)
    assert "BoundedContext(Ctx)" in repr(ctx)
    assert ctx.get_subdomain("SD") == sd
    assert ctx.get_subdomain("missing") is None
    assert ctx.get_aggregate("Agg") == agg
    assert ctx.get_service("Svc") == svc
    assert ctx.get_aggregate("missing") is None

    # ContextMap and Relationship
    ctx2 = Context(name="Ctx2")
    rel = Relationship(left=ctx, right=ctx2, type="Customer-Supplier", roles=["Customer", "Supplier"])
    assert "Ctx -> Ctx2" in repr(rel)
    
    cm = ContextMap(name="Map", type="SYSTEM_LANDSCAPE", state="AS_IS")
    cm.contexts = [ctx, ctx2]
    cm.relationships = [rel]
    assert "Map" in repr(cm)
    assert cm.get_context("Ctx") == ctx
    assert cm.get_context("missing") is None
    
    rels = cm.get_context_relationships("Ctx")
    assert rel in rels
    
    assert cm.get_relationship("Ctx", "Ctx2") == rel
    assert cm.get_relationship("Ctx2", "Ctx") == rel
    assert cm.get_relationship("Ctx", "Missing") is None

    # Relationship filtering
    assert cm.get_relationships_by_type("Customer-Supplier") == [rel]
    assert cm.get_relationships_by_type("Partnership") == []
    assert cm.get_relationships_by_type("Customer") == [rel] # by role

    # Other simple reprs
    uc = UseCase(name="UC")
    assert "UC" in repr(uc)
    
    us = UserStory(name="US")
    assert "US" in repr(us)

    sh = Stakeholder(name="SH")
    assert "SH" in repr(sh)

    shg = StakeholderGroup(name="SHG")
    assert "SHG" in repr(shg)

    val = Value(name="Val")
    assert "Val" in repr(val)

    vc = ValueCluster(name="VC")
    assert "VC" in repr(vc)

    vr = ValueRegister(name="VR")
    assert "VR" in repr(vr)

    cmd = Command(name="Cmd")
    assert "Cmd" in repr(cmd)

    fs = FlowStep(type="command", name="Cmd")
    assert "FlowStep" in repr(fs)

    flow = Flow(name="Flow")
    assert "Flow" in repr(flow)

    coord = Coordination(name="Coord")
    assert "Coord" in repr(coord)

    app = Application()
    assert "Application" in repr(app)

    mod = Module(name="Mod")
    assert "Mod" in repr(mod)

    # CML
    cml = CML()
    cml.parse_results = pr_ok
    cml.context_maps.append(cm)
    cml.domains.append(dom)
    cml.contexts.append(ctx)
    cml.use_cases.append(uc)
    assert "CML" in repr(cml)
    
    assert cml.get_domain("D") == dom
    assert cml.get_domain("missing") is None
    
    assert cml.get_context_map("Map") == cm
    assert cml.get_context_map("missing") is None
    
    assert cml.get_context("Ctx") == ctx
    assert cml.get_context("missing") is None
    
    assert cml.get_aggregate("Agg", context_name="Ctx") == agg
    assert cml.get_aggregate("Agg") == agg
    assert cml.get_aggregate("missing") is None
    
    assert cml.get_entity("E", context_name="Ctx", aggregate_name="Agg") == ent
    assert cml.get_entity("E") == ent
    assert cml.get_entity("missing") is None

    assert cml.get_use_case("UC") == uc
    assert cml.get_use_case("missing") is None
    
    assert cml.get_subdomain("SD", domain_name="D") == sd
    assert cml.get_subdomain("SD") == sd
    assert cml.get_subdomain("missing") is None
