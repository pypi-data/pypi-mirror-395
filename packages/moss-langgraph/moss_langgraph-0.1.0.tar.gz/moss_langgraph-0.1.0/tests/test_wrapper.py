import pytest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass, field
from typing import Optional

from moss_langgraph import signed_node, SignedNodeFactory
from moss_langgraph.wrapper import _state_to_payload, _get_or_create_subject, _attach_envelope
from moss import Subject, Envelope


@pytest.fixture
def temp_moss_dir(tmp_path):
    """Use a temporary directory for MOSS data"""
    keys_dir = tmp_path / "keys"
    seq_dir = tmp_path / "seq"
    with patch('moss.keystore.KEYS_DIR', keys_dir), \
         patch('moss.sequence.SEQ_DIR', seq_dir):
        yield tmp_path


class TestStateToPayload:
    def test_dict_state(self):
        state = {"key": "value", "count": 42}
        payload = _state_to_payload(state)
        assert payload == {"key": "value", "count": 42}

    def test_dict_excludes_moss_envelope(self):
        state = {"result": "data", "moss_envelope": "should_be_excluded"}
        payload = _state_to_payload(state)
        assert payload == {"result": "data"}
        assert "moss_envelope" not in payload

    def test_object_with_dict_method(self):
        obj = MagicMock()
        obj.dict = MagicMock(return_value={"from_dict": True, "moss_envelope": "exclude"})
        payload = _state_to_payload(obj)
        assert payload == {"from_dict": True}

    def test_generic_object(self):
        class CustomState:
            def __init__(self):
                self.data = "test"
                self.moss_envelope = "exclude"
        
        obj = CustomState()
        payload = _state_to_payload(obj)
        assert payload == {"data": "test"}


class TestAttachEnvelope:
    def test_dict_state(self):
        state = {"result": "value"}
        envelope = MagicMock(spec=Envelope)
        
        result = _attach_envelope(state, envelope)
        
        assert result["moss_envelope"] is envelope

    def test_object_state(self):
        class State:
            pass
        
        state = State()
        envelope = MagicMock(spec=Envelope)
        
        result = _attach_envelope(state, envelope)
        
        assert result.moss_envelope is envelope


class TestGetOrCreateSubject:
    def test_creates_new_subject(self, temp_moss_dir):
        subject = _get_or_create_subject("moss:flow:new-node")
        assert subject.subject == "moss:flow:new-node"

    def test_loads_existing_subject(self, temp_moss_dir):
        Subject.create("moss:flow:existing")
        subject = _get_or_create_subject("moss:flow:existing")
        assert subject.subject == "moss:flow:existing"


class TestSignedNode:
    def test_wraps_sync_function(self, temp_moss_dir):
        def node_fn(state):
            state["processed"] = True
            return state
        
        wrapped = signed_node(node_fn, "moss:flow:sync")
        
        result = wrapped({"input": "data"})
        
        assert result["processed"] is True
        assert "moss_envelope" in result
        assert isinstance(result["moss_envelope"], Envelope)

    def test_envelope_has_correct_subject(self, temp_moss_dir):
        def node_fn(state):
            return state
        
        wrapped = signed_node(node_fn, "moss:flow:subject-test")
        result = wrapped({})
        
        assert result["moss_envelope"].subject == "moss:flow:subject-test"

    def test_envelope_verifiable(self, temp_moss_dir):
        def node_fn(state):
            state["result"] = "computed"
            return state
        
        wrapped = signed_node(node_fn, "moss:flow:verify")
        result = wrapped({"input": "test"})
        
        verify_result = Subject.verify(result["moss_envelope"], check_replay=False)
        assert verify_result.valid is True

    def test_sequence_increments(self, temp_moss_dir):
        def node_fn(state):
            return state
        
        wrapped = signed_node(node_fn, "moss:flow:seq")
        
        result1 = wrapped({"n": 1})
        result2 = wrapped({"n": 2})
        result3 = wrapped({"n": 3})
        
        assert result1["moss_envelope"].seq == 1
        assert result2["moss_envelope"].seq == 2
        assert result3["moss_envelope"].seq == 3

    def test_none_return_unchanged(self, temp_moss_dir):
        def node_fn(state):
            return None
        
        wrapped = signed_node(node_fn, "moss:flow:none")
        result = wrapped({})
        
        assert result is None

    def test_preserves_function_name(self, temp_moss_dir):
        def my_custom_node(state):
            return state
        
        wrapped = signed_node(my_custom_node, "moss:flow:name")
        
        assert wrapped.__name__ == "my_custom_node"


class TestAsyncSignedNode:
    @pytest.mark.asyncio
    async def test_wraps_async_function(self, temp_moss_dir):
        async def async_node(state):
            state["async_processed"] = True
            return state
        
        wrapped = signed_node(async_node, "moss:flow:async")
        
        result = await wrapped({"input": "data"})
        
        assert result["async_processed"] is True
        assert "moss_envelope" in result
        assert isinstance(result["moss_envelope"], Envelope)

    @pytest.mark.asyncio
    async def test_async_envelope_verifiable(self, temp_moss_dir):
        async def async_node(state):
            state["result"] = "async_computed"
            return state
        
        wrapped = signed_node(async_node, "moss:flow:async-verify")
        result = await wrapped({})
        
        verify_result = Subject.verify(result["moss_envelope"], check_replay=False)
        assert verify_result.valid is True


class TestSignedNodeFactory:
    def test_factory_creates_wrapped_nodes(self, temp_moss_dir):
        factory = SignedNodeFactory("moss:flow:factory")
        
        def node1(state):
            state["step"] = 1
            return state
        
        def node2(state):
            state["step"] = 2
            return state
        
        wrapped1 = factory.wrap(node1)
        wrapped2 = factory.wrap(node2)
        
        result1 = wrapped1({})
        result2 = wrapped2({})
        
        assert result1["moss_envelope"].subject == "moss:flow:factory"
        assert result2["moss_envelope"].subject == "moss:flow:factory"

    def test_factory_sequences_across_nodes(self, temp_moss_dir):
        factory = SignedNodeFactory("moss:flow:shared-seq")
        
        wrapped1 = factory.wrap(lambda s: s)
        wrapped2 = factory.wrap(lambda s: s)
        
        result1 = wrapped1({})
        result2 = wrapped2({})
        
        assert result2["moss_envelope"].seq > result1["moss_envelope"].seq


class TestDataclassState:
    def test_dataclass_state(self, temp_moss_dir):
        @dataclass
        class GraphState:
            input: str = ""
            output: str = ""
            moss_envelope: Optional[Envelope] = None
        
        def node_fn(state: GraphState) -> GraphState:
            state.output = f"processed: {state.input}"
            return state
        
        wrapped = signed_node(node_fn, "moss:flow:dataclass")
        
        state = GraphState(input="test")
        result = wrapped(state)
        
        assert result.output == "processed: test"
        assert result.moss_envelope is not None
        assert isinstance(result.moss_envelope, Envelope)


class TestMultipleNodes:
    def test_different_subjects_per_node(self, temp_moss_dir):
        def step1(state):
            state["step1"] = True
            return state
        
        def step2(state):
            state["step2"] = True
            return state
        
        wrapped1 = signed_node(step1, "moss:flow:step1")
        wrapped2 = signed_node(step2, "moss:flow:step2")
        
        state = {}
        state = wrapped1(state)
        env1 = state["moss_envelope"]
        
        state = wrapped2(state)
        env2 = state["moss_envelope"]
        
        assert env1.subject == "moss:flow:step1"
        assert env2.subject == "moss:flow:step2"
