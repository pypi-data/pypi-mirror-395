from .actor import ActorStub


def test_identifiers():
    stub = ActorStub.model_validate({"identifiers": "acct:some@domain"})

    assert stub.identifiers == ["acct:some@domain"]


def test_manually_approves_followers():
    stub = ActorStub.model_validate({"manuallyApprovesFollowers": True})

    assert stub
