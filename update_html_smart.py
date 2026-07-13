import os

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Defer scripts
html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js" defer></script>')
html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js" defer></script>')
html = html.replace('<script src="https://unpkg.com/lucide@latest"></script>', '<script src="https://unpkg.com/lucide@latest" defer></script>')

# 2. Hardware Accel
html = html.replace('    canvas {\n      display: block; position: absolute;', '    canvas {\n      display: block; position: absolute;\n      transform: translateZ(0);\n      will-change: transform;')
html = html.replace('    .hero-overlay {\n      position: absolute;', '    .hero-overlay {\n      position: absolute;\n      transform: translateZ(0);\n      will-change: transform, opacity;')

# 3. Lazy loads
html = html.replace('<img src="file:///C:/Users/nikit/.gemini/antigravity-ide/brain/cb0b91d9-f525-420c-917a-e91c95f455d3/resort_stay_1783941055739.png" alt="Premium Nature Resort Stay with Pool">', '<img src="file:///C:/Users/nikit/.gemini/antigravity-ide/brain/cb0b91d9-f525-420c-917a-e91c95f455d3/resort_stay_1783941055739.png" alt="Premium Nature Resort Stay with Pool" loading="lazy" decoding="async">')
html = html.replace('<iframe src="https://www.google.com/maps/embed', '<iframe loading="lazy" decoding="async" src="https://www.google.com/maps/embed')

# 4. JS preloader
old_js_vars = """    // Frames folder
    const imgFolder = "ezgif-74dc65c3b7383343-jpg (1)";
    const getImagePath = (index) => {
      const num = (index + 1).toString().padStart(3, '0');
      return `./${imgFolder}/ezgif-frame-${num}.jpg`;
    };

    let loadedCount = 0;"""

new_js_vars = """    // Frames folder
    const imgFolder = "frames-webp";
    const getImagePath = (index) => {
      const num = (index + 1).toString().padStart(3, '0');
      return `./${imgFolder}/ezgif-frame-${num}.webp`;
    };

    let loadedCount = 0;
    const preloadTarget = 15;"""
html = html.replace(old_js_vars, new_js_vars)

old_preload = """    function preloadImages() {
      for (let i = 0; i < frameCount; i++) {
        const img = new Image();
        img.onload = img.onerror = () => {
          loadedCount++;
          const percent = Math.floor((loadedCount / frameCount) * 100);
          progressEl.innerText = `Loading Adventure ${percent}%`;
          if (loadedCount === frameCount) {
            initAnimation();
          }
        };
        img.src = getImagePath(i);
        images.push(img);
      }
    }

    // Kickoff Preloader
    preloadImages();"""

new_preload = """    function preloadImages() {
      // First, create all 300 Image objects in the array
      for (let i = 0; i < frameCount; i++) {
        images.push(new Image());
      }
      
      // Only wait for the first 'preloadTarget' frames to remove the loader
      let initialLoaded = 0;
      for (let i = 0; i < preloadTarget; i++) {
        images[i].onload = images[i].onerror = () => {
          initialLoaded++;
          const percent = Math.floor((initialLoaded / preloadTarget) * 100);
          if(progressEl) progressEl.innerText = `Loading Adventure ${percent}%`;
          
          if (initialLoaded === preloadTarget) {
            initAnimation();
            backgroundLoadRest(); // Silently load the rest
          }
        };
        images[i].src = getImagePath(i);
      }
    }

    function backgroundLoadRest() {
      for (let i = preloadTarget; i < frameCount; i++) {
        images[i].src = getImagePath(i);
      }
    }

    // Kickoff Preloader
    window.addEventListener('load', () => {
       preloadImages();
    });"""
html = html.replace(old_preload, new_preload)

# Wrap lucide.createIcons() inside DOMContentLoaded due to defer
html = html.replace("lucide.createIcons();", "document.addEventListener('DOMContentLoaded', () => {\n      lucide.createIcons();\n    });")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.html")
