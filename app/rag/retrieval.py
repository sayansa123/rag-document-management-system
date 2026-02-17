from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.rag.vector_store import vector_store


def retrieve_answer(question: str, allowed_levels: list[int]) -> str:
    # check valid question or not
    if not question or not question.strip():
        return "Please provide a valid question"
    
    # Filter for allowed access levels
    # ChromaDB filter syntax: {"access_level": {"$in": [0, 1, 2]}}
    access_filter = {"access_level": {"$in": allowed_levels}}

    # retrieve related top 5 docs
    retriever = vector_store.as_retriever(
        # search_type = 'mmr',      # better to use the vanilla similarity search here
        search_kwargs={'k': 5, 'filter': access_filter}
    )

    retrieved_docs = retriever.invoke(question)
    if not retrieved_docs:
        return """I don't have enough information in the available documents to answer your question.
            This could mean:
            - The information is not in the documents you have access to
            - The documents haven't been uploaded yet
            - Your question might need to be rephrased

            Please try asking in a different way or contact an administrator if you believe you should have access to this information."""
    
    # Combine retrieve chunks -> text
    retrieved_texts = '\n\n'.join(i.page_content for i in retrieved_docs)

    # model
    llm = HuggingFaceEndpoint(
        repo_id='mistralai/Mistral-7B-Instruct-v0.2',
        task='text-generation'
    )
    model = ChatHuggingFace(llm=llm)

    # prompt
    prompt = ChatPromptTemplate([
        ("system", """You are a helpful AI assistant for a company's internal documentation system.
            Your role is to answer questions based ONLY on the provided context from company documents.

            Guidelines:
            - Only use information from the provided context
            - If the context doesn't contain enough information, clearly state that
            - Be concise but thorough in your responses
            - Maintain a professional and helpful tone
            - If you're not certain about something, acknowledge it
            - Do not make up information or use external knowledge"""
        ),
        ("human", """Context from company documents:
            {context}\n
            User Question: {question}\n
            Please provide a clear and accurate answer based on the context above.""")
    ])

    # output parser
    parser = StrOutputParser()

    # chain
    chain = prompt | model | parser

    # call chain
    answer = chain.invoke({
        'context': retrieved_texts,
        'question': question
    })

    return answer
