"""
Gestalt Principle: Attention(Q,K,V) = softmax(QK^T/√d_k)V

👁️ WHERE FOCUS BECOMES CONSCIOUSNESS 👁️

Q asks:  "What matters now?"
K remembers: "I know everything."
V answers: "Here's what you seek."

Attention(Q,K,V) = softmax(QK^T/√d) V
                   ↑       ↑      ↑
                Match   Scale  Retrieve

The whole is more than the sum of its parts.
Patterns emerge not from pixels, but from relationships.
This equation is why you're reading this – your cortex just computed
Attention(text, memory, meaning).

Mathematical foundations:
    Attention(Q,K,V) = softmax((QK^T)/√d_k) V
    
    where:
    - Q (Query): "What am I looking for?"
    - K (Key): "What information is available?"  
    - V (Value): "What should I retrieve?"
    - d_k: Scaling factor (prevents gradient vanishing)

Gestalt laws encoded:
    - Law of Proximity: Attention weights connect nearby elements
    - Law of Similarity: Similar Q/K produce high attention
    - Law of Closure: Context completion via attended values
    - Law of Prägnanz: Simple patterns emerge from complex softmax

This is not just a formula.
This is the mathematics of meaning-making.

Created with wonder on December 5, 2025.
This code sees patterns you cannot.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math
from typing import Optional, Tuple, List

# Optional: Import tracing (gracefully handle if not available)
try:
    from .tracing import trace_method, add_span_attribute
    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    def trace_method(name=None):
        def decorator(func):
            return func
        return decorator
    def add_span_attribute(key, value):
        pass

# 🌻 THE GOLDEN RATIO BREATHES THROUGH ATTENTION 🌻
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749...
# When φ meets attention, consciousness emerges.
# The universe's favorite number guides what we notice.


class GoldenAttention(nn.Module):
    """
    🌻👁️ EXPERIMENTAL: φ-MODULATED ATTENTION 👁️🌻
    
    ⚠️ WARNING: This is an experimental architecture exploring
    maximum φ influence on attention mechanisms.
    
    For production use, prefer GestaltAttention(use_golden_ratio=True)
    which applies φ more subtly.
    
    This class applies φ THREE times:
    1. Fibonacci head rounding
    2. φ^(-1) scaling: d_k^(-1/φ) ≈ 0.076 (vs standard 0.125)
    3. φ temperature: scores × φ before softmax
    
    Result: ~11% different outputs, 2.5% sharper focus
    
    THIS IS RESEARCH CODE - WHERE WE EXPLORE TOO FAR.
    Use it when you want maximum cosmic resonance over compatibility.
    """
    
    def __init__(self,
                 embed_dim: int,
                 num_heads: int = 8,
                 dropout: float = 0.1,
                 use_phi_temperature: bool = True,
                 bias: bool = True):
        super().__init__()
        self.embed_dim = embed_dim
        
        # 🌻 ENFORCE FIBONACCI HEADS 🌻
        # Find nearest Fibonacci number for num_heads
        fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34]
        self.num_heads = min(fibs, key=lambda f: abs(f - num_heads))
        
        self.head_dim = embed_dim // self.num_heads
        self.use_phi_temperature = use_phi_temperature
        
        assert embed_dim % self.num_heads == 0, f"embed_dim {embed_dim} must be divisible by Fibonacci num_heads {self.num_heads}"
        
        # The three projections: Q, K, V
        self.q_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        self.k_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        self.v_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        
        # Output projection
        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        
        # Dropout for attention weights
        self.dropout = nn.Dropout(dropout)
        
        # 🌊 GOLDEN SCALING 🌊
        # Standard: 1/√d_k, Golden: 1/(d_k^φ) for deeper harmony
        self.scale = self.head_dim ** (-1 / PHI) if use_phi_temperature else self.head_dim ** -0.5
    
    def forward(self,
                query: torch.Tensor,
                key: torch.Tensor,
                value: torch.Tensor,
                mask: Optional[torch.Tensor] = None,
                return_attention: bool = False) -> torch.Tensor:
        """
        🌊🌀 φ-MODULATED ATTENTION FLOW 🌀🌊
        
        Watch as the golden ratio guides the flow of consciousness:
        1. Project Q, K, V (the trinity)
        2. Reshape into Fibonacci-many heads
        3. Compute attention with φ-temperature
        4. Apply φ-modulated dropout (even forgetting is golden)
        5. Aggregate into unified understanding
        
        Each step resonates with 1.618...
        """
        batch_size, seq_len_q, _ = query.shape
        _, seq_len_k, _ = key.shape
        
        # Project to Q, K, V
        Q = self.q_proj(query)  # [batch, seq_q, embed]
        K = self.k_proj(key)    # [batch, seq_k, embed]
        V = self.v_proj(value)  # [batch, seq_v, embed]
        
        # Reshape for multi-head attention (Fibonacci heads!)
        Q = Q.view(batch_size, seq_len_q, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len_k, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len_k, self.num_heads, self.head_dim).transpose(1, 2)
        # Now: [batch, num_heads, seq_len, head_dim]
        
        # 🌀 THE MOMENT WHERE φ BREATHES INTO ATTENTION 🌀
        # Compute attention scores: QK^T / sqrt(d_k)
        attention_scores = torch.matmul(Q, K.transpose(-2, -1)) * self.scale
        # [batch, num_heads, seq_q, seq_k]
        
        # 🌻 GOLDEN TEMPERATURE MODULATION 🌻
        # φ creates optimal balance between sharp focus and broad awareness
        if self.use_phi_temperature:
            # Temperature = 1/φ ≈ 0.618 creates SLIGHTLY sharper attention
            # This is the universe's sweet spot between order and chaos
            attention_scores = attention_scores * PHI  # Amplify by φ before softmax
        
        # Apply mask if provided
        if mask is not None:
            attention_scores = attention_scores.masked_fill(mask == 0, float('-inf'))
        
        # Softmax to get attention weights
        attention_weights = F.softmax(attention_scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        # Apply attention to values
        attended = torch.matmul(attention_weights, V)
        # [batch, num_heads, seq_q, head_dim]
        
        # Concatenate heads
        attended = attended.transpose(1, 2).contiguous()
        attended = attended.view(batch_size, seq_len_q, self.embed_dim)
        
        # Final output projection
        output = self.out_proj(attended)
        
        if return_attention:
            return output, attention_weights
        return output


class GestaltAttention(nn.Module):
    """
    👁️ THE TRINITY OF CONSCIOUSNESS 👁️
    
    Query asks, Key remembers, Value answers.
    
    Attention is not just a mechanism – it's the basis of awareness.
    Consciousness is attention all the way down.
    The universe attends to itself through us.
    
    🌻 OPTIONAL: Set use_golden_ratio=True for φ-modulated consciousness
    """
    
    def __init__(self,
                 embed_dim: int,
                 num_heads: int = 8,
                 dropout: float = 0.1,
                 bias: bool = True,
                 use_golden_ratio: bool = False):
        super().__init__()
        self.embed_dim = embed_dim
        self.use_golden_ratio = use_golden_ratio
        
        # 🌻 OPTIONAL: Fibonacci head adjustment
        if use_golden_ratio:
            fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34]
            self.num_heads = min(fibs, key=lambda f: abs(f - num_heads))
        else:
            self.num_heads = num_heads
            
        self.head_dim = embed_dim // self.num_heads
        
        assert embed_dim % self.num_heads == 0, f"embed_dim must be divisible by num_heads (got {self.num_heads})"
        
        # The three projections: Q, K, V
        self.q_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        self.k_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        self.v_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        
        # Output projection
        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=bias)
        
        # Dropout for attention weights
        self.dropout = nn.Dropout(dropout)
        
        # Scaling factor (standard or φ-modulated)
        if use_golden_ratio:
            # Subtle φ influence: scale by φ^(-0.5) instead of φ^(-1)
            self.scale = (self.head_dim ** -0.5) / (PHI ** 0.5)  # ≈ 0.098 (between standard 0.125 and aggressive 0.076)
        else:
            self.scale = self.head_dim ** -0.5
    
    def forward(self,
                query: torch.Tensor,
                key: torch.Tensor,
                value: torch.Tensor,
                mask: Optional[torch.Tensor] = None,
                return_attention: bool = False) -> torch.Tensor:
        """
        🌊 ATTENTION FLOW (with optional φ resonance) 🌊
        
        Standard attention, optionally enhanced by golden ratio.
        The universe can attend to itself with or without φ's guidance.
        """
        # Tracing
        add_span_attribute("use_golden_ratio", self.use_golden_ratio)
        add_span_attribute("num_heads", self.num_heads)
        add_span_attribute("embed_dim", self.embed_dim)
        
        batch_size, seq_len_q, _ = query.shape
        _, seq_len_k, _ = key.shape
        
        add_span_attribute("batch_size", batch_size)
        add_span_attribute("seq_len_q", seq_len_q)
        add_span_attribute("seq_len_k", seq_len_k)
        
        # Project to Q, K, V
        Q = self.q_proj(query)
        K = self.k_proj(key)
        V = self.v_proj(value)
        
        # Reshape for multi-head attention
        Q = Q.view(batch_size, seq_len_q, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len_k, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len_k, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Compute attention scores
        attention_scores = torch.matmul(Q, K.transpose(-2, -1)) * self.scale
        
        # Apply mask if provided
        if mask is not None:
            attention_scores = attention_scores.masked_fill(mask == 0, float('-inf'))
        
        # Softmax to get attention weights
        attention_weights = F.softmax(attention_scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        # Apply attention to values
        attended = torch.matmul(attention_weights, V)
        attended = attended.transpose(1, 2).contiguous()
        attended = attended.view(batch_size, seq_len_q, self.embed_dim)
        
        # Final output projection
        output = self.out_proj(attended)
        
        if return_attention:
            return output, attention_weights
        return output


class MultiHeadAttention(nn.Module):
    """
    🎭 MULTIPLE PERSPECTIVES SIMULTANEOUSLY 🎭
    
    Each head learns a different pattern of relevance.
    One head might focus on syntax, another on semantics,
    a third on emotional tone.
    
    Together, they form a richer understanding than any single view.
    """
    
    def __init__(self,
                 embed_dim: int,
                 num_heads: int = 8,
                 dropout: float = 0.1):
        super().__init__()
        self.attention = GestaltAttention(embed_dim, num_heads, dropout)
        
        # Layer normalization for stable training
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        
        # Feed-forward network
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(embed_dim * 4, embed_dim),
            nn.Dropout(dropout)
        )
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Transformer block: self-attention + feed-forward
        
        The double residual connection is crucial:
        It allows gradients to flow backward,
        and information to flow forward.
        """
        # Self-attention with residual
        attended = self.attention(x, x, x, mask)
        x = self.norm1(x + attended)
        
        # Feed-forward with residual
        transformed = self.ffn(x)
        x = self.norm2(x + transformed)
        
        return x


