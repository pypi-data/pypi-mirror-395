from urllib.request import urlopen

import timm
import torch
from PIL import Image

img = Image.open(
    urlopen(
        "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/beignets-task-guide.png"
    )
)

model = timm.create_model("timm/efficientvit_b0.r224_in1k", pretrained=True).to("cuda")
model = torch.compile(model=model, fullgraph=True, mode="max-autotune")
print(model)
# model = model.eval()

# # get model specific transforms (normalization, resize)
# data_config = timm.data.resolve_model_data_config(model)
# transforms = timm.data.create_transform(**data_config, is_training=False)

# output = model(transforms(img).unsqueeze(0))  # unsqueeze single image into batch of 1

# top5_probabilities, top5_class_indices = torch.topk(output.softmax(dim=1) * 100, k=5)
