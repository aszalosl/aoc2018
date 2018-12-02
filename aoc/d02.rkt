#lang racket
(define ids (file->lines "02.in"))

; elemek ismétlődésének száma rendezett lista esetén 
(define (counter lst)
  (define (count ch lst n ns)
    (cond
      [(empty? lst) (cons n ns)]
      [(eq? ch (car lst)) (count ch (cdr lst) (add1 n) ns)]
      [else (count (car lst) (cdr lst) 1 (cons n ns))]))
  (count (car lst) (cdr lst) 1 '()))

; szerepel-e benne 2 illetve 3
(define (double-test str)
  (let ([lst (counter (sort (string->list str) char<?))])
    (cons (member 2 lst) (member 3 lst))))

; ismétlődések összeszámolása
(define (dc lst)
  (define (double-calc lst two three)
    (cond
      [(empty? lst) (cons two three)]
      [(and (caar lst) (cdar lst))      ; mindkettő
       (double-calc (cdr lst) (add1 two) (add1 three))]
      [(caar lst)                       ; csak 2 
       (double-calc (cdr lst) (add1 two) three)]
      [(cdar lst)                       ; csak 3
       (double-calc (cdr lst) two (add1 three))]
      [else                             ; egyik sem
       (double-calc (cdr lst) two three)]
      ))
  (double-calc lst 0 0))

; első rész válasza
(define counters (dc (map double-test ids)))
(display (* (car counters) (cdr counters)))
(display "\n")

; két azonos hosszú sztring csak egy betűben tér el?
(define (dist1 lst1 lst2)
  (cond
    [(equal? lst1 lst2) #f]
    [(equal? (car lst1) (car lst2)) (dist1 (cdr lst1) (cdr lst2))]
    [else (equal? (cdr lst1) (cdr lst2))]))

; két szting közös része (ugyanazon indexeknél)
(define (common str1 str2)
  (define (cmn lst0 lst1 lst2)
    (cond
      [(empty? lst1) (list->string (reverse lst0))]
      [(equal? (car lst1) (car lst2))
       (cmn (cons (car lst1) lst0) (cdr lst1) (cdr lst2))]
      [else
       (cmn lst0 (cdr lst1) (cdr lst2))]))
  (cmn '() (string->list str1) (string->list str2)))
    
    
; második rész válasza
(display (car (for*/list ([i ids]
                          [j ids]
                          #:when (dist1 (string->list i)
                                        (string->list j)))
                (common i j))))