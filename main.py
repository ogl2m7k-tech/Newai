import requests
import html
from xml.etree import ElementTree
from datetime import datetime

def haber_ara_ve_kaydet():
    # Google News RSS - Teknik olarak daha sağlam yapı
    url = "https://news.google.com/rss/search?q=yapay+zeka&hl=tr&gl=TR&ceid=TR:tr"
    
    try:
        # 1. Güvenlik: Timeout ve Hata Kontrolü
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        root = ElementTree.fromstring(response.content)
        haberler_html = ""

        # 2. Sağlamlık: XML Parse Hatalarını Engelleme
        for item in root.findall('.//item')[:15]:
            baslik = item.findtext('title', default='Başlık bulunamadı')
            link = item.findtext('link', default='#')
            tarih = item.findtext('pubDate', default='Tarih yok')
            
            # 3. Güvenlik: XSS Koruması
            baslik = html.escape(baslik)

            # 4. UI: Kart Tasarımı (Hover Efektli)
            haberler_html += f"""
            <div class="card">
                <h3>{baslik}</h3>
                <p class="date">📅 {tarih}</p>
                <a href="{link}" target="_blank" class="btn">Haberi Oku →</a>
            </div>
            """

        # 5. UI: Modern Tasarım (Responsive & Dark Mode Support)
        tam_site = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI News Center</title>
            <style>
                :root {{ --bg: #f4f7f6; --text: #2c3e50; --card: #ffffff; --accent: #3498db; }}
                @media (prefers-color-scheme: dark) {{
                    :root {{ --bg: #1a1a1a; --text: #ecf0f1; --card: #2c2c2c; --accent: #3498db; }}
                }}
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }}
                header {{ text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #2c3e50, #3498db); color: white; border-radius: 12px; margin-bottom: 30px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .card {{ background: var(--card); padding: 20px; border-radius: 12px; shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s; border: 1px solid rgba(0,0,0,0.1); }}
                .card:hover {{ transform: translateY(-5px); }}
                .date {{ font-size: 0.85em; opacity: 0.7; }}
                .btn {{ display: inline-block; margin-top: 10px; color: var(--accent); text-decoration: none; font-weight: bold; }}
                footer {{ text-align: center; margin-top: 50px; opacity: 0.6; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <header>
                <h1>AI News Daily</h1>
                <p>Yapay Zeka Dünyasından Anlık Gelişmeler</p>
                <small>Son Güncelleme: {datetime.now().strftime('%d/%m/%Y %H:%M')}</small>
            </header>
            <div class="grid">
                {haberler_html}
            </div>
            <footer>
                © 2026 AI News Center | GitHub Actions ile 7/24 Otomatik Güncellenir
            </footer>
        </body>
        </html>
        """

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(tam_site)

    except Exception as e:
        print(f"Sistem hatası: {e}")

if __name__ == "__main__":
    haber_ara_ve_kaydet()
          
