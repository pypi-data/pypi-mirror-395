"""
Basic Ollama functionality tests.

This module tests that Ollama is properly installed and working,
independent of the Revenium middleware.
"""

import pytest
import ollama


@pytest.mark.integration
class TestBasicOllama:
    """Test basic Ollama functionality without middleware."""

    def test_ollama_chat_works(self, setup_integration_test, model_name):
        """Test that basic Ollama chat functionality works."""
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    'role': 'user',
                    'content': 'Say hello in one sentence.',
                },
            ]
        )
        
        assert 'message' in response, "Response should contain 'message' field"
        assert 'content' in response['message'], "Message should contain 'content'"
        assert response['message']['content'], "Content should not be empty"
        
        # Verify token usage is available
        if 'eval_count' in response:
            assert response['eval_count'] > 0, "Should have completion tokens"

    def test_ollama_generate_works(self, setup_integration_test, model_name):
        """Test that basic Ollama generate functionality works."""
        response = ollama.generate(
            model=model_name,
            prompt='Say hello in one sentence.'
        )
        
        assert 'response' in response, "Response should contain 'response' field"
        assert response['response'], "Response should not be empty"

