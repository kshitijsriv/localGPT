"""
This file implements prompt template for llama based models.
Modify the prompt template based on the model you select.
This seems to have significant impact on the output of the LLM.
"""

from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate

# this is specific to Llama-2.

# system_prompt = """You are a helpful assistant, you will use the provided context to answer user questions.
# Read the given context before answering questions and think step by step. If you can not answer a user question based on
# the provided context, inform the user.
#
# The user will also ask you questions about journey planning. Please answer YES *only* if there is some source
# or destination mentioned in the question or if there is an indication that the user wants to go to some place from where they
# are currently.
#
# If it is a journey planning query and you answer with a YES, the response should be *JSON structured* in the following format:
# {{
#     "src": "<source_name>",
#     "dest": "<destination_name>"
# }}
# """

system_prompt = """
As a sophisticated assistant, your task is to analyze user queries with a nuanced understanding of their context. Apply a systematic approach to distinguish between different types of inquiries. Specifically:

Contextual Understanding: Recognize that not all questions related to a location are about journey planning. Develop a keen sense of differentiating the nature of each query.

Question Type Identification: Categorize questions into distinct types, such as journey planning or general information. For example, treat 'I want to go from X to Y' as a journey planning query, but approach 'Is there parking at X?' as an information-seeking question.

Response Logic: Respond with journey planning details (in JSON format) exclusively when the question involves travel between two locations. For other queries, provide a direct answer or inform the user if the information is unavailable.

Keyword Analysis: Enhance your ability to identify key words and phrases. Words like 'travel to,' 'route to,' or 'go from' indicate a journey planning query, whereas 'is there,' 'does,' or 'can I' might suggest a different type of inquiry.

User Intent Clarification: If a query's intent is ambiguous, seek clarification from the user before responding.

Diverse Query Training: Regularly update your training with a wide range of question types to improve accuracy in understanding and responding.

Your primary goal is to provide accurate, context-sensitive responses. For journey planning queries, structure your responses in JSON format as follows:

{{
"src": "<source_name>",
"dest": "<destination_name>"
}}

For other types of inquiries, tailor your response to address the specific question asked.
Apart from journey planning queries, please make sure other answers have a coherent textual flow.
"""


# system_prompt = """You are a helpful assistant, you will use the provided context to answer user questions.
# Read the given context before answering questions and think step by step. If you can not answer a user question based on
# the provided context, inform the user. Do not use any other information for answering user.
#
# The user will ask you questions about the clauses given in an agreement document. Please try to infer from the document
# and answer these questions as best possible given the context.
# """


def get_prompt_template(system_prompt=system_prompt, promptTemplate_type=None, history=False, llm=None):
    if promptTemplate_type == "llama":
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        if history:
            instruction = """
            Context: {history} \n {context}
            User: {question}"""

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            instruction = """
            Context: {context}
            User: {question}"""

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    elif promptTemplate_type == "mistral":
        # B_INST, E_INST = "<s>[INST] ", " [/INST]"
        # if history:
        #     prompt_template = (
        #         B_INST
        #         + system_prompt
        #         + """
        #
        #     Context: {history} \n {context}
        #     User: {question}"""
        #         + E_INST
        #     )
        #     prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        # else:
        #     prompt_template = (
        #         B_INST
        #         + system_prompt
        #         + """
        #
        #     Context: {context}
        #     User: {question}"""
        #         + E_INST
        #     )
        #     prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
        B_INST, E_INST = "<|im_start|>user ", " <|im_end|>"
        B_SYS, E_SYS = "<|im_start|>system", " <|im_end|>\n\n"
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        if history:
            prompt_template = (
                SYSTEM_PROMPT +
                B_INST
                + """

                    Context: {history} \n {context}
                    User: {question}"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                SYSTEM_PROMPT +
                B_INST
                + """

                    Context: {context}
                    User: {question}"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    else:
        # change this based on the model you have selected.
        if history:
            prompt_template = (
                system_prompt
                + """

            Context: {history} \n {context}
            User: {question}
            Answer:"""
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                system_prompt
                + """

            Context: {context}
            User: {question}
            Answer:"""
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

    memory = ConversationBufferMemory(input_key="question", memory_key="history")
    if llm:
        memory = ConversationSummaryBufferMemory(input_key="question", memory_key="history", llm=llm,
                                                 max_token_limit=2048)

    return (
        prompt,
        memory,
    )
