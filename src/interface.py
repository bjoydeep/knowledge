from datetime import time
import os
import logging

from dotenv import load_dotenv
import streamlit as st

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.react.tool_parser import ReActOutput
from llama_stack_client.types.toolgroup_register_params import McpEndpoint

load_dotenv()


# ——————————————
# Page setup
# ——————————————
st.set_page_config(
    page_title="KG Demo",
    page_icon="assets/favicon.ico",
    #page_icon="random",
    layout="wide",
    #initial_sidebar_state="expanded",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# ———————— Dark Background CSS ————————
# st.markdown(
#     """
#     <style>
#       /* Entire app background */
#       [data-testid="stAppViewContainer"] {
#         background-color: #000000 !important;
#       }
#       /* Main content area (under header) */
#       [data-testid="stAppMain"] {
#         background-color: #000000 !important;
#       }
#       /* Sidebar background */
#       [data-testid="stSidebar"] {
#         background-color: #111111 !important;
#       }
#       /* Optional: invert text to white for readability */
#       .css-1d391kg, .css-1v0mbdj, .stText, h1, h2, h3, h4, p, span {
#         color: #f0f0f0 !important;
#       }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

##E8F0FE
# Custom CSS
st.markdown(
    """
    <style>
      /* Chat bubbles */
      .stChatMessage p { font-family: "Helvetica Neue", sans-serif; line-height: 1.5; }
      /* User bubble */
      .stChatMessage[data-role="user"] .stMarkdown { 
        background-color: #F1F3F4 !important;
        border-radius: 12px; padding: 8px;
      }
      /* Assistant bubble */
      .stChatMessage[data-role="assistant"] .stMarkdown { 
        background-color: #F1F3F4 !important;
        border-radius: 12px; padding: 8px;
      }
      /* Hide default Streamlit menu */
      .css-1adrfps { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------
# Branded header (using st.image)
# --------------------------
logo_path = "assets/RedHat_logo.png"

# # Use columns for precise control
# col_logo, col_title = st.columns([1, 8], gap="small")
# with col_logo:
#     st.image(logo_path, width=180)  # increase from 50→80px
# with col_title:
#     st.markdown(
#         """
#         <h1 style="margin:0; font-size:2.5rem;">Knowledge Graph Demo</h1>
#         <p style="color:gray; margin-top:-10px;">
#         Agentic AI with Llama Stack and MCP Server
#         </p>
#         """,
#         unsafe_allow_html=True,
#     )

# Row 1: logo by itself
st.image(logo_path, width=180)

# Row 2: title (and subtitle) by itself
st.markdown(
    """
    <h1 style="margin:0; font-size:2.5rem;">Knowledge Graph Demo</h1>
    <p style="color:gray; margin-top:-10px;">
      Agentic AI with Llama Stack and MCP Server
    </p>
    """,
    unsafe_allow_html=True,
)

# Sidebar logo & controls
st.sidebar.image("assets/RedHat_logo.png", width=180)
st.sidebar.header("Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.001)
model_choice = st.sidebar.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

# ——————————————
# Logging & LlamaStack setup
# ——————————————
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

LLAMA_STACK_SERVER = os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_MODEL = f"openai/{model_choice}"

client = LlamaStackClient(base_url=LLAMA_STACK_SERVER)
client.toolgroups.register(
    toolgroup_id="mcp::neo",
    provider_id="model-context-protocol",
    mcp_endpoint=McpEndpoint(uri="http://localhost:8000/sse"),
)

# ——————————————
# Chat state & layout
# ——————————————
if "messages" not in st.session_state:
    st.session_state.messages = []


#left_col, right_col = st.columns((3, 1))
left_col = st.columns(1)[0]

# Chat area
with left_col:
    #Display chat history
    for msg in st.session_state.messages:
        avatar = (
            "assets/user.png" if msg["role"] == "user" else "assets/assistant.png"
        )
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Setting up the prompt
    instruct=(
            "You are a helpful assistant constrained to answer only from the Neo4j graph data."
            "When a user asks about a node “X”:"
            "1. Find any node whose `name` property matches X (case-insensitive, approximate match)."  
            "2. If no match, find all nodes labeled X (case-insensitive). " 
            "3. For the matched node(s), fetch all directly connected neighbors (both incoming and outgoing).  "
            "4. Return your answer based solely on those graph results. "
            )

    # Input for new messages
    prompt = st.chat_input("Ask something...")
    if prompt:
        # Append user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "avatar_url": "assets/user.png",
        })
        
        # Build and run agent
        agent = Agent(
            client,
            model=LLAMA_STACK_MODEL,
            instructions = instruct,
            tools=["mcp::neo"],
            #response_format={
            #    "type": "json_schema",
            #    "json_schema": ReActOutput.model_json_schema(),
            #},
            output_shields=[],
            enable_session_persistence=True,
            sampling_params={"strategy": {"type": "top_p", "temperature": temperature, "top_p": 0.9}},
        )
        session_id = agent.create_session("streamlit-session")

        full_response = ""

        # Display immediately
        with st.chat_message("user", avatar="assets/user.png"):
            st.markdown(prompt)


        # Get response from LlamaStack API
        with st.chat_message("assistant", avatar="assets/assistant.png"):
            message_placeholder = st.empty()
            response = agent.create_turn(
                messages=[{"role": "user", "content": prompt}],
                session_id=session_id,
            )
            for chunk in response:

                # if hasattr(chunk.event.payload.delta, "text"):
                #     full_response += chunk.event.payload.delta.text
                #     message_placeholder.markdown(full_response + "▌")
                
                try: 
                    #logger.info(f"chunk: {chunk}\n")
                    if chunk.event.payload.event_type == "step_progress":
                        if chunk.event.payload.delta.type == "text":
                            full_response += chunk.event.payload.delta.text
                            message_placeholder.markdown(full_response + "▌")
                    
                    if chunk.event.payload.event_type == "step_complete":
                        if chunk.event.payload.step_details:
                            step_details = chunk.event.payload.step_details
                            ###################
                            # Check if this is a tool execution step
                            if hasattr(step_details, 'step_type') and step_details.step_type == 'tool_execution':
                                logger.info("="*60)
                                logger.info("🔧 TOOL EXECUTION STEP DETECTED")
                                
                                # Extract tool calls
                                if hasattr(step_details, 'tool_calls') and step_details.tool_calls:
                                    logger.info("📞 TOOL CALLS:")
                                    for i, tool_call in enumerate(step_details.tool_calls):
                                        logger.info(f"  Call #{i+1}:")
                                        logger.info(f"    Tool Name: {tool_call.tool_name}")
                                        logger.info(f"    Call ID: {tool_call.call_id}")
                                        logger.info(f"    Arguments: {tool_call.arguments}")
                                        logger.info(f"    Arguments JSON: {tool_call.arguments_json}")
                                
                                # Extract tool responses
                                if hasattr(step_details, 'tool_responses') and step_details.tool_responses:
                                    logger.info("📋 TOOL RESPONSES:")
                                    for i, tool_response in enumerate(step_details.tool_responses):
                                        logger.info(f"  Response #{i+1}:")
                                        logger.info(f"    Tool Name: {tool_response.tool_name}")
                                        logger.info(f"    Call ID: {tool_response.call_id}")
                                        
                                        # Extract content from tool response
                                        if hasattr(tool_response, 'content') and tool_response.content:
                                            for j, content_item in enumerate(tool_response.content):
                                                if hasattr(content_item, 'text'):
                                                    logger.info(f"    Content #{j+1}: {content_item.text}")
                                                    
                                                    # Pretty print JSON if it looks like JSON
                                                    try:
                                                        import json
                                                        parsed_json = json.loads(content_item.text)
                                                        logger.info(f"    Parsed JSON: {json.dumps(parsed_json, indent=2)}")
                                                    except:
                                                        pass  # Not JSON, that's fine
                                
                                # Log timing information
                                if hasattr(step_details, 'started_at') and hasattr(step_details, 'completed_at'):
                                    duration = step_details.completed_at - step_details.started_at
                                    logger.info(f"⏱️  Tool execution took: {duration.total_seconds():.2f} seconds")                               

                            ####################
                            if hasattr(step_details, "violation") and step_details.violation:
                                violation = step_details.violation
                                logger.info(f"violation: {violation}")
                                full_response = violation.metadata.get("violation_type", "") + " " + violation.user_message

                except:
                    logger.info("oops! Error! Lets keep moving..........")
            
            message_placeholder.markdown(full_response)

            # Append assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "avatar_url": "assets/assistant.png",
            })
        logger.info("--- Instruction to LLM: ---")
        logger.info(instruct)
       
        # Force a rerun to update the display
        st.rerun()




# Optionally you can put additional docs or logs here
#with right_col:
#    st.markdown("#### Logs")
#    st.text("See console for details")
