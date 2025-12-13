from __future__ import annotations
from typing import Any, Dict, List
import asyncio
from topaz_agent_kit.utils.json_utils import JSONUtils
from topaz_agent_kit.utils.logger import Logger
from topaz_agent_kit.utils.expression_evaluator import evaluate_expression
from topaz_agent_kit.core.exceptions import ConfigurationError

# System context variable names
REPEAT_INSTANCE_CONTEXT_KEY = "repeat_instance"  # Context key for repeat pattern instance metadata


class BaseRunner:
    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    async def run(self, context: Dict[str, Any]) -> Any:
        raise NotImplementedError


class StepRunner(BaseRunner):
    def __init__(
        self,
        node_ref: str,
        agent_runner,
        populate_upstream_context_func=None,
        output_manager=None,
    ) -> None:
        super().__init__()
        self.node_ref = node_ref  # "agent_id" (protocol suffix no longer used)
        self.agent_runner = agent_runner
        self.populate_upstream_context_func = populate_upstream_context_func
        self.output_manager = output_manager

    async def run(self, context: Dict[str, Any]) -> Any:
        # node_ref is just agent_id (protocol suffix removed)
        agent_id = self.node_ref
        # Remove protocol suffix if present (for backward compatibility during migration)
        if ':' in agent_id:
            agent_id, _ = agent_id.split(':', 1)
            agent_id = agent_id.strip()

        self.logger.debug(
            "Executing step for agent: {}", agent_id
        )

        # Emit edge_protocol event for UI (always A2A for remote, in-proc for local)
        emitter = context.get("emitter")
        if emitter and hasattr(emitter, "edge_protocol"):
            try:
                # Determine protocol based on run_mode
                edge_protocol = "a2a"  # Default to A2A for remote
                try:
                    # Get agent config to check run_mode
                    # Try context first (for regular pipelines)
                    agent_factory = context.get("agent_factory")
                    agent_config = None
                    
                    if agent_factory:
                        agent_config = agent_factory.get_agent_config(agent_id)
                    elif self.agent_runner and hasattr(self.agent_runner, "agent_bus"):
                        # Fallback: use agent_bus to get agent config (works in sub-pipelines)
                        # Extract base agent ID if this is an instance ID
                        base_agent_id = agent_id
                        if hasattr(self.agent_runner.agent_bus, "_extract_base_agent_id"):
                            try:
                                base_agent_id = self.agent_runner.agent_bus._extract_base_agent_id(agent_id, context)
                            except Exception:
                                pass
                        
                        if hasattr(self.agent_runner.agent_bus, "_get_agent_cfg"):
                            agent_config = self.agent_runner.agent_bus._get_agent_cfg(base_agent_id)
                    
                    if agent_config:
                        run_mode = agent_config.get("run_mode", "").lower()
                        if run_mode == "local":
                            edge_protocol = "in-proc"
                except Exception:
                    # If we can't check run_mode, default to A2A
                    pass

                self.logger.debug(
                    "Emitting edge_protocol event: {} -> {} ({})",
                    context.get("previous_agent", "orchestrator"),
                    agent_id,
                    edge_protocol,
                )
                emitter.edge_protocol(
                    from_agent=context.get("previous_agent", "orchestrator"),
                    to_agent=agent_id,
                    protocol=edge_protocol,
                )
            except Exception as e:
                self.logger.warning("Failed to emit edge_protocol event: {}", e)

        # Check if this is a repeat pattern instance
        instance_id = agent_id  # Default to agent_id
        base_agent_id = agent_id  # Default to agent_id
        
        # First, check if this StepRunner has instance_metadata (single-agent repeat pattern)
        # This is how nested instances (e.g., problem solvers) work - they have instance_metadata set directly
        if hasattr(self, "instance_metadata") and self.instance_metadata:
            # This is a repeat pattern instance
            instance_id = self.instance_metadata.get("instance_id", agent_id)
            base_agent_id = self.instance_metadata.get("base_agent_id", agent_id)
            self.logger.debug(
                "Repeat pattern instance detected (from StepRunner metadata): base_agent_id={}, instance_id={}",
                base_agent_id, instance_id
            )
        else:
            # Check context for instance metadata (nested sequential pattern within repeat)
            # This is how regular instances (e.g., file reader, file report generator) work
            # InstanceContextWrapper sets _instance_context_key in context
            instance_context_key = context.get("_instance_context_key")
            if instance_context_key:
                instance_ctx = context.get(instance_context_key, {})
                if isinstance(instance_ctx, dict):
                    # We're running within a repeat pattern instance (nested sequential)
                    # Construct instance_id by appending index to base agent_id
                    # InstanceContextWrapper sets "index" in the instance context
                    idx = instance_ctx.get("index")
                    if isinstance(idx, int):
                        instance_id = f"{agent_id}_{idx}"
                        base_agent_id = agent_id
                        self.logger.debug(
                            "Repeat pattern instance detected (from context): base_agent_id={}, instance_id={}, index={}, context_key={}",
                            base_agent_id, instance_id, idx, instance_context_key
                        )
                    else:
                        self.logger.warning(
                            "Instance context key '{}' found but 'index' is not an integer: {} (type: {})",
                            instance_context_key, idx, type(idx)
                        )
                else:
                    self.logger.warning(
                        "Instance context key '{}' found but value is not a dict: {} (type: {})",
                        instance_context_key, instance_ctx, type(instance_ctx)
                    )
            else:
                # Log available context keys for debugging
                context_keys = [k for k in context.keys() if k.startswith("_instance") or k.startswith("file_instance")]
                self.logger.warning(
                    "No instance context key found in context for agent '{}'. Available instance-related keys: {}",
                    agent_id, context_keys
                )
        
        # Log the final instance_id that will be used for execute_agent
        if instance_id != agent_id:
            self.logger.debug(
                "StepRunner will use instance_id='{}' (base_agent_id='{}') for execute_agent",
                instance_id, base_agent_id
            )
        
        # Use base_agent_id for config lookup, but instance_id for registration
        agent = await self.agent_runner.build_agent(base_agent_id, instance_id, context)
        self.logger.debug("Built agent: {} (instance: {})", base_agent_id, instance_id)

        self.logger.debug("Executing agent: {} (instance: {})", base_agent_id, instance_id)
        try:
            result = await self.agent_runner.execute_agent(instance_id, agent, context)
            self.logger.success("Agent {} (instance: {}) completed successfully", base_agent_id, instance_id)
        except Exception as e:
            raise

        # Normalize result before passing to upstream context (match pre-MVP6 behavior)
        normalized_result = JSONUtils.normalize_for_ui(result)

        # Track previous agent for next step's edge_protocol event
        context["previous_agent"] = instance_id

        # Populate upstream context for downstream agents (use normalized result)
        # Note: InstanceContextWrapper will redirect this to use instance_id
        if self.populate_upstream_context_func:
            self.logger.debug("Populating upstream context for agent: {}", instance_id)
            self.populate_upstream_context_func(instance_id, normalized_result, context)

        # Process intermediate output if configured
        try:
            emitter = context.get("emitter")
            if (
                self.output_manager
                and emitter
                and self.output_manager.has_intermediate_outputs()
            ):
                self.logger.debug(
                    "Processing intermediate output for agent: {}", agent_id
                )
                intermediate_result = self.output_manager.process_intermediate_output(
                    agent_id, result, emitter
                )
                if intermediate_result:
                    self.logger.info(
                        "Processed intermediate output for node: {}", agent_id
                    )
        except Exception as e:
            self.logger.warning(
                "Failed to process intermediate output for node {}: {}", agent_id, e
            )

        return result


class GateRunner(BaseRunner):
    def __init__(
        self,
        gate_ref: str,
        gate_config: Dict[str, Any],
        pipeline_runner_gate_handler_func,
        flow_control_config: Dict[str, Any],
    ) -> None:
        super().__init__()
        self.gate_ref = gate_ref
        self.gate_config = gate_config
        self.pipeline_runner_gate_handler_func = pipeline_runner_gate_handler_func
        self.flow_control_config = flow_control_config

    async def run(self, context: Dict[str, Any]) -> Any:
        """
        Execute HITL gate and handle flow control decisions.

        Returns:
            result: {"decision": "approve/continue", "data": {...}, "flow_action": "continue/retry/skip/stop"}
        """
        self.logger.debug("Executing gate: {}", self.gate_ref)
        
        try:
            # Execute gate through pipeline_runner's gate handler
            result = await self.pipeline_runner_gate_handler_func(
                context, self.gate_ref, self.gate_config, self.flow_control_config
            )

            flow_action = result.get("flow_action", "continue")
            self.logger.success(
                "Gate {} completed with flow_action: {}",
                self.gate_ref,
                flow_action,
            )
            
            return result
        except Exception as e:
            raise


class ConditionalStepRunner(BaseRunner):
    """Execute step only if condition evaluates to true."""

    def __init__(self, step_runner: BaseRunner, condition: str) -> None:
        super().__init__()
        self.step_runner = step_runner
        self.condition = condition

    async def run(self, context: Dict[str, Any]) -> Any:
        """
        Evaluate condition and execute step if true.

        Returns:
            Result from step_runner if condition true, empty dict if skipped
        """
        # Get node_id for logging
        node_id = None
        if hasattr(self.step_runner, "node_ref"):
            node_id = self.step_runner.node_ref.split(":")[0]
        elif hasattr(self.step_runner, "gate_ref"):
            node_id = self.step_runner.gate_ref
        else:
            node_id = type(self.step_runner).__name__

        try:
            # Evaluate condition
            result = evaluate_expression(self.condition, context)

            if result:
                self.logger.success(
                    "Condition true for node {}: {}", node_id, self.condition
                )
                step_result = await self.step_runner.run(context)
                
                self.logger.debug(
                    "ConditionalStepRunner for {} returned result with keys: {}",
                    node_id,
                    list(step_result.keys())
                    if isinstance(step_result, dict)
                    else "not a dict",
                )
                return step_result
            else:
                self.logger.info(
                    "Condition false, skipping node {}: {}", node_id, self.condition
                )
                
                
                return None  # Return None instead of empty dict to indicate skipped

        except Exception as e:
            # Re-raise if this is a pipeline flow control exception (stop action)
            from topaz_agent_kit.core.exceptions import PipelineStoppedByUser

            if isinstance(e, PipelineStoppedByUser):
                self.logger.info(
                    "Pipeline flow control action detected in conditional gate, re-raising"
                )
                raise

            self.logger.error(
                "Condition evaluation error for node {}: {} - Error: {}",
                node_id,
                self.condition,
                e,
            )
            
            
            return {}


