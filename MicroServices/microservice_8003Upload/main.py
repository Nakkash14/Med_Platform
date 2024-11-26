
from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import shutil
from fastapi.staticfiles import StaticFiles

# Ajout du middleware pour servir les fichiers statiques


# Configuration de l'application FastAPI
app = FastAPI()

# Configuration des templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
# Répertoires pour les fichiers
UPLOAD_DIR_IMAGES = "uploads/images"
UPLOAD_DIR_DOCUMENTS = "uploads/documents"
MAX_FILES = 2

os.makedirs(UPLOAD_DIR_IMAGES, exist_ok=True)
os.makedirs(UPLOAD_DIR_DOCUMENTS, exist_ok=True)

# Endpoint pour afficher la page de téléversement
@app.get("/", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

# Endpoint pour téléverser un fichier
@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...), file_type: str = Form(...)):
    # Vérifier le type de fichier
    if file_type not in ["image", "document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Choose 'image' or 'document'.")

    # Déterminer le répertoire cible
    upload_dir = UPLOAD_DIR_IMAGES if file_type == "image" else UPLOAD_DIR_DOCUMENTS

    # Vérifier le nombre de fichiers existants
    existing_files = os.listdir(upload_dir)
    if len(existing_files) >= MAX_FILES:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum file limit ({MAX_FILES}) reached for {file_type}s."
        )

    # Sauvegarder le fichier
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"{file_type.capitalize()} uploaded successfully.", "file_path": file_path}

# Endpoint pour lister les fichiers téléversés
@app.get("/list-files")
async def list_files(type: str):
    # Vérifier le type de fichier
    if type not in ["image", "document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Choose 'image' or 'document'.")

    # Déterminer le répertoire cible
    upload_dir = UPLOAD_DIR_IMAGES if type == "image" else UPLOAD_DIR_DOCUMENTS
    files = os.listdir(upload_dir)

    return {"file_type": type, "files": files}
