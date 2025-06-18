from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
from skimage import io, measure, color,filters
import numpy as np
import cv2

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
    # imagen_gris = imagen.convert("L")
#---------------------------
    # image = cv2.imread('../imagenes/Habitacion2.jpg')
    image=imagen
    gray_image= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    _,binarizada=cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV)
    labels = measure.label(binarizada ,connectivity=1)
    borders = np.max(labels)

    border_muestra = 1618

    if borders >= border_muestra-5 and borders <= border_muestra+5 :
        print(f"La imagen tiene {borders} bordes, lo cual significa que la habitacion esta limpia")
    else:
        print(f"La imagen tiene {borders} bordes, lo cual significa que la habitacion esta desordenada")

#---------------------------


    # Guardar la imagen procesada en un buffer
    buffer = io.BytesIO()
    gray_image.save(buffer, format="PNG")
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/ping")
def ping():
    return {"mensaje": "Servidor activo"}
