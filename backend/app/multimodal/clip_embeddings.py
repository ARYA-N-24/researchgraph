import torch
import open_clip
from PIL import Image
import os

from app.config import settings


class CLIPEmbedding:
    """
    Generate embeddings from images using CLIP.

    Uses native CLIP dimension:
    512 (ViT-B-32)

    Pinecone index MUST also be 512.
    """

    def __init__(self):

        print("🔄 Loading CLIP model...")

        self.model, _, self.preprocess = (
            open_clip.create_model_and_transforms(
                "ViT-B-32",
                pretrained="openai"
            )
        )

        self.model.eval()

        self.image_dir = settings.IMAGES_DIR

        # CLIP native dimension
        self.dimension = 512


    def embed_all_images(self):

        """
        Generate embeddings for all images.
        Uses 512-dimension vectors.
        """

        image_embeddings = []

        # Safety: check folder exists
        if not os.path.exists(self.image_dir):

            print("⚠️ Image directory not found")

            return image_embeddings


        for img_file in os.listdir(self.image_dir):

            if img_file.endswith(
                (".png", ".jpg", ".jpeg")
            ):

                img_path = os.path.join(
                    self.image_dir,
                    img_file
                )

                print(
                    f"🖼️ CLIP embedding: {img_file}"
                )

                try:

                    # Load image safely
                    image = self.preprocess(
                        Image.open(img_path).convert("RGB")
                    ).unsqueeze(0)

                    with torch.no_grad():

                        features = (
                            self.model.encode_image(
                                image
                            )
                        )

                    embedding = (
                        features[0]
                        .cpu()
                        .numpy()
                        .tolist()
                    )

                    # Safety check
                    if len(embedding) != self.dimension:

                        print(
                            f"⚠️ Skipping {img_file} "
                            f"(unexpected dimension)"
                        )

                        continue

                    image_embeddings.append({

                        "embedding": embedding,

                        "source": img_file

                    })

                except Exception as e:

                    print(
                        f"⚠️ Error processing "
                        f"{img_file}: {e}"
                    )


        print(
            f"🖼️ Total CLIP embeddings: "
            f"{len(image_embeddings)}"
        )

        return image_embeddings