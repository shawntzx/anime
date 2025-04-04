import streamlit as st
import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <!-- 加载 p5.js -->
    <script src="https://cdn.jsdelivr.net/npm/p5@1.4.2/lib/p5.js"></script>
    <style>
      body {
        margin: 0;
        padding: 0;
        overflow: hidden;
        background: #000; /* 深色背景对比 */
      }
    </style>
  </head>
  <body>
    <script>
      /*******************************************************
       * HEART → CARTOON PIG
       * 增大 & 加强鼻子区块
       *******************************************************/

      const NUM_PARTICLES = 1000;  // 总粒子数
      let globalDelay = 180;      // 心形静止时长(帧数)
      let morphProgress = 0;      // 从 0(心) 到 1(猪头)
      let particles = [];

      function setup() {
        createCanvas(windowWidth, windowHeight);

        for (let i = 0; i < NUM_PARTICLES; i++) {
          // 1) 爱心形状 (初始)
          let t = random(TWO_PI);
          let scaleFactor = random(5, 10);
          let heartX = scaleFactor * 16 * pow(sin(t), 3) + width / 2;
          let heartY = -scaleFactor * (
            13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t)
          ) + height / 2;

          // 2) 猪头形状 (目标)
          let shapeRand = random();
          let targetX, targetY;
          let cR, cG, cB;

          // 随机椭圆点函数
          function randomPointInEllipse(cx, cy, rx, ry) {
            let angle = random(TWO_PI);
            let r = sqrt(random(1));
            return [
              cx + r * cos(angle) * rx,
              cy + r * sin(angle) * ry
            ];
          }

          let cx = width / 2;
          let cy = height / 2;

          if (shapeRand < 0.05) {
            /********** LEFT EAR (5%) **********/
            let [x, y] = randomPointInEllipse(cx - 60, cy - 70, 25, 30);
            targetX = x;
            targetY = y;
            cR = 255; cG = 160; cB = 200; // 耳朵粉

          } else if (shapeRand < 0.10) {
            /********** RIGHT EAR (5%) **********/
            let [x, y] = randomPointInEllipse(cx + 60, cy - 70, 25, 30);
            targetX = x;
            targetY = y;
            cR = 255; cG = 160; cB = 200; // 耳朵粉

          } else if (shapeRand < 0.55) {
            /********** FACE (45%) **********/
            let [x, y] = randomPointInEllipse(cx, cy, 80, 70);
            targetX = x;
            targetY = y;
            cR = 255; cG = 185; cB = 200; // 脸部浅粉

          } else if (shapeRand < 0.65) {
            /********** NOSE (10%) (更大 + 更多粒子) **********/
            // 鼻子椭圆加大
            let [x, y] = randomPointInEllipse(cx, cy + 20, 40, 25);
            targetX = x;
            targetY = y;
            // 鼻子颜色更饱和、偏深一点
            cR = 255; cG = 120; cB = 180;

          } else if (shapeRand < 0.70) {
            /********** NOSE HOLES (5%) **********/
            // 鼻孔保持原大小，但可能也可略增
            let [x, y] = randomPointInEllipse(cx, cy + 20, 15, 10);
            targetX = x;
            targetY = y;
            // 鼻孔黑色
            cR = 0; cG = 0; cB = 0;

          } else if (shapeRand < 0.80) {
            /********** CHEEKS (10%) **********/
            if (random() < 0.5) {
              var [x, y] = randomPointInEllipse(cx - 35, cy + 15, 12, 12);
            } else {
              var [x, y] = randomPointInEllipse(cx + 35, cy + 15, 12, 12);
            }
            targetX = x;
            targetY = y;
            cR = 255; cG = 150; cB = 180; // 腮红

          } else if (shapeRand < 0.90) {
            /********** EYES (10%) **********/
            if (random() < 0.5) {
              // 左眼
              var [x, y] = randomPointInEllipse(cx - 30, cy - 15, 5, 5);
            } else {
              // 右眼
              var [x, y] = randomPointInEllipse(cx + 30, cy - 15, 5, 5);
            }
            targetX = x;
            targetY = y;
            cR = 0; cG = 0; cB = 0; // 眼睛黑色

          } else {
            /********** FACE HIGHLIGHT (10%) **********/
            let [x, y] = randomPointInEllipse(cx + 25, cy - 35, 20, 15);
            targetX = x;
            targetY = y;
            // 高光
            cR = 255; cG = 210; cB = 220;
          }

          particles.push(new Particle(heartX, heartY, targetX, targetY, cR, cG, cB));
        }
      }

      function draw() {
        // 半透明背景，营造拖尾
        background(0, 25);

        // 前期保持心形静止
        if (globalDelay > 0) {
          globalDelay--;
        } else {
          // 开始形变
          if (morphProgress < 1) {
            morphProgress += 0.005;  // 调整形变速度
            morphProgress = min(morphProgress, 1);
          }
        }

        // 更新 & 绘制
        for (let p of particles) {
          p.update(morphProgress);
          p.show();
        }
      }

      class Particle {
        constructor(heartX, heartY, targetX, targetY, r, g, b) {
          this.heartX = heartX;
          this.heartY = heartY;
          this.targetX = targetX;
          this.targetY = targetY;

          this.currentX = heartX;
          this.currentY = heartY;

          this.r = r;
          this.g = g;
          this.b = b;
          this.alpha = 255;
          this.size = random(3, 6);
        }

        update(morphProgress) {
          // 从心形坐标插值到目标猪头坐标
          this.currentX = lerp(this.heartX, this.targetX, morphProgress);
          this.currentY = lerp(this.heartY, this.targetY, morphProgress);

          // 形变完毕后给一点微小漂移
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

st.set_page_config(page_title="Heart → More Prominent Nose Pig", layout="wide")
st.title("从爱心到卡通猪头：加强鼻子 (Heart → Pig with Bigger Nose)")

components.html(html_code, height=650)
