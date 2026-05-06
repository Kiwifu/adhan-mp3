import os
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = r"C:\Users\Badr\Desktop\Athan"

# (english_name, arabic_name, url)
RECITERS = [
    # Named reciters
    ("Rabeh Ibn Darah Al Jazairi", "رابح بن دراح الجزائري", "https://media.assabile.com/assabile/adhan_3435370/0bf83c80b583.mp3"),
    ("Ahmed El Kourdi", "أحمد الكردي", "https://media.assabile.com/assabile/adhan_3435370/8c052a5edec1.mp3"),
    ("Adham Al Sharqawe", "أدهم الشرقاوي", "https://media.assabile.com/assabile/adhan_3435370/cbcd8d249dcc.mp3"),
    ("Hamza Al Majale", "حمزة المجالي", "https://media.assabile.com/assabile/adhan_3435370/495dea4f4ea5.mp3"),
    ("Muhammad Al Damradash", "محمد الدمرداش", "https://media.assabile.com/assabile/adhan_3435370/cd17c7200df5.mp3"),
    ("Ismail Al Sheikh", "إسماعيل الشيخ", "https://media.assabile.com/assabile/adhan_3435370/6734c28f3a2d.mp3"),
    ("Muhammad Abu Al Maqarem", "محمد أبو المقارم", "https://media.assabile.com/assabile/adhan_3435370/d4f3a1736f99.mp3"),
    ("Al Duqale Muhammad Al Alam", "الدقالي محمد العلام", "https://media.assabile.com/assabile/adhan_3435370/c5c12e0cdba9.mp3"),
    ("Aby Yasser Al Jazaire", "أبو ياسر الجزائري", "https://media.assabile.com/assabile/adhan_3435370/3959e8c5f5d2.mp3"),
    ("Mohammed Salahuddin Kabbara 1", "محمد صلاح الدين كبارة", "https://media.assabile.com/assabile/adhan_3435370/6a992c01763d.mp3"),
    ("Mohammed Salahuddin Kabbara 2", "محمد صلاح الدين كبارة", "https://media.assabile.com/assabile/adhan_3435370/8bd66fa73ff9.mp3"),
    ("Abdel Moneim Abdel Mobdi", "عبد المنعم عبد المبدي", "https://media.assabile.com/assabile/adhan_3435370/c3460e1ab635.mp3"),
    ("Abdulah Al Maknawe", "عبدالله المكناوي", "https://media.assabile.com/assabile/adhan_3435370/af79859edca6.mp3"),
    ("Akhdam Bnu Al Madane", "أخدام بن المداني", "https://media.assabile.com/assabile/adhan_3435370/3d8ef25160a8.mp3"),
    ("Nasser Al Obaid 1", "ناصر العبيد", "https://media.assabile.com/assabile/adhan_3435370/c81e4e141865.mp3"),
    ("Nasser Al Obaid 2", "ناصر العبيد", "https://media.assabile.com/assabile/adhan_3435370/45299e6a8a68.mp3"),
    ("Nasser Al Obaid 3", "ناصر العبيد", "https://media.assabile.com/assabile/adhan_3435370/e6ced81e9955.mp3"),
    ("Tareq Fathe Ahmad", "طارق فتح أحمد", "https://media.assabile.com/assabile/adhan_3435370/290f81d9a73b.mp3"),
    ("Hecham Khalel", "هشام خليل", "https://media.assabile.com/assabile/adhan_3435370/bb9f1f375a27.mp3"),
    ("Hassan Salah Baalul", "حسن صالح بعلول", "https://media.assabile.com/assabile/adhan_3435370/a031983fa2b6.mp3"),
    ("Ahmed Al-Haddad", "أحمد الحداد", "https://media.assabile.com/assabile/adhan_3435370/f30b7631d625.mp3"),
    ("Mahmud Mustafa Al Najar", "محمود مصطفى النجار", "https://media.assabile.com/assabile/adhan_3435370/8e9025f379f2.mp3"),
    ("Samer Al Sagher", "سامر الصغير", "https://media.assabile.com/assabile/adhan_3435370/8ea93508d061.mp3"),
    ("BalBaSher Abdel Qadir", "بلباشر عبد القادر", "https://media.assabile.com/assabile/adhan_3435370/edc62005fb50.mp3"),
    ("Muhammed Ibrahem Ismael Abd Allah", "محمد إبراهيم إسماعيل عبدالله", "https://media.assabile.com/assabile/adhan_3435370/6df79edd050f.mp3"),
    ("Bnu Sawana 1", "بن سوانة", "https://media.assabile.com/assabile/adhan_3435370/0dbbe429d7d2.mp3"),
    ("Bnu Sawana 2", "بن سوانة", "https://media.assabile.com/assabile/adhan_3435370/ca039c2aa2ca.mp3"),
    ("Abdul Rahman Kassab 1", "عبدالرحمن كساب", "https://media.assabile.com/assabile/adhan_3435370/2cb233a7a776.mp3"),
    ("Abdul Rahman Kassab 2", "عبدالرحمن كساب", "https://media.assabile.com/assabile/adhan_3435370/0f9525955696.mp3"),
    ("Fares Abdul Ghane", "فارس عبد الغني", "https://media.assabile.com/assabile/adhan_3435370/82e70e435a79.mp3"),
    ("Hassan Mahmud Bare", "حسن محمود باره", "https://media.assabile.com/assabile/adhan_3435370/ddc60a4c3bc6.mp3"),
    ("Ezzedine Amarna", "عز الدين عمارنة", "https://media.assabile.com/assabile/adhan_3435370/651e00a18442.mp3"),
    ("Ahmad Al Aane", "أحمد العاني", "https://media.assabile.com/assabile/adhan_3435370/766e61f1a137.mp3"),
    ("Badee Jadu 1", "بديع جادو", "https://media.assabile.com/assabile/adhan_3435370/525b55254e29.mp3"),
    ("Badee Jadu 2", "بديع جادو", "https://media.assabile.com/assabile/adhan_3435370/a88b936d08a9.mp3"),
    ("Badee Jadu 3", "بديع جادو", "https://media.assabile.com/assabile/adhan_3435370/f0c14e23d534.mp3"),
    ("Al Ameen Muhammad Qanyouh", "الأمين محمد قانيوح", "https://media.assabile.com/assabile/adhan_3435370/591080dd2e06.mp3"),
    ("Zayd Al Aatya", "زيد العاطية", "https://media.assabile.com/assabile/adhan_3435370/097fd8491db6.mp3"),
    ("Jamal Abu Al Hamed Al Jaafare", "جمال أبو الحامد الجعفري", "https://media.assabile.com/assabile/adhan_3435370/83a95150c12f.mp3"),
    ("Islam Yassen", "إسلام ياسين", "https://media.assabile.com/assabile/adhan_3435370/12cd996ece7f.mp3"),
    ("Issa Al Hajlawe", "عيسى الهجلاوي", "https://media.assabile.com/assabile/adhan_3435370/a56ded8b4a29.mp3"),
    ("Abdul Rahman Majde", "عبدالرحمن ماجد", "https://media.assabile.com/assabile/adhan_3435370/ca451594384d.mp3"),
    ("Hamad Al Daghriri", "حمد الدغريري", "https://media.assabile.com/assabile/adhan_3435370/08008b8fec6c.mp3"),
    ("Ihssan Hamed Al Dulayme", "إحسان حامد الدليمي", "https://media.assabile.com/assabile/adhan_3435370/79a61f53cdbe.mp3"),
    ("Adal Malek Abdulah Al Massre", "عادل مالك عبدالله المصري", "https://media.assabile.com/assabile/adhan_3435370/acf3223cf1a5.mp3"),
    ("Muhammad Ben Mussa", "محمد بن موسى", "https://media.assabile.com/assabile/adhan_3435370/da87d1a24164.mp3"),
    ("Muhammad Abd Al Hakem", "محمد عبد الحكم", "https://media.assabile.com/assabile/adhan_3435370/7a837173da2c.mp3"),
    ("Mansur Al Zahrane", "منصور الزهراني", "https://media.assabile.com/assabile/adhan_3435370/cb51ad2c0c7e.mp3"),
    ("Wadi Hamad Al-Yamani", "وادي حمد اليماني", "https://media.assabile.com/assabile/adhan_3435370/091fa01b11f4.mp3"),
    ("Taleb Al Qanube", "طالب القنوبي", "https://media.assabile.com/assabile/adhan_3435370/731011a5ee48.mp3"),
    ("Muhammad Ramadan Saad - Al Haram Al Maki", "محمد رمضان سعد - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/e9bb86af0d30.mp3"),
    ("Ahmad Aamer Muhammad", "أحمد عامر محمد", "https://media.assabile.com/assabile/adhan_3435370/1994d371bfc1.mp3"),
    ("Fayz Abd Al Salam", "فايز عبد السلام", "https://media.assabile.com/assabile/adhan_3435370/d55c09c3357c.mp3"),
    ("Muhammad Fathe Hantur", "محمد فتحي حنتور", "https://media.assabile.com/assabile/adhan_3435370/f068e9a33c4e.mp3"),
    ("Omru Sobhe", "عمرو صبحي", "https://media.assabile.com/assabile/adhan_3435370/3a06c2aa464d.mp3"),
    ("Al Sayed Muslim", "السيد مسلم", "https://media.assabile.com/assabile/adhan_3435370/9d5456d06e1e.mp3"),
    ("Hussam Al Deen Obade", "حسام الدين عبادة", "https://media.assabile.com/assabile/adhan_3435370/c5c9053ff919.mp3"),
    ("Muhammad Ashraf Aawad", "محمد أشرف عوض", "https://media.assabile.com/assabile/adhan_3435370/0c7103f3a045.mp3"),
    ("Abdulah Al Sabaawe", "عبدالله الصباوي", "https://media.assabile.com/assabile/adhan_3435370/45bf762b4f22.mp3"),
    ("Muhammad Al Kurayne Al Maluke 1", "محمد القرين الملوكي", "https://media.assabile.com/assabile/adhan_3435370/229d65e40fdf.mp3"),
    ("Muhammad Al Kurayne Al Maluke 2", "محمد القرين الملوكي", "https://media.assabile.com/assabile/adhan_3435370/061632f7ec55.mp3"),
    ("Fawaz Farhan Al Dumane", "فواز فرحان الدماني", "https://media.assabile.com/assabile/adhan_3435370/7864560c8f5e.mp3"),
    ("Salem Hamde", "سالم حمدة", "https://media.assabile.com/assabile/adhan_3435370/b991587a0047.mp3"),
    ("Omran Mansur - Egypt", "عمران منصور - مصر", "https://media.assabile.com/assabile/adhan_3435370/68b0e4999e85.mp3"),
    ("Anuar Duman - Turkey", "أنوار دومان - تركيا", "https://media.assabile.com/assabile/adhan_3435370/4da17588fe1b.mp3"),
    ("Abdul Rahman Al Arake 1", "عبدالرحمن العراقي", "https://media.assabile.com/assabile/adhan_3435370/ee104f375ae5.mp3"),
    ("Abdul Rahman Al Arake 2", "عبدالرحمن العراقي", "https://media.assabile.com/assabile/adhan_3435370/f0e3b7062e99.mp3"),
    ("Abdul Rahman Al Arake 3", "عبدالرحمن العراقي", "https://media.assabile.com/assabile/adhan_3435370/06a860dce992.mp3"),
    ("Muhammad Hessen Al Shahawe", "محمد حسن الشهاوي", "https://media.assabile.com/assabile/adhan_3435370/3018380066dd.mp3"),
    ("Abdulah Al Dahbe - Egypt", "عبدالله الذهبي - مصر", "https://media.assabile.com/assabile/adhan_3435370/c2f802f38c47.mp3"),
    ("Ibraheem Jabr Abu Raheq - Fajr", "إبراهيم جبر أبو رحيق - الفجر", "https://media.assabile.com/assabile/adhan_3435370/dcc77fd7b6a1.mp3"),
    ("Ibraheem Jabr Abu Raheq", "إبراهيم جبر أبو رحيق", "https://media.assabile.com/assabile/adhan_3435370/e37acc95ebe1.mp3"),
    ("Tamer Islam", "تامر إسلام", "https://media.assabile.com/assabile/adhan_3435370/060a426e8644.mp3"),
    ("Yasser Abdu Allah Al Hawre - Qatar", "ياسر عبدالله الهوري - قطر", "https://media.assabile.com/assabile/adhan_3435370/1e21d991e100.mp3"),
    ("Waled Mahsas 1", "وليد محساس", "https://media.assabile.com/assabile/adhan_3435370/a07ffd1ae7fe.mp3"),
    ("Waled Mahsas 2 - Algeria", "وليد محساس - الجزائر", "https://media.assabile.com/assabile/adhan_3435370/c2f99053fed8.mp3"),
    ("Ahmad Fakhru - Qatar", "أحمد فخرو - قطر", "https://media.assabile.com/assabile/adhan_3435370/ac58ff63de71.mp3"),
    ("Ahmd At-Trablsy 1", "أحمد الطرابلسي", "https://media.assabile.com/assabile/adhan_3435370/69dbed4439df.mp3"),
    ("Ahmd At-Trablsy 2", "أحمد الطرابلسي", "https://media.assabile.com/assabile/adhan_3435370/ebfa3977664d.mp3"),
    ("Ahmd At-Trablsy 3", "أحمد الطرابلسي", "https://media.assabile.com/assabile/adhan_3435370/0ac57c399dc8.mp3"),
    ("Ahmd At-Trablsy 4", "أحمد الطرابلسي", "https://media.assabile.com/assabile/adhan_3435370/37a192967b75.mp3"),
    ("Ahmd At-Trablsy 5", "أحمد الطرابلسي", "https://media.assabile.com/assabile/adhan_3435370/9302b5c2153b.mp3"),
    ("Ahmd At-Trablsy - Fajr Kuwait", "أحمد الطرابلسي - فجر الكويت", "https://media.assabile.com/assabile/adhan_3435370/31f4182515ea.mp3"),
    ("Ahmad Al Batal", "أحمد البطل", "https://media.assabile.com/assabile/adhan_3435370/e675b3b07c97.mp3"),
    ("Riad Al Djazairi - Algeria", "رياض الجزائري - الجزائر", "https://media.assabile.com/assabile/adhan_3435370/c1e523eb696f.mp3"),
    ("Yaseen Al Aassaf 1", "ياسين الأسف", "https://media.assabile.com/assabile/adhan_3435370/e46d891b0acd.mp3"),
    ("Yaseen Al Aassaf 2 - Fajr Iraq", "ياسين الأسف - فجر العراق", "https://media.assabile.com/assabile/adhan_3435370/b0c404561e49.mp3"),
    ("Othman Al Masseme", "عثمان المسعمي", "https://media.assabile.com/assabile/adhan_3435370/7b64c1f6986a.mp3"),
    ("Ibraheem Al Jumayle", "إبراهيم الجميل", "https://media.assabile.com/assabile/adhan_3435370/a3194e614319.mp3"),
    ("Muhammad Nasser Al Dine Al Albane - Jordan", "محمد ناصر الدين الألباني - الأردن", "https://media.assabile.com/assabile/adhan_3435370/affead740cb6.mp3"),
    ("Yasser Al-Dosari - Saudi Arabia", "ياسر الدوسري - المملكة العربية السعودية", "https://media.assabile.com/assabile/adhan_3435370/f5370aa1a7e2.mp3"),
    ("Mohamed Siddiq El-Minshawi - Afghanistan", "محمد صديق المنشاوي - أفغانستان", "https://media.assabile.com/assabile/adhan_3435370/984f3e129c8c.mp3"),
    ("Mohamed Siddiq El-Minshawi - Egypt 1", "محمد صديق المنشاوي - مصر", "https://media.assabile.com/assabile/adhan_3435370/5771e6a59f2b.mp3"),
    ("Mohamed Siddiq El-Minshawi - Egypt 2", "محمد صديق المنشاوي - مصر", "https://media.assabile.com/assabile/adhan_3435370/a2b25725149e.mp3"),
    ("Muhammad Hamud - Colombia", "محمد حمود - كولومبيا", "https://media.assabile.com/assabile/adhan_3435370/f579c205b4b7.mp3"),
    ("Muhammad Hamud", "محمد حمود", "https://media.assabile.com/assabile/adhan_3435370/592e8a809f00.mp3"),
    ("Muhammad Najee 1", "محمد ناجي", "https://media.assabile.com/assabile/adhan_3435370/1d989d7b7507.mp3"),
    ("Muhammad Najee 2", "محمد ناجي", "https://media.assabile.com/assabile/adhan_3435370/08e9c70dc6bc.mp3"),
    ("Muhammad Najee 3", "محمد ناجي", "https://media.assabile.com/assabile/adhan_3435370/e028aa90ee1f.mp3"),
    ("Mukhtar Abelhamed Hafed", "مختار عبد الحميد حافظ", "https://media.assabile.com/assabile/adhan_3435370/61f9b6863789.mp3"),
    ("Ahmad Al Harasses", "أحمد الحراسيس", "https://media.assabile.com/assabile/adhan_3435370/23bbed4ace14.mp3"),
    ("Omar Al Kazabri", "عمر القزابري", "https://media.assabile.com/assabile/adhan_3435370/f77bff859f61.mp3"),
    ("Muhammad Al Saed Maher", "محمد السيد ماهر", "https://media.assabile.com/assabile/adhan_3435370/0e5fd7cf0c28.mp3"),
    ("Ibraheem Jabar 1", "إبراهيم جابر", "https://media.assabile.com/assabile/adhan_3435370/f477362a775e.mp3"),
    ("Ibraheem Jabar 2", "إبراهيم جابر", "https://media.assabile.com/assabile/adhan_3435370/671bd7114293.mp3"),
    ("Mustafa Waled", "مصطفى وليد", "https://media.assabile.com/assabile/adhan_3435370/11ecc060171f.mp3"),
    ("Mahmud Al Tawakh 1", "محمود الطواخ", "https://media.assabile.com/assabile/adhan_3435370/8cac04ba4137.mp3"),
    ("Mahmud Al Tawakh 2 - Masjid Al Rifai Cairo", "محمود الطواخ - مسجد الرفاعي القاهرة", "https://media.assabile.com/assabile/adhan_3435370/bdf9f3101b4c.mp3"),
    ("Kamal Muhammad Al Marush 1", "كمال محمد المرعوش", "https://media.assabile.com/assabile/adhan_3435370/faf99a86e98d.mp3"),
    ("Kamal Muhammad Al Marush 2 - Morocco", "كمال محمد المرعوش - المغرب", "https://media.assabile.com/assabile/adhan_3435370/dedbc7c0f60c.mp3"),
    ("Adam Abu Sakhra", "آدم أبو سخرة", "https://media.assabile.com/assabile/adhan_3435370/d9f8f948565c.mp3"),
    ("Ahmad Ali 1", "أحمد علي", "https://media.assabile.com/assabile/adhan_3435370/a0d6a4e20bc9.mp3"),
    ("Ahmad Ali 2 - Egypt", "أحمد علي - مصر", "https://media.assabile.com/assabile/adhan_3435370/f77eba62a35f.mp3"),
    ("Rabee Abdul Raheem Essa", "ربيع عبد الرحيم عيسى", "https://media.assabile.com/assabile/adhan_3435370/64775bf3b434.mp3"),
    ("Ahmad Ali Murtada", "أحمد علي مرتضى", "https://media.assabile.com/assabile/adhan_3435370/356f39051866.mp3"),
    ("Nasser Al Qatami 1 - Saudi Arabia", "ناصر القطامي - المملكة العربية السعودية", "https://media.assabile.com/assabile/adhan_3435370/6f509ec934a4.mp3"),
    ("Nasser Al Qatami 2 - Riyadh", "ناصر القطامي - الرياض", "https://media.assabile.com/assabile/adhan_3435370/d3aa494b7320.mp3"),
    ("Ali Ibn Ahmad Mala 1 - Al Haram Al Maki", "علي بن أحمد ملا - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/54944191e2e2.mp3"),
    ("Ali Ibn Ahmad Mala 2 - Al Haram Al Maki", "علي بن أحمد ملا - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/a3c148ae770f.mp3"),
    ("Ali Ibn Ahmad Mala 3 - Al Haram Al Maki", "علي بن أحمد ملا - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/a4ab138564ce.mp3"),
    ("Ali Ibn Ahmad Mala 4 - Al Haram Al Maki", "علي بن أحمد ملا - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/77873f64ead9.mp3"),
    ("Ali Ibn Ahmad Mala 5 - Al Haram Al Maki", "علي بن أحمد ملا - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/166d1f7c435a.mp3"),
    ("Ali Ibn Ahmad Mala 6 - Al Haram Al Maki", "علي بن أحمد ملا - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/3b44ab2cf844.mp3"),
    ("Muhammad Khaleel Raml - Al Haram Al Maki", "محمد خليل رمل - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/c7ba5fb672b3.mp3"),
    ("Nayf Fedah - Al Haram Al Maki", "نايف فداح - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/7f701468a8dc.mp3"),
    ("Faruq Abdul Rahman Hadrawe - Al Haram Al Maki", "فاروق عبدالرحمن حضراوي - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/1aadb2df7d5c.mp3"),
    ("Assem Bukhrare - Al Haram Al Maki", "عاصم بخراري - الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/7487fa449eeb.mp3"),
    ("Mishary Rashid Alafasy 1 - Kuwait", "مشاري راشد العفاسي - الكويت", "https://media.assabile.com/assabile/adhan_3435370/b45e93f1efb3.mp3"),
    ("Mishary Rashid Alafasy 2 - Kuwait", "مشاري راشد العفاسي - الكويت", "https://media.assabile.com/assabile/adhan_3435370/e9ab8052fdb8.mp3"),
    ("Mishary Rashid Alafasy 3 - Fajr Kuwait", "مشاري راشد العفاسي - فجر الكويت", "https://media.assabile.com/assabile/adhan_3435370/ddb21f7363eb.mp3"),
    ("Mishary Rashid Alafasy 4 - Fajr Kuwait", "مشاري راشد العفاسي - فجر الكويت", "https://media.assabile.com/assabile/adhan_3435370/b91e1c5095cd.mp3"),
    ("Abdulbasit Abdusamad 1 - Egypt", "عبد الباسط عبد الصمد - مصر", "https://media.assabile.com/assabile/adhan_3435370/1a014366658c.mp3"),
    ("Abdulbasit Abdusamad 2 - Egypt", "عبد الباسط عبد الصمد - مصر", "https://media.assabile.com/assabile/adhan_3435370/0e56abfb1eb3.mp3"),
    ("Abdulbasit Abdusamad 3 - Egypt", "عبد الباسط عبد الصمد - مصر", "https://media.assabile.com/assabile/adhan_3435370/566852c1d145.mp3"),
    ("Abdulbasit Abdusamad 4 - Egypt", "عبد الباسط عبد الصمد - مصر", "https://media.assabile.com/assabile/adhan_3435370/d336be9b95d7.mp3"),
    ("Abdulbasit Abdusamad 5 - Cairo", "عبد الباسط عبد الصمد - القاهرة", "https://media.assabile.com/assabile/adhan_3435370/02f1bec971bb.mp3"),
    ("Abdulbasit Abdusamad 6 - Fajr Egypt", "عبد الباسط عبد الصمد - فجر مصر", "https://media.assabile.com/assabile/adhan_3435370/1125f640d83b.mp3"),
    ("Abdulbasit Abdusamad 7 - Fajr Egypt", "عبد الباسط عبد الصمد - فجر مصر", "https://media.assabile.com/assabile/adhan_3435370/4318b757fd42.mp3"),
    ("Mustafa Ismail - Egypt", "مصطفى إسماعيل - مصر", "https://media.assabile.com/assabile/adhan_3435370/dd5f42239b71.mp3"),
    ("Mahmoud Khalil Al Hussary - Cairo", "محمود خليل الحصري - القاهرة", "https://media.assabile.com/assabile/adhan_3435370/cdb24a4bd658.mp3"),
    ("Abul Ainain Shuaisha - Cairo", "أبو العينين شعيشع - القاهرة", "https://media.assabile.com/assabile/adhan_3435370/414827669391.mp3"),
    ("Ahmed Nuinaa 1 - Egypt", "أحمد نعينع - مصر", "https://media.assabile.com/assabile/adhan_3435370/97ff79250506.mp3"),
    ("Ahmed Nuinaa 2 - Cairo", "أحمد نعينع - القاهرة", "https://media.assabile.com/assabile/adhan_3435370/da48b2a26635.mp3"),
    ("Mahmoud Ali Al Banna - Cairo", "محمود علي البنا - القاهرة", "https://media.assabile.com/assabile/adhan_3435370/48f9d6984758.mp3"),
    ("Muhammad Refaat - Cairo", "محمد رفعت - القاهرة", "https://media.assabile.com/assabile/adhan_3435370/d8a3a72860e8.mp3"),
    ("NurDin Hamza Al Maghriby - Al Aqsa Jerusalem", "نور الدين حمزة المغربي - المسجد الأقصى القدس", "https://media.assabile.com/assabile/adhan_3435370/768559b47c2e.mp3"),
    ("Najee Qazaz - Al Aqsa Jerusalem", "ناجي قزاز - المسجد الأقصى القدس", "https://media.assabile.com/assabile/adhan_3435370/c888cbd50d15.mp3"),
    ("Ahmad Al Amade 1 - Qatar", "أحمد العمادي - قطر", "https://media.assabile.com/assabile/adhan_3435370/232673ccf543.mp3"),
    ("Ahmad Al Amade 2 - Qatar", "أحمد العمادي - قطر", "https://media.assabile.com/assabile/adhan_3435370/3cf9690b4671.mp3"),
    ("Al Saed Metwale AL Aal", "السيد متولي الآل", "https://media.assabile.com/assabile/adhan_3435370/152f81cfd66c.mp3"),
    ("Hamdan Al Maleke - Najran Saudi Arabia", "حمدان الملكي - نجران السعودية", "https://media.assabile.com/assabile/adhan_3435370/2bdf5fda46cf.mp3"),
    ("Mahde Al Bechee", "مهدي البشي", "https://media.assabile.com/assabile/adhan_3435370/9847153e75b3.mp3"),
    ("Zaher Muhammad Taresh", "زاهر محمد طريش", "https://media.assabile.com/assabile/adhan_3435370/7ab8c2883671.mp3"),
    ("Abd Alrazaq Saleh - Lebanon", "عبد الرزاق صالح - لبنان", "https://media.assabile.com/assabile/adhan_3435370/83d71480327a.mp3"),
    ("Hamza Al Halabea", "حمزة الحلبي", "https://media.assabile.com/assabile/adhan_3435370/4fa42504da3b.mp3"),
    ("Abdu Al Karem Jabare", "عبد الكريم جابري", "https://media.assabile.com/assabile/adhan_3435370/e659e9128faf.mp3"),
    ("Al Bahlul Abu Arqub 1", "البهلول أبو عرقوب", "https://media.assabile.com/assabile/adhan_3435370/d319fff24477.mp3"),
    ("Al Bahlul Abu Arqub 2", "البهلول أبو عرقوب", "https://media.assabile.com/assabile/adhan_3435370/1077f911aaf9.mp3"),
    ("Saheb Hane Khatab - Palestine", "صاحب هاني خطاب - فلسطين", "https://media.assabile.com/assabile/adhan_3435370/7879228bc194.mp3"),
    ("Ahmad Nawaf Al Mejlad 1", "أحمد نواف المجلد", "https://media.assabile.com/assabile/adhan_3435370/e5ed59196ed9.mp3"),
    ("Ahmad Nawaf Al Mejlad 2 - Fajr", "أحمد نواف المجلد - الفجر", "https://media.assabile.com/assabile/adhan_3435370/5862e9e11c7a.mp3"),
    ("Haj Sulaiman Mukhtar - Algeria", "حاج سليمان مختار - الجزائر", "https://media.assabile.com/assabile/adhan_3435370/251cb703bcad.mp3"),
    ("Hassan Khalfan - Qatar", "حسن خلفان - قطر", "https://media.assabile.com/assabile/adhan_3435370/ebdaa88540dd.mp3"),
    ("Saleh Al Nabet - Qatar", "صالح النابت - قطر", "https://media.assabile.com/assabile/adhan_3435370/ac16894fd536.mp3"),
    ("Ali Hassan Abd Al Khaliq - Qatar", "علي حسن عبد الخالق - قطر", "https://media.assabile.com/assabile/adhan_3435370/27662a08c410.mp3"),
    ("Muad Al Qaseme - Qatar", "معاذ القاسمي - قطر", "https://media.assabile.com/assabile/adhan_3435370/492b38278518.mp3"),
    ("Nasser Al Abd Al Jabar - Qatar", "ناصر عبد الجبار - قطر", "https://media.assabile.com/assabile/adhan_3435370/f0c25ce57633.mp3"),
    ("Hafed Hessen Erq", "حافظ حسين عرق", "https://media.assabile.com/assabile/adhan_3435370/aeab77ef8810.mp3"),
    # Location-only entries
    ("Adhan Al Haram Al Madani - Al Madinah 1", "أذان الحرم المدني - المدينة المنورة", "https://media.assabile.com/assabile/adhan_3435370/b30ca9a3e115.mp3"),
    ("Adhan Al Haram Al Madani - Al Madinah 2", "أذان الحرم المدني - المدينة المنورة", "https://media.assabile.com/assabile/adhan_3435370/c84496bf1a8c.mp3"),
    ("Adhan Al Aqsa - Jerusalem", "أذان المسجد الأقصى - القدس", "https://media.assabile.com/assabile/adhan_3435370/03fb23407291.mp3"),
    ("Adhan Malaysia 1", "أذان ماليزيا", "https://media.assabile.com/assabile/adhan_3435370/9024ca483958.mp3"),
    ("Adhan Malaysia 2", "أذان ماليزيا", "https://media.assabile.com/assabile/adhan_3435370/153d445c4ae6.mp3"),
    ("Adhan Georgia", "أذان جورجيا", "https://media.assabile.com/assabile/adhan_3435370/cb6f68b97ea0.mp3"),
    ("Adhan Pakistan", "أذان باكستان", "https://media.assabile.com/assabile/adhan_3435370/fec1f7e9250e.mp3"),
    ("Adhan Tunisia", "أذان تونس", "https://media.assabile.com/assabile/adhan_3435370/09215c77c5f0.mp3"),
    ("Adhan India", "أذان الهند", "https://media.assabile.com/assabile/adhan_3435370/a0bb07fedee7.mp3"),
    ("Adhan Muscat Oman", "أذان مسقط عُمان", "https://media.assabile.com/assabile/adhan_3435370/062d856eb556.mp3"),
    ("Adhan Maldives", "أذان جزر المالديف", "https://media.assabile.com/assabile/adhan_3435370/1a8c8b301ac8.mp3"),
    ("Adhan Syria", "أذان سوريا", "https://media.assabile.com/assabile/adhan_3435370/a5a348cb518f.mp3"),
    ("Adhan Brunei 1", "أذان بروناي", "https://media.assabile.com/assabile/adhan_3435370/9118dfdd28be.mp3"),
    ("Adhan Brunei 2", "أذان بروناي", "https://media.assabile.com/assabile/adhan_3435370/31a9285c3ca6.mp3"),
    ("Adhan Brunei 3", "أذان بروناي", "https://media.assabile.com/assabile/adhan_3435370/2f7c04a67a24.mp3"),
    ("Adhan Ajman UAE", "أذان عجمان الإمارات", "https://media.assabile.com/assabile/adhan_3435370/19de39ba56eb.mp3"),
    ("Adhan Dubai UAE", "أذان دبي الإمارات", "https://media.assabile.com/assabile/adhan_3435370/c1dea6614fdb.mp3"),
    ("Adhan Turkey 1", "أذان تركيا", "https://media.assabile.com/assabile/adhan_3435370/3073e5ff27a5.mp3"),
    ("Adhan Turkey 2", "أذان تركيا", "https://media.assabile.com/assabile/adhan_3435370/baab3a1b17ef.mp3"),
    ("Adhan Masjid Al Rajehe Saudi Arabia 1", "أذان مسجد الراجحي السعودية", "https://media.assabile.com/assabile/adhan_3435370/81c22585afb5.mp3"),
    ("Adhan Masjid Al Rajehe Saudi Arabia 2", "أذان مسجد الراجحي السعودية", "https://media.assabile.com/assabile/adhan_3435370/d03e858bb952.mp3"),
    ("Adhan Masjid Al Rajehe Saudi Arabia 3", "أذان مسجد الراجحي السعودية", "https://media.assabile.com/assabile/adhan_3435370/101c4a790ab1.mp3"),
    ("Adhan Kuwait", "أذان الكويت", "https://media.assabile.com/assabile/adhan_3435370/a4af4ff71c86.mp3"),
    ("Adhan Indonesia", "أذان إندونيسيا", "https://media.assabile.com/assabile/adhan_3435370/426b72f6444f.mp3"),
    ("Adhan Riyadh Saudi Arabia", "أذان الرياض السعودية", "https://media.assabile.com/assabile/adhan_3435370/5a91acdece6e.mp3"),
    ("Adhan Kenya", "أذان كينيا", "https://media.assabile.com/assabile/adhan_3435370/7d55981e66d4.mp3"),
    ("Adhan Fajr Al Haram Al Maki", "أذان الفجر الحرم المكي", "https://media.assabile.com/assabile/adhan_3435370/518b4e081437.mp3"),
    ("Adhan Fajr Al Haram Al Madani", "أذان الفجر الحرم المدني", "https://media.assabile.com/assabile/adhan_3435370/efc564e3b1d2.mp3"),
    ("Adhan Fajr Algeria", "أذان الفجر الجزائر", "https://media.assabile.com/assabile/adhan_3435370/5e35645d76b2.mp3"),
    ("Adhan Fajr Umm Al Quwain", "أذان الفجر أم القيوين", "https://media.assabile.com/assabile/adhan_3435370/bb596a0f509b.mp3"),
    ("Adhan Fajr Cairo Egypt", "أذان الفجر القاهرة مصر", "https://media.assabile.com/assabile/adhan_3435370/b97727c9dffc.mp3"),
    ("Adhan Fajr Kuwait 1", "أذان الفجر الكويت", "https://media.assabile.com/assabile/adhan_3435370/cd03fc75a7f2.mp3"),
    ("Adhan Fajr Kuwait 2", "أذان الفجر الكويت", "https://media.assabile.com/assabile/adhan_3435370/c6bbb7699f82.mp3"),
]

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '-', name)

def download_file(entry):
    en_name, ar_name, url = entry
    filename = sanitize_filename(f"{en_name} ({ar_name}).mp3")
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        return f"SKIP {filename}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        with open(filepath, "wb") as f:
            f.write(data)
        return f"OK   {filename}"
    except Exception as e:
        return f"FAIL {filename} — {e}"

print(f"Downloading {len(RECITERS)} adhan recordings to {OUTPUT_DIR}\n")

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(download_file, entry): entry for entry in RECITERS}
    ok = fail = skip = 0
    for future in as_completed(futures):
        result = future.result()
        print(result)
        if result.startswith("OK"):
            ok += 1
        elif result.startswith("FAIL"):
            fail += 1
        else:
            skip += 1

print(f"\nDone. {ok} downloaded, {skip} skipped (already exist), {fail} failed.")
