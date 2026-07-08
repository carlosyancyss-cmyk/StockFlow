from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent

ORIGINAL = BASE / "assets" / "icons" / "icon_1024.png"

DESTINOS = {
    "drawable-mdpi": 108,
    "drawable-hdpi": 162,
    "drawable-xhdpi": 216,
    "drawable-xxhdpi": 324,
    "drawable-xxxhdpi": 432,
}

RES = (
    BASE
    / "build"
    / "flutter"
    / "android"
    / "app"
    / "src"
    / "main"
    / "res"
)

if not ORIGINAL.exists():
    raise FileNotFoundError(f"Não encontrei:\n{ORIGINAL}")

img = Image.open(ORIGINAL).convert("RGBA")

for pasta, tamanho in DESTINOS.items():

    destino = RES / pasta
    destino.mkdir(parents=True, exist_ok=True)

    icone = img.resize((tamanho, tamanho), Image.LANCZOS)

    arquivo = destino / "ic_launcher_foreground.png"

    icone.save(arquivo)

    print(f"✔ {arquivo}")

print("\nTodos os ícones foram gerados com sucesso.")