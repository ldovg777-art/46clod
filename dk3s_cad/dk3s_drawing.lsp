;;; ============================================================================
;;;  dk3s_drawing.lsp  —  Чертёж общего вида датчика концентрации ДК-3С-210АВ
;;;  Версия: 1.1.0  (2026-09-19)
;;;  Платформа: nanoCAD / AutoCAD / BricsCAD / ZWCAD (AutoLISP, только entmake)
;;;
;;;  Источник геометрии:
;;;    - «Техническое описание K1» (англ.), стр. 16 — монтажный чертёж датчика
;;;      (векторная графика, масштаб восстановлен по размеру 411 мм);
;;;    - Fig. 1 (общий вид), Fig. 4 (узел рабочего электрода: Ø1,4 мм, выступ 2 мм).
;;;
;;;  Команда:  DK3S   — строит чертёж (формат А3, масштаб 1:2) в текущем документе.
;;;            Всё в пространстве модели: датчик 1:1, рамка и надписи увеличены в 2 раза,
;;;            печать листа с масштабом 1:2 даёт А3.
;;;
;;;  Кириллица в строках записана как \U+XXXX — работает при любой кодировке файла.
;;;  Все размеры вынесены в таблицу параметров (раздел 1) — правьте только её.
;;; ============================================================================

;;; ---------------------------------------------------------------------------
;;; 1. ТАБЛИЦА ПАРАМЕТРОВ (мм). Ось Z — вдоль датчика от вершины скобы,
;;;    R — радиус/смещение от оси. В главном виде Z направлена вправо, R — вверх.
;;; ---------------------------------------------------------------------------

;; --- Лист и оформление --------------------------------------------------------
(setq g_dk3s_sheet_w      420.0)   ; формат А3 (альбомный), мм бумаги
(setq g_dk3s_sheet_h      297.0)
(setq g_dk3s_scale_den    2.0)     ; знаменатель масштаба главного вида (1:2)
(setq g_dk3s_detail_mul   4.0)     ; выносной элемент А: 4x в модели = 2:1 на листе
(setq g_dk3s_font         "GOST.shx")       ; шрифт надписей как в чертежах ЭКОР (стиль GOST, наклон 15); в поставке nanoCAD его нет:
                                           ; скопировать GOST.shx в C:\ProgramData\Nanosoft\nanoCAD XX\SHX или поставить "CS_Gost2304.shx"
(setq g_dk3s_txt_h        3.5)     ; высота текста на бумаге, мм
(setq g_dk3s_font_k       1.08)    ; запас по ширине надписей сверх пропорций ГОСТ 2.304 тип Б (другой шрифт, подмена)
;; толщины линий (сотые мм) как в чертежах ЭКОР: контур 0,6; тонкие 0,3; рамка 0,6; размеры и текст 0,25
(setq g_dk3s_lw_main 60)  (setq g_dk3s_lw_thin 30)  (setq g_dk3s_lw_frame 60)  (setq g_dk3s_lw_dim 25)
(setq g_dk3s_designation  "302123.000 \\U+0412\\U+041E")   ; обозначение: 302123.000 - перв. примен. деталей корпуса (уточнить!)
(setq g_dk3s_name1        "\\U+0414\\U+0430\\U+0442\\U+0447\\U+0438\\U+043A \\U+043A\\U+043E\\U+043D\\U+0446\\U+0435\\U+043D\\U+0442\\U+0440\\U+0430\\U+0446\\U+0438\\U+0438")
(setq g_dk3s_name2        "\\U+0414\\U+041A-3\\U+0421-210\\U+0410\\U+0412")
(setq g_dk3s_name3        "\\U+041E\\U+0431\\U+0449\\U+0438\\U+0439 \\U+0432\\U+0438\\U+0434")
(setq g_dk3s_org1         "\\U+041E\\U+041E\\U+041E \\U+041D\\U+0422\\U+041F \"\\U+042D\\U+043A\\U+043E\\U+0440\"")   ; графа организации 50x15, две строки
(setq g_dk3s_org2         "\\U+041B\\U+044C\\U+0432\\U+043E\\U+0432")
(setq g_dk3s_author       "")      ; Разраб. (фамилия)
(setq g_dk3s_checker      "")      ; Пров.

;; --- Защитная скоба и наконечник ---------------------------------------------
(setq g_dk3s_guard_h      15.6)    ; высота скобы над торцом гильзы
(setq g_dk3s_guard_w      28.0)    ; ширина скобы (наружная)
(setq g_dk3s_guard_d      2.0)     ; диаметр проволоки скобы
(setq g_dk3s_guard_r      4.0)     ; наружный радиус гиба скобы
(setq g_dk3s_tip_off      5.5)     ; смещение оси наконечника от оси датчика
(setq g_dk3s_tip_d        7.0)     ; наконечник: шестигранник 1/4" (S6,35, по углам 7,3)
(setq g_dk3s_tip_s        6.35)    ; размер под ключ наконечника
(setq g_dk3s_tip_len      18.0)    ; длина шестигранной части наконечника
(setq g_dk3s_tip_cone     2.5)     ; длина конуса наконечника
(setq g_dk3s_tip_nose_d   2.0)     ; диаметр торца конуса
(setq g_dk3s_tip_vis      3.7)     ; выступ шестигранника над торцом гильзы
(setq g_dk3s_we_d         1.4)     ; рабочий электрод: проволока Ø1,4
(setq g_dk3s_we_len       2.0)     ; выступ рабочего электрода из наконечника
(setq g_dk3s_tube_d       6.0)     ; защитная трубка токоотвода (наружный Ø)
(setq g_dk3s_tube_wall    0.5)     ; стенка защитной трубки
(setq g_dk3s_tap_d        3.0)     ; токоотвод рабочего электрода (резьба шаг 0,5)
(setq g_dk3s_tip_bore_len 15.0)    ; глубина резьбового отверстия в наконечнике

;; --- Защитная гильза ----------------------------------------------------------
(setq g_dk3s_z_sleeve     15.6)    ; торец гильзы
(setq g_dk3s_sleeve_d     32.0)    ; наружный диаметр гильзы
(setq g_dk3s_hole_d       6.0)     ; перфорация: диаметр отверстий
(setq g_dk3s_hole_z1      25.5)    ; первое фронтальное отверстие (от вершины скобы)
(setq g_dk3s_hole_pitch   20.0)    ; шаг отверстий в ряду
(setq g_dk3s_hole_n       3)       ; отверстий во фронтальном ряду
(setq g_dk3s_hole_side_n  2)       ; боковых отверстий на сторону (в шахматном порядке)

;; --- Корпус 714.761.000 (S46, M42x3, фланец Ø59, длина 61), гайка нажимная 714.541.000 (S36, M33x2) ---
(setq g_dk3s_z_shell      224.8)   ; торец резьбы M42x3 корпуса (правый торец корпуса 285.8, длина 61 h12)
(setq g_dk3s_shell_d      42.0)    ; наружный диаметр резьбы M42x3-6f
(setq g_dk3s_thread_pitch 3.0)
(setq g_dk3s_shell_ch     1.0)     ; фаска торца корпуса 1x45
(setq g_dk3s_z_relief     253.8)   ; начало проточки перед фланцем (34 от торца до фланца)
(setq g_dk3s_relief_d     39.0)
(setq g_dk3s_z_plate      258.8)   ; фланец-пластина
(setq g_dk3s_plate_d      59.0)
(setq g_dk3s_z_hex1       265.8)   ; шестигранник S46 корпуса
(setq g_dk3s_hex1_s       46.0)
(setq g_dk3s_hex1_e       52.0)    ; по углам S46 (Ø52 по чертежу корпуса 714.761.000); фаска 30° со стороны гайки
(setq g_dk3s_z_cyl        285.8)   ; правый торец корпуса; далее видимая резьба M33x2 гайки нажимной
(setq g_dk3s_cyl_d        33.0)    ; M33x2-6g гайки
(setq g_dk3s_thread2_pitch 2.0)
(setq g_dk3s_z_groove     293.2)   ; канавка Ø30 x 3 у шестигранника гайки
(setq g_dk3s_groove_d     30.0)
(setq g_dk3s_z_hex2       296.6)   ; шестигранник S36 гайки нажимной (длина 10, фаска 30° с наружного торца)
(setq g_dk3s_hex2_s       36.0)
(setq g_dk3s_hex2_e       41.0)    ; по углам S36 (Ø41 по чертежу гайки 714.541.000)
(setq g_dk3s_z_neck       306.6)   ; труба электродного узла Ø20,8 (проходит через гайку и грундбуксу)
(setq g_dk3s_neck_d       20.8)
(setq g_dk3s_z_step       314.6)   ; ступень Ø18,8
(setq g_dk3s_step_d       18.8)
(setq g_dk3s_z_taper      315.6)   ; конус Ø16 -> Ø15,4
(setq g_dk3s_taper_d1     16.0)
(setq g_dk3s_taper_d2     15.4)
(setq g_dk3s_z_tag        325.2)   ; бирка с заводским номером
(setq g_dk3s_tag_w        16.0)
(setq g_dk3s_z_tag_end    335.1)

;; --- Токоотводы, мостики, хомуты ----------------------------------------------
(setq g_dk3s_bridge_d     3.2)     ; электролитический мостик (трубка)
(setq g_dk3s_bridge_r     4.6)     ; ось мостика от оси датчика (прижат к трубке Ø6)
(setq g_dk3s_z_clamp1     367.0)   ; хомуты (начало), длина и диаметр
(setq g_dk3s_z_clamp2     467.2)
(setq g_dk3s_clamp_len    7.6)
(setq g_dk3s_clamp_d      13.6)
(setq g_dk3s_z_bend       476.0)   ; начало разводки мостиков к электродам сравнения
(setq g_dk3s_z_we_end     483.7)   ; конец трубки Ø6, начало разъёма WE
(setq g_dk3s_conn_collar_d 8.0)    ; разъём (штырь): буртик, корпус, штырь
(setq g_dk3s_conn_collar_l 2.0)
(setq g_dk3s_conn_body_d  6.5)
(setq g_dk3s_conn_body_l  14.0)
(setq g_dk3s_conn_pin_d   2.5)
(setq g_dk3s_conn_pin_l   14.0)
(setq g_dk3s_conn_tip_l   1.0)
(setq g_dk3s_se_r         -24.6)   ; ось провода вспомогательного электрода (снизу)
(setq g_dk3s_se_d         3.0)
(setq g_dk3s_z_se_start   283.7)
(setq g_dk3s_z_se_end     481.9)

;; --- Электроды сравнения (2 шт.) ----------------------------------------------
(setq g_dk3s_re_r         22.8)    ; ось электрода сравнения от оси датчика
(setq g_dk3s_re_d         20.0)
(setq g_dk3s_z_re         521.7)   ; верх (начало) электрода сравнения
(setq g_dk3s_re_seg1      24.1)    ; первый сегмент
(setq g_dk3s_re_neck      3.0)     ; перемычка Ø16
(setq g_dk3s_re_neck_d    16.0)
(setq g_dk3s_re_seg2      34.0)    ; второй сегмент
(setq g_dk3s_re_gap       1.0)     ; зазор до буртика штыря

;; --- Итоговые (вычисляются) ---------------------------------------------------
(setq g_dk3s_z_re_end     (+ g_dk3s_z_re g_dk3s_re_seg1 g_dk3s_re_neck g_dk3s_re_seg2))   ; 582.8
(setq g_dk3s_z_total      (+ g_dk3s_z_re_end g_dk3s_re_gap g_dk3s_conn_body_l 1.0
                             g_dk3s_conn_pin_l g_dk3s_conn_tip_l))                         ; 613.8

