import subprocess
import logging

logger = logging.getLogger(__name__)


def text_to_phonemes(text: str, lang: str) -> str:
    """
    Appelle le binaire système espeak-ng pour convertir du texte en phonèmes.
    """
    try:
        commande = ["espeak-ng", "-q", "--ipa", "-v", lang, text]

        result = subprocess.run(commande, capture_output=True, text=True, check=True)

        phonemes = result.stdout.strip()

        return phonemes

    except FileNotFoundError:
        logger.error("The binary 'espeak-ng' is not installed in the system.")
        raise RuntimeError(
            "Can't find espeak-ng. Please be sure to have it installed."
            "(ex: sudo apt-get install espeak-ng)."
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error espeak-ng (code {e.returncode}): {e.stderr}")
        raise RuntimeError(f"Can't make phonemic conversion for : '{text}'")
