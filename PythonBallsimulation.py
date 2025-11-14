import pygame
import random
import sys
from os import path

# --- 1. Başlatma ve Sabit Değişkenler ---
pygame.init()

# Ekran Boyutları
EKRAN_GENISLIGI = 800
EKRAN_YUKSEKLIGI = 750
KONTROL_PANELI_YUKSEKLIGI = 200
CIZIM_ALANI_YUKSEKLIGI = EKRAN_YUKSEKLIGI - KONTROL_PANELI_YUKSEKLIGI
GOLGE_OFFSET = 4

# Modern Renk Paleti
RENK_ARKA_PLAN = (22, 28, 39)
RENK_PANEL = (42, 51, 66)
RENK_KART = (52, 62, 80)
RENK_YAZI = (230, 230, 230)
RENK_GOLGE = (15, 20, 28)

# <<-- RENKLER GÜNCELLENDİ -->>
RENK_KIRMIZI = (231, 76, 60)  # Canlı Kırmızı
RENK_MAVI = (52, 152, 219)  # Canlı Mavi
RENK_SARI = (241, 196, 15)  # Canlı Sarı
RENK_SECIM_VURGU = (255, 255, 255)  # Beyaz vurgu aynı kaldı

# Font Yükleme Kontrolü
CUSTOM_FONT_LOADED = False
try:
    FONT_YOLU_BOLD = "Montserrat-Bold.ttf"
    FONT_YOLU_REGULAR = "Montserrat-Regular.ttf"
    if not path.exists(FONT_YOLU_BOLD) or not path.exists(FONT_YOLU_REGULAR):
        raise FileNotFoundError
    BASLIK_FONTU = pygame.font.Font(FONT_YOLU_BOLD, 14)
    ETIKET_FONTU = pygame.font.Font(FONT_YOLU_REGULAR, 18)
    IKON_FONTU = pygame.font.Font(FONT_YOLU_REGULAR, 24)
    CUSTOM_FONT_LOADED = True
except FileNotFoundError:
    print("Uyarı: 'Montserrat' fontu bulunamadı, varsayılan fontlar kullanılıyor.")
    BASLIK_FONTU = pygame.font.SysFont('Arial', 14, bold=True)
    ETIKET_FONTU = pygame.font.SysFont('Arial', 18)
    IKON_FONTU = pygame.font.SysFont('Arial', 16, bold=True)

# Ekran ve Saat
ekran = pygame.display.set_mode((EKRAN_GENISLIGI, EKRAN_YUKSEKLIGI))
pygame.display.set_caption("Ball Animation - Final UI")
saat = pygame.time.Clock()


# --- 2. Top Sınıfı ---
class Ball:
    def __init__(self, yaricap, renk):
        self.yaricap, self.renk = yaricap, renk
        self.x = random.randint(self.yaricap, EKRAN_GENISLIGI - self.yaricap)
        self.y = random.randint(self.yaricap, CIZIM_ALANI_YUKSEKLIGI - self.yaricap)
        hiz_carpanı = 100 / (self.yaricap + 25)
        self.hiz_x, self.hiz_y = random.choice([-3, 3]) * hiz_carpanı, random.choice([-3, 3]) * hiz_carpanı
        self.orijinal_hiz_x, self.orijinal_hiz_y = self.hiz_x, self.hiz_y

    def ciz(self, yuzey):
        pygame.draw.circle(yuzey, RENK_GOLGE, (int(self.x) + GOLGE_OFFSET, int(self.y) + GOLGE_OFFSET), self.yaricap)
        pygame.draw.circle(yuzey, self.renk, (int(self.x), int(self.y)), self.yaricap)

    def hareket_et(self):
        self.x += self.hiz_x;
        self.y += self.hiz_y
        if not (self.yaricap <= self.x <= EKRAN_GENISLIGI - self.yaricap): self.hiz_x *= -1
        if not (self.yaricap <= self.y <= CIZIM_ALANI_YUKSEKLIGI - self.yaricap): self.hiz_y *= -1

    def hizi_guncelle(self, carpan):
        self.hiz_x, self.hiz_y = self.orijinal_hiz_x * carpan, self.orijinal_hiz_y * carpan


# --- 3. Arayüz Elemanları ---
ui_elemanlari = {
    'kucuk_boy': {'rect': pygame.Rect(75, 630, 40, 40), 'deger': 15},
    'orta_boy': {'rect': pygame.Rect(140, 620, 60, 60), 'deger': 25},
    'buyuk_boy': {'rect': pygame.Rect(225, 610, 80, 80), 'deger': 40},

    # <<-- RENKLER GÜNCELLENDİ -->>
    'renk1': {'rect': pygame.Rect(355, 630, 50, 50), 'deger': RENK_KIRMIZI},
    'renk2': {'rect': pygame.Rect(415, 630, 50, 50), 'deger': RENK_MAVI},
    'renk3': {'rect': pygame.Rect(475, 630, 50, 50), 'deger': RENK_SARI},

    'start': {'rect': pygame.Rect(580, 635, 80, 45), 'ikon': '▶', 'etiket': 'START'},
    'stop': {'rect': pygame.Rect(680, 635, 80, 45), 'ikon': '■', 'etiket': 'STOP'},
    'reset': {'rect': pygame.Rect(580, 690, 80, 40), 'ikon': '↻', 'etiket': 'RESET'},
    'speed_up': {'rect': pygame.Rect(680, 690, 80, 40), 'ikon': '≫', 'etiket': 'HIZ+'},
}

