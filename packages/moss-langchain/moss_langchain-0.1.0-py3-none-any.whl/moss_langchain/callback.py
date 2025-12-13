from typing import Any, Dict, List, Optional
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage

from moss import Subject, Envelope
from moss.errors import KeyNotFound


def _get_or_create_subject(subject_id: str) -> Subject:
    """Load existing subject or create new one."""
    try:
        return Subject.load(subject_id)
    except KeyNotFound:
        return Subject.create(subject_id)


def _output_to_payload(output: Any) -> dict:
    """Convert LangChain output to signable payload."""
    if isinstance(output, dict):
        return output
    elif isinstance(output, str):
        return {"content": output}
    elif isinstance(output, LLMResult):
        generations = []
        for gen_list in output.generations:
            for gen in gen_list:
                generations.append({
                    "text": gen.text,
                    "type": type(gen).__name__
                })
        return {
            "generations": generations,
            "llm_output": output.llm_output
        }
    elif isinstance(output, BaseMessage):
        return {
            "content": output.content,
            "type": output.type,
            "additional_kwargs": output.additional_kwargs
        }
    elif hasattr(output, "generations") and hasattr(output, "llm_output"):
        generations = []
        for gen_list in output.generations:
            for gen in gen_list:
                generations.append({
                    "text": getattr(gen, "text", str(gen)),
                    "type": type(gen).__name__
                })
        return {
            "generations": generations,
            "llm_output": output.llm_output
        }
    elif hasattr(output, "return_values"):
        return {"return_values": str(output.return_values)}
    elif hasattr(output, "content"):
        return {"content": output.content}
    elif hasattr(output, "dict") and callable(output.dict):
        try:
            return output.dict()
        except Exception:
            return {"output": str(output)}
    else:
        return {"output": str(output)}


class SignedCallbackHandler(BaseCallbackHandler):
    """
    LangChain callback handler that signs outputs with MOSS.
    
    Args:
        subject_id: MOSS subject identifier (e.g., "moss:bot:summary")
    
    Attributes:
        envelope: The most recent MOSS envelope (after any signed output)
        envelopes: List of all envelopes from this handler session
        last_output: The most recent output that was signed
    
    Example:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI
        from moss_langchain import SignedCallbackHandler
        
        cb = SignedCallbackHandler("moss:bot:summary")
        chain = ChatPromptTemplate.from_template("...") | ChatOpenAI()
        
        result = chain.invoke({"input": "..."}, config={"callbacks": [cb]})
        
        # Access the signature
        envelope = cb.envelope
        
        # Verify
        from moss import Subject
        assert Subject.verify(envelope).valid
    """
    
    def __init__(self, subject_id: str, **kwargs):
        super().__init__(**kwargs)
        self.subject_id = subject_id
        self._subject = _get_or_create_subject(subject_id)
        self.envelope: Optional[Envelope] = None
        self.envelopes: List[Envelope] = []
        self.last_output: Optional[Any] = None
    
    def _sign_output(self, output: Any) -> Envelope:
        """Sign an output and store the envelope."""
        payload = _output_to_payload(output)
        envelope = self._subject.sign(payload)
        self.envelope = envelope
        self.envelopes.append(envelope)
        self.last_output = output
        return envelope
    
    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign LLM output when generation completes."""
        self._sign_output(response)
    
    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign chain output when chain completes."""
        self._sign_output(outputs)
    
    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign tool output when tool execution completes."""
        self._sign_output(output)
    
    def on_agent_finish(
        self,
        finish: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign agent output when agent finishes."""
        self._sign_output(finish)
    
    def on_retriever_end(
        self,
        documents: List[Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign retriever output."""
        self._sign_output({"documents": [str(d) for d in documents]})
    
    def clear(self) -> None:
        """Clear all stored envelopes and outputs."""
        self.envelope = None
        self.envelopes = []
        self.last_output = None


class AsyncSignedCallbackHandler(SignedCallbackHandler):
    """
    Async version of SignedCallbackHandler.
    
    Same interface as SignedCallbackHandler but for async chains.
    """
    
    async def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign LLM output when generation completes."""
        self._sign_output(response)
    
    async def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign chain output when chain completes."""
        self._sign_output(outputs)
    
    async def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign tool output when tool execution completes."""
        self._sign_output(output)
    
    async def on_agent_finish(
        self,
        finish: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign agent output when agent finishes."""
        self._sign_output(finish)
    
    async def on_retriever_end(
        self,
        documents: List[Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Sign retriever output."""
        self._sign_output({"documents": [str(d) for d in documents]})
