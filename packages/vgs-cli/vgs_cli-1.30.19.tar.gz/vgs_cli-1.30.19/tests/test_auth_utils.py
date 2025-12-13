from vgscli.auth_utils import generate_code_verifier, code_challenge


def test_generate_code_verifier():
    code_verifier = generate_code_verifier()
    fixed_code_verifier = generate_code_verifier(20)
    assert len(code_verifier) == 64
    assert len(fixed_code_verifier) == 20


def test_code_challenge():
    code_verifier = generate_code_verifier()
    code_challenge(code_verifier)
