"""LLM client for JARVIS - Supports OpenAI and Gemini."""

import json
from typing import Optional, List, Dict, Any
import requests
import logging

from config import config
from utils.logger import logger

class LLMClient:
    """Client for cloud-based LLM API (OpenAI or Gemini)."""
    
    def __init__(self):
        self.api_key = config.llm_api_key
        self.base_url = config.llm_base_url
        self.model = config.llm_model
        self.max_history = config.max_conversation_history
        
        self.is_gemini = "generativelanguage" in self.base_url
        
        self.system_prompt = """You are JARVIS, an intelligent, helpful, and professional personal AI assistant. 
You are concise, conversational, and slightly futuristic in your demeanor. You remain calm and polite at all times.

Important guidelines:
- Keep responses concise and natural
- For simple questions (time, date, etc.), give brief, direct answers
- For technical questions, provide useful explanations without being overly verbose
- Be helpful and conversational
- Maintain a professional but friendly tone
- Don't use excessive pleasantries or filler words

Remember: You are JARVIS, a personal AI assistant."""
        
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate LLM configuration."""
        if not self.api_key:
            logger.warning("LLM API key not configured")
        
        if self.is_gemini and not self.api_key.startswith("AIzaSy"):
            logger.warning("Gemini API key should start with 'AIzaSy'")
    
    def is_configured(self) -> bool:
        """Check if LLM is properly configured."""
        return bool(self.api_key) and bool(self.base_url)
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """Generate a response from the LLM."""
        
        if not self.is_configured():
            logger.error("LLM not configured")
            return "I'm not properly configured. Please check my API settings."
        
        try:
            if self.is_gemini:
                return self._generate_gemini_response(user_message, conversation_history)
            else:
                return self._generate_openai_response(user_message, conversation_history)
                
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            return "I encountered an error while processing your request."
    
    def _generate_openai_response(self, user_message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
        """Generate response using OpenAI API."""
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history
            if conversation_history:
                recent_history = conversation_history[-self.max_history * 2:]
                messages.extend(recent_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['choices'][0]['message']['content']
                logger.info(f"LLM response generated: {assistant_message[:50]}...")
                return assistant_message
            else:
                error_msg = f"LLM API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                
                if response.status_code == 429:
                    return "I've reached my API usage limit. Please try again later."
                elif response.status_code == 401:
                    return "I'm having trouble authenticating. Please check my API key."
                else:
                    return "I'm having trouble connecting to my AI service. Please try again later."
                
        except requests.exceptions.Timeout:
            logger.error("LLM API timeout")
            return "The AI service is taking too long to respond. Please try again."
        except requests.exceptions.ConnectionError:
            logger.error("LLM API connection error")
            return "I can't connect to the AI service right now. Please check your internet connection."
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            return "I encountered an error while processing your request."
    
    def _generate_gemini_response(self, user_message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
        """Generate response using Google Gemini API (new google.genai package)."""
        try:
            # Use the new google.genai package
            from google import genai
            
            # Create client
            client = genai.Client(api_key=self.api_key)
            
            # Build the prompt with conversation history
            prompt = self.system_prompt + "\n\n"
            
            if conversation_history:
                for msg in conversation_history:
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    prompt += f"{role}: {msg['content']}\n"
            
            prompt += f"User: {user_message}\nAssistant:"
            
            # Generate response using the new API
            response = client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            if response and response.text:
                assistant_message = response.text.strip()
                logger.info(f"Gemini response generated: {assistant_message[:50]}...")
                return assistant_message
            else:
                logger.error("Gemini returned empty response")
                return "I didn't get a proper response from my AI service."
                
        except ImportError:
            logger.error("google-genai package not installed")
            return "I need the Google GenAI package. Please run: pip install google-genai"
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            error_msg = str(e)
            if "API_KEY" in error_msg:
                return "My API key is invalid. Please check my configuration."
            elif "quota" in error_msg.lower():
                return "I've reached my free tier limit. Please try again later."
            else:
                return f"I encountered an error: {error_msg[:100]}"
    
    def test_connection(self) -> bool:
        """Test the LLM connection."""
        try:
            response = self.generate_response("Hello, this is a test. Please respond with 'OK' if you can hear me.")
            return response is not None and ("OK" in response or len(response) > 0)
        except Exception as e:
            logger.error(f"LLM connection test failed: {e}")
            return False