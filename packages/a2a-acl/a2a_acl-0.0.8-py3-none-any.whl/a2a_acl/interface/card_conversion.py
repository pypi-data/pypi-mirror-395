from a2a.types import AgentCard, AgentCapabilities

from a2a_acl.protocol import EXTENSION
from a2a_acl.interface.interface import ACLAgentCard
from a2a_acl.interface.skill_conversion import (
    a2a_skill_of_bdi_skill,
    bdi_skill_of_a2a_skill,
)


def a2a_card_from_bdi_card(c: ACLAgentCard, url: str) -> AgentCard:
    asp_skills = [a2a_skill_of_bdi_skill(s) for s in c.skills]
    return AgentCard(
        name=c.name,
        description=c.doc,
        url=url,
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(
            streaming=False,
            push_notifications=True,
            extensions=[EXTENSION],
        ),
        skills=asp_skills,
        supports_authenticated_extended_card=False,
    )


def bdi_card_from_a2a_card(c: AgentCard) -> ACLAgentCard:
    """
    Example of card for a BDI agent :
        additional_interfaces=None
        capabilities=AgentCapabilities(extensions=[AgentExtension(description='MOSAICO A2A BDI', params=None, required=True, uri='https://gitlab.eclipse.org/eclipse-research-labs/mosaico-project/a2a-agentspeak/-/blob/main/a2a_acl_protocol/MOSAICO_A2A_BDI_PROTOCOL')], push_notifications=True, state_transition_history=None, streaming=False)
        default_input_modes=['text']
        default_output_modes=['text']
        description='An agent which sends ping'
        documentation_url=None
        icon_url=None
        name='Pinger Agent'
        preferred_transport='JSONRPC'
        protocol_version='0.3.0'
        provider=None
        security=None
        security_schemes=None
        signatures=None
        skills=[
            AgentSkill(description='send a ping request (needs 1 parameter)', examples=['(achieve,do_ping(0))'], id='do_ping', input_modes=None, name='do_ping (from BDI agent)', output_modes=None, security=None, tags=['do_ping']),
            AgentSkill(description='send a secret (needs 1 parameter)', examples=['(achieve,share_secret(0))'], id='share_secret', input_modes=None, name='share_secret (from BDI agent)', output_modes=None, security=None, tags=['share_secret']),
            AgentSkill(description='do nothing (needs 0 parameter)', examples=['(tell,pong)'], id='pong', input_modes=None, name='pong (from BDI agent)', output_modes=None, security=None, tags=['pong'])
            ]
        supports_authenticated_extended_card=False
        url='http://127.0.0.1:9999/'
        version='1.0.0'
    """
    skills = [bdi_skill_of_a2a_skill(s) for s in c.skills]
    return ACLAgentCard(c.name, c.description, skills, [])
