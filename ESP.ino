#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "jakeis";
const char* password = "Jackjack333.";

const int ledPin = 18;

WebServer server(80);

// Timer variables
unsigned long ledOnTime = 0;
bool ledState = false;

void handleDroneDetected() {
  digitalWrite(ledPin, HIGH);
  ledOnTime = millis();
  ledState = true;

  server.send(200, "text/plain", "Triggered");
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

  server.on("/drone_detected", handleDroneDetected);
  server.begin();
}

void loop() {
  server.handleClient();

  // Turn OFF LED after 1 second (non-blocking)
  if (ledState && millis() - ledOnTime > 1000) {
    digitalWrite(ledPin, LOW);
    ledState = false;
  }
}
