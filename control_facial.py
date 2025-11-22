import cv2
import pyautogui
import os
import time  # Necesario para controlar el tiempo entre clicks

# --- CONFIGURACIÓN DEL HACKER ---
SUAVIZADO = 0.13 # (0.1 = Muy suave/lento, 0.9 = Rápido/tembloroso). Juega con esto.
SENSIBILIDAD_X = 4.5   # Multiplicador ancho (aumenta si no llegas a los lados)
SENSIBILIDAD_Y = 4.5   # Multiplicador alto (aumenta si no llegas arriba/abajo)
COOLDOWN_CLICK = 1.0   # Segundos de espera después de un click (para que no se pegue)

# Configuración técnica
pyautogui.FAILSAFE = False
ancho_pantalla, alto_pantalla = pyautogui.size()
pyautogui.PAUSE = 0    # Hace que el mouse se mueva más fluido

# Variables de estado (Memoria del programa)
prev_x, prev_y = 0, 0  # Recordamos dónde estaba el mouse antes
ultimo_tiempo_click = 0

# Cargar cerebro
cascade_path = 'haarcascade_frontalface_default.xml'
if not os.path.exists(cascade_path):
    print("ERROR: Falta el archivo XML.")
    exit()

face_cascade = cv2.CascadeClassifier(cascade_path)
camara = cv2.VideoCapture(0)

print(">>> CONTROL 2.0 INICIADO")
print(">>> Usa BARRA ESPACIADORA para click.")

while True:
    ret, frame = camara.read()
    if not ret: break
    
    # Espejo y procesado
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar cara
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    # Obtener dimensiones de cámara
    cam_alto, cam_ancho = frame.shape[:2]
    centro_cam_x = cam_ancho // 2
    centro_cam_y = cam_alto // 2

    for (x, y, w, h) in faces:
        # Dibujar referencia visual
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
        
        # 1. Calcular centro crudo de la cara
        raw_x = x + w // 2
        raw_y = y + h // 2
        
        # 2. Calcular distancia desde el centro (Joystick)
        delta_x = raw_x - centro_cam_x
        delta_y = raw_y - centro_cam_y
        
        # 3. Mapeo a pantalla con SENSIBILIDAD (Solución a "No llega a esquinas")
        target_x = (ancho_pantalla // 2) + (delta_x * (ancho_pantalla / cam_ancho) * SENSIBILIDAD_X)
        target_y = (alto_pantalla // 2) + (delta_y * (alto_pantalla / cam_alto) * SENSIBILIDAD_Y)
        
        # 4. Limitar a bordes de pantalla
        target_x = max(0, min(target_x, ancho_pantalla))
        target_y = max(0, min(target_y, alto_pantalla))
        
        # 5. SUAVIZADO (Solución a "Tiembla mucho")
        # Fórmula: Posición Actual = (Un poco de la nueva) + (Mucho de la vieja)
        curr_x = prev_x + (target_x - prev_x) * SUAVIZADO
        curr_y = prev_y + (target_y - prev_y) * SUAVIZADO
        
        # Mover mouse
        pyautogui.moveTo(curr_x, curr_y)
        
        # Actualizar memoria para el siguiente cuadro
        prev_x, prev_y = curr_x, curr_y

    # Mostrar ventana (hazla pequeña para que no moleste)
    cv2.imshow('Control', frame)
    
    # Captura de teclas
    key = cv2.waitKey(1) & 0xFF
    
    # --- LÓGICA DE CLICK MEJORADA (Solución a "Click Pegado") ---
    if key == 32: # Barra Espaciadora
        tiempo_actual = time.time()
        
        # Solo permitimos click si pasó el tiempo de COOLDOWN
        if tiempo_actual - ultimo_tiempo_click > COOLDOWN_CLICK:
            pyautogui.click()
            print("CLICK EJECUTADO ✅")
            ultimo_tiempo_click = tiempo_actual
        else:
            print("Click bloqueado por enfriamiento ⏳")
            
    elif key == 27: # ESC
        break

camara.release()
cv2.destroyAllWindows()