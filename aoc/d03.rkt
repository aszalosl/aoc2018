#lang racket

(define (filter-num-char ch)
  (if (char-numeric? ch) ch #\space))

(define (filter-num str)
  (list->string
   (map filter-num-char (string->list str))))

(define facts
  (map (lambda (line)
         (map string->number (string-split (filter-num line)))) (file->lines "03.in")))


(define (less-pair p1 p2)
  (cond
    [(< (car p1) (car p2)) #t]
    [(< (car p2) (car p1)) #f]
    [(< (second p1) (second p2)) #t]
    [(< (second p2) (second p1)) #f]
    [else #t]))

(define pos (for*/list
                ([f facts]
                 [i (range (fourth f))]
                 [j (range (fifth f))])
                 (list (+ (second f) i) (+ (third f) j))))

(define (pair-length pairs)
  (define (pl c p ps t)
    (cond
      [(empty? ps) (cons (cons c p) t)]
      [(equal? p (car ps)) (pl (add1 c) p (cdr ps) t)]
      [else (pl 1 (car ps) (cdr ps) (cons (cons c p) t))]))
  (pl 1 (car pairs) (cdr pairs) '()))

(define all (pair-length (sort pos less-pair)))
;(define double (filter-not (lambda (x) (= 1 (car x))) all))
(define simple (filter (lambda (x) (= 1 (car x))) all))
(define s (for/set ([t all] #:when (= 1 (first t))) (list (second t) (third t))))
(display (- (length all) (length simple)))
(display "\n")

;; part 2
(define (free lst)
  (cond
    [(empty? lst) '()]
    [(letrec ([f (car lst)]
q              [h (for*/set ([i (range (fourth f))]
                            [j (range (fifth f))])
                (list (+ (second f) i) (+ (third f) j)))])
       (subset? h s)) (caar lst)]
    [else (free (cdr lst))]))

(display (free facts))