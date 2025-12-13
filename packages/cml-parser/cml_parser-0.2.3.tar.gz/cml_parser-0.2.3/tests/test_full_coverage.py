import os
import sys
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Ensure package import works without installation
sys.path.insert(0, str(ROOT / "src"))

from cml_parser.parser import parse_file
from cml_parser.cml_objects import (
    RelationshipType,
    SubdomainType,
    Stakeholder,
    ValueRegister,
    Application,
    CommandEvent,
    DataTransferObject,
    Module,
)

def test_full_coverage():
    cml_file = Path(__file__).with_name("test_full_coverage.cml")
    cml = parse_file(str(cml_file))
    
    # 1. Verify Context Map & Relationships
    assert len(cml.context_maps) == 1
    cm = cml.context_maps[0]
    assert len(cm.relationships) == 1
    rel = cm.relationships[0]
    assert rel.left.name == "CustomerManagement"
    assert rel.right.name == "PolicyManagement"
    assert rel.implementation_technology == "REST/JSON"
    assert rel.downstream_rights == "VETO_RIGHT"
    assert rel.exposed_aggregates == ["PolicyAgg"]
    
    # 2. Verify Application Layer
    ctx = cml.get_context("CustomerManagement")
    assert ctx.application is not None
    app = ctx.application
    assert len(app.commands) == 1
    assert app.commands[0].name == "CreateCustomer"
    assert len(app.flows) == 1
    flow = app.flows[0]
    assert flow.name == "CustomerOnboarding"
    assert len(flow.steps) == 2
    assert flow.steps[0].type == "command"
    assert flow.steps[0].name == "CreateCustomer"
    assert flow.steps[1].type == "event"
    
    # 3. Verify Tactical DDD Extensions
    agg = ctx.get_aggregate("CustomerAgg")
    assert len(agg.command_events) == 1
    assert agg.command_events[0].name == "CreateCustomerCommand"
    assert len(agg.data_transfer_objects) == 1
    assert agg.data_transfer_objects[0].name == "CustomerDTO"
    
    # 4. Verify Modules
    ctx2 = cml.get_context("PolicyManagement")
    assert len(ctx2.modules) == 1
    mod = ctx2.modules[0]
    assert mod.name == "PolicyModule"
    assert len(mod.aggregates) == 1
    assert mod.aggregates[0].name == "PolicyAgg"
    
    # 5. Verify Stakeholders
    assert len(cml.stakeholder_groups) == 1
    group = cml.stakeholder_groups[0]
    assert group.name == "Management"
    assert len(group.stakeholders) == 1
    assert group.stakeholders[0].name == "CEO"
    assert group.stakeholders[0].influence == "High"
    
    assert len(cml.stakeholders) == 1
    assert cml.stakeholders[0].name == "Developer"
    
    # 6. Verify Values
    assert len(cml.value_registers) == 1
    reg = cml.value_registers[0]
    assert reg.name == "MyValues"
    assert reg.context == "CustomerManagement"
    assert len(reg.clusters) == 1
    cluster = reg.clusters[0]
    assert cluster.name == "Efficiency"
    assert cluster.core_value == "EfficiencyValue"
    assert len(cluster.values) == 1
    assert cluster.values[0].name == "EfficiencyValue"
    assert cluster.values[0].is_core is True
