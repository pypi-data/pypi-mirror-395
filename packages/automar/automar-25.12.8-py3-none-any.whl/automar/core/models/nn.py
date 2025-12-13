# -*- coding: utf-8 -*-
"""
Module containing the artificial neural networks (ANN) for stock market
forecasting.
"""

import math

from torch import nn
import torch


class GRUNet(nn.Module):
    """
    GRU-based model.

    Args:
        input_dim (int): Dimension of the input layer.
        hidden_dim (int): Size of the hidden layers.
        output_dim (int): Dimension of the output layers.
        n_layers (int): Number of hidden layers in GRU.
        drop_prob (float): [0., 1.], dropout probability.

    Attributes:
        input_dim (int): Dimension of the input layer.
        hidden_dim (int): Size of the hidden layers.
        output_dim (int): Dimension of the output layers.
        n_layers (int): Number of hidden layers in GRU.
        drop_prob (float): [0., 1.], dropout probability.
    """

    def __init__(
        self, input_dim, hidden_dim, output_dim, n_layers, drop_prob, layer_norm=True
    ):
        super(GRUNet, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        self.gru = nn.GRU(
            input_dim, hidden_dim, n_layers, batch_first=True, dropout=drop_prob
        )

        self.layer_norm = nn.LayerNorm(hidden_dim) if layer_norm else nn.Identity()
        self.dropout = nn.Dropout(drop_prob)
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.act = nn.GELU()
        self.fc2 = nn.Linear(hidden_dim // 2, output_dim)

        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, x, h=None):
        """
        Forward pass step.

        Args:
            x (tensor): Input tensor.
            h (tensor, optional): Short memory tensor of the GRU
                 layer. Defaults to zeros if not provided.

        Returns:
            Transformer out (tensor) vector and short term memory h (tensor)
            vector.
        """

        out, _ = self.gru(x, h)

        out = out[:, -1, :]
        out = self.layer_norm(out)
        out = self.dropout(out)

        out = self.fc1(out)
        out = self.act(out)
        out = self.dropout(out)
        logits = self.fc2(out)

        return logits.squeeze(-1)

    def init_hidden(self, batch_size, device):
        """
        Initialize the short term memory layer of GRU.

        Args:
            batch_size (int): Dimension of the batch size.
            device (str): Device where to store the generated tensor.

        Returns:
            hidden (tensor) containing a 0-filled short term memory layer.

        """
        weight = next(self.parameters()).data
        hidden = (
            weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device)
        )
        return hidden


class Transnet(nn.Module):
    def __init__(
        self,
        input_dim,
        hidden_dim,
        output_dim,
        n_layers,
        head_div,
        drop_prob,
        ff_mult=4,
        max_seq_len=1000,
        use_learned_pos=True,
    ):
        super().__init__()

        self.embed = nn.Linear(input_dim, hidden_dim, bias=True)

        if use_learned_pos:
            self.pos = nn.Parameter(torch.zeros(1, max_seq_len, hidden_dim))
            nn.init.trunc_normal_(self.pos, std=0.02)
        else:
            self.pos = None

        nhead = hidden_dim // head_div
        assert nhead >= 1 and hidden_dim % nhead == 0

        enc_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=nhead,
            dim_feedforward=ff_mult * hidden_dim,
            dropout=drop_prob,
            batch_first=True,
            norm_first=True,
            activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(
            enc_layer, num_layers=n_layers, enable_nested_tensor=False
        )

        self.mlp = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.GELU(),
            nn.Dropout(drop_prob),
            nn.Linear(hidden_dim // 2, output_dim),
        )
        self._init_weights()

    def forward(self, x, padding_mask: torch.Tensor | None = None):
        x = self.embed(x)
        if self.pos is not None:
            x = x + self.pos[:, : x.size(1), :]
        x = self.encoder(x, src_key_padding_mask=padding_mask)

        if padding_mask is not None:
            x = x.masked_fill(padding_mask.unsqueeze(-1), 0.0)
            lengths = (~padding_mask).sum(dim=1, keepdim=True).clamp(min=1)
            x = x.sum(dim=1) / lengths
        else:
            x = x.mean(dim=1)

        logits = self.mlp(x)
        if logits.size(-1) == 1:
            logits = logits.squeeze(-1)

        return logits

    def _init_weights(self) -> None:
        """
        Xavier-uniform for Linear/projection layers, zeros for biases,
        unit-gain LayerNorm, and a light init for embeddings.
        Safe for Transformer stacks and stable for hyperparameter sweeps.
        """
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

            elif isinstance(m, nn.LayerNorm):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)

            elif isinstance(m, nn.Embedding):
                nn.init.normal_(m.weight, mean=0.0, std=0.02)

            elif isinstance(m, nn.MultiheadAttention):
                if hasattr(m, "in_proj_weight") and m.in_proj_weight is not None:
                    nn.init.xavier_uniform_(m.in_proj_weight)
                if hasattr(m, "in_proj_bias") and m.in_proj_bias is not None:
                    nn.init.zeros_(m.in_proj_bias)

                nn.init.xavier_uniform_(m.out_proj.weight)
                if m.out_proj.bias is not None:
                    nn.init.zeros_(m.out_proj.bias)
