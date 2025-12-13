import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4

from moss_langchain import SignedCallbackHandler, AsyncSignedCallbackHandler
from moss_langchain.callback import _output_to_payload, _get_or_create_subject
from moss import Subject, Envelope


@pytest.fixture
def temp_moss_dir(tmp_path):
    """Use a temporary directory for MOSS data"""
    keys_dir = tmp_path / "keys"
    seq_dir = tmp_path / "seq"
    with patch('moss.keystore.KEYS_DIR', keys_dir), \
         patch('moss.sequence.SEQ_DIR', seq_dir):
        yield tmp_path


@pytest.fixture
def run_id():
    return uuid4()


class MockLLMResult:
    def __init__(self, text="Generated text"):
        self.generations = [[MagicMock(text=text)]]
        self.llm_output = {"model": "test-model"}


class MockMessage:
    def __init__(self, content="Hello"):
        self.content = content
        self.type = "ai"
        self.additional_kwargs = {}


class TestOutputToPayload:
    def test_dict_passthrough(self):
        output = {"key": "value", "nested": {"a": 1}}
        payload = _output_to_payload(output)
        assert payload == output

    def test_string_wrapped(self):
        output = "some text"
        payload = _output_to_payload(output)
        assert payload == {"content": "some text"}

    def test_llm_result(self):
        result = MockLLMResult("Test generation")
        payload = _output_to_payload(result)
        assert "generations" in payload
        assert payload["generations"][0]["text"] == "Test generation"

    def test_message(self):
        msg = MockMessage("Hello world")
        payload = _output_to_payload(msg)
        assert payload["content"] == "Hello world"

    def test_object_with_dict_method(self):
        obj = MagicMock(spec=["dict"])
        obj.dict = MagicMock(return_value={"from_dict": True})
        payload = _output_to_payload(obj)
        assert payload == {"from_dict": True}


class TestGetOrCreateSubject:
    def test_creates_new_subject(self, temp_moss_dir):
        subject = _get_or_create_subject("moss:bot:new")
        assert subject.subject == "moss:bot:new"

    def test_loads_existing_subject(self, temp_moss_dir):
        Subject.create("moss:bot:existing")
        subject = _get_or_create_subject("moss:bot:existing")
        assert subject.subject == "moss:bot:existing"


class TestSignedCallbackHandler:
    def test_init(self, temp_moss_dir):
        cb = SignedCallbackHandler("moss:bot:test")
        assert cb.subject_id == "moss:bot:test"
        assert cb.envelope is None
        assert cb.envelopes == []
        assert cb.last_output is None

    def test_on_llm_end(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:llm")
        response = MockLLMResult("Generated response")
        
        cb.on_llm_end(response, run_id=run_id)
        
        assert cb.envelope is not None
        assert isinstance(cb.envelope, Envelope)
        assert cb.envelope.subject == "moss:bot:llm"
        assert len(cb.envelopes) == 1

    def test_on_chain_end(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:chain")
        outputs = {"result": "chain output", "metadata": {"key": "value"}}
        
        cb.on_chain_end(outputs, run_id=run_id)
        
        assert cb.envelope is not None
        assert cb.envelope.subject == "moss:bot:chain"

    def test_on_tool_end(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:tool")
        output = "Tool execution result"
        
        cb.on_tool_end(output, run_id=run_id)
        
        assert cb.envelope is not None
        assert cb.envelope.subject == "moss:bot:tool"

    def test_on_agent_finish(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:agent")
        
        class MockAgentFinish:
            return_values = {"output": "agent result"}
        
        finish = MockAgentFinish()
        
        cb.on_agent_finish(finish, run_id=run_id)
        
        assert cb.envelope is not None

    def test_on_retriever_end(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:retriever")
        documents = [MagicMock(__str__=lambda s: "doc1"), MagicMock(__str__=lambda s: "doc2")]
        
        cb.on_retriever_end(documents, run_id=run_id)
        
        assert cb.envelope is not None

    def test_multiple_outputs_tracked(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:multi")
        
        cb.on_llm_end(MockLLMResult("first"), run_id=run_id)
        cb.on_chain_end({"output": "second"}, run_id=run_id)
        cb.on_tool_end("third", run_id=run_id)
        
        assert len(cb.envelopes) == 3
        assert cb.envelopes[0].seq == 1
        assert cb.envelopes[1].seq == 2
        assert cb.envelopes[2].seq == 3
        assert cb.envelope == cb.envelopes[-1]

    def test_envelope_verifiable(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:verify")
        cb.on_chain_end({"result": "test"}, run_id=run_id)
        
        result = Subject.verify(cb.envelope, check_replay=False)
        assert result.valid is True
        assert result.subject == "moss:bot:verify"

    def test_clear(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:clear")
        cb.on_llm_end(MockLLMResult(), run_id=run_id)
        
        assert cb.envelope is not None
        
        cb.clear()
        
        assert cb.envelope is None
        assert cb.envelopes == []
        assert cb.last_output is None

    def test_last_output_stored(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:lastout")
        output = {"result": "stored"}
        
        cb.on_chain_end(output, run_id=run_id)
        
        assert cb.last_output == output


class TestAsyncSignedCallbackHandler:
    @pytest.mark.asyncio
    async def test_async_on_llm_end(self, temp_moss_dir, run_id):
        cb = AsyncSignedCallbackHandler("moss:bot:async-llm")
        response = MockLLMResult("Async response")
        
        await cb.on_llm_end(response, run_id=run_id)
        
        assert cb.envelope is not None
        assert cb.envelope.subject == "moss:bot:async-llm"

    @pytest.mark.asyncio
    async def test_async_on_chain_end(self, temp_moss_dir, run_id):
        cb = AsyncSignedCallbackHandler("moss:bot:async-chain")
        outputs = {"result": "async chain output"}
        
        await cb.on_chain_end(outputs, run_id=run_id)
        
        assert cb.envelope is not None

    @pytest.mark.asyncio
    async def test_async_on_tool_end(self, temp_moss_dir, run_id):
        cb = AsyncSignedCallbackHandler("moss:bot:async-tool")
        
        await cb.on_tool_end("async tool result", run_id=run_id)
        
        assert cb.envelope is not None

    @pytest.mark.asyncio
    async def test_async_envelope_verifiable(self, temp_moss_dir, run_id):
        cb = AsyncSignedCallbackHandler("moss:bot:async-verify")
        await cb.on_chain_end({"async": True}, run_id=run_id)
        
        result = Subject.verify(cb.envelope, check_replay=False)
        assert result.valid is True


class TestMultipleHandlers:
    def test_separate_subjects(self, temp_moss_dir, run_id):
        cb1 = SignedCallbackHandler("moss:bot:handler1")
        cb2 = SignedCallbackHandler("moss:bot:handler2")
        
        cb1.on_chain_end({"from": "handler1"}, run_id=run_id)
        cb2.on_chain_end({"from": "handler2"}, run_id=run_id)
        
        assert cb1.envelope.subject == "moss:bot:handler1"
        assert cb2.envelope.subject == "moss:bot:handler2"
        
        assert Subject.verify(cb1.envelope, check_replay=False).valid
        assert Subject.verify(cb2.envelope, check_replay=False).valid


class TestWithParentRunId:
    def test_with_parent_run_id(self, temp_moss_dir, run_id):
        cb = SignedCallbackHandler("moss:bot:parent")
        parent_id = uuid4()
        
        cb.on_chain_end(
            {"output": "nested"},
            run_id=run_id,
            parent_run_id=parent_id
        )
        
        assert cb.envelope is not None
