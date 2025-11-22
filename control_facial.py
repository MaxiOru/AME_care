import cv2
import mediapipe as mp
import pyautogui
import time
import math
import numpy as np

# --- CONFIGURACIÓN DE CALIBRACIÓN ---
SENSIBILIDAD = 5.0        
SUAVIZADO = 0.2          
ZONA_MUERTA = 3           

# 1. CLICK (Ratio del Ojo) -> MENOS es más cerrado
# OJO: Mira el valor en pantalla. Si parpadeas y baja a 0.20, pon esto en 0.22
UMBRAL_EAR_CLICK = 0.23   
TIEMPO_PARA_CLICK = 0.3   

# 2. SCROLL (Cejas) -> MÁS es más levantado
# Mira el valor en pantalla. Si sorprendido sube a 0.05, pon esto en 0.045
MARGEN_SCROLL = 80        # Qué tan cerca del borde debes estar para activar scroll
VELOCIDAD_SCROLL = 15     # Velocidad BAJA para tener control total
TIEMPO_ENTRE_SCROLLS = 0.05 # Pausa técnica para que no se acelere

# 3. EMERGENCIA (Boca) -> MÁS es más abierto
UMBRAL_BOCA = 0.50          # Ratio ancho/alto de la boca
TIEMPO_EMERGENCIA = 1.5   

# Configuración Técnica
pyautogui.FAILSAFE = False
ancho_pant, alto_pant = pyautogui.size()
prev_x, prev_y = 0, 0

# Inicializar MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True, 
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

camara = cv2.VideoCapture(0)

# Estados
inicio_guiño = 0
inicio_boca = 0
ultimo_scroll = 0
click_hecho = False

def calcular_distancia(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def calcular_ear_ojo(mesh, p_arriba, p_abajo, p_izq, p_der):
    # Eye Aspect Ratio: Altura / Ancho
    # Si cierras el ojo, la altura es casi 0, el ratio baja.
    altura = calcular_distancia(mesh[p_arriba], mesh[p_abajo])
    ancho = calcular_distancia(mesh[p_izq], mesh[p_der])
    return altura / ancho

def calcular_ratio_boca(mesh):
    # Altura (labio sup/inf) / Ancho (comisuras)
    altura = calcular_distancia(mesh[13], mesh[14])
    ancho = calcular_distancia(mesh[61], mesh[291])
    return altura / ancho

print(">>> IRON MAN 5.0 ACTIVO")

while True:
    ret, frame = camara.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h_img, w_img, _ = frame.shape
    
    results = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks:
        mesh = results.multi_face_landmarks[0].landmark
        
        # --- 1. MOUSE (ESTABILIZADO) ---
        nariz = mesh[4]
        cx, cy = nariz.x - 0.5, nariz.y - 0.5
        target_x = (ancho_pant/2) + (cx * ancho_pant * SENSIBILIDAD)
        target_y = (alto_pant/2) + (cy * alto_pant * SENSIBILIDAD)
        
        # Zona muerta
        if math.hypot(target_x - prev_x, target_y - prev_y) < ZONA_MUERTA:
            target_x, target_y = prev_x, prev_y
            
        # Suavizado
        curr_x = prev_x + (target_x - prev_x) * SUAVIZADO
        curr_y = prev_y + (target_y - prev_y) * SUAVIZADO
        
        # Limitar a pantalla
        curr_x = max(0, min(curr_x, ancho_pant))
        curr_y = max(0, min(curr_y, alto_pant))
        
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        # --- 2. CLICK(EAR) ---
        # Puntos del ojo izquierdo (arriba, abajo, interior, exterior)
        ear = calcular_ear_ojo(mesh, 159, 145, 33, 133)
        
        # Mostrar valor para calibrar
        color_ojo = (0, 255, 0) if ear < UMBRAL_EAR_CLICK else (255, 255, 255)
        cv2.putText(frame, f"CLICK (EAR): {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_ojo, 2)

        if ear < UMBRAL_EAR_CLICK:
            if inicio_guiño == 0: inicio_guiño = time.time()
            
            duracion = time.time() - inicio_guiño
            # Feedback visual carga
            cv2.circle(frame, (w_img//2, h_img//2), int(10+duracion*100), (0,255,255), 2)
            
            if duracion > TIEMPO_PARA_CLICK and not click_hecho:
                pyautogui.click()
                print(">>> CLICK ✅")
                click_hecho = True
                cv2.circle(frame, (w_img//2, h_img//2), 60, (0,255,0), -1)
        else:
            inicio_guiño = 0
            click_hecho = False

# --- 2. SCROLL CONTROLADO  ---
        # Dibujar líneas guía en la cámara
        cv2.line(frame, (0, 100), (w_img, 100), (255, 0, 0), 1) # Línea Azul Arriba
        cv2.line(frame, (0, h_img - 100), (w_img, h_img - 100), (0, 0, 255), 1) # Línea Roja Abajo

        tiempo_actual = time.time()
        
        # Solo hacemos scroll si pasó el tiempo de espera (freno)
        if tiempo_actual - ultimo_scroll > TIEMPO_ENTRE_SCROLLS:
            # SUBIR (Zona Azul)
            if curr_y < MARGEN_SCROLL:
                pyautogui.scroll(VELOCIDAD_SCROLL)
                ultimo_scroll = tiempo_actual
                cv2.circle(frame, (w_img//2, 50), 20, (255,0,0), -1)
                cv2.putText(frame, "SUBIENDO", (w_img//2 + 30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
                
            # BAJAR (Zona Roja)
            elif curr_y > alto_pant - MARGEN_SCROLL:
                pyautogui.scroll(-VELOCIDAD_SCROLL)
                ultimo_scroll = tiempo_actual
                cv2.circle(frame, (w_img//2, h_img-50), 20, (0,0,255), -1)
                cv2.putText(frame, "BAJANDO", (w_img//2 + 30, h_img-50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        # --- 4. EMERGENCIA (BOCA + TECLA 'E') ---
        ratio_boca = calcular_ratio_boca(mesh)
        
        if ratio_boca > UMBRAL_BOCA:
            if inicio_boca == 0: inicio_boca = time.time()
            duracion = time.time() - inicio_boca
            progreso = min(duracion/TIEMPO_EMERGENCIA, 1.0)
            
            cv2.rectangle(frame, (50, h_img-50), (int(50 + 200*progreso), h_img-20), (0,0,255), -1)
            cv2.putText(frame, "EMERGENCIA...", (50, h_img-60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

            if duracion > TIEMPO_EMERGENCIA:
                print(">>> 🚨 ENVIO SEÑAL EMERGENCIA 🚨")
                pyautogui.press('e') # Presiona la tecla E que escucha el JS
                inicio_boca = time.time() + 3.0 # Pausa larga
        else:
            inicio_boca = 0

    cv2.imshow('Calibracion Iron Man', frame)
    if cv2.waitKey(1) & 0xFF == 27: break

camara.release()
cv2.destroyAllWindows()