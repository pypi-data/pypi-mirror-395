# langchain-openmemory

> One-line, persistent, temporal memory for LangChain — powered by OpenMemory.

```python
from langchain_openmemory import Memory

m = Memory()  # zero friction, no user id needed!
```

That’s it. `Memory` works as:

- a **retriever**
- a **chat history backend**
- a **LCEL Runnable** that injects rich context
- a **persistent long-term memory** across sessions

All backed by [OpenMemory](https://github.com/CaviraOSS/OpenMemory): local-first, temporal, explainable memory for AI agents.

---

## Features

- 🧠 **One-line API** — `Memory()` is all you need
- 🪢 **LangChain-native** — works as a `Runnable`, retriever, and chat history
- 🕒 **Temporal memory** — recall state across time, not just similar text
- 📚 **Multi-chat context** — memory persists over many conversations
- 💾 **Local-first** — backed by OpenMemory’s SQLite / engine, no vector DB required
- 🔍 **Explainable** (via OpenMemory metadata) — you can inspect what was recalled and why

---

## Installation

```bash
pip install openmemory-py langchain-core langchain-openmemory
```

> Requires Python 3.9+.

---

## Quickstart

### 1. Create memory

```python
from langchain_openmemory import Memory

memory = Memory()  # optional: Memory("user123")
```

### 2. Use with an LLM via LCEL

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_openmemory import Memory

memory = Memory()

prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant."
    "Here is what you remember: {context}"
    "User: {question}"
)

llm = ChatOpenAI()

chain = (
    {"context": memory, "question": RunnablePassthrough()}
    | prompt
    | llm
)

print(chain.invoke("Remember that I like dark themes and short answers."))
print(chain.invoke("What did I say about themes?"))
```

### 3. Manual recall

```python
print(memory("what does the user prefer?"))
```

### 4. Store extra facts

```python
memory.store("user123 loves Minecraft and Pterodactyl panels.")
```

---

## How it works

Internally, `Memory`:

1. Uses the Python `openmemory` client in **local** mode by default.
2. Stores chat messages and facts into OpenMemory.
3. Retrieves relevant memories with temporal + sector-aware ranking.
4. Exposes a LangChain-compatible `Runnable` that returns a context block.
5. Provides an internal retriever and chat history implementation.

You get:

- real long-term memory
- across many sessions
- with minimal boilerplate

---

## Using as a retriever

```python
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_openmemory import Memory

memory = Memory()
retriever = memory.retriever

llm = ChatOpenAI()

qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    return_source_documents=True,
)

res = qa.invoke({"question": "What does this user like?"})
print(res["answer"])
```

---

## Using as chat history

```python
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openmemory import Memory

memory = Memory()

prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant."),
     ("human", "{input}")]
)
llm = ChatOpenAI()
base_chain = prompt | llm

def get_history(session_id: str):
    return memory.history

chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

print(chain.invoke({"input": "Remember that I live in Hyderabad."}, config={"configurable": {"session_id": "s1"}}))
print(chain.invoke({"input": "Where do I live?"}, config={"configurable": {"session_id": "s1"}}))
```

---

## Examples

See the [`examples/`](./examples) folder for:

- `chatbot.py` — simple chatbot with persistent memory
- `agent.py` — agent-style usage
- `retrieval.py` — manual recall demo

---

## Roadmap

- [ ] Better temporal filters
- [ ] First-class LangChain docs integration
- [ ] Benchmarks vs vector DB + Redis memory

---

## License

MIT — see [LICENSE](./LICENSE).
