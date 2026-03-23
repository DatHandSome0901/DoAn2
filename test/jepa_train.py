# import torch
# import torch.nn as nn
# import numpy as np
# from sentence_transformers import SentenceTransformer
# import os

# # ================= LOAD DATA =================
# docs = [l.strip() for l in open("data/all_text.txt", encoding="utf-8") if l.strip()]
# print("Docs:", len(docs))

# model_emb = SentenceTransformer("intfloat/multilingual-e5-base")
# emb = model_emb.encode(docs).astype("float32")

# # normalize tránh NaN
# emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)

# # tạo dữ liệu X → Y dự đoán embedding dòng tiếp theo
# X = torch.tensor(emb[:-1], dtype=torch.float32)
# Y = torch.tensor(emb[1:], dtype=torch.float32)

# print("X shape:", X.shape, "Y shape:", Y.shape)

# # ================= JEPA MODEL =================
# class JEPA(nn.Module):
#     def __init__(self, d):
#         super().__init__()
#         self.net = nn.Sequential(
#             nn.Linear(d, d),
#             nn.ReLU(),
#             nn.Linear(d, d)
#         )
#     def forward(self, x):
#         return self.net(x)

# m = JEPA(emb.shape[1])

# # learning rate nhỏ lại để không nổ gradient
# opt = torch.optim.Adam(m.parameters(), lr=1e-4)
# loss_fn = nn.MSELoss()

# # ================= TRAIN =================
# for e in range(30):
#     opt.zero_grad()
#     pred = m(X)
#     loss = loss_fn(pred, Y)
#     loss.backward()
#     opt.step()
#     print(f"Epoch {e} Loss {loss.item():.6f}")

# # ================= SAVE MODEL =================
# os.makedirs("models", exist_ok=True)
# torch.save(m.state_dict(), "models/jepa_model.pt")
# print("✅ Saved models/jepa_model.pt")
