# Momento API

## Aperçu
Cette API basée sur Flask extrait le texte de divers types de fichiers, y compris les PDF, DOCX, PPTX et images, et génère des flashcards et des résumés. Elle utilise actuellement `TextBlob` pour la création de flashcards et un pipeline `transformers` pour le résumé.

## Fonctionnalités
- Extraction de texte de fichiers PDF, DOCX, PPTX et images.
- Génération de flashcards à partir du texte extrait.
- Résumé de texte pour capturer les points clés.

## Plans futurs
Migration prévue vers l'API GPT-4 pour améliorer la génération de flashcards et de résumés.

## Usage
Envoyez des fichiers en POST à `/upload` pour les flashcards et à `/summarize` pour le résumé.

## Installation

Installez les dépendances suivantes via `pip` :

- Flask : `pip install Flask`
- PyPDF2 : `pip install PyPDF2`
- python-docx : `pip install python-docx`
- python-pptx : `pip install python-pptx`
- Pillow : `pip install Pillow`
- pytesseract : `pip install pytesseract`
- transformers : `pip install transformers`

Ces installations sont nécessaires pour le bon fonctionnement de l'API, qui extrait le texte de différents formats de fichiers et génère des flashcards et des résumés.

*Remarque : Cette API est en développement actif, et les fonctionnalités évolueront avec l'intégration de GPT-4.*
