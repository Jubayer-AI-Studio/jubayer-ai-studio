import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 640

# Fonts
font_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 48)
font_title_bn = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 38)
font_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20)
font_pill = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
font_feature_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 15)
font_feature_desc = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
font_chip = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 13)
font_watermark = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 13)
font_metric_num = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 32)
font_metric_label = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 12)

def create_banner(config, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Base Gradient Canvas
    img = Image.new('RGB', (W, H), config['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    # Add subtle background grid lines
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=config['grid_color'], width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=config['grid_color'], width=1)
        
    # Glow Circle in top right and bottom left
    glow_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    
    # Accent ambient glow top-right
    r1, g1, b1 = config['accent_rgb']
    for r in range(350, 0, -25):
        alpha = int(25 * (1 - r / 350))
        glow_draw.ellipse([W - 100 - r, -100 - r, W - 100 + r, -100 + r], fill=(r1, g1, b1, alpha))
        
    # Secondary ambient glow bottom-left
    for r in range(300, 0, -20):
        alpha = int(18 * (1 - r / 300))
        glow_draw.ellipse([-50 - r, H - 50 - r, -50 + r, H - 50 + r], fill=(r1, g1, b1, alpha))
        
    img = Image.alpha_composite(img.convert('RGBA'), glow_overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Outer Border Framing (8px offset)
    draw.rounded_rectangle([20, 20, W - 20, H - 20], radius=16, outline=config['border_color'], width=2)
    
    # Top Category Pill
    pill_text = config['pill_text']
    pill_bbox = font_pill.getbbox(pill_text)
    pw = pill_bbox[2] - pill_bbox[0] + 32
    ph = 32
    px, py = 50, 48
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=16, fill=config['pill_bg'], outline=config['accent_color'], width=1)
    draw.text((px + 16, py + 7), pill_text, fill=config['accent_color'], font=font_pill)
    
    # Live Status Indicator
    status_text = "● LIVE SYSTEM"
    s_bbox = font_pill.getbbox(status_text)
    sw = s_bbox[2] - s_bbox[0] + 24
    sx = W - 50 - sw
    draw.rounded_rectangle([sx, py, sx + sw, py + ph], radius=16, fill=(16, 185, 129, 25), outline=(16, 185, 129), width=1)
    draw.text((sx + 12, py + 7), status_text, fill=(52, 211, 153), font=font_pill)
    
    # Title & Subtitle
    ty = 105
    draw.text((50, ty), config['title'], fill=(255, 255, 255), font=font_title)
    draw.text((50, ty + 62), config['subtitle'], fill=(148, 163, 184), font=font_sub)
    
    # Middle Section: 4 Feature Highlight Cards (2x2 Grid)
    card_w = 370
    card_h = 76
    card_gap_x = 24
    card_gap_y = 16
    start_x = 50
    start_y = 205
    
    for i, feat in enumerate(config['features']):
        col = i % 2
        row = i // 2
        cx = start_x + col * (card_w + card_gap_x)
        cy = start_y + row * (card_h + card_gap_y)
        
        # Card Background with Glass border
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=10, fill=config['card_bg'], outline=config['card_border'], width=1)
        # Accent left indicator bar
        draw.rounded_rectangle([cx, cy, cx + 4, cy + card_h], radius=2, fill=config['accent_color'])
        # Card Content
        draw.text((cx + 16, cy + 14), feat['title'], fill=(241, 245, 249), font=font_feature_title)
        draw.text((cx + 16, cy + 40), feat['desc'], fill=(148, 163, 184), font=font_feature_desc)

    # Right Hero Metric Card (370px width)
    mx = start_x + 2 * (card_w + card_gap_x)
    my = start_y
    mh = card_h * 2 + card_gap_y
    mw = W - 50 - mx
    draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=12, fill=config['metric_bg'], outline=config['accent_color'], width=1)
    
    # Metric Card Content
    draw.text((mx + 24, my + 24), config['metric_num'], fill=config['accent_color'], font=font_metric_num)
    draw.text((mx + 24, my + 68), config['metric_title'], fill=(255, 255, 255), font=font_feature_title)
    draw.text((mx + 24, my + 94), config['metric_sub'], fill=(148, 163, 184), font=font_metric_label)
    
    # Horizontal divider
    draw.line([(50, 400), (W - 50, 400)], fill=config['grid_color'], width=1)
    
    # Bottom Section: Tech Stack Badges
    by = 425
    draw.text((50, by), "ENGINEERING STACK:", fill=(148, 163, 184), font=font_pill)
    
    chip_x = 50
    chip_y = by + 26
    for tag in config['stack']:
        t_bbox = font_chip.getbbox(tag)
        tw = t_bbox[2] - t_bbox[0] + 20
        th = 28
        draw.rounded_rectangle([chip_x, chip_y, chip_x + tw, chip_y + th], radius=6, fill=config['chip_bg'], outline=config['card_border'], width=1)
        draw.text((chip_x + 10, chip_y + 6), tag, fill=(226, 232, 240), font=font_chip)
        chip_x += tw + 10
        
    # Watermark Footer
    footer_y = H - 56
    author_text = "⚡ ARCHITECTED BY JUBAYER AHMAD  |  JUBAYER AI STUDIO"
    draw.text((50, footer_y), author_text, fill=config['accent_color'], font=font_watermark)
    
    gh_badge = "github.com/Jubayer-AI-Studio"
    gh_bbox = font_watermark.getbbox(gh_badge)
    draw.text((W - 50 - (gh_bbox[2] - gh_bbox[0]), footer_y), gh_badge, fill=(148, 163, 184), font=font_watermark)
    
    img.save(output_path, 'PNG', optimize=True)
    print(f"Generated: {output_path}")

