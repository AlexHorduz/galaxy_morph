import os
import pandas as pd
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import matplotlib.pyplot as plt

dataset_path = "./filtered_images"
labels_path = os.path.join(dataset_path, "gz_decals_auto_posteriors_existing_top_400_each.csv")
images_folder = os.path.join(dataset_path, "gz_decals_dr5_png_cropped_top_400")

labels = pd.read_csv(labels_path)

labels = labels[[
    "iauname", "smooth-or-featured_smooth_fraction",
    "smooth-or-featured_featured-or-disk_fraction", "smooth-or-featured_artifact_fraction"
]]

labels.columns = ["iauname", "smooth", "featured", "artifact"]

labels["label"] = labels.values[:, 1:].argmax(axis=1)

print(labels.head())
print(labels["label"].value_counts())

# sampled_labels = pd.DataFrame()
# num_img_for_class = 400
# for label in [0, 1, 2]:
#     label_subset = labels[labels["label"] == label]
#     if len(label_subset) >= num_img_for_class:
#         label_subset = label_subset.sample(n=400, random_state=123)
#     else:
#         print(f"Warning: Not enough images for label {label} (only {len(label_subset)})")
#     sampled_labels = pd.concat([sampled_labels, label_subset], ignore_index=True)
#
# print("Sampled label distribution:")
# print(sampled_labels["label"].value_counts())

images = []
i = 1
for filename in labels["iauname"].values:
    image_name = os.path.join(images_folder, f"{filename}.png")

    image = Image.open(image_name)
    image_array = np.array(image)
    # print(f'{i}: Extracted: {image_name}')
    i += 1
    images.append(image_array)

images = np.array(images)
print(images.shape)

images_flat = images.reshape(images.shape[0], -1)
print(f"Flattened images shape: {images_flat.shape}")

scaler = StandardScaler()
images_flat_scaled = scaler.fit_transform(images_flat)

pca = PCA()
images_pca = pca.fit_transform(images_flat_scaled)
print(f"PCA applied. Reduced dimensions: {images_pca.shape}")

explained_variance = pca.explained_variance_ratio_
print(f"Explained variance ratio: {explained_variance}")
print(f"Total explained variance: {np.sum(explained_variance)}")
cumulative_explained_variance = np.cumsum(explained_variance)

plt.figure()
plt.plot(
    range(1, len(cumulative_explained_variance) + 1),
    cumulative_explained_variance,
    marker='o', linestyle='--'
)
plt.title("Cumulative Explained Variance")
plt.xlabel("Number of Principal Components")
plt.ylabel("Cumulative Explained Variance")
plt.grid()
plt.savefig("./variance.png")

threshold = 0.9
n_components_optimal = np.argmax(cumulative_explained_variance >= threshold) + 1
print(f"Number of components needed to explain {threshold * 100}% of variance: {n_components_optimal}")

loading_scores = pca.components_.T

pc1_loadings = np.abs(loading_scores[:, 0])
top_features_idx = np.argsort(pc1_loadings)[::-1]

top_n = 10
top_features = top_features_idx[:top_n]

print(f"Top {top_n} features contributing to PC1:")
for idx in top_features:
    print(f"Feature {idx}, Loading score: {pc1_loadings[idx]:.4f}")

plt.figure(figsize=(12, 6))
plt.bar(range(len(pc1_loadings)), pc1_loadings, color="skyblue")
plt.title("Feature Contribution to PC1")
plt.xlabel("Feature Index")
plt.ylabel("Absolute Loading Score")
plt.savefig("feature_contribution_pc1.png")

fig = px.scatter_3d(
    x=images_pca[:, 0], y=images_pca[:, 1], z=images_pca[:, 2],
    color=labels["label"].astype(str),
    title="PCA of Galaxy Images with Labels for smooth, featured, artifact",
    labels={'color': 'Label'},
    color_continuous_scale='Viridis'
)

fig.write_html("galaxies_pca_plot.html")
print("Plot saved as pca_plot.html")