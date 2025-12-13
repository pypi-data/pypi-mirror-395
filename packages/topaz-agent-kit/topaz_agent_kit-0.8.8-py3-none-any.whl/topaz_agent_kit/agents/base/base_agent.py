"""
Minimal agent interface that all agents must implement.
This provides the contract for agent orchestration while allowing framework-specific implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pathlib import Path
from dotenv import load_dotenv

from topaz_agent_kit.utils.json_utils import JSONUtils
from topaz_agent_kit.utils.prompt_loader import PromptLoader
from topaz_agent_kit.frameworks.framework_config_manager import FrameworkConfigManager
from topaz_agent_kit.frameworks.framework_model_factory import FrameworkModelFactory
from topaz_agent_kit.utils.logger import Logger
from topaz_agent_kit.core.exceptions import AgentError
from topaz_agent_kit.frameworks.framework_mcp_manager import FrameworkMCPManager
from topaz_agent_kit.utils.agent_output_parser import AgentOutputParser

class BaseAgent(ABC):
    """
    Minimal interface that all agents must implement.
    Framework-specific base classes inherit from this and provide framework-specific implementations.
    """
    
    def __init__(self, agent_id: str, agent_type: str, **kwargs):
        # Add logger for base class
        self.logger = Logger(f"BaseAgent({agent_id})")

        # Agent instance
        self.agent = None
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.framework_type = agent_type
        self.agent_config = kwargs.get("agent_config", {})
        self.mcp_config = kwargs.get("mcp_config")
        
        # Common attributes for all agents
        self.name = self.agent_config.get("name", agent_id)
        self.model_preference = self.agent_config.get("model")
        self.llm = None
        self.tools = []
        self.project_dir = ""

        # Prompt configuration
        self.prompt = ""
        self._prompt_spec = self.agent_config.get("prompt")
        self._prompt_loader = None  # Will be initialized when project_dir is available

        self._initialized = False
    
    @abstractmethod
    async def _filter_mcp_tools(self) -> None:
        """Framework-specific MCP tool filtering logic"""
        pass

    @abstractmethod
    async def _log_tool_details(self) -> None:
        """Framework-specific tool detail logging"""
        pass
    
    @abstractmethod
    def _setup_environment(self):
        """
        Setup framework-specific environment
        
        Args:
            project_dir: Project directory
        """
        pass

    @abstractmethod
    def _create_agent(self):
        """Create framework-specific agent"""
        pass

    @abstractmethod
    def get_agent_variables(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get agent-specific variables for prompt population."""
        pass

    @abstractmethod
    def _execute_agent(self, context: Dict[str, Any]):
        """
        Execute framework-specific agent

        Args:
            context: Execution context
        """
        pass

    @abstractmethod
    def _initialize_agent(self):
        """Initialize framework-specific agent"""
        pass

    def is_initialized(self) -> bool:
        """Check if agent has been initialized"""
        return self._initialized
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get basic agent information"""
        return {
            "id": self.agent_id,
            "type": self.agent_type,
            "initialized": self._initialized
        } 

    async def initialize(self, context: Dict[str, Any]) -> None:
        """Initialize the agent with context"""
        try:
            self.logger.debug("Initializing {} agent with context keys: {}", self.agent_type, list(context.keys()))
            self.logger.debug("Agent config: {}", self.agent_config)
            self.logger.debug("Model preference: {}", self.model_preference)
            
            self.project_dir = context.get("project_dir")
            if self.project_dir:
                self.project_dir = Path(self.project_dir)
                self.logger.info("Project directory from context: {}", self.project_dir)
            else:
                self.logger.error("No project_dir in context or parameter")
                raise AgentError("No project_dir in context or parameter")
            
            # Initialize prompt loader
            self._prompt_loader = PromptLoader(self.project_dir)
            
            # Setup environment
            load_dotenv(self.project_dir / ".env")
            self._setup_environment()

            # Load prompt
            if self._prompt_spec:
                self.logger.info("Loading prompt for agent {}...", self.agent_id)
                if self.agent_type != "crewai":
                    self.prompt = self._load_prompt(self._prompt_spec)
                    self.logger.success("Loaded prompt - instruction: {} chars, inputs: {} chars", len(self.prompt["instruction"]), len(self.prompt["inputs"]))
            else:
                self.logger.warning("No prompt specified")
                raise AgentError("No prompt specified")
            
            # Initialize LLM using unified factory
            self.logger.info("Starting LLM initialization with unified factory...")
            self._initialize_llm(context)
            self.logger.success("LLM initialization completed")
            
            # Initialize MCP tools using unified manager
            self.logger.info("Starting MCP tools initialization with unified manager...")
            await self._initialize_mcp_tools(context)
            self.logger.success("MCP tools initialization completed")

            # Initialize agent for any framework-specific initialization
            self.logger.info("Starting {} agent framework-specific initialization...", self.agent_type)
            self._initialize_agent()
            self._initialized = True
            self.logger.success(f"{self.agent_type} agent initialized successfully")

            # Create agent instance
            self.logger.debug(f"Creating {self.agent_type} agent...")
            self._create_agent()
            self.logger.success(f"{self.agent_type} agent created successfully")
            
        except Exception as e:
            self.logger.error(f"{self.agent_type} agent initialization failed: {e}")
            raise AgentError(f"{self.agent_type} agent initialization failed: {e}")

    def _load_prompt(self, prompt_spec: Dict[str, Any]) -> Dict[str, str]:
        """Load prompt template with instruction and inputs sections"""
        try:
            result = {}
            self.logger.debug("Using prompt format with instruction/inputs sections")
            
            # Load instruction prompt template (without rendering variables)
            instruction_spec = prompt_spec["instruction"]
            result["instruction"] = self._prompt_loader.load_prompt(instruction_spec)
            
            # Load inputs prompt template (without rendering variables)
            inputs_spec = prompt_spec["inputs"]
            result["inputs"] = self._prompt_loader.load_prompt(inputs_spec)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to load prompt: {e}")
            raise AgentError(f"Prompt loading failed: {e}")
    
    def _get_nested_value(self, data: Any, path: str) -> Any:
        """
        Get a nested value from a dictionary using dot notation path.
        
        Args:
            data: Dictionary or value to traverse
            path: Dot-separated path (e.g., "rfp_data.evaluation_criteria")
            
        Returns:
            Value at the path if found, None otherwise
        """
        if not path or not isinstance(data, dict):
            return None
        
        parts = path.split(".")
        value = data
        
        for field in parts:
            if isinstance(value, dict) and field in value:
                value = value[field]
            else:
                return None
        
        return value
    
    def _resolve_array_indexed_variable(self, parsed_data: dict, var_name: str, context: Dict[str, Any], agent_id: str) -> Any:
        """
        Resolve a variable that includes array indexing (e.g., "supplier_response_paths[supplier_loop.index]").
        
        Args:
            parsed_data: The parsed data dictionary to search in
            var_name: Variable name that may include array indexing
            context: Execution context for evaluating index expressions
            agent_id: Agent ID for logging purposes
            
        Returns:
            The resolved value if found, None otherwise
        """
        if '[' not in var_name or ']' not in var_name:
            return None
        
        # Extract base field name and index expression
        bracket_start = var_name.find('[')
        bracket_end = var_name.find(']')
        if bracket_start >= bracket_end:
            return None
        
        base_field = var_name[:bracket_start]
        index_expr = var_name[bracket_start + 1:bracket_end]
        
        # Get the base field value
        base_value = None
        if base_field in parsed_data:
            base_value = parsed_data[base_field]
        else:
            # Try nested path for base field
            base_value = self._get_nested_value(parsed_data, base_field)
        
        if base_value is None or not isinstance(base_value, list):
            return None
        
        # Evaluate index expression from context
        index_value = None
        if '.' in index_expr:
            # Nested path like "supplier_loop.index"
            # First try direct context access (e.g., context["supplier_loop"]["index"])
            index_value = self._get_nested_value(context, index_expr)
            # If not found, try accessing through variables (for loop context)
            if index_value is None:
                parts = index_expr.split('.')
                if len(parts) == 2:
                    obj_name, field_name = parts
                    obj = context.get(obj_name)
                    if isinstance(obj, dict) and field_name in obj:
                        index_value = obj[field_name]
                    # Also try accessing from base variables (which includes loop context)
                    # This handles cases where loop context is added to variables dict
                    if index_value is None:
                        base_vars = self._get_base_agent_variables(context)
                        if obj_name in base_vars:
                            obj = base_vars[obj_name]
                            if isinstance(obj, dict) and field_name in obj:
                                index_value = obj[field_name]
        else:
            # Simple variable name
            index_value = context.get(index_expr)
            # Also try from base variables
            if index_value is None:
                base_vars = self._get_base_agent_variables(context)
                index_value = base_vars.get(index_expr)
        
        if index_value is None or not isinstance(index_value, int):
            self.logger.warning("Could not evaluate index expression '{}' for '{}' in agent '{}' (got: {}). Context keys: {}", index_expr, base_field, agent_id, index_value, list(context.keys())[:10])
            return None
        
        # Access list at index
        if 0 <= index_value < len(base_value):
            self.logger.debug("Found array-indexed variable '{}' in agent '{}' parsed data: {}", var_name, agent_id, base_value[index_value])
            return base_value[index_value]
        else:
            self.logger.warning("Index {} out of range for '{}' in agent '{}' (list length: {})", index_value, base_field, agent_id, len(base_value))
            return None
    
    def _get_upstream_variable(self, context: Dict[str, Any], agent_name: str, var_name: str) -> Any:
        """
        Get a variable from upstream agent output.
        Always uses parsed data for reliable extraction.
        Supports nested paths using dot notation (e.g., "rfp_data.evaluation_criteria").
        
        Args:
            context: Execution context
            agent_name: ID of the upstream agent, or "auto" to search all
            var_name: Name of the variable to extract (can be nested like "rfp_data.evaluation_criteria")
            
        Returns:
            Variable value if found, None otherwise
        """
        try:
            if agent_name == "auto":
                # 🆕 FIXED: Search through ALL upstream agents, not just direct parents
                upstream_context = context.get("upstream", {})
                
                # Search through all agents in upstream context
                for agent_id, agent_data in upstream_context.items():
                    # Skip the current agent itself
                    if agent_id == self.agent_id:
                        continue
                    
                    # Handle accumulated loop results (list of results from multiple iterations)
                    # When accumulate_results is true, upstream context contains lists instead of single dicts
                    if isinstance(agent_data, list):
                        # Get the current iteration's result (last element in the list)
                        if not agent_data:
                            continue  # Skip empty lists
                        # Use the last element (most recent iteration's result)
                        agent_data = agent_data[-1]
                        # Ensure we have a dict after extracting from list
                        if not isinstance(agent_data, dict):
                            continue  # Skip non-dict results
                    
                    # Try to get the variable from this agent's output
                    if isinstance(agent_data, dict):
                        # Try parsed data first
                        if "parsed" in agent_data:
                            parsed_data = agent_data["parsed"]
                            if isinstance(parsed_data, dict):
                                # Handle array indexing (e.g., "supplier_response_paths[supplier_loop.index]")
                                array_indexed_value = self._resolve_array_indexed_variable(parsed_data, var_name, context, agent_id)
                                if array_indexed_value is not None:
                                    return array_indexed_value
                                
                                # Try direct key first (for backward compatibility)
                                if var_name in parsed_data:
                                    self.logger.debug("Found variable '{}' in agent '{}' parsed data: {}", var_name, agent_id, parsed_data[var_name])
                                    return parsed_data[var_name]
                                # Try nested path
                                nested_value = self._get_nested_value(parsed_data, var_name)
                                if nested_value is not None:
                                    self.logger.debug("Found nested variable '{}' in agent '{}' parsed data", var_name, agent_id)
                                    return nested_value
                        
                        # Try raw data with JSON parsing
                        if "result" in agent_data:
                            result = JSONUtils.extract_variable_from_output(agent_data["result"], var_name)
                            if result is not None:
                                self.logger.debug("Found variable '{}' in agent '{}' raw data: {}", var_name, agent_id, result)
                                return result
                
                self.logger.warning("Variable '{}' not found in any upstream agent", var_name)
                return None
            else:
                # Get from specific upstream agent
                # The upstream context structure is: context["upstream"][agent_name]
                upstream_context = context.get("upstream", {})
                parent_output = upstream_context.get(agent_name, {})
                
                # CRITICAL: If agent_name not found in upstream, check top-level context for alias
                # This handles enhanced repeat patterns where instance results are stored under instance IDs
                # (e.g., enhanced_math_repeater_file_reader_0) but accessed via base agent ID alias
                # (e.g., enhanced_math_repeater_file_reader) in top-level context
                if not parent_output and agent_name in context:
                    # Check if this is an alias (dict with parsed output structure)
                    alias_data = context[agent_name]
                    if isinstance(alias_data, dict):
                        # This is likely an alias - use it as the parent output
                        parent_output = {"parsed": alias_data}
                        self.logger.debug(
                            "Using agent ID alias '{}' from top-level context (for enhanced repeat pattern)",
                            agent_name
                        )
                
                if not parent_output:
                    self.logger.warning("Upstream agent '{}' not found in context or upstream", agent_name)
                    return None
                
                # Handle accumulated loop results (list of results from multiple iterations)
                # When accumulate_results is true, upstream context contains lists instead of single dicts
                if isinstance(parent_output, list):
                    # Get the current iteration's result (last element in the list)
                    # During loop execution, the list contains results from previous iterations
                    # For the current iteration, we want the most recent result
                    if not parent_output:
                        self.logger.warning("Upstream agent '{}' has empty accumulated results", agent_name)
                        return None
                    # Use the last element (most recent iteration's result)
                    parent_output = parent_output[-1]
                    # Ensure we have a dict after extracting from list
                    if not isinstance(parent_output, dict):
                        self.logger.warning("Upstream agent '{}' accumulated result is not a dict: {}", agent_name, type(parent_output))
                        return None
                
                # Try parsed data first (preferred - structured output)
                if isinstance(parent_output, dict) and "parsed" in parent_output:
                    parsed_data = parent_output["parsed"]
                    if isinstance(parsed_data, dict):
                        # Handle array indexing (e.g., "supplier_response_paths[supplier_loop.index]")
                        array_indexed_value = self._resolve_array_indexed_variable(parsed_data, var_name, context, agent_name)
                        if array_indexed_value is not None:
                            return array_indexed_value
                        
                        # Try direct key first (for backward compatibility)
                        if var_name in parsed_data:
                            self.logger.debug("Found variable '{}' in agent '{}' parsed data: {}", var_name, agent_name, parsed_data[var_name])
                            return parsed_data[var_name]
                        # Try nested path
                        nested_value = self._get_nested_value(parsed_data, var_name)
                        if nested_value is not None:
                            self.logger.debug("Found nested variable '{}' in agent '{}' parsed data", var_name, agent_name)
                            return nested_value
                
                # Fallback to raw data with JSON parsing
                if isinstance(parent_output, dict) and "result" in parent_output:
                    result = JSONUtils.extract_variable_from_output(parent_output["result"], var_name)
                    if result is not None:
                        self.logger.debug("Found variable '{}' in agent '{}' raw data: {}", var_name, agent_name, result)
                        return result
                
                self.logger.warning("Variable '{}' not found in upstream agent '{}'", var_name, agent_name)
                return None
                
        except Exception as e:
            self.logger.error("Error getting upstream variable {} from {}: {}", var_name, agent_name, e)
            return None
    
    def _get_variable_from_context(self, context: Dict[str, Any], var_name: str) -> Any:
        """
        Get a variable from context with fallback logic.
        First checks main context (for standalone agents), then upstream context (for pipeline agents).
        Now supports agent_id.variable_name format.
        
        Args:
            context: Execution context
            var_name: Name of the variable to extract (can be 'variable_name' or 'agent_id.variable_name')
            
        Returns:
            Variable value if found, None otherwise
        """
        try:
            # Handle prefixed variables (agent_id.variable_name)
            if '.' in var_name:
                parts = var_name.split('.', 1)  # Split only on first '.'
                agent_id = parts[0]
                field_name = parts[1]
                
                # Try to get from specific upstream agent
                upstream_value = self._get_upstream_variable(context, agent_id, field_name)
                if upstream_value is not None:
                    return upstream_value
                
                # Fallback: try as simple variable (backward compatibility)
                # This handles cases where someone uses "context.something" format
                if var_name in context:
                    return context[var_name]
                
                return None
            
            # Original logic for simple variables (backward compatible)
            # First, check main context (for standalone agents with additional_context)
            if var_name in context:
                value = context[var_name]
                return value
            
            # Check HITL results if available (these are added by _get_base_agent_variables)
            hitl_results = context.get("hitl_results", {})
            if var_name in hitl_results:
                value = hitl_results[var_name]
                self.logger.info("Found HITL variable '{}' = '{}' (type: {})", var_name, value, type(value))
                return value
            else:
                self.logger.debug("HITL variable '{}' not found in hitl_results: {}", var_name, list(hitl_results.keys()))
            
            # Fallback to upstream context (for pipeline agents) - search for field name
            upstream_value = self._get_upstream_variable(context, 'auto', var_name)
            if upstream_value is not None:
                return upstream_value

            return None
            
        except Exception as e:
            self.logger.error("Error getting variable {} from context: {}", var_name, e)
            return None
    
    def _resolve_input_variable(self, context: Dict[str, Any], var_spec: str) -> Any:
        """
        Resolve input variable that may be:
        - Simple: 'variable_name'
        - Prefixed: 'agent_id.variable_name'
        - Expression: 'agent_id.field if condition else default'
        - Array-indexed: 'agent_id.array[index]' or 'agent_id.array[loop_context.index]'
        
        Uses existing ExpressionEvaluator class (no duplication).
        For array-indexed variables, uses custom resolver.
        
        Args:
            context: Execution context
            var_spec: Variable specification (simple name, prefixed, expression, or array-indexed)
        
        Returns:
            Resolved variable value
        """
        try:
            # Check if this is an array-indexed variable (e.g., supplier_response_paths[supplier_loop.index])
            if '[' in var_spec and ']' in var_spec and '.' in var_spec:
                # Try to resolve as array-indexed variable first
                # Format: agent_id.field[index_expr]
                bracket_start = var_spec.find('[')
                bracket_end = var_spec.find(']')
                if bracket_start < bracket_end:
                    base_path = var_spec[:bracket_start]
                    index_expr = var_spec[bracket_start + 1:bracket_end]
                    
                    # Get the base array
                    base_value = self._get_variable_from_context(context, base_path)
                    if base_value is not None and isinstance(base_value, list):
                        # Resolve the index expression
                        index_value = None
                        if '.' in index_expr:
                            # Nested path like "supplier_loop.index"
                            index_value = self._get_nested_value(context, index_expr)
                            if index_value is None:
                                # Try accessing through variables (for loop context)
                                parts = index_expr.split('.')
                                if len(parts) == 2:
                                    obj_name, field_name = parts
                                    obj = context.get(obj_name)
                                    if isinstance(obj, dict) and field_name in obj:
                                        index_value = obj[field_name]
                                    # Also try from base variables
                                    if index_value is None:
                                        base_vars = self._get_base_agent_variables(context)
                                        if obj_name in base_vars:
                                            obj = base_vars[obj_name]
                                            if isinstance(obj, dict) and field_name in obj:
                                                index_value = obj[field_name]
                        else:
                            # Simple variable name
                            index_value = context.get(index_expr)
                            if index_value is None:
                                base_vars = self._get_base_agent_variables(context)
                                index_value = base_vars.get(index_expr)
                        
                        if index_value is not None and isinstance(index_value, int):
                            if 0 <= index_value < len(base_value):
                                self.logger.debug("Resolved array-indexed variable '{}' = {}", var_spec, base_value[index_value])
                                return base_value[index_value]
                            else:
                                self.logger.warning("Index {} out of range for array '{}' (length: {})", index_value, base_path, len(base_value))
                        else:
                            self.logger.warning("Could not resolve index expression '{}' for '{}' (got: {})", index_expr, var_spec, index_value)
            
            # Try to evaluate as expression first (ExpressionEvaluator will raise ValueError if invalid)
            from topaz_agent_kit.utils.expression_evaluator import evaluate_expression_value
            return evaluate_expression_value(var_spec, context)
        except ValueError:
            # Not an expression or expression evaluation failed - fall back to variable resolution
            return self._get_variable_from_context(context, var_spec)
        except Exception as e:
            self.logger.warning("Error resolving input variable '{}': {}", var_spec, e)
            return None
    
    def _expand_loop_variable(self, context: Dict[str, Any], list_var_name: str, loop_var_name: str) -> Dict[str, Any]:
        """
        Expand a loop variable to show values for each iteration in the INPUTS tab.
        
        This method is called at RUNTIME (not code generation time) to dynamically expand
        loop variables based on the actual list length. The iteration count is only known
        at runtime when the upstream agent results are available.
        
        For a loop like {% for eval_result in requirements_evaluator_list %}, this method:
        1. Gets the list variable from context (e.g., "rfp_rsp_eval_requirements_evaluator")
        2. Expands it dynamically to show loop_var[0], loop_var[1], etc. for each iteration
        3. The number of iterations is determined by the actual list length at runtime
        
        For a loop like {% for instance_id, solver_data in math_repeater_solver_instances.items() %}, this method:
        1. Gets the dictionary variable from context (e.g., "math_repeater_solver_instances")
        2. Expands the VALUE variable (solver_data) to show solver_data[0], solver_data[1], etc.
        3. The values are extracted from the dictionary in order
        
        Example (list):
            If rfp_rsp_eval_requirements_evaluator = [result1, result2] at runtime,
            this returns: {"eval_result[0]": result1, "eval_result[1]": result2}
        
        Example (dictionary):
            If math_repeater_solver_instances = {"solver_0": data1, "solver_1": data2} at runtime,
            this returns: {"solver_data[0]": data1, "solver_data[1]": data2}
        
        Args:
            context: Execution context (contains upstream agent results)
            list_var_name: Name of the list/dict variable (e.g., "rfp_rsp_eval_requirements_evaluator" or "math_repeater_solver_instances")
                          This is the actual upstream agent variable, not the Jinja2 local variable
            loop_var_name: Name of the loop variable (e.g., "eval_result" or "solver_data")
            
        Returns:
            Dictionary with keys like "loop_var[0]", "loop_var[1]", etc., mapping to each iteration's value
            The number of keys depends on the actual list/dict length at runtime
        """
        try:
            # Get the list/dict variable from context at RUNTIME
            # The length is only known at runtime when upstream agents have executed
            # First try from variables dict (which includes upstream agent data)
            base_vars = self._get_base_agent_variables(context)
            list_value = base_vars.get(list_var_name)
            
            # If not found, try getting it directly from context
            if list_value is None:
                list_value = self._get_variable_from_context(context, list_var_name)
            
            # Also check context directly for _instances dictionaries (for remote agents)
            if list_value is None and list_var_name in context:
                list_value = context[list_var_name]
            
            if list_value is None:
                self.logger.warning(
                    "List/dict variable '{}' not found for loop variable '{}'. Available keys in base_vars: {}, context keys: {}",
                    list_var_name,
                    loop_var_name,
                    sorted(base_vars.keys()),
                    sorted(context.keys()) if isinstance(context, dict) else "N/A"
                )
                return {}
            
            # Handle dictionaries (for .items() patterns)
            if isinstance(list_value, dict):
                # Extract values from dictionary in order
                # For .items() patterns, we expand the VALUE variable (e.g., solver_data)
                # The values are extracted in the order they appear in the dictionary
                dict_values = list(list_value.values())
                expanded = {}
                for index, item in enumerate(dict_values):
                    key = f"{loop_var_name}[{index}]"
                    expanded[key] = item
                self.logger.debug("Expanded loop variable '{}' from dict '{}': {} iterations (runtime expansion)", loop_var_name, list_var_name, len(expanded))
                return expanded
            
            # Handle lists (for regular loops)
            # Ensure it's a list
            if not isinstance(list_value, list):
                # If it's a single item, wrap it in a list
                list_value = [list_value]
            
            # Expand dynamically based on actual list length at runtime
            # This is where the iteration count is determined - it's not known at code generation time
            expanded = {}
            for index, item in enumerate(list_value):
                key = f"{loop_var_name}[{index}]"
                expanded[key] = item
            
            self.logger.debug("Expanded loop variable '{}' from list '{}': {} iterations (runtime expansion)", loop_var_name, list_var_name, len(expanded))
            return expanded
            
        except Exception as e:
            self.logger.error("Error expanding loop variable '{}' from '{}': {}", loop_var_name, list_var_name, e)
            return {}
    
    def _validate_mcp_servers(self) -> List[Dict[str, Any]]:
        """
        Validate MCP server configurations from self.agent_config.
        Returns list of valid servers or empty list if validation fails.
        """
        try:
            mcp_config = self.agent_config.get("mcp", {})
            
            # NEW: MCP is enabled by presence of config, not enabled flag
            if not mcp_config:
                self.logger.info("No MCP configuration found, skipping MCP tools initialization")
                return []
            
            servers = mcp_config.get("servers", [])
            if not servers:
                self.logger.warning("MCP config present but no servers configured, skipping MCP tools initialization")
                return []
            
            # Validate each server configuration
            valid_servers = []
            for i, server in enumerate(servers):
                server_url = server.get("url")
                toolkits = server.get("toolkits", [])
                tools = server.get("tools", [])
                
                if not server_url:
                    self.logger.warning(f"Server {i+1} missing URL, skipping")
                    continue
                    
                if not toolkits:
                    self.logger.warning(f"Server {i+1} ({server_url}) missing toolkits, skipping")
                    continue
                    
                if not tools:
                    self.logger.warning(f"Server {i+1} ({server_url}) missing tools, skipping")
                    continue
                
                valid_servers.append(server)
                self.logger.debug(f"Server {i+1} validated: {server_url} with {len(toolkits)} toolkits, {len(tools)} tools")
            
            if not valid_servers:
                self.logger.error("No valid MCP server configurations found, skipping MCP tools initialization")
                return []
            
            return valid_servers
            
        except Exception as e:
            self.logger.error("Error validating MCP servers: {}", e)
            return []
    
    async def _initialize_mcp_tools(self, context: Dict[str, Any]) -> None:
        """Common MCP tools initialization logic"""
        try:
            valid_servers = self._validate_mcp_servers()
            if not valid_servers:
                self.tools = []
                self._original_mcp_tools = []
                return
            
            # Create MCP tools for all valid servers
            all_tools = []
            for server in valid_servers:
                server_url = server["url"]
                self.logger.info(f"Creating MCP tools for server: {server_url}")
                
                server_tools = await FrameworkMCPManager.create_framework_mcp_tools(
                    framework=self.framework_type,  # Use self.framework_type
                    mcp_url=server_url
                )
                await FrameworkMCPManager.connect_framework_mcp_tools(server_tools)
                all_tools.extend(server_tools)
            
            self.tools = all_tools
            # Store original tools before filtering for cleanup
            self._original_mcp_tools = all_tools.copy()
            self.logger.debug(f"Created {len(self.tools)} MCP tools from {len(valid_servers)} servers")
            
            # Framework-specific filtering
            await self._filter_mcp_tools()
            
            # Framework-specific tool detail logging
            await self._log_tool_details()
            
        except Exception as e:
            self.logger.error("Failed to initialize MCP tools: {}", e)
            self.tools = []
            self._original_mcp_tools = []
    
    def _validate_variables(self, variables: Dict[str, Any]) -> None:
        """Simple validation to catch unknown variables that require user input"""
        for key, value in variables.items():
            if value == "VARIABLE_REQUIRES_USER_INPUT":
                raise AgentError(
                    f"Variable '{key}' requires user input. "
                    "Please check the generated code for required fixes. "
                    "This variable was detected by Prompt Variables Intelligence Engine but its value source is unclear."
                )
    
    def _get_input_template(self) -> Optional[str]:
        """Get input template based on framework type"""
        if self.framework_type == "crewai":
            # CrewAI uses task.description
            if hasattr(self, 'task_description') and self.task_description:
                return self.task_description
            else:
                # Fallback: try loading from prompt spec
                task_spec = self._prompt_spec.get("task")
                if task_spec:
                    return self._prompt_loader.load_prompt(spec=task_spec.get("description"))
                return None
        else:
            # Other frameworks use prompt["inputs"]
            if isinstance(self.prompt, dict) and "inputs" in self.prompt:
                return self.prompt["inputs"]
            return None

    def _render_prompt_with_variables(self, prompt_template: str, variables: Dict[str, Any]) -> str:
        """Render prompt template with variables using the PromptLoader class"""
        try:
            # Use the PromptLoader class for rendering
            rendered = self._prompt_loader.render_prompt(prompt_template, variables=variables)
            
            # Store rendered inputs for UI display
            self._captured_rendered_inputs = rendered
            
            return rendered
        except Exception as e:
            self.logger.error("Failed to render prompt template: {}", e)
            raise AgentError(f"Failed to render prompt template: {e}")
    
    def _should_process_files(self, prompt_key: str = "inputs") -> bool:
        """
        Check if the agent's prompt template uses the user_files variable.
        This helps avoid unnecessary file processing when agents don't need files.
        
        Args:
            prompt_key: The key in self.prompt to check (default: "inputs", but CrewAI uses "task")
            
        Returns:
            bool: True if the prompt uses {{user_files}}, False otherwise
        """
        prompt_section = self.prompt.get(prompt_key, {})
        prompt_template = ""
        
        if isinstance(prompt_section, dict):
            prompt_template = prompt_section.get("inline", "") or prompt_section.get("file", "") or prompt_section.get("jinja", "")
        elif isinstance(prompt_section, str):
            prompt_template = prompt_section
        
        # Check for both {{user_files}} and {{ user_files }} (with/without spaces)
        uses_user_files = "{{user_files}}" in prompt_template or "{{ user_files }}" in prompt_template
        
        if not uses_user_files:
            self.logger.debug("Agent prompt doesn't use user_files variable - will skip file processing")
        
        return uses_user_files
    
    
    async def cleanup(self) -> None:
        """cleanup method - cleanup resources and close connections"""
        try:
            self.agent = None
            # Always cleanup original tools (before filtering) to ensure all created tools are cleaned up
            tools_to_cleanup = getattr(self, '_original_mcp_tools', None) or getattr(self, 'tools', []) or []
            await FrameworkMCPManager.cleanup_framework_mcp_tools(tools_to_cleanup)
            self.logger.success("Cleaned up MCP tools")
        except Exception as e:
            self.logger.warning("Cleanup failed: {}", e)
    
    
    def _initialize_llm(self, context: Dict[str, Any]) -> None:
        """
        Initialize LLM using unified framework-aware factory.
        Reads model configuration from pipeline.yml via agent_config.
        """
        try:
            # Get model type from agent_config (pipeline.yml)
            model_type = self.agent_config.get("model")
            if not model_type:
                self.logger.error(f"Agent {self.agent_id} missing 'model' configuration in pipeline.yml")
                raise AgentError(f"Agent {self.agent_id} missing 'model' configuration in pipeline.yml")
            
            # Get configuration from unified config manager
            config_manager = FrameworkConfigManager()
            model_config = config_manager.get_model_config(
                model_type=model_type,
                framework=self.framework_type  # agno, langgraph, crewai, adk, sk, oak
            )
            
            # Create model using framework-aware factory
            self.llm = FrameworkModelFactory.get_model(
                model_type=model_type,
                framework=self.framework_type,
                **model_config
            )
            
            self.logger.success("Initialized {} {} model using unified factory", 
                            self.framework_type.title(), model_type)
            
        except Exception as e:
            self.logger.error("Failed to initialize LLM: {}", e)
            raise
    
    
    def _get_base_agent_variables(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get base variables for all agents.
        Only provides truly system-level variables that are framework-provided.
        All user input and upstream variables should be handled by generated classes.
        
        Args:
            context: Execution context
            
        Returns:
            Dictionary of variable names to values
        """
        variables = {
            # Only system-level variables that are always available
            "context": context,
            "pipeline_data": context.get("pipeline_data", {}),
        }
        
        # Add project_dir if available in context (for path resolution in prompts)
        if "project_dir" in context:
            project_dir = context["project_dir"]
            # Convert Path to string for Jinja rendering
            variables["project_dir"] = str(project_dir) if project_dir else None
        
        # Add pipeline data variables
        pipeline_data = context.get("pipeline_data", {})
        for agent_id, output in pipeline_data.items():
            variables[f"{agent_id}_output"] = output
        
        # Add common context variables that are frequently used in templates
        # Only add if not already present (to avoid overwriting values from generated agents)
        if "user_text" in context and "user_text" not in variables:
            variables["user_text"] = context["user_text"]
        
        # Add upstream agent data to variables dict so Jinja2 can evaluate expressions.
        #
        # IMPORTANT BEHAVIOR:
        # - For single-run agents, upstream[agent_id] is a dict with optional "parsed" field.
        #   We expose variables[agent_id] = parsed_dict (or the raw dict if no parsed).
        # - For loop / accumulated agents, upstream[agent_id] is a list of per-iteration results,
        #   where each element is typically a dict like {"result": ..., "parsed": {...}, ...}.
        #   For Jinja2 templates (especially comparison / aggregation agents), it is far more
        #   convenient to iterate over a list of parsed dicts. So here we flatten the list to:
        #       variables[agent_id] = [parsed_dict1, parsed_dict2, ...]
        #   falling back to the raw item when no "parsed" field exists.
        #
        # NOTE:
        # - We DO NOT modify context["upstream"] itself. All pattern runners and helper logic
        #   continue to see the original upstream structure with {"result", "parsed"} wrappers.
        #   This keeps backward compatibility for any code that inspects upstream directly.
        upstream = context.get("upstream", {})
        for agent_id, agent_data in upstream.items():
            # Handle arrays (from loop accumulated results)
            if isinstance(agent_data, list):
                # Only add if not already present (to avoid overwriting)
                if agent_id in variables:
                    continue

                flattened_list = []
                for item in agent_data:
                    # Prefer parsed content when available
                    if isinstance(item, dict) and "parsed" in item and isinstance(item["parsed"], dict):
                        flattened_list.append(item["parsed"])
                    else:
                        flattened_list.append(item)

                variables[agent_id] = flattened_list

            elif isinstance(agent_data, dict):
                # Prefer parsed data if available
                if "parsed" in agent_data and isinstance(agent_data["parsed"], dict):
                    # Only add if not already present (to avoid overwriting)
                    if agent_id not in variables:
                        variables[agent_id] = agent_data["parsed"]
                # Fallback to direct agent data
                elif agent_id not in variables:
                    variables[agent_id] = agent_data
            else:
                # Unexpected type - log warning but don't add to variables
                self.logger.warning(
                    "Unexpected upstream agent data type for '{}': {} (expected dict or list)",
                    agent_id,
                    type(agent_data),
                )
        
        # CRITICAL: Check top-level context for agent ID aliases (added by SequentialRunner for enhanced repeat patterns)
        # These aliases allow subsequent agents in a sequential pattern to access instance-specific results
        # using the base agent ID (e.g., "enhanced_math_repeater_file_reader") even though results are stored
        # under instance IDs (e.g., "enhanced_math_repeater_file_reader_0") in upstream
        # We only add aliases that look like agent IDs (contain underscores) and are dicts (parsed outputs)
        for key in context.keys():
            if key in variables:
                continue  # Already added from upstream, skip
            # Check if this looks like an agent ID alias (contains underscores, is a dict, not a system variable)
            if "_" in key and isinstance(context[key], dict) and key not in {"context", "pipeline_data", "project_dir"}:
                # Check if this key is not in upstream (meaning it's an alias, not a direct upstream entry)
                if key not in upstream:
                    # This is likely an agent ID alias - add it to variables
                    variables[key] = context[key]
                    self.logger.debug(
                        "Added agent ID alias '{}' from top-level context to variables (for enhanced repeat pattern)",
                        key
                    )
        
        # Add repeat pattern instances dictionaries (e.g., math_repeater_solver_instances)
        # These are created by RepeatPatternRunner and stored in context for downstream agents
        # Pattern: {base_agent_id}_instances = {instance_id: instance_data, ...}
        for key in context.keys():
            if key in variables:
                continue  # Already added, skip
            value = context[key]
            # Check for _instances dictionaries (created by RepeatPatternRunner)
            if key.endswith("_instances") and isinstance(value, dict):
                variables[key] = value
                self.logger.debug("Added repeat pattern instances dictionary to variables: {} ({} keys)", key, len(value))
        
        # Add loop context variables (e.g., supplier_loop, loop_iteration) to variables dict
        # These are injected by LoopRunner and RepeatPatternRunner for iteration-specific access
        # Loop context can be:
        # 1. A dict with 'index' and/or 'iteration' keys (e.g., supplier_loop = {index: 0, iteration: 1})
        # 2. Individual variables ending with _index or _iteration (e.g., supplier_loop_index, supplier_loop_iteration)
        # 3. Known loop context keys (loop_iteration, repeat_instance, etc.)
        for key in context.keys():
            if key in variables:
                continue  # Already added, skip
            value = context[key]
            # Check for loop context dict (most common case)
            if isinstance(value, dict) and ("index" in value or "iteration" in value):
                variables[key] = value
            # Check for individual index/iteration variables
            elif key.endswith("_index") or key.endswith("_iteration"):
                variables[key] = value
            # Check for known loop context keys
            elif key in ["loop_iteration", "repeat_instance"]:
                variables[key] = value
        
        # Add instance-specific variables from context (for repeat pattern instances)
        # This ensures variables from input_mapping are available for both local and remote agents
        # Called here so it works even if generated code hasn't been regenerated
        self._add_instance_context_variables(variables, context)
        
        # Unwrap content wrapping from all variables before returning
        return self._unwrap_content_from_variables(variables)
    
    def _add_instance_context_variables(self, variables: Dict[str, Any], context: Dict[str, Any]) -> None:
        """
        Add instance-specific variables from context to variables dict.
        
        This method is called from generated get_agent_variables() methods to ensure
        instance-specific variables from input_mapping (injected by InstanceContextWrapper)
        are available for both local and remote agents.
        
        Examples of instance-specific variables:
        - problem_text, problem_index (from repeat pattern input_mapping)
        - supplier, supplier_id (from loop pattern input_mapping)
        
        Args:
            variables: Variables dict to add instance variables to (modified in place)
            context: Execution context containing instance-specific variables
        """
        # Skip system/internal variables (starting with _) and already-added variables
        system_vars = {"context", "pipeline_data", "project_dir", "emitter", "mcp_client", "user_text", "index"}
        upstream_agents = set(context.get("upstream", {}).keys())
        
        for key in context.keys():
            if key in variables:
                continue  # Already added, skip
            if key in system_vars:
                continue  # Skip system variables
            if key.startswith("_"):
                continue  # Skip internal variables (e.g., _base_agent_id, _instance_id_template)
            if key in upstream_agents:
                continue  # Skip upstream agent dicts (they're added separately)
            # Add any other variables from context that look like user variables
            # This ensures instance-specific variables from input_mapping are available
            value = context[key]
            # Only add simple types (str, int, float, bool, dict, list) - skip complex objects
            if isinstance(value, (str, int, float, bool, dict, list, type(None))):
                variables[key] = value
                self.logger.debug("Added instance-specific variable to variables: {} = {}", key, type(value).__name__)
    
    def _unwrap_content_from_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively unwrap content wrapping ({"content": ...}) from all variables.
        This ensures variables are clean before being used in Jinja2 templates.
        
        Args:
            variables: Dictionary of variable names to values
            
        Returns:
            Dictionary with content wrapping removed from all values
        """
        def unwrap_value(value: Any) -> Any:
            """Recursively unwrap content wrapping from a value."""
            if isinstance(value, dict):
                # Check if this is a content wrapper (only has "content" key)
                if len(value) == 1 and "content" in value:
                    content_value = value["content"]
                    # Recursively unwrap nested content wrappers
                    return unwrap_value(content_value)
                # Not a content wrapper, recursively unwrap all values in the dict
                return {k: unwrap_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                # Recursively unwrap all items in the list
                return [unwrap_value(item) for item in value]
            else:
                # Not a dict or list, return as-is
                return value
        
        # Unwrap all variables
        unwrapped_variables = {}
        for key, value in variables.items():
            # Skip system variables that shouldn't be unwrapped
            if key in ["context", "pipeline_data"]:
                unwrapped_variables[key] = value
            else:
                unwrapped_value = unwrap_value(value)
                # Only update if value changed (to avoid unnecessary logging)
                if unwrapped_value != value:
                    self.logger.debug("Unwrapped content from variable '{}'", key)
                unwrapped_variables[key] = unwrapped_value
        
        return unwrapped_variables
    
    def _filter_variables_for_inputs_tab(
        self, 
        variables: Dict[str, Any], 
        context: Dict[str, Any],
        log_prefix: str = "INPUTS FILTER"
    ) -> Dict[str, Any]:
        """
        Filter variables to only show those explicitly detected from YAML configuration.
        
        This ensures the INPUTS tab only displays variables that the user explicitly
        put in their YAML file, not system variables or upstream agent dicts.
        
        Special handling for instance-specific variables from repeat pattern input_mapping:
        - These are added via _add_instance_context_variables() and are not in _inputs_section_variables
        - They should still be shown in INPUTS tab for remote agents
        
        Args:
            variables: Full variables dict from get_agent_variables()
            context: Execution context
            log_prefix: Prefix for log messages (e.g., "INPUTS FILTER" or "INPUTS FILTER REMOTE")
            
        Returns:
            Filtered variables dict containing only YAML-explicit variables
        """
        system_vars = {"context", "pipeline_data", "project_dir"}
        upstream_agents = set(context.get("upstream", {}).keys())
        
        # Get base variables to identify what was added by generated code vs base
        base_variables = self._get_base_agent_variables(context)
        
        # Log for debugging INPUTS tab filtering
        self.logger.debug(f"[{log_prefix}] All variables keys: {sorted(variables.keys())}")
        self.logger.debug(f"[{log_prefix}] Base variables keys: {sorted(base_variables.keys())}")
        self.logger.debug(f"[{log_prefix}] Upstream agents: {sorted(upstream_agents)}")
        self.logger.debug(f"[{log_prefix}] System vars to exclude: {system_vars}")
        
        # Use _inputs_section_variables if available (set by generated agent code)
        # This is the most precise way to filter - only show variables explicitly in inputs section
        if hasattr(self, '_inputs_section_variables') and self._inputs_section_variables:
            self.logger.debug(f"[{log_prefix}] Using _inputs_section_variables for filtering: {sorted(self._inputs_section_variables)}")
            # Trust the generated code - only show variables explicitly in inputs section
            # Also include instance-specific vars (from repeat pattern input_mapping)
            # These are variables in variables dict but not in base_variables (added by _add_instance_context_variables)
            instance_specific_vars = {
                k for k in variables.keys()
                if k not in base_variables
                and k not in system_vars
                and not k.startswith("_")
                and k not in upstream_agents
                and not k.endswith("_output")
                and not k.endswith("_instances")
                and isinstance(variables.get(k), (str, int, float, bool, type(None), dict, list))
            }
            self.logger.debug(f"[{log_prefix}] Instance-specific vars detected: {sorted(instance_specific_vars)}")
            filtered_variables = {
                k: v for k, v in variables.items()
                if k in self._inputs_section_variables or k in instance_specific_vars
            }
        else:
            # ERROR: _inputs_section_variables should always be set by generated agent code
            # This indicates the agent code needs to be regenerated
            self.logger.error(
                f"[{log_prefix}] _inputs_section_variables not found for agent {self.agent_id}. "
                f"This indicates the agent code needs to be regenerated. "
                f"Run: topaz-agent-kit init --starter <starter> <project_path>"
            )
            # Return empty dict to make the issue obvious - no variables will show in INPUTS tab
            # This forces the user to regenerate the agent code
            filtered_variables = {}
        
        # Log filtered results
        self.logger.debug(f"[{log_prefix}] Filtered variables keys (will show in INPUTS tab): {sorted(filtered_variables.keys())}")
        excluded_vars = set(variables.keys()) - set(filtered_variables.keys())
        self.logger.debug(f"[{log_prefix}] Excluded variables: {sorted(excluded_vars)}")
        
        return filtered_variables

    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Agent logic.

        Args:
            context: Execution context
            
        Returns:
            Output data from the agent
        """
        if not self._initialized:
            self.logger.error(f"Agent {self.agent_id} not initialized. Call initialize() first.")
            raise AgentError(f"Agent {self.agent_id} not initialized. Call initialize() first.")

        self.logger.debug("Context keys: {}", list(context.keys()))
        
        # Get variables for prompt rendering
        variables = self.get_agent_variables(context)
        
        # Unwrap content wrapping from all variables before using them
        # This ensures variables are clean before being used in Jinja2 templates
        variables = self._unwrap_content_from_variables(variables)
        
        # Simple validation to catch unknown variables that require user input
        self._validate_variables(variables)
        
        # Get input template based on framework
        input_template = self._get_input_template()
        if not input_template:
            self.logger.warning(f"No input template found for framework {self.framework_type}")
        
        # Render inputs using framework-appropriate template
        rendered_inputs = None
        if input_template:
            rendered_inputs = self._render_prompt_with_variables(input_template, variables)
        
        # Store rendered inputs for framework-specific classes to use (avoid re-rendering)
        self._rendered_inputs = rendered_inputs
        
        # Emit step_input here (after rendering, before execution) - ONLY for local agents
        # Remote agents add agent_inputs to result, extracted and emitted in agent_runner after execution
        emitter = context.get("emitter")
        step_name = context.get("current_step_name")
        run_mode = context.get("run_mode", "local")
        if emitter and hasattr(emitter, "step_input") and step_name and run_mode == "local":
            # Filter to only show variables explicitly detected from YAML configuration
            filtered_variables = self._filter_variables_for_inputs_tab(variables, context, "INPUTS FILTER")
            
            # Send both structured variables and rendered prompt
            # Frontend can use structured data for rich display, rendered_prompt as fallback
            inputs_data = {}
            if filtered_variables:
                inputs_data["variables"] = filtered_variables
            if rendered_inputs:
                inputs_data["rendered_prompt"] = rendered_inputs
            
            # Use node_id from context (set by LocalClient with instance ID) or fallback to agent_id
            # LocalClient sets context["node_id"] = recipient (the instance ID for repeat patterns)
            # This ensures INPUTS tab data is correctly associated with the instance card
            node_id = context.get("node_id", self.agent_id)
            emitter.step_input(
                step_name=step_name,
                node_id=node_id,
                inputs=inputs_data if inputs_data else None,
            )
        
        # Execute agent (frameworks use self._rendered_inputs, no re-rendering needed)
        try:
            # Generated classes MUST implement _execute_agent with actual LLM execution
            raw_result = await self._execute_agent(context, variables)
            
            # Parse and validate the result using AgentOutputParser
            # This handles all framework-specific output formats consistently
            # Check if lenient parsing is enabled in agent config (for agents that may return incomplete/malformed JSON)
            lenient_parsing = self.agent_config.get("lenient_parsing", False)
            
            parsed_result = AgentOutputParser.parse_agent_output(
                raw_result,
                agent_label=f"{self.__class__.__name__}({self.agent_id})",
                agent_id=self.agent_id,
                lenient=lenient_parsing
            )
            
            # For remote agents, add agent_inputs to result for transport
            # Local agents emit step_input directly above (no need to add to result)
            if run_mode == "remote":
                # Use same filtering logic as local agents - only show variables explicitly from YAML
                filtered_variables = self._filter_variables_for_inputs_tab(variables, context, "INPUTS FILTER REMOTE")
                
                # Send both structured variables and rendered prompt
                agent_inputs = {}
                if filtered_variables:
                    agent_inputs["variables"] = filtered_variables
                if rendered_inputs:
                    agent_inputs["rendered_prompt"] = rendered_inputs
                
                if agent_inputs:
                    parsed_result["agent_inputs"] = agent_inputs
            
            self.logger.debug(f"Successfully parsed agent output with keys: {list(parsed_result.keys())}")
            self.logger.debug(f"Agent {self.agent_id} Output: {parsed_result}")
            
            return parsed_result
            
        except Exception as e:
            self.logger.error(f"Agent {self.agent_id} execution failed: {e}")
            raise