;;; ============================================================================
;;;  dk3s_drawing.lsp  —  Чертёж общего вида датчика концентрации ДК-3С-210АВ
;;;  Версия: 1.0  (2026-09-19)
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
(setq g_dk3s_font         "ISOCPEUR.ttf")   ; шрифт надписей (замена: "arial.ttf")
(setq g_dk3s_txt_h        3.5)     ; высота текста на бумаге, мм
(setq g_dk3s_designation  "\\U+042D\\U+041A\\U+041E\\U+0420.\\U+0414\\U+041A3\\U+0421.210\\U+0410\\U+0412.000 \\U+0412\\U+041E")   ; обозначение (уточнить!)
(setq g_dk3s_name1        "\\U+0414\\U+0430\\U+0442\\U+0447\\U+0438\\U+043A \\U+043A\\U+043E\\U+043D\\U+0446\\U+0435\\U+043D\\U+0442\\U+0440\\U+0430\\U+0446\\U+0438\\U+0438")
(setq g_dk3s_name2        "\\U+0414\\U+041A-3\\U+0421-210\\U+0410\\U+0412")
(setq g_dk3s_name3        "\\U+041E\\U+0431\\U+0449\\U+0438\\U+0439 \\U+0432\\U+0438\\U+0434")
(setq g_dk3s_org          "\\U+042D\\U+041A\\U+041E\\U+0420, \\U+041B\\U+044C\\U+0432\\U+043E\\U+0432")
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