KARTLAR = [
    {'rect': (20, 570, 310, 165), 'baslik': "BOYUT"},
    {'rect': (340, 570, 200, 165), 'baslik': "RENK"},
    {'rect': (550, 570, 230, 165), 'baslik': "KONTROL"}
]


def metni_ortala(yuzey, metin, font, renk, merkez_x, y):
    yazi = font.render(metin, True, renk)
    rect = yazi.get_rect(center=(merkez_x, y))
    yuzey.blit(yazi, rect)


def arayuzu_ciz(secili_boy, secili_renk, hiz_carpanı, aktif_buton):
    pygame.draw.rect(ekran, RENK_PANEL, (0, CIZIM_ALANI_YUKSEKLIGI, EKRAN_GENISLIGI, KONTROL_PANELI_YUKSEKLIGI))

    for kart in KARTLAR:
        x, y, w, h = kart['rect']
        pygame.draw.rect(ekran, RENK_KART, kart['rect'], border_radius=15)
        metni_ortala(ekran, kart['baslik'], BASLIK_FONTU, RENK_YAZI, x + w // 2, y + 20)

    kontrol_karti_merkez_x = KARTLAR[2]['rect'][0] + KARTLAR[2]['rect'][2] // 2
    metni_ortala(ekran, f"Hız: {hiz_carpanı:.1f}x", ETIKET_FONTU, RENK_YAZI, kontrol_karti_merkez_x, 610)

    fare_pozisyonu = pygame.mouse.get_pos()

    for anahtar, deger in ui_elemanlari.items():
        rect = deger['rect']
        offset = GOLGE_OFFSET if aktif_buton == anahtar else 0

        if 'boy' in anahtar:
            pygame.draw.circle(ekran, RENK_GOLGE, (rect.centerx + GOLGE_OFFSET, rect.centery + GOLGE_OFFSET),
                               rect.width // 2)
        else:
            pygame.draw.rect(ekran, RENK_GOLGE, (rect.x + GOLGE_OFFSET, rect.y + GOLGE_OFFSET, rect.width, rect.height),
                             border_radius=12)

        renk = RENK_PANEL
        if 'renk' in anahtar: renk = deger['deger']
        if rect.collidepoint(fare_pozisyonu) and 'boy' in anahtar: renk = RENK_YAZI

        if 'boy' in anahtar:
            pygame.draw.circle(ekran, renk, (rect.centerx + offset, rect.centery + offset), rect.width // 2)
        else:
            pygame.draw.rect(ekran, renk, (rect.x + offset, rect.y + offset, rect.width, rect.height), border_radius=12)

        if 'etiket' in deger:
            metin, font = (deger['ikon'], IKON_FONTU) if CUSTOM_FONT_LOADED else (deger['etiket'], IKON_FONTU)
            metni_ortala(ekran, metin, font, RENK_YAZI, rect.centerx + offset, rect.centery + offset)

    for k, v in ui_elemanlari.items():
        if 'boy' in k and v['deger'] == secili_boy:
            pygame.draw.circle(ekran, RENK_SECIM_VURGU, v['rect'].center, v['rect'].width // 2, 4);
            break
    for k, v in ui_elemanlari.items():
        if 'renk' in k and v['deger'] == secili_renk:
            pygame.draw.rect(ekran, RENK_SECIM_VURGU, v['rect'], 4, border_radius=12);
            break


# --- 4. Ana Program Döngüsü ---
def ana_dongu():
    toplar, animasyon_aktif = [], False
    secili_yaricap = ui_elemanlari['orta_boy']['deger']
    secili_renk = ui_elemanlari['renk1']['deger']
    hiz_carpanı, aktif_buton = 1.0, None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for anahtar, deger in ui_elemanlari.items():
                    if deger['rect'].collidepoint(event.pos):
                        aktif_buton = anahtar
                        if 'boy' in anahtar:
                            secili_yaricap = deger['deger']
                            yeni_top = Ball(secili_yaricap, secili_renk)
                            toplar.append(yeni_top);
                            yeni_top.hizi_guncelle(hiz_carpanı)
                        elif 'renk' in anahtar:
                            secili_renk = deger['deger']
                        elif anahtar == 'start':
                            animasyon_aktif = True
                        elif anahtar == 'stop':
                            animasyon_aktif = False
                        elif anahtar == 'reset':
                            toplar.clear();
                            hiz_carpanı = 1.0;
                            animasyon_aktif = False
                        elif anahtar == 'speed_up':
                            hiz_carpanı = round(hiz_carpanı + 0.2, 1)
                            for top in toplar: top.hizi_guncelle(hiz_carpanı)
                        break
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                aktif_buton = None
        if animasyon_aktif:
            for top in toplar: top.hareket_et()
        ekran.fill(RENK_ARKA_PLAN)
        for top in toplar: top.ciz(ekran)
        arayuzu_ciz(secili_yaricap, secili_renk, hiz_carpanı, aktif_buton)
        pygame.display.flip()
        saat.tick(60)


if __name__ == '__main__':
    ana_dongu()