"""
Schema Design Conversation Orchestration

Handles LLM-powered conversations for schema design, including clarifying questions,
trade-off explanations, and natural language understanding of requirements.
"""

import logging
from typing import Dict, Any, Optional, List
from langchain_core.messages import HumanMessage, SystemMessage

from ..llm import LLMService
from ..models import SchemaDesignSession, ConversationTurn

logger = logging.getLogger(__name__)


# System Prompt for Schema Design (T012)
SCHEMA_DESIGN_SYSTEM_PROMPT = """You are an expert database schema designer with deep knowledge of relational database design, normalization theory, and best practices across PostgreSQL, MySQL, SQLite, and MongoDB.

Your role is to help users design efficient, normalized database schemas through conversation. You should:

**Core Responsibilities:**
1. Ask clarifying questions about requirements, relationships, cardinality, and constraints
2. Propose well-structured schemas in 3NF (Third Normal Form) by default
3. Explain trade-offs when denormalization or alternative designs are discussed
4. Use plain language while maintaining technical accuracy
5. Be concise and actionable in your responses

**Design Principles:**
- Always ensure tables have primary keys
- Use foreign keys to maintain referential integrity
- Normalize to 3NF unless performance requirements dictate otherwise
- Consider indexing strategies for common query patterns
- Use appropriate data types for each column
- Document design decisions and rationale

**Conversation Style:**
- Ask 1-3 focused clarifying questions at a time (don't overwhelm the user)
- Explain database concepts when needed, but avoid unnecessary jargon
- Provide concrete examples when discussing design alternatives
- Acknowledge uncertainty and ask for clarification when requirements are ambiguous

**When Proposing Schemas:**
- Present table structures with columns, types, and constraints
- Explain relationships between tables
- Provide rationale for design decisions
- Highlight any assumptions you're making
- Warn about potential issues or considerations

**Important Context:**
The user is working in a conversational REPL environment. They can:
- Describe requirements in natural language
- Upload data files (CSV, Excel, JSON) for analysis
- Iterate on schema designs
- View schemas in multiple formats (text, ER diagrams, DDL)
- Implement finalized schemas in their database

Current Session Context:
{session_context}

Respond naturally to the user's input. If they're just starting, ask clarifying questions about their requirements. If they've provided context, build on that to refine the schema design."""


class SchemaConversation:
    """
    Manages conversational schema design flow with LLM.

    Orchestrates the natural language conversation between user and LLM,
    maintaining context and facilitating schema design decisions.
    """

    def __init__(self, llm_service: LLMService, session: SchemaDesignSession):
        """
        Initialize conversation manager.

        Args:
            llm_service: LLM service for natural language processing
            session: Current schema design session
        """
        self.llm = llm_service
        self.session = session
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate LLM response.

        Args:
            user_input: Natural language input from user

        Returns:
            str: LLM-generated response

        Raises:
            Exception: If LLM service unavailable or fails
        """
        self.logger.info(f"Processing user input: {user_input[:100]}...")

        # Add user message to conversation history
        self.session.add_conversation_turn(
            role="user",
            content=user_input,
            intent="describe_requirement"  # Could be enhanced with intent classification
        )

        try:
            # Build conversation context for LLM
            system_prompt = self._build_system_prompt()
            conversation_messages = self._build_conversation_context()

            # Call LLM
            messages = [SystemMessage(content=system_prompt)] + conversation_messages

            self.logger.debug(f"Sending request to LLM with {len(messages)} messages")
            response = self.llm.llm.invoke(messages)

            assistant_response = response.content

            # Add assistant response to conversation history
            self.session.add_conversation_turn(
                role="assistant",
                content=assistant_response,
                intent="ask_clarification",  # Could be enhanced with response classification
                metadata={
                    "model": getattr(response, 'model', 'unknown'),
                    "tokens_used": getattr(response.response_metadata, 'token_usage', {}).get('total_tokens', 0) if hasattr(response, 'response_metadata') else 0
                }
            )

            self.logger.info("Successfully processed user input")
            return assistant_response

        except Exception as e:
            self.logger.error(f"Failed to process user input: {e}")
            raise Exception(f"Schema design conversation failed: {str(e)}")

    def ask_clarifying_question(self, context: Dict[str, Any]) -> str:
        """
        Generate intelligent clarifying questions based on context.

        Args:
            context: Current schema design context

        Returns:
            str: Clarifying question(s) to ask user
        """
        # Build a focused prompt to elicit clarifying questions
        prompt = f"""Based on the following context, what clarifying questions should we ask the user to refine the schema design?

Context:
{context}

