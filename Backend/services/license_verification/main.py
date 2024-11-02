from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simulate a verification function for licenses
def verify_license(file: UploadFile) -> bool:
    try:
        # Simulation : Pour le moment, on vérifie si le fichier a un certain format ou nom
        # Remplacez cette logique par la vraie vérification de la licence
        if file.filename.endswith(".pdf") or file.filename.endswith(".jpg"):
            return True
    except Exception as e:
        print(f"Error verifying license: {e}")
        return False
    return False

@app.post("/verify-license/")
async def verify_license_api(file: UploadFile = File(...)):
    is_valid = verify_license(file)
    if is_valid:
        return {"status": "valid", "message": "La licence est authentique."}
    else:
        return {"status": "invalid", "message": "La licence n'est pas valide."}
