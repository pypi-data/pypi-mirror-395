import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path

from moss_crewai import moss_wrap
from moss_crewai.wrapper import _result_to_payload, _get_or_create_subject
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
    """Create a mock CrewAI agent."""
    agent = MagicMock()
    agent.execute_task = MagicMock(return_value="Task completed successfully")
    agent.execute = MagicMock(return_value={"result": "data"})
    agent.run = MagicMock(return_value="Run output")
    return agent


class TestResultToPayload:
    def test_dict_passthrough(self):
        result = {"key": "value", "nested": {"a": 1}}
        payload = _result_to_payload(result)
        assert payload == result

    def test_string_wrapped(self):
        result = "some output"
        payload = _result_to_payload(result)
        assert payload == {"output": "some output"}

    def test_object_with_raw(self):
        obj = MagicMock()
        obj.raw = "raw content"
        payload = _result_to_payload(obj)
        assert payload == {"output": "raw content"}

    def test_object_with_dict_method(self):
        obj = MagicMock()
        del obj.raw
        obj.dict = MagicMock(return_value={"from_dict": True})
        payload = _result_to_payload(obj)
        assert payload == {"from_dict": True}

    def test_generic_object(self):
        class CustomResult:
            def __str__(self):
                return "custom string"
        
        obj = CustomResult()
        payload = _result_to_payload(obj)
        assert payload["output"] == "custom string"
        assert payload["type"] == "CustomResult"


class TestGetOrCreateSubject:
    def test_creates_new_subject(self, temp_moss_dir):
        subject = _get_or_create_subject("moss:test:new-agent")
        assert subject.subject == "moss:test:new-agent"

    def test_loads_existing_subject(self, temp_moss_dir):
        Subject.create("moss:test:existing")
        subject = _get_or_create_subject("moss:test:existing")
        assert subject.subject == "moss:test:existing"


class TestMossWrap:
    def test_wraps_agent(self, temp_moss_dir, mock_agent):
        wrapped = moss_wrap(mock_agent, "moss:test:wrapper")
        assert wrapped is mock_agent
        assert hasattr(wrapped, "moss_envelope")
        assert hasattr(wrapped, "_moss_subject")

    def test_execute_task_signs_output(self, temp_moss_dir, mock_agent):
        wrapped = moss_wrap(mock_agent, "moss:test:exec-task")
        
        result = wrapped.execute_task("some task")
        
        assert result == "Task completed successfully"
        assert wrapped.moss_envelope is not None
        assert isinstance(wrapped.moss_envelope, Envelope)
        assert wrapped.moss_envelope.subject == "moss:test:exec-task"

    def test_execute_signs_output(self, temp_moss_dir, mock_agent):
        wrapped = moss_wrap(mock_agent, "moss:test:execute")
        
        result = wrapped.execute()
        
        assert result == {"result": "data"}
        assert wrapped.moss_envelope is not None
        assert wrapped.moss_envelope.subject == "moss:test:execute"

    def test_run_signs_output(self, temp_moss_dir, mock_agent):
        wrapped = moss_wrap(mock_agent, "moss:test:run")
        
        result = wrapped.run()
        
        assert result == "Run output"
        assert wrapped.moss_envelope is not None

    def test_envelope_updated_on_each_call(self, temp_moss_dir, mock_agent):
        wrapped = moss_wrap(mock_agent, "moss:test:multi")
        
        wrapped.execute_task("task1")
        env1 = wrapped.moss_envelope
        
        wrapped.execute_task("task2")
        env2 = wrapped.moss_envelope
        
        assert env1.seq == 1
        assert env2.seq == 2

    def test_envelope_verifiable(self, temp_moss_dir, mock_agent):
        wrapped = moss_wrap(mock_agent, "moss:test:verify")
        
        wrapped.execute_task("task")
        
        result = Subject.verify(wrapped.moss_envelope, check_replay=False)
        assert result.valid is True
        assert result.subject == "moss:test:verify"

    def test_none_result_no_envelope(self, temp_moss_dir):
        agent = MagicMock()
        agent.execute = MagicMock(return_value=None)
        
        wrapped = moss_wrap(agent, "moss:test:none")
        wrapped.execute()
        
        assert wrapped.moss_envelope is None

    def test_missing_methods_ignored(self, temp_moss_dir):
        agent = MagicMock(spec=[])
        wrapped = moss_wrap(agent, "moss:test:minimal")
        assert wrapped is agent


class TestAsyncMethods:
    @pytest.mark.asyncio
    async def test_async_method_wrapped(self, temp_moss_dir):
        agent = MagicMock()
        agent.execute = AsyncMock(return_value="async result")
        
        wrapped = moss_wrap(agent, "moss:test:async")
        
        result = await wrapped.execute()
        
        assert result == "async result"
        assert wrapped.moss_envelope is not None
        assert wrapped.moss_envelope.subject == "moss:test:async"


class TestSubjectReuse:
    def test_uses_same_subject_across_calls(self, temp_moss_dir, mock_agent):
        wrapped = moss_wrap(mock_agent, "moss:test:reuse")
        
        wrapped.execute_task("task1")
        env1 = wrapped.moss_envelope
        
        wrapped.execute_task("task2")
        env2 = wrapped.moss_envelope
        
        assert env1.subject == env2.subject
        assert env2.seq > env1.seq
