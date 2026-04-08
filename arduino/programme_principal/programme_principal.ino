// setup pour initialiser la carte

#define led_B 3

#define led_G 5

#define led_R 6

#define bouton 2


int couleur = 0; //Correspond au mode de lumière (quel couleur)


void setup() { // début du setup
  
pinMode(led_B, OUTPUT) ; // initialise le port numérique led_B comme sortie
pinMode(led_G, OUTPUT) ; // initialise le port numérique led_G comme sortie
pinMode(led_R, OUTPUT) ; // initialise le port numérique led_R comme sortie
pinMode(bouton, INPUT); // initialise le port numérique bouton comme entrée

arbitrage_couleur(couleur); //Initialise la couleur de la led
} // fin du setup


// cette boucle va se répéter sans arrêt
void loop() { // début de la boucle

  if (digitalRead(bouton) == HIGH) {
    couleur= couleur + 1; // On passe au prochain mode
    if (couleur == 7) { // Si on dépasse le nombre de mode de couleur prédéfini, on retourne au premier
      couleur = 0;
    }
    
    arbitrage_couleur(couleur); // Actualise la led
    delay(800); //Delai de 1 secondes pour avoir un switch de couleur fiable
  }

}

void arbitrage_couleur(int col) {
  if (col == 0) {  // Allumer la LED en rouge
    setColor(130, 0, 0);
  }

  if (col == 1) {  // Allumer la LED en vert
    setColor(0, 130, 0);
  }
  if (col == 2) {  // Allumer la LED en bleu
    setColor(0, 0, 150);
  }
  if (col == 3) {  // Allumer la LED en jaune
    setColor(130, 130, 0);
  }
  if (col == 4) {  // Allumer la LED en violet
    setColor(130, 0, 150);
  }
  if (col == 5) {  // Allumer la LED en cyan
    setColor(0, 130, 150);
  }
  if (col == 6) {  // Allumer la LED en blanc
    setColor(130, 130, 150);
  }
}

void setColor(int redValue, int greenValue, int blueValue) {
  // Régler l'intensité lumineuse de chaque couleur
  analogWrite(led_R, redValue);
  analogWrite(led_G, greenValue);
  analogWrite(led_B, blueValue);
}
