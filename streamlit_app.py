import streamlit as st
import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <!-- Load p5.js from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/p5@1.4.2/lib/p5.js"></script>
    <style>
      body {
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: #000; /* Dark background for contrast */
      }
    </style>
  </head>
  <body>
    <script>
      let particles = [];
      let NUM_PARTICLES = 600;

      function setup() {
        createCanvas(windowWidth, windowHeight);
        // Generate particles around a heart shape using a parametric equation
        for (let i = 0; i < NUM_PARTICLES; i++) {
          let t = random(TWO_PI);
          let scaleFactor = random(5, 10);
          let x = scaleFactor * 16 * pow(sin(t), 3);
          let y = -scaleFactor * (13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t));
          x += width / 2;
          y += height / 2;
          particles.push(new Particle(x, y));
        }
      }

      function draw() {
        background(0, 25); 
        // Slightly transparent background creates a trailing effect
        for (let p of particles) {
          p.update();
          p.show();
        }
      }

      class Particle {
        constructor(x, y) {
          this.x = x;
          this.y = y;
          this.vx = random(-0.5, 0.5);
          this.vy = random(-0.5, 0.5);
          this.r = random(200, 255);
          this.g = 0;
          this.b = random(100, 200);
          this.alpha = 255; 
          this.size = random(2, 5);
          // Delay before fading begins (in frames)
          this.delay = int(random(60, 120));
        }

        update() {
          this.x += this.vx;
          this.y += this.vy;
          // Only start fading after the delay has elapsed
          if (this.delay > 0) {
            this.delay--;
          } else {
            this.alpha -= 1.0;
          }
          // When a particle has faded out completely, reset its properties
          if (this.alpha < 0) {
            this.alpha = 255;
            this.delay = int(random(60, 120)); // Reset delay for the new particle

            let t = random(TWO_PI);
            let scaleFactor = random(5, 10);
            this.x = scaleFactor * 16 * pow(sin(t), 3) + width / 2;
            this.y = -scaleFactor * (13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)) + height / 2;
            this.vx = random(-0.5, 0.5);
            this.vy = random(-0.5, 0.5);
          }
        }

        show() {
          noStroke();
          fill(this.r, this.g, this.b, this.alpha);
          ellipse(this.x, this.y, this.size);
        }
      }

      function windowResized() {
        resizeCanvas(windowWidth, windowHeight);
      }
    </script>
  </body>
</html>
"""

st.set_page_config(page_title="Heart Particle Animation", layout="wide")
st.title("Sparkling Heart Animation with p5.js (Initial Heart Lingers)")

components.html(html_code, height=600)
