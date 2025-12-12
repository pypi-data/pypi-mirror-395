AVAILABLE_LLMS = '/llms'
DEFAULT_PROMPTS = '/prompts/defaults'

WORKSPACES = '/workspaces'
WORKSPACE = WORKSPACES + '/{workspace_id}'

AUDIT = WORKSPACE + '/query-audit'

USERS = WORKSPACE + '/users'
USERS_ADHOC = WORKSPACE + '/users/adhoc'

USER = WORKSPACE + '/users/{user_id}'
USER_GROUPS = USER + '/groups'
USER_WORKSPACES = '/users/{user_id}/workspaces'
USER_VIEWS = USER + '/views'
USER_TOKEN = USER + '/token'
USER_ROLE = USER + '/role'
USER_ATTRIBUTES = USER + '/attributes'

DATASOURCES = WORKSPACE + '/datasources'
DATASOURCE = DATASOURCES + '/{datasource_id}'
DATASOURCE_PING = DATASOURCE + '/ping'
DATASOURCE_DATA = DATASOURCE + '/data/secure'
DATASOURCE_TREE = DATASOURCE + '/tree'

DATASOURCE_RELATIONS = DATASOURCE + '/metadata/relations'
DATASOURCE_DESCRIPTIONS = DATASOURCE + '/metadata/descriptions'

DATASOURCE_PERMISSIONS = DATASOURCE + '/permissions'
DATASOURCE_PERMISSION = DATASOURCE + '/permissions/{permission_id}'

PERMISSIONS = WORKSPACE + '/permissions'

GROUPS = WORKSPACE + '/groups'
GROUP = WORKSPACE + '/groups/{group_id}'
GROUP_USERS = GROUP + '/users'

VIEWS = WORKSPACE + '/views'
VIEW = VIEWS + '/{view_id}'
VIEW_CONNECTION_STRING = VIEW + '/users/{user_id}/connection_strings'
VIEW_EXECUTE = VIEW + '/execute'
VIEW_ENTITIES = VIEW + '/entities'
VIEW_PERMISSIONS = VIEW + '/permissions'
VIEW_TREE_DISPLAY = VIEW + '/tree/display'
VIEW_MCP = VIEW + '/mcp'

LLMS = WORKSPACE + '/llms'
LLM = LLMS + '/{llm_id}'

MCPS = WORKSPACE + '/mcps'
MCPS_IDS = MCPS + '/ids'
MCPS_PERMITTED = MCPS + '/permitted'
MCP = MCPS + '/{mcp_id}'
MCP_TOOLS = MCP + '/tools'
MCP_VIEW = MCP + '/view'

AGENTS = WORKSPACE + '/agents'
AGENTS_PERMITTED = AGENTS + '/permitted'
AGENTS_PERMITTED_SESSIONS = AGENTS_PERMITTED + '/sessions'
AGENT = AGENTS + '/{agent_id}'
AGENT_GENERATE = AGENT + '/generate'
AGENT_SESSIONS = AGENT + '/sessions'
AGENT_ENTITIES = AGENT + '/entities'
AGENT_PERMITTED_SESSIONS = AGENT_SESSIONS + '/permitted'

SESSION = AGENT_SESSIONS + '/{session_id}'
SESSION_TITLE = SESSION + '/title'
SESSION_MESSAGE = SESSION + '/message'
SESSION_GENERATE = SESSION + '/generate'
