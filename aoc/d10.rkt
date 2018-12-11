#lang racket

(define (scan-star line)
  (let ([x (string->number (string-trim (substring line 10 16)))]
	[y (string->number (string-trim (substring line 17 24)))]
	[u (string->number (string-trim (substring line 36 38)))]
	[v (string->number (string-trim (substring line 39 42)))])
    (list x y u v)))

(define lines (map scan-star (file->lines "10.in")))

(define (points i) 
  (for/list ([d lines])
            (cons (+ (first d) (* i (third d)))
                  (+ (second d) (* i (fourth d))))))

(define (limits ps)
  (let* ([xs (map car ps)]
         [ys (map cdr ps)]
         [xl (apply min xs)]
         [xh (apply max xs)]
         [yl (apply min ys)]
         [yh (apply max ys)])
    (list xl xh yl yh)))

(define (rectangle ps)
  (let* ([lst (limits ps)]
         [xl (first lst)]
         [xh (second lst)]
         [yl (third lst)]
         [yh (fourth lst)])
    (* (- xh xl) (- yh yl))))

(define minimal
  (let* ([sizes (for/list ([i (range 15000)]) (cons i (rectangle (points i))))]
        [min-prod (apply min (map cdr sizes))])
  (filter (lambda (x) (= min-prod (cdr x))) sizes)))


(define (plot i)
  (let* ([ps (points i)] 
         [borders (limits ps)])
    (for ([y (range (third borders) (add1 (fourth borders)))])
         (for ([x (range (first borders) (add1 (second borders)))])
           (if (member (cons x y) ps)
               (display "#")
               (display ".")))
         (display "\n"))))
(plot (caar minimal))
