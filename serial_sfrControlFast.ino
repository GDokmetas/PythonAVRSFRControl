
void setup() {
Serial.begin(115200);
}

void loop() {
while(Serial.available() == 0) {}
delay(1);
unsigned char rw = Serial.read();
unsigned char *ptr = Serial.read();
unsigned char val = Serial.read();
if(rw == 0)
{
  Serial.write(*ptr);
}

if(rw == 1)
{
  *ptr = val;
}

}