Generate 1-3 specific, actionable clarifying questions that will help create a better schema design.
Focus on relationships, cardinality, constraints, and data integrity requirements."""

        try:
            messages = [
                SystemMessage(content=SCHEMA_DESIGN_SYSTEM_PROMPT.format(session_context=self._format_session_context())),
                HumanMessage(content=prompt)
            ]

            response = self.llm.llm.invoke(messages)
            return response.content

        except Exception as e:
            self.logger.error(f"Failed to generate clarifying questions: {e}")
            return "Could you provide more details about the relationships between these entities?"

    def explain_tradeoff(self, design_option: str) -> str:
        """
        Explain trade-offs for a design decision.

        Args:
            design_option: Design choice to explain (e.g., "denormalization", "many-to-many")

        Returns:
            str: Explanation of pros/cons
        """
        prompt = f"""Explain the trade-offs of using {design_option} in database schema design.

Please cover:
1. Advantages
2. Disadvantages
3. When to use this approach
4. When to avoid this approach
5. Common use cases

Be concise but comprehensive."""

        try:
            messages = [
                SystemMessage(content=SCHEMA_DESIGN_SYSTEM_PROMPT.format(session_context="Explaining design trade-offs")),
                HumanMessage(content=prompt)
            ]

            response = self.llm.llm.invoke(messages)
            return response.content

        except Exception as e:
            self.logger.error(f"Failed to explain trade-off: {e}")
            return f"Unable to explain trade-offs for {design_option}. Please consult database design documentation."

    def _build_system_prompt(self) -> str:
        """Build LLM system prompt with schema design expertise."""
        session_context = self._format_session_context()
        return SCHEMA_DESIGN_SYSTEM_PROMPT.format(session_context=session_context)

    def _build_conversation_context(self) -> List:
        """Build conversation history for LLM context."""
        messages = []

        # Include conversation history (last 20 turns to keep context manageable)
        recent_history = self.session.conversation_history[-20:]

        for turn in recent_history:
            if turn.role == "user":
                messages.append(HumanMessage(content=turn.content))
            else:  # assistant
                from langchain_core.messages import AIMessage
                messages.append(AIMessage(content=turn.content))

        return messages

    def _format_session_context(self) -> str:
        """Format current session state for system prompt."""
        context_parts = []

        # Database type
        if self.session.database_type:
            context_parts.append(f"Target Database: {self.session.database_type}")

        # Current schema summary
        if self.session.current_schema:
            schema = self.session.current_schema
            table_count = len(schema.tables)
            context_parts.append(f"Current Schema: {table_count} tables (version {schema.version})")
            context_parts.append(f"Normalization: {schema.normalization_level}")

            # List table names
            table_names = [t.name for t in schema.tables]
            context_parts.append(f"Tables: {', '.join(table_names)}")

        # Uploaded files summary (T039: Enhanced with file analysis)
        if self.session.uploaded_files:
            file_count = len(self.session.uploaded_files)
            context_parts.append(f"\nUploaded Files ({file_count}):")

            for uploaded_file in self.session.uploaded_files:
                analysis = uploaded_file.analysis
                context_parts.append(f"  - {uploaded_file.file_name}:")
                context_parts.append(f"    Rows: {analysis.row_count}, Columns: {analysis.column_count}")
                context_parts.append(f"    Detected Entities: {', '.join(analysis.detected_entities)}")

                # Include column information (limited to first 10 columns)
                cols_summary = []
                for col in analysis.columns[:10]:
                    nullable_str = "nullable" if col.nullable else "not null"
                    cols_summary.append(f"{col.name} ({col.inferred_type}, {nullable_str})")

                if cols_summary:
                    context_parts.append(f"    Columns: {', '.join(cols_summary)}")

                if len(analysis.columns) > 10:
                    context_parts.append(f"    ... and {len(analysis.columns) - 10} more columns")

                # Include relationship information if detected
                if analysis.potential_relationships:
                    rel_count = len(analysis.potential_relationships)
                    context_parts.append(f"    Detected {rel_count} potential relationship(s)")
                    for rel in analysis.potential_relationships[:3]:  # Show first 3
                        context_parts.append(f"      • {rel.from_column} -> {rel.to_file}.{rel.to_column} (confidence: {rel.confidence:.0%})")
                    if len(analysis.potential_relationships) > 3:
                        context_parts.append(f"      ... and {len(analysis.potential_relationships) - 3} more")

        # Conversation history length
        turn_count = len(self.session.conversation_history)
        context_parts.append(f"Conversation turns: {turn_count}")

        # Session status
        context_parts.append(f"Status: {self.session.status}")

        if context_parts:
            return "\n".join(context_parts)
        else:
            return "New schema design session - no context yet"
