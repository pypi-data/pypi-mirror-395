from a2a_acl.interface.interface import (
    DeclarativeForce,
    SkillDeclaration,
    ACLAgentCard,
)


class SyntaxError(Exception):
    def __init__(self, message: str, filename: str, line: str):
        self.message = message
        self.filename = filename
        self.line = line


def read_file(intf: str) -> ACLAgentCard:
    with open(intf, "r") as f:
        l = f.readline()
        assert l.startswith("name = ")
        name = l.removeprefix("name = ").removesuffix("\n")

        l = f.readline()
        assert l.startswith("doc = ")
        agent_doc = l.removeprefix("doc = ").removesuffix("\n")

        lines = []

        for l in f:

            if l == "\n":
                pass
            else:
                try:
                    [k, functor, arity, doc] = l.removesuffix("\n").split(" : ")
                    match k:
                        case "belief":
                            lines.append(
                                SkillDeclaration(
                                    declaration_kind=DeclarativeForce.BELIEF,
                                    doc=doc,
                                    functor=functor,
                                    arity=int(arity),
                                )
                            )
                        case "input":
                            lines.append(
                                SkillDeclaration(
                                    declaration_kind=DeclarativeForce.INPUT,
                                    doc=doc,
                                    functor=functor,
                                    arity=int(arity),
                                )
                            )
                        case "action":
                            lines.append(
                                SkillDeclaration(
                                    declaration_kind=DeclarativeForce.ACTION,
                                    doc=doc,
                                    functor=functor,
                                    arity=int(arity),
                                )
                            )
                        case _:
                            raise SyntaxError(intf, l, "Bad kind: " + k)
                except SyntaxError as e:
                    raise e
                except Exception as e:
                    raise SyntaxError(intf, l, "bad line structure")

        return ACLAgentCard(name, agent_doc, lines, [])
