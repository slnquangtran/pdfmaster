# Data Model: AI Agent Builder Framework

**Feature**: 009-ai-agent-builder  
**Date**: 2026-03-23

## Entities

### AgentTemplate
Defines an AI agent's complete configuration.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique template identifier (UUID) |
| name | str | Human-readable agent name |
| description | str | Brief description of agent purpose |
| version | str | Semantic version (e.g., "1.0.0") |
| category | str | Category (pdf, design, text, data, custom) |
| icon | str | Emoji or icon identifier |
| instruction_blocks | List[InstructionBlock] | Ordered instruction sections |
| tools | List[str] | List of allowed tool IDs |
| behavior_rules | List[BehaviorRule] | Behavioral constraints |
| response_format | ResponseFormat | Output format configuration |
| variables | List[VariableDef] | Placeholder variables |
| metadata | dict | Author, created_at, updated_at, etc. |

### InstructionBlock
A section of agent instructions following Claude's pattern.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Block identifier |
| type | str | persona, rules, examples, constraints, format |
| content | str | Instruction text with {variables} |
| priority | int | Execution priority (1=highest) |
| enabled | bool | Whether block is active |

### BehaviorRule
Defines how the agent should or should not behave.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Rule identifier |
| trigger | str | Condition that triggers this rule |
| action | str | Required action (allow, deny, modify, escalate) |
| message | str | Response message when triggered |
| severity | str | info, warning, critical |

### Tool
A capability that agents can use.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Tool identifier |
| name | str | Display name |
| category | str | Tool category |
| description | str | What the tool does |
| parameters | List[ParamDef] | Input parameters |
| returns | str | Return type description |
| enabled | bool | Whether tool is available |

### AgentSession
A running instance of an agent with history.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Session identifier |
| agent_id | str | Template ID being used |
| started_at | datetime | Session start time |
| messages | List[Message] | Conversation history |
| tool_calls | List[ToolCall] | Tools invoked during session |
| variables | dict | Current variable values |
| status | str | active, completed, error |

### Message
A single message in agent conversation.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Message identifier |
| role | str | user, assistant, system, tool |
| content | str | Message content |
| timestamp | datetime | Message time |
| metadata | dict | Additional metadata |

### ToolCall
Record of a tool invocation.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Call identifier |
| tool_id | str | Which tool was called |
| parameters | dict | Input parameters |
| result | str | Tool output |
| status | str | success, error, timeout |
| duration_ms | int | Execution time |
| timestamp | datetime | Call time |

### AgentChain
A sequence of agents for pipeline processing.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Chain identifier |
| name | str | Chain display name |
| steps | List[ChainStep] | Ordered agent steps |
| input_mapping | dict | Maps input to first agent |
| output_mapping | dict | Maps last agent output |
| created_at | datetime | Creation time |

### ChainStep
A single step in an agent chain.

| Field | Type | Description |
|-------|------|-------------|
| position | int | Step order (1-indexed) |
| agent_id | str | Agent template to use |
| input_from | str | Previous step or "input" |
| transform | Optional[str] | Data transformation expression |
| condition | Optional[str] | Conditional execution |

### TestResult
Output from an agent test session.

| Field | Type | Description |
|-------|------|-------------|
| id | str | Test result identifier |
| agent_id | str | Agent that was tested |
| session_id | str | Session used |
| input | str | Test input |
| output | str | Agent response |
| tool_calls | List[ToolCall] | Tools used |
| passed | bool | Whether test passed |
| notes | str | Tester notes |

## Relationships

```
AgentTemplate 1──* InstructionBlock
AgentTemplate 1──* BehaviorRule
AgentTemplate *──* Tool (through tool_ids)
AgentTemplate 1──* AgentSession
AgentTemplate 1──* TestResult
AgentChain 1──* ChainStep
ChainStep *──1 AgentTemplate
AgentSession 1──* Message
AgentSession 1──* ToolCall
```

## Validation Rules

1. AgentTemplate must have at least one instruction block of type "persona"
2. Tool references must exist in the tool registry
3. Variable placeholders in instructions must have matching VariableDef
4. Chain steps must reference valid agent templates
5. Response format schema must be valid JSON Schema if type is "json"
6. Behavior rules must have valid trigger syntax
7. Session messages must maintain chronological order

## State Transitions

### Template States
```
[Draft] → [Active] → [Archived]
   ↑         ↓
   └─[Edit]─┘
```

### Session States
```
[Created] → [Active] → [Completed]
               ↓
            [Error] → [Retry]
```

### Chain States
```
[Draft] → [Ready] → [Running] → [Completed]
                            ↓
                         [Error]
```