class SwitchRunner(BaseRunner):
    """Execute different branches based on expression or field value."""

    def __init__(
        self,
        field_or_expression: str,
        cases: Dict[Any, BaseRunner],
        default: BaseRunner = None,
    ) -> None:
        super().__init__()
        self.field_or_expression = (
            field_or_expression  # Can be field name or expression
        )
        self.cases = cases  # Dict[value, compiled_runner]
        self.default = default

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate expression/field and execute matching case.

        Returns:
            Result from executed case branch
        """
        try:
            # Check if this is a simple field reference or an expression
            # If it contains operators, parentheses (for functions or grouping), or comparison operators, it's an expression
            # CRITICAL: Check for parentheses first as they indicate expressions
            is_expression = (
                "(" in self.field_or_expression and ")" in self.field_or_expression
            ) or any(
                op in self.field_or_expression
                for op in [
                    ">",
                    "<",
                    "==",
                    "!=",
                    ">=",
                    "<=",
                    "AND",
                    "OR",
                    "NOT",
                    "+",
                    "-",
                    "*",
                    "/",
                    "%",
                    "//",
                    "=",
                ]
            )

            self.logger.debug(
                "Switch evaluating '{}', is_expression={}",
                self.field_or_expression,
                is_expression,
            )

            if is_expression:
                # Evaluate as expression
                field_value = evaluate_expression(self.field_or_expression, context)
                self.logger.success(
                    "Switch expression evaluated: '{}' = {}",
                    self.field_or_expression,
                    field_value,
                )
            else:
                # Resolve as simple field reference
                field_value = self._resolve_field(self.field_or_expression, context)
                self.logger.success(
                    "Switch field resolved: '{}' = {}",
                    self.field_or_expression,
                    field_value,
                )

            # Find matching case - try exact match first, then with type conversion
            if field_value in self.cases:
                self.logger.info("Executing case: {}", field_value)
                runner = self.cases[field_value]
                result = await runner.run(context)
                return result

            # Try string conversion for case matching
            if str(field_value) in self.cases:
                self.logger.info("Executing case (string match): {}", str(field_value))
                runner = self.cases[str(field_value)]
                result = await runner.run(context)
                return result

            # Try numeric conversion for case matching
            if isinstance(field_value, (int, float)):
                for case_key in self.cases:
                    try:
                        if (
                            isinstance(case_key, (int, float))
                            and abs(case_key - field_value) < 0.001
                        ):
                            self.logger.info(
                                "Executing case (numeric match): {} ≈ {}",
                                case_key,
                                field_value,
                            )
                            runner = self.cases[case_key]
                            result = await runner.run(context)
                            return result
                    except (ValueError, TypeError):
                        continue

            # Try boolean conversion
            if isinstance(field_value, bool):
                # Try string keys first
                bool_key = "true" if field_value else "false"
                if bool_key in self.cases:
                    self.logger.info(
                        "Executing case (boolean->string match): {}", bool_key
                    )
                    runner = self.cases[bool_key]
                    result = await runner.run(context)
                    return result
                # Try boolean keys directly
                if field_value in self.cases:
                    self.logger.info("Executing case (boolean match): {}", field_value)
                    runner = self.cases[field_value]
                    result = await runner.run(context)
                    return result
                # Try reverse: string case keys with boolean value
                for case_key in self.cases:
                    if isinstance(case_key, bool) and case_key == field_value:
                        self.logger.info(
                            "Executing case (boolean key match): {}", case_key
                        )
                        runner = self.cases[case_key]
                        result = await runner.run(context)
                        # Extract nested pattern from step stack after execution
                        return result

            # No match found - use default or error
            if self.default:
                self.logger.warning(
                    "No case matched for value '{}', executing default", field_value
                )
                result = await self.default.run(context)
                return result
            else:
                error_msg = f"No case matched for value '{field_value}' ({type(field_value).__name__}) and no default provided"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

        except Exception as e:
            self.logger.error(
                "Switch evaluation error: '{}' - Error: {}", self.field_or_expression, e
            )
            raise

    def _resolve_field(self, field_name: str, context: Dict[str, Any]) -> Any:
        """Resolve field using same logic as expression evaluator."""
        # This should mirror the logic in expression_evaluator._resolve_variable
        # IMPORTANT: This method should NOT be called for expressions with operators/functions
        # Only use for simple field references like "agent.field"
        if "." in field_name and not any(
            op in field_name
            for op in ["(", ")", ">", "<", "=", "!", "+", "-", "*", "/"]
        ):
            parts = field_name.split(".")
            agent_id = parts[0]
            field_path = parts[1:]

            # Try upstream first
            upstream = context.get("upstream", {})
            if agent_id in upstream:
                node_data = upstream[agent_id]
                # Check if this is the parsed output structure
                if isinstance(node_data, dict) and "parsed" in node_data:
                    value = node_data["parsed"]
                else:
                    value = node_data

                for field in field_path:
                    if isinstance(value, dict) and field in value:
                        value = value[field]
                    else:
                        raise ValueError(
                            f"Field not found: {field_name} (missing {field} in path)"
                        )
                return value

            # Fallback to root context
            if agent_id in context:
                value = context[agent_id]
                for field in field_path:
                    if isinstance(value, dict) and field in value:
                        value = value[field]
                    else:
                        raise ValueError(f"Field not found: {field_name}")
                return value

            raise ValueError(f"Variable not found: {field_name}")
        else:
            # Simple variable - try root context
            if field_name in context:
                return context[field_name]
            raise ValueError(f"Variable not found: {field_name}")


class SequentialRunner(BaseRunner):
    def __init__(self, steps: List[BaseRunner]) -> None:
        super().__init__()
        self.steps = steps

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.input(
            "Starting sequential execution with {} steps", len(self.steps)
        )
        # Log step types for debugging
        self.logger.info("=" * 80)
        self.logger.info("SEQUENTIAL RUNNER - COMPILED STEPS:")
        for idx, step in enumerate(self.steps):
            step_type = type(step).__name__
            step_info = f"Step {idx + 1}: {step_type}"
            if hasattr(step, "node_ref"):
                step_info += f" (node: {step.node_ref})"
            elif step_type == "ParallelRunner" and hasattr(step, "steps"):
                step_info += f" (parallel with {len(step.steps)} sub-steps)"
                # Log sub-steps if it's a parallel runner
                for sub_idx, sub_step in enumerate(step.steps):
                    sub_type = type(sub_step).__name__
                    if hasattr(sub_step, "node_ref"):
                        step_info += f"\n    Sub-step {sub_idx + 1}: {sub_type} (node: {sub_step.node_ref})"
                    else:
                        step_info += f"\n    Sub-step {sub_idx + 1}: {sub_type}"
            elif step_type == "RepeatPatternRunner":
                if hasattr(step, "nested_pattern_config") and step.nested_pattern_config:
                    step_info += f" (enhanced repeat with nested pattern)"
                elif hasattr(step, "base_agent_id"):
                    step_info += f" (base_agent_id: {step.base_agent_id})"
            self.logger.info(step_info)
        self.logger.info("=" * 80)
        results = {}
        i = 0
        retry_counts = {}  # Track retry attempts per node
        execution_error = None

        while i < len(self.steps):
            step = self.steps[i]
            step_type = type(step).__name__
            self.logger.input("Executing sequential step {}/{}: {}", i + 1, len(self.steps), step_type)


            try:
                result = await step.run(context)
                self.logger.debug("Step {} returned result type: {}, value keys: {}", 
                    i + 1, 
                    type(result).__name__,
                    list(result.keys()) if isinstance(result, dict) else "N/A"
                )
            except Exception as e:
                execution_error = str(e)
                self.logger.error(
                    "Sequential step {}/{} failed with exception: {}",
                    i + 1, len(self.steps), e
                )
                raise  # Re-raise to stop pipeline execution

            # Check if this is a gate result with flow action
            if isinstance(result, dict) and "flow_action" in result:
                flow_action = result.get("flow_action")

                if flow_action == "retry_node":
                    retry_target = result.get("retry_target")
                    max_retries = result.get("max_retries", 3)

                    # Find the target node index
                    target_idx = None
                    for idx, s in enumerate(self.steps):
                        if hasattr(s, "node_ref") and s.node_ref.startswith(
                            retry_target
                        ):
                            target_idx = idx
                            break

                    if target_idx is not None:
                        # Check retry count
                        retry_key = f"{retry_target}_{i}"
                        retry_counts[retry_key] = retry_counts.get(retry_key, 0) + 1

                        if retry_counts[retry_key] < max_retries:
                            self.logger.info(
                                "Retrying node {} (attempt {}/{})",
                                retry_target,
                                retry_counts[retry_key] + 1,
                                max_retries,
                            )
                            i = target_idx  # Jump back to retry target
                            continue
                        else:
                            self.logger.warning(
                                "Max retries ({}) reached for node {}",
                                max_retries,
                                retry_target,
                            )
                            # Continue to next step after max retries

                elif flow_action == "skip_to_node":
                    skip_to = result.get("skip_to")
                    if isinstance(skip_to, str):
                        # Find target node
                        for idx, s in enumerate(self.steps):
                            if hasattr(s, "node_ref") and s.node_ref.startswith(
                                skip_to
                            ):
                                self.logger.info("Skipping to node {}", skip_to)
                                i = idx
                                continue
                    elif isinstance(skip_to, dict):
                        # Conditional skip based on selection
                        # (skip_to already resolved in _determine_flow_action)
                        pass

            # Store result for non-gate steps
            # CRITICAL: Check step type BEFORE checking node_ref to ensure RepeatPatternRunner is handled correctly
            if isinstance(step, RepeatPatternRunner):
                # Enhanced repeat pattern: result is a dict with instance IDs as keys (e.g., {"file_0": {...}, "file_1": {...}})
                # For enhanced repeat patterns, we need to merge the results into the parent results dict
                # The instances dictionary is already stored in context by RepeatPatternRunner
                if isinstance(result, dict):
                    # Merge the instance results into the parent results
                    results.update(result)
                    self.logger.success(
                        "Sequential step {} completed: enhanced repeat pattern with {} instances",
                        i + 1,
                        len(result)
                    )
                else:
                    results.update(result if isinstance(result, dict) else {})
                    self.logger.success("Sequential step {} completed: enhanced repeat pattern", i + 1)
                
                # CRITICAL: Log that we're continuing to next step after repeat pattern
                self.logger.info("After repeat pattern completion: i={}, len(steps)={}", i, len(self.steps))
                if i + 1 < len(self.steps):
                    next_step = self.steps[i + 1]
                    next_step_type = type(next_step).__name__
                    if hasattr(next_step, "node_ref"):
                        self.logger.info(
                            "Continuing to next sequential step {}: {} (node: {})",
                            i + 2, next_step_type, next_step.node_ref
                        )
                    else:
                        self.logger.info(
                            "Continuing to next sequential step {}: {}",
                            i + 2, next_step_type
                        )
                else:
                    self.logger.warning("No next step after repeat pattern! i={}, len(steps)={}", i, len(self.steps))
            elif hasattr(step, "node_ref"):
                agent_id = step.node_ref.split(":")[0]
                # Use upstream context to get normalized parsed output
                upstream = context.get("upstream", {})
                
                # Check if we're running within an enhanced repeat pattern instance
                # If so, look for results using instance ID (e.g., enhanced_math_repeater_file_reader_0)
                # instead of base agent ID (e.g., enhanced_math_repeater_file_reader)
                instance_context_key = context.get("_instance_context_key")
                instance_id_for_lookup = agent_id
                if instance_context_key:
                    instance_ctx = context.get(instance_context_key, {})
                    if isinstance(instance_ctx, dict):
                        idx = instance_ctx.get("index")
                        if isinstance(idx, int):
                            instance_id_for_lookup = f"{agent_id}_{idx}"
                
                # Try instance ID first (for enhanced repeat patterns), then fall back to base agent ID
                if instance_id_for_lookup in upstream and "parsed" in upstream[instance_id_for_lookup]:
                    results[agent_id] = upstream[instance_id_for_lookup]["parsed"]
                elif agent_id in upstream and "parsed" in upstream[agent_id]:
                    results[agent_id] = upstream[agent_id]["parsed"]
                else:
                    results[agent_id] = result
                
                # CRITICAL: Add base agent ID alias to instance context (not shared upstream) for subsequent agents
                # This allows subsequent agents in the sequential pattern (e.g., file_report_generator) to access
                # instance-specific results using the base agent ID (e.g., "enhanced_math_repeater_file_reader.problem_count")
                # We add it to the instance context (which is a copy) rather than the shared upstream context
                # to avoid conflicts when multiple file instances run in parallel
                if instance_id_for_lookup != agent_id and instance_id_for_lookup in upstream:
                    if "parsed" in upstream[instance_id_for_lookup]:
                        # Add alias to instance context (not shared upstream) for subsequent agents in this sequential pattern
                        if agent_id not in context:
                            context[agent_id] = upstream[instance_id_for_lookup]["parsed"]
                            self.logger.debug(
                                "Added base agent ID alias '{}' -> instance '{}' in instance context for subsequent agents",
                                agent_id, instance_id_for_lookup
                            )
                
                self.logger.success("Sequential step {} completed: {}", i + 1, agent_id)
            elif hasattr(step, "gate_ref"):
                self.logger.success(
                    "Sequential step {} completed: gate {}", i + 1, step.gate_ref
                )
            else:
                # Nested runner (e.g., ConditionalStepRunner, SwitchRunner)
                if isinstance(result, dict):
                    # Check if this is a ConditionalStepRunner that returned a dict with agent_id key
                    if isinstance(step, ConditionalStepRunner) and hasattr(
                        step.step_runner, "node_ref"
                    ):
                        agent_id = step.step_runner.node_ref.split(":")[0]
                        # Use upstream context to get normalized parsed output
                        upstream = context.get("upstream", {})
                        if agent_id in upstream and "parsed" in upstream[agent_id]:
                            results[agent_id] = upstream[agent_id]["parsed"]
                        else:
                            results[agent_id] = result
                        self.logger.success(
                            "Sequential step {} completed: conditional node {}",
                            i + 1,
                            agent_id,
                        )
                    else:
                        # Handle nested runner results
                        # Check if result has agent_id at top level (local agents)
                        agent_id = result.get("agent_id")
                        if agent_id:
                            # Store under agent_id key
                            results[agent_id] = result
                            self.logger.success(
                                "Sequential step {} completed: nested agent {}",
                                i + 1,
                                agent_id,
                            )
                        # Check if result has a "content" wrapper (from remote agents)
                        elif "content" in result and "responses" in result:
                            # This is a wrapped remote agent result - extract the content
                            wrapped_content = result["content"]
                            if isinstance(wrapped_content, dict):
                                # Check if wrapped content has agent_id to use as key
                                wrapped_agent_id = wrapped_content.get("agent_id")
                                if wrapped_agent_id:
                                    # Store under agent_id key
                                    results[wrapped_agent_id] = wrapped_content
                                    self.logger.success(
                                        "Sequential step {} completed: wrapped agent {}",
                                        i + 1,
                                        wrapped_agent_id,
                                    )
                                else:
                                    # No agent_id, merge the fields directly
                                    results.update(wrapped_content)
                                    self.logger.warning(
                                        "Sequential step {}: wrapped content has no agent_id, merging fields directly",
                                        i + 1,
                                    )
                            else:
                                # Content is not a dict, merge the whole result
                                results.update(result)
                        else:
                            # Normal nested runner result - merge as-is
                            results.update(result)

                        self.logger.success(
                            "Sequential step {} completed (nested runner)", i + 1
                        )
                elif result is None:
                    # Conditional step was skipped (returned None)
                    self.logger.info(
                        "Sequential step {} skipped (conditional node)", i + 1
                    )
                else:
                    # Unexpected result type - log and continue
                    self.logger.warning(
                        "Sequential step {} returned unexpected result type: {}",
                        i + 1,
                        type(result).__name__
                    )
                    if isinstance(result, dict):
                        results.update(result)

            i += 1
            self.logger.debug("After step {}: i={}, len(steps)={}, continuing loop", i, i, len(self.steps))

        self.logger.success(
            "Sequential execution completed with {} total results", len(results)
        )
        self.logger.debug("Sequential execution results keys: {}", list(results.keys()))
        
        return results


class ParallelRunner(BaseRunner):
    def __init__(self, steps: List[BaseRunner]) -> None:
        super().__init__()
        self.steps = steps

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        execution_error = None
        
        # MVP: wait_all + first_error via gather
        self.logger.input("Starting parallel execution with {} steps", len(self.steps))
        
        # Create a wrapper function for running steps
        async def run_step(step):
            return await step.run(context)
        
        try:
            # Run steps in parallel
            results_list = await asyncio.gather(*(run_step(s) for s in self.steps))
            self.logger.success("All parallel steps completed")
        except Exception as e:
            execution_error = str(e)
            raise
        results = {}
        for i, step in enumerate(self.steps):
            result = results_list[i]
            # Extract agent_id from step and store result
            if hasattr(step, "node_ref"):
                agent_id = step.node_ref.split(":")[0]
                results[agent_id] = result
                self.logger.success(
                    "Parallel step {} result stored: {}", i + 1, agent_id
                )
            else:
                # If step is a nested runner, merge its results
                if isinstance(result, dict):
                    results.update(result)
                    self.logger.success(
                        "Parallel step {} result merged: {} results", i + 1, len(result)
                    )
        self.logger.success(
            "Parallel execution completed with {} total results", len(results)
        )
        
        return results


class RepeatPatternRunner(BaseRunner):
    """Execute the same agent or pipeline multiple times in parallel with instance-specific inputs.
    
    This runner evaluates the instance count at runtime (supports both static integers
    and expression strings), then creates multiple agent/pipeline instances with unique IDs
    and instance-specific input mappings.
    """
    
    def __init__(
        self,
        base_agent_id: str = None,
        node_ref: str = None,
        pipeline_id: str = None,  # NEW: For pipeline repeat
        nested_pattern_config: Dict[str, Any] = None,
        instances_spec: int | str = None,
        input_mapping: Dict[str, str] = {},
        instance_id_template: str = "{{node_id}}_instance_{{index}}",
        agent_runner = None,
        compile_step_func = None,
        populate_upstream_context_func=None,
        instance_context_key: str = REPEAT_INSTANCE_CONTEXT_KEY,
        config_result = None,  # NEW: Needed for pipeline compilation
    ) -> None:
        super().__init__()
        self.base_agent_id = base_agent_id
        self.node_ref = node_ref
        self.pipeline_id = pipeline_id  # NEW: For pipeline repeat
        self.nested_pattern_config = nested_pattern_config  # NEW: For enhanced repeat pattern (sequential)
        self.instances_spec = instances_spec
        self.input_mapping = input_mapping
        self.instance_id_template = instance_id_template
        self.instance_context_key = instance_context_key  # Configurable context key
        self.agent_runner = agent_runner
        self.compile_step_func = compile_step_func
        self.populate_upstream_context_func = populate_upstream_context_func
        self.config_result = config_result  # NEW: For pipeline compilation
        self.logger = Logger("RepeatPatternRunner")
        
        # Validate configuration
        config_count = sum([
            bool(nested_pattern_config),
            bool(node_ref),
            bool(pipeline_id)
        ])
        if config_count != 1:
            raise ValueError(
                "RepeatPatternRunner requires exactly one of: 'node_ref' (single agent), "
                "'pipeline_id' (single pipeline), or 'nested_pattern_config' (enhanced repeat)"
            )
    
    def _strip_jinja2_template(self, expression: str) -> str:
        """Strip Jinja2-style {{...}} template markers from expression.
        
        Handles both {{expression}} and plain expression formats.
        """
        expression = expression.strip()
        if expression.startswith("{{") and expression.endswith("}}"):
            # Remove outer {{ and }}
            return expression[2:-2].strip()
        return expression
    
    def _evaluate_instances(self, context: Dict[str, Any]) -> int:
        """Evaluate instances count, handling both integer and expression string."""
        if isinstance(self.instances_spec, int):
            return self.instances_spec
        
        # CRITICAL: For nested repeat patterns, add upstream instance results to context with base agent ID as alias
        # This allows expressions like "enhanced_math_repeater_file_reader.problem_count" to work
        # even though results are stored under instance ID "enhanced_math_repeater_file_reader_0"
        # This must run dynamically here (not in InstanceContextWrapper) because file_reader results
        # are only available after it completes, which happens before this nested repeat pattern runs
        self._add_upstream_aliases_for_nested_repeat(context)
        
        # It's a string expression - strip Jinja2 template markers if present
        expression = self._strip_jinja2_template(self.instances_spec)
        
        # Evaluate it
        try:
            from topaz_agent_kit.utils.expression_evaluator import evaluate_expression_value
            result = evaluate_expression_value(expression, context)
            if isinstance(result, (int, float)):
                return int(result)
            raise ValueError(f"Instance count expression must evaluate to a number, got: {type(result)}")
        except Exception as e:
            self.logger.warning(
                "Failed to evaluate instances expression '{}': {}. Using default 1.",
                self.instances_spec, e
            )
            return 1  # Safe default
    
    def _add_upstream_aliases_for_nested_repeat(self, context: Dict[str, Any]) -> None:
        """Add upstream instance results to context with base agent ID as alias for nested repeat patterns.
        
        This allows expressions like "enhanced_math_repeater_file_reader.problem_count" to work
        even though results are stored under instance ID "enhanced_math_repeater_file_reader_0".
        """
        upstream = context.get("upstream", {})
        if not upstream:
            return
        
        import re
        # Get the current parent instance index (this is the index of the outer repeat pattern instance)
        # For example, if we're in file_0, parent_index is 0
        parent_index = context.get("_parent_instance_index")
        if parent_index is None:
            # Try to get it from instance context
            instance_context_key = context.get("_instance_context_key")
            if instance_context_key:
                instance_data = context.get(instance_context_key, {})
                if isinstance(instance_data, dict) and "index" in instance_data:
                    parent_index = instance_data["index"]
        
        if parent_index is None:
            return
        
        # For each upstream agent, if we have an instance result matching the parent index, add alias
        # This allows nested repeat patterns to access upstream results using base agent ID
        for upstream_agent_id, upstream_data in upstream.items():
            # Check if this is an instance ID (ends with _N)
            instance_match = re.match(r'^(.+?)_(\d+)$', upstream_agent_id)
            if instance_match:
                upstream_base_id = instance_match.group(1)
                upstream_instance_index = int(instance_match.group(2))
                
                # Only add alias if this instance matches the current parent instance index
                # and we have parsed results
                if upstream_instance_index == parent_index:
                    if "parsed" in upstream_data:
                        # Only add alias if base agent ID is not already in context (to avoid overwriting)
                        if upstream_base_id not in context:
                            context[upstream_base_id] = upstream_data["parsed"]
                            self.logger.debug(
                                "Added base agent ID alias '{}' -> instance '{}' (parent_index={}) for nested repeat pattern expression evaluation",
                                upstream_base_id, upstream_agent_id, parent_index
                            )
    
    def _substitute_index(self, template: str, index: int, base_id: str) -> str:
        """Substitute {{index}}, {{node_id}}, and {{pipeline_id}} in template string."""
        result = template.replace("{{index}}", str(index))
        result = result.replace("{index}", str(index))
        result = result.replace("{{node_id}}", base_id)
        result = result.replace("{node_id}", base_id)
        result = result.replace("{{pipeline_id}}", base_id)
        result = result.replace("{pipeline_id}", base_id)
        return result
    
    def _create_instance_runner(self, index: int, context: Dict[str, Any]) -> BaseRunner:
        """Create a runner for a specific instance with instance-specific inputs."""
        # Check if we're a nested repeat pattern (running within another repeat pattern)
        # If so, include parent instance index in instance ID to ensure uniqueness
        # The parent index is stored in context by InstanceContextWrapper when wrapping nested patterns
        parent_instance_index = context.get("_parent_instance_index")
        
        # Generate instance ID for result storage
        # For nested patterns, use a default base_agent_id if not provided
        # For pipeline repeats, use pipeline_id
        if self.pipeline_id:
            base_id_for_template = self.pipeline_id
        else:
            base_id_for_template = self.base_agent_id or "sequential"
        
        # Generate base instance ID
        instance_id = self._substitute_index(
            self.instance_id_template,
            index,
            base_id_for_template
        )
        
        # If we're a nested single-agent or single-pipeline repeat pattern (not an enhanced repeat with nested sequential),
        # and we have a parent instance index, reconstruct instance_id with parent_index first, then nested_index
        # This makes the ID structure match the display format: {base}_{parent_index}_{nested_index}
        # e.g., problem_solver_0_0 (for parent file_0, problem 0) -> problem_solver_0_0
        #      problem_solver_0_1 (for parent file_0, problem 1) -> problem_solver_0_1
        #      problem_solver_1_0 (for parent file_1, problem 0) -> problem_solver_1_0
        if parent_instance_index is not None and not self.nested_pattern_config:
            # This is a nested single-agent repeat pattern (e.g., problem solvers within files)
            # Extract base agent ID from instance_id (remove the nested index that was added by template)
            # The instance_id_template typically uses {{node_id}}_{{index}}, so we need to remove the trailing _{index}
            import re
            # Remove trailing _{index} from instance_id to get base agent ID
            base_agent_id_match = re.search(r'^(.*?)_\d+$', instance_id)
            if base_agent_id_match:
                base_agent_id = base_agent_id_match.group(1)
            else:
                # Fallback: use base_id_for_template if pattern doesn't match
                base_agent_id = base_id_for_template
            
            # Reconstruct with parent_index first, then nested_index
            instance_id = f"{base_agent_id}_{parent_instance_index}_{index}"
        
        if self.nested_pattern_config:
            # NEW: Enhanced repeat pattern - compile nested sequential pattern
            # nested_pattern_config is already a full pattern dict with type: sequential
            # Pass parent instance index to nested pattern compilation so nested repeats can include it
            parent_instance_index = context.get("index")  # Get parent instance index if available
            if parent_instance_index is not None:
                # Store parent instance index in context for nested repeat patterns
                # This allows nested repeat patterns to include parent index in their instance IDs
                nested_context = context.copy()
                nested_context["_parent_instance_index"] = parent_instance_index
                nested_context["_parent_instance_id"] = context.get(self.instance_context_key, {}).get("instance_id", f"parent_{parent_instance_index}")
            else:
                nested_context = context
            
            nested_runner = self.compile_step_func(self.nested_pattern_config)
            
            # Store instance metadata for nested pattern
            parent_instance_id = context.get(self.instance_context_key, {}).get("instance_id", f"parent_{parent_instance_index}" if parent_instance_index is not None else None)
            instance_metadata = {
                "index": index,
                "instance_id": instance_id,
                "input_mapping": self.input_mapping,
                "instance_id_template": self.instance_id_template,
                "parent_instance_index": parent_instance_index,  # Pass parent index to nested patterns
                "parent_instance_id": parent_instance_id,  # Pass parent instance ID for scoping nested instances dictionaries
            }
            
            # Wrap the nested runner to inject instance context and handle result storage
            return InstanceContextWrapper(
                nested_runner,
                index,
                instance_id,
                self.input_mapping,
                self.populate_upstream_context_func,
                instance_metadata,
                instance_context_key=self.instance_context_key
            )
        elif self.pipeline_id:
            # NEW: Single pipeline repeat pattern
            # Compile the pipeline step
            step_config = {
                "pipeline": self.pipeline_id,
                "input_mapping": self.input_mapping
            }
            step_runner = self.compile_step_func(step_config)
            
            # For pipeline repeats, we need to customize the instance_id for storage
            # Set instance_pipeline_id on the PipelineStepRunner so it uses instance_id for storage
            if hasattr(step_runner, 'pipeline_id'):
                # Store original pipeline_id and set instance_pipeline_id for this instance
                step_runner.instance_pipeline_id = instance_id  # Use instance_id for storage
            elif hasattr(step_runner, 'runner') and hasattr(step_runner.runner, 'pipeline_id'):
                # Handle wrapped runners (e.g., ConditionalStepRunner)
                step_runner.runner.instance_pipeline_id = instance_id
            
            # Store instance metadata
            if not hasattr(step_runner, "instance_metadata"):
                step_runner.instance_metadata = {}
            instance_metadata = {
                "index": index,
                "instance_id": instance_id,
                "base_pipeline_id": self.pipeline_id,
                "input_mapping": self.input_mapping,
                "instance_id_template": self.instance_id_template,
                "parent_instance_index": parent_instance_index,
            }
            step_runner.instance_metadata = instance_metadata
            
            # Wrap the step runner to inject instance context and handle result storage
            return InstanceContextWrapper(
                step_runner, 
                index, 
                instance_id, 
                self.input_mapping, 
                self.populate_upstream_context_func, 
                instance_metadata,
                instance_context_key=self.instance_context_key
            )
        else:
            # EXISTING: Single agent repeat pattern
            # IMPORTANT: Use the base agent_id for config lookup, but instance_id for result storage
            # This ensures the agent factory finds the correct config file
            # The StepRunner will be wrapped to store results with instance_id
            
            # Compile the step using the base node_ref (so config lookup works)
            step_config = {"node": self.node_ref}
            step_runner = self.compile_step_func(step_config)
            
            # Store instance metadata
            if not hasattr(step_runner, "instance_metadata"):
                step_runner.instance_metadata = {}
            instance_metadata = {
                "index": index,
                "instance_id": instance_id,
                "base_agent_id": self.base_agent_id,
                "input_mapping": self.input_mapping,
                "instance_id_template": self.instance_id_template,
                "parent_instance_index": parent_instance_index,  # Pass parent index for nested patterns
            }
            step_runner.instance_metadata = instance_metadata
            
            # Wrap the step runner to inject instance context and handle result storage
            return InstanceContextWrapper(
                step_runner, 
                index, 
                instance_id, 
                self.input_mapping, 
                self.populate_upstream_context_func, 
                instance_metadata,
                instance_context_key=self.instance_context_key
            )
    
    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multiple instances of the same agent or nested sequential pattern in parallel."""
        # Evaluate instance count
        num_instances = self._evaluate_instances(context)
        
        # Use appropriate description based on pattern type
        if self.nested_pattern_config:
            pattern_desc = "nested sequential pattern"
        elif self.pipeline_id:
            pattern_desc = f"pipeline {self.pipeline_id}"
        else:
            pattern_desc = f"agent {self.base_agent_id}"
        self.logger.input(
            "Starting repeat pattern execution with {} instances of {}",
            num_instances, pattern_desc
        )
        
        if num_instances < 1:
            self.logger.warning("Instance count is less than 1, skipping execution")
            return {}
        
        # Create runners for each instance first
        instance_runners = []
        for i in range(num_instances):
            runner = self._create_instance_runner(i, context)
            instance_runners.append(runner)
        
        # Execute all instances in parallel
        # Use return_exceptions=True to prevent premature cancellation when one instance fails
        # This ensures all instances complete before returning, preventing premature cleanup
        self.logger.info("Executing {} instances in parallel", num_instances)
        execution_error = None
        
        # Create a wrapper function for running instances
        async def run_instance(runner):
            instance_id = runner.instance_metadata.get("instance_id", "unknown")
            self.logger.info("Running repeat instance {}", instance_id)
            return await runner.run(context)
        
        try:
            results_list = await asyncio.gather(
                *(run_instance(r) for r in instance_runners),
                return_exceptions=True  # Don't cancel remaining tasks on first exception
            )
        except Exception as e:
            execution_error = str(e)
            raise
        
        # Aggregate results with instance IDs
        # Handle both successful results and exceptions
        results = {}
        for i, (runner, result) in enumerate(zip(instance_runners, results_list)):
            instance_id = runner.instance_metadata["instance_id"]
            
            if isinstance(result, Exception):
                # Handle exception - log and store error result
                self.logger.error(
                    "Instance {} (index {}) failed: {}", 
                    instance_id, 
                    i, 
                    result
                )
                results[instance_id] = {
                    "error": str(result),
                    "instance_id": instance_id,
                    "index": i,
                    "exception_type": type(result).__name__
                }
            else:
                # Success case
                results[instance_id] = result
                self.logger.success(
                    "Instance {} (index {}) completed: {}", instance_id, i, type(result).__name__
                )
        
        # Check if any instances failed (exceptions OR error dictionaries)
        exception_count = sum(1 for r in results_list if isinstance(r, Exception))
        error_results = [
            (instance_id, result) 
            for instance_id, result in results.items() 
            if isinstance(result, dict) and result.get("error")
        ]
        
        # Also check upstream context for errors (parsed_content may contain errors)
        upstream = context.get("upstream", {})
        for instance_id in results.keys():
            if instance_id in upstream:
                upstream_data = upstream[instance_id]
                if isinstance(upstream_data, dict):
                    parsed = upstream_data.get("parsed", {})
                    if isinstance(parsed, dict) and parsed.get("error"):
                        # Add to error_results if not already there
                        if not any(instance_id == eid for eid, _ in error_results):
                            error_results.append((instance_id, parsed))
                            self.logger.error(
                                "Instance {} has error in upstream context: {}",
                                instance_id,
                                parsed.get("error", "Unknown error")
                            )
        
        failed_count = exception_count + len(error_results)
        
        if failed_count > 0:
            # Log all failures
            if error_results:
                for instance_id, error_result in error_results:
                    error_msg = error_result.get("error", "Unknown error")
                    self.logger.error(
                        "Instance {} failed with error: {}",
                        instance_id,
                        error_msg
                    )
            
            # Check for exceptions
            exception_results = [
                (instance_id, result) 
                for instance_id, result in zip(
                    [r.instance_metadata["instance_id"] for r in instance_runners],
                    results_list
                )
                if isinstance(result, Exception)
            ]
            
            if exception_results:
                for instance_id, exception in exception_results:
                    self.logger.error(
                        "Instance {} raised exception: {}",
                        instance_id,
                        str(exception)
                    )
            
            # Raise exception to stop pipeline immediately
            failed_instance_ids = []
            error_messages = []
            
            if error_results:
                failed_instance_ids.extend([instance_id for instance_id, _ in error_results])
                error_messages.extend([r.get("error", "Unknown error") for _, r in error_results])
            
            if exception_results:
                failed_instance_ids.extend([instance_id for instance_id, _ in exception_results])
                error_messages.extend([str(e) for _, e in exception_results])
            
            # Remove duplicates
            failed_instance_ids = list(dict.fromkeys(failed_instance_ids))
            
            raise RuntimeError(
                f"Repeat pattern execution failed: {failed_count} instance(s) failed out of {num_instances} total. "
                f"Failed instances: {', '.join(failed_instance_ids)}. "
                f"Errors: {'; '.join(error_messages[:3])}"  # Show first 3 errors
            )
        else:
            self.logger.success(
                "Repeat pattern execution completed with {} instances", num_instances
            )
        
        # Store aggregated results in context for downstream agents to access
        # Create {base_agent_id}_instances dictionary with all instance results
        # This allows downstream agents to iterate over instances using:
        # {% for instance_id, instance_data in base_agent_id_instances.items() %}
        # For enhanced repeat patterns (nested sequential), use the last agent in the sequence
        # as the base agent ID for the instances key (e.g., file_report_generator_instances)
        # For pipeline repeats, use the pipeline_id (e.g., math_repeater_instances)
        if self.pipeline_id:
            # Pipeline repeat: use pipeline_id as base for instances key
            base_id_for_key = self.pipeline_id
        elif self.nested_pattern_config and not self.base_agent_id:
            # Enhanced repeat pattern: extract the last agent ID from the nested sequential pattern
            steps = self.nested_pattern_config.get("steps", [])
            if steps:
                # Get the last step (which should be the file report generator)
                last_step = steps[-1]
                if isinstance(last_step, dict) and "node" in last_step:
                    # Extract agent ID from node reference (format: "agent_id" or "agent_id:config_file")
                    node_ref = last_step["node"]
                    base_id_for_key = node_ref.split(":")[0] if ":" in node_ref else node_ref
                else:
                    # Fallback to "sequential" if we can't extract agent ID
                    base_id_for_key = "sequential"
            else:
                base_id_for_key = "sequential"
        else:
            base_id_for_key = self.base_agent_id or "sequential"
        
        # Check if we're running within an outer repeat pattern instance (e.g., nested repeat within enhanced repeat)
        # If so, scope the instances key to the parent instance to avoid overwrites
        # For example: enhanced_math_repeater_problem_solver_instances_file_0
        parent_instance_id = context.get("_parent_instance_id")
        if parent_instance_id and not self.nested_pattern_config:
            # This is a nested single-agent repeat pattern (e.g., problem solvers within files)
            # Scope the instances key to the parent instance to avoid overwrites across parallel parent instances
            instances_key = f"{base_id_for_key}_instances_{parent_instance_id}"
        else:
            instances_key = f"{base_id_for_key}_instances"
        
        if "upstream" not in context:
            context["upstream"] = {}
        
        # Build instances dictionary from upstream context (which has parsed results)
        instances_dict = {}
        upstream = context.get("upstream", {})
        for instance_id in results.keys():
            if instance_id in upstream:
                # For pipeline repeats, upstream[instance_id] has the full pipeline structure:
                # {result, parsed, nodes: {...}, intermediate: {...}}
                # We should use the full structure so downstream agents can access nodes
                if self.pipeline_id:
                    # Pipeline repeat: store the full pipeline output structure
                    instance_data = upstream[instance_id]
                    instances_dict[instance_id] = instance_data
                elif self.nested_pattern_config:
                    # Enhanced repeat: result is nested structure {agent_id: result}
                    # Store the entire nested structure
                    instance_data = upstream[instance_id]
                    instances_dict[instance_id] = instance_data.get("parsed", instance_data)
                else:
                    # Single agent: get the parsed result
                    instance_data = upstream[instance_id].get("parsed", {})
                    instances_dict[instance_id] = instance_data
            else:
                # Fallback to raw result if not in upstream
                instances_dict[instance_id] = results[instance_id]
        
        # Store in context at top level for easy access in Jinja templates
        context[instances_key] = instances_dict
        
        # If we're running within an outer repeat pattern instance (e.g., nested repeat within enhanced repeat),
        # also store with the unscoped key for easier access by agents within that instance context
        # This allows the file report generator to access problem_solver_instances without needing to know the parent instance ID
        if parent_instance_id and not self.nested_pattern_config:
            unscoped_key = f"{base_id_for_key}_instances"
            context[unscoped_key] = instances_dict
            self.logger.debug(
                "Also stored instances with unscoped key: {} (for access within parent instance context)",
                unscoped_key
            )
        
        self.logger.debug(
            "Stored {} instances in context[{}] with {} keys",
            num_instances,
            instances_key,
            len(instances_dict)
        )
        
        return results


