inteiro: n
flutuante: m


inteiro fatorial(inteiro: n)
    inteiro: fat
    se n > 0 então {não calcula se n > 0}
        n := fat
        repita
            fat := fat * n
            n := n - 1
        até n = 0
        retorna(fat) {retorna o valor do fatorial de n}
    senão
        retorna(0)
    fim
fim

inteiro principal()
    m := 10.1
    leia(n)
    escreva(fatorial(n))
    retorna(0)
fim