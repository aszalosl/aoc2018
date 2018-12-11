#lang racket

(define STEP 7)
(define TAKE-IT 23)
 

(define (step lst tsl n limit ps)
  (cond
    [(zero? (modulo n TAKE-IT))
     ;(display (format "~a ~a ~a\n" (reverse tsl) lst n))
     (if (>= (length tsl) (add1 STEP))
         (let-values ([(back other) (split-at tsl (add1 STEP))])
           ;(display (format "~a| ~a" back other))
           (let* ([rev (reverse back)]
                  [x (car rev)]
                  [y (cadr rev)]
                  [remains (cddr rev)]
                  [id (modulo n (vector-length ps))])
            ;(display (format "~a ~a\n" id x))
            (vector-set! ps id (+ (vector-ref ps id) x n))
            (step (append remains lst) (cons y other) (add1 n) limit ps)))
         (let-values ([(start end) (split-at lst 
                                             (- (+ (length lst) 
                                                   (length tsl)) 8))])
             ;(display (format "start: ~a\nend: ~a\n" start end))
  	       (let ([id (modulo n (vector-length ps))]
                 [lst1 (append (cddr end) (reverse tsl) start)]
                 [tsl1 (list (cadr end))])
             (vector-set! ps id (+ (vector-ref ps id) (car end) n))
	           (step lst1 tsl1 (add1 n) limit ps))
             ;(display (format "~a| ~a" start end))
             ;(display "TODO hard")
             ;(display (format "~a ~a ~a\n" (reverse tsl) lst n)))
	       ))]
    [(= n limit)
     ;(append (reverse tsl) lst)]
     (apply max (vector->list ps))]
    [(null? lst)
     (let ([lst0 (reverse tsl)])
       (step (cdr lst0) (list n (car lst0)) (add1 n) limit ps))]
    [(null? (cdr lst))
     (step (append (reverse tsl) lst (list n)) '() (add1 n) limit ps)]
    [else
      (step (cdr lst) (cons n (cons (car lst) tsl)) (add1 n) limit ps)]))

;(displayln (step '(0) '() 1 25 9))
;(displayln (step '(0) '() 1 1619 10))
;(displayln points)

(define (d08 players worth)
  (define points (make-vector players))
  (displayln (step '(0) '() 1 (add1 worth) points)))

