;; факториал в (неэффективном) рекурсивном стиле
(define (fact x)
  (if (< x 3)
      x
      (* (fact (- x 1)) x)))
 
;; функция Фибоначчи — требует параллельной рекурсии
(define (fib n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (else (+ (fib (- n 1))
                 (fib (- n 2))))))
 
;; сумма элементов списка в характерном для Scheme стиле
;; (вспомогательная функция loop выражает цикл с помощью
;; хвостовой рекурсии и переменной-аккумулятора)
(define (sum-list x)
  (let loop ((x x) (n 0))
    (if (null? x)
        n
        (loop (cdr x) (+ (car x) n)))))
 
(fact 14)
(fib 10)
(sum-list '(6 8 100))
(sum-list (map fib '(1 2 3 4)))
