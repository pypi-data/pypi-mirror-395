# A2A ACL
ACL agents on A2A protocol (work in progress).

# Features
 * Agents that send and receive messages with an illocution/performative on top of A2A.
 * Simply describe A2A agent cards and skills in an interface file in a dedicated format.
 * Targets that are not declared in the interface are private and ignored from incoming messages.
 * Extension of the A2A protocol that supports _tell_, _achieve_, and _ask_ performatives.
 * Asynchronous answers for _achieve_ messages (to request some actions and optionally answer later).
 * Different codecs can be used to encode/decode the content of the messages.


# Examples and Documentation

Some examples are given in the `sample_agents` and `tests` directories. This is the only source of documentation currently.


# Requirements
This module relies on the A2A Protocol (package `a2a-sdk`). 


