import os
import subprocess
from pathlib import Path


def install_model(destination: str = "fr_dep_news_trf-3.8.0", use_intranet: bool = False):
    """
    Télécharge et décompresse le modèle NLP nécessaire.

    Args:
        destination: chemin où installer le modèle
        use_intranet: True si téléchargement depuis Nexus interne, False depuis internet
    """
    dest_path = Path(destination)
    if dest_path.exists():
        print(f"Le modèle existe déjà dans {dest_path}")
        return

    if use_intranet:
        url = "https://nexus.insee.fr/repository/huggingface-hosted/spacy/fr_dep_news_trf/model.tar.gz"
        tar_path = dest_path / "model.tar.gz"
        dest_path.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", url, "--output", str(tar_path)], check=True)
        subprocess.run(["tar", "-xzf", str(tar_path), "-C", str(dest_path)], check=True)
        tar_path.unlink()
    else:
        url = "https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.8.0-py3-none-any.zip"
        zip_path = Path(".") / "fr_dep_news_trf-3.8.0-py3-none-any.zip"
        subprocess.run(["wget", "-P", ".", url], check=True)
        subprocess.run(["unzip", str(zip_path), "-d", str(dest_path)], check=True)
        zip_path.unlink()

    print(f"Modèle installé dans {dest_path}")
