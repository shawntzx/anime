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
      const NUM_PARTICLES = 600;
      // Global delay (in frames) before morphing starts (e.g., 180 frames ~3 seconds at 60fps)
      let globalDelay = 180;
      // Morph progress goes from 0 (heart) to 1 (pig head)
      let morphProgress = 0;

      function setup() {
        createCanvas(windowWidth, windowHeight);
        // Generate particles with two sets of coordinates:
        // - heartX, heartY: initial heart shape positions
        // - targetX, targetY: target positions for the pig head shape
        for (let i = 0; i < NUM_PARTICLES; i++) {
          // Compute heart shape position using the parametric equation
          let t = random(TWO_PI);
          let scaleFactor = random(5, 10);
          let heartX = scaleFactor * 16 * pow(sin(t), 3) + width / 2;
          let heartY = -scaleFactor * (13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)) + height / 2;
          
          // Compute pig head target position:
          // We assign approximately 70% of particles to the main head circle,
          // 15% to the left ear, and 15% to the right ear.
          let assign = random();
          let targetX, targetY;
          if (assign < 0.7) {
            // Main head circle (centered at canvas center, radius ~80)
            let angle = random(TWO_PI);
            let r = random(0, 80);
            targetX = width / 2 + r * cos(angle);
            targetY = height / 2 + r * sin(angle);
          } else if (assign < 0.85) {
            // Left ear circle (centered to the left and above the main head)
            let angle = random(TWO_PI);
            let r = random(0, 20);
            targetX = width / 2 - 50 + r * cos(angle);
            targetY = height / 2 - 80 + r * sin(angle);
          } else {
            // Right ear circle (centered to the right and above the main head)
            let angle = random(TWO_PI);
            let r = random(0, 20);
            targetX = width / 2 + 50 + r * cos(angle);
            targetY = height / 2 - 80 + r * sin(angle);
          }
          
          particles.push(new Particle(heartX, heartY, targetX, targetY));
        }
      }

      function draw() {
        // A slightly transparent background creates a trailing effect.
        background(0, 25);
        
        // After the global delay, start morphing from heart to pig head.
        if (globalDelay > 0) {
          globalDelay--;
        } else {
          if (morphProgress < 1) {
            morphProgress += 0.005;  // Adjust the speed of the morph here.
            if (morphProgress > 1) {
              morphProgress = 1;
            }
          }
        }
        
        // Update and display each particle.
        for (let p of particles) {
          p.update(morphProgress);
          p.show();
        }
      }

      // Particle class holds both heart (initial) and pig head (target) positions.
      class Particle {
        constructor(heartX, heartY, targetX, targetY) {
          this.heartX = heartX;
          this.heartY = heartY;
          this.targetX = targetX;
          this.targetY = targetY;
          // Current position starts at the heart position.
          this.currentX = heartX;
          this.currentY = heartY;
          // Color: random red/pink tones.
          this.r = random(200, 255);
          this.g = 0;
          this.b = random(100, 200);
          this.alpha = 255;
          this.size = random(2, 5);
        }

        // Update current position based on morph progress.
        update(morphProgress) {
          // Linear interpolation between heart and pig head positions.
          this.currentX = lerp(this.heartX, this.targetX, morphProgress);
          this.currentY = lerp(this.heartY, this.targetY, morphProgress);
          // Optionally, once the morph is complete, add a gentle drift.
          if (morphProgress >= 1) {
            this.currentX += random(-0.5, 0.5);
            this.currentY += random(-0.5, 0.5);
          }
        }

        show() {
          noStroke();
          fill(this.r, this.g, this.b, this.alpha);
          ellipse(this.currentX, this.currentY, this.size);
        }
      }

      function windowResized() {
        resizeCanvas(windowWidth, windowHeight);
      }
    </script>
  </body>
</html>
"""

st.set_page_config(page_title="Morphing Heart to Pig Head", layout="wide")
st.title("Morph from Heart to 卡通猪头")

# Embed the p5.js sketch in the Streamlit app.
components.html(html_code, height=600)
