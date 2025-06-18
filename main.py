from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI(title="Image Processing API", version="1.0")

@app.post("/procesar-imagen")
async def procesar_imagen(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    # Leer el contenido del archivo
    imagen_bytes = await file.read()

    try:
        # Abrir imagen desde los bytes
        imagen = Image.open(io.BytesIO(imagen_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al abrir la imagen: {e}")

    # Procesar imagen: convertir a escala de grises
    imagen_gris = imagen.convert("L")

    # Guardar la imagen procesada en un buffer
    buffer = io.BytesIO()
    imagen_gris.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")

@app.get("/ping")
def ping():
    return {"mensaje": "Servidor activo"}
