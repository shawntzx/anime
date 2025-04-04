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
      const NUM_PARTICLES = 800;  // Increase for a denser look

      // Global delay (in frames) before morphing starts (e.g., 180 frames ~3s at 60fps)
      let globalDelay = 180;

      // Morph progress goes from 0 (heart) to 1 (cartoon pig).
      let morphProgress = 0;

      function setup() {
        createCanvas(windowWidth, windowHeight);

        for (let i = 0; i < NUM_PARTICLES; i++) {
          // 1) HEART SHAPE (initial position)
          let t = random(TWO_PI);
          let scaleFactor = random(5, 10);
          let heartX = scaleFactor * 16 * pow(sin(t), 3) + width / 2;
          let heartY = -scaleFactor * (
            13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
          ) + height / 2;

          // 2) CARTOON PIG SHAPE (target position + color)
          // We break the pig into multiple ellipses:
          //   - Face, Ears, Eyes, Nose, Cheeks
          // Each particle randomly goes to one "region" with its own color.
          // Adjust distribution (percentages) and ellipse sizes to match your style.

          let shapeRand = random();
          let targetX, targetY;
          let cR, cG, cB; // color for this particle

          // Canvas center
          let cx = width / 2;
          let cy = height / 2;

          // A helper function: random point inside an ellipse
          function randomPointInEllipse(centerX, centerY, rx, ry) {
            let angle = random(TWO_PI);
            let r = sqrt(random(1));  // uniform distribution in circle
            let x = r * cos(angle) * rx;
            let y = r * sin(angle) * ry;
            return [centerX + x, centerY + y];
          }

          if (shapeRand < 0.60) {
            // Face (~60% of particles)
            let [x, y] = randomPointInEllipse(cx, cy, 80, 70);
            targetX = x;
            targetY = y;
            // Light pink face
            cR = 255; 
            cG = 185; 
            cB = 200;
          } else if (shapeRand < 0.70) {
            // Left Ear (~10%)
            let [x, y] = randomPointInEllipse(cx - 55, cy - 70, 20, 25);
            targetX = x;
            targetY = y;
            // Slightly darker pink for ears
            cR = 255; 
            cG = 150; 
            cB = 200;
          } else if (shapeRand < 0.80) {
            // Right Ear (~10%)
            let [x, y] = randomPointInEllipse(cx + 55, cy - 70, 20, 25);
            targetX = x;
            targetY = y;
            // Same color as left ear
            cR = 255; 
            cG = 150; 
            cB = 200;
          } else if (shapeRand < 0.85) {
            // Left Eye (~5%)
            let [x, y] = randomPointInEllipse(cx - 25, cy - 20, 6, 6);
            targetX = x;
            targetY = y;
            // Black eyes
            cR = 0; 
            cG = 0; 
            cB = 0;
          } else if (shapeRand < 0.90) {
            // Right Eye (~5%)
            let [x, y] = randomPointInEllipse(cx + 25, cy - 20, 6, 6);
            targetX = x;
            targetY = y;
            // Black eyes
            cR = 0; 
            cG = 0; 
            cB = 0;
          } else if (shapeRand < 0.95) {
            // Nose (~5%)
            let [x, y] = randomPointInEllipse(cx, cy + 15, 15, 10);
            targetX = x;
            targetY = y;
            // Slightly darker pink for nose
            cR = 255; 
            cG = 140; 
            cB = 180;
          } else {
            // Cheeks (~5%)
            // Randomly choose left or right cheek
            if (random() < 0.5) {
              let [x, y] = randomPointInEllipse(cx - 30, cy + 10, 10, 10);
              targetX = x;
              targetY = y;
            } else {
              let [x, y] = randomPointInEllipse(cx + 30, cy + 10, 10, 10);
              targetX = x;
              targetY = y;
            }
            // Rosy cheeks
            cR = 255; 
            cG = 160; 
            cB = 180;
          }

          particles.push(new Particle(heartX, heartY, targetX, targetY, cR, cG, cB));
        }
      }

      function draw() {
        // Slightly transparent background for trailing effect
        background(0, 25);

        // Keep the heart static until globalDelay finishes
        if (globalDelay > 0) {
          globalDelay--;
        } else {
          // Once delay is over, gradually move morphProgress toward 1
          if (morphProgress < 1) {
            morphProgress += 0.005; // Adjust morph speed
            morphProgress = min(morphProgress, 1);
          }
        }

        // Update & display each particle
        for (let p of particles) {
          p.update(morphProgress);
          p.show();
        }
      }

      class Particle {
        constructor(heartX, heartY, targetX, targetY, r, g, b) {
          // Heart position (start)
          this.heartX = heartX;
          this.heartY = heartY;
          // Pig shape position (target)
          this.targetX = targetX;
          this.targetY = targetY;

          // Current position starts at the heart
          this.currentX = heartX;
          this.currentY = heartY;

          // Each particle has a color assigned by its target shape
          this.r = r;
          this.g = g;
          this.b = b;
          this.alpha = 255;

          // Slight variation in particle size
          this.size = random(3, 6);
        }

        update(morphProgress) {
          // Linear interpolation from heart to pig shape
          this.currentX = lerp(this.heartX, this.targetX, morphProgress);
          this.currentY = lerp(this.heartY, this.targetY, morphProgress);

          // Once fully morphed, add a gentle drift
          if (morphProgress >= 1) {
            this.currentX += random(-0.3, 0.3);
            this.currentY += random(-0.3, 0.3);
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

st.set_page_config(page_title="Heart → Cartoon Pig", layout="wide")
st.title("Happy Friday Little Piggy!")

# Embed the p5.js sketch in the Streamlit app
components.html(html_code, height=600)
