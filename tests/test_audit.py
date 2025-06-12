import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.helpers import log_audit, AUDIT_LOG
import csv
import tempfile
from datetime import datetime

def test_log_audit():
    with tempfile.TemporaryDirectory() as tmpdir:
        audit_file = os.path.join(tmpdir, 'sync_audit.csv')
        # Patch le chemin du log d’audit
        import utils.helpers as helpers
        helpers.AUDIT_LOG = audit_file
        log_audit('order-1', 'success', 'Test OK')
        log_audit('order-2', 'error', 'Erreur de test')
        with open(audit_file, newline='') as f:
            rows = list(csv.reader(f))
            assert len(rows) == 2
            assert rows[0][1] == 'order-1'
            assert rows[0][2] == 'success'
            assert rows[1][1] == 'order-2'
            assert rows[1][2] == 'error'
