# moss-langchain

MOSS signing integration for LangChain via callback handler.

## Installation

```bash
pip install moss-langchain
```

## Usage

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from moss_langchain import SignedCallbackHandler

# Create callback handler
cb = SignedCallbackHandler("moss:bot:summary")

# Create your chain
chain = ChatPromptTemplate.from_template("Summarize: {text}") | ChatOpenAI()

# Invoke with callback
result = chain.invoke(
    {"text": "Long document..."},
    config={"callbacks": [cb]}
)

# Access the signature
envelope = cb.envelope
```

## Verification

```python
from moss import Subject

# Verify the output
result = Subject.verify(cb.envelope)
assert result.valid
```

## Multiple Outputs

The handler tracks all outputs during a session:

```python
cb = SignedCallbackHandler("moss:bot:pipeline")

# Run multiple operations
chain1.invoke(input1, config={"callbacks": [cb]})
chain2.invoke(input2, config={"callbacks": [cb]})

# Access all envelopes
for envelope in cb.envelopes:
    print(f"Seq {envelope.seq}: {envelope.payload_hash}")

# Clear for next session
cb.clear()
```

## Async Chains

```python
from moss_langchain import AsyncSignedCallbackHandler

cb = AsyncSignedCallbackHandler("moss:bot:async")
result = await chain.ainvoke(input, config={"callbacks": [cb]})
```

## Signed Events

The handler signs outputs from:
- `on_llm_end` - LLM generation complete
- `on_chain_end` - Chain execution complete
- `on_tool_end` - Tool execution complete
- `on_agent_finish` - Agent finished
- `on_retriever_end` - Retriever returned documents
