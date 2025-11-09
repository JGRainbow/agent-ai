from typing import List, Dict, Any, Optional
from openai import OpenAI
from openai.types.chat import ChatCompletion
import logging
from src.llm.provider import AbstractLLMProvider
from src.config import settings

logger = logging.getLogger(__name__)


class OpenAIProvider(AbstractLLMProvider):
    """OpenAI implementation of the LLM provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the OpenAI provider.

        Args:
            api_key: OpenAI API key. If None, uses settings.openai_api_key
            model: Model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.api_key = api_key or settings.openai_api_key
        self.model = model
        self.client = None

        if self.api_key and self.api_key != "test-api-key":
            self.client = OpenAI(api_key=self.api_key)
        else:
            logger.warning("OpenAI API key not set or using test key. LLM calls will be mocked.")

    def is_available(self) -> bool:
        """Check if OpenAI is available."""
        return self.client is not None

    def _build_prompt(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """
        Build the prompt for the LLM with context from retrieved chunks.

        Args:
            query: The user's question
            retrieved_chunks: Retrieved document chunks

        Returns:
            Formatted prompt string
        """
        # Build context from retrieved chunks
        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_parts.append(
                f"[Document {i} - {chunk.get('doc_name', 'Unknown')}]\n"
                f"{chunk.get('text', '')}\n"
            )

        context = "\n".join(context_parts)

        prompt = f"""You are a helpful assistant that answers questions about changing names after marriage in the UK, based on official government documents.

Use ONLY the information provided in the context below to answer the question. If the context doesn't contain enough information to answer the question, say so clearly.

Context from official documents:
{context}

Question: {query}

Instructions:
1. Answer the question based ONLY on the provided context
2. Be specific and cite which document the information comes from
3. If the context doesn't contain the answer, say "I don't have enough information in the provided documents to answer this question."
4. Keep your answer concise but complete
5. Use UK English spelling and terminology

Answer:"""

        return prompt

    def _calculate_confidence(
        self,
        retrieved_chunks: List[Dict[str, Any]],
        response: ChatCompletion
    ) -> float:
        """
        Calculate confidence score based on retrieved chunks and response.

        Args:
            retrieved_chunks: Retrieved chunks
            response: LLM response

        Returns:
            Confidence score between 0.0 and 1.0
        """
        if not retrieved_chunks:
            return 0.0

        # Base confidence on:
        # 1. Number of relevant chunks (more chunks = higher confidence)
        # 2. Average relevance score of chunks
        # 3. Whether response indicates uncertainty

        avg_score = sum(chunk.get("score", 0.0) for chunk in retrieved_chunks) / len(retrieved_chunks)

        # Check if response indicates uncertainty
        response_text = response.choices[0].message.content.lower()
        uncertainty_indicators = [
            "i don't know",
            "i don't have",
            "not enough information",
            "unclear",
            "uncertain"
        ]

        has_uncertainty = any(indicator in response_text for indicator in uncertainty_indicators)

        # Base confidence on average score, penalize if uncertain
        confidence = min(avg_score * 1.2, 1.0)  # Boost slightly, cap at 1.0
        if has_uncertainty:
            confidence *= 0.6  # Reduce confidence if uncertain

        return max(0.0, min(1.0, confidence))

    def generate_answer(
        self,
        query: str,
        retrieved_chunks: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate an answer using OpenAI.

        Args:
            query: The user's question
            retrieved_chunks: Retrieved document chunks
            context: Optional additional context (not used currently)

        Returns:
            Dictionary with answer, confidence, and reasoning
        """
        # If no chunks retrieved, return early
        if not retrieved_chunks:
            return {
                "answer": "I couldn't find any relevant information to answer your question. Please try rephrasing it or check if the documents contain information about this topic.",
                "confidence": 0.0,
                "reasoning": "No chunks retrieved"
            }

        # If using test key, return mock response
        if not self.is_available():
            logger.warning("Using mock LLM response (test API key)")
            return {
                "answer": f"Mock answer for: {query}. Based on {len(retrieved_chunks)} retrieved chunks.",
                "confidence": 0.7,
                "reasoning": "Mock response - API key not configured"
            }

        try:
            # Build prompt
            prompt = self._build_prompt(query, retrieved_chunks)

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions about UK name change procedures based on official government documents."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=500,    # Limit response length
            )

            answer = response.choices[0].message.content.strip()
            confidence = self._calculate_confidence(retrieved_chunks, response)

            return {
                "answer": answer,
                "confidence": confidence,
                "reasoning": f"Generated using {self.model} based on {len(retrieved_chunks)} retrieved chunks"
            }

        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}", exc_info=True)
            # Fallback to a basic answer
            return {
                "answer": f"I encountered an error while generating an answer. However, I found {len(retrieved_chunks)} relevant document(s) that might help. Please try again or check the sources below.",
                "confidence": 0.3,
                "reasoning": f"Error: {str(e)}"
            }
