#lang racket
(require racket/set)

;(define FILE "070.in")
(define FILE "07.in")

; read the two important chars
(define (pair line)
  (cons (string-ref line 5) (string-ref line 36)))

; which nodes can be first ones if we delete 'used' nodes?
(define (firsts pairs used)
  (let* ([p2 (filter-not 
              (lambda (x) (or (member (car x) used) 
                              (member (cdr x) used))) pairs)]
         [a (remove-duplicates (map car p2))]
         [d (remove-duplicates (map cdr p2))]
         [diff (remove* d a)])
    (sort diff char<? )))

; which are the last nodes of the graph? (maybe one, maybe more)
(define (lasts pairs others)
  (let* ([seconds (remove-duplicates (map cdr pairs))]
         [end (remove* others seconds)])
    (sort end char<? )))

; build the order step-by-step adding to its end the very first node
(define (step order used)
  (let ([fs (firsts lines used)])
    ;(display (format "~a / ~a : ~a\n" order used fs))
    (cond
      [(null? fs) order]
      [else (step (append order (list (car fs))) (cons (car fs) used))])))

; the problem contains these directed edges
(define lines (map pair (file->lines FILE)))

; solution of part 1
(define result1 
  (let ([butlast (step '() '())])
    (list->string (append butlast (lasts lines butlast)))))
(displayln result1)

;; part 2
;(define assembly 
;  (for/hash ([c "*ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
;             [i (range 30)])
;    (values c i)))

(define assembly 
  (for/hash ([c "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
             [i (range 60 90)])
    (values c i)))


; extended graph
(define lines2 (cons (cons (string-ref result1 (- (string-length result1) 1)) #\*) lines))

(define (max-path-length path time)
  (let ([next (map cdr (filter (lambda (x) (eq? (car x) (car path))) lines2))])
    ;(displayln (format "max-len: ~a ~a : ~a" next path time))
    (cond
      [(null? next) time]
      [else (apply max (for/list ([n next])
                         (max-path-length (cons n path) 
                                          (+ time (hash-ref assembly n 0)))))])))
(define (pre-cond n pairs)
  (map car (filter (lambda (x) (eq? (cdr x) n)) pairs)))

(define (contains? big small)
  (if (null? small) #t
      (and (member (car small) big)
           (contains? big (cdr small)))))

(define (requirements completed preconditions until-now time)
  ;(display (format "req: ~a ~a ~a \n" preconditions until-now time))
  (cond
    [(contains? until-now preconditions) time]
    [(null? completed) #f]
    [else (requirements (cdr completed) preconditions (cons (caar completed) until-now) (cdar completed))]))

(define (start-time node completed next-time)
  (let* ([pc (pre-cond node lines2)]
        [cond-time (requirements completed  pc '() 0)]
        [start (max cond-time next-time)])
    ;(display (format "start node ~a : ~a\n" node start))
    (max-path-length (list node) (+ start (hash-ref assembly node 0)))))

(define (time-constraint jobs completed used)
  (let ([fs (firsts lines2 used)])
    ;(display (format "~a ~a ~a ~a \n" jobs completed used fs))
    (if (null? fs) (apply max jobs)
        (let*
            ([costly (map (lambda (f) (cons f (start-time f completed (car jobs)))) fs)]
             [next (caar (sort costly > #:key cdr))]
             [pc (pre-cond next lines2)]
             [time (requirements completed pc '() 0)]
             [new-end (+ (max time (car jobs)) (hash-ref assembly next 0))]
             [newjobs (sort (cons new-end (cdr jobs)) <)]
             [new-comp (sort (cons (cons next new-end) completed) < #:key cdr)])
          ;(display (format "next: ~a  end: ~a nj: ~a\n" costly new-end newjobs) )
          (time-constraint newjobs new-comp (cons next used))))))

;(display (time-constraint '(0 0) '() '()))
(display (time-constraint '(0 0 0 0 0) '() '()))
;(for ([c "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
;  (display (format "\n~a : ~a" c (pre-cond c lines2))))