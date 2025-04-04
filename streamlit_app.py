import streamlit as st
import streamlit.components.v1 as components

# Embed p5.js code in an HTML string
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
        background: #000; /* Dark background to highlight the particles */
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
          // 'scale' controls the size of the heart
          let scale = random(5, 10); 
          let x = scale * 16 * pow(sin(t), 3);
          let y = -scale * (
            13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
          );
          // Center them on screen
          x += width / 2;
          y += height / 2;

          particles.push(new Particle(x, y));
        }
      }

      function draw() {
        background(0, 25); 
        // Slightly transparent background for trailing effect
        for (let p of particles) {
          p.update();
          p.show();
        }
      }

      class Particle {
        constructor(x, y) {
          this.x = x;
          this.y = y;
          // Give each particle a small random velocity
          this.vx = random(-0.5, 0.5);
          this.vy = random(-0.5, 0.5);
          // Particle color: random shades of red/pink
          this.r = random(200, 255);
          this.g = 0;
          this.b = random(100, 200);
          this.alpha = 255; 
          this.size = random(2, 5);
        }

        update() {
          this.x += this.vx;
          this.y += this.vy;
          // Fade out gradually
          this.alpha -= 1.0; 
          // If particle becomes invisible, reset it to a new position in the heart
          if (this.alpha < 0) {
            this.alpha = 255;
            let t = random(TWO_PI);
            let scale = random(5, 10);
            this.x = scale * 16 * pow(sin(t), 3) + width / 2;
            this.y = -scale * (
              13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
            ) + height / 2;
            // Random velocity again
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
st.title("Sparkling Heart Animation with p5.js")

# Display the p5.js code as a component in Streamlit
components.html(html_code, height=600)
