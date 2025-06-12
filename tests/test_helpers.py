import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ancien test helpers supprimé car la gestion par fichier texte n’est plus utilisée.
# Les tests pertinents sont dans test_database.py (gestion SQLite) et test_audit.py (audit CSV).
