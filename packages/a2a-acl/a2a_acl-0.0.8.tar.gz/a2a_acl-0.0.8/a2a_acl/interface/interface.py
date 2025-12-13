from dataclasses import dataclass
from enum import StrEnum


class DeclarativeForce(StrEnum):
    """Declarations kinds that can be made in .asi interface files."""

    BELIEF = "belief"  # a belief is readable (with ask)
    INPUT = "input"  # a belief can be added (with tell)
    ACTION = "action"  # a goal can be activated (with achieve)


@dataclass
class SkillRequest:
    """Description of skills used to filter skills."""

    declaration_kind: DeclarativeForce
    functor: str
    arity: int


@dataclass
class SkillDeclaration:
    """A skill as declared in a .asi interface file"""

    declaration_kind: DeclarativeForce
    functor: str
    arity: int
    doc: str

    def conforms_to(self, intf: SkillRequest) -> bool:
        return (
            self.declaration_kind == intf.declaration_kind
            and self.functor == intf.functor
            and self.arity == intf.arity
        )


@dataclass
class ACLAgentCard:
    """An agent card as declared in a .asi interface file."""

    name: str
    doc: str
    skills: list[SkillDeclaration]
    supported_codecs: list[str]

    def has_declared_skill(self, r: SkillRequest) -> bool:
        for skill in self.skills:
            if skill.conforms_to(r):
                return True
        return False

    def has_declared_skills(self, s: list[SkillRequest]) -> bool:
        # forall
        for skill in s:
            if not self.has_declared_skill(skill):
                return False
        return True

    def add_codecs(self, codecs):
        for c in codecs:
            self.supported_codecs.append(c)
        return self
