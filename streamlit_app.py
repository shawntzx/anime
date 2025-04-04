import streamlit as st

st.title("Heart Beating Animation")

# Use st.markdown with unsafe_allow_html to embed custom HTML and CSS
st.markdown("""
<style>
/* Define the heart shape and its animation */
.heart {
  width: 100px;
  height: 90px;
  background: red;
  position: relative;
  transform: rotate(-45deg);
  animation: beat 1s infinite;
  margin: 0 auto;
}

/* Create the two circles of the heart using pseudo-elements */
.heart::before,
.heart::after {
  content: "";
  background: red;
  border-radius: 50%;
  width: 100px;
  height: 100px;
  position: absolute;
}

/* Position the circles */
.heart::before {
  top: -50px;
  left: 0;
}
.heart::after {
  left: 50px;
  top: 0;
}

/* Define the keyframes for the beat animation */
@keyframes beat {
  0%, 100% {
    transform: scale(1) rotate(-45deg);
  }
  50% {
    transform: scale(1.2) rotate(-45deg);
  }
}
</style>

<!-- Insert the heart element -->
<div class="heart"></div>
""", unsafe_allow_html=True)

st.write("Enjoy the beating heart animation!")