;; --- Корпус, фланец, сальниковая втулка ---------------------------------------
(setq g_dk3s_z_shell      237.6)   ; начало корпуса (резьба M42x3)
(setq g_dk3s_shell_d      42.0)    ; наружный диаметр резьбы M42x3
(setq g_dk3s_thread_pitch 3.0)
(setq g_dk3s_shell_ch     2.0)     ; фаска корпуса
(setq g_dk3s_z_relief     253.8)   ; начало проточки перед фланцем
(setq g_dk3s_relief_d     39.0)
(setq g_dk3s_z_plate      258.8)   ; фланец-пластина
(setq g_dk3s_plate_d      59.0)
(setq g_dk3s_z_hex1       265.8)   ; шестигранник S46
(setq g_dk3s_hex1_s       46.0)
(setq g_dk3s_z_hex1_ch    283.7)   ; начало фаски S46
(setq g_dk3s_z_cyl        285.8)   ; цилиндр Ø33
(setq g_dk3s_cyl_d        33.0)
(setq g_dk3s_z_groove     293.2)   ; шейка Ø28 с пояском Ø30
(setq g_dk3s_groove_d     28.0)
(setq g_dk3s_collar_d     30.0)
(setq g_dk3s_z_collar1    293.8)
(setq g_dk3s_z_collar2    295.6)
(setq g_dk3s_z_hex2       296.6)   ; шестигранник S36
(setq g_dk3s_hex2_s       36.0)
(setq g_dk3s_z_hex2_ch    305.0)
(setq g_dk3s_z_neck       306.6)   ; шейка Ø20,8
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
(defun dk3s_text (p h str rot just lay / hj vj)
  (cond ((= just 1) (setq hj 1 vj 2))
        ((= just 2) (setq hj 2 vj 0))
        ((= just 3) (setq hj 1 vj 0))
        ((= just 4) (setq hj 0 vj 2))
        (T (setq hj 0 vj 0)))
  (dk3s_made (entmake (list '(0 . "TEXT") '(100 . "AcDbEntity") (cons 8 lay)
                            '(100 . "AcDbText") (cons 10 p) (cons 40 h) (cons 1 str)
                            (cons 50 rot) (cons 7 g_dk3s_style) (cons 72 hj) (cons 11 p)
                            '(100 . "AcDbText") (cons 73 vj))))
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
                            '(70 . 0) '(3 . "Osevaya ____ _ ____ _ ____") '(72 . 65) '(73 . 4)
                            '(40 . 24.0) '(49 . 16.0) '(74 . 0) '(49 . -3.0) '(74 . 0)
                            '(49 . 2.0) '(74 . 0) '(49 . -3.0) '(74 . 0))))
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

;; Размерный стиль: текст 3,5, стрелки 2,5, DIMSCALE = знаменатель масштаба,
;; десятичный разделитель — запятая, нули подавляются, текст над линией (ЕСКД)
(defun dk3s_make_dimstyle ( / st lst)
  (if (not (tblsearch "DIMSTYLE" g_dk3s_dimstyle))
    (progn
      (setq lst (list '(0 . "DIMSTYLE") '(100 . "AcDbSymbolTableRecord")
                      '(100 . "AcDbDimStyleTableRecord") (cons 2 g_dk3s_dimstyle) '(70 . 0)
                      (cons 40 g_dk3s_scale_den)   ; DIMSCALE
                      '(41 . 2.5)                  ; DIMASZ
                      '(42 . 0.0)                  ; DIMEXO
                      '(43 . 7.0)                  ; DIMDLI
                      '(44 . 2.0)                  ; DIMEXE
                      (cons 140 g_dk3s_txt_h)      ; DIMTXT
                      '(144 . 1.0)                 ; DIMLFAC
                      '(147 . 1.0)                 ; DIMGAP
                      '(73 . 0) '(74 . 0)          ; DIMTIH DIMTOH — текст вдоль линии
                      '(77 . 1)                    ; DIMTAD — текст над линией
                      '(78 . 8)                    ; DIMZIN — без хвостовых нулей
                      '(271 . 1)                   ; DIMDEC — один знак
                      '(278 . 44)                  ; DIMDSEP — запятая
                      '(279 . 0)                   ; DIMTMOVE
                      '(171 . 2) '(172 . 0) '(174 . 0) '(175 . 0) '(176 . 0) '(177 . 0)))
      (if (setq st (tblobjname "STYLE" g_dk3s_style))
        (setq lst (append lst (list (cons 340 st))))     ; DIMTXSTY
      )
      (if (not (entmake lst))
        (progn
          ;; запасной вариант: переменные текущего стиля + размеры командой
          (setq g_dk3s_dim_mode "command")
          (setvar "DIMSCALE" g_dk3s_scale_den) (setvar "DIMASZ" 2.5) (setvar "DIMEXO" 0.0)
          (setvar "DIMEXE" 2.0) (setvar "DIMTXT" g_dk3s_txt_h) (setvar "DIMGAP" 1.0)
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
(defun dk3s_leader (pt ps dir str / h w pe)
  (setq h (* g_dk3s_txt_h g_dk3s_scale_den))
  (setq w (* h 0.6 (dk3s_strlen_vis str)))       ; оценка длины текста (ISOCPEUR ~0,6h)
  (setq pe (list (+ (car ps) (* dir w)) (cadr ps) 0.0))
  (dk3s_dot pt (* 0.5 g_dk3s_scale_den) g_dk3s_lay_thin)
  (dk3s_line pt ps g_dk3s_lay_thin)
  (dk3s_line ps pe g_dk3s_lay_thin)
  (dk3s_text (list (if (> dir 0) (car ps) (car pe)) (+ (cadr ps) (* 0.25 h)) 0.0)
             h str 0.0 0 g_dk3s_lay_text)
)

;;; ---------------------------------------------------------------------------
;;; 6. РАМКА И ОСНОВНАЯ НАДПИСЬ (ГОСТ 2.104, форма 1, 185x55)
;;;    Все размеры бумаги умножаются на g_dk3s_scale_den.
;;; ---------------------------------------------------------------------------

;; Линия внутри основной надписи по координатам бумаги (мм от левого нижнего угла штампа)
(defun dk3s_tb_line (x1 y1 x2 y2)
  (dk3s_line (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x1)) (+ g_dk3s_tby (* g_dk3s_scale_den y1)))
             (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x2)) (+ g_dk3s_tby (* g_dk3s_scale_den y2)))
             g_dk3s_lay_frame)
)

;; Текст в штампе: x,y — бумага (мм от угла штампа), h — высота на бумаге, just — как в dk3s_text
(defun dk3s_tb_text (x y h str just)
  (dk3s_text (dk3s_ps (+ g_dk3s_tbx (* g_dk3s_scale_den x)) (+ g_dk3s_tby (* g_dk3s_scale_den y)))
             (* h g_dk3s_scale_den) str 0.0 just g_dk3s_lay_text)
)

(defun dk3s_draw_frame ( / s w h x0 y0 x1 y1)
  (setq s g_dk3s_scale_den w (* s g_dk3s_sheet_w) h (* s g_dk3s_sheet_h))
  ;; граница листа (тонкая) и рамка (основная): поля 20 слева, 5 остальные
  (dk3s_rect (dk3s_ps 0.0 0.0) (dk3s_ps w h) g_dk3s_lay_thin)
  (setq x0 (* s 20.0) y0 (* s 5.0) x1 (- w (* s 5.0)) y1 (- h (* s 5.0)))
  (dk3s_rect (dk3s_ps x0 y0) (dk3s_ps x1 y1) g_dk3s_lay_frame)
  ;; основная надпись — правый нижний угол рамки
  (setq g_dk3s_tbx (- x1 (* s 185.0)) g_dk3s_tby y0)
  (dk3s_tb_line 0.0 0.0 0.0 55.0)  (dk3s_tb_line 0.0 55.0 185.0 55.0)
  ;; левая часть 65 мм: вертикали и горизонтали через 5
  (dk3s_tb_line 65.0 0.0 65.0 55.0)
  (dk3s_tb_line 7.0 30.0 7.0 55.0)   (dk3s_tb_line 17.0 0.0 17.0 55.0)
  (dk3s_tb_line 40.0 0.0 40.0 55.0)  (dk3s_tb_line 55.0 0.0 55.0 55.0)
  (foreach yy '(5.0 10.0 15.0 20.0 25.0 30.0 35.0 40.0 45.0 50.0) (dk3s_tb_line 0.0 yy 65.0 yy))
  ;; правая часть 120 мм
  (dk3s_tb_line 65.0 40.0 185.0 40.0)   ; низ графы обозначения
  (dk3s_tb_line 65.0 15.0 135.0 15.0)   ; низ графы наименования
  (dk3s_tb_line 135.0 0.0 135.0 40.0)
  (dk3s_tb_line 135.0 35.0 185.0 35.0)  (dk3s_tb_line 135.0 30.0 185.0 30.0)
  (dk3s_tb_line 135.0 25.0 185.0 25.0)
  (dk3s_tb_line 150.0 30.0 150.0 40.0)  (dk3s_tb_line 170.0 30.0 170.0 40.0)
  (dk3s_tb_line 140.0 30.0 140.0 35.0)  (dk3s_tb_line 145.0 30.0 145.0 35.0)
  (dk3s_tb_line 155.0 25.0 155.0 30.0)
  ;; подписи граф (2,5 мм)
  (dk3s_tb_text 3.5 31.2 2.5 "\\U+0418\\U+0437\\U+043C." 3)      (dk3s_tb_text 12.0 31.2 2.5 "\\U+041B\\U+0438\\U+0441\\U+0442" 3)
  (dk3s_tb_text 28.5 31.2 2.5 "\\U+2116 \\U+0434\\U+043E\\U+043A\\U+0443\\U+043C." 3) (dk3s_tb_text 47.5 31.2 2.5 "\\U+041F\\U+043E\\U+0434\\U+043F." 3)
  (dk3s_tb_text 60.0 31.2 2.5 "\\U+0414\\U+0430\\U+0442\\U+0430" 3)
  (dk3s_tb_text 1.0 26.2 2.5 "\\U+0420\\U+0430\\U+0437\\U+0440\\U+0430\\U+0431." 0)   (dk3s_tb_text 1.0 21.2 2.5 "\\U+041F\\U+0440\\U+043E\\U+0432." 0)
  (dk3s_tb_text 1.0 16.2 2.5 "\\U+0422.\\U+043A\\U+043E\\U+043D\\U+0442\\U+0440." 0)  (dk3s_tb_text 1.0 6.2 2.5 "\\U+041D.\\U+043A\\U+043E\\U+043D\\U+0442\\U+0440." 0)
  (dk3s_tb_text 1.0 1.2 2.5 "\\U+0423\\U+0442\\U+0432." 0)
  (dk3s_tb_text 142.5 36.2 2.5 "\\U+041B\\U+0438\\U+0442." 3)    (dk3s_tb_text 160.0 36.2 2.5 "\\U+041C\\U+0430\\U+0441\\U+0441\\U+0430" 3)
  (dk3s_tb_text 177.5 36.2 2.5 "\\U+041C\\U+0430\\U+0441\\U+0448\\U+0442\\U+0430\\U+0431" 3)
  (dk3s_tb_text 137.0 26.2 2.5 "\\U+041B\\U+0438\\U+0441\\U+0442" 0)    (dk3s_tb_text 157.0 26.2 2.5 "\\U+041B\\U+0438\\U+0441\\U+0442\\U+043E\\U+0432" 0)
  ;; содержимое граф
  (dk3s_tb_text 125.0 45.5 5.0 g_dk3s_designation 3)
  (dk3s_tb_text 100.0 32.5 3.5 g_dk3s_name1 3)
  (dk3s_tb_text 100.0 26.0 3.5 g_dk3s_name2 3)
  (dk3s_tb_text 100.0 18.0 3.5 g_dk3s_name3 3)
  (dk3s_tb_text 177.5 31.0 3.5 (strcat "1:" (rtos g_dk3s_scale_den 2 0)) 3)
  (dk3s_tb_text 148.0 26.2 2.5 "1" 0)       (dk3s_tb_text 173.0 26.2 2.5 "1" 0)
  (dk3s_tb_text 160.0 10.0 3.5 g_dk3s_org 3)
  (dk3s_tb_text 18.0 26.2 2.5 g_dk3s_author 0)
  (dk3s_tb_text 18.0 21.2 2.5 g_dk3s_checker 0)
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

;; Шестигранник в боковой проекции (грань к наблюдателю): s — размер под ключ
(defun dk3s_hex (z1 z2 s / e)
  (setq e (/ s (cos (dk3s_rad 30.0))))
  (dk3s_cyl z1 z2 (/ e 2.0) 0.0)
  (dk3s_cyl z1 z2 (/ e 4.0) 0.0)
  (dk3s_face z1 (/ e -2.0) (/ e 2.0))
  (dk3s_face z2 (/ e -2.0) (/ e 2.0))
  e
)

;; Фаска шестигранника: от углов e при z1 к диаметру d при z2
(defun dk3s_hex_chamfer (z1 z2 e d)
  (dk3s_line (dk3s_p z1 (/ e 2.0)) (dk3s_p z2 (/ d 2.0)) g_dk3s_lay_main)
  (dk3s_line (dk3s_p z1 (/ e -2.0)) (dk3s_p z2 (/ d -2.0)) g_dk3s_lay_main)
  (dk3s_face z2 (/ d -2.0) (/ d 2.0))
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
(defun dk3s_draw_gland ( / rs rr rp e1 e2 rc rg rk rn rst zsh d1 h)
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
  ;; шестигранник S46 с фаской
  (setq e1 (dk3s_hex g_dk3s_z_hex1 g_dk3s_z_hex1_ch g_dk3s_hex1_s))
  (dk3s_hex_chamfer g_dk3s_z_hex1_ch g_dk3s_z_cyl e1 g_dk3s_hex1_s)
  ;; цилиндр Ø33, шейка Ø28 с пояском Ø30
  (setq rc (/ g_dk3s_cyl_d 2.0) rg (/ g_dk3s_groove_d 2.0) rk (/ g_dk3s_collar_d 2.0))
  (dk3s_cyl g_dk3s_z_cyl g_dk3s_z_groove rc 0.0)
  (dk3s_face g_dk3s_z_groove (- rc) rc)
  (dk3s_cyl g_dk3s_z_groove g_dk3s_z_collar1 rg 0.0)
  (dk3s_face g_dk3s_z_collar1 (- rk) rk)
  (dk3s_cyl g_dk3s_z_collar1 g_dk3s_z_collar2 rk 0.0)
  (dk3s_face g_dk3s_z_collar2 (- rk) rk)
  (dk3s_cyl g_dk3s_z_collar2 g_dk3s_z_hex2 rg 0.0)
  ;; шестигранник S36 с фаской
  (setq e2 (dk3s_hex g_dk3s_z_hex2 g_dk3s_z_hex2_ch g_dk3s_hex2_s))
  (dk3s_hex_chamfer g_dk3s_z_hex2_ch g_dk3s_z_neck e2 g_dk3s_hex2_s)
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
(defun dk3s_draw_axis ()
  (dk3s_line (dk3s_p -6.0 0.0) (dk3s_p (+ g_dk3s_z_we_end g_dk3s_conn_collar_l g_dk3s_conn_body_l
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
  (dk3s_leader (dk3s_p 6.0 (- rtap)) (dk3s_p -2.0 (- (- rtip) 13.0)) 1 "\\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434 \\U+0440\\U+0430\\U+0431\\U+043E\\U+0447\\U+0435\\U+0433\\U+043E \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434\\U+0430")
  ;; заголовок вида
  (dk3s_text (dk3s_p (/ zw 2.0) (+ rtip 14.0)) (* h 1.4) "\\U+0410 (2:1)" 0.0 3 g_dk3s_lay_text)
  (dk3s_line (dk3s_p (- (/ zw 2.0) 7.0) (+ rtip 13.2)) (dk3s_p (+ (/ zw 2.0) 7.0) (+ rtip 13.2)) g_dk3s_lay_thin)
)

;;; ---------------------------------------------------------------------------
;;; 9. РАЗМЕРЫ, ВЫНОСКИ И ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ ГЛАВНОГО ВИДА
;;;    Размерные точки берутся из таблицы параметров — значения вычисляются CAD.
;;; ---------------------------------------------------------------------------

(defun dk3s_draw_dims_main ( / rs re e1 e2 rp zh1 zh2 zre1 zre2 y1 y2 y3 y4 zpl)
  (setq rs (/ g_dk3s_sleeve_d 2.0) re (/ g_dk3s_re_d 2.0) rp (/ g_dk3s_plate_d 2.0))
  (setq e1 (/ g_dk3s_hex1_s (cos (dk3s_rad 30.0))) e2 (/ g_dk3s_hex2_s (cos (dk3s_rad 30.0))))
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
  ;; диаметры и размеры под ключ — вертикальные размеры на деталях
  (dk3s_dim (dk3s_p 130.0 rs) (dk3s_p 130.0 (- rs)) (dk3s_p 130.0 0.0) 90.0 "%%c<>")
  (dk3s_dim (dk3s_p 246.0 (/ g_dk3s_shell_d 2.0)) (dk3s_p 246.0 (/ g_dk3s_shell_d -2.0)) (dk3s_p 246.0 0.0) 90.0
            (strcat "M<>x" (dk3s_num g_dk3s_thread_pitch 0)))
  (dk3s_dim (dk3s_p 262.3 rp) (dk3s_p 262.3 (- rp)) (dk3s_p 262.3 0.0) 90.0 "%%c<>")
  (setq zh1 (/ (+ g_dk3s_z_hex1 g_dk3s_z_hex1_ch) 2.0) zh2 (/ (+ g_dk3s_z_hex2 g_dk3s_z_hex2_ch) 2.0))
  (dk3s_dim (dk3s_p zh1 (/ g_dk3s_hex1_s 2.0)) (dk3s_p zh1 (/ g_dk3s_hex1_s -2.0)) (dk3s_p zh1 0.0) 90.0 "S<>")
  (dk3s_dim (dk3s_p zh2 (/ g_dk3s_hex2_s 2.0)) (dk3s_p zh2 (/ g_dk3s_hex2_s -2.0)) (dk3s_p zh2 0.0) 90.0 "S<>")
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

(defun dk3s_draw_labels_main ( / ya yb yc rs rp rc rre e2)
  (setq ya 52.0 yb 68.0 yc 84.0)                  ; полки выносок: три ряда над датчиком
  (setq rs (/ g_dk3s_sleeve_d 2.0) rp (/ g_dk3s_plate_d 2.0) rc (/ g_dk3s_clamp_d 2.0))
  (setq e2 (/ g_dk3s_hex2_s (cos (dk3s_rad 30.0))) rre (+ g_dk3s_re_r (/ g_dk3s_re_d 2.0)))
  ;; ряд A
  (dk3s_leader (dk3s_p (- g_dk3s_z_sleeve 2.0) (+ g_dk3s_tip_off (/ g_dk3s_tip_d 2.0)))
               (dk3s_p 22.0 ya) 1 "\\U+041D\\U+0430\\U+043A\\U+043E\\U+043D\\U+0435\\U+0447\\U+043D\\U+0438\\U+043A (\\U+0441\\U+043C. \\U+0410)")
  (dk3s_leader (dk3s_p 250.0 (/ g_dk3s_shell_d 2.0)) (dk3s_p 236.0 ya) 1 "\\U+041A\\U+043E\\U+0440\\U+043F\\U+0443\\U+0441")
  (dk3s_leader (dk3s_p (+ g_dk3s_z_clamp1 3.8) rc) (dk3s_p 372.0 ya) 1 "\\U+0425\\U+043E\\U+043C\\U+0443\\U+0442")
  (dk3s_leader (dk3s_p 492.0 (/ g_dk3s_conn_body_d 2.0)) (dk3s_p 455.0 ya) 1 "\\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434 \\U+0440\\U+0430\\U+0431\\U+043E\\U+0447\\U+0435\\U+0433\\U+043E \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434\\U+0430")
  ;; ряд B
  (dk3s_leader (dk3s_p 150.0 rs) (dk3s_p 120.0 yb) 1 "\\U+0417\\U+0430\\U+0449\\U+0438\\U+0442\\U+043D\\U+0430\\U+044F \\U+0433\\U+0438\\U+043B\\U+044C\\U+0437\\U+0430")
  (dk3s_leader (dk3s_p 300.8 (/ e2 2.0)) (dk3s_p 282.0 yb) 1 "\\U+0421\\U+0430\\U+043B\\U+044C\\U+043D\\U+0438\\U+043A\\U+043E\\U+0432\\U+0430\\U+044F \\U+0432\\U+0442\\U+0443\\U+043B\\U+043A\\U+0430")
  (dk3s_leader (dk3s_p 430.0 (+ g_dk3s_bridge_r (/ g_dk3s_bridge_d 2.0))) (dk3s_p 400.0 yb) 1
               "\\U+042D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+043B\\U+0438\\U+0442\\U+0438\\U+0447\\U+0435\\U+0441\\U+043A\\U+0438\\U+0439 \\U+043C\\U+043E\\U+0441\\U+0442\\U+0438\\U+043A (2 \\U+0448\\U+0442.)")
  (dk3s_leader (dk3s_p 605.0 (+ g_dk3s_re_r (/ g_dk3s_conn_pin_d 2.0))) (dk3s_p 590.0 yb) 1
               "\\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434 \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434\\U+0430 \\U+0441\\U+0440\\U+0430\\U+0432\\U+043D\\U+0435\\U+043D\\U+0438\\U+044F")
  ;; ряд C
  (dk3s_leader (dk3s_p 8.0 (/ g_dk3s_guard_w 2.0)) (dk3s_p -12.0 yc) 1 "\\U+0417\\U+0430\\U+0449\\U+0438\\U+0442\\U+043D\\U+0430\\U+044F \\U+0441\\U+043A\\U+043E\\U+0431\\U+0430")
  (dk3s_leader (dk3s_p 262.3 rp) (dk3s_p 256.0 yc) 1 "\\U+0424\\U+043B\\U+0430\\U+043D\\U+0435\\U+0446")
  (dk3s_leader (dk3s_p 330.0 (/ g_dk3s_tag_w 2.0)) (dk3s_p 320.0 yc) 1 "\\U+0411\\U+0438\\U+0440\\U+043A\\U+0430 \\U+0441 \\U+0437\\U+0430\\U+0432\\U+043E\\U+0434\\U+0441\\U+043A\\U+0438\\U+043C \\U+043D\\U+043E\\U+043C\\U+0435\\U+0440\\U+043E\\U+043C")
  (dk3s_leader (dk3s_p 560.0 rre) (dk3s_p 520.0 yc) 1 "\\U+042D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434 \\U+0441\\U+0440\\U+0430\\U+0432\\U+043D\\U+0435\\U+043D\\U+0438\\U+044F (2 \\U+0448\\U+0442.)")
  ;; снизу
  (dk3s_leader (dk3s_p 400.0 (- g_dk3s_se_r (/ g_dk3s_se_d 2.0))) (dk3s_p 330.0 -46.0) 1
               "\\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434 \\U+0432\\U+0441\\U+043F\\U+043E\\U+043C\\U+043E\\U+0433\\U+0430\\U+0442\\U+0435\\U+043B\\U+044C\\U+043D\\U+043E\\U+0433\\U+043E \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434\\U+0430")
  ;; обозначение выносного элемента А на главном виде
  (dk3s_circle (dk3s_p 9.0 g_dk3s_tip_off) 20.0 g_dk3s_lay_thin)
  (dk3s_text (dk3s_p 26.0 (+ g_dk3s_tip_off 14.0)) (* 1.4 g_dk3s_txt_h g_dk3s_scale_den) "\\U+0410" 0.0 0 g_dk3s_lay_text)
)

;; Технические требования — над основной надписью
(defun dk3s_draw_notes (x y / h dy lines i)
  (setq h (* g_dk3s_txt_h g_dk3s_scale_den) dy (* h 1.7))
  (setq lines (list
    "1. * \\U+0420\\U+0430\\U+0437\\U+043C\\U+0435\\U+0440\\U+044B \\U+0434\\U+043B\\U+044F \\U+0441\\U+043F\\U+0440\\U+0430\\U+0432\\U+043E\\U+043A."
    "2. \\U+0420\\U+0430\\U+0431\\U+043E\\U+0447\\U+0438\\U+0439 \\U+044D\\U+043B\\U+0435\\U+043A\\U+0442\\U+0440\\U+043E\\U+0434 - \\U+043F\\U+0440\\U+043E\\U+0432\\U+043E\\U+043B\\U+043E\\U+043A\\U+0430 \\U+00D81,4 \\U+043C\\U+043C, \\U+0432\\U+044B\\U+0441\\U+0442\\U+0443\\U+043F 2 \\U+043C\\U+043C."
    "3. \\U+041D\\U+0430\\U+043A\\U+043E\\U+043D\\U+0435\\U+0447\\U+043D\\U+0438\\U+043A - \\U+0448\\U+0435\\U+0441\\U+0442\\U+0438\\U+0433\\U+0440\\U+0430\\U+043D\\U+043D\\U+0438\\U+043A 1/4\", \\U+0440\\U+0435\\U+0437\\U+044C\\U+0431\\U+0430 \\U+0442\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434\\U+0430 - \\U+0448\\U+0430\\U+0433 0,5 \\U+043C\\U+043C."
    "4. \\U+041F\\U+0440\\U+0438\\U+0441\\U+043E\\U+0435\\U+0434\\U+0438\\U+043D\\U+0435\\U+043D\\U+0438\\U+0435 - \\U+0440\\U+0435\\U+0437\\U+044C\\U+0431\\U+0430 M42x3 \\U+0432\\U+0445\\U+043E\\U+0434\\U+043D\\U+043E\\U+0433\\U+043E \\U+0443\\U+0437\\U+043B\\U+0430 \\U+0444\\U+043B\\U+0430\\U+043D\\U+0446\\U+0430 DN50."
    "5. \\U+0422\\U+043E\\U+043A\\U+043E\\U+043E\\U+0442\\U+0432\\U+043E\\U+0434\\U+044B: RE1 - \\U+0441\\U+0438\\U+043D\\U+0438\\U+0439, RE2 - \\U+0431\\U+0435\\U+043B\\U+044B\\U+0439, WE - \\U+043A\\U+0440\\U+0430\\U+0441\\U+043D\\U+044B\\U+0439, SE - \\U+0447\\U+0451\\U+0440\\U+043D\\U+044B\\U+0439."
    "6. \\U+0413\\U+0435\\U+043E\\U+043C\\U+0435\\U+0442\\U+0440\\U+0438\\U+044F - \\U+043F\\U+043E \\U+043C\\U+043E\\U+043D\\U+0442\\U+0430\\U+0436\\U+043D\\U+043E\\U+043C\\U+0443 \\U+0447\\U+0435\\U+0440\\U+0442\\U+0435\\U+0436\\U+0443 \\U+0442\\U+0435\\U+0445\\U+043E\\U+043F\\U+0438\\U+0441\\U+0430\\U+043D\\U+0438\\U+044F K1 (\\U+043B\\U+0438\\U+0441\\U+0442 16)."))
  (setq i 0)
  (foreach s lines
    (dk3s_text (dk3s_ps x (- y (* i dy))) h s 0.0 0 g_dk3s_lay_text)
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
  (dk3s_make_layer g_dk3s_lay_main  7 "Continuous" 50)
  (dk3s_make_layer g_dk3s_lay_thin  8 "Continuous" 25)
  (dk3s_make_layer g_dk3s_lay_axis  1 g_dk3s_ltype_axis 25)
  (dk3s_make_layer g_dk3s_lay_dim   4 "Continuous" 25)
  (dk3s_make_layer g_dk3s_lay_text  2 "Continuous" 25)
  (dk3s_make_layer g_dk3s_lay_frame 7 "Continuous" 70)
  (dk3s_make_style)
  (dk3s_make_dimstyle)

  (setq g_dk3s_stage "FRAME")
  (dk3s_draw_frame)

  (setq g_dk3s_stage "MAIN")
  (setq g_dk3s_ox (* s 45.0) g_dk3s_oy (* s 220.0) g_dk3s_k 1.0)   ; начало главного вида
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
  (dk3s_draw_notes (* s 232.0) (* s 118.0))

  (setq g_dk3s_stage "DONE")
  (command "_.ZOOM" "_E")
  (dk3s_restore)
  (princ (strcat "\nDK3S: drawing complete, entities: " (itoa g_dk3s_cnt)
                 ", dims: " g_dk3s_dim_mode ", text style: " g_dk3s_style))
  (princ)
)

(princ "\nDK3S v1.0 loaded. Command: DK3S")
(princ)