;;; ---------------------------------------------------------------------------
;;; 2. СЛУЖЕБНЫЕ ПЕРЕМЕННЫЕ (не править)
;;; ---------------------------------------------------------------------------
(setq g_dk3s_lay_main   "DK3S_CONTOUR")   ; основные линии 0,5
(setq g_dk3s_lay_thin   "DK3S_THIN")      ; тонкие линии 0,25 (штриховка, выноски)
(setq g_dk3s_lay_axis   "DK3S_AXIS")      ; осевые
(setq g_dk3s_lay_dim    "DK3S_DIM")       ; размеры
(setq g_dk3s_lay_text   "DK3S_TEXT")      ; надписи
(setq g_dk3s_lay_frame  "DK3S_FRAME")     ; рамка и основная надпись
(setq g_dk3s_style      "DK3S_GOST")      ; текстовый стиль
(setq g_dk3s_dimstyle   "DK3S")           ; размерный стиль
(setq g_dk3s_ltype_axis "DK3S_CENTER")    ; тип линии осевых
(setq g_dk3s_ox 0.0)  (setq g_dk3s_oy 0.0)  (setq g_dk3s_k 1.0)   ; текущее начало/масштаб вида
(setq g_dk3s_dim_mode "entmake")          ; "entmake" | "command" (авто-переключение при сбое)
(setq g_dk3s_stage "")                    ; текущая стадия построения (FSM, для диагностики)
(setq g_dk3s_cnt 0)                       ; счётчик созданных примитивов

;;; ---------------------------------------------------------------------------
;;; 3. ПРИМИТИВЫ (entmake). Все координаты — модель, мм.
;;; ---------------------------------------------------------------------------

;; Точка вида: z вдоль оси, r поперёк; учитывает начало и масштаб текущего вида
(defun dk3s_p (z r)
  (list (+ g_dk3s_ox (* g_dk3s_k z)) (+ g_dk3s_oy (* g_dk3s_k r)) 0.0)
)

;; Точка листа (абсолютная)
(defun dk3s_ps (x y) (list x y 0.0))

;; Масштабированная длина (для радиусов, высот текста в текущем виде)
(defun dk3s_l (v) (* g_dk3s_k v))

(defun dk3s_deg (a) (* 180.0 (/ a pi)))
(defun dk3s_rad (a) (* pi (/ a 180.0)))


;; Число строкой с запятой в качестве разделителя (ЕСКД), prec — знаков после запятой
(defun dk3s_num (v prec / s i c r)
  (setq s (rtos v 2 prec) r "" i 1)
  (while (<= i (strlen s))
    (setq c (substr s i 1))
    (setq r (strcat r (if (= c ".") "," c)))
    (setq i (1+ i))
  )
  r
)


;; Число видимых знаков в строке: код \U+XXXX (7 символов) считается одним знаком
(defun dk3s_strlen_vis (s / i n)
  (setq i 1 n 0)
  (while (<= i (strlen s))
    (if (= (substr s i 3) "\\U+") (setq i (+ i 7)) (setq i (1+ i)))
    (setq n (1+ n))
  )
  n
)

;; Учёт созданного примитива
(defun dk3s_made (r) (if r (setq g_dk3s_cnt (1+ g_dk3s_cnt))) r)

