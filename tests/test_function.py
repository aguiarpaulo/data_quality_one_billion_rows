from app.function import testing

def test_function_testing():
    output = testing()
    result = 'test is done'
    assert output == result