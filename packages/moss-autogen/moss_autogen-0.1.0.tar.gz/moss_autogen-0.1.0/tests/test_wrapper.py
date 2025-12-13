import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path

from moss_autogen import signed_agent
from moss_autogen.wrapper import _result_to_payload, _get_or_create_subject
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
def mock_agent():
    """Create a mock AutoGen agent."""
    agent = MagicMock()
    agent.generate_reply = MagicMock(return_value="I'll analyze that for you.")
    agent.receive = MagicMock(return_value=None)
    agent.send = MagicMock(return_value={"content": "sent message"})
    return agent


class TestResultToPayload:
    def test_dict_passthrough(self):
        result = {"content": "hello", "role": "assistant"}
        payload = _result_to_payload(result)
        assert payload == result

    def test_string_wrapped(self):
        result = "some reply"
        payload = _result_to_payload(result)
        assert payload == {"content": "some reply"}

    def test_list_of_messages(self):
        result = [{"content": "msg1"}, {"content": "msg2"}]
        payload = _result_to_payload(result)
        assert payload == {"messages": [{"content": "msg1"}, {"content": "msg2"}]}

    def test_list_of_strings(self):
        result = ["reply1", "reply2"]
        payload = _result_to_payload(result)
        assert payload == {"messages": [{"content": "reply1"}, {"content": "reply2"}]}

    def test_object_with_dict_method(self):
        obj = MagicMock()
        obj.dict = MagicMock(return_value={"from_dict": True})
        payload = _result_to_payload(obj)
        assert payload == {"from_dict": True}

    def test_generic_object(self):
        class CustomResult:
            def __str__(self):
                return "custom string"
        
        obj = CustomResult()
        payload = _result_to_payload(obj)
        assert payload["content"] == "custom string"
        assert payload["type"] == "CustomResult"


class TestGetOrCreateSubject:
    def test_creates_new_subject(self, temp_moss_dir):
        subject = _get_or_create_subject("moss:test:new-agent")
        assert subject.subject == "moss:test:new-agent"

    def test_loads_existing_subject(self, temp_moss_dir):
        Subject.create("moss:test:existing")
        subject = _get_or_create_subject("moss:test:existing")
        assert subject.subject == "moss:test:existing"


class TestSignedAgent:
    def test_wraps_agent(self, temp_moss_dir, mock_agent):
        wrapped = signed_agent(mock_agent, "moss:test:wrapper")
        assert wrapped is mock_agent
        assert hasattr(wrapped, "moss_envelope")
        assert hasattr(wrapped, "_moss_subject")

    def test_generate_reply_signs_output(self, temp_moss_dir, mock_agent):
        wrapped = signed_agent(mock_agent, "moss:test:gen-reply")
        
        result = wrapped.generate_reply(messages=[{"content": "hello"}])
        
        assert result == "I'll analyze that for you."
        assert wrapped.moss_envelope is not None
        assert isinstance(wrapped.moss_envelope, Envelope)
        assert wrapped.moss_envelope.subject == "moss:test:gen-reply"

    def test_generate_reply_with_sender(self, temp_moss_dir, mock_agent):
        wrapped = signed_agent(mock_agent, "moss:test:sender")
        sender = MagicMock()
        
        result = wrapped.generate_reply(messages=[{"content": "hi"}], sender=sender)
        
        assert result == "I'll analyze that for you."
        assert wrapped.moss_envelope is not None

    def test_send_signs_output(self, temp_moss_dir, mock_agent):
        wrapped = signed_agent(mock_agent, "moss:test:send")
        
        result = wrapped.send()
        
        assert result == {"content": "sent message"}
        assert wrapped.moss_envelope is not None

    def test_receive_with_none_no_envelope(self, temp_moss_dir, mock_agent):
        wrapped = signed_agent(mock_agent, "moss:test:receive")
        wrapped.receive()
        assert wrapped.moss_envelope is None

    def test_envelope_updated_on_each_call(self, temp_moss_dir, mock_agent):
        wrapped = signed_agent(mock_agent, "moss:test:multi")
        
        wrapped.generate_reply(messages=[{"content": "msg1"}])
        env1 = wrapped.moss_envelope
        
        wrapped.generate_reply(messages=[{"content": "msg2"}])
        env2 = wrapped.moss_envelope
        
        assert env1.seq == 1
        assert env2.seq == 2

    def test_envelope_verifiable(self, temp_moss_dir, mock_agent):
        wrapped = signed_agent(mock_agent, "moss:test:verify")
        
        wrapped.generate_reply(messages=[])
        
        result = Subject.verify(wrapped.moss_envelope, check_replay=False)
        assert result.valid is True
        assert result.subject == "moss:test:verify"

    def test_dict_reply_signed(self, temp_moss_dir):
        agent = MagicMock()
        agent.generate_reply = MagicMock(return_value={
            "content": "Here's my analysis",
            "role": "assistant"
        })
        
        wrapped = signed_agent(agent, "moss:test:dict-reply")
        wrapped.generate_reply(messages=[])
        
        assert wrapped.moss_envelope is not None
        result = Subject.verify(wrapped.moss_envelope, check_replay=False)
        assert result.valid

    def test_missing_methods_ignored(self, temp_moss_dir):
        agent = MagicMock(spec=[])
        wrapped = signed_agent(agent, "moss:test:minimal")
        assert wrapped is agent


