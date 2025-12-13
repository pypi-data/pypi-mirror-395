import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cml_parser import parse_text
from cml_parser.cml_objects import SubdomainType

def test_builder_coverage_scenarios():
    cml_text = """
    ContextMap Map {
        type = ORGANIZATIONAL
        state = TO_BE
        contains Ctx1, Ctx2
    }

    BoundedContext Ctx1 {
        implementationTechnology = "Java"
        knowledgeLevel = CONCRETE
        type = SYSTEM
        responsibilities = "Resp1"
    }

    BoundedContext Ctx2 implements GenericSub {
    }

    Domain D {
        Subdomain GenericSub type GENERIC_SUBDOMAIN {
            domainVisionStatement = "SubVision"
        }
        
        Subdomain InvalidAttrSub {
            // "type = FEATURE" is parsed as BoundedContextAttribute
            // Subdomain has 'type' attribute. Visitor will assign string "FEATURE".
            type = FEATURE 
        }
    }

    BoundedContext AggrContext {
        Aggregate Aggr {
            knowledgeLevel = ABSTRACT
            responsibilities = "AggResp"
    
            // Aggregate does not have vision, so this should trigger the check failure path (coverage)
            domainVisionStatement = "AggVision"
    
            // Aggregate does not have implementationTechnology
            implementationTechnology = "AggTech"
        }
    }
    
    // Flow coverage
    BoundedContext P {
        Application {
             Flow MyFlow {
                 command C1;
                 command C2 delegates to Thing [ -> State ];
                 command C3 emits event E1;
                 
                 event E1 triggers C2;
                 event E2 + E3 triggers Op1 + Op2;
                 
                 operation Op1;
             }
        }
    }
    
    // Value Register and Stakeholders
    ValueRegister VR for P {
        ValueCluster VC {
            core CoreVal
            demonstrator "Demo"
            Value V1 {
                isCore
                demonstrator "VDemo"
                Stakeholder SH1 {}
            }
        }
    }
    """
    
    model = parse_text(cml_text)
    
    # ContextMap
    cm = model.get_context_map("Map")
    assert cm.type == "ORGANIZATIONAL"
    assert cm.state == "TO_BE"
    # check contains link
    ctx1 = model.get_context("Ctx1")
    ctx2 = model.get_context("Ctx2")
    assert ctx1 in cm.contexts
    assert ctx2 in cm.contexts
    
    # Ctx1 attributes
    assert ctx1.knowledge_level == "CONCRETE"
    assert ctx1.implementation_technology == "Java"
    assert ctx1.type == "SYSTEM"
    assert ctx1.responsibilities == "Resp1"
    
    # Linkage to subdomain
    sd = model.get_subdomain("GenericSub")
    assert sd in ctx2.implements
    assert ctx2 in sd.implementations
    
    # Subdomain invalid attr override
    # sd_inv = model.get_subdomain("InvalidAttrSub")
    # Actually the parser visitor logic assigns it if hasattr. 
    # Subdomain has 'type' field (Enum). Assigning "FEATURE" (str) works in Python at runtime.
    # assert sd_inv.type == "FEATURE" 

    # Aggregate attributes
    agg = model.get_aggregate("Aggr", context_name=None)
    assert agg.knowledge_level == "ABSTRACT"
    assert agg.responsibilities == "AggResp"
    # Ensure ignored attributes didn't crash
    # (Checking coverage of the 'else' or 'if not hasattr' branches)

    # Flow
    p_ctx = model.get_context("P")
    flow = p_ctx.application.flows[0]
    assert len(flow.steps) > 0
    # command C2 delegates
    step2 = flow.steps[1]
    assert step2.delegate == "Thing"
    
    # event E2 + E3 triggers Op1 + Op2
    # The visitor creates one step per invocation?
    # Let's check the steps
    # C1, C2, C3, E1, E2+E3...
    
    # Value Register
    vr = model.value_registers[0]
    assert vr.name == "VR"
    assert vr.context == "P"
    vc = vr.clusters[0]
    assert vc.core_value == "CoreVal"
    assert vc.demonstrator == "Demo"
    val = vc.values[0]
    assert val.is_core is True
    assert val.demonstrator == "VDemo"
    assert val.stakeholders[0].name == "SH1"
