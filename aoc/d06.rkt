#lang racket

(define (split-line row)
  (map string->number (string-split row ", ")))

(define NAN -1)  ; tie in distance
(define MAX 100) ; maximum number of points
;(define REGION 32)
;(define FILE "060.in")
(define REGION 10000)
(define FILE "06.in")

(define lines (map split-line (file->lines FILE)))

(define xl (apply min (map car lines)))
(define xh (apply max (map car lines)))
(define yl (apply min (map cadr lines)))
(define yh (apply max (map cadr lines)))

(define (min-distance x y lst)
  (let* ([all (for/list ([uv lst][i (range MAX)])
          (cons (+ (abs (- x (car uv)))
                (abs (- y (cadr uv)))) i))]
         [ds (sort all #:key car < )])
    (if (< (caar ds) (caadr ds)) (cdar ds) NAN)))

(define labels
  (for*/hash ([i (in-range xl (add1 xh))]
              [j (in-range yl (add1 yh))])
    (values (cons i j) (min-distance i j lines))))

(define (border labels) (set-add
  (for/set ([(k v) labels] 
                   #:when (or (= (car k) xl)
                              (= (car k) xh)
                              (= (cdr k) yl)
                              (= (cdr k) yh))) v) NAN))

(define (mayor-inner border-set) 
  (let ([elems (for/list ([(k v) labels] #:when (not (set-member? border-set v))) v)]
        [ht (make-hash)])
    (for ([key elems]) (hash-update! ht key add1 0))
      (car (sort (hash->list ht) #:key cdr > ))))

; result 1
(display (cdr (mayor-inner (border labels))))

(define (sum-distance x y lst)
  (apply + (for/list ([uv lst][i (range MAX)])
             (+ (abs (- x (car uv)))
                (abs (- y (cadr uv)))) )))

(define (region lst)
  (let ([cnt 0])
    (for* ([i (in-range xl (add1 xh))]
           [j (in-range yl (add1 yh))] 
           #:when (< (sum-distance i j lst) REGION)) 
      (set! cnt (add1 cnt)))
    cnt))
;result 2
(display "\n")
(display (region lines))
