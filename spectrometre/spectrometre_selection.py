import os
import platform
# On désactive les warnings de Qt AVANT tout import de cv2 ou matplotlib #Problème de management de THreade, ça pollue la console
os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.warning=false"
os.environ["QT_QPA_PLATFORM"] = "xcb"

import cv2
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from cv2_enumerate_cameras import enumerate_cameras


def select_webcam():
    #Personnalise le backend en fonction du système
    system = platform.system()
    backend = cv2.CAP_MSMF #Cas de base pour Windows
    if system == "Linux":
        backend = cv2.CAP_V4L2
    if system == "Darwin": #Mac
        backend = cv2.CAP_AVFOUNDATION

    print("Listes des caméras disponibles")
    cams = enumerate_cameras(backend) #On énumère toute les cameras
    cam = -1
    for i in range(len(cams)) : #On propose les choix de caméra à l'utilisateur
        print(f"{i+1} - {cams[i].name}")

    while cam == -1:
        prop = int(input("Quel caméra voulez vous utiliser ? (mettre le chiffre) : "))  #On demande quel caméra il veut utiliser
        if prop-1 in range(len(cams)): #Si la proposition est valide
            cam=prop-1 
        else:
            print("Proposition non valide.")
    print("\n")
    return cams[cam].index


def main():

    cam = select_webcam() 
    cap = cv2.VideoCapture(cam) #On selectionne la Webcam

    # Vérification que la caméra est ouverte
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la caméra.")
        return

    roi_selected = False
    r = None # On initialise la zone ROI
    cropped = None
    image_fix = None

    print("Contrôles :")
    print("'r' : Sélectionner une zone (ROI) -> Appuyez sur ENTRÉE pour valider")
    print("'s' : Analyser la zone sélectionnée (Graphique)")
    print("'q' : Retour en arrière / Quitter")

    while True:
        ret, frame = cap.read() 
        frame = cv2.flip(frame, 1)

        if not ret:
            break
        
        # Masque binaire pour récupérer le code ASCII correct de la touche appuyé (nécessaire sur certains OS)
        k = cv2.waitKey(1) & 0xFF
        
        # Si une ROI est active, on découpe l'image courante
        if roi_selected and r is not None:
            # r = (x, y, w, h)
            cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        # --- GESTION DES TOUCHES ---

        if k == ord("s"):
            if roi_selected and cropped is not None and cropped.size > 0: #Si on a une ROI bien défini
                print("Analyse en cours...")
                
                
                cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB) #On doit convertir les couleurs de BGR (opencv) vers RGB ()
                #Calcul des moyennes par colonne
                
                means = np.mean(cropped_rgb, axis=0) # axis=0 calcule la moyenne verticale pour chaque colonne 
                
                r_dist = means[:, 0] # Rouge
                g_dist = means[:, 1] # Vert
                b_dist = means[:, 2] # Bleu
                i_dist = np.mean(means, axis=1) # Intensité moyenne

                #Affichage Matplotlib
                plt.figure(figsize=(10, 8))
                
                plt.subplot(2, 1, 1)
                plt.title("Zone sélectionnée (RGB)")
                plt.imshow(cropped_rgb)
                plt.axis('off')

                plt.subplot(2, 1, 2)
                plt.title("Profil colorimétrique moyen par colonne")
                plt.plot(r_dist, color='r', label='Rouge') #Courbe du rouge
                plt.plot(g_dist, color='g', label='Vert') #Courbe du Vert
                plt.plot(b_dist, color='b', label='Bleu') #COurbe du bleu
                plt.plot(i_dist, color='k', linestyle='--', label='Intensité')
                plt.legend(loc="upper right")
                plt.xlabel("Pixels (Largeur)")
                plt.ylabel("Valeur moyenne (0-255)")
                print("Fermez la fenetre pour relancer la vidéo")
                plt.show() 
                roi_selected = False #Une fois l'analyse terminé, je reviens à la phase de sélection.
                cropped = None
                image_fix = None
            else:
               print("Veuillez d'abord sélectionner une ROI avec 'r'.")
        elif k == ord('q'): 
            if roi_selected and cropped is not None: # SI je suis dans une zone figé, je reviens juste à l'image complète
                roi_selected = False
                cropped = None
                image_fix = None
            else:
                break #On arrete la boucle while
        elif k == ord('r'):
            # selectROI bloque le script jusqu'à ce que la sélection soit faite + Entrée ou espace
            print("Sélectionnez une zone et appuyez sur ENTRÉE (ou ESPACE).")
            r = cv2.selectROI("Selection", frame, showCrosshair=True, fromCenter=False, printNotice=False)
            cv2.destroyWindow("Selection") # Ferme la fenêtre statique de sélection
            
            # Vérification que la sélection n'est pas vide (w=0 ou h=0)
            if r[2] > 0 and r[3] > 0:
                roi_selected = True
                image_fix = frame
                print(r)
                cropped = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                print(f"ROI sélectionnée : {r}")
            else:
                image_fix = None
                roi_selected = False
                print("Sélection annulée ou invalide.")
            
        
        # --- AFFICHAGE ---
        if roi_selected and cropped is not None:
            # On affiche juste la zone découpée figé
            cv2.imshow('Flux Video', cropped)
        else:
            # On affiche toute la caméra en direct
            cv2.imshow('Flux Video', frame)
    cap.release()
    cv2.destroyAllWindows() #On termine le programme et on supprime les fenêtres

if __name__ == '__main__':
    main()