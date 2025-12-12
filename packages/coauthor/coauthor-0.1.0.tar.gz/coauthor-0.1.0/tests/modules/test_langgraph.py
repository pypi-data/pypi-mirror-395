# # import os

# import pytest

# from langsmith import traceable

# from openai import OpenAI
# from typing import List
# import nest_asyncio

# # from coauthor.modules.langgraph import search_c2platform_website

# from coauthor.utils.logger import Logger
# import logging


# def test_rag_app():
#     import os
#     import nest_asyncio
#     import operator
#     from langchain.schema import Document
#     from langchain_core.messages import HumanMessage, AnyMessage, get_buffer_string
#     from langchain_openai import ChatOpenAI
#     from langgraph.graph import StateGraph, START, END
#     from IPython.display import Image, display
#     from typing import List
#     from typing_extensions import TypedDict, Annotated
#     from coauthor.utils.retriever import get_vector_db_retriever, RAG_PROMPT
#     from coauthor.utils.evaluators import compare_semantic_similarity

#     nest_asyncio.apply()

#     # TODO
#     logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
#     retriever = get_vector_db_retriever()
#     llm = ChatOpenAI(
#         model_name="gpt-4o-mini",
#         temperature=0,
#     )

#     # Define Graph state
#     class GraphState(TypedDict):
#         question: str
#         messages: Annotated[List[AnyMessage], operator.add]
#         documents: List[Document]

#     # Define Nodes
#     def retrieve_documents(state: GraphState):
#         messages = state.get("messages", [])
#         question = state["question"]
#         documents = retriever.invoke(f"{get_buffer_string(messages)} {question}")
#         return {"documents": documents}

#     def generate_response(state: GraphState):
#         question = state["question"]
#         messages = state["messages"]
#         documents = state["documents"]
#         formatted_docs = "\n\n".join(doc.page_content for doc in documents)

#         rag_prompt_formatted = RAG_PROMPT.format(context=formatted_docs, conversation=messages, question=question)
#         generation = llm.invoke([HumanMessage(content=rag_prompt_formatted)])
#         return {"documents": documents, "messages": [HumanMessage(question), generation]}

#     # Define Graph
#     graph_builder = StateGraph(GraphState)
#     graph_builder.add_node("retrieve_documents", retrieve_documents)
#     graph_builder.add_node("generate_response", generate_response)
#     graph_builder.add_edge(START, "retrieve_documents")
#     graph_builder.add_edge("retrieve_documents", "generate_response")
#     graph_builder.add_edge("generate_response", END)

#     simple_rag_graph = graph_builder.compile()
#     # display(Image(simple_rag_graph.get_graph().draw_mermaid_png()))

#     inputs = {"question": "How do I set up tracing if I'm using LangChain?"}
#     reference_outputs = {
#         "output": "To set up tracing in LangChain, you need to set the environment variable `LANGCHAIN_TRACING_V2` to 'true' and also set the `LANGCHAIN_API_KEY` to your API key. This configuration allows traces to be logged to LangSmith, with the default project being named \"default.\" If you want to log traces to a different project, you can refer to the relevant section in the documentation."
#     }

#     # answer = simple_rag_graph.invoke({"question": inputs["question"]}, config={"metadata": {"foo": "bar"}})
#     answer = simple_rag_graph.invoke({"question": inputs["question"]})
#     outputs = {"output": answer}

#     similarity_score = compare_semantic_similarity(inputs, reference_outputs, outputs)
#     logger.debug(f"inputs: {inputs}")
#     logger.debug(f"reference_outputs: {reference_outputs}")
#     logger.debug(f"outputs: {outputs}")

#     assert similarity_score["score"] >= 2

#     reference_outputs = {
#         "output": "To set up tracing in LangChain, you need to set `LANGCHAIN_TRACING_V2` to 'true' and also set the `LANGCHAIN_API_KEY` to your API key."
#     }

