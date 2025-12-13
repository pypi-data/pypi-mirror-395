import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cml_parser import parse_file_safe

def test_tactical_ddd_objects_basic():
    """Test that tactical DDD objects are parsed with attributes."""
    import tempfile
    from pathlib import Path
    
    cml_content = """
    ContextMap TestMap {
        contains OrderContext
    }
    
    BoundedContext OrderContext {
        Aggregate OrderAggregate {
            owner OrderTeam
            
            Entity Order {
                aggregateRoot
                - OrderId orderId
                String customerName
                - List<OrderLine> orderLines
            }
            
            ValueObject OrderId {
                String id key
            }
            
            ValueObject OrderLine {
                String product
                int quantity
            }
            
            enum OrderStatus {
                CREATED, CONFIRMED, SHIPPED, DELIVERED
            }
            
            Service OrderService {
            }
        }
    }
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cml', delete=False) as f:
        f.write(cml_content)
        temp_path = f.name
    
    try:
        cml = parse_file_safe(temp_path)
        
        # Check parsing succeeded
        assert cml.parse_results.ok, f"Parse failed: {cml.parse_results.errors}"
        
        # Get the context
        cm = cml.get_context_map("TestMap")
        assert cm is not None, "ContextMap not found"
        
        ctx = cm.get_context("OrderContext")
        assert ctx is not None, "BoundedContext not found"
        
        # Check aggregate
        assert len(ctx.aggregates) == 1, f"Expected 1 aggregate, found {len(ctx.aggregates)}"
        agg = ctx.aggregates[0]
        assert agg.name == "OrderAggregate"
        assert agg.owner == "OrderTeam"
        
        # Check entities
        assert len(agg.entities) == 1, f"Expected 1 entity, found {len(agg.entities)}"
        order = agg.entities[0]
        assert order.name == "Order"
        assert order.is_aggregate_root == True
        
        # Check entity attributes
        print(f"Order has {len(order.attributes)} attributes")
        for attr in order.attributes:
            print(f"  - {attr}")
        
        assert len(order.attributes) == 3, f"Expected 3 attributes, found {len(order.attributes)}"
        
        # Check first attribute (orderId)
        order_id_attr = order.get_attribute("orderId")
        assert order_id_attr is not None, "orderId attribute not found"
        assert order_id_attr.is_reference == True, "orderId should be a reference"
        assert "OrderId" in order_id_attr.type
        
        # Check customer name
        name_attr = order.get_attribute("customerName")
        assert name_attr is not None, "customerName attribute not found"
        assert name_attr.type == "String"
        assert name_attr.is_reference == False
        
        # Check value objects
        assert len(agg.value_objects) == 2, f"Expected 2 value objects, found {len(agg.value_objects)}"
        
        order_id_vo = agg.get_value_object("OrderId")
        assert order_id_vo is not None
        assert len(order_id_vo.attributes) == 1
        assert order_id_vo.attributes[0].is_key == True
        
        # Check enums
        assert len(agg.enums) == 1, f"Expected 1 enum, found {len(agg.enums)}"
        status_enum = agg.get_enum("OrderStatus")
        assert status_enum is not None
        assert len(status_enum.values) == 4
        assert "CREATED" in status_enum.values
        
        # Check services
        assert len(agg.services) == 1
        assert agg.services[0].name == "OrderService"
        
        print("✓ All tactical DDD objects tests passed!")
        
    finally:
        Path(temp_path).unlink(missing_ok=True)

if __name__ == "__main__":
    test_tactical_ddd_objects_basic()
