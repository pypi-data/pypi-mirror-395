def time_to_words(time_str):
    """
    Daxil edilmiş saatı (HH:MM formatında) Azərbaycan dilində təbii və dəqiq şəkildə ifadə edir.
    Bütün 24 saatlıq formatlar (00:XX, 23:XX və s.) düzgün ifadə olunur.
    """
    try:
        clock_h, minute_m = map(int, time_str.split(':'))
    except (ValueError, IndexError):
        return "Xəta: Saat 'HH:MM' formatında daxil edilməlidir."

    if not (0 <= clock_h <= 23 and 0 <= minute_m <= 59):
        return "Xəta: Saat və ya dəqiqə düzgün aralıqda deyil."

    # Rəqəmlərin sözlə ifadəsi (0-dan 30-a qədər)
    reqemler_sozle = {
        0: "tam", 1: "bir", 2: "iki", 3: "üç", 4: "dörd", 5: "beş", 6: "altı",
        7: "yeddi", 8: "səkkiz", 9: "doqquz", 10: "on", 11: "on bir", 12: "on iki",
        13: "on üç", 14: "on dörd", 15: "on beş", 16: "on altı", 17: "on yeddi",
        18: "on səkkiz", 19: "on doqquz", 20: "iyirmi", 21: "iyirmi bir", 22: "iyirmi iki",
        23: "iyirmi üç", 24: "iyirmi dörd", 25: "iyirmi beş", 26: "iyirmi altı",
        27: "iyirmi yeddi", 28: "iyirmi səkkiz", 29: "iyirmi doqquz", 30: "otuz"
    }
    
    # ------------------ SAAT DƏYƏRLƏRİNİN HESABLANMASI ------------------
    
    # Cari saatın 12 saatlıq formatda rəqəmi
    cari_saat_12 = clock_h % 12
    if cari_saat_12 == 0:
        cari_saat_12 = 12

    # Növbəti saatın 12 saatlıq formatda rəqəmi
    novbeti_saat_h = (clock_h + 1) % 24
    novbeti_saat_12 = novbeti_saat_h % 12
    if novbeti_saat_12 == 0:
        novbeti_saat_12 = 12
        
    # ------------------ HALLARIN İDARƏ EDİLMƏSİ ------------------
    
    # 1. Tam Saat (XX:00)
    if minute_m == 0:
        saat_sozle = reqemler_sozle.get(cari_saat_12, str(cari_saat_12))
        return f"Saat **{saat_sozle}** tam"

    # 2. Yarım Saat (XX:30)
    elif minute_m == 30:
        saat_sozle = reqemler_sozle.get(cari_saat_12, str(cari_saat_12))
        return f"Saat **{saat_sozle}** yarım"

    # 3. İşləmə (Keçmə) forması (01-29 dəqiqələr)
    elif 1 <= minute_m <= 29:
        deqiqe_sozle = reqemler_sozle.get(minute_m, str(minute_m))
        
        # 00:XX (Gecə 12:01-12:29) üçün xüsusi hal: 12 yox, 1-i ifadə edirik.
        if clock_h == 0 and cari_saat_12 == 12:
            saat_sozle = "bir" # 00:15 -> Biri on beş dəqiqə işləyib
        else:
            saat_sozle = reqemler_sozle.get(cari_saat_12, str(cari_saat_12))
        
        if minute_m == 1:
            return f"Saat **{saat_sozle}** bir dəqiqə işləyib"
        
        return f"Saat **{saat_sozle}** **{deqiqe_sozle}** dəqiqə işləyib"

    # 4. Qalma forması (31-59 dəqiqələr)
    else: # 31 <= minute_m <= 59
        qalma_deqiqe = 60 - minute_m
        qalma_deqiqe_sozle = reqemler_sozle.get(qalma_deqiqe, str(qalma_deqiqe))
        novbeti_saat_sozle = reqemler_sozle.get(novbeti_saat_12, str(novbeti_saat_12))
        
        # 1 dəqiqə üçün xüsusi hal
        if qalma_deqiqe == 1:
            return f"Saat **{novbeti_saat_sozle}**ə bir dəqiqə qalıb"
        
        return f"Saat **{novbeti_saat_sozle}**ə **{qalma_deqiqe_sozle}** dəqiqə qalıb"

if __name__ == "__main__":
    print("--- Təkmilləşdirilmiş Azərbaycan Saati Testləri ---")
    
    test_saatlar = {
        "00:00": "Saat on iki tam",
        "00:01": "Saat biri bir dəqiqə işləyib",
        "09:30": "Saat doqquz yarım",
        "10:38": "Saat on birə iyirmi iki dəqiqə qalıb",
        "12:59": "Saat birə bir dəqiqə qalıb",
        "16:40": "Saat beşə iyirmi dəqiqə qalıb",
    }
    
    for t in test_saatlar:
        result = time_to_words(t)
        print(f"'{t}' -> '{result}'")