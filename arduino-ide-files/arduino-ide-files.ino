#include <SPI.h>
#include "Adafruit_GFX.h"
#include "Adafruit_RA8875.h"

// Library only supports hardware SPI at this time
// Connect SCLK to UNO Digital #13 (Hardware SPI clock)
// Connect MISO to UNO Digital #12 (Hardware SPI MISO)
// Connect MOSI to UNO Digital #11 (Hardware SPI MOSI)
#define RA8875_INT 7
#define RA8875_CS 10
#define RA8875_RESET 9

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 480
#define SCREEN_MARGIN 50

#define BUTTON_COLS 3
#define BUTTON_ROWS 2
#define BUTTON_MARGIN 50

const int button_width = (SCREEN_WIDTH - 2*SCREEN_MARGIN - BUTTON_MARGIN * (BUTTON_COLS - 1)) / BUTTON_COLS;
const int button_height = (SCREEN_HEIGHT - 2*SCREEN_MARGIN - BUTTON_MARGIN * (BUTTON_ROWS - 1)) / BUTTON_ROWS;
int button_coords[BUTTON_ROWS][BUTTON_COLS][2];

const char button_fns[BUTTON_ROWS][BUTTON_COLS] = 
{ 
  {'A', 'B', 'C'}, 
  {'D', 'E', 'F'}
};

int button_states[BUTTON_ROWS][BUTTON_COLS];
bool pressed = false;
unsigned long last_touch = 0;


Adafruit_RA8875 tft = Adafruit_RA8875(RA8875_CS, RA8875_RESET);
uint16_t tx, ty, mx, my, x, y; // x and y are the actual coords you want here

void setup() {
  Serial.begin(115200);
  Serial.println("RA8875 start");

  /* Initialize the display using 'RA8875_480x80', 'RA8875_480x128', 'RA8875_480x272' or 'RA8875_800x480' */
  if (!tft.begin(RA8875_800x480)) {
    Serial.println("RA8875 Not Found!");
    while (1);
  }

  Serial.println("Found RA8875");

  // these are the four lines you need to make this thing turn on
  tft.displayOn(true);
  tft.GPIOX(true);      // Enable TFT - display enable tied to GPIOX
  tft.PWM1config(true, RA8875_PWM_CLK_DIV1024); // PWM output for backlight
  tft.PWM1out(255);

  tft.fillScreen(RA8875_BLACK);
  init_buttons();

  pinMode(RA8875_INT, INPUT);
  digitalWrite(RA8875_INT, HIGH);
  
  mx = tft.width();
  my = tft.height();

  tft.touchEnable(true);

  Serial.print("Status: "); Serial.println(tft.readStatus(), HEX);
  Serial.println("Waiting for touch events ...");
}

void loop() {
  poll_buttons();
}


/**
 * Calculate button coords & draw to screen
 * 
 * For each button, calculate the x & y coords for the top left corner, then draw a white rectangle
 * to represent the button onscreen.
 */
void init_buttons() {
  for (int i = 0; i < BUTTON_ROWS; i++) {
    int button_y = SCREEN_MARGIN + i*(BUTTON_MARGIN+button_height);
    for (int j = 0; j < BUTTON_COLS; j++) {
      int button_x = SCREEN_MARGIN + j*(BUTTON_MARGIN+button_width);
      button_coords[i][j][0] = button_x;
      button_coords[i][j][1] = button_y;
      tft.fillRect(button_coords[i][j][0], button_coords[i][j][1], button_width, button_height, RA8875_WHITE);
    }
  }
}

void button_press(int x, int y) {
  Serial.println("+" + String(button_fns[x][y]));
  tft.fillRect(button_coords[x][y][0], button_coords[x][y][1], button_width, button_height, RA8875_BLUE);
}

void button_unpress(int x, int y) {
  Serial.println("-" + String(button_fns[x][y]));
  tft.fillRect(button_coords[x][y][0], button_coords[x][y][1], button_width, button_height, RA8875_WHITE);
}



void poll_buttons() {

  // if touch report available, read & handle
  if (!digitalRead(RA8875_INT)) {
    if (tft.touched()) {
      tft.touchRead(&tx, &ty);
      x = map(tx, 50, 970, 0, mx);
      y = map(ty, 140, 930, 0, my);
      
      // check if touch is on any button
      for (int i = 0; i < BUTTON_ROWS; i++) {
        for (int j = 0; j < BUTTON_COLS; j++) {
          if (button_coords[i][j][0] <= x && x <= (button_coords[i][j][0] + button_width) && button_coords[i][j][1] <= y && y <= (button_coords[i][j][1] + button_height)) {
            // if button touched, increment state counter; 5 reports trigger button
            if (button_states[i][j] == 5) {
              button_press(i, j);
              button_states[i][j]++;
            } else if (button_states[i][j] < 5) {
              button_states[i][j]++;
            }
            // any given touch report can only be on one button, so once we find it we can stop checking
            goto loop_breakout; // https://xkcd.com/292/
          } 
        }
      }
loop_breakout:
      // reset touch timeout watchdog
      last_touch = millis();
    }

    // if no touch report, check timeout and unpress buttons if elapsed - kind of a makeshift watchdog
  } else if ((millis() - last_touch) > 100) {
    for (int i = 0; i < BUTTON_ROWS; i++) {
      for (int j = 0; j < BUTTON_COLS; j++) {
        // if button pressed, unpress
        if (button_states[i][j] > 5) {
          button_unpress(i,j);
        }
        // reset button counters regardless
        button_states[i][j] = 0;
      }
    }
    last_touch = millis();
  }
}
