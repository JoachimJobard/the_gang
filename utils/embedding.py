import numpy as np
import flax.linen as nn

def convert_to_num(card_list) -> np.ndarray:
    converted_array = np.zeros(len(card_list), dtype=int)
    suit_equivalence = {'Heart': 0, 'Diamond': 1, 'Club': 2, 'Spade': 3}
    for i in range(len(card_list)):
        rank, suit = card_list[i]
        converted_array[i] = rank + 13 * suit_equivalence.get(suit, 0)
    return converted_array

class CardEncoder(nn.Module):
    embedding_dim: int

    @nn.compact
    def __call__(self, cards, mask):
        embedder = nn.Embed(num_embeddings=53, features=self.embedding_dim) # 52 cards + 1 for masked cards
        embedded_cards = embedder(cards) #(batch_size, num_cards, embedding_dim)
        masked_embedding = embedded_cards * mask[:, :, None] # (batch_size, num_cards, embedding_dim)
        masked_embedding = masked_embedding.sum(axis=1) # (batch_size, embedding_dim) summing is not destructive since we are in high dimension
        return masked_embedding

