import os

import agentspeak
from agentspeak import AslError
from mistralai import Mistral

from a2a_agentspeak import actions
from a2a_acl.utils.strings import neutralize_str

llm_api_key = os.environ["MISTRAL_API_KEY"]
llm_model = "mistral-small-latest"

llm_client = Mistral(api_key=llm_api_key)

failure = agentspeak.Literal("failure")


def log(m):
    print("[LOG] " + m)


def ask_llm_for_coverage(spec, req_list) -> bool:
    try:
        chat_response = llm_client.chat.complete(
            model=llm_model,
            messages=[
                {
                    "role": "system",
                    "content": "Given a specification of a system, and a list of atomic requirements, tell if that list of atomic requirements covers well that specification."
                    + " Answer COMPLETE is the specification is well covered."
                    + " Answer PARTIAL otherwise.",
                },
                {
                    "role": "user",
                    "content": "Specification: "
                    + spec
                    + "(end of the specification) List of requirements: "
                    + req_list
                    + "(end of list of requirements).",
                },
            ],
            max_tokens=3,
        )
        r = chat_response.choices[0].message.content
        log(
            "I had an interaction with mistral to check coverage.\n"
            + "I gave the following spec: "
            + spec
            + "\n"
            + "I also gave the following requirements: "
            + req_list
            + "\n"
            + "Mistral gave me the following answer: "
            + r
        )
        if r.startswith("COMPLETE"):
            return True
        elif r.startswith("PARTIAL"):
            return False
        else:
            raise Exception("Cannot understand LLM answer.")
    except Exception as e:
        print(str(e))
        raise AslError("LLM failure: " + str(type(e)))


def ask_llm_for_completion(spec: str, req_list: str):
    try:
        chat_response = llm_client.chat.complete(
            model=llm_model,
            messages=[
                {
                    "role": "system",
                    "content": "Given a specification of a system, and a list of atomic requirements, give an atomic requirements that covers the specification and which is not included in the given list of requirements."
                    + " Answer with the new requirement, don't explain.",
                },
                {
                    "role": "user",
                    "content": "Specification: "
                    + spec
                    + "(end of the specification) List of requirements: "
                    + req_list
                    + "(end of list of requirements).",
                },
            ],
            max_tokens=50,
        )
        res = chat_response.choices[0].message.content
        log(
            "I had an interaction with mistral to generate a requirement. "
            + "I gave the following spec: "
            + spec
            + "I also gave the following requirements: "
            + req_list
            + " "
            + "Mistral gave me the following answer: "
            + res
        )
        return res
    except Exception as e:
        print(str(e))
        raise AslError("LLM failure: " + str(type(e))) from e


def prompt_completeness(
    s: agentspeak.Literal, r: agentspeak.Literal
) -> agentspeak.Literal:
    assert s.functor == "spec"
    assert r.functor == "req"
    try:
        res = ask_llm_for_coverage(str(s.args[0]), str(r.args[0]))
        return agentspeak.Literal("complete" if res else "incomplete")
    except Exception as e:
        print("Failure while talking with the llm")
        print(str(e))
        return failure


def prompt_generation(s, r) -> agentspeak.Literal:
    assert s.functor == "spec"
    assert r.functor == "req"
    try:
        res = ask_llm_for_completion(str(s.args[0]), str(r.args[0]))
        res = res if res.startswith('"') and res.endswith('"') else neutralize_str(res)
        return agentspeak.Literal(res)
    except Exception as e:
        print("Failure while talking with the llm")
        print(str(e))
        return failure


action_prompt_completeness = actions.Action(
    "function",
    ".prompt_completeness",
    (agentspeak.Literal, agentspeak.Literal),
    prompt_completeness,
)

action_prompt_generate = actions.Action(
    "function",
    ".prompt_generate",
    (agentspeak.Literal, agentspeak.Literal),
    prompt_generation,
)
