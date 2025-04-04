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
        background: #000; /* Dark background */
      }
    </style>
  </head>
  <body>
    <script>
      /*******************************************************
       * HEART → CARTOON PIG HEAD
       * A more detailed pig face with ears, eyes, nose, cheeks,
       * highlight, and separate color regions.
       *******************************************************/

      // Number of total particles
      const NUM_PARTICLES = 1000;

      // Delay (in frames) before morphing starts (e.g., 180 ~3s at 60fps)
      let globalDelay = 180;

      // Morph progress goes from 0 (heart) to 1 (pig)
      let morphProgress = 0;

      let particles = [];

      function setup() {
        createCanvas(windowWidth, windowHeight);

        // Generate particles
        for (let i = 0; i < NUM_PARTICLES; i++) {
          // 1) HEART SHAPE (initial position)
          //    Using the classic heart parametric equation
          let t = random(TWO_PI);
          let scaleFactor = random(5, 10);
          let heartX = scaleFactor * 16 * pow(sin(t), 3) + width / 2;
          let heartY = -scaleFactor * (
            13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
          ) + height / 2;

          // 2) CARTOON PIG SHAPE (target position & color)
          //    We'll define multiple overlapping "regions":
          //    ears, face, nose, nose holes, cheeks, eyes, highlight, etc.
          //    Each region is assigned a fraction of the particles.

          let shapeRand = random(); // 0..1
          let targetX, targetY;
          let cR, cG, cB;

          // Helper: random point inside an ellipse
          function randomPointInEllipse(cx, cy, rx, ry) {
            // sqrt() + random angle ensures uniform distribution in ellipse
            let angle = random(TWO_PI);
            let r = sqrt(random(1));
            let x = r * cos(angle) * rx;
            let y = r * sin(angle) * ry;
            return [cx + x, cy + y];
          }

          // Canvas center
          let cx = width / 2;
          let cy = height / 2;

          // We’ll distribute shapeRand across regions in ascending order.
          // Adjust intervals to change how many particles go to each region.

          if (shapeRand < 0.05) {
            /********** LEFT EAR (5%) **********/
            let [x, y] = randomPointInEllipse(cx - 60, cy - 70, 25, 30);
            targetX = x; 
            targetY = y;
            // Slightly darker pink
            cR = 255; cG = 160; cB = 200;

          } else if (shapeRand < 0.10) {
            /********** RIGHT EAR (5%) **********/
            let [x, y] = randomPointInEllipse(cx + 60, cy - 70, 25, 30);
            targetX = x; 
            targetY = y;
            // Same as left ear
            cR = 255; cG = 160; cB = 200;

          } else if (shapeRand < 0.60) {
            /********** FACE (50%) **********/
            // A main ellipse for the face
            let [x, y] = randomPointInEllipse(cx, cy, 80, 70);
            targetX = x; 
            targetY = y;
            // Light pink
            cR = 255; cG = 185; cB = 200;

          } else if (shapeRand < 0.65) {
            /********** NOSE (5%) **********/
            // Snout area
            let [x, y] = randomPointInEllipse(cx, cy + 20, 30, 20);
            targetX = x; 
            targetY = y;
            // Medium pink
            cR = 255; cG = 140; cB = 190;

          } else if (shapeRand < 0.70) {
            /********** NOSE HOLES (5%) **********/
            // Two black nostrils. We'll just scatter them in the snout ellipse.
            let [x, y] = randomPointInEllipse(cx, cy + 20, 15, 10);
            targetX = x; 
            targetY = y;
            // Black
            cR = 0; cG = 0; cB = 0;

          } else if (shapeRand < 0.80) {
            /********** CHEEKS (10%) **********/
            // Left or right cheek
            if (random() < 0.5) {
              // Left cheek
              var [x, y] = randomPointInEllipse(cx - 35, cy + 15, 12, 12);
            } else {
              // Right cheek
              var [x, y] = randomPointInEllipse(cx + 35, cy + 15, 12, 12);
            }
            targetX = x; 
            targetY = y;
            // Rosy pink
            cR = 255; cG = 150; cB = 180;

          } else if (shapeRand < 0.90) {
            /********** EYES (10%) **********/
            // Left or right eye
            if (random() < 0.5) {
              // Left eye
              var [x, y] = randomPointInEllipse(cx - 30, cy - 15, 5, 5);
            } else {
              // Right eye
              var [x, y] = randomPointInEllipse(cx + 30, cy - 15, 5, 5);
            }
            targetX = x; 
            targetY = y;
            // Black eyes
            cR = 0; cG = 0; cB = 0;

          } else {
            /********** FACE HIGHLIGHT (10%) **********/
            // A lighter ellipse in top-right corner
            let [x, y] = randomPointInEllipse(cx + 25, cy - 35, 20, 15);
            targetX = x;
            targetY = y;
            // Very light pink for the highlight
            cR = 255; cG = 210; cB = 220;
          }

          // Create our particle
          particles.push(new Particle(heartX, heartY, targetX, targetY, cR, cG, cB));
        }
      }

      function draw() {
        background(0, 25);  // Slightly transparent for trailing

        // Keep heart static until the global delay finishes
        if (globalDelay > 0) {
          globalDelay--;
        } else {
          // Once delay is over, morphProgress gradually goes to 1
          if (morphProgress < 1) {
            morphProgress += 0.005;  // Increase/decrease for faster/slower
            morphProgress = min(morphProgress, 1);
          }
        }

        // Update & display each particle
        for (let p of particles) {
          p.update(morphProgress);
          p.show();
        }
      }

      // Particle class
      class Particle {
        constructor(heartX, heartY, targetX, targetY, r, g, b) {
          // Starting: heart
          this.heartX = heartX;
          this.heartY = heartY;
          // Target: pig feature
          this.targetX = targetX;
          this.targetY = targetY;

          // Current position starts at the heart
          this.currentX = heartX;
          this.currentY = heartY;

          // Particle color
          this.r = r;
          this.g = g;
          this.b = b;
          this.alpha = 255;

          // Slight random size
          this.size = random(3, 6);
        }

        update(morphProgress) {
          // Linear interpolation from heart coords to pig coords
          this.currentX = lerp(this.heartX, this.targetX, morphProgress);
          this.currentY = lerp(this.heartY, this.targetY, morphProgress);

          // Once fully morphed, let them drift slightly
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

st.set_page_config(page_title="Heart → Cute Pig Morph", layout="wide")
st.title("从爱心到更精致的卡通猪头 (Heart → More Detailed Pig)")

# Embed the p5.js sketch in the Streamlit app
components.html(html_code, height=650)
