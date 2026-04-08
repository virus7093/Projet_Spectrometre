// setup pour initialiser la carte

#define led_B 2;


int eclairage = 0;
bool p_o_m = true;

void setup() { // début du setup
  
pinMode(led_B, OUTPUT) ; // initialise le port numérique 2 comme sortie

} // fin du setup


// cette boucle va se répéter sans arrêt
void loop() { // début de la boucle
  analogWrite(led_B, eclairage)
  if ( p_o_m ) {
    eclairage = eclairage + 10;
    if (eclairage >= 255 ) {
      eclairage = 255;
      p_o_m = false;
    }
  }
  else { 
    eclairage = eclairage - 10
    if ( eclairage <= 0 ) {
      eclairage = 0
      p_o_m = true;
    }
    }
}
