from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
from skimage import io, measure, color,filters
import numpy as np
import cv2
from modules import dbconnection

app = FastAPI(title="Image Processing API", version="1.0")

@app.post("/procesar-imagen")
async def procesar_imagen(
    id: int = Form(...),
    file: UploadFile = File(...)
  ):
    if not file.content_type.startswith("image/"):
        print("El archivo debe ser una imagen")
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    imagen_bytes = await file.read()

    try:
        imagen = Image.open(io.BytesIO(imagen_bytes))
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        raise HTTPException(status_code=400, detail=f"Error al abrir la imagen: {e}")

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
        """
        try:
            conn = await dbconnection.get_db_connection()
            await conn.execute(
                UPDATE "imagen-pdi"
                SET idEstado = 2
                WHERE id = $1
            , id)  
            await conn.close()
        except Exception as e:
            print(f"Error al actualizar la base de datos: {e}")
        """
    buffer = io.BytesIO()
    gray_image.save(buffer, format="PNG")
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/ping")
def ping():
    return {"mensaje": "Servidor activo"}
