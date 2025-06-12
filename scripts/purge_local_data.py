import os

FILES_TO_PURGE = [
    os.path.join(os.path.dirname(__file__), '../sync_local.db'),
    os.path.join(os.path.dirname(__file__), '../sync_audit.csv'),
]

def purge():
    for f in FILES_TO_PURGE:
        if os.path.exists(f):
            os.remove(f)
            print(f"Supprimé : {f}")
        else:
            print(f"Déjà absent : {f}")

if __name__ == "__main__":
    purge()
