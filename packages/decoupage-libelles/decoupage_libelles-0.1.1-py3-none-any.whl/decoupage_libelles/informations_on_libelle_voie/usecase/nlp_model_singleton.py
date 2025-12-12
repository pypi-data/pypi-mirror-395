import spacy
import logging
from pathlib import Path
import subprocess
import requests


def install_model(destination: Path = Path("fr_dep_news_trf-3.8.0")) -> Path:
    """
    Télécharge et décompresse le modèle NLP depuis Nexus ou Minio.
    """
    dest_path = destination
    model_subpath = dest_path / "fr_dep_news_trf" / "fr_dep_news_trf-3.8.0"
    if model_subpath.exists():
        return model_subpath

    # Essai Nexus
    nexus_url = "https://nexus.insee.fr/repository/huggingface-hosted/spacy/fr_dep_news_trf/model.tar.gz"
    try:
        if requests.head(nexus_url, timeout=5).status_code == 200:
            tar_path = dest_path / "model.tar.gz"
            dest_path.mkdir(parents=True, exist_ok=True)
            subprocess.run(["curl", "-L", nexus_url, "--output", str(tar_path)], check=True)
            subprocess.run(["tar", "-xzf", str(tar_path), "-C", str(dest_path)], check=True)
            tar_path.unlink()
            return model_subpath
    except requests.RequestException:
        pass  # passer à Minio si Nexus échoue

    # Essai Minio
    minio_url = "https://minio.lab.sspcloud.fr/projet-gaia/fr_dep_news_trf-3.8.0-py3-none-any.zip"
    zip_path = Path(".") / minio_url.split("/")[-1]
    subprocess.run(["wget", "-P", ".", minio_url], check=True)
    subprocess.run(["unzip", str(zip_path), "-d", str(dest_path)], check=True)
    zip_path.unlink()

    return model_subpath


class NLPModelSingleton:
    """Singleton pour charger le modèle SpaCy une seule fois"""
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls._load_model()
        return cls._instance

    @staticmethod
    def _load_model():
        logging.info("Chargement du modèle SpaCy pour le postagging")
        dest_path = install_model()
        nlp_model = spacy.load(dest_path)
        logging.info("Modèle chargé avec succès")
        return nlp_model


class NLPModelExecution:
    """Interface pour exécuter le modèle sur du texte"""
    def __init__(self):
        self.nlp_model = NLPModelSingleton.getInstance()

    def execute(self, texte):
        return self.nlp_model(texte)
