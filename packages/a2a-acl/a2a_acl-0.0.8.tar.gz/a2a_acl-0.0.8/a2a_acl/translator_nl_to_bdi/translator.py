from a2a.types import AgentCard

from a2a_acl.protocol.acl_message import Illocution
from a2a_acl.interface.skill_conversion import bdi_skill_of_a2a_skill, illoc_of_decl
from a2a_acl.translator_nl_to_bdi.mistral_config import ask_llm


class LLMError(Exception):
    pass


system_prompt_message = {
    "role": "system",
    "content": "Your task is to translate a human request into an ACL message",
}


def build_user_prompt_message(agent_type: str, catalog: str, user_request: str):
    return {
        "role": "user",
        "content": (
            "Your task is to translate a human request into an ACL message for the following agent: "
            + agent_type
            + " The possible achievements are described in the following list. [BEGIN LIST OF ACHIEVEMENTS] "
            + catalog
            + "[END OF LIST OF ACHIEVEMENTS]"
            + " Here is the sentence to translate. [BEGIN] "
            + user_request
            + "[END] "
            + "Respond with only one achievement. "
            + "For example you can answer 'do_dig' if that achievement has arity 0, or 'do_wait(300)' if arity is 1."
        ),
    }


def handled_illocutions(card: AgentCard) -> set:
    res = set()
    for s in card.skills:
        res.add(illoc_of_decl(bdi_skill_of_a2a_skill(s).declaration_kind))
    return res


def doc_illoc(i: Illocution) -> str:
    prefix = str(i) + " ("
    suffix = ")"
    match i:
        case Illocution.TELL:
            return prefix + "to give an information" + suffix
        case Illocution.ACHIEVE:
            return prefix + "to request an action" + suffix
        case Illocution.ASK:
            return prefix + "to ask for some information" + suffix


def select_illocution(card: AgentCard, request: str) -> Illocution:
    s = handled_illocutions(card)
    l = [e for e in s]
    n = len(l)
    assert n > 0
    if n == 1:
        return l[0]
    else:
        system_prompt_message = {
            "role": "system",
            "content": "Your task is to extract an ACL illocution from a human request.",
        }
        user_prompt = {
            "role": "user",
            "content": (
                "Your task is to extract an ACL illocution from a human request. "
                + " The possible ACL illocutions are: "
                + str([doc_illoc(i) for i in l])
                + " Here is the human request. [BEGIN] "
                + request
                + "[END] "
                + "Respond with only one illocution. "
            ),
        }
        r = ask_llm(system_prompt=system_prompt_message, user_prompt=user_prompt)
        return r


def translate(card: AgentCard, request: str) -> str:
    try:
        illoc = select_illocution(card=card, request=request)
    except Exception:
        raise LLMError()
    try:
        user_prompt = build_user_prompt_message(
            str(card.description), str(card.skills), request
        )
        res = ask_llm(system_prompt=system_prompt_message, user_prompt=user_prompt)
    except Exception:
        raise LLMError()
    return (illoc, res)
