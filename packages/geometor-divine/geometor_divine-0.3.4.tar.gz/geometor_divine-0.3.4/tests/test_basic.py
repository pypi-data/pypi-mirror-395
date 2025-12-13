from geometor.model import Model
from geometor.divine import register_divine_hook

def test_divine_integration():
    model = Model("divine_test")
    
    # Register the hook
    register_divine_hook(model)
    
    A = model.set_point(0, 0)
    B = model.set_point(1, 0)
    model.construct_line(A, B)
    
    # Just verify we can import and run a function from divine
    import geometor.divine
    assert geometor.divine is not None
