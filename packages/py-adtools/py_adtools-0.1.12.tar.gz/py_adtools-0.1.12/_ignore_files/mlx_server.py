"""
Copyright (c) 2025 Rui Zhang <rzhang.cs@gmail.com>

NOTICE: This code is under MIT license. This code is intended for academic/research purposes only.
Commercial use of this software or its derivatives requires prior written permission.
"""

try:
    import mlx_lm
    import mlx.core as mx
except ImportError:
    raise ImportError('Python package "mlx_lm" is not installed.')

from typing import Optional, List, Literal, Dict, Any
import os

from .lm_base import LanguageModel


class MLXServer(LanguageModel):
    def __init__(self,
                 model_path: str,
                 tokenizer_path: Optional[str] = None,
                 max_model_len: int = 16384,
                 dtype: str = 'float16',
                 seed: int = 0,
                 mlx_log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO',
                 chat_template_kwargs: Optional[Dict[str, Any]] = None):
        """Initialize an MLX-based language model server.
        Args:
            model_path: Path to the model to load.
            tokenizer_path: Path to the tokenizer to use. Defaults to model_path.
            max_model_len: Maximum model length.
            dtype: Data type for model weights.
            seed: Random seed.
            mlx_log_level: Log level for MLX.
            chat_template_kwargs: Keyword arguments for chat template.

        Example:
            # Initialize MLX server
            llm = MLXServer(
                model_path='path/to/model',
                tokenizer_path='path/to/tokenizer',
                dtype='float16'
            )
            # Generate text
            response = llm.chat_completion('Hello, how are you?')

            # Release resources
            llm.close()
        """
        self._model_path = model_path
        self._tokenizer_path = tokenizer_path if tokenizer_path is not None else model_path
        self._max_model_len = max_model_len
        self._dtype = dtype
        self._seed = seed
        self._mlx_log_level = mlx_log_level
        self._chat_template_kwargs = chat_template_kwargs

        # Set MLX log level
        os.environ['MLX_LOG_LEVEL'] = mlx_log_level

        # Initialize model and tokenizer
        self.model, self.tokenizer = self._load_model()

    def _load_model(self):
        """Load the model and tokenizer using mlx_lm."""
        print(f'[MLX] Loading model from: {self._model_path}')
        print(f'[MLX] Loading tokenizer from: {self._tokenizer_path}')
        # Load model and tokenizer
        return mlx_lm.load(self._model_path)

    def chat_completion(
            self,
            message: str,
            max_tokens: Optional[int] = None,
            temperature: float = 0.9,
            top_p: float = 0.9,
            chat_template_kwargs: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate a chat completion response.
        Args:
            message: The input message string.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Top-p sampling parameter.
            chat_template_kwargs: Additional chat template arguments.
        Returns:
            Generated response text.
        """
        # Prepare the prompt
        prompt = message.strip()

        # Format as chat message if using chat template
        if self._chat_template_kwargs or chat_template_kwargs:
            messages = [{'role': 'user', 'content': prompt}]
            prompt = mlx_lm.format_chat(messages, self.tokenizer)

        # Generate response
        response = mlx_lm.generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens or self._max_model_len,
            temp=temperature,
            top_p=top_p,
            verbose=True
        )
        return response

    def generate(self,
                 prompt: str,
                 max_tokens: Optional[int] = None,
                 temperature: float = 0.9,
                 top_p: float = 0.9) -> str:
        """Generate text from a prompt (non-chat format).
        Args:
            prompt: Input prompt text.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Top-p sampling parameter.
        Returns:
            Generated text.
        """
        response = mlx_lm.generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens or self._max_model_len,
            temp=temperature,
            top_p=top_p,
            verbose=True
        )
        return response

    def close(self):
        """Release model resources."""
        print('[MLX] Releasing model resources')
        # MLX models are in memory, so we just clear references
        self.model = None
        self.tokenizer = None
        mx.metal.clear_cache()

    def __del__(self):
        self.close()
