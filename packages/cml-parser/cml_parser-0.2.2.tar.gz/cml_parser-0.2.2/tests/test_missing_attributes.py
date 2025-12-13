import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Ensure package import works without installation
sys.path.insert(0, str(ROOT / "src"))

from cml_parser.parser import parse_file_safe

def test_missing_attributes(tmp_path):
    text = """
    ContextMap MyMap {
        type = SYSTEM_LANDSCAPE
        state = TO_BE
        contains MyContext
    }

    Domain MyDomain {
        domainVisionStatement = "A great domain"
    }

    BoundedContext MyContext {
        type = SYSTEM
        domainVisionStatement = "A context vision"
        responsibilities = "Doing things"
        implementationTechnology = "Python"
        knowledgeLevel = CONCRETE
    }

    UseCase MyUseCase {
        actor "User"
        benefit "Value"
        scope "System"
        level "Summary"
    }
    """
    file_path = tmp_path / "missing_attrs.cml"
    file_path.write_text(text, encoding="utf-8")
    cml = parse_file_safe(str(file_path))
    assert cml.parse_results.errors == []

    # ContextMap
    cm = cml.context_maps[0]
    assert cm.type == "SYSTEM_LANDSCAPE"
    assert cm.state == "TO_BE"

    # Domain
    d = cml.domains[0]
    assert d.vision == "A great domain"

    # Context
    ctx = cm.get_context("MyContext")
    assert ctx
    assert ctx.type == "SYSTEM"
    assert ctx.vision == "A context vision"
    assert ctx.responsibilities == "Doing things"
    assert ctx.implementation_technology == "Python"
    assert ctx.knowledge_level == "CONCRETE"

    # UseCase
    uc = cml.get_use_case("MyUseCase")
    assert uc
    assert uc.actor == "User"
    assert uc.benefit == "Value"
    assert uc.scope == "System"
    assert uc.level == "Summary"
