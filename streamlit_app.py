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

      // Global delay (in frames) before morphing starts (e.g., 180 frames ~3s at 60fps)
      let globalDelay = 180;

      // Morph progress goes from 0 (heart) to 1 (pig head).
      let morphProgress = 0;

      function setup() {
        createCanvas(windowWidth, windowHeight);

        for (let i = 0; i < NUM_PARTICLES; i++) {
          // 1) Heart shape (initial position)
          let t = random(TWO_PI);
          let scaleFactor = random(5, 10);
          let heartX = scaleFactor * 16 * pow(sin(t), 3) + width / 2;
          let heartY = -scaleFactor * (
            13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
          ) + height / 2;

          // 2) Pig head shape (target position)
          //    Approximate the pig head with 4 circles:
          //      - main head (70%)
          //      - left ear (10%)
          //      - right ear (10%)
          //      - nose (10%)
          let assign = random();
          let targetX, targetY;

          if (assign < 0.7) {
            // Main face circle
            let angle = random(TWO_PI);
            let r = random(0, 80);
            targetX = width / 2 + r * cos(angle);
            targetY = height / 2 + r * sin(angle);
          } else if (assign < 0.8) {
            // Left ear
            let angle = random(TWO_PI);
            let r = random(0, 20);
            targetX = (width / 2 - 50) + r * cos(angle);
            targetY = (height / 2 - 80) + r * sin(angle);
          } else if (assign < 0.9) {
            // Right ear
            let angle = random(TWO_PI);
            let r = random(0, 20);
            targetX = (width / 2 + 50) + r * cos(angle);
            targetY = (height / 2 - 80) + r * sin(angle);
          } else {
            // Nose
            let angle = random(TWO_PI);
            let r = random(0, 15);
            targetX = (width / 2) + r * cos(angle);
            targetY = (height / 2 + 20) + r * sin(angle);
          }

          particles.push(new Particle(heartX, heartY, targetX, targetY));
        }
      }

      function draw() {
        // Slightly transparent background for a trailing effect
        background(0, 25);

        // Keep the heart static until the global delay finishes
        if (globalDelay > 0) {
          globalDelay--;
        } else {
          // Once delay is over, gradually move morphProgress toward 1
          if (morphProgress < 1) {
            morphProgress += 0.005; // Controls the speed of the morph
            morphProgress = min(morphProgress, 1);
          }
        }

        // Update and display each particle
        for (let p of particles) {
          p.update(morphProgress);
          p.show();
        }
      }

      class Particle {
        constructor(heartX, heartY, targetX, targetY) {
          // Initial heart position
          this.heartX = heartX;
          this.heartY = heartY;
          // Target pig head position
          this.targetX = targetX;
          this.targetY = targetY;

          // Current position starts at the heart position
          this.currentX = heartX;
          this.currentY = heartY;

          // Color: random red/pink tones
          this.r = random(200, 255);
          this.g = 0;
          this.b = random(100, 200);
          this.alpha = 255;
          this.size = random(2, 5);
        }

        update(morphProgress) {
          // Linear interpolation between heart position and pig head position
          this.currentX = lerp(this.heartX, this.targetX, morphProgress);
          this.currentY = lerp(this.heartY, this.targetY, morphProgress);

          // Once fully morphed, add a tiny drift so it's not perfectly static
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

st.set_page_config(page_title="Morphing Heart to Cartoon Pig", layout="wide")
st.title("从爱心到卡通猪头的粒子动画 (Heart → Pig)")

# Embed the p5.js sketch in the Streamlit app
components.html(html_code, height=600)
