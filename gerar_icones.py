from PIL import Image
from pathlib import Path

PASTA = Path("assets/icons")

logo = Image.open(PASTA / "logo.png")

# --------------------------
# ICO Windows
# --------------------------

logo.save(
    PASTA / "stockflow.ico",
    format="ICO",
    sizes=[
        (16,16),
        (24,24),
        (32,32),
        (48,48),
        (64,64),
        (128,128),
        (256,256)
    ]
)

# --------------------------
# Android
# --------------------------

logo.resize((1024,1024)).save(
    PASTA / "icon_1024.png"
)

# --------------------------
# Favicon
# --------------------------

logo.resize((64,64)).save(
    PASTA / "favicon.ico",
    format="ICO"
)

print("Ícones gerados com sucesso!")