(defun dk3s_line (p1 p2 lay)
  (dk3s_made (entmake (list '(0 . "LINE") '(100 . "AcDbEntity") (cons 8 lay)
                            '(100 . "AcDbLine") (cons 10 p1) (cons 11 p2))))
)

(defun dk3s_circle (c r lay)
  (dk3s_made (entmake (list '(0 . "CIRCLE") '(100 . "AcDbEntity") (cons 8 lay)
                            '(100 . "AcDbCircle") (cons 10 c) (cons 40 r))))
)

;; Дуга: углы в градусах, против часовой стрелки от a1 к a2
(defun dk3s_arc (c r a1 a2 lay)
  (dk3s_made (entmake (list '(0 . "ARC") '(100 . "AcDbEntity") (cons 8 lay)
                            '(100 . "AcDbCircle") (cons 10 c) (cons 40 r)
                            '(100 . "AcDbArc") (cons 50 a1) (cons 51 a2))))
)

;; Дуга через три точки p1 -> p2 -> p3 (p2 — любая промежуточная точка дуги); точки — модель
(defun dk3s_arc3 (p1 p2 p3 lay / ax ay bx by cx cy d ux uy c a1 a2 a3 tw)
  (setq ax (car p1) ay (cadr p1) bx (car p2) by (cadr p2) cx (car p3) cy (cadr p3))
  (setq d (* 2.0 (+ (* ax (- by cy)) (* bx (- cy ay)) (* cx (- ay by)))))
  (setq ux (/ (+ (* (+ (* ax ax) (* ay ay)) (- by cy)) (* (+ (* bx bx) (* by by)) (- cy ay))
                 (* (+ (* cx cx) (* cy cy)) (- ay by))) d)
        uy (/ (+ (* (+ (* ax ax) (* ay ay)) (- cx bx)) (* (+ (* bx bx) (* by by)) (- ax cx))
                 (* (+ (* cx cx) (* cy cy)) (- bx ax))) d))
  (setq c (list ux uy 0.0) tw (* 2.0 pi))
  (setq a1 (angle c p1) a2 (angle c p2) a3 (angle c p3))
  ;; против часовой от a1 к a3 должна лежать a2, иначе дуга идёт от a3 к a1
  (if (< (rem (+ (- a2 a1) tw tw) tw) (rem (+ (- a3 a1) tw tw) tw))
    (dk3s_arc c (distance c p1) (dk3s_deg a1) (dk3s_deg a3) lay)
    (dk3s_arc c (distance c p1) (dk3s_deg a3) (dk3s_deg a1) lay))
)

;; Полилиния по списку 3D-точек; closed = T/nil; width — постоянная ширина
(defun dk3s_pline (pts closed width lay / lst)
  (setq lst (list '(0 . "LWPOLYLINE") '(100 . "AcDbEntity") (cons 8 lay)
                  '(100 . "AcDbPolyline") (cons 90 (length pts))
                  (cons 70 (if closed 1 0)) (cons 43 width)))
  (foreach p pts (setq lst (append lst (list (list 10 (car p) (cadr p))))))
  (dk3s_made (entmake lst))
)

;; Прямоугольник по двум противоположным углам (замкнутая полилиния)
(defun dk3s_rect (p1 p2 lay)
  (dk3s_pline (list p1 (list (car p2) (cadr p1) 0.0) p2 (list (car p1) (cadr p2) 0.0)) T 0.0 lay)
)

;; Закрашенная точка (полилиния из двух дуг с шириной = диаметру)
(defun dk3s_dot (c d lay / lst)
  (setq lst (list '(0 . "LWPOLYLINE") '(100 . "AcDbEntity") (cons 8 lay)
                  '(100 . "AcDbPolyline") '(90 . 2) '(70 . 1) (cons 43 d)
                  (list 10 (- (car c) (/ d 4.0)) (cadr c)) '(42 . 1.0)
                  (list 10 (+ (car c) (/ d 4.0)) (cadr c)) '(42 . 1.0)))
  (dk3s_made (entmake lst))
)

;; Эллипс через полилинию (портативно: без entmake ELLIPSE)
;; c — центр, a — полуось по X, b — полуось по Y
(defun dk3s_ellipse (c a b lay / i n pts ang)
  (setq n 32 i 0 pts nil)
  (while (< i n)
    (setq ang (* 2.0 pi (/ i (float n))))
    (setq pts (cons (list (+ (car c) (* a (cos ang))) (+ (cadr c) (* b (sin ang))) 0.0) pts))
    (setq i (1+ i))
  )
  (dk3s_pline (reverse pts) T 0.0 lay)
)

;; Текст: p — точка вставки, h — высота, rot — градусы,
;; just — 0 левый/низ, 1 центр/центр, 2 правый/низ, 3 центр/низ, 4 левый/середина
(defun dk3s_text (p h str rot just lay)
  (dk3s_text_wf p h str rot just lay 1.0)
)

;; То же с коэффициентом ширины wf (группа 41): так в штампах ЭКОР подгоняют надпись под графу
(defun dk3s_text_wf (p h str rot just lay wf / hj vj)
  (cond ((= just 1) (setq hj 1 vj 2))
        ((= just 2) (setq hj 2 vj 0))
        ((= just 3) (setq hj 1 vj 0))
        ((= just 4) (setq hj 0 vj 2))
        (T (setq hj 0 vj 0)))
  (dk3s_made (entmake (list '(0 . "TEXT") '(100 . "AcDbEntity") (cons 8 lay)
                            '(100 . "AcDbText") (cons 10 p) (cons 40 h) (cons 1 str)
                            (cons 50 rot) (cons 41 wf) (cons 7 g_dk3s_style) (cons 72 hj) (cons 11 p)
                            '(100 . "AcDbText") (cons 73 vj))))
)

;; Оценка ширины надписи (в единицах h) при коэффициенте ширины 1 — с запасом, по пропорциям
;; шрифта ГОСТ 2.304 тип Б (таков CS_Gost2304.shx nanoCAD; GOST.shx ЭКОР тоже широкий — в их
;; штампах подписи сжаты до 0,6-0,95): прописная 0,8h, строчная и цифра 0,7h, пробел 0,6h,
;; точка, запятая, скобки, дефис 0,45h; плюс вынос наклона 15 градусов 0,27h.
;; Коды кириллицы (обратный слэш, U+, четыре цифры) считаются одним знаком.
(defun dk3s_text_w (s h / i n c k w)
  (setq i 1 w 0.0 n (strlen s))
  (while (<= i n)
    (setq c (ascii (substr s i 1)))
    (if (and (= c 92) (= (substr s (1+ i) 2) "U+"))
      (progn
        (setq k (dk3s_hex4 (substr s (+ i 3) 4)))
        (setq w (+ w (cond ((or (= k 1025) (and (>= k 1040) (<= k 1071))) 0.8)
                           ((= k 8470) 1.0)
                           (T 0.7))))
        (setq i (+ i 7)))
      (progn
        (setq w (+ w (cond ((and (>= c 65) (<= c 90)) 0.8)
                           ((= c 32) 0.6)
                           ((member c '(33 34 39 40 41 44 45 46 58 59 73 105 108)) 0.45)
                           (T 0.7))))
        (setq i (1+ i)))))
  (* h (+ w 0.27) g_dk3s_font_k)
)

;; Четыре шестнадцатеричные цифры -> целое (для кодов кириллицы)
(defun dk3s_hex4 (s / i c r)
  (setq i 1 r 0)
  (while (<= i (strlen s))
    (setq c (ascii (substr s i 1)))
    (setq r (+ (* r 16) (cond ((<= c 57) (- c 48)) ((<= c 70) (- c 55)) (T (- c 87)))))
    (setq i (1+ i)))
  r
)

;; Перенос по словам: первая строка не шире w1, следующие не шире w2 (единицы модели)
(defun dk3s_wrap (s h w1 w2 / words cur res i c lim)
  (setq words nil cur "" i 1)
  (while (<= i (strlen s))
    (setq c (substr s i 1))
    (if (= c " ")
      (progn (if (/= cur "") (setq words (cons cur words))) (setq cur ""))
      (setq cur (strcat cur c)))
    (setq i (1+ i)))
  (if (/= cur "") (setq words (cons cur words)))
  (setq words (reverse words) res nil cur "" lim w1)
  (foreach wd words
    (if (and (/= cur "") (> (dk3s_text_w (strcat cur " " wd) h) lim))
      (setq res (cons cur res) cur wd lim w2)
      (setq cur (if (= cur "") wd (strcat cur " " wd)))))
  (if (/= cur "") (setq res (cons cur res)))
  (reverse res)
)

;; Штриховка выпуклого многоугольника линиями под 45° с шагом pitch (тонкие линии)
(defun dk3s_hatch_poly (pts pitch lay / xs ys cmin cmax c i n p1 p2 ts t1 t2 d x0 y0 x1 y1 den tt)
  (setq xs (mapcar 'car pts) ys (mapcar 'cadr pts))
  ;; линии y = x + c ; c от min(y-x) до max(y-x)
  (setq cmin (apply 'min (mapcar '- ys xs)) cmax (apply 'max (mapcar '- ys xs)))
  (setq d (* pitch (sqrt 2.0)))
  (setq c (+ cmin (/ d 2.0)))
  (setq n (length pts))
  (while (< c cmax)
    ;; пересечения линии y = x + c с рёбрами многоугольника; параметр t = x
    (setq ts nil i 0)
    (while (< i n)
      (setq p1 (nth i pts) p2 (nth (rem (1+ i) n) pts))
      (setq x0 (car p1) y0 (cadr p1) x1 (car p2) y1 (cadr p2))
      ;; ребро: (x,y) = p1 + s*(p2-p1), s in [0,1]; решаем y0 + s*dy = x0 + s*dx + c
      (setq den (- (- y1 y0) (- x1 x0)))
      (if (> (abs den) 1e-9)
        (progn
          (setq tt (/ (- (+ x0 c) y0) den))
          (if (and (>= tt -1e-9) (<= tt (+ 1.0 1e-9)))
            (setq ts (cons (+ x0 (* tt (- x1 x0))) ts))
          )
        )
      )
      (setq i (1+ i))
    )
    (if (>= (length ts) 2)
      (progn
        (setq t1 (apply 'min ts) t2 (apply 'max ts))
        (if (> (- t2 t1) 1e-6)
          (dk3s_line (list t1 (+ t1 c) 0.0) (list t2 (+ t2 c) 0.0) lay)
        )
      )
    )
    (setq c (+ c d))
  )
)

;;; ---------------------------------------------------------------------------
;;; 4. ТАБЛИЦЫ: слои, тип линии, текстовый и размерный стили
;;; ---------------------------------------------------------------------------

(defun dk3s_make_ltype ()
  (if (not (tblsearch "LTYPE" g_dk3s_ltype_axis))
    (if (not (entmake (list '(0 . "LTYPE") '(100 . "AcDbSymbolTableRecord")
                            '(100 . "AcDbLinetypeTableRecord") (cons 2 g_dk3s_ltype_axis)
                            '(70 . 0) '(3 . "GOST 2.303-5 ____ _ ____ _ ____") '(72 . 65) '(73 . 4)
                            '(40 . 24.0) '(49 . 20.0) '(74 . 0) '(49 . -1.5) '(74 . 0)
                            '(49 . 1.0) '(74 . 0) '(49 . -1.5) '(74 . 0))))
      (setq g_dk3s_ltype_axis "Continuous")   ; запасной вариант — сплошная
    )
  )
)

;; Слой: color — номер цвета, lw — толщина в сотых мм (50 = 0,5 мм)
(defun dk3s_make_layer (name color ltype lw)
  (if (not (tblsearch "LAYER" name))
    (if (not (entmake (list '(0 . "LAYER") '(100 . "AcDbSymbolTableRecord")
                            '(100 . "AcDbLayerTableRecord") (cons 2 name) '(70 . 0)
                            (cons 62 color) (cons 6 ltype) (cons 370 lw))))
      ;; запасной вариант — через команду
      (command "_.-LAYER" "_M" name "_C" (itoa color) name "_L" ltype name "")
    )
  )
)

(defun dk3s_make_style ()
  (if (not (tblsearch "STYLE" g_dk3s_style))
    (if (not (entmake (list '(0 . "STYLE") '(100 . "AcDbSymbolTableRecord")
                            '(100 . "AcDbTextStyleTableRecord") (cons 2 g_dk3s_style)
                            '(70 . 0) '(40 . 0.0) '(41 . 1.0) '(50 . 15.0) '(71 . 0)
                            (cons 42 (* g_dk3s_txt_h g_dk3s_scale_den))
                            (cons 3 g_dk3s_font) '(4 . ""))))
      (setq g_dk3s_style "Standard")   ; запасной вариант — стандартный стиль
    )
  )
)

;; Размерный стиль как GOSTMTM/ЕСКД в чертежах ЭКОР: текст 3,5, стрелки 3,0, выносные 1,25,
;; отступ 0,625, зазор 0,625, DIMSCALE = знаменатель масштаба, запятая, нули подавляются, текст над линией
(defun dk3s_make_dimstyle ( / st lst)
  (if (not (tblsearch "DIMSTYLE" g_dk3s_dimstyle))
    (progn
      (setq lst (list '(0 . "DIMSTYLE") '(100 . "AcDbSymbolTableRecord")
                      '(100 . "AcDbDimStyleTableRecord") (cons 2 g_dk3s_dimstyle) '(70 . 0)
                      (cons 40 g_dk3s_scale_den)   ; DIMSCALE
                      '(41 . 3.0)                  ; DIMASZ
                      '(42 . 0.625)                ; DIMEXO
                      '(43 . 7.0)                  ; DIMDLI
                      '(44 . 1.25)                 ; DIMEXE
                      (cons 140 g_dk3s_txt_h)      ; DIMTXT
                      '(144 . 1.0)                 ; DIMLFAC
                      '(147 . 0.625)               ; DIMGAP
                      '(73 . 0) '(74 . 0)          ; DIMTIH DIMTOH — текст вдоль линии
                      '(77 . 1)                    ; DIMTAD — текст над линией
                      '(78 . 8)                    ; DIMZIN — без хвостовых нулей
                      '(271 . 1)                   ; DIMDEC — один знак
                      '(278 . 44)                  ; DIMDSEP — запятая
                      '(279 . 1)                   ; DIMTMOVE
                      '(171 . 2) '(172 . 0) '(174 . 0) '(175 . 0) '(176 . 0) '(177 . 0)))
      (if (setq st (tblobjname "STYLE" g_dk3s_style))
        (setq lst (append lst (list (cons 340 st))))     ; DIMTXSTY
      )
      (if (not (entmake lst))
        (progn
          ;; запасной вариант: переменные текущего стиля + размеры командой
          (setq g_dk3s_dim_mode "command")
          (setvar "DIMSCALE" g_dk3s_scale_den) (setvar "DIMASZ" 3.0) (setvar "DIMEXO" 0.625)
          (setvar "DIMEXE" 1.25) (setvar "DIMTXT" g_dk3s_txt_h) (setvar "DIMGAP" 0.625)
          (setvar "DIMTIH" 0) (setvar "DIMTOH" 0) (setvar "DIMTAD" 1) (setvar "DIMZIN" 8)
          (setvar "DIMDEC" 1) (setvar "DIMDSEP" ",") (setvar "DIMTXSTY" g_dk3s_style)
        )
      )
    )
  )
)

;;; ---------------------------------------------------------------------------
;;; 5. РАЗМЕРЫ И ВЫНОСКИ
;;; ---------------------------------------------------------------------------

;; Линейный размер. p1, p2 — точки объекта; pd — точка на размерной линии;
;; rot — 0 (горизонтальный) или 90 (вертикальный); txt — "" (авто) или переопределение
;; ("%%c<>" — диаметр, "S<>" — под ключ и т.п.)
(defun dk3s_dim (p1 p2 pd rot txt / r)
  (if (= g_dk3s_dim_mode "entmake")
    (progn
      (setq r (entmake (list '(0 . "DIMENSION") '(100 . "AcDbEntity") (cons 8 g_dk3s_lay_dim)
                             '(100 . "AcDbDimension") (cons 10 pd) '(70 . 32) (cons 1 txt)
                             (cons 3 g_dk3s_dimstyle)
                             '(100 . "AcDbAlignedDimension") (cons 13 p1) (cons 14 p2)
                             (cons 50 rot) '(100 . "AcDbRotatedDimension"))))
      (if r
        (dk3s_made r)
        (setq g_dk3s_dim_mode "command")   ; entmake не прошёл — переключаемся на команду
      )
    )
  )
  (if (/= g_dk3s_dim_mode "entmake")
    (progn
      (if (= txt "")
        (command "_.DIMLINEAR" p1 p2 (if (= rot 90) "_V" "_H") pd)
        (command "_.DIMLINEAR" p1 p2 (if (= rot 90) "_V" "_H") "_T" txt pd)
      )
      (setq g_dk3s_cnt (1+ g_dk3s_cnt))
    )
  )
)

;; Выноска: точка на детали (с точкой), излом, полка и текст над полкой
;; pt — точка на детали, ps — начало полки, dir — 1 полка вправо, -1 влево
(defun dk3s_leader (pt ps dir str / h w g pe)
  (setq h (* g_dk3s_txt_h g_dk3s_scale_den))
  (setq w (dk3s_text_w str h))                   ; ширина надписи (ГОСТ 2.304 тип Б, с запасом)
  (setq g (* 0.3 h))                             ; полка выступает за выноску: надпись не касается выноски
  (setq pe (list (+ (car ps) (* dir (+ w g))) (cadr ps) 0.0))
  (dk3s_dot pt (* 0.5 g_dk3s_scale_den) g_dk3s_lay_thin)
  (dk3s_line pt ps g_dk3s_lay_thin)
  (dk3s_line ps pe g_dk3s_lay_thin)
  ;; надпись прижата к выноске: вправо — от левого края, влево — от правого (лишняя ширина уходит от выноски)
  (dk3s_text (list (+ (car ps) (* dir g)) (+ (cadr ps) (* 0.25 h)) 0.0)
             h str 0.0 (if (> dir 0) 0 2) g_dk3s_lay_text)
)

;;; ---------------------------------------------------------------------------
;;; 6. РАМКА И ОСНОВНАЯ НАДПИСЬ (ГОСТ 2.104, форма 1, 185x55)
;;;    Все размеры бумаги умножаются на g_dk3s_scale_den.
;;; ---------------------------------------------------------------------------

;; Линия внутри основной надписи по координатам бумаги (мм от левого нижнего угла штампа);
;; основные (толстые) линии — слой рамки, тонкие (строки по 5 мм, подграфы) — тонкий слой
(defun dk3s_tb_line (x1 y1 x2 y2)
  (dk3s_line (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x1)) (+ g_dk3s_tby (* g_dk3s_scale_den y1)))
             (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x2)) (+ g_dk3s_tby (* g_dk3s_scale_den y2)))
             g_dk3s_lay_frame)
)
(defun dk3s_tb_thin (x1 y1 x2 y2)
  (dk3s_line (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x1)) (+ g_dk3s_tby (* g_dk3s_scale_den y1)))
             (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x2)) (+ g_dk3s_tby (* g_dk3s_scale_den y2)))
             g_dk3s_lay_thin)
)

;; Текст в штампе: x,y — бумага (мм от угла штампа), h — высота на бумаге, just — как в dk3s_text
(defun dk3s_tb_text (x y h str just)
  (dk3s_text (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x)) (+ g_dk3s_tby (* g_dk3s_scale_den y)))
             (* h g_dk3s_scale_den) str 0.0 just g_dk3s_lay_text)
)

;; Текст в штампе, подогнанный по ширине: не шире maxw (мм бумаги), иначе сжатие по ширине
(defun dk3s_tb_fit (x y h str just maxw / w wf)
  (setq w (dk3s_text_w str h))
  (setq wf (if (> w maxw) (/ maxw w) 1.0))
  (dk3s_text_wf (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x)) (+ g_dk3s_tby (* g_dk3s_scale_den y)))
                (* h g_dk3s_scale_den) str 0.0 just g_dk3s_lay_text wf)
)

(defun dk3s_draw_frame ( / s w h x0 y0 x1 y1 gx0 gx1)
  (setq s g_dk3s_scale_den w (* s g_dk3s_sheet_w) h (* s g_dk3s_sheet_h))
  ;; граница листа (тонкая) и рамка (основная): поля 20 слева, 5 остальные
  (dk3s_rect (dk3s_ps 0.0 0.0) (dk3s_ps w h) g_dk3s_lay_thin)
  (setq x0 (* s 20.0) y0 (* s 5.0) x1 (- w (* s 5.0)) y1 (- h (* s 5.0)))
  (dk3s_rect (dk3s_ps x0 y0) (dk3s_ps x1 y1) g_dk3s_lay_frame)
  ;; основная надпись — правый нижний угол рамки
  (setq g_dk3s_tbx (- x1 (* s 185.0)) g_dk3s_tby y0)
  (dk3s_tb_line 0.0 0.0 0.0 55.0)  (dk3s_tb_line 0.0 55.0 185.0 55.0)
  ;; левая часть 65 мм: вертикали основные, строки по 5 тонкие, граница табл. изменений основная
  (dk3s_tb_line 65.0 0.0 65.0 55.0)
  (dk3s_tb_line 7.0 30.0 7.0 55.0)   (dk3s_tb_line 17.0 0.0 17.0 55.0)
  (dk3s_tb_line 40.0 0.0 40.0 55.0)  (dk3s_tb_line 55.0 0.0 55.0 55.0)
  (dk3s_tb_line 0.0 30.0 65.0 30.0)
  (foreach yy '(5.0 10.0 15.0 20.0 25.0 35.0 40.0 45.0 50.0) (dk3s_tb_thin 0.0 yy 65.0 yy))
  ;; правая часть 120 мм (форма 1): обозначение 120x15; наименование 70x25, материал 70x15;
  ;; справа 50 мм: Лит./Масса/Масштаб 15/17/18 (подписи 5, значения 15), Лист/Листов 20/30 (5), организация 15
  (dk3s_tb_line 65.0 40.0 185.0 40.0)   ; низ графы обозначения
  (dk3s_tb_line 65.0 15.0 135.0 15.0)   ; низ графы наименования
  (dk3s_tb_line 135.0 0.0 135.0 40.0)
  (dk3s_tb_line 135.0 35.0 185.0 35.0)  (dk3s_tb_line 135.0 20.0 185.0 20.0)
  (dk3s_tb_line 135.0 15.0 185.0 15.0)
  (dk3s_tb_line 150.0 20.0 150.0 40.0)  (dk3s_tb_line 167.0 20.0 167.0 40.0)
  (dk3s_tb_thin 140.0 20.0 140.0 35.0)  (dk3s_tb_thin 145.0 20.0 145.0 35.0)
  (dk3s_tb_line 155.0 15.0 155.0 20.0)
  ;; подписи граф 3 мм, как в чертежах ЭКОР; не входит в графу (с зазором 1 мм с каждой стороны) — сжатие по ширине, как у ЭКОР
  (dk3s_tb_fit 3.5 31.0 3.0 "\\U+0418\\U+0437\\U+043C." 3 5.0)       (dk3s_tb_fit 12.0 31.0 3.0 "\\U+041B\\U+0438\\U+0441\\U+0442" 3 8.0)
  (dk3s_tb_fit 28.5 31.0 3.0 "\\U+2116 \\U+0434\\U+043E\\U+043A\\U+0443\\U+043C." 3 21.0) (dk3s_tb_fit 47.5 31.0 3.0 "\\U+041F\\U+043E\\U+0434\\U+043F." 3 13.0)
  (dk3s_tb_fit 60.0 31.0 3.0 "\\U+0414\\U+0430\\U+0442\\U+0430" 3 8.0)
  (dk3s_tb_fit 1.0 26.0 3.0 "\\U+0420\\U+0430\\U+0437\\U+0440\\U+0430\\U+0431." 0 15.0)   (dk3s_tb_fit 1.0 21.0 3.0 "\\U+041F\\U+0440\\U+043E\\U+0432." 0 15.0)
  (dk3s_tb_fit 1.0 16.0 3.0 "\\U+0422.\\U+043A\\U+043E\\U+043D\\U+0442\\U+0440." 0 15.0)  (dk3s_tb_fit 1.0 6.0 3.0 "\\U+041D.\\U+043A\\U+043E\\U+043D\\U+0442\\U+0440." 0 15.0)
  (dk3s_tb_fit 1.0 1.0 3.0 "\\U+0423\\U+0442\\U+0432." 0 15.0)
  (dk3s_tb_fit 142.5 36.0 3.0 "\\U+041B\\U+0438\\U+0442." 3 13.0)    (dk3s_tb_fit 158.5 36.0 3.0 "\\U+041C\\U+0430\\U+0441\\U+0441\\U+0430" 3 15.0)
  (dk3s_tb_fit 176.0 36.0 3.0 "\\U+041C\\U+0430\\U+0441\\U+0448\\U+0442\\U+0430\\U+0431" 3 16.0)
  (dk3s_tb_fit 136.5 16.0 3.0 "\\U+041B\\U+0438\\U+0441\\U+0442" 0 8.0)     (dk3s_tb_fit 156.5 16.0 3.0 "\\U+041B\\U+0438\\U+0441\\U+0442\\U+043E\\U+0432" 0 12.0)
  ;; дополнительные графы (ГОСТ 2.104, форма 2): левое поле снизу вверх 25/35/25/25/35,
  ;; сверху "Перв. примен." и "Справ. №" по 60; графа обозначения 70x14 на верхней рамке
  (setq gx0 (* s 8.0) gx1 x0)
  (dk3s_line (dk3s_ps gx0 y0) (dk3s_ps gx0 (+ y0 (* s 145.0))) g_dk3s_lay_frame)
  (foreach yy '(25.0 60.0 85.0 110.0 145.0)
    (dk3s_line (dk3s_ps gx0 (+ y0 (* s yy))) (dk3s_ps gx1 (+ y0 (* s yy))) g_dk3s_lay_frame))
  (foreach g (list (list 12.5 "\\U+0418\\U+043D\\U+0432. \\U+2116 \\U+043F\\U+043E\\U+0434\\U+043B.") (list 42.5 "\\U+041F\\U+043E\\U+0434\\U+043F. \\U+0438 \\U+0434\\U+0430\\U+0442\\U+0430") (list 72.5 "\\U+0412\\U+0437\\U+0430\\U+043C. \\U+0438\\U+043D\\U+0432. \\U+2116")
                   (list 97.5 "\\U+0418\\U+043D\\U+0432. \\U+2116 \\U+0434\\U+0443\\U+0431\\U+043B.") (list 127.5 "\\U+041F\\U+043E\\U+0434\\U+043F. \\U+0438 \\U+0434\\U+0430\\U+0442\\U+0430"))
    (dk3s_text (dk3s_ps (+ gx0 (* s 6.0)) (+ y0 (* s (car g)))) (* 2.5 s) (cadr g) 90.0 1 g_dk3s_lay_text))
  (dk3s_line (dk3s_ps gx0 (- y1 (* s 120.0))) (dk3s_ps gx0 y1) g_dk3s_lay_frame)
  (foreach yy '(60.0 120.0)
    (dk3s_line (dk3s_ps gx0 (- y1 (* s yy))) (dk3s_ps gx1 (- y1 (* s yy))) g_dk3s_lay_frame))
  (dk3s_text (dk3s_ps (+ gx0 (* s 6.0)) (- y1 (* s 30.0))) (* 2.5 s) "\\U+041F\\U+0435\\U+0440\\U+0432. \\U+043F\\U+0440\\U+0438\\U+043C\\U+0435\\U+043D." 90.0 1 g_dk3s_lay_text)
  (dk3s_text (dk3s_ps (+ gx0 (* s 6.0)) (- y1 (* s 90.0))) (* 2.5 s) "\\U+0421\\U+043F\\U+0440\\U+0430\\U+0432. \\U+2116" 90.0 1 g_dk3s_lay_text)
  (dk3s_rect (dk3s_ps x0 (- y1 (* s 14.0))) (dk3s_ps (+ x0 (* s 70.0)) y1) g_dk3s_lay_frame)
  (dk3s_text (dk3s_ps (+ x0 (* s 35.0)) (- y1 (* s 7.0))) (* 5.0 s) g_dk3s_designation 180.0 1 g_dk3s_lay_text)
  ;; под основной надписью
  (dk3s_text (dk3s_ps (+ g_dk3s_tbx (* s 100.0)) (- y0 (* s 4.0))) (* 2.5 s) "\\U+041A\\U+043E\\U+043F\\U+0438\\U+0440\\U+043E\\U+0432\\U+0430\\U+043B" 0.0 3 g_dk3s_lay_text)
  (dk3s_text (dk3s_ps (+ g_dk3s_tbx (* s 165.0)) (- y0 (* s 4.0))) (* 2.5 s) "\\U+0424\\U+043E\\U+0440\\U+043C\\U+0430\\U+0442 \\U+04103" 0.0 3 g_dk3s_lay_text)
  ;; содержимое граф
  (dk3s_tb_fit 125.0 45.5 5.0 g_dk3s_designation 3 116.0)
  (dk3s_tb_fit 100.0 33.5 4.0 g_dk3s_name1 3 66.0)
  (dk3s_tb_fit 100.0 26.0 4.0 g_dk3s_name2 3 66.0)
  (dk3s_tb_fit 100.0 18.5 4.0 g_dk3s_name3 3 66.0)
  (dk3s_tb_text 176.0 27.5 5.0 (strcat "1:" (rtos g_dk3s_scale_den 2 0)) 1)
  (dk3s_tb_text 148.0 16.0 3.0 "1" 0)       (dk3s_tb_text 176.0 16.0 3.0 "1" 0)
  (dk3s_tb_fit 160.0 8.5 3.5 g_dk3s_org1 3 46.0)
  (dk3s_tb_fit 160.0 3.0 3.5 g_dk3s_org2 3 46.0)
  (dk3s_tb_fit 18.0 26.0 3.0 g_dk3s_author 0 22.0)
  (dk3s_tb_fit 18.0 21.0 3.0 g_dk3s_checker 0 22.0)
)

;;; ---------------------------------------------------------------------------
;;; 7. ГЛАВНЫЙ ВИД: узлы датчика (координаты z, r — таблица параметров)
;;; ---------------------------------------------------------------------------

;; Образующие цилиндра (две продольные линии) от z1 до z2 при радиусе r, ось на r0
(defun dk3s_cyl (z1 z2 r r0)
  (dk3s_line (dk3s_p z1 (+ r0 r)) (dk3s_p z2 (+ r0 r)) g_dk3s_lay_main)
  (dk3s_line (dk3s_p z1 (- r0 r)) (dk3s_p z2 (- r0 r)) g_dk3s_lay_main)
)

;; Торцевая линия при z от r1 до r2
(defun dk3s_face (z r1 r2)
  (dk3s_line (dk3s_p z r1) (dk3s_p z r2) g_dk3s_lay_main)
)

;; Шестигранник в боковой проекции (по углам к наблюдателю: видны три грани), как в чертежах ЭКОР.
;; z1 — торец без фаски, z2 — торец с фаской 30 градусов до диаметра s; s — под ключ, e — по углам.
;; Фаска режет рёбра на глубине c = (e - s)/2 * tg30; на каждой грани — дуга через концы рёбер
;; и середину грани на торце (у гайки ЭКОР 714.541.000 так совпадает до 0,02 мм).
(defun dk3s_hex (z1 z2 s e / c zc ys)
  (setq c (* (/ (- e s) 2.0) (/ (sin (dk3s_rad 30.0)) (cos (dk3s_rad 30.0)))))
  (setq zc (if (> z2 z1) (- z2 c) (+ z2 c)))          ; конец рёбер у фаски
  (setq ys (* s (/ (sqrt 3.0) 4.0)))                   ; середина боковой грани в проекции
  (dk3s_cyl z1 zc (/ e 2.0) 0.0)                       ; крайние рёбра
  (dk3s_cyl z1 zc (/ e 4.0) 0.0)                       ; рёбра средней грани
  (dk3s_face z1 (/ e -2.0) (/ e 2.0))                  ; торец без фаски
  (dk3s_face z2 (/ s -2.0) (/ s 2.0))                  ; торец с фаской (окружность фаски = s)
  (dk3s_line (dk3s_p z2 (/ s 2.0)) (dk3s_p zc (/ e 2.0)) g_dk3s_lay_main)
  (dk3s_line (dk3s_p z2 (/ s -2.0)) (dk3s_p zc (/ e -2.0)) g_dk3s_lay_main)
  (dk3s_arc3 (dk3s_p zc (/ e -4.0)) (dk3s_p z2 0.0) (dk3s_p zc (/ e 4.0)) g_dk3s_lay_main)
  (dk3s_arc3 (dk3s_p zc (/ e 4.0)) (dk3s_p z2 ys) (dk3s_p zc (/ e 2.0)) g_dk3s_lay_main)
  (dk3s_arc3 (dk3s_p zc (/ e -2.0)) (dk3s_p z2 (- ys)) (dk3s_p zc (/ e -4.0)) g_dk3s_lay_main)
  e
)

;; Разъём-штырь токоотвода: буртик, корпус, штырь с острием; z0 — начало, r0 — ось
(defun dk3s_connector (z0 r0 / z1 z2 z3 z4 rp)
  (setq z1 (+ z0 g_dk3s_conn_collar_l) z2 (+ z1 g_dk3s_conn_body_l)
        z3 (+ z2 1.0 g_dk3s_conn_pin_l) z4 (+ z3 g_dk3s_conn_tip_l) rp (/ g_dk3s_conn_pin_d 2.0))
  (dk3s_face z0 (- r0 (/ g_dk3s_conn_collar_d 2.0)) (+ r0 (/ g_dk3s_conn_collar_d 2.0)))
  (dk3s_cyl z0 z1 (/ g_dk3s_conn_collar_d 2.0) r0)
  (dk3s_face z1 (- r0 (/ g_dk3s_conn_collar_d 2.0)) (+ r0 (/ g_dk3s_conn_collar_d 2.0)))
  (dk3s_cyl z1 z2 (/ g_dk3s_conn_body_d 2.0) r0)
  (dk3s_face z2 (- r0 (/ g_dk3s_conn_body_d 2.0)) (+ r0 (/ g_dk3s_conn_body_d 2.0)))
  (dk3s_cyl z2 z3 rp r0)
  (dk3s_line (dk3s_p z3 (+ r0 rp)) (dk3s_p z4 (+ r0 (* 0.4 rp))) g_dk3s_lay_main)
  (dk3s_line (dk3s_p z3 (- r0 rp)) (dk3s_p z4 (- r0 (* 0.4 rp))) g_dk3s_lay_main)
  (dk3s_face z4 (- r0 (* 0.4 rp)) (+ r0 (* 0.4 rp)))
  z4
)

;; Скоба (П-образная, проволока Ø2) с центральной перемычкой — как на монтажном чертеже
(defun dk3s_draw_guard ( / w2 d ro ri zs zc)
  (setq w2 (/ g_dk3s_guard_w 2.0) d g_dk3s_guard_d ro g_dk3s_guard_r ri (- ro d) zs g_dk3s_z_sleeve zc ro)
  ;; наружный контур
  (dk3s_line (dk3s_p zs w2) (dk3s_p zc w2) g_dk3s_lay_main)
  (dk3s_arc (dk3s_p zc (- w2 ro)) (dk3s_l ro) 90.0 180.0 g_dk3s_lay_main)
  (dk3s_line (dk3s_p 0.0 (- w2 ro)) (dk3s_p 0.0 (- ro w2)) g_dk3s_lay_main)
  (dk3s_arc (dk3s_p zc (- ro w2)) (dk3s_l ro) 180.0 270.0 g_dk3s_lay_main)
  (dk3s_line (dk3s_p zc (- w2)) (dk3s_p zs (- w2)) g_dk3s_lay_main)
  ;; внутренний контур
  (dk3s_line (dk3s_p zs (- w2 d)) (dk3s_p zc (- w2 d)) g_dk3s_lay_main)
  (dk3s_arc (dk3s_p zc (- w2 ro)) (dk3s_l ri) 90.0 180.0 g_dk3s_lay_main)
  (dk3s_line (dk3s_p d (- w2 ro)) (dk3s_p d (- ro w2)) g_dk3s_lay_main)
  (dk3s_arc (dk3s_p zc (- ro w2)) (dk3s_l ri) 180.0 270.0 g_dk3s_lay_main)
  (dk3s_line (dk3s_p zc (- d w2)) (dk3s_p zs (- d w2)) g_dk3s_lay_main)
  ;; центральная перемычка
  (dk3s_cyl d zs (/ d 2.0) 0.0)
)

;; Наконечник с рабочим электродом (видимая часть над торцом гильзы), ось смещена
(defun dk3s_draw_tip_main ( / r0 zh zc zn zw rt rn e)
  (setq r0 g_dk3s_tip_off rt (/ g_dk3s_tip_d 2.0) rn (/ g_dk3s_tip_nose_d 2.0))
  (setq zh (- g_dk3s_z_sleeve g_dk3s_tip_vis) zc (- zh g_dk3s_tip_cone) zw (- zc g_dk3s_we_len))
  (setq e (/ g_dk3s_tip_s (cos (dk3s_rad 30.0))))
  ;; шестигранная часть (видимая)
  (dk3s_cyl zh g_dk3s_z_sleeve rt r0)
  (dk3s_cyl zh g_dk3s_z_sleeve (/ e 4.0) r0)
  (dk3s_face zh (- r0 rt) (+ r0 rt))
  ;; конус
  (dk3s_line (dk3s_p zh (+ r0 rt)) (dk3s_p zc (+ r0 rn)) g_dk3s_lay_main)
  (dk3s_line (dk3s_p zh (- r0 rt)) (dk3s_p zc (- r0 rn)) g_dk3s_lay_main)
  (dk3s_face zc (- r0 rn) (+ r0 rn))
  ;; рабочий электрод Ø1,4, выступ 2
  (dk3s_cyl zw zc (/ g_dk3s_we_d 2.0) r0)
  (dk3s_face zw (- r0 (/ g_dk3s_we_d 2.0)) (+ r0 (/ g_dk3s_we_d 2.0)))
)

;; Защитная гильза с перфорацией
(defun dk3s_draw_sleeve ( / r i z rs a b)
  (setq r (/ g_dk3s_sleeve_d 2.0))
  (dk3s_face g_dk3s_z_sleeve (- r) r)
  (dk3s_cyl g_dk3s_z_sleeve g_dk3s_z_shell r 0.0)
  ;; фронтальный ряд отверстий
  (setq i 0)
  (repeat g_dk3s_hole_n
    (setq z (+ g_dk3s_hole_z1 (* i g_dk3s_hole_pitch)))
    (dk3s_circle (dk3s_p z 0.0) (dk3s_l (/ g_dk3s_hole_d 2.0)) g_dk3s_lay_main)
    (setq i (1+ i))
  )
  ;; боковые отверстия (в шахматном порядке) — видны как эллипсы на образующих
  (setq rs (* r (sin (dk3s_rad 25.0))))          ; удаление центра от образующей ~0,42R
  (setq a (/ g_dk3s_hole_d 2.0) b (* (/ g_dk3s_hole_d 2.0) (cos (dk3s_rad 60.0))))
  (setq i 0)
  (repeat g_dk3s_hole_side_n
    (setq z (+ g_dk3s_hole_z1 (/ g_dk3s_hole_pitch 2.0) (* i g_dk3s_hole_pitch)))
    (dk3s_ellipse (dk3s_p z (- r rs)) (dk3s_l a) (dk3s_l b) g_dk3s_lay_main)
    (dk3s_ellipse (dk3s_p z (- rs r)) (dk3s_l a) (dk3s_l b) g_dk3s_lay_main)
    (setq i (1+ i))
  )
)

;; Корпус с резьбой, фланец, сальниковая втулка (шестигранники), шейка, бирка
(defun dk3s_draw_gland ( / rs rr rp e1 e2 rc rg rn rst zsh d1 h)
  (setq rs (/ g_dk3s_shell_d 2.0) rr (/ g_dk3s_relief_d 2.0) rp (/ g_dk3s_plate_d 2.0))
  ;; корпус M42x3: торец с фаской, наружный диаметр, внутренний диаметр резьбы (тонкая)
  (setq zsh (+ g_dk3s_z_shell g_dk3s_shell_ch))
  (dk3s_face g_dk3s_z_shell (- (/ g_dk3s_sleeve_d 2.0)) (- (- rs g_dk3s_shell_ch)))
  (dk3s_face g_dk3s_z_shell (/ g_dk3s_sleeve_d 2.0) (- rs g_dk3s_shell_ch))
  (dk3s_line (dk3s_p g_dk3s_z_shell (- rs g_dk3s_shell_ch)) (dk3s_p zsh rs) g_dk3s_lay_main)
  (dk3s_line (dk3s_p g_dk3s_z_shell (- g_dk3s_shell_ch rs)) (dk3s_p zsh (- rs)) g_dk3s_lay_main)
  (dk3s_cyl zsh g_dk3s_z_relief rs 0.0)
  (setq d1 (- g_dk3s_shell_d (* 1.0825 g_dk3s_thread_pitch)))   ; внутренний диаметр резьбы
  (dk3s_line (dk3s_p zsh (/ d1 2.0)) (dk3s_p g_dk3s_z_relief (/ d1 2.0)) g_dk3s_lay_thin)
  (dk3s_line (dk3s_p zsh (/ d1 -2.0)) (dk3s_p g_dk3s_z_relief (/ d1 -2.0)) g_dk3s_lay_thin)
  ;; проточка
  (dk3s_face g_dk3s_z_relief (- rs) rs)
  (dk3s_cyl g_dk3s_z_relief g_dk3s_z_plate rr 0.0)
  ;; фланец-пластина
  (dk3s_face g_dk3s_z_plate (- rp) rp)
  (dk3s_cyl g_dk3s_z_plate g_dk3s_z_hex1 rp 0.0)
  (dk3s_face g_dk3s_z_hex1 (- rp) rp)
  ;; шестигранник S46 корпуса: фаска 30° со стороны гайки, дуги на гранях (как у ЭКОР)
  (setq e1 (dk3s_hex g_dk3s_z_hex1 g_dk3s_z_cyl g_dk3s_hex1_s g_dk3s_hex1_e))
  ;; видимая резьба M33x2 гайки нажимной (наружный Ø33, внутренний - тонкая линия) и канавка Ø30
  (setq rc (/ g_dk3s_cyl_d 2.0) rg (/ g_dk3s_groove_d 2.0))
  (dk3s_cyl g_dk3s_z_cyl g_dk3s_z_groove rc 0.0)
  (setq d1 (- g_dk3s_cyl_d (* 1.0825 g_dk3s_thread2_pitch)))
  (dk3s_line (dk3s_p g_dk3s_z_cyl (/ d1 2.0)) (dk3s_p g_dk3s_z_groove (/ d1 2.0)) g_dk3s_lay_thin)
  (dk3s_line (dk3s_p g_dk3s_z_cyl (/ d1 -2.0)) (dk3s_p g_dk3s_z_groove (/ d1 -2.0)) g_dk3s_lay_thin)
  (dk3s_face g_dk3s_z_groove (- rc) rc)
  (dk3s_cyl g_dk3s_z_groove g_dk3s_z_hex2 rg 0.0)
  ;; шестигранник S36 гайки нажимной: фаска 30° с наружного торца
  (setq e2 (dk3s_hex g_dk3s_z_hex2 g_dk3s_z_neck g_dk3s_hex2_s g_dk3s_hex2_e))
  ;; шейка Ø20,8, ступень Ø18,8, конус Ø16 -> Ø15,4
  (setq rn (/ g_dk3s_neck_d 2.0) rst (/ g_dk3s_step_d 2.0))
  (dk3s_cyl g_dk3s_z_neck g_dk3s_z_step rn 0.0)
  (dk3s_face g_dk3s_z_step (- rn) rn)
  (dk3s_cyl g_dk3s_z_step g_dk3s_z_taper rst 0.0)
  (dk3s_face g_dk3s_z_taper (- rst) rst)
  (dk3s_line (dk3s_p g_dk3s_z_taper (/ g_dk3s_taper_d1 2.0)) (dk3s_p g_dk3s_z_tag (/ g_dk3s_taper_d2 2.0)) g_dk3s_lay_main)
  (dk3s_line (dk3s_p g_dk3s_z_taper (/ g_dk3s_taper_d1 -2.0)) (dk3s_p g_dk3s_z_tag (/ g_dk3s_taper_d2 -2.0)) g_dk3s_lay_main)
  ;; бирка с заводским номером (16 x 10) и логотип
  (dk3s_rect (dk3s_p g_dk3s_z_tag (/ g_dk3s_tag_w -2.0)) (dk3s_p g_dk3s_z_tag_end (/ g_dk3s_tag_w 2.0)) g_dk3s_lay_main)
  (setq h (dk3s_l 4.0))
  (dk3s_text (dk3s_p (/ (+ g_dk3s_z_tag g_dk3s_z_tag_end) 2.0) 0.0) h "\\U+042D\\U+041A" 0.0 1 g_dk3s_lay_text)
)

;; Трубка токоотвода РЭ Ø6, мостики, хомуты и разъём WE
(defun dk3s_draw_bundle ( / rt rb z1 z2 zc1 zc2 rc)
  (setq rt (/ g_dk3s_tube_d 2.0) rb (+ g_dk3s_bridge_r (/ g_dk3s_bridge_d 2.0)))
  (setq zc1 g_dk3s_z_clamp1 zc2 g_dk3s_z_clamp2 rc (/ g_dk3s_clamp_d 2.0))
  ;; трубка Ø6 сегментами между хомутами
  (dk3s_cyl g_dk3s_z_tag_end zc1 rt 0.0)
  (dk3s_cyl (+ zc1 g_dk3s_clamp_len) zc2 rt 0.0)
  (dk3s_cyl (+ zc2 g_dk3s_clamp_len) g_dk3s_z_we_end rt 0.0)
  ;; наружные образующие мостиков (внутренние совпадают с трубкой)
  (dk3s_line (dk3s_p g_dk3s_z_tag_end rb) (dk3s_p zc1 rb) g_dk3s_lay_main)
  (dk3s_line (dk3s_p g_dk3s_z_tag_end (- rb)) (dk3s_p zc1 (- rb)) g_dk3s_lay_main)
  (dk3s_line (dk3s_p (+ zc1 g_dk3s_clamp_len) rb) (dk3s_p zc2 rb) g_dk3s_lay_main)
  (dk3s_line (dk3s_p (+ zc1 g_dk3s_clamp_len) (- rb)) (dk3s_p zc2 (- rb)) g_dk3s_lay_main)
  (dk3s_line (dk3s_p (+ zc2 g_dk3s_clamp_len) rb) (dk3s_p g_dk3s_z_bend rb) g_dk3s_lay_main)
  (dk3s_line (dk3s_p (+ zc2 g_dk3s_clamp_len) (- rb)) (dk3s_p g_dk3s_z_bend (- rb)) g_dk3s_lay_main)
  ;; хомуты
  (dk3s_rect (dk3s_p zc1 (- rc)) (dk3s_p (+ zc1 g_dk3s_clamp_len) rc) g_dk3s_lay_main)
  (dk3s_rect (dk3s_p zc2 (- rc)) (dk3s_p (+ zc2 g_dk3s_clamp_len) rc) g_dk3s_lay_main)
  ;; разъём токоотвода рабочего электрода
  (dk3s_connector g_dk3s_z_we_end 0.0)
)

;; Провод токоотвода вспомогательного электрода с разъёмом
(defun dk3s_draw_se ( / r0 rw)
  (setq r0 g_dk3s_se_r rw (/ g_dk3s_se_d 2.0))
  (dk3s_cyl g_dk3s_z_se_start g_dk3s_z_se_end rw r0)
  (dk3s_connector g_dk3s_z_se_end r0)
)

;; S-образный изгиб мостика: от (z1, r1) к (z2, r2), касательные вдоль оси;
;; рисуются две образующие на расстоянии ±rb/2 от осевой линии
(defun dk3s_draw_bend (z1 r1 z2 r2 rb / dx dy R th sgn c1 c2 a1 a2 hb)
  (setq dx (- z2 z1) dy (- r2 r1) sgn (if (< dy 0.0) -1.0 1.0) dy (abs dy) hb (/ rb 2.0))
  (setq R (/ (+ (* dx dx) (* dy dy)) (* 4.0 dy)))
  (setq th (dk3s_deg (atan (/ dx 2.0) (- R (/ dy 2.0)))))
  ;; первая дуга: центр над началом (по направлению sgn), от 270° до 270°+th (при sgn>0)
  (setq c1 (dk3s_p z1 (+ r1 (* sgn R))) c2 (dk3s_p z2 (- r2 (* sgn R))))
  (if (> sgn 0.0)
    (progn
      (dk3s_arc c1 (dk3s_l (- R hb)) 270.0 (+ 270.0 th) g_dk3s_lay_main)
      (dk3s_arc c1 (dk3s_l (+ R hb)) 270.0 (+ 270.0 th) g_dk3s_lay_main)
      (dk3s_arc c2 (dk3s_l (- R hb)) 90.0 (+ 90.0 th) g_dk3s_lay_main)
      (dk3s_arc c2 (dk3s_l (+ R hb)) 90.0 (+ 90.0 th) g_dk3s_lay_main)
    )
    (progn
      (dk3s_arc c1 (dk3s_l (- R hb)) (- 90.0 th) 90.0 g_dk3s_lay_main)
      (dk3s_arc c1 (dk3s_l (+ R hb)) (- 90.0 th) 90.0 g_dk3s_lay_main)
      (dk3s_arc c2 (dk3s_l (- R hb)) (- 270.0 th) 270.0 g_dk3s_lay_main)
      (dk3s_arc c2 (dk3s_l (+ R hb)) (- 270.0 th) 270.0 g_dk3s_lay_main)
    )
  )
)

;; Электрод сравнения на оси r0 (два сегмента, перемычка, штырь)
(defun dk3s_draw_re (r0 / r rn z1 z2 z3 z4)
  (setq r (/ g_dk3s_re_d 2.0) rn (/ g_dk3s_re_neck_d 2.0))
  (setq z1 g_dk3s_z_re z2 (+ z1 g_dk3s_re_seg1) z3 (+ z2 g_dk3s_re_neck) z4 (+ z3 g_dk3s_re_seg2))
  (dk3s_face z1 (- r0 r) (+ r0 r))
  (dk3s_cyl z1 z2 r r0)
  (dk3s_face z2 (- r0 r) (+ r0 r))
  (dk3s_cyl z2 z3 rn r0)
  (dk3s_face z3 (- r0 r) (+ r0 r))
  (dk3s_cyl z3 z4 r r0)
  (dk3s_face z4 (- r0 r) (+ r0 r))
  ;; зазор 1 мм до буртика штыря (Ø корпуса разъёма)
  (dk3s_cyl z4 (+ z4 g_dk3s_re_gap) (/ g_dk3s_conn_body_d 2.0) r0)
  (dk3s_connector (+ z4 g_dk3s_re_gap) r0)
  ;; осевая электрода
  (dk3s_line (dk3s_p (- z1 5.0) r0) (dk3s_p (+ g_dk3s_z_total 4.0) r0) g_dk3s_lay_axis)
)

;; Осевая линия датчика
;; Ось датчика; на бирке прерывается, чтобы не пересекать надпись на ней
(defun dk3s_draw_axis ()
  (dk3s_line (dk3s_p -6.0 0.0) (dk3s_p g_dk3s_z_tag 0.0) g_dk3s_lay_axis)
  (dk3s_line (dk3s_p g_dk3s_z_tag_end 0.0)
             (dk3s_p (+ g_dk3s_z_we_end g_dk3s_conn_collar_l g_dk3s_conn_body_l
                        1.0 g_dk3s_conn_pin_l g_dk3s_conn_tip_l 5.0) 0.0) g_dk3s_lay_axis)
)

(defun dk3s_draw_main_view ()
  (dk3s_draw_axis)
  (dk3s_draw_guard)
  (dk3s_draw_tip_main)
  (dk3s_draw_sleeve)
  (dk3s_draw_gland)
  (dk3s_draw_bundle)
  (dk3s_draw_se)
  (dk3s_draw_bend g_dk3s_z_bend g_dk3s_bridge_r g_dk3s_z_re g_dk3s_re_r g_dk3s_bridge_d)
  (dk3s_draw_bend g_dk3s_z_bend (- g_dk3s_bridge_r) g_dk3s_z_re (- g_dk3s_re_r) g_dk3s_bridge_d)
  (dk3s_draw_re g_dk3s_re_r)
  (dk3s_draw_re (- g_dk3s_re_r))
)

;;; ---------------------------------------------------------------------------
;;; 8. ВЫНОСНОЙ ЭЛЕМЕНТ А (2:1): узел рабочего электрода — как Fig. 4 описания K1.
;;;    Локальная ось z' — вдоль токоотвода (0 — начало защитной трубки), r' — от оси.
;;;    Разрез: защитная трубка и наконечник заштрихованы, стержни — без штриховки.
;;; ---------------------------------------------------------------------------

(defun dk3s_draw_detail_a ( / rt rti rtap rtip rn rw rb zt zh zc zw zb hp h pts sgn ztap)
  (setq rt (/ g_dk3s_tube_d 2.0) rti (- rt g_dk3s_tube_wall) rtap (/ g_dk3s_tap_d 2.0)
        rtip (/ g_dk3s_tip_d 2.0) rn (/ g_dk3s_tip_nose_d 2.0) rw (/ g_dk3s_we_d 2.0)
        rb (+ rw 0.1))                                  ; отверстие под электрод
  (setq zt 18.0)                                        ; конец трубки = начало наконечника
  (setq zh (+ zt g_dk3s_tip_len))                       ; конец шестигранника
  (setq zc (+ zh g_dk3s_tip_cone))                      ; торец конуса
  (setq zw (+ zc g_dk3s_we_len))                        ; конец электрода
  (setq zb (+ zt g_dk3s_tip_bore_len))                  ; дно резьбового отверстия
  (setq ztap (- zb 1.0))                                ; конец токоотвода
  (setq hp (* 1.5 g_dk3s_scale_den))                    ; шаг штриховки на листе 1,5 мм
  ;; осевая
  (dk3s_line (dk3s_p -4.0 0.0) (dk3s_p (+ zw 4.0) 0.0) g_dk3s_lay_axis)
  ;; защитная трубка (в разрезе): наружные и внутренние образующие, обрыв слева
  (dk3s_cyl 0.0 zt rt 0.0)
  (dk3s_cyl 0.0 zt rti 0.0)
  (dk3s_face zt rti rt) (dk3s_face zt (- rt) (- rti))
  (foreach sgn '(1.0 -1.0)
    (setq pts (list (dk3s_p 0.0 (* sgn rti)) (dk3s_p zt (* sgn rti)) (dk3s_p zt (* sgn rt)) (dk3s_p 0.0 (* sgn rt))))
    (dk3s_hatch_poly pts hp g_dk3s_lay_thin)
  )
  ;; токоотвод Ø3 (стержень, без штриховки), резьбовой конец с фаской
  (dk3s_cyl 0.0 ztap rtap 0.0)
  (dk3s_face ztap (- rtap) rtap)
  ;; линия обрыва слева (волнистая упрощённо — ломаная)
  (dk3s_pline (list (dk3s_p 0.0 (- rt 0.5)) (dk3s_p -0.6 (* 0.5 rt)) (dk3s_p 0.6 0.0)
                    (dk3s_p -0.6 (* -0.5 rt)) (dk3s_p 0.0 (- 0.5 rt))) nil 0.0 g_dk3s_lay_thin)
  ;; наконечник (в разрезе): наружный контур шестигранника + конус, отверстия
  (dk3s_face zt rtap rtip) (dk3s_face zt (- rtip) (- rtap))
  (dk3s_cyl zt zh rtip 0.0)
  (dk3s_line (dk3s_p zh rtip) (dk3s_p zc rn) g_dk3s_lay_main)
  (dk3s_line (dk3s_p zh (- rtip)) (dk3s_p zc (- rn)) g_dk3s_lay_main)
  (dk3s_face zc rb rn) (dk3s_face zc (- rn) (- rb))
  (dk3s_cyl zt zb rtap 0.0)             ; резьбовое отверстие (стенки)
  (dk3s_face zb rb rtap) (dk3s_face zb (- rtap) (- rb))
  (dk3s_cyl zb zc rb 0.0)               ; отверстие под электрод
  ;; штриховка наконечника: 3 выпуклых участка на сторону
  (foreach sgn '(1.0 -1.0)
    (dk3s_hatch_poly (list (dk3s_p zt (* sgn rtap)) (dk3s_p zb (* sgn rtap))
                           (dk3s_p zb (* sgn rtip)) (dk3s_p zt (* sgn rtip))) hp g_dk3s_lay_thin)
    (dk3s_hatch_poly (list (dk3s_p zb (* sgn rb)) (dk3s_p zh (* sgn rb))
                           (dk3s_p zh (* sgn rtip)) (dk3s_p zb (* sgn rtip))) hp g_dk3s_lay_thin)
    (dk3s_hatch_poly (list (dk3s_p zh (* sgn rb)) (dk3s_p zc (* sgn rb))
                           (dk3s_p zc (* sgn rn)) (dk3s_p zh (* sgn rtip))) hp g_dk3s_lay_thin)
  )
  ;; рабочий электрод Ø1,4: приварен к торцу токоотвода, выступает на 2 мм
  (dk3s_cyl ztap zw rw 0.0)
  (dk3s_face zw (- rw) rw)
  ;; размеры выносного элемента (текст задан явно — вид увеличен)
  (setq h (* g_dk3s_txt_h g_dk3s_scale_den))
  (dk3s_dim (dk3s_p zw rw) (dk3s_p zw (- rw)) (dk3s_p (+ zw 3.0) 0.0) 90.0
            (strcat "%%c" (dk3s_num g_dk3s_we_d 1)))
  (dk3s_dim (dk3s_p zc (- rn)) (dk3s_p zw (- rn)) (dk3s_p 0.0 (- (- rtip) 3.0)) 0.0
            (dk3s_num g_dk3s_we_len 0))
  (dk3s_dim (dk3s_p 9.0 rt) (dk3s_p 9.0 (- rt)) (dk3s_p 9.0 0.0) 90.0
            (strcat "%%c" (dk3s_num g_dk3s_tube_d 0)))
  (dk3s_dim (dk3s_p 4.0 rtap) (dk3s_p 4.0 (- rtap)) (dk3s_p 4.0 0.0) 90.0
            (strcat "%%c" (dk3s_num g_dk3s_tap_d 0)))
  (dk3s_dim (dk3s_p (+ zt 9.0) rtip) (dk3s_p (+ zt 9.0) (- rtip)) (dk3s_p (+ zt 9.0) 0.0) 90.0
            (strcat "S" (dk3s_num g_dk3s_tip_s 2)))
  ;; надписи выносного элемента
  (dk3s_leader (dk3s_p 12.0 rt) (dk3s_p 6.0 (+ rtip 6.0)) 1 "\\U+0417\\U+0430\\U+0449\\U+0438\\U+0442\\U+043D\\U+0430\\U+044F \\U+0442\\U+0440\\U+0443\\U+0431\\U+043A\\U+0430")
  (dk3s_leader (dk3s_p (+ zt 4.0) (- rtip)) (dk3s_p (+ zt 6.0) (- (- rtip) 7.0)) 1 "\\U+041D\\U+0430\\U+043A\\U+043E\\U+043D\\U+0435\\U+0447\\U+043D\\U+0438\\U+043A")
  (dk3s_leader (dk3s_p (+ zc 1.0) rw) (dk3s_p (+ zc 3.0) (+ rtip 6.0)) 1 "\\U+0420\\U+0430\\U+0431\\U+043E\\U+0447\\U+0438\\U+0439 \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434")
  (dk3s_leader (dk3s_p 6.0 (- rtap)) (dk3s_p 12.0 (- (- rtip) 13.0)) 1 "\\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434 \\U+0440\\U+0430\\U+0431\\U+043E\\U+0447\\U+0435\\U+0433\\U+043E \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434\\U+0430")
  ;; заголовок вида
  (dk3s_text (dk3s_p (/ zw 2.0) (+ rtip 14.0)) (* h 1.4) "\\U+0410 (2:1)" 0.0 3 g_dk3s_lay_text)
  (dk3s_line (dk3s_p (- (/ zw 2.0) 7.0) (+ rtip 13.2)) (dk3s_p (+ (/ zw 2.0) 7.0) (+ rtip 13.2)) g_dk3s_lay_thin)
)

;;; ---------------------------------------------------------------------------
;;; 9. РАЗМЕРЫ, ВЫНОСКИ И ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ ГЛАВНОГО ВИДА
;;;    Размерные точки берутся из таблицы параметров — значения вычисляются CAD.
;;; ---------------------------------------------------------------------------

(defun dk3s_draw_dims_main ( / rs re rp zre1 zre2 y1 y2 y3 y4 zpl)
  (setq rs (/ g_dk3s_sleeve_d 2.0) re (/ g_dk3s_re_d 2.0) rp (/ g_dk3s_plate_d 2.0))
  (setq y1 -40.0 y2 -56.0 y3 -70.0 y4 -84.0)       ; уровни горизонтальных размеров (снизу)
  ;; перфорация: первое отверстие от вершины скобы и шаг
  (dk3s_dim (dk3s_p 0.0 0.0) (dk3s_p g_dk3s_hole_z1 0.0) (dk3s_p 0.0 y1) 0.0 "")
  (dk3s_dim (dk3s_p g_dk3s_hole_z1 0.0) (dk3s_p (+ g_dk3s_hole_z1 g_dk3s_hole_pitch) 0.0) (dk3s_p 0.0 y1) 0.0 "")
  (dk3s_dim (dk3s_p (+ g_dk3s_hole_z1 g_dk3s_hole_pitch) 0.0)
            (dk3s_p (+ g_dk3s_hole_z1 (* 2.0 g_dk3s_hole_pitch)) 0.0) (dk3s_p 0.0 y1) 0.0 "")
  ;; длина гильзы; вершина скобы -> низ фланца; низ фланца -> штыри; общая длина
  (dk3s_dim (dk3s_p g_dk3s_z_sleeve (- rs)) (dk3s_p g_dk3s_z_shell (- rs)) (dk3s_p 0.0 y2) 0.0 "")
  (setq zpl g_dk3s_z_hex1)
  (dk3s_dim (dk3s_p 0.0 0.0) (dk3s_p zpl (- rp)) (dk3s_p 0.0 y3) 0.0 "")
  (dk3s_dim (dk3s_p zpl (- rp)) (dk3s_p g_dk3s_z_total (- g_dk3s_re_r)) (dk3s_p 0.0 y3) 0.0 "")
  (dk3s_dim (dk3s_p 0.0 0.0) (dk3s_p g_dk3s_z_total (- g_dk3s_re_r)) (dk3s_p 0.0 y4) 0.0 "*<>")
  ;; высота скобы (сверху)
  (dk3s_dim (dk3s_p 0.0 (/ g_dk3s_guard_w 2.0)) (dk3s_p g_dk3s_z_sleeve (/ g_dk3s_guard_w 2.0))
            (dk3s_p 0.0 42.0) 0.0 "")
  ;; диаметры: гильза и присоединительная резьба M42x3 корпуса
  (dk3s_dim (dk3s_p 130.0 rs) (dk3s_p 130.0 (- rs)) (dk3s_p 130.0 0.0) 90.0 "%%c<>")
  (dk3s_dim (dk3s_p 246.0 (/ g_dk3s_shell_d 2.0)) (dk3s_p 246.0 (/ g_dk3s_shell_d -2.0)) (dk3s_p 246.0 0.0) 90.0
            (strcat "M<>x" (dk3s_num g_dk3s_thread_pitch 0)))
  ;; размеры корпуса и гайки нажимной (Ø59, S46, M33x2, S36, Ø20,8) на общем виде не ставятся —
  ;; они на чертежах деталей 714.761.000 и 714.541.000 (решение 19.09.2026)
  (dk3s_dim (dk3s_p g_dk3s_z_shell (/ g_dk3s_shell_d -2.0)) (dk3s_p g_dk3s_z_cyl (/ g_dk3s_hex1_s -2.0)) (dk3s_p 0.0 -40.0) 0.0 "")
  (dk3s_dim (dk3s_p 455.0 (/ g_dk3s_tube_d 2.0)) (dk3s_p 455.0 (/ g_dk3s_tube_d -2.0)) (dk3s_p 455.0 0.0) 90.0 "%%c<>")
  (dk3s_dim (dk3s_p 440.0 (+ g_dk3s_se_r (/ g_dk3s_se_d 2.0))) (dk3s_p 440.0 (- g_dk3s_se_r (/ g_dk3s_se_d 2.0)))
            (dk3s_p 440.0 g_dk3s_se_r) 90.0 "%%c<>")
  ;; электроды сравнения: диаметр, длина, расстояние между осями
  (setq zre1 g_dk3s_z_re zre2 g_dk3s_z_re_end)
  (dk3s_dim (dk3s_p 565.0 (+ g_dk3s_re_r re)) (dk3s_p 565.0 (- g_dk3s_re_r re)) (dk3s_p 565.0 g_dk3s_re_r) 90.0 "%%c<>")
  (dk3s_dim (dk3s_p zre1 (+ g_dk3s_re_r re)) (dk3s_p zre2 (+ g_dk3s_re_r re)) (dk3s_p 0.0 (+ g_dk3s_re_r re 12.0)) 0.0 "")
  (dk3s_dim (dk3s_p (+ g_dk3s_z_total 4.0) g_dk3s_re_r) (dk3s_p (+ g_dk3s_z_total 4.0) (- g_dk3s_re_r))
            (dk3s_p (+ g_dk3s_z_total 14.0) 0.0) 90.0 "")
)

(defun dk3s_draw_labels_main ( / ya yb yc ye yd yd2 rs rp rc rre e2)
  ;; полки выносок: ряды над датчиком и под ним (между размерными цепями).
  ;; Раскладка подобрана перебором (19.09.2026, plan_labels.py; запас ширины g_dk3s_font_k, зазор 0,5 мм): при ширине надписей
  ;; шрифтом ГОСТ 2.304 тип Б надписи не пересекаются ни с чем, выноски не пересекают друг друга,
  ;; полки, размеры и надписи; линии деталей пересекают только выноски наконечника (изнутри скобы)
  ;; и токоотвода рабочего электрода (под мостиками). Проверка — tools/lispcheck/check_text_fit.py.
  (setq ya 52.0 yb 68.0 yc 84.0 ye 100.0 yd -46.0 yd2 -52.0)
  (setq rs (/ g_dk3s_sleeve_d 2.0) rp (/ g_dk3s_plate_d 2.0) rc (/ g_dk3s_clamp_d 2.0))
  (setq e2 g_dk3s_hex2_e rre (+ g_dk3s_re_r (/ g_dk3s_re_d 2.0)))
  ;; ряд A
  (dk3s_leader (dk3s_p (- g_dk3s_z_sleeve 2.0) (+ g_dk3s_tip_off (/ g_dk3s_tip_d 2.0)))
               (dk3s_p 31.6 ya) 1 "\\U+041D\\U+0430\\U+043A\\U+043E\\U+043D\\U+0435\\U+0447\\U+043D\\U+0438\\U+043A (\\U+0441\\U+043C. \\U+0410)")
  (dk3s_leader (dk3s_p 240.0 (/ g_dk3s_shell_d 2.0))
               (dk3s_p 240.0 ya) -1 "\\U+041A\\U+043E\\U+0440\\U+043F\\U+0443\\U+0441 714.761.000")
  (dk3s_leader (dk3s_p (+ g_dk3s_z_clamp1 3.8) rc)
               (dk3s_p (+ g_dk3s_z_clamp1 3.8) ya) 1 "\\U+0425\\U+043E\\U+043C\\U+0443\\U+0442")
  ;; ряд B
  (dk3s_leader (dk3s_p 0.6 9.5)
               (dk3s_p -7.4 yb) 1 "\\U+0417\\U+0430\\U+0449\\U+0438\\U+0442\\U+043D\\U+0430\\U+044F \\U+0441\\U+043A\\U+043E\\U+0431\\U+0430")
  (dk3s_leader (dk3s_p 130.0 rs)
               (dk3s_p 130.0 yb) 1 "\\U+0417\\U+0430\\U+0449\\U+0438\\U+0442\\U+043D\\U+0430\\U+044F \\U+0433\\U+0438\\U+043B\\U+044C\\U+0437\\U+0430")
  (dk3s_leader (dk3s_p 327.0 (/ g_dk3s_tag_w 2.0))
               (dk3s_p 327.0 yb) 1 "\\U+0411\\U+0438\\U+0440\\U+043A\\U+0430 \\U+0441 \\U+0437\\U+0430\\U+0432\\U+043E\\U+0434\\U+0441\\U+043A\\U+0438\\U+043C \\U+043D\\U+043E\\U+043C\\U+0435\\U+0440\\U+043E\\U+043C")
  (dk3s_leader (dk3s_p 605.0 (+ g_dk3s_re_r (/ g_dk3s_conn_pin_d 2.0)))
               (dk3s_p 571.0 yb) 1 "\\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434 \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434\\U+0430 \\U+0441\\U+0440\\U+0430\\U+0432\\U+043D\\U+0435\\U+043D\\U+0438\\U+044F")
  ;; ряд C
  (dk3s_leader (dk3s_p 262.3 rp)
               (dk3s_p 262.3 yc) -1 "\\U+0424\\U+043B\\U+0430\\U+043D\\U+0435\\U+0446 \\U+043A\\U+043E\\U+0440\\U+043F\\U+0443\\U+0441\\U+0430")
  (dk3s_leader (dk3s_p 298.5 (/ e2 2.0))
               (dk3s_p 298.5 yc) 1 "\\U+0413\\U+0430\\U+0439\\U+043A\\U+0430 \\U+043D\\U+0430\\U+0436\\U+0438\\U+043C\\U+043D\\U+0430\\U+044F")
  (dk3s_leader (dk3s_p 530.0 rre)
               (dk3s_p 520.0 yc) 1 "\\U+042D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434 \\U+0441\\U+0440\\U+0430\\U+0432\\U+043D\\U+0435\\U+043D\\U+0438\\U+044F (2 \\U+0448\\U+0442.)")
  ;; ряд D
  (dk3s_leader (dk3s_p 470.0 (+ g_dk3s_bridge_r (/ g_dk3s_bridge_d 2.0)))
               (dk3s_p 470.0 ye) -1 "\\U+042D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+043B\\U+0438\\U+0442\\U+0438\\U+0447\\U+0435\\U+0441\\U+043A\\U+0438\\U+0439 \\U+043C\\U+043E\\U+0441\\U+0442\\U+0438\\U+043A (2 \\U+0448\\U+0442.)")
  (dk3s_leader (dk3s_p 488.0 (/ g_dk3s_conn_body_d 2.0))
               (dk3s_p 488.0 ye) 1 "\\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434 \\U+0440\\U+0430\\U+0431\\U+043E\\U+0447\\U+0435\\U+0433\\U+043E \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434\\U+0430")
  ;; снизу, второй ряд
  (dk3s_leader (dk3s_p 400.0 (- g_dk3s_se_r (/ g_dk3s_se_d 2.0)))
               (dk3s_p 400.0 yd2) 1 "\\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434 \\U+0432\\U+0441\\U+043F\\U+043E\\U+043C\\U+043E\\U+0433\\U+0430\\U+0442\\U+0435\\U+043B\\U+044C\\U+043D\\U+043E\\U+0433\\U+043E \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434\\U+0430")
  ;; обозначение выносного элемента А на главном виде
  (dk3s_circle (dk3s_p 9.0 g_dk3s_tip_off) 20.0 g_dk3s_lay_thin)
  (dk3s_text (dk3s_p 28.0 (+ g_dk3s_tip_off 15.0)) (* 1.4 g_dk3s_txt_h g_dk3s_scale_den) "\\U+0410" 0.0 0 g_dk3s_lay_text)
)

;; Технические требования: строки переносятся по ширине до рамки (продолжение — с отступом под номером),
;; блок ставится так, чтобы последняя строка была на 8 мм выше основной надписи; y — не выше этого уровня
(defun dk3s_draw_notes (x y / h dy lines i xr rows w0 n y0 r)
  (setq h (* g_dk3s_txt_h g_dk3s_scale_den) dy (* h 1.7))
  (setq xr (* g_dk3s_scale_den (- g_dk3s_sheet_w 8.0)))          ; правый край текста: рамка минус 3 мм
  (setq lines (list
    "1. * \\U+0420\\U+0430\\U+0437\\U+043C\\U+0435\\U+0440\\U+044B \\U+0434\\U+043B\\U+044F \\U+0441\\U+043F\\U+0440\\U+0430\\U+0432\\U+043E\\U+043A."
    "2. \\U+0420\\U+0430\\U+0431\\U+043E\\U+0447\\U+0438\\U+0439 \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434 - \\U+043F\\U+0440\\U+043E\\U+0432\\U+043E\\U+043B\\U+043E\\U+043A\\U+0430 \\U+00D81,4 \\U+043C\\U+043C, \\U+0432\\U+044B\\U+0441\\U+0442\\U+0443\\U+043F 2 \\U+043C\\U+043C."
    "3. \\U+041D\\U+0430\\U+043A\\U+043E\\U+043D\\U+0435\\U+0447\\U+043D\\U+0438\\U+043A - \\U+0448\\U+0435\\U+0441\\U+0442\\U+0438\\U+0433\\U+0440\\U+0430\\U+043D\\U+043D\\U+0438\\U+043A 1/4\", \\U+0440\\U+0435\\U+0437\\U+044C\\U+0431\\U+0430 \\U+0442\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434\\U+0430 - \\U+0448\\U+0430\\U+0433 0,5 \\U+043C\\U+043C."
    "4. \\U+041F\\U+0440\\U+0438\\U+0441\\U+043E\\U+0435\\U+0434\\U+0438\\U+043D\\U+0435\\U+043D\\U+0438\\U+0435 - \\U+0440\\U+0435\\U+0437\\U+044C\\U+0431\\U+0430 M42x3 \\U+0432 \\U+0433\\U+043D\\U+0435\\U+0437\\U+0434\\U+043E 713.165.001 \\U+0432\\U+0445\\U+043E\\U+0434\\U+043D\\U+043E\\U+0433\\U+043E \\U+0443\\U+0437\\U+043B\\U+0430 \\U+0444\\U+043B\\U+0430\\U+043D\\U+0446\\U+0430 DN50."
    "5. \\U+041A\\U+043E\\U+0440\\U+043F\\U+0443\\U+0441, \\U+0433\\U+0430\\U+0439\\U+043A\\U+0430 \\U+043D\\U+0430\\U+0436\\U+0438\\U+043C\\U+043D\\U+0430\\U+044F, \\U+0433\\U+0440\\U+0443\\U+043D\\U+0434\\U+0431\\U+0443\\U+043A\\U+0441\\U+0430 - 08\\U+042518\\U+041D10\\U+0422 \\U+0413\\U+041E\\U+0421\\U+0422 5949-75 (\\U+0447\\U+0435\\U+0440\\U+0442. 714.761.000, 714.541.000, 711.171.000)."
    "6. \\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434\\U+044B: RE1 - \\U+0441\\U+0438\\U+043D\\U+0438\\U+0439, RE2 - \\U+0431\\U+0435\\U+043B\\U+044B\\U+0439, WE - \\U+043A\\U+0440\\U+0430\\U+0441\\U+043D\\U+044B\\U+0439, SE - \\U+0447\\U+0451\\U+0440\\U+043D\\U+044B\\U+0439."
    "7. \\U+0413\\U+0435\\U+043E\\U+043C\\U+0435\\U+0442\\U+0440\\U+0438\\U+044F - \\U+043F\\U+043E \\U+043C\\U+043E\\U+043D\\U+0442\\U+0430\\U+0436\\U+043D\\U+043E\\U+043C\\U+0443 \\U+0447\\U+0435\\U+0440\\U+0442\\U+0435\\U+0436\\U+0443 \\U+0442\\U+0435\\U+0445\\U+043E\\U+043F\\U+0438\\U+0441\\U+0430\\U+043D\\U+0438\\U+044F K1 (\\U+043B\\U+0438\\U+0441\\U+0442 16) \\U+0438 \\U+0447\\U+0435\\U+0440\\U+0442\\U+0435\\U+0436\\U+0430\\U+043C \\U+0434\\U+0435\\U+0442\\U+0430\\U+043B\\U+0435\\U+0439 \\U+042D\\U+041A\\U+041E\\U+0420."))
  ;; разбивка на строки: список (текст отступ)
  (setq rows nil)
  (foreach s lines
    (setq w0 (- (dk3s_text_w (substr s 1 3) h) (* 0.27 h)))       ; ширина "N. " — отступ продолжения
    (setq r 0)
    (foreach ln (dk3s_wrap s h (- xr x) (- xr x w0))
      (setq rows (cons (list ln (if (= r 0) 0.0 w0)) rows) r (1+ r))
    )
  )
  (setq rows (reverse rows) n (length rows))
  (setq y0 (+ g_dk3s_tby (* g_dk3s_scale_den 63.0) (* (1- n) dy)))  ; низ последней строки: штамп + 8 мм
  (if (< y y0) (setq y0 y))
  (setq i 0)
  (foreach rw rows
    (dk3s_text (dk3s_ps (+ x (cadr rw)) (- y0 (* i dy))) h (car rw) 0.0 0 g_dk3s_lay_text)
    (setq i (1+ i))
  )
)

;;; ---------------------------------------------------------------------------
;;; 10. ГЛАВНАЯ КОМАНДА (конечный автомат стадий: INIT -> TABLES -> FRAME ->
;;;     MAIN -> DETAIL -> DIMS -> LABELS -> NOTES -> DONE)
;;; ---------------------------------------------------------------------------

(defun dk3s_error (msg)
  (if (not (member msg '("Function cancelled" "quit / exit abort")))
    (princ (strcat "\nDK3S: error at stage " g_dk3s_stage ": " msg))
  )
  (dk3s_restore)
  (princ)
)

(defun dk3s_restore ()
  (if g_dk3s_old_err (setq *error* g_dk3s_old_err))
  (if g_dk3s_old_vars
    (foreach v g_dk3s_old_vars (setvar (car v) (cdr v)))
  )
  (setq g_dk3s_old_vars nil)
)

(defun c:dk3s ( / s)
  (setq g_dk3s_old_err *error* *error* dk3s_error)
  (setq g_dk3s_stage "INIT" g_dk3s_cnt 0 g_dk3s_dim_mode "entmake")
  (setq g_dk3s_old_vars (list (cons "CMDECHO" (getvar "CMDECHO")) (cons "OSMODE" (getvar "OSMODE"))
                              (cons "CLAYER" (getvar "CLAYER"))))
  (setvar "CMDECHO" 0) (setvar "OSMODE" 0)
  (setq s g_dk3s_scale_den)

  (setq g_dk3s_stage "TABLES")
  (dk3s_make_ltype)
  (dk3s_make_layer g_dk3s_lay_main  7 "Continuous" g_dk3s_lw_main)
  (dk3s_make_layer g_dk3s_lay_thin  8 "Continuous" g_dk3s_lw_thin)
  (dk3s_make_layer g_dk3s_lay_axis  1 g_dk3s_ltype_axis g_dk3s_lw_thin)
  (dk3s_make_layer g_dk3s_lay_dim   4 "Continuous" g_dk3s_lw_dim)
  (dk3s_make_layer g_dk3s_lay_text  2 "Continuous" g_dk3s_lw_dim)
  (dk3s_make_layer g_dk3s_lay_frame 7 "Continuous" g_dk3s_lw_frame)
  (dk3s_make_style)
  (dk3s_make_dimstyle)

  (setq g_dk3s_stage "FRAME")
  (dk3s_draw_frame)

  (setq g_dk3s_stage "MAIN")
  (setq g_dk3s_ox (* s 48.0) g_dk3s_oy (* s 215.0) g_dk3s_k 1.0)   ; начало главного вида
  (dk3s_draw_main_view)

  (setq g_dk3s_stage "DIMS")
  (dk3s_draw_dims_main)

  (setq g_dk3s_stage "LABELS")
  (dk3s_draw_labels_main)

  (setq g_dk3s_stage "DETAIL")
  (setq g_dk3s_ox (* s 50.0) g_dk3s_oy (* s 95.0) g_dk3s_k g_dk3s_detail_mul)
  (dk3s_draw_detail_a)

  (setq g_dk3s_stage "NOTES")
  (setq g_dk3s_ox 0.0 g_dk3s_oy 0.0 g_dk3s_k 1.0)
  (dk3s_draw_notes (* s 232.0) (* s 160.0))

  (setq g_dk3s_stage "DONE")
  (command "_.ZOOM" "_E")
  (dk3s_restore)
  (princ (strcat "\nDK3S: drawing complete, entities: " (itoa g_dk3s_cnt)
                 ", dims: " g_dk3s_dim_mode ", text style: " g_dk3s_style))
  (princ)
)

(princ "\nDK3S v1.1.0 loaded. Command: DK3S")
(princ)
