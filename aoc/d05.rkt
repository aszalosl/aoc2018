#lang racket
(define lines (string->list (car (file->lines "05.in"))))

(define (opposite a b)
  (and
   (not (null? a))
   (not (null? b))
   (not (eq? a b))
   (eq? (char-upcase a) (char-upcase b))))

(define (react row stack skip)
  (cond
    [(empty? row) (length stack)]
    [(empty? stack)
     (react (cdr row) (list (car row)) skip)]
    [(eq? (char-downcase (car row)) skip)
     (react (cdr row) stack skip)]
    [(opposite (car row) (car stack))
     (react (cdr row) (cdr stack) skip)]
    [else
     (react (cdr row) (cons (car row) stack) skip)]))

; part 1
(display (react lines '() '()))

;part 2
(define (alfabet row)
  (for/list ([c (string->list "abcdefghijklmnopqrstuvwxyz")])
    (react row '() c)))

(display "\n")
(display (apply min (alfabet lines)))