 - Added databse connections
 - agent execution 
 ''' 
 sql
 CREATE TABLE agent_executions (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    query TEXT NOT NULL,
    response TEXT NOT NULL,

    agent_name TEXT NOT NULL,
    model TEXT
);
'''
- tool_calls
'''
CREATE TABLE tool_calls (
    id BIGSERIAL PRIMARY KEY,
    execution_id BIGINT NOT NULL REFERENCES agent_executions(id) ON DELETE CASCADE,

    tool_name TEXT NOT NULL,
    arguments JSONB NOT NULL,
    call_order INTEGER NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
'''

## We're currently dividing our system into 2 parts - The core which is agent execution and a sub-part: tool execution.
    - After creating the 2 tables, we need to create datamodels for the same.
    - As we need to store the tool calls in the database, we need to create a tool call and execution model.