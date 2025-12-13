"""
CrewAI framework base class implementing the BaseAgent interface.
Uses official CrewAI SDK for agent creation and management.
"""

from typing import Any, Dict

import os

from crewai import Agent, Crew, Task

from topaz_agent_kit.agents.base.base_agent import BaseAgent
from topaz_agent_kit.core.exceptions import AgentError
from topaz_agent_kit.utils.file_utils import FileUtils
from topaz_agent_kit.utils.logger import Logger
from topaz_agent_kit.utils.mcp_utils import matches_tool_patterns


class CrewAIBaseAgent(BaseAgent):
    """
    Base class for CrewAI agents using official SDK patterns.
    Handles CrewAI-specific initialization, tool management, and execution.
    """
    
    def __init__(self, agent_id: str, **kwargs):
        # Ensure agent_config is in kwargs before calling parent
        if "agent_config" not in kwargs:
            raise AgentError("CrewAI agent requires agent_config in constructor")
        
        super().__init__(agent_id, "crewai", **kwargs)
        
        # Override logger with framework-specific name
        self.logger = Logger(f"CrewAIAgent({agent_id})")
        
        # CrewAI-specific attributes only
        self.crew = None
        self.role = ""
        self.goal = ""
        self.backstory = ""
        self.task = None
        self.task_description = ""
        self.task_expected_output = ""
        
    def _setup_environment(self):
        """Setup CrewAI environment"""
        self._setup_azure_openai_env()

    def _setup_azure_openai_env(self) -> None:
        """Simplified Azure environment setup - just sets required variables without checks"""

        # Set LiteLLM's expected variables
        os.environ["AZURE_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
        os.environ["AZURE_API_BASE"] = os.getenv("AZURE_OPENAI_API_BASE")
        os.environ["AZURE_API_VERSION"] = os.getenv("AZURE_OPENAI_API_VERSION")
    
    def _initialize_agent(self) -> None:
        """Initialize CrewAI agent"""
            
        self.logger.info("Initializing CrewAI agent: {}", self.agent_id)
        
        try:
            # Load CrewAI fields (role, goal, backstory) with support for inline/file/jinja
            self.role = self._prompt_loader.load_prompt(spec=self._prompt_spec.get("role"))
            self.goal = self._prompt_loader.load_prompt(spec=self._prompt_spec.get("goal"))
            self.backstory = self._prompt_loader.load_prompt(spec=self._prompt_spec.get("backstory"))
            
            if not self.role or not self.goal or not self.backstory:
                self.logger.error("CrewAI agent missing required fields: role, goal, backstory")
                raise AgentError("CrewAI agent missing required fields: role, goal, backstory")
            
            self.logger.debug("Loaded CrewAI fields - role: {} chars, goal: {} chars, backstory: {} chars", len(self.role), len(self.goal), len(self.backstory))
            
            # Load task description and expected output 
            self._task_spec = self._prompt_spec.get("task")
            self.task_description = self._prompt_loader.load_prompt(spec=self._task_spec.get("description"))
            self.task_expected_output = self._prompt_loader.load_prompt(spec=self._task_spec.get("expected_output"))
            
            if not self.task_description:
                self.logger.error("CrewAI agent missing required field: task_description")
                raise AgentError("CrewAI agent missing required field: task_description")
                
            if not self.task_expected_output:
                self.logger.warning("CrewAI agent missing optional field: task_expected_output")
            
        except Exception as e:
            self.logger.error("Failed to initialize CrewAI agent: {}", e)
            raise
    
    
    async def _log_tool_details(self) -> None:
        """Log filtered tool details for CrewAI framework"""
        if not hasattr(self, '_filtered_individual_tools') or not self._filtered_individual_tools:
            self.logger.info("No tools attached")
            return
        
        # After-filter format: count + one-per-line names
        names = []
        for tool in self._filtered_individual_tools:
            if hasattr(tool, 'name'):
                names.append(tool.name)
            else:
                names.append(type(tool).__name__)
        
        self.logger.success(f"MCP tools count after filtering: {len(names)}")
        for name in sorted(set(names)):
            self.logger.success(f"  - {name}")
    
    
    async def _filter_mcp_tools(self) -> None:
        """Single function to filter MCP tools (handles both wrappers and individual tools)"""
        if not self.tools:
            return
            
        mcp_config = self.agent_config.get("mcp", {})
        servers_config = mcp_config.get("servers", [])
        
        if not servers_config:
            return
            
        # Aggregate wildcard patterns and toolkits from pipeline.yml
        all_patterns = []
        all_toolkits = []
        for server in servers_config:
            all_patterns.extend(server.get("tools", []))
            all_toolkits.extend(server.get("toolkits", []))
        # De-duplicate while preserving order
        all_patterns = list(dict.fromkeys(all_patterns))
        all_toolkits = list(dict.fromkeys(all_toolkits))
        self.logger.info(f"Allowed tool patterns from pipeline.yml: {all_patterns}")
        self.logger.info(f"Allowed toolkits from pipeline.yml: {all_toolkits}")
        
        # Handle CrewAI MCP tools (returned directly as list from framework_mcp_manager)
        # Following working example: adapter.tools returns list of tools directly
        if self.tools:
            original_count = len(self.tools)
            self.logger.info(f"MCP tools count before filtering: {original_count}")
            
            # Filter tools using wildcard matcher
            filtered_tools = []
            seen_tool_names = set()  # Prevent duplicates
            
            for tool in self.tools:
                if hasattr(tool, 'name'):
                    tool_name = tool.name
                    
                    # Check if this tool is allowed via wildcard patterns
                    if matches_tool_patterns(tool_name, all_patterns, all_toolkits) and tool_name not in seen_tool_names:
                        filtered_tools.append(tool)
                        seen_tool_names.add(tool_name)
                        self.logger.debug(f"Keeping tool: {tool_name}")
                    else:
                        self.logger.debug(f"Filtering out tool: {tool_name}")
                else:
                    self.logger.warning(f"Tool {type(tool).__name__} has no name attribute, filtering it out")
            
            # Store filtered tools for use in _create_agent
            self._filtered_individual_tools = filtered_tools
        else:
            self._filtered_individual_tools = []
            self.logger.info("No MCP tools to filter")
    
    
    def _create_agent(self) -> None:
        """Create CrewAI agent and crew - single unified approach"""
        try:
            self.logger.debug("Creating CrewAI agent with LLM: {} (type: {})", self.llm, type(self.llm))
            self.logger.debug("CrewAI agent goal: {}", self.goal)

            # Handle MCP tools - use filtered tools from _filter_mcp_tools
            # Tools are returned directly as a list from framework_mcp_manager (adapter.tools)
            if hasattr(self, '_filtered_individual_tools') and self._filtered_individual_tools:
                self._mcp_tools = self._filtered_individual_tools
                self.logger.success("Using native CrewAI MCP tools ({} tools)", len(self._mcp_tools))
            else:
                self._mcp_tools = []
                self.logger.info("No MCP tools found, proceeding without MCP tools")

            # Create agent with filtered tools (empty list is fine if no tools)
            # Always set multimodal=True to enable multimodal support when images are present
            # (No performance impact for text-only tasks)
            self.agent = Agent(
                role=self.role,
                goal=self.goal,
                backstory=self.backstory,
                tools=self._mcp_tools,
                llm=self.llm,
                multimodal=True,  # Enable multimodal support for images
                verbose=True
            )
            
            self.logger.success("Created CrewAI components: agent, task, crew")
            self.logger.info("Agent tools: {} tools available (added dynamically)", len(self.tools))
    
        except Exception as e:
            raise AgentError(f"Failed to create CrewAI components: {e}")
    
    def _build_multimodal_content(self, rendered_inputs: str, context: Dict[str, Any]) -> str:
        """
        Build enhanced task description for CrewAI with embedded multimodal content.
        
        CrewAI multimodal support:
        - ✅ Image URLs: Direct HTTP/HTTPS URLs work reliably with AddImageTool
        - ⚠️ Local images: Not fully supported (see known limitations)
        - ✅ Documents: Extracted text included directly in description
        
        Args:
            rendered_inputs: Rendered prompt text
            context: Execution context containing user_files_data
            
        Returns:
            Enhanced task description with embedded multimodal content
        """
        description_parts = [rendered_inputs] if rendered_inputs else []
        user_files_data = context.get("user_files_data", {})
        
        # Check if the agent's prompt template uses user_files variable
        # If not, skip file processing to avoid unnecessary data processing
        # Note: CrewAI uses "task" instead of "inputs" for prompt key
        if not self._should_process_files(prompt_key="task"):
            return rendered_inputs or ""
        
        # Add image URLs - these work reliably with CrewAI's AddImageTool
        # Format matches CrewAI examples: "Please analyze this image: {url}"
        urls = user_files_data.get("urls", [])
        for url_data in urls:
            url_type = url_data.get("type")
            url = url_data["url"]
            try:
                if url_type == "image":
                    description_parts.append(f"\n\nPlease analyze this image: {url}")
                    self.logger.debug("Added image URL to CrewAI task description: {}", url)
                elif url_type == "document":
                    description_parts.append(f"\n\nPlease analyze this document: {url}")
                    self.logger.debug("Added document URL to CrewAI task description: {}", url)
            except Exception as e:
                self.logger.error("Failed to add {} URL {} to CrewAI task: {}", url_type, url, e)
                raise  # Fail agent execution on error
        
        # Add local images - marked as limitation, but attempt base64 for basic support
        # Note: Local image processing has known compatibility issues with Azure OpenAI
        images = user_files_data.get("images", [])
        if images:
            self.logger.warning("Local images detected - CrewAI has known limitations with local image processing")
            for idx, img in enumerate(images, 1):
                try:
                    # Attempt base64 data URL (may not work reliably)
                    base64_data = FileUtils.encode_bytes_to_base64(img["data"])
                    data_url = f"data:{img['metadata']['mime_type']};base64,{base64_data}"
                    if len(images) > 1:
                        description_parts.append(f"\n\nHere is image {idx}: {data_url}")
                    else:
                        description_parts.append(f"\n\nHere is an image: {data_url}")
                    self.logger.debug("Added local image to CrewAI task description (may not process correctly): {}", img["name"])
                except Exception as e:
                    self.logger.error("Failed to add local image {} to CrewAI task: {}", img.get("name", "unknown"), e)
                    raise  # Fail agent execution on error
        
        # Add local documents
        # For text-based documents: include extracted text directly
        # For binary documents: include reference (agent can use MCP tools if needed)
        documents = user_files_data.get("documents", [])
        for doc in documents:
            try:
                if doc.get("text"):
                    # Include extracted text directly in description
                    description_parts.append(f"\n\nDocument: {doc['name']}\n{doc['text']}")
                    self.logger.debug("Added document text to CrewAI task description: {}", doc["name"])
                else:
                    # For binary documents without extractable text, include reference
                    # Agent can use common_read_document MCP tool if needed
                    description_parts.append(
                        f"\n\nDocument reference: {doc['name']} "
                        f"({doc['metadata']['mime_type']}, {doc['metadata']['size_bytes']} bytes). "
                        f"File path: {doc['path']}"
                    )
                    self.logger.debug("Added document reference to CrewAI task description: {}", doc["name"])
            except Exception as e:
                self.logger.error("Failed to add document {} to CrewAI task: {}", doc.get("name", "unknown"), e)
                raise  # Fail agent execution on error
        
        return "\n".join(description_parts)

    async def _execute_agent(self, context: Dict[str, Any], variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute CrewAI workflow - create new Task and Crew with rendered description.
        Uses persistent MCP tools.
        """
        try:
            # Use pre-rendered inputs from base_agent.execute() (stored in self._rendered_inputs)
            rendered_inputs = self._rendered_inputs if hasattr(self, '_rendered_inputs') else None
            if not rendered_inputs:
                # Fallback: render if not available (shouldn't happen in normal flow)
                rendered_inputs = self._render_prompt_with_variables(self.task_description, variables)
            self.logger.debug(f"Agent {self.agent_id} Inputs: {rendered_inputs}")

            # Build multimodal content (embeds images/documents/URLs in description)
            enhanced_description = self._build_multimodal_content(rendered_inputs, context)

            # Create new task with enhanced description (includes multimodal content)
            self.task = Task(
                description=enhanced_description,
                agent=self.agent,
                expected_output=self.task_expected_output
            )
                    
            # Create new crew with persistent MCP tools
            self.crew = Crew(
                agents=[self.agent],
                tasks=[self.task],
                verbose=True
            )
                    
            # Execute crew with persistent MCP tools
            self.logger.info("Executing CrewAI workflow with rendered inputs")
            result = self.crew.kickoff()
            
            self.logger.success("CrewAI workflow execution completed successfully")
            
            # Return raw result - base_agent.execute() will parse it
            return result
            
        except Exception as e:
            self.logger.error("CrewAI execution failed: {}", e)
            raise AgentError(f"CrewAI execution failed: {e}")
    
    async def cleanup(self) -> None:
        """Cleanup MCP resources"""
        # MCPServerAdapter manages its own lifecycle, no explicit cleanup needed
        # Just call parent cleanup
        await super().cleanup()
 