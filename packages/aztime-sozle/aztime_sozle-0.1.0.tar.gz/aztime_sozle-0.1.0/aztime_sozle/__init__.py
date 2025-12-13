def time_to_words(time_str):
    try:
        clock_h,  minute_m = map(int, time_str.split(':'))
    except (ValueError,  IndexError):
        return "Xeta: Saat 'HH:MM' formatinda daxil edilmelidir."
    
    if not (0 <= clock_h <= 23 and 0 <= minute_m <= 59):
        return "Xeta: Saat ve ya deqiqe duzgun araliqda deyil."
    
    reqemler_sozle = {
        0: "tam", 1: "bir", 2: "iki", 3: "üç", 4: "dörd", 5: "beş", 6: "altı",
        7: "yeddi", 8: "səkkiz", 9: "doqquz", 10: "on", 11: "on bir", 12: "on iki",
        13: "on üç", 14: "on dörd", 15: "on beş", 16: "on altı", 17: "on yeddi",
        18: "on səkkiz", 19: "on doqquz", 20: "iyirmi", 21: "iyirmi bir", 22: "iyirmi iki",
        23: "iyirmi üç", 24: "iyirmi dörd", 25: "iyirmi beş", 26: "iyirmi altı",
        27: "iyirmi yeddi", 28: "iyirmi səkkiz", 29: "iyirmi doqquz", 30: "otuz"
    }

    clock_12 = clock_h % 12
    if clock_12 == 0:
        saat_sozle = reqemler_sozle.get(clock_12,  str(clock_12))
        return f"Saat **{saat_sozle}** tam"

    elif minute_m == 30:
        saat_sozle = reqemler_sozle.get(clock_12,  str(clock_12))
        return f"Saat **{saat_sozle}** yarim"
    
    elif 1 <= minute_m <= 29:
        deqiqe_sozle = reqemler_sozle.get(minute_m,  str(minute_m))
        saat_sozle = reqemler_sozle.get(clock_12,  str(clock_12))

        if minute_m == 1:
            return f"Saat **{saat_sozle}** bir deqiqe isleyib"
        
        return f"Saat **{saat_sozle}** **{deqiqe_sozle}** deqiqe işləyib"
    
    else:
        qalma_deqiqe = 60 - minute_m
        novbeti_saat = (clock_h + 1) % 24
        novbeti_saat_12 = novbeti_saat % 12 
        if novbeti_saat_12 == 0: novbeti_saat_12 = 12

        qalma_deqiqe_sozle = reqemler_sozle.get(qalma_deqiqe, str(qalma_deqiqe))
        novbet_saat_sozle = reqemler_sozle.get(novbeti_saat_12,  str(novbeti_saat_12))

        if qalma_deqiqe == 1:
            return f"Saat **{novbet_saat_sozle}**e bir deqiqe qalib"
        
        return f"Saat **{novbet_saat_sozle}**e  **{qalma_deqiqe_sozle}** deqiqe qalib"
    
if __name__ == "__main__":
    test_saatlar = ["10:38", "10:15", "10:30", "11:00", "00:01", "23:59", "12:45"]
    for t in test_saatlar:
        print(f"{t} -> {time_to_words(t)}")