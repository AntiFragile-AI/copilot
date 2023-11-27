from terraform import Terraform, Args

def test_completion():
    args = Args()
    t = Terraform(args)
    resp = t.get_completion_langchain("Make a dynamodb instance called Demo")
    assert resp == "hello"
