#lang racket
(require srfi/1) ; circular-list
; olvassuk be az összes számot egy listába
(define numbers
  (map string->number
       (string-split
        (file->string "01.in") "\n")))
; majd összegezzük a listát
(display (apply + numbers))
(display "\n")

;; első ismétlődés keresése
(define (first-twice numbers)
  (define (cycle fr h ns)     ; kell egy rekurzív függvény
    (if (hash-has-key? h fr)  ; ha már elődult, kész vagyunk
        fr
        (begin
          (hash-set! h fr 1)  ; egyébként eltároljuk
          (cycle (+ (car ns) fr) h (cdr ns))))) ; és mehet a következő
  (define ht (make-weak-hash))
  ; a kiinduló frekvencia 0, kell egy üres hash, illetve a lista végtelenítve
  (cycle 0 ht (apply circular-list numbers))) 

(module+ test
  (require rackunit)
  (check-equal? (first-twice '(1 -1)) 0)
  (check-equal? (first-twice '(3 3 4 -2 -4)) 10)
  (check-equal? (first-twice '(-6 3 8 5 -6)) 5)
  (check-equal? (first-twice '(7 7 -2 -7 -4)) 14))

(display (first-twice numbers))
