import msvcrt  # Windows'ta tuşa basılıp basılmadığını beklemeden okumaya yarar
import time


class Car:
    """Gaz, fren ve boşta gitmeyi basit fizik kurallarıyla hesaplayan araba."""

    def __init__(self, brand: str, mass_kg: float, power_kw: float) -> None:
        self.brand = brand
        self.mass = mass_kg              # arabanın ağırlığı (kg)
        self.power = power_kw * 1000     # motor gücü (watt)
        self.speed = 0.0                 # hız (metre/saniye), 0'dan başlar

    def speed_kmh(self) -> float:
        return self.speed * 3.6          # m/s'yi km/sa'e çevirir

    def resistance(self) -> float:
        """Arabayı yavaşlatan kuvvetler (Newton): hava direnci + lastik sürtünmesi."""
        air = 0.5 * 1.2 * 0.01 * self.speed ** 2   # hız arttıkça karesiyle büyür
        rolling = 0.012 * self.mass * 9.81          # hızdan bağımsız, hep aynı
        return air + rolling

    def drive(self, dt: float) -> None:
        """Gaza basılı: motor kuvveti - direnç."""
        grip = self.mass * 9.81 * 0.9                # lastik bundan fazlasını yere aktaramaz (patinaj)
        engine = 0.85 * self.power / max(self.speed, 1.0)  # güç sabitken hız artınca kuvvet azalır
        self.apply_force(min(grip, engine) - self.resistance(), dt)

    def brake(self, dt: float) -> None:
        """Frene basılı: ~0.8 g'lik sert fren + direnç."""
        self.apply_force(-self.mass * 8.0 - self.resistance(), dt)

    def coast(self, dt: float) -> None:
        """Hiçbir pedal yok: motor freni + direnç arabayı yavaşça durdurur."""
        engine_brake = self.mass * 0.4
        self.apply_force(-engine_brake - self.resistance(), dt)

    def apply_force(self, force: float, dt: float) -> None:
        """Newton'un 2. yasası: ivme = kuvvet / kütle. Hız 0'ın altına inmez."""
        acceleration = force / self.mass
        self.speed = max(0.0, self.speed + acceleration * dt)


def show(car: Car, pedal: str) -> None:
    """Hızı terminalde tek satırda, yerinde güncelleyerek gösterir."""
    kmh = car.speed_kmh()
    bar = "█" * int(kmh / 10)                    # her 10 km/sa için bir kare
    print(f"\r{pedal:<5} | {kmh:6.1f} km/sa | {bar:<35}", end="", flush=True)


def main() -> None:
    bentley = Car("Bentley", mass_kg=2300, power_kw=485)
    # Karşılaştırmak için alttaki satırın başındaki # işaretini kaldır:
    # bentley = Car("Fiat Egea", mass_kg=1250, power_kw=70)

    print(f"{bentley.brand} hazır.  G = gaz   F = fren   Boşluk = pedalı bırak   Q = çık")
    print("Hız tekrar 0 olunca program durur.\n")

    pedal = "BOŞ"
    dt = 0.05             # her adım 0,05 saniye (saniyede 20 güncelleme)
    moved = False         # araba hiç hareket etti mi?
    elapsed = 0.0
    zero_to_100 = None    # 0-100 km/sa süresi

    while True:
        # Basılan tuş varsa oku (yoksa beklemeden devam et)
        while msvcrt.kbhit():
            key = msvcrt.getwch().lower()
            if key == "g":
                pedal = "GAZ"
            elif key == "f":
                pedal = "FREN"
            elif key == " ":
                pedal = "BOŞ"
            elif key == "q":
                print("\nÇıkış yapıldı.")
                return

        if pedal == "GAZ":
            bentley.drive(dt)
        elif pedal == "FREN":
            bentley.brake(dt)
        else:
            bentley.coast(dt)

        if bentley.speed > 0:
            moved = True
            elapsed += dt
        if zero_to_100 is None and bentley.speed_kmh() >= 100:
            zero_to_100 = elapsed

        show(bentley, pedal)

        if moved and bentley.speed == 0:
            print("\n\nAraç durdu.")
            if zero_to_100 is not None:
                print(f"0-100 km/sa: {zero_to_100:.1f} saniye")
            break

        time.sleep(dt)


if __name__ == "__main__":
    main()