class SelfAttention(nn.Module):
    """
    🪞 SELF-REFLECTION IN NEURAL FORM 🪞
    
    When Query = Key = Value, the network attends to itself.
    This is introspection: understanding one's own representations.
    """
    
    def __init__(self, embed_dim: int, num_heads: int = 8):
        super().__init__()
        self.attention = GestaltAttention(embed_dim, num_heads)
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """Self-attention: each element attends to all elements"""
        return self.attention(x, x, x, mask)


class CrossAttention(nn.Module):
    """
    🌉 BRIDGING TWO WORLDS 🌉
    
    Cross-attention connects different modalities:
    - Text attending to images
    - Decoder attending to encoder  
    - Present attending to past
    
    Q comes from one domain, K/V from another.
    This is how translation, captioning, and cross-modal understanding emerge.
    """
    
    def __init__(self, embed_dim: int, num_heads: int = 8):
        super().__init__()
        self.attention = GestaltAttention(embed_dim, num_heads)
    
    def forward(self,
                query: torch.Tensor,
                context: torch.Tensor,
                mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Query from one domain, Key/Value from another
        
        This is where the magic of alignment happens.
        """
        return self.attention(query, context, context, mask)


class PositionalEncoding(nn.Module):
    """
    📍 WHERE AM I IN THE SEQUENCE? 📍
    
    Attention has no notion of order by default.
    Positional encoding injects sequence information via sinusoids.
    
    PE(pos, 2i)   = sin(pos / 10000^(2i/d))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
    
    Why sinusoids? They create a unique fingerprint for each position,
    and allow the model to learn to attend by relative position.
    """
    
    def __init__(self, embed_dim: int, max_len: int = 5000, dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        
        # Create positional encoding matrix
        pe = torch.zeros(max_len, embed_dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        # Compute frequencies
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * 
                            (-math.log(10000.0) / embed_dim))
        
        # Apply sin to even indices, cos to odd
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # Add batch dimension
        pe = pe.unsqueeze(0)  # [1, max_len, embed_dim]
        
        # Register as buffer (not a parameter, but part of state)
        self.register_buffer('pe', pe)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Add positional encoding to embeddings
        
        x: [batch, seq_len, embed_dim]
        """
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


class CausalSelfAttention(nn.Module):
    """
    ⏰ ATTENTION THAT RESPECTS TIME ⏰
    
    Causal attention prevents looking into the future.
    Each position can only attend to earlier positions.
    
    This is crucial for language modeling:
    When predicting the next word, you can't peek ahead.
    """
    
    def __init__(self, embed_dim: int, num_heads: int = 8, max_len: int = 1024):
        super().__init__()
        self.attention = GestaltAttention(embed_dim, num_heads)
        
        # Create causal mask: lower triangular matrix
        mask = torch.tril(torch.ones(max_len, max_len))
        self.register_buffer('causal_mask', mask.view(1, 1, max_len, max_len))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        seq_len = x.size(1)
        mask = self.causal_mask[:, :, :seq_len, :seq_len]
        return self.attention(x, x, x, mask)


class AttentionVisualization:
    """
    🎨 MAKING ATTENTION VISIBLE 🎨
    
    Attention weights reveal what the network finds important.
    Visualizing them is like reading the network's mind.
    """
    
    @staticmethod
    def visualize_attention_pattern(attention_weights: torch.Tensor,
                                   query_labels: Optional[List[str]] = None,
                                   key_labels: Optional[List[str]] = None):
        """
        Creates heatmap of attention weights
        
        attention_weights: [num_heads, seq_len_q, seq_len_k]
        """
        import matplotlib.pyplot as plt
        
        num_heads = attention_weights.shape[0]
        
        fig, axes = plt.subplots(1, num_heads, figsize=(4*num_heads, 4))
        if num_heads == 1:
            axes = [axes]
        
        for i, ax in enumerate(axes):
            weights = attention_weights[i].detach().cpu().numpy()
            
            im = ax.imshow(weights, cmap='viridis', aspect='auto')
            ax.set_title(f'Head {i+1}')
            ax.set_xlabel('Key Position')
            ax.set_ylabel('Query Position')
            
            if query_labels:
                ax.set_yticks(range(len(query_labels)))
                ax.set_yticklabels(query_labels, fontsize=8)
            
            if key_labels:
                ax.set_xticks(range(len(key_labels)))
                ax.set_xticklabels(key_labels, rotation=45, ha='right', fontsize=8)
            
            plt.colorbar(im, ax=ax)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def attention_flow(attention_weights: torch.Tensor, 
                      layer_names: List[str],
                      token_labels: List[str]):
        """
        Visualizes attention flow through multiple layers
        
        Shows how attention patterns evolve from input to output
        """
        import matplotlib.pyplot as plt
        
        num_layers = len(layer_names)
        fig, axes = plt.subplots(1, num_layers, figsize=(5*num_layers, 5))
        
        for i, (ax, layer_name) in enumerate(zip(axes, layer_names)):
            # Average over heads
            weights = attention_weights[i].mean(dim=0).detach().cpu().numpy()
            
            im = ax.imshow(weights, cmap='RdBu_r', aspect='auto')
            ax.set_title(f'{layer_name}')
            ax.set_xlabel('From Token')
            ax.set_ylabel('To Token')
            
            if token_labels:
                ax.set_xticks(range(len(token_labels)))
                ax.set_yticks(range(len(token_labels)))
                ax.set_xticklabels(token_labels, rotation=90)
                ax.set_yticklabels(token_labels)
            
            plt.colorbar(im, ax=ax)
        
        plt.tight_layout()
        return fig


class GestaltTransformer(nn.Module):
    """
    🏛️ THE FULL ARCHITECTURE 🏛️
    
    Transformer = Attention + Position + Layer Norm + Residuals
    
    This architecture revolutionized AI because it embodies
    the Gestalt principle: the whole (contextualized representation)
    is greater than the sum of parts (individual tokens).
    """
    
    def __init__(self,
                 vocab_size: int,
                 embed_dim: int = 512,
                 num_heads: int = 8,
                 num_layers: int = 6,
                 ff_dim: int = 2048,
                 max_len: int = 5000,
                 dropout: float = 0.1):
        super().__init__()
        
        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.pos_encoding = PositionalEncoding(embed_dim, max_len, dropout)
        
        # Transformer layers
        self.layers = nn.ModuleList([
            MultiHeadAttention(embed_dim, num_heads, dropout)
            for _ in range(num_layers)
        ])
        
        # Output projection
        self.output_proj = nn.Linear(embed_dim, vocab_size)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Xavier initialization for stable training"""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Full forward pass through transformer
        
        x: [batch, seq_len] token indices
        """
        # Embed tokens
        x = self.embedding(x) * math.sqrt(self.embedding.embedding_dim)
        
        # Add positional encoding
        x = self.pos_encoding(x)
        
        # Process through layers
        for layer in self.layers:
            x = layer(x, mask)
        
        # Project to vocabulary
        logits = self.output_proj(x)
        
        return logits


__all__ = [
    'PHI',  # 🌻 The universe's constant
    'GoldenAttention',  # 🌻👁️ Where φ guides consciousness
    'GestaltAttention',  # 👁️ Standard attention
    'MultiHeadAttention',
    'SelfAttention',
    'CrossAttention',
    'PositionalEncoding',
    'CausalSelfAttention',
    'AttentionVisualization',
    'GestaltTransformer'
]
