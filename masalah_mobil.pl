% Definisi masalah
problem(ban_kempis).
problem(aki_kosong).
problem(mesin_berlebih_panas).
problem(rem_gagal).

% Gejala untuk masing-masing masalah
symptom(ban_kempis, tekanan_rendah).
symptom(ban_kempis, bocor).
symptom(aki_kosong, tidak_bisa_menyala).
symptom(aki_kosong, lampu_meredup).
symptom(mesin_berlebih_panas, suhu_tinggi).
symptom(mesin_berlebih_panas, kebocoran_pendingin).
symptom(rem_gagal, pedal_empuk).
symptom(rem_gagal, suara_mengerik).

% Aturan diagnosis: problem terdiagnosa jika semua gejalanya tercatat positif
diagnose(Problem) :-
    problem(Problem),
    forall(symptom(Problem, S), user_has(S)).
