import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


__all__ = ["compare_vectors_1d"]


def cosine_similarity(x1, x2):
    return torch.cosine_similarity(x1, x2, dim=0)


def element_wise_difference_stats(x1, x2):
    difference = x1 - x2
    stats = {
        "Mean": np.mean(difference),
        "Standard deviation": np.std(difference),
        "Min": np.min(difference),
        "Max": np.max(difference),
    }
    return pd.DataFrame(stats.items(), columns=["Statistic", "Difference"])


def plot_raw_embeddings(embeddings):
    plt.figure(figsize=(10, 6))
    for name, vector in embeddings.items():
        plt.scatter(range(len(vector)), vector, label=name, alpha=0.4)
    plt.xlabel("Dimension")
    plt.ylabel("Value")
    plt.title("Raw Vector Values")
    plt.legend()
    plt.show()


def plot_embedding_differences(embeddings):
    names = list(embeddings.keys())
    vectors = list(embeddings.values())
    difference = vectors[0] - vectors[1]

    plt.figure(figsize=(12, 6))
    plt.plot(range(len(difference)), difference, label="Difference", color="blue")

    # y_min = min(np.min(vectors[0]), np.min(vectors[1])) - 0.1
    # y_max = max(np.max(vectors[0]), np.max(vectors[1])) + 0.1

    # for i, (name, vector) in enumerate(embeddings.items()):
    #     color = 'red' if i == 0 else 'orange'
    #     plt.axhline(y=np.min(vector), color=color, linestyle='--', alpha=0.5, label=f'Min of {name}')
    #     plt.axhline(y=np.max(vector), color=color, linestyle='--', alpha=0.5, label=f'Max of {name}')

    y_min, y_max = -1, 1
    plt.ylim(y_min, y_max)

    plt.axhline(y=0, color="black", linestyle="-", alpha=0.5, label="Zero")
    plt.xlabel("Dimension")
    plt.ylabel("Value")
    # plt.title(f'Difference between Embeddings\n(Scaled to Embedding Range)')
    plt.title(f"'{names[0]}' - '{names[1]}'")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_difference_histogram(embeddings):
    names = list(embeddings.keys())
    vectors = list(embeddings.values())
    difference = vectors[0] - vectors[1]

    plt.figure(figsize=(10, 6))
    plt.hist(difference, bins=30, edgecolor="black")
    plt.xlabel("Difference")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of Differences between {names[0]} and {names[1]}")
    plt.show()


def compare_vectors_1d(embeddings):
    from IPython.display import display

    # Assert that the input dictionary contains exactly two items
    assert (
        len(embeddings) == 2
    ), "The input dictionary must contain exactly two embeddings."

    # Convert PyTorch tensors to NumPy arrays if necessary
    for name, vector in embeddings.items():
        if isinstance(vector, torch.Tensor):
            embeddings[name] = vector.detach().cpu().numpy()

    names = list(embeddings.keys())
    vectors = list(embeddings.values())

    # Cosine similarity
    cos_sim = cosine_similarity(torch.tensor(vectors[0]), torch.tensor(vectors[1]))
    print(f"Cosine similarity between {names[0]} and {names[1]}: {cos_sim.item()}")

    # Element-wise difference statistics
    diff_stats = element_wise_difference_stats(vectors[0], vectors[1])
    display(diff_stats)

    # Visualizations
    plot_raw_embeddings(embeddings)
    plot_embedding_differences(embeddings)
    plot_difference_histogram(embeddings)
