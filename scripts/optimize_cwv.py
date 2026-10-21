path = 'C:/Users/ASSDi/Desktop/github/jubayer-ai-studio/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add preload for hero avatar
target1 = '<link rel="icon" type="image/jpeg" href="assets/jubayer_avatar.jpg">'
repl1 = target1 + '\n    <link rel="preload" as="image" href="assets/jubayer_avatar.jpg" fetchpriority="high">'
if target1 in content:
    content = content.replace(target1, repl1, 1)

# 2. Defer lucide script
target2 = '<script src="https://unpkg.com/lucide@latest"></script>'
repl2 = '<script src="https://unpkg.com/lucide@latest" defer></script>'
if target2 in content:
    content = content.replace(target2, repl2, 1)

# 3. Hero avatar attributes for CLS and LCP
target3 = 'alt="Jubayer AI Specialist — Portrait with Cybernetic Telemetry Ring"'
repl3 = 'alt="Jubayer AI Specialist — Portrait with Cybernetic Telemetry Ring" width="384" height="384" fetchpriority="high"'
if target3 in content:
    content = content.replace(target3, repl3, 1)

# 4. Lazy load cover and coding images
target4 = 'alt="Jubayer AI Studio Command Center Banner"'
repl4 = 'alt="Jubayer AI Studio Command Center Banner" loading="lazy" width="1200" height="458"'
if target4 in content:
    content = content.replace(target4, repl4, 1)

target5 = 'alt="Jubayer AI Specialist coding at his development workstation"'
repl5 = 'alt="Jubayer AI Specialist coding at his development workstation" loading="lazy" width="600" height="400"'
if target5 in content:
    content = content.replace(target5, repl5, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully applied Core Web Vitals optimizations to index.html!")