class InstanceContextWrapper(BaseRunner):
    """Wrapper that injects instance-specific context before agent execution and stores results with instance ID."""
    
    def __init__(
        self,
        wrapped_runner: BaseRunner,
        index: int,
        instance_id: str,
        input_mapping: Dict[str, str],
        populate_upstream_context_func=None,
        instance_metadata: Dict[str, Any] = None,
        instance_context_key: str = REPEAT_INSTANCE_CONTEXT_KEY,
    ) -> None:
        super().__init__()
        self.wrapped_runner = wrapped_runner
        self.index = index
        self.instance_id = instance_id
        self.input_mapping = input_mapping
        self.populate_upstream_context_func = populate_upstream_context_func
        self.instance_metadata = instance_metadata or {}
        self.instance_context_key = instance_context_key  # Configurable context key
        self.logger = Logger("InstanceContextWrapper")
    
    def _add_upstream_aliases_for_nested_repeat(self, context: Dict[str, Any]) -> None:
        """Add upstream instance results to context with base agent ID as alias for nested repeat patterns.
        
        This allows expressions like "enhanced_math_repeater_file_reader.problem_count" to work
        even though results are stored under instance ID "enhanced_math_repeater_file_reader_0".
        """
        upstream = context.get("upstream", {})
        if not upstream:
            return
        
        import re
        # Get the current parent instance index (this is the index of the outer repeat pattern instance)
        # For example, if we're in file_0, parent_index is 0
        parent_index = context.get("_parent_instance_index")
        if parent_index is None:
            # Try to get it from instance context
            instance_context_key = context.get("_instance_context_key")
            if instance_context_key:
                instance_data = context.get(instance_context_key, {})
                if isinstance(instance_data, dict) and "index" in instance_data:
                    parent_index = instance_data["index"]
        
        if parent_index is None:
            return
        
        # For each upstream agent, if we have an instance result matching the parent index, add alias
        # This allows nested repeat patterns to access upstream results using base agent ID
        for upstream_agent_id, upstream_data in upstream.items():
            # Check if this is an instance ID (ends with _N)
            instance_match = re.match(r'^(.+?)_(\d+)$', upstream_agent_id)
            if instance_match:
                upstream_base_id = instance_match.group(1)
                upstream_instance_index = int(instance_match.group(2))
                
                # Only add alias if this instance matches the current parent instance index
                # and we have parsed results
                if upstream_instance_index == parent_index:
                    if "parsed" in upstream_data:
                        # Only add alias if base agent ID is not already in context (to avoid overwriting)
                        if upstream_base_id not in context:
                            context[upstream_base_id] = upstream_data["parsed"]
                            self.logger.debug(
                                "Added base agent ID alias '{}' -> instance '{}' (parent_index={}) for nested repeat pattern expression evaluation",
                                upstream_base_id, upstream_agent_id, parent_index
                            )
    
    async def run(self, context: Dict[str, Any]) -> Any:
        """Inject instance metadata into context, then run wrapped runner."""
        # Create a copy of context to avoid mutating the original
        instance_context = context.copy()
        
        
        # Inject instance metadata using configurable context key
        if self.instance_context_key not in instance_context:
            instance_context[self.instance_context_key] = {}
        instance_context[self.instance_context_key] = {
            "index": self.index,
            "instance_id": self.instance_id,
        }
        # Also expose index at top-level for expression evaluation in input_mapping
        # (e.g., enhanced_math_repeater_folder_scanner.file_paths[index])
        # This mirrors how simple repeat patterns expose index to expressions.
        instance_context["index"] = self.index
        # Store the context key name so agent_runner can use it to find instance_id
        instance_context["_instance_context_key"] = self.instance_context_key
        
        
        # Store instance_id_template in context for dynamic base agent ID extraction
        # This allows agent_runner to reverse-engineer the base agent ID from instance ID
        instance_context["_instance_id_template"] = self.instance_metadata.get("instance_id_template")
        instance_context["_base_agent_id"] = self.instance_metadata.get("base_agent_id")
        
        # If this is a nested repeat pattern instance (e.g., file_0, file_1), store the parent instance index
        # so that nested repeat patterns (e.g., problem solvers) can include it in their instance IDs
        # The parent index is the index of the outer repeat pattern instance (e.g., file index)
        parent_instance_index = self.instance_metadata.get("parent_instance_index")
        if parent_instance_index is not None:
            instance_context["_parent_instance_index"] = parent_instance_index
        # Also check if we're running within an instance context (from outer repeat pattern)
        # If so, use that index as the parent index for nested repeat patterns
        elif self.instance_context_key in instance_context:
            instance_data = instance_context.get(self.instance_context_key, {})
            if isinstance(instance_data, dict) and "index" in instance_data:
                # We're running within an outer repeat pattern instance
                # Use the outer instance index as parent index for nested repeat patterns
                instance_context["_parent_instance_index"] = instance_data["index"]
        
        # Also store the parent instance ID if available (for scoping nested repeat pattern instances dictionaries)
        # This allows nested repeat patterns to scope their instances dictionaries to the parent instance
        # For example: enhanced_math_repeater_problem_solver_instances_file_0
        parent_instance_id = self.instance_metadata.get("parent_instance_id")
        if parent_instance_id:
            instance_context["_parent_instance_id"] = parent_instance_id
        elif self.instance_context_key in instance_context:
            instance_data = instance_context.get(self.instance_context_key, {})
            if isinstance(instance_data, dict) and "instance_id" in instance_data:
                # We're running within an outer repeat pattern instance
                # Use the outer instance ID as parent instance ID for nested repeat patterns
                instance_context["_parent_instance_id"] = instance_data["instance_id"]
        
        # CRITICAL: For nested repeat patterns, add upstream instance results to context with base agent ID as alias
        # This must run before input_mapping evaluation so expressions like "enhanced_math_repeater_file_reader.problems[index]" work
        # This runs dynamically here (not at InstanceContextWrapper start) because file_reader results are only available after it completes
        self._add_upstream_aliases_for_nested_repeat(instance_context)
        
        # Apply input_mapping to create instance-specific variables
        # These will be available in agent input templates via {{variable_name}}
        if self.input_mapping:
            for var_name, template in self.input_mapping.items():
                from topaz_agent_kit.utils.expression_evaluator import evaluate_expression_value
                
                # Strip outer Jinja2 template markers if present ({{expression}} -> expression)
                substituted = template.strip()
                if substituted.startswith("{{") and substituted.endswith("}}"):
                    substituted = substituted[2:-2].strip()
                
                # Substitute {{index}}, {index}, {{node_id}}, and {node_id} if present
                # Support both double braces (Jinja2 style) and single braces (template style)
                substituted = substituted.replace("{{index}}", str(self.index))
                substituted = substituted.replace("{index}", str(self.index))
                substituted = substituted.replace("{{node_id}}", self.instance_id)
                substituted = substituted.replace("{node_id}", self.instance_id)
                
                # For array indexing, handle [{{index}}] and [index] patterns
                # Replace [{{index}}] with actual index value
                import re
                substituted = re.sub(r'\[\{\{index\}\}\]', f'[{self.index}]', substituted)
                # Replace [index] with actual index value (for plain format: agent.field[index])
                substituted = re.sub(r'\[index\]', f'[{self.index}]', substituted)
                
                # Add index to context for expression evaluation (in case it's used as a variable)
                instance_context["index"] = self.index
                
                # Check if expression contains array indexing [N] or [index]
                # The expression evaluator tokenizer doesn't support [ and ], so we need to
                # resolve array access manually before evaluation
                array_match = re.search(r'\[(\d+)\]', substituted)
                if array_match:
                    # Extract base variable (everything before [)
                    base_var = substituted[:array_match.start()].strip()
                    index_value = int(array_match.group(1))
                    
                    # Resolve the base variable first
                    try:
                        base_value = evaluate_expression_value(base_var, instance_context)
                        if isinstance(base_value, (list, tuple)):
                            if 0 <= index_value < len(base_value):
                                value = base_value[index_value]
                                instance_context[var_name] = value
                                self.logger.debug(
                                    "Mapped input variable '{}' = {}[{}] = {} (from template: '{}')",
                                    var_name, base_var, index_value, type(value).__name__, template
                                )
                            else:
                                raise IndexError(f"Array index {index_value} out of range for {base_var} (length: {len(base_value)})")
                        else:
                            raise TypeError(f"Cannot index into {type(base_value).__name__}, expected list or tuple")
                    except Exception as e:
                        self.logger.warning(
                            "Failed to resolve array access for '{}': {}. Trying full expression evaluation.",
                            var_name, e
                        )
                        # Fallback: try evaluating the full expression (might work if tokenizer is updated)
                        try:
                            value = evaluate_expression_value(substituted, instance_context)
                            instance_context[var_name] = value
                            self.logger.debug(
                                "Mapped input variable '{}' = {} (from template: '{}')",
                                var_name, type(value).__name__, template
                            )
                        except Exception as e2:
                            self.logger.warning(
                                "Failed to evaluate input mapping for '{}': {}. Using template as-is.",
                                var_name, e2
                            )
                            # Fallback: use the substituted template as string
                            instance_context[var_name] = substituted
                else:
                    # No array indexing - evaluate normally
                    try:
                        value = evaluate_expression_value(substituted, instance_context)
                        instance_context[var_name] = value
                        self.logger.debug(
                            "Mapped input variable '{}' = {} (from template: '{}')",
                            var_name, type(value).__name__, template
                        )
                    except Exception as e:
                        self.logger.warning(
                            "Failed to evaluate input mapping for '{}': {}. Using template as-is.",
                            var_name, e
                        )
                        # Fallback: use the substituted template as string
                        instance_context[var_name] = substituted
        
        # Wrap populate_upstream_context_func to redirect to instance_id
        original_populate_func = None
        if hasattr(self.wrapped_runner, "populate_upstream_context_func"):
            original_populate_func = self.wrapped_runner.populate_upstream_context_func
        
        def instance_populate_func(agent_id, result, ctx):
            """Redirect result storage to instance_id instead of base agent_id."""
            # Store with instance_id
            if self.populate_upstream_context_func:
                self.populate_upstream_context_func(self.instance_id, result, ctx)
            # Also call original if it exists (for any other side effects)
            if original_populate_func:
                # Don't call with base agent_id to avoid duplicate storage
                pass
        
        # Temporarily replace populate function
        if hasattr(self.wrapped_runner, "populate_upstream_context_func"):
            self.wrapped_runner.populate_upstream_context_func = instance_populate_func
        
        try:
            # Execute with timeout protection (e.g., 5 minutes per instance)
            timeout_seconds = 300  # 5 minutes
            
            result = await asyncio.wait_for(
                self.wrapped_runner.run(instance_context),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            self.logger.error(
                "Instance {} (index {}) timed out after {} seconds",
                self.instance_id,
                self.index,
                timeout_seconds
            )
            # Return error result instead of hanging
            result = {
                "error": f"Instance execution timed out after {timeout_seconds} seconds",
                "instance_id": self.instance_id,
                "index": self.index
            }
        except Exception as e:
            self.logger.error(
                "Instance {} (index {}) failed: {}",
                self.instance_id,
                self.index,
                e
            )
            raise
        finally:
            # Restore original populate function
            if hasattr(self.wrapped_runner, "populate_upstream_context_func"):
                self.wrapped_runner.populate_upstream_context_func = original_populate_func
        
        return result


class LoopRunner(BaseRunner):
    def __init__(
        self, 
        body: BaseRunner, 
        max_iterations: int | str, 
        termination_condition: str | None = None,
        loop_context_key: str | None = None,
        accumulate_results: bool = True
    ) -> None:
        super().__init__()
        self.body = body
        self.max_iterations = max_iterations  # Can be int or expression string
        self.termination_condition = termination_condition
        self.loop_context_key = loop_context_key or "loop_iteration"  # Default key for loop iteration context
        self.accumulate_results = accumulate_results  # Whether to accumulate results in arrays

    def _resolve_context_value(self, path: str, context: Dict[str, Any]) -> Any:
        """Resolve a dot-separated path from context (e.g., 'agent_id.field')."""
        parts = path.split('.')
        value = context
        
        # First try to resolve from context root
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
                if value is None:
                    break
            else:
                raise TypeError(f"Cannot access '{part}' on non-dict value")
        
        # If not found in root context, try upstream context
        if value is None and len(parts) >= 2:
            upstream = context.get("upstream", {})
            agent_id = parts[0]
            if agent_id in upstream:
                agent_data = upstream[agent_id]
                # Prefer parsed data if available
                if isinstance(agent_data, dict) and "parsed" in agent_data:
                    agent_data = agent_data["parsed"]
                
                # Navigate through remaining parts
                value = agent_data
                for part in parts[1:]:
                    if isinstance(value, dict):
                        value = value.get(part)
                        if value is None:
                            raise KeyError(f"Path '{path}' not found in upstream context at '{part}'")
                    else:
                        raise TypeError(f"Cannot access '{part}' on non-dict value")
                return value
        
        if value is None:
            raise KeyError(f"Path '{path}' not found in context")
        return value
    
    def _evaluate_max_iterations(self, context: Dict[str, Any]) -> int:
        """Evaluate max_iterations, handling both integer and expression string."""
        if isinstance(self.max_iterations, int):
            return self.max_iterations
        
        # It's a string expression - evaluate it
        try:
            import re
            import math
            
            expr = str(self.max_iterations).strip()
            
            # Handle min/max functions with context variable resolution
            # Pattern: min(agent.field, number) or min(number, number)
            pattern = r'(min|max)\(([^)]+)\)'
            
            def replace_func(match):
                func_name = match.group(1)
                args_str = match.group(2)
                args = [arg.strip() for arg in args_str.split(',')]
                values = []
                
                for arg in args:
                    # Try to resolve from context (dot-separated path)
                    if '.' in arg:
                        try:
                            value = self._resolve_context_value(arg, context)
                            values.append(float(value) if isinstance(value, (int, float)) else value)
                        except (KeyError, TypeError, ValueError):
                            # If not found, try as literal
                            try:
                                values.append(int(arg))
                            except ValueError:
                                values.append(float(arg))
                    else:
                        # Try as literal number first
                        try:
                            values.append(int(arg))
                        except ValueError:
                            try:
                                values.append(float(arg))
                            except ValueError:
                                # Try to resolve from context root
                                if arg in context:
                                    value = context[arg]
                                    values.append(float(value) if isinstance(value, (int, float)) else value)
                                else:
                                    raise ValueError(f"Cannot resolve argument: {arg}")
                
                # Apply function
                func = getattr(math, func_name)
                result = func(*values)
                return str(int(result))
            
            # Replace all min/max function calls
            while re.search(pattern, expr):
                expr = re.sub(pattern, replace_func, expr)
            
            # Resolve any remaining variable references in the expression
            # Pattern: word characters and dots (e.g., "agent_id.field")
            var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z0-9_]+)+)\b'
            def replace_var(match):
                var_path = match.group(1)
                try:
                    value = self._resolve_context_value(var_path, context)
                    return str(value) if isinstance(value, (int, float)) else str(value)
                except (KeyError, TypeError, ValueError):
                    # If can't resolve, return original (might be a builtin or function)
                    return var_path
            
            # Replace variable references with their values
            expr = re.sub(var_pattern, replace_var, expr)
            
            # Evaluate final expression (should be a number now)
            result = eval(expr, {"__builtins__": {}}, {})
            return int(result)
            
        except Exception as e:
            self.logger.warning(
                "Failed to evaluate max_iterations expression '{}': {}. Using default 50.",
                self.max_iterations, e
            )
            return 50  # Safe default

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        execution_error = None
        
        # Evaluate max_iterations (handles both int and expression)
        max_iter = self._evaluate_max_iterations(context)
        
        self.logger.input(
            "Starting loop execution with max {} iterations", max_iter
        )
        results = {}
        termination_reason = None
        
        # Initialize upstream context if needed
        if "upstream" not in context:
            context["upstream"] = {}
        
        # Track which agents were in upstream before the loop starts
        # This allows us to only accumulate agents that ran INSIDE the loop, not agents from before the loop
        upstream_before_loop = set(context.get("upstream", {}).keys())
        
        for iteration in range(max_iter):
            self.logger.input(
                "Executing loop iteration {}/{}", iteration + 1, max_iter
            )
            # Inject loop iteration context for agents to access
            # CRITICAL: Create a deep copy of upstream to prevent overwriting accumulated results
            # When body.run() populates loop_context["upstream"], it should not affect context["upstream"]
            import copy
            loop_context = context.copy()
            # Deep copy the upstream dict to isolate each iteration's results
            if "upstream" in loop_context:
                loop_context["upstream"] = copy.deepcopy(loop_context["upstream"])
            # Use configurable context key (default: "loop_iteration") for structured access
            loop_context[self.loop_context_key] = {
                "index": iteration,  # 0-based index
                "iteration": iteration + 1,  # 1-based index
            }
            # Also inject index and iteration directly using the same key prefix for convenience
            # This allows both {{loop_context_key.index}} and {{loop_context_key_index}} patterns
            loop_context[f"{self.loop_context_key}_index"] = iteration  # 0-based index
            loop_context[f"{self.loop_context_key}_iteration"] = iteration + 1  # 1-based index
            
            result = await self.body.run(loop_context)
            
            # Accumulate results in arrays in upstream context if enabled
            # This allows downstream agents to access all loop iterations
            if self.accumulate_results and "upstream" in loop_context:
                for agent_id, agent_result in loop_context["upstream"].items():
                    # Only accumulate agents that ran INSIDE the loop body
                    # Skip agents that were already in upstream before the loop started (e.g., folder_scanner)
                    if agent_id in upstream_before_loop:
                        # This agent ran before the loop - don't accumulate it
                        continue
                    
                    if agent_id not in context["upstream"]:
                        # First iteration for this agent - store directly
                        context["upstream"][agent_id] = agent_result
                    else:
                        # Subsequent iteration - convert to array and append
                        existing = context["upstream"][agent_id]
                        if not isinstance(existing, list):
                            # Convert first result to array
                            context["upstream"][agent_id] = [existing]
                        # Append this iteration's result (deep copy to avoid reference issues)
                        context["upstream"][agent_id].append(copy.deepcopy(agent_result))
            elif not self.accumulate_results:
                # If accumulation is disabled, just update with latest result (overwrite)
                if "upstream" in loop_context:
                    context["upstream"].update(loop_context["upstream"])
            
            # If body is a nested runner, merge its results
            if isinstance(result, dict):
                results.update(result)
                self.logger.success(
                    "Loop iteration {} completed: {} results",
                    iteration + 1,
                    len(result),
                )
            else:
                # If body is a single step, extract agent_id and store result
                if hasattr(self.body, "node_ref"):
                    agent_id = self.body.node_ref.split(":")[0]
                    results[agent_id] = result
                    self.logger.success(
                        "Loop iteration {} completed: {}", iteration + 1, agent_id
                    )
            
            # Check termination condition (similar to group chat)
            # CRITICAL: Use loop_context (not context) to check termination condition
            # because loop_context contains the updated values from the current iteration
            # The termination condition needs to see the latest agent results (e.g., ag_email_selector.current_email_id)
            if self.termination_condition:
                try:
                    # Use loop_context which has the most up-to-date values from this iteration
                    eval_context = loop_context.copy()
                    eval_context["iteration"] = iteration + 1
                    eval_context["results"] = results
                    
                    if evaluate_expression(self.termination_condition, eval_context):
                        self.logger.info(
                            "Termination condition met: {}", self.termination_condition
                        )
                        termination_reason = "condition_met"
                        break
                except Exception as e:
                    self.logger.warning(
                        "Failed to evaluate termination condition: {}", e
                    )
        
        if not termination_reason:
            termination_reason = "max_iterations"
        
        
        self.logger.success(
            "Loop execution completed after {} iterations with {} total results (reason: {})",
            iteration + 1,
            len(results),
            termination_reason,
        )
        return results


