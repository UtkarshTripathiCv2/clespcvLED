#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "jakeis";
const char* password = "Jackjack333.";

const int ledPin = 18;

WebServer server(80);

// TURN ON LED
void handleDroneOn() {
  Serial.println("🟢 Drone Present - LED ON");
  digitalWrite(ledPin, HIGH);
  server.send(200, "text/plain", "ON");
}

// TURN OFF LED
void handleDroneOff() {
  Serial.println("🔴 No Drone - LED OFF");
  digitalWrite(ledPin, LOW);
  server.send(200, "text/plain", "OFF");
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Routes
  server.on("/drone_on", handleDroneOn);
  server.on("/drone_off", handleDroneOff);

  server.begin();
}

void loop() {
  server.handleClient();
}