class TestAsyncMethods:
    @pytest.mark.asyncio
    async def test_async_generate_reply(self, temp_moss_dir):
        agent = MagicMock()
        agent.a_generate_reply = AsyncMock(return_value="async reply")
        
        wrapped = signed_agent(agent, "moss:test:async-gen")
        
        result = await wrapped.a_generate_reply(messages=[])
        
        assert result == "async reply"
        assert wrapped.moss_envelope is not None
        assert wrapped.moss_envelope.subject == "moss:test:async-gen"

    @pytest.mark.asyncio
    async def test_async_receive(self, temp_moss_dir):
        agent = MagicMock()
        agent.receive = AsyncMock(return_value={"content": "received"})
        
        wrapped = signed_agent(agent, "moss:test:async-recv")
        
        result = await wrapped.receive()
        
        assert result == {"content": "received"}
        assert wrapped.moss_envelope is not None


class TestSubjectReuse:
    def test_uses_same_subject_across_calls(self, temp_moss_dir, mock_agent):
        wrapped = signed_agent(mock_agent, "moss:test:reuse")
        
        wrapped.generate_reply(messages=[{"content": "1"}])
        env1 = wrapped.moss_envelope
        
        wrapped.generate_reply(messages=[{"content": "2"}])
        env2 = wrapped.moss_envelope
        
        assert env1.subject == env2.subject
        assert env2.seq > env1.seq


class TestMultiAgentScenario:
    def test_multiple_agents_different_subjects(self, temp_moss_dir):
        agent1 = MagicMock()
        agent1.generate_reply = MagicMock(return_value="Agent 1 reply")
        
        agent2 = MagicMock()
        agent2.generate_reply = MagicMock(return_value="Agent 2 reply")
        
        wrapped1 = signed_agent(agent1, "moss:lab:agent1")
        wrapped2 = signed_agent(agent2, "moss:lab:agent2")
        
        wrapped1.generate_reply(messages=[])
        wrapped2.generate_reply(messages=[])
        
        assert wrapped1.moss_envelope.subject == "moss:lab:agent1"
        assert wrapped2.moss_envelope.subject == "moss:lab:agent2"
        
        result1 = Subject.verify(wrapped1.moss_envelope, check_replay=False)
        result2 = Subject.verify(wrapped2.moss_envelope, check_replay=False)
        
        assert result1.valid
        assert result2.valid
