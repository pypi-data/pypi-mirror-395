from rdflib import Namespace

CS = Namespace("http://cs-framework.org/schema/")

# Classes
CONCEPT = CS.Concept
SYNCHRONIZATION = CS.Synchronization
ACTION = CS.Action
EVENT = CS.Event
ACTION_INVOCATION = CS.ActionInvocation

# Properties
HAS_NAME = CS.hasName
HAS_STATE = CS.hasState
BELONGS_TO = CS.belongsTo
TRIGGERED_BY = CS.triggeredBy
CAUSED_BY = CS.causedBy
INVOKES = CS.invokes
HAS_CONDITION = CS.hasCondition
STATUS = CS.status
