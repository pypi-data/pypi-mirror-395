import os

import agentspeak
import openai
from agentspeak import AslError
from openai import OpenAI

from a2a_agentspeak import actions
from a2a_acl.utils.strings import neutralize_str

openai.log = "debug"

llm_api_key = os.environ["OPENAI_API_KEY"]
llm_model = "gpt-4o-mini"


llm_timeout = 60  # seconds


failure = agentspeak.Literal("failure")


def log(m):
    print("[LOG] " + m)


def ask_llm_for_coverage(spec: str, req_list: str) -> bool:
    log("Asking LLM for coverage (timeout " + str(llm_timeout) + " seconds)")
    try:
        llm_client = OpenAI(api_key=llm_api_key)
        chat_response = llm_client.responses.create(
            model=llm_model,
            instructions=(
                "Given a specification of a system, and a list of atomic requirements, tell if that list of atomic requirements covers well that specification."
                + " Answer COMPLETE is the specification is well covered."
                + " Answer PARTIAL otherwise."
            ),
            input=(
                "Specification: "
                + spec
                + "(end of the specification) List of requirements: "
                + req_list
                + "(end of list of requirements)."
            ),
            timeout=llm_timeout,
            background=False,
            max_output_tokens=16,  # 16 is the minimum for gpt-4o-mini
        )
        log("Resonse from LLM received")
        r = chat_response.output_text
        log(
            "I had an interaction with gpt to check coverage.\n "
            + "I gave the following spec: "
            + spec
            + "\n"
            + "I also gave the following requirements: "
            + req_list
            + "\n"
            + "Gpt gave me the following answer: "
            + r
        )
        if r.startswith("COMPLETE"):
            return True
        elif r.startswith("PARTIAL"):
            return False
        else:
            raise Exception("Cannot understand LLM answer.")
    except RuntimeError as e:
        print("Runtime Error: " + str(e))
        raise AslError("LLM failure: " + str(type(e))) from e
    except Exception as e:
        print("Exception: " + str(e))
        raise AslError("LLM failure: " + str(type(e))) from e


def ask_llm_for_completion(spec: str, req_list: str):
    log("Asking LLM for completion  (timeout " + str(llm_timeout) + " seconds)")
    try:
        llm_client = OpenAI(api_key=llm_api_key)
        chat_response = llm_client.responses.create(
            model=llm_model,
            instructions="Given a specification of a system, and a list of atomic requirements, give an atomic requirements that covers the specification and which is not included in the given list of requirements."
            + " Answer with the new requirement, don't explain.",
            input="Specification: "
            + spec
            + "(end of the specification) List of requirements: "
            + req_list
            + "(end of list of requirements).",
            timeout=llm_timeout,
            background=False,
            # max_output_tokens=50,
        )
        log("Resonse from LLM received")
        res = chat_response.output_text
        log(
            "I had an interaction with gpt to generate a requirement. "
            + "I gave the following spec: "
            + spec
            + "I also gave the following requirements: "
            + req_list
            + " "
            + "Gpt gave me the following answer: "
            + res
        )
        return res
    except Exception as e:
        print(str(e))
        raise AslError("LLM failure: " + str(type(e)))


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

action_prompt_generation = actions.Action(
    "function",
    ".prompt_generate",
    (agentspeak.Literal, agentspeak.Literal),
    prompt_generation,
)
