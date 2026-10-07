import os
from PIL import Image, ImageDraw, ImageFont

def create_pv_bridge_gif(output_filename="pv_bridge_demo.gif"):
    # Bild-Einstellungen
    width, height = 650, 360
    bg_color = (15, 18, 25)        # Dunkles Terminal-Theme
    box_bg = (24, 28, 38)          # Karten-Hintergrund
    text_color = (220, 225, 235)   # Standard-Text
    green_color = (46, 204, 113)   # Highlight Ersparnis / Aktiv
    red_color = (231, 76, 60)      # Highlight Standard / Inaktiv
    accent_blue = (52, 152, 219)   # Header Accent
    line_color = (40, 48, 62)

    # Schriftart laden (Monospace / Standard)
    try:
        font_title = ImageFont.truetype("consola.ttf", 18)
        font_body = ImageFont.truetype("consola.ttf", 15)
        font_bold = ImageFont.truetype("consolab.ttf", 16)
    except IOError:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    frames = []

    def draw_frame(state_active):
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # Rahmen / Terminal-Fenster
        draw.rectangle([15, 15, width - 15, height - 15], fill=box_bg, outline=line_color, width=2)
        
        # Header
        draw.text((35, 30), "E4COLOGIC pv_bridge ESP32 MONITOR", font=font_title, fill=accent_blue)
        draw.line([(35, 58), (width - 35, 58)], fill=line_color, width=1)

        if state_active:
            # Zustand MIT pv_bridge
            status_text = "[MODUS: MIT pv_bridge ACTIVE (6.4x)]"
            status_color = green_color
            
            lines = [
                ("Datenvolumen : ", "2560 Werte (statt 16384)"),
                ("Speicherlast : ", "15.63% (Optimiert)"),
                ("Rechenkosten : ", "$15.63 USD"),
                ("Ersparnis    : ", "$84.38 USD (84.38%)")
            ]
        else:
            # Zustand OHNE pv_bridge
            status_text = "[MODUS: OHNE BRIDGE (Standard / Vollfeld)]"
            status_color = red_color
            
            lines = [
                ("Datenvolumen : ", "16384 Werte (Vollfeld)"),
                ("Speicherlast : ", "100.00% (Voller Overhead)"),
                ("Rechenkosten : ", "$100.00 USD"),
                ("Ersparnis    : ", "$0.00 USD (0.00%)")
            ]

        # Status Rendern
        draw.text((35, 75), status_text, font=font_bold, fill=status_color)

        # Werte Rendern
        y_offset = 115
        for label, val in lines:
            draw.text((35, y_offset), label, font=font_body, fill=text_color)
            
            # Besondere Hervorhebung für Ersparnis
            if "Ersparnis" in label and state_active:
                draw.text((170, y_offset), val, font=font_bold, fill=green_color)
            elif "Ersparnis" in label and not state_active:
                draw.text((170, y_offset), val, font=font_body, fill=red_color)
            else:
                draw.text((170, y_offset), val, font=font_body, fill=(180, 190, 205))
                
            y_offset += 32

        # Visueller Ladebalken / Ersparnis-Gauge
        draw.line([(35, 260), (width - 35, 260)], fill=line_color, width=1)
        draw.text((35, 275), "Effizienz-Index:", font=font_body, fill=text_color)
        
        # Balken-Geometrie
        bar_x1, bar_y1 = 180, 275
        bar_w, bar_h = 400, 20
        draw.rectangle([bar_x1, bar_y1, bar_x1 + bar_w, bar_y1 + bar_h], outline=line_color, fill=(30, 35, 45))

        if state_active:
            fill_w = int(bar_w * 0.8438)
            draw.rectangle([bar_x1, bar_y1, bar_x1 + fill_w, bar_y1 + bar_h], fill=green_color)
            draw.text((bar_x1 + fill_w + 10, bar_y1 + 2), "84.38%", font=font_bold, fill=green_color)
        else:
            fill_w = int(bar_w * 0.1563)
            draw.rectangle([bar_x1, bar_y1, bar_x1 + fill_w, bar_y1 + bar_h], fill=red_color)
            draw.text((bar_x1 + fill_w + 10, bar_y1 + 2), "0.00%", font=font_body, fill=red_color)

        # Footer
        draw.text((35, 315), "Simulations-Wechsel alle 3 Sekunden...", font=font_body, fill=(100, 110, 125))

        return img

    # Frames generieren: Frame 0 (Ohne Bridge) und Frame 1 (Mit Bridge)
    frames.append(draw_frame(state_active=False))
    frames.append(draw_frame(state_active=True))

    # Als GIF speichern (jeder Frame steht 3000 ms = 3 Sekunden)
    frames[0].save(
        output_filename,
        save_all=True,
        append_images=[frames[1]],
        duration=3000,
        loop=0
    )
    print(f"GIF erfolgreich erstellt: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_pv_bridge_gif()