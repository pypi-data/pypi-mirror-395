import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cml_parser.parser import parse_file, parse_text, CmlSyntaxError, main

def test_parser_strict_syntax_error(tmp_path):
    f = tmp_path / "bad.cml"
    f.write_text('ContextMap "M"') # Invalid quotes
    
    with pytest.raises(CmlSyntaxError) as excinfo:
        parse_file(str(f))
    assert "no viable alternative" in str(excinfo.value) or "mismatched input" in str(excinfo.value) or "extraneous input" in str(excinfo.value)

def test_parser_builder_exception():
    with patch('cml_parser.parser.CMLModelBuilder') as MockBuilder:
        mock_instance = MockBuilder.return_value
        mock_instance.visit.side_effect = Exception("Boom")
        
        with pytest.raises(CmlSyntaxError) as excinfo:
            parse_text("ContextMap M {}", strict=True)
        assert "Boom" in str(excinfo.value)

        res = parse_text("ContextMap M {}", strict=False)
        assert res.parse_results.ok is False
        assert len(res.parse_results.errors) > 0
        assert "Boom" in res.parse_results.errors[0].message

def test_repository_logic():
    cml = """
    BoundedContext BC {
        Aggregate Agg {
            Entity E
            Repository Rep {
                void save(@E entity);
            }
        }
    }
    """
    model = parse_text(cml)
    repo = model.contexts[0].aggregates[0].repositories[0]
    assert len(repo.operations) == 1
    assert repo.operations[0].name == "save"

def test_relationship_attributes_extras():
    cml = """
    ContextMap M {
        C1 -> C2 {
             implementationTechnology "REST"
             downstreamRights VETO_RIGHT
             exposedAggregates A1, A2
        }
    }
    BoundedContext C1
    BoundedContext C2
    """
    model = parse_text(cml)
    rel = model.context_maps[0].relationships[0]
    assert rel.implementation_technology == "REST"
    assert rel.downstream_rights == "VETO_RIGHT"
    assert rel.exposed_aggregates == ["A1", "A2"]

def test_use_case_extras():
    cml = """
    UseCase UC {
        scope "S"
        level "L"
        benefit "B"
        interactions
            "Step 1"
            read "Something"
    }
    """
    model = parse_text(cml)
    uc_obj = model.use_cases[0]
    
    assert uc_obj.scope == "S"
    assert uc_obj.level == "L"
    assert uc_obj.benefit == "B"
    assert any("Step 1" in i for i in uc_obj.interactions)
    assert any("read" in i for i in uc_obj.interactions)

def test_value_object_operations_and_visibility():
    cml = """
    BoundedContext BC {
        Module M {
            ValueObject VO {
                private String secret;
                public void getSecret();
            }
        }
    }
    """
    model = parse_text(cml)
    vo = model.contexts[0].modules[0].domain_objects[0]
    attr = vo.attributes[0]
    assert attr.visibility == "private"
    op = vo.operations[0]
    assert op.visibility == "public"

def test_domain_event_operation():
    cml = """
    BoundedContext BC {
        Module M {
            DomainEvent DE {
                void op();
            }
        }
    }
    """
    model = parse_text(cml)
    de = model.get_context("BC").modules[0].domain_objects[0] 
    assert len(de.operations) == 1
    assert de.operations[0].name == "op"

def test_user_story():
    cml = """
    UserStory US {
        As a "User"
        I want to "do something"
        so that "I get benefit"
    }
    """
    model = parse_text(cml)
    assert len(model.user_stories) == 1
    us = model.user_stories[0]
    assert us.name == "US"
    assert us.role == "User"
    assert us.feature == "do something"
    assert us.benefit == "I get benefit"

def test_repository_method_visibility():
    cml = """
    BoundedContext BC {
        Aggregate A {
            Repository R {
                public void save();
                private void internal();
            }
        }
    }
    """
    model = parse_text(cml)
    repo = model.get_context("BC").aggregates[0].repositories[0]
    op1 = repo.operations[0]
    assert op1.name == "save"
    assert op1.visibility == "public"
    op2 = repo.operations[1]
    assert op2.name == "internal"
    assert op2.visibility == "private"

def test_diagnostic_col_none():
    from cml_parser.cml_objects import Diagnostic
    d = Diagnostic(message="Msg", filename="f", line=1, col=None)
    assert d.pretty() == "[f:1] Msg"

def test_stakeholder_full():
    cml = """
    Stakeholders of Project {
        Stakeholder SH {
            influence HIGH
            interest MEDIUM
            impact LOW
            priority HIGH
            consequences good "C1" bad "C2"
        }
    }
    """
    model = parse_text(cml)
    assert len(model.stakeholders) == 1
    sh = model.stakeholders[0]
    assert sh.influence == "HIGH"
    assert sh.interest == "MEDIUM"
    assert sh.consequences == ['good"C1"', 'bad"C2"']

def test_cli_exceptions():
    # parse logic in main is mostly covered, but let's ensure we hit paths
    pass