# Configurations for the 4 banners
banners = [
    {
        'title': "NoorHub SaaS (নূরহাব)",
        'subtitle': "Universal Islamic Education Management & Cloud SaaS Platform",
        'pill_text': "ENTERPRISE CLOUD SaaS • MULTI-TENANT ARCHITECTURE",
        'bg_dark': (7, 16, 28),
        'accent_color': (52, 211, 153),
        'accent_rgb': (16, 185, 129),
        'border_color': (16, 185, 129, 60),
        'grid_color': (15, 33, 55),
        'card_bg': (10, 25, 45),
        'card_border': (30, 58, 95),
        'pill_bg': (16, 185, 129, 25),
        'metric_bg': (11, 30, 50),
        'chip_bg': (15, 35, 60),
        'metric_num': "29 ROUTES",
        'metric_title': "Full Lifecycle SaaS",
        'metric_sub': "Bilingual • Offline PWA • Multi-Tenant",
        'features': [
            {'title': "🗺️ Spatial GIS Mapping", 'desc': "Full 64-district clustering with Leaflet GIS"},
            {'title': "🪪 Dynamic ID Engine", 'desc': "Real-time Code-128 & QR ID badge generator"},
            {'title': "📱 Offline-First PWA", 'desc': "Service Worker caching for unstable connectivity"},
            {'title': "🎙️ Noor AI Voice Bot", 'desc': "Gemini AI vocal queries & intent mapping"}
        ],
        'stack': ["Next.js 15", "React 19", "TypeScript", "Drizzle ORM", "PostgreSQL", "Tailwind CSS", "Leaflet GIS", "PWA"],
        'output': "C:/Users/ASSDi/Desktop/github/NoorHub-Madrasa-Management-SaaS/assets/social_preview.png"
    },
    {
        'title': "Jubayer AI (Desktop Jarvis)",
        'subtitle': "100% Hands-Free Autonomous Desktop OS with Biometrics & Vision",
        'pill_text': "AUTONOMOUS AI RUNTIME • COMPUTER VISION WORKSTATION",
        'bg_dark': (6, 10, 20),
        'accent_color': (56, 189, 248),
        'accent_rgb': (14, 165, 233),
        'border_color': (14, 165, 233, 60),
        'grid_color': (15, 25, 45),
        'card_bg': (10, 18, 35),
        'card_border': (25, 45, 80),
        'pill_bg': (14, 165, 233, 25),
        'metric_bg': (10, 22, 42),
        'chip_bg': (15, 30, 55),
        'metric_num': "100% FREE",
        'metric_title': "Zero-Touch OS",
        'metric_sub': "Voiceprint Frequency • Vision Gestures",
        'features': [
            {'title': "🎙️ Biometric Voiceprint", 'desc': "Owner voice frequency authentication defense"},
            {'title': "👁️ Vision & Landmarks", 'desc': "MediaPipe & OpenCV hands-free gesture control"},
            {'title': "🔮 Floating Arc Reactor", 'desc': "Interactive HUD with audio waveform reactivity"},
            {'title': "📱 Smartphone Remote", 'desc': "Local network QR web dashboard control"}
        ],
        'stack': ["Python 3.11", "OpenCV", "MediaPipe", "Google Gemini AI", "CustomTkinter", "SpeechRecognition", "Sockets"],
        'output': "C:/Users/ASSDi/Desktop/github/jubayer-ai-studio/assets/og_banners/jarvis_social_preview.png"
    },
    {
        'title': "Shafin Blade Fighter 3D",
        'subtitle': "Cross-Platform Browser Combat Arcade Game with Custom 3D Physics",
        'pill_text': "60 FPS CANVAS ENGINE • ARCADE COMBAT PWA",
        'bg_dark': (14, 10, 22),
        'accent_color': (245, 158, 11),
        'accent_rgb': (245, 158, 11),
        'border_color': (245, 158, 11, 60),
        'grid_color': (30, 20, 45),
        'card_bg': (22, 15, 34),
        'card_border': (55, 35, 80),
        'pill_bg': (245, 158, 11, 25),
        'metric_bg': (25, 18, 40),
        'chip_bg': (30, 20, 48),
        'metric_num': "60 FPS",
        'metric_title': "Zero GPU Overhead",
        'metric_sub': "Procedural Web Audio • Frame-Accurate",
        'features': [
            {'title': "🕹️ Custom Canvas Physics", 'desc': "Frame-accurate hitboxes and combo chaining"},
            {'title': "🔊 Web Audio Synthesizer", 'desc': "Instant procedural impact sound synthesis"},
            {'title': "📱 Adaptive Multi-Input", 'desc': "Gamepads, keyboards and virtual touch controls"},
            {'title': "📦 Standalone PWA", 'desc': "Zero-network offline gameplay capability"}
        ],
        'stack': ["HTML5 Canvas", "JavaScript (ES6+)", "Web Audio API", "Three.js", "PWA", "CSS3 Animations"],
        'output': "C:/Users/ASSDi/Desktop/github/Shafin-Blade-Fighter-Game/assets/social_preview.png"
    },
    {
        'title': "Shono AI (শোনো এআই)",
        'subtitle': "Bangladeshi Dialect-Aware Real-Time Voice Assistant HUD",
        'pill_text': "REGIONAL SPEECH AI • CYBERPUNK HUD INTERFACE",
        'bg_dark': (13, 8, 26),
        'accent_color': (168, 85, 247),
        'accent_rgb': (168, 85, 247),
        'border_color': (168, 85, 247, 60),
        'grid_color': (28, 18, 50),
        'card_bg': (22, 14, 40),
        'card_border': (50, 30, 85),
        'pill_bg': (168, 85, 247, 25),
        'metric_bg': (25, 15, 48),
        'chip_bg': (32, 20, 58),
        'metric_num': "3 DIALECTS",
        'metric_title': "Regional Intent Map",
        'metric_sub': "Sylheti • Chatgaya • Dhakaiya Native",
        'features': [
            {'title': "🗣️ Dialect Intent Mapping", 'desc': "Maps spoken colloquial phonetics to action APIs"},
            {'title': "🌌 Cyberpunk Live HUD", 'desc': "Real-time Web Audio API animated spectrum"},
            {'title': "⚡ Zero-Latency Pipeline", 'desc': "Low latency Web Speech API client processing"},
            {'title': "📱 Single-File Architecture", 'desc': "Zero framework build step, 100% portable"}
        ],
        'stack': ["JavaScript", "Web Speech API", "Web Audio API", "Tailwind CSS", "HUD Visualizer"],
        'output': "C:/Users/ASSDi/Desktop/github/Shono-AI-Bangladeshi-Jarvis/assets/social_preview.png"
    }
]

for b in banners:
    create_banner(b, b['output'])
    # Also save a copy in jubayer-ai-studio/assets/og_banners/
    basename = os.path.basename(b['output'])
    copy_path = os.path.join("C:/Users/ASSDi/Desktop/github/jubayer-ai-studio/assets/og_banners", basename)
    if copy_path != b['output']:
        create_banner(b, copy_path)

print("All 4 Open Graph Social Preview Banners generated successfully!")