#     # answer = simple_rag_graph.invoke({"question": inputs["question"]}, config={"metadata": {"foo": "bar"}})
#     answer = simple_rag_graph.invoke({"question": inputs["question"]})
#     outputs = {"output": answer}

#     similarity_score = compare_semantic_similarity(inputs, reference_outputs, outputs)
#     logger.debug(f"inputs: {inputs}")
#     logger.debug(f"reference_outputs: {reference_outputs}")
#     logger.debug(f"outputs: {outputs}")

#     assert similarity_score["score"] >= 2


# def test_rag_app_c2platform_org():

#     import os
#     import nest_asyncio
#     import operator
#     from langchain.schema import Document
#     from langchain_core.messages import HumanMessage, AnyMessage, get_buffer_string
#     from langchain_openai import ChatOpenAI
#     from langgraph.graph import StateGraph, START, END
#     from IPython.display import Image, display
#     from typing import List
#     from typing_extensions import TypedDict, Annotated

#     from coauthor.utils.retriever import RAG_PROMPT

#     from coauthor.utils.c2platform_org import search_using_ddg

#     # from coauthor.modules.langgraph import search_c2platform_website
#     from coauthor.utils.evaluators import compare_semantic_similarity

#     nest_asyncio.apply()

#     # TODO
#     logger = Logger(__name__, level=logging.DEBUG, log_file=f"{os.getcwd()}/debug.log")
#     # retriever = get_vector_db_retriever()
#     llm = ChatOpenAI(
#         model_name="gpt-4o-mini",
#         temperature=0,
#     )

#     # Define Graph state
#     class GraphState(TypedDict):
#         question: str
#         messages: Annotated[List[AnyMessage], operator.add]
#         documents: List[Document]

#     # Define Nodes
#     def retrieve_documents(state: GraphState):
#         messages = state.get("messages", [])
#         question = state["question"]
#         documents = search_using_ddg(question, 2)
#         return {"documents": documents}

#     def generate_response(state: GraphState):
#         question = state["question"]
#         messages = state["messages"]
#         documents = state["documents"]
#         formatted_docs = "\n\n".join(doc["formatted-doc-md"] for doc in documents)
#         rag_prompt_formatted = RAG_PROMPT.format(context=formatted_docs, conversation=messages, question=question)
#         generation = llm.invoke([HumanMessage(content=rag_prompt_formatted)])
#         return {"documents": documents, "messages": [HumanMessage(question), generation]}

#     # Define Graph
#     graph_builder = StateGraph(GraphState)
#     graph_builder.add_node("retrieve_documents", retrieve_documents)
#     graph_builder.add_node("generate_response", generate_response)
#     graph_builder.add_edge(START, "retrieve_documents")
#     graph_builder.add_edge("retrieve_documents", "generate_response")
#     graph_builder.add_edge("generate_response", END)

#     simple_rag_graph = graph_builder.compile()
#     # display(Image(simple_rag_graph.get_graph().draw_mermaid_png()))

#     inputs = {"question": "How do I set up C2 platform development environment?"}
#     reference_outputs = {
#         "output": """To set up the C2 platform development environment, you can follow
#             the step-by-step instructions provided in the "Manage Your Development
#             Environment" section on the C2 Platform website. This includes installing
#             necessary tools like Ansible, Vagrant, and VirtualBox, and configuring
#             your environment for development tasks. For detailed guidance, visit the
#             documentation at [C2 Platform](https://c2platform.org/docs/howto/dev-environment/)"""
#     }

#     # answer = simple_rag_graph.invoke({"question": inputs["question"]}, config={"metadata": {"foo": "bar"}})
#     answer = simple_rag_graph.invoke({"question": inputs["question"]})
#     outputs = {"output": answer}

#     similarity_score = compare_semantic_similarity(inputs, reference_outputs, outputs)

#     assert similarity_score["score"] >= 9
