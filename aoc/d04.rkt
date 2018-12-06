#lang racket
(define months (vector 31 28 31 30 31 30 31 31 30 31 30 31))

(define (last-day month day)
  (= day (vector-ref months (sub1 month))))

;[1518-11-01 00:25] wakes up
;01234567890123456789012345678

(define (dt-split str)  ; split a line into numbers
  (letrec ([month (string->number (substring str  6  8))]
           [day   (string->number (substring str  9 11))]
           [hour  (string->number (substring str 12 14))]
           [min   (string->number (substring str 15 17))]
           [ch    (string-ref str 25)]
           [key   (cond
                    [(equal? ch #\a) "a"]
                    [(equal? ch #\u) "u"]
                    [else (car (string-split (substring str 25)))])])
    (if (= 23 hour)
        (if (last-day month day)
            (list (add1 month) 1 (- min 60) key)
            (list month (add1 day) (- min 60) key))
        (list month day min key))))

(define (less-list x y)    ; for soring the records
  (or (< (car x) (car y))
      (and (= (car x) (car y))
           (less-list (cdr x) (cdr y)))))

(define (collect lst)      ; collect together the actions of the same day
  (define (collect2 lst acc acts month day guard)
    (cond
      [(null? lst) (cons  (cons (list guard month day)
                                (list (reverse acts)))
                          acc)] ; finish
      [(and (= month (caar lst))
            (= day (cadar lst)))
       (collect2 (cdr lst) acc (cons (caddar lst) acts) month day guard)] ; store the next action
      [else
       (collect2 (cdr lst)
                 (cons (cons (list guard month day) (list (reverse acts)))
                       acc)
                 '() (caar lst) (cadar lst) (car (cdddar lst)))])) ; new day, new guard
  (collect2 lst '() '() 0 0 0))

(define sleeps (make-hash))

(define (inc-hash hash guard start stop) ; increment one sleep
  (for ([i (in-range start stop)])
    (hash-set! hash (cons guard i)
	       (add1 (hash-ref hash (cons guard i) 0)))))

(define (store-sleeps hash guard lst) ; increment all the sleeps
  (unless (empty? lst)
    (inc-hash hash guard (first lst) (second lst))
    (store-sleeps hash guard (cddr lst))))

(define (store hash pair)
  (let ([guard (caar pair)]
        [data (cadr pair)])
    (store-sleeps hash guard data)))

(define (sum-guards hash guards)
  (for/list ([g guards])
    (list g (apply + (for/list ([i (in-range 60)])
                       (hash-ref sleeps (cons g i) 0))))))

(define (solution1 hash guards)
  (letrec ([guard (car (argmax second (sum-guards hash guards)))]
           [ns (for/list ([i (in-range 60)])
                 (list i (hash-ref hash (cons guard i) 0)))])
    (* (string->number (substring guard 1))
       (car (argmax second ns)))))

(define (solution2 hash)
  (letrec ([maxi (argmax  cdr (hash->list hash))]
           [guard (string->number (substring (caar maxi) 1))]
           [minute (cdar maxi)])
    (* guard minute)))

(define lines (collect (sort (map dt-split (file->lines "04.in")) less-list)))

(for ([pair lines]) (store sleeps pair))

(define guards (list->set (map car (hash-keys sleeps))))

(display (solution1 sleeps guards))
(display "\n")
(display (solution2 sleeps))
