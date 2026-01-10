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


Our data model:
AgentExecution:
query='Lets talk about ITC?' response="Here's an overview of **ITC Limited** based on the latest data:\n\n- **Current Price**: ₹338.25\n- **Percent Change**: -0.78% (slight decline)\n- **P/E Ratio**: 21.16 (Price-to-Earnings ratio, indicating valuation)\n- **Industry**: Diversified FMCG (Fast-Moving Consumer Goods)\n\n### Key Points About ITC:\n1. **Business Segments**:\n   - **FMCG**: Cigarettes, packaged foods, personal care, and education products.\n   - **Hotels**: Luxury and premium hotel chains under brands like *ITC Hotels*.\n   - **Paperboards & Packaging**: Leading player in sustainable packaging solutions.\n   - **Agri-Business**: Exports agricultural commodities like wheat, rice, and spices.\n   - **IT & Financial Services**: ITC Infotech and investments in financial services.\n\n2. **Recent Performance**:\n   - The stock is slightly down today (-0.78%), but ITC has historically been a resilient stock with strong dividends.\n   - The **P/E ratio of 21.16** suggests it is moderately valued compared to peers.\n\n3. **Why Investors Like ITC**:\n   - **Dividend Yield**: Known for consistent dividends, making it attractive for income investors.\n   - **Diversification**: Strong presence across multiple sectors, reducing risk.\n   - **ESG Focus**: Leader in sustainability, with initiatives like plastic-neutral packaging.\n\n4. **Challenges**:\n   - **Regulatory Risks**: Cigarette business faces high taxation and regulatory pressures.\n   - **Competition**: FMCG segment competes with giants like HUL, Nestlé, and Britannia.\n\nWould you like a deeper analysis on any specific aspect (e.g., financials, dividend history, or sector comparison)?" agent_name='finance_agent' model=None 

tool_calls=[ToolCall(tool_name='fetch_security_data', arguments={'symbol': 'ITC'}, call_order=1, created_at=datetime.datetime(2026, 1, 10, 17, 1, 19, 955961))] created_at=datetime.datetime(2026, 1, 10, 17, 1, 19, 957139)