class HandoffRunner(BaseRunner):
    """
    Handoff pattern runner - LLM-driven routing to specialist agents.

    Flow:
    1. Execute orchestrator agent (custom or generic)
    2. Parse LLM's handoff decision from response
    3. Execute chosen specialist agent
    4. Return to orchestrator for finalization

    The orchestrator is automatically built from agent descriptions
    if no custom orchestrator is provided.
    """

    def __init__(
        self,
        orchestrator_ref: str | None,
        handoffs: Dict[str, BaseRunner],
        agent_runner,
        orchestrator_model: str,
        populate_upstream_context_func=None,
        output_manager=None,
    ):
        super().__init__()
        self.orchestrator_ref = orchestrator_ref  # Optional custom orchestrator
        self.orchestrator_model = orchestrator_model  # Model for orchestrator LLM
        self.handoffs = handoffs  # Dict[agent_id, BaseRunner]
        self.agent_runner = agent_runner
        self.populate_upstream_context_func = populate_upstream_context_func
        self.output_manager = output_manager

        if not self.orchestrator_model:
            raise ConfigurationError("Orchestrator model is required")

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute handoff pattern with orchestrator and specialist agents."""
        execution_error = None

        # Step 1: Execute orchestrator
        self.logger.info("Executing orchestrator agent")
        try:
            orchestrator_result = await self._execute_orchestrator(context)
        except Exception as e:
            execution_error = str(e)
            raise

        # Step 2: Parse handoff decision
        specialist_id = self._parse_handoff_decision(orchestrator_result)

        if not specialist_id:
            # No handoff detected - orchestrator handled directly
            self.logger.info("No handoff detected, orchestrator handled directly")
            return orchestrator_result

        # Step 3: Execute specialist
        self.logger.info("Handing off to specialist: {}", specialist_id)

        if specialist_id not in self.handoffs:
            self.logger.error("Specialist {} not found in handoffs", specialist_id)
            return orchestrator_result

        # Prepare context for specialist
        specialist_context = self._prepare_specialist_context(
            context, orchestrator_result, specialist_id
        )

        # Execute specialist and track it
        specialist_runner = self.handoffs[specialist_id]
        try:
            specialist_result = await specialist_runner.run(specialist_context)
        except Exception as e:
            execution_error = str(e)
            raise

        # Step 4: Return to orchestrator for finalization
        self.logger.info("Returning to orchestrator for finalization")
        try:
            final_result = await self._return_to_orchestrator(
                context, orchestrator_result, specialist_result, specialist_id
            )
        except Exception as e:
            execution_error = str(e)
            raise

        return final_result

    async def _execute_orchestrator(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute orchestrator (custom or generic)."""

        if self.orchestrator_ref:
            # Use custom orchestrator
            self.logger.debug("Using custom orchestrator: {}", self.orchestrator_ref)
            orchestrator_runner = StepRunner(
                self.orchestrator_ref,
                self.agent_runner,
                self.populate_upstream_context_func,
                self.output_manager,
            )
            return await orchestrator_runner.run(context)
        else:
            # Build and execute generic orchestrator
            self.logger.debug("Building generic orchestrator from agent descriptions")

            # Load agent descriptions
            agent_descriptions = await self._load_agent_descriptions(
                self.handoffs, context
            )

            # Build orchestrator prompt
            orchestrator_prompt = self._build_generic_orchestrator_prompt(
                agent_descriptions
            )

            # Execute generic orchestrator
            return await self._execute_virtual_orchestrator(
                orchestrator_prompt, context
            )

    async def _load_agent_descriptions(
        self, handoffs: Dict[str, BaseRunner], context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Load descriptions for all handoff agents from ui_manifest."""
        descriptions = []
        
        # Get pipeline_id and project_dir from context
        pipeline_id = context.get("pipeline_id")
        project_dir = context.get("project_dir")
        
        # Load ui_manifest for the pipeline
        ui_manifest = {}
        if pipeline_id and project_dir:
            try:
                from pathlib import Path
                import yaml
                ui_manifest_path = Path(project_dir) / "config" / "ui_manifests" / f"{pipeline_id}.yml"
                if ui_manifest_path.exists():
                    with open(ui_manifest_path, 'r', encoding='utf-8') as f:
                        ui_manifest = yaml.safe_load(f) or {}
                    self.logger.debug("Loaded UI manifest for pipeline {}: {} agents", pipeline_id, len(ui_manifest.get("agents", [])))
                else:
                    self.logger.warning("UI manifest not found for pipeline {}: {}", pipeline_id, ui_manifest_path)
            except Exception as e:
                self.logger.warning("Failed to load UI manifest for pipeline {}: {}", pipeline_id, e)
        
        # Create a map of agent_id -> subtitle from ui_manifest
        agent_subtitle_map = {}
        agents = ui_manifest.get("agents", [])
        for agent in agents:
            agent_id = agent.get("id")
            subtitle = agent.get("subtitle")
            if agent_id and subtitle:
                agent_subtitle_map[agent_id] = subtitle

        for agent_id, runner in handoffs.items():
            try:
                # Get description from ui_manifest
                description = agent_subtitle_map.get(agent_id)
                if not description:
                    # If not found in ui_manifest, raise error (subtitle is mandatory)
                    raise ValueError(f"Agent '{agent_id}' not found in ui_manifest.agents or missing subtitle")

                descriptions.append({"id": agent_id, "description": description})
                self.logger.debug(
                    "Loaded description for {} from ui_manifest: {}", agent_id, description[:50]
                )
            except Exception as e:
                self.logger.error(
                    "Failed to load description for {}: {}", agent_id, e
                )
                # Fail fast - don't use fallback since subtitle is mandatory
                raise RuntimeError(f"Failed to load agent description for {agent_id}: {e}")

        return descriptions

    def _build_generic_orchestrator_prompt(
        self, agent_descriptions: List[Dict[str, str]]
    ) -> str:
        """Build orchestrator prompt from agent descriptions."""

        specialist_list = []
        for i, desc in enumerate(agent_descriptions, 1):
            specialist_list.append(f"{i}. {desc['id']}: {desc['description']}")

        prompt = f"""You are an intelligent routing agent. Your role is to understand user requests and route them to the most appropriate specialist.

Available Specialists:
{chr(10).join(specialist_list)}

How to Hand Off:
When a user needs a specialist, respond EXACTLY with:
HANDOFF: <specialist_id>

Example:
User: "Translate this to Spanish"
You: "HANDOFF: spanish_translator"

User: "What's 2+2?"
You: "I can help with that. The answer is 4."

Guidelines:
- Help users directly when the task doesn't require a specialist
- Hand off only when a specialist is genuinely needed
- Use EXACTLY the format: "HANDOFF: <specialist_id>"
- Include a brief explanation in your response"""

        return prompt

    async def _execute_virtual_orchestrator(
        self, orchestrator_prompt: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute virtual orchestrator agent with generated prompt."""

        # Virtual orchestrator always uses langgraph for routing decisions
        # Framework is hardcoded since orchestrator is always virtual (no config file)
        # Model comes from pattern configuration (orchestrator_model)
        model = self.orchestrator_model

        # Create virtual agent config
        virtual_agent_config = {
            "instruction": orchestrator_prompt,
            "framework": "langgraph",  # Always langgraph for virtual orchestrator
            "model": model,
        }

        # Execute virtual agent using AgentRunner (bypasses AgentFactory lookup)
        result = await self.agent_runner.execute_virtual_agent(
            agent_id="__orchestrator__",
            inline_config=virtual_agent_config,
            context=context,
        )

        return result

    def _parse_handoff_decision(
        self, orchestrator_result: Dict[str, Any]
    ) -> str | None:
        """Parse handoff decision from orchestrator response."""
        import re

        if not isinstance(orchestrator_result, dict):
            return None

        # Get the response content
        content = orchestrator_result.get("content", "")
        if not content:
            # Try agent_inputs
            agent_inputs = orchestrator_result.get("agent_inputs", {})
            if isinstance(agent_inputs, dict):
                content = agent_inputs.get("content", "")

        if not content:
            return None

        # Look for "HANDOFF: <agent_id>" pattern
        match = re.search(r"HANDOFF:\s*(\w+)", str(content), re.IGNORECASE)

        if match:
            agent_id = match.group(1)
            self.logger.info("Detected handoff to: {}", agent_id)
            return agent_id

        return None

    def _prepare_specialist_context(
        self,
        context: Dict[str, Any],
        orchestrator_result: Dict[str, Any],
        specialist_id: str,
    ) -> Dict[str, Any]:
        """Prepare context for specialist execution."""

        # Copy main context
        specialist_context = context.copy()

        # Add orchestrator result to upstream context
        specialist_context["upstream"] = specialist_context.get("upstream", {})
        specialist_context["upstream"]["__orchestrator__"] = orchestrator_result

        # Track handoff metadata
        specialist_context["_is_handoff"] = True
        specialist_context["_handoff_to"] = specialist_id

        self.logger.debug("Prepared context for specialist: {}", specialist_id)

        return specialist_context

    async def _return_to_orchestrator(
        self,
        context: Dict[str, Any],
        orchestrator_result: Dict[str, Any],
        specialist_result: Dict[str, Any],
        specialist_id: str,
    ) -> Dict[str, Any]:
        """Return to orchestrator with specialist response."""

        # Prepare return context
        return_context = context.copy()

        # Store both results in upstream
        return_context["upstream"] = return_context.get("upstream", {})
        return_context["upstream"]["__orchestrator__"] = orchestrator_result
        return_context["upstream"][specialist_id] = specialist_result

        # Get specialist response
        specialist_response = specialist_result.get("content", "")
        if not specialist_response and "agent_inputs" in specialist_result:
            specialist_response = specialist_result["agent_inputs"].get("content", "")

        # Update user_text for orchestrator
        return_context[
            "user_text"
        ] = f"""The specialist ({specialist_id}) has provided the following response:

{specialist_response}

Please provide a final, helpful closing message to the user."""

        # Track return to orchestrator
        return_context["_return_to_orchestrator"] = True
        return_context["_handoff_complete"] = True

        # Execute orchestrator again
        self.logger.info("Executing orchestrator with specialist response")
        final_result = await self._execute_orchestrator(return_context)

        return final_result


class GroupChatRunner(BaseRunner):
    """
    Group Chat pattern runner - Multiple agents collaborate in shared conversation.

    Flow:
    1. Initialize chat with user input
    2. Loop: Select speaker → Execute agent → Record message → Check termination
    3. Return full chat history and final result

    Speaker Selection:
    - round_robin: Fixed rotation through participants
    - llm: Orchestrator decides next speaker (custom or virtual)
    """

    def __init__(
        self,
        participants: Dict[str, str],  # {participant_id: participant_ref}
        participant_runners: Dict[str, BaseRunner],  # {participant_id: runner}
        selection_strategy: str,
        agent_runner,
        termination: Dict[str, Any],
        orchestrator_ref: str | None = None,
        orchestrator_model: str | None = None,
        populate_upstream_context_func=None,
        output_manager=None,
    ):
        super().__init__()
        self.participants = participants  # {participant_id: participant_ref}
        self.participant_runners = participant_runners  # {participant_id: runner}
        self.selection_strategy = selection_strategy  # "llm" or "round_robin"
        self.agent_runner = agent_runner
        self.termination = termination  # {max_rounds, condition?}
        self.orchestrator_ref = orchestrator_ref  # Optional custom orchestrator
        self.orchestrator_model = orchestrator_model  # For virtual orchestrator
        self.populate_upstream_context_func = populate_upstream_context_func
        self.output_manager = output_manager

        # Validate
        if self.selection_strategy not in ["llm", "round_robin"]:
            raise ConfigurationError(
                f"Invalid selection_strategy: {self.selection_strategy}. "
                "Must be 'llm' or 'round_robin'"
            )

        if not self.termination.get("max_rounds"):
            raise ConfigurationError("termination.max_rounds is required")

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute group chat with multiple rounds of agent interactions."""
        execution_error = None

        self.logger.info(
            "Starting group chat with {} participants, strategy: {}",
            len(self.participants),
            self.selection_strategy,
        )

        # Initialize chat state
        chat_history = []
        current_round = 0
        max_rounds = self.termination["max_rounds"]
        termination_condition = self.termination.get("condition")

        # Add user input as initial message
        user_text = context.get("user_text", "")
        if user_text:
            chat_history.append({"round": 0, "speaker": "user", "content": user_text})
            self.logger.debug("Added user message to chat history")

        # Build all participant agents
        participant_agents = {}
        for agent_id, node_ref in self.participants.items():
            agent = await self.agent_runner.build_agent(agent_id, context)
            participant_agents[agent_id] = agent
            self.logger.debug("Built participant agent: {}", agent_id)

        # Conversation loop
        participant_list = list(self.participants.keys())
        round_robin_index = 0
        termination_reason = None

        while current_round < max_rounds:
            current_round += 1
            self.logger.info("Group chat round {}/{}", current_round, max_rounds)

            # Select next speaker
            if self.selection_strategy == "round_robin":
                speaker_id = participant_list[round_robin_index % len(participant_list)]
                round_robin_index += 1
                self.logger.debug("Round-robin selected speaker: {}", speaker_id)
            else:  # llm
                speaker_id = await self._select_speaker_via_llm(
                    chat_history, participant_list, context
                )
                self.logger.debug("LLM selected speaker: {}", speaker_id)

            # Execute selected participant (agent or pipeline)
            agent_response = await self._execute_participant(
                speaker_id,
                participant_agents.get(speaker_id),  # None for pipeline participants
                self.participant_runners.get(speaker_id),  # None for agent participants
                chat_history,
                current_round,
                participant_list,
                context,
            )

            # Add response to chat history
            chat_history.append(
                {
                    "round": current_round,
                    "speaker": speaker_id,
                    "content": agent_response,
                }
            )

            self.logger.success(
                "Round {} complete: {} spoke ({} chars)",
                current_round,
                speaker_id,
                len(agent_response),
            )

            # Check termination condition
            if termination_condition:
                try:
                    # Shortcut: handle contains(last_message, '...') safely in Python
                    import re as _re

                    m = _re.fullmatch(
                        r"\s*contains\(\s*last_message\s*,\s*['\"](.+?)['\"]\s*\)\s*",
                        termination_condition,
                    )
                    if m:
                        needle = m.group(1)
                        if needle in str(agent_response or ""):
                            self.logger.info(
                                "Termination (python shortcut) met: contains(last_message, '{}')",
                                needle,
                            )
                            termination_reason = "condition_met"
                            break
                    else:
                        # Prepare context with last_message for general evaluation
                        eval_context = context.copy()
                        eval_context["last_message"] = agent_response
                        eval_context["chat_history"] = chat_history

                        if evaluate_expression(termination_condition, eval_context):
                            self.logger.info(
                                "Termination condition met: {}", termination_condition
                            )
                            termination_reason = "condition_met"
                            break
                except Exception as e:
                    self.logger.warning(
                        "Failed to evaluate termination condition: {}", e
                    )

        # Determine termination reason
        if not termination_reason:
            termination_reason = "max_rounds"

        # Build result
        final_message = chat_history[-1]["content"] if chat_history else ""

        result = {
            "participants": participant_list,
            "rounds": current_round,
            "chat_history": chat_history,
            "final_message": final_message,
            "termination_reason": termination_reason,
        }

        self.logger.success(
            "Group chat completed: {} rounds, reason: {}",
            current_round,
            termination_reason,
        )
        return result

    async def _select_speaker_via_llm(
        self, chat_history: List[Dict], participants: List[str], context: Dict[str, Any]
    ) -> str:
        """Use orchestrator LLM to select next speaker."""

        # Build selection prompt
        if self.orchestrator_ref:
            # Use custom orchestrator
            self.logger.debug("Using custom orchestrator: {}", self.orchestrator_ref)
            selection_prompt = self._build_selection_prompt(chat_history, participants)

            # Execute custom orchestrator
            orchestrator_agent = await self.agent_runner.build_agent(
                self.orchestrator_ref.split(":")[0], context
            )

            # Prepare context for orchestrator
            orchestrator_context = context.copy()
            orchestrator_context["user_text"] = selection_prompt

            result = await self.agent_runner.execute_agent(
                self.orchestrator_ref.split(":")[0],
                orchestrator_agent,
                orchestrator_context,
            )

            response_content = result.get("content", "")
        else:
            # Build virtual orchestrator
            self.logger.debug("Using virtual orchestrator")

            # Load participant descriptions
            participant_descriptions = await self._load_participant_descriptions(
                participants, context
            )

            # Build orchestrator prompt
            orchestrator_prompt = self._build_virtual_orchestrator_prompt(
                participant_descriptions
            )

            # Build selection prompt
            selection_prompt = self._build_selection_prompt(chat_history, participants)

            # Execute virtual orchestrator
            virtual_config = {
                "instruction": orchestrator_prompt,
                "framework": "langgraph",
                "model": self.orchestrator_model,
            }

            selection_context = context.copy()
            selection_context["user_text"] = selection_prompt

            result = await self.agent_runner.execute_virtual_agent(
                agent_id="__group_chat_orchestrator__",
                inline_config=virtual_config,
                context=selection_context,
            )

            response_content = result.get("content", "")

        # Parse NEXT_SPEAKER: agent_id
        import re

        match = re.search(r"NEXT_SPEAKER:\s*(\w+)", response_content, re.IGNORECASE)

        if match:
            speaker_id = match.group(1)
            if speaker_id in participants:
                return speaker_id
            else:
                self.logger.warning(
                    "Orchestrator selected invalid speaker: {}, falling back to round-robin",
                    speaker_id,
                )
        else:
            self.logger.warning(
                "Failed to parse speaker selection, falling back to round-robin"
            )

        # Fallback: use round-robin
        return participants[len(chat_history) % len(participants)]

    async def _load_participant_descriptions(
        self, participants: List[str], context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Load descriptions for all participants from ui_manifest."""
        descriptions = []
        
        # Get pipeline_id and project_dir from context
        pipeline_id = context.get("pipeline_id")
        project_dir = context.get("project_dir")
        
        # Load ui_manifest for the pipeline
        ui_manifest = {}
        if pipeline_id and project_dir:
            try:
                from pathlib import Path
                import yaml
                ui_manifest_path = Path(project_dir) / "config" / "ui_manifests" / f"{pipeline_id}.yml"
                if ui_manifest_path.exists():
                    with open(ui_manifest_path, 'r', encoding='utf-8') as f:
                        ui_manifest = yaml.safe_load(f) or {}
                    self.logger.debug("Loaded UI manifest for pipeline {}: {} agents", pipeline_id, len(ui_manifest.get("agents", [])))
                else:
                    self.logger.warning("UI manifest not found for pipeline {}: {}", pipeline_id, ui_manifest_path)
            except Exception as e:
                self.logger.warning("Failed to load UI manifest for pipeline {}: {}", pipeline_id, e)
        
        # Create a map of agent_id -> subtitle from ui_manifest
        agent_subtitle_map = {}
        agents = ui_manifest.get("agents", [])
        for agent in agents:
            agent_id = agent.get("id")
            subtitle = agent.get("subtitle")
            if agent_id and subtitle:
                agent_subtitle_map[agent_id] = subtitle

        for agent_id in participants:
            try:
                # Get description from ui_manifest
                description = agent_subtitle_map.get(agent_id)
                if not description:
                    # If not found in ui_manifest, raise error (subtitle is mandatory)
                    raise ValueError(f"Agent '{agent_id}' not found in ui_manifest.agents or missing subtitle")

                descriptions.append({"id": agent_id, "description": description})
                self.logger.debug(
                    "Loaded description for {} from ui_manifest: {}", agent_id, description[:50]
                )
            except Exception as e:
                self.logger.error(
                    "Failed to load description for {}: {}", agent_id, e
                )
                # Fail fast - don't use fallback since subtitle is mandatory
                raise RuntimeError(f"Failed to load agent description for {agent_id}: {e}")

        return descriptions

    def _build_virtual_orchestrator_prompt(
        self, participant_descriptions: List[Dict[str, str]]
    ) -> str:
        """Build virtual orchestrator system prompt from participant descriptions."""

        participant_list = []
        for i, desc in enumerate(participant_descriptions, 1):
            participant_list.append(f"{i}. {desc['id']}: {desc['description']}")

        prompt = f"""You are a group chat facilitator managing a conversation between multiple participants.

Participants:
{chr(10).join(participant_list)}

Your Role:
- Analyze the conversation history
- Determine who should speak next based on context and participant expertise
- Select the most relevant participant to contribute

Response Format:
Respond EXACTLY with:
NEXT_SPEAKER: <participant_id>

Example:
NEXT_SPEAKER: poet_form

Guidelines:
- Consider each participant's expertise and role
- Balance participation (don't always pick the same agent)
- Choose based on conversation flow and needs
- Use EXACTLY the format: "NEXT_SPEAKER: <participant_id>"
"""

        return prompt

    def _build_selection_prompt(
        self, chat_history: List[Dict], participants: List[str]
    ) -> str:
        """Build prompt for speaker selection."""

        # Format chat history
        history_text = []
        for msg in chat_history[-5:]:  # Last 5 messages for context
            speaker = msg["speaker"]
            content = msg["content"][:200]  # Truncate long messages
            history_text.append(f"[{speaker}]: {content}")

        prompt = f"""Conversation History:
{chr(10).join(history_text)}

Available Participants: {", ".join(participants)}

Who should speak next?"""

        return prompt

    async def _execute_participant(
        self,
        participant_id: str,
        agent: Any,
        participant_runner: BaseRunner,
        chat_history: List[Dict],
        current_round: int,
        participants: List[str],
        context: Dict[str, Any],
    ) -> str:
        """Execute a participant (agent or pipeline) with group chat context."""

        # Build chat context for participant
        participant_context = context.copy()

        # Format chat history for participant prompt
        history_text = []
        for msg in chat_history:
            speaker = msg["speaker"]
            content = msg["content"]
            history_text.append(f"[{speaker}]: {content}")

        # Create enriched user_text with chat context
        chat_context_text = f"""You are participating in a group chat with: {", ".join([p for p in participants if p != participant_id])}

Conversation so far:
{chr(10).join(history_text)}

It's your turn to respond. Provide your input to the discussion."""

        participant_context["user_text"] = chat_context_text
        participant_context["chat_history"] = chat_history
        participant_context["current_round"] = current_round
        participant_context["my_role"] = participant_id
        participant_context["other_participants"] = [
            p for p in participants if p != participant_id
        ]

        # Check if this is a pipeline or agent participant
        if participant_runner and isinstance(participant_runner, PipelineStepRunner):
            # Pipeline participant - execute pipeline
            self.logger.debug("Executing pipeline participant: {}", participant_id)
            result = await participant_runner.run(participant_context)
            
            # Extract response from pipeline final output
            # Pipeline outputs are stored in context.upstream[pipeline_id]
            upstream = participant_context.get("upstream", {})
            pipeline_output = upstream.get(participant_id, {})
            if isinstance(pipeline_output, dict):
                parsed = pipeline_output.get("parsed", {})
                if isinstance(parsed, dict):
                    # Try to get a content-like field
                    response = parsed.get("content") or parsed.get("result") or parsed.get("response") or str(parsed)
                else:
                    response = str(parsed)
            else:
                response = str(pipeline_output)
        elif agent:
            # Agent participant - execute agent
            self.logger.debug("Executing agent participant: {}", participant_id)
            result = await self.agent_runner.execute_agent(
                participant_id, agent, participant_context
            )
            
            # Extract response content
            response = result.get("content", "")
            if not response and "agent_inputs" in result:
                response = result["agent_inputs"].get("content", "")
        else:
            raise ValueError(f"Participant {participant_id} has neither agent nor pipeline runner")

        return response


class PipelineStepRunner(BaseRunner):
    """Runner for executing a sub-pipeline as a node within a parent pipeline.
    
    This runner:
    1. Applies input_mapping to transform parent context values for sub-pipeline
    2. Executes the sub-pipeline with shared context
    3. Stores sub-pipeline results in nested structure: nodes, intermediate, and final outputs
    """
    
    def __init__(
        self,
        pipeline_id: str,
        compiled_pattern_runner: BaseRunner,
        input_mapping: Dict[str, str],
        sub_pipeline_config: Dict[str, Any],
        config_result,
        populate_upstream_context_func=None,
        output_manager=None,
    ) -> None:
        super().__init__()
        self.pipeline_id = pipeline_id
        self.compiled_pattern_runner = compiled_pattern_runner
        self.input_mapping = input_mapping
        self.sub_pipeline_config = sub_pipeline_config
        self.config_result = config_result
        self.populate_upstream_context_func = populate_upstream_context_func
        self.output_manager = output_manager
        
        # Track node outputs during execution
        self.node_outputs = {}
    
    def _evaluate_input_value(self, template: str, context: Dict[str, Any]) -> Any:
        """Evaluate input mapping value (supports both expressions and Jinja2 templates).
        
        Args:
            template: Expression string or Jinja2 template
            context: Execution context
            
        Returns:
            Evaluated value
        """
        # Strip outer Jinja2 template markers if present ({{expression}} -> expression)
        stripped = template.strip()
        is_jinja2 = stripped.startswith("{{") and stripped.endswith("}}")
        
        if is_jinja2:
            # Try Jinja2 template first
            try:
                from jinja2 import Template, Environment, Undefined
                env = Environment(undefined=Undefined, autoescape=False)
                tmpl = env.from_string(stripped)
                
                # Build render context with upstream data flattened
                render_context = dict(context)
                upstream = context.get("upstream", {})
                if isinstance(upstream, dict):
                    # Add agent namespaces: render_context[agent_id] = upstream[agent_id].parsed
                    for agent_id, node_data in upstream.items():
                        if isinstance(node_data, dict):
                            parsed = node_data.get("parsed", {})
                            if isinstance(parsed, dict):
                                render_context[agent_id] = parsed
                                # Also flatten for convenience
                                for k, v in parsed.items():
                                    if k not in render_context:
                                        render_context[k] = v
                
                result = tmpl.render(**render_context)
                return result
            except Exception as e:
                self.logger.debug("Jinja2 template evaluation failed, trying expression: {}", e)
                # Fall through to expression evaluation
        
        # Try expression evaluation
        try:
            from topaz_agent_kit.utils.expression_evaluator import evaluate_expression_value
            result = evaluate_expression_value(stripped, context)
            return result
        except Exception as e:
            self.logger.warning("Expression evaluation failed for '{}': {}", template, e)
            # Return as string if both fail
            return template
    
    def _apply_input_mapping(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply input_mapping to create context variables for sub-pipeline's first node.
        
        Args:
            context: Parent pipeline context
            
        Returns:
            Modified context with input variables set
        """
        if not self.input_mapping:
            return context
        
        self.logger.debug("Applying input mapping for pipeline {}: {}", self.pipeline_id, self.input_mapping)
        
        # Evaluate each input mapping
        for var_name, template in self.input_mapping.items():
            try:
                value = self._evaluate_input_value(template, context)
                # Set in context so first node can access it
                context[var_name] = value
                self.logger.debug("Mapped input '{}' = {} (type: {})", var_name, value, type(value).__name__)
            except Exception as e:
                self.logger.error("Failed to evaluate input mapping '{}' = '{}': {}", var_name, template, e)
                raise ValueError(f"Input mapping failed for '{var_name}': {e}")
        
        return context
    
    def _store_pipeline_outputs(
        self, 
        pipeline_result: Dict[str, Any], 
        context: Dict[str, Any],
        sub_pipeline_upstream: Dict[str, Any]
    ) -> None:
        """Store sub-pipeline outputs in nested structure for parent access.
        
        Structure:
        context.upstream[pipeline_id] = {
            "result": final_output,
            "parsed": final_parsed,
            "nodes": {
                node_id: {
                    "result": node_result,
                    "parsed": node_parsed
                }
            },
            "intermediate": {
                output_id: {
                    "value": intermediate_value
                }
            }
        }
        """
        # Initialize upstream context if needed
        if "upstream" not in context:
            context["upstream"] = {}
        
        # Use instance_pipeline_id if available (for repeat patterns), otherwise use pipeline_id
        storage_id = getattr(self, 'instance_pipeline_id', None) or self.pipeline_id
        
        # Get final output from sub-pipeline
        # Try to get from output_manager first, then fallback to pipeline_result
        final_output = pipeline_result
        final_parsed = pipeline_result
        
        outputs_config = self.sub_pipeline_config.get("outputs", {})
        final_config = outputs_config.get("final", {})
        if final_config:
            final_node_id = final_config.get("node")
            if final_node_id and final_node_id in sub_pipeline_upstream:
                final_node_data = sub_pipeline_upstream[final_node_id]
                if isinstance(final_node_data, dict):
                    final_output = final_node_data.get("result", pipeline_result)
                    final_parsed = final_node_data.get("parsed", pipeline_result)
            elif isinstance(pipeline_result, dict) and final_node_id in pipeline_result:
                # Final output might be in pipeline_result directly
                final_output = pipeline_result[final_node_id]
                if isinstance(final_output, dict):
                    final_parsed = final_output.get("parsed", final_output)
                else:
                    final_parsed = final_output
        
        # Build nodes dict from sub-pipeline upstream
        nodes_dict = {}
        for node_id, node_data in sub_pipeline_upstream.items():
            if isinstance(node_data, dict):
                nodes_dict[node_id] = {
                    "result": node_data.get("result"),
                    "parsed": node_data.get("parsed", {})
                }
        
        # Build intermediate outputs dict
        intermediate_dict = {}
        intermediate_configs = outputs_config.get("intermediate", [])
        for intermediate_config in intermediate_configs:
            output_id = intermediate_config.get("id") or intermediate_config.get("node")
            node_id = intermediate_config.get("node")
            if node_id and node_id in nodes_dict:
                # Extract value using selectors if specified
                node_parsed = nodes_dict[node_id].get("parsed", {})
                selectors = intermediate_config.get("selectors", [])
                if selectors and isinstance(node_parsed, dict):
                    # Extract using selectors
                    extracted_value = {}
                    for selector in selectors:
                        if selector in node_parsed:
                            extracted_value[selector] = node_parsed[selector]
                    intermediate_dict[output_id] = {"value": extracted_value if extracted_value else node_parsed}
                else:
                    intermediate_dict[output_id] = {"value": node_parsed}
        
        # Store in upstream context using storage_id (instance_id for repeat patterns)
        context["upstream"][storage_id] = {
            "result": final_output,
            "parsed": final_parsed,
            "nodes": nodes_dict,
            "intermediate": intermediate_dict
        }
        
        self.logger.info(
            "Stored pipeline outputs for '{}': {} nodes, {} intermediate outputs",
            storage_id,
            len(nodes_dict),
            len(intermediate_dict)
        )
    
    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sub-pipeline with input mapping and store results.
        
        Args:
            context: Parent pipeline context (shared with sub-pipeline)
            
        Returns:
            Sub-pipeline execution result
        """
        self.logger.input("Executing pipeline step: {}", self.pipeline_id)
        
        # Create isolated context for sub-pipeline execution
        # We need to:
        # 1. Share read-only data (project_dir, emitter, etc.) - shallow copy is fine
        # 2. Isolate upstream dict - deep copy so sub-pipeline writes don't affect parent
        # 3. Remove parent's agent_factory so sub-pipeline creates its own
        import copy
        modified_context = context.copy()  # Shallow copy for top-level keys
        
        # Deep copy upstream dict for isolation
        # Sub-pipeline can read parent's upstream data, but writes won't affect parent
        if "upstream" in context:
            modified_context["upstream"] = copy.deepcopy(context["upstream"])
            self.logger.debug("Deep copied upstream context for sub-pipeline isolation")
        else:
            modified_context["upstream"] = {}
        
        # Apply input mapping to context
        # This sets variables that the first node in sub-pipeline expects
        self._apply_input_mapping(modified_context)
        
        # CRITICAL: Remove parent's agent_factory from context so sub-pipeline creates its own
        # The sub-pipeline's AgentRunner needs to create an AgentFactory with sub_config_result
        # to find agents from the sub-pipeline's nodes section
        if "agent_factory" in modified_context:
            del modified_context["agent_factory"]
            self.logger.debug("Removed parent's agent_factory from context for sub-pipeline execution")
        
        # Store original upstream keys to track what sub-pipeline adds
        original_upstream_keys = set(modified_context.get("upstream", {}).keys())
        
        # Get sub-pipeline node IDs for filtering
        sub_pipeline_nodes = self.sub_pipeline_config.get("nodes", [])
        sub_pipeline_node_ids = {node.get("id") for node in sub_pipeline_nodes if isinstance(node, dict)}
        
        # Execute sub-pipeline pattern
        try:
            # Execute the compiled pattern runner
            pipeline_result = await self.compiled_pattern_runner.run(modified_context)
            
            # Get sub-pipeline's upstream (what was added during execution)
            # Filter to only include nodes from sub-pipeline (not parent nodes)
            sub_pipeline_upstream = modified_context.get("upstream", {})
            filtered_upstream = {
                node_id: node_data 
                for node_id, node_data in sub_pipeline_upstream.items()
                if node_id in sub_pipeline_node_ids and node_id not in original_upstream_keys
            }
            
            # Store pipeline outputs in nested structure
            self._store_pipeline_outputs(pipeline_result, context, filtered_upstream)
            
            self.logger.success("Pipeline step '{}' completed", self.pipeline_id)
            return pipeline_result
            
        except Exception as e:
            self.logger.error("Pipeline step '{}' failed: {}", self.pipeline_id, e)
            raise
