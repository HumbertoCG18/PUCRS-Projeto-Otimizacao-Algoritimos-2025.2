import sys

# ----------------------------------------------------
# Versão 1: Recursiva Simples
# ----------------------------------------------------
def downto1_recursiva(n):
    """
    Versão recursiva simples.
    Retorna o número mínimo de operações para reduzir n a 1 (ou múltiplo de 7).
    """
    if n <= 1 or n % 7 == 0:
        return 0
    
    opcoes = [downto1_recursiva(n - 1)]
    if n % 2 == 0:
        opcoes.append(downto1_recursiva(n // 2))
    if n % 3 == 0:
        opcoes.append(downto1_recursiva(n // 3))
    
    return 1 + min(opcoes)


# ----------------------------------------------------
# Versão 2: Recursiva com Memorização
# ----------------------------------------------------
def downto1_memo(n, memo=None):
    """
    Versão recursiva com memorização (top-down DP).
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1 or n % 7 == 0:
        memo[n] = 0
        return 0
    
    opcoes = [downto1_memo(n - 1, memo)]
    if n % 2 == 0:
        opcoes.append(downto1_memo(n // 2, memo))
    if n % 3 == 0:
        opcoes.append(downto1_memo(n // 3, memo))
    
    memo[n] = 1 + min(opcoes)
    return memo[n]


# ----------------------------------------------------
# Versão 3: Iterativa (Bottom-up)
# ----------------------------------------------------
def downto1_iterativa(n):
    """
    Versão iterativa (programação dinâmica bottom-up).
    """
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + 1
        if i % 2 == 0:
            dp[i] = min(dp[i], dp[i // 2] + 1)
        if i % 3 == 0:
            dp[i] = min(dp[i], dp[i // 3] + 1)
        if i % 7 == 0:
            dp[i] = 0  # múltiplo de 7 é estado terminal
    return dp[n]


# ----------------------------------------------------
# BÔNUS: Reconstrução da sequência ótima
# ----------------------------------------------------
def reconstruir_operacoes(n):
    """
    Retorna a sequência de operações mínimas até chegar a 1 ou múltiplo de 7.
    """
    dp = [0] * (n + 1)
    prev = [0] * (n + 1)

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + 1
        prev[i] = i - 1
        if i % 2 == 0 and dp[i // 2] + 1 < dp[i]:
            dp[i] = dp[i // 2] + 1
            prev[i] = i // 2
        if i % 3 == 0 and dp[i // 3] + 1 < dp[i]:
            dp[i] = dp[i // 3] + 1
            prev[i] = i // 3
        if i % 7 == 0:
            dp[i] = 0
            prev[i] = -1  # marca múltiplo de 7 como terminal

    caminho = []
    while n > 1 and prev[n] != -1:
        if n - 1 == prev[n]:
            caminho.append("-1")
        elif n // 2 == prev[n]:
            caminho.append("/2")
        elif n // 3 == prev[n]:
            caminho.append("/3")
        n = prev[n]

    return caminho


# ----------------------------------------------------
# Execução via linha de comando
# ----------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python downto1.py <numero_inteiro>")
        sys.exit(1)
    n = int(sys.argv[1])

    print(f"Recursiva simples: {downto1_recursiva(n)} operações")
    print(f"Com memorização:  {downto1_memo(n)} operações")
    print(f"Iterativa:         {downto1_iterativa(n)} operações")
    print(f"Sequência ótima:   {' '.join(reconstruir_operacoes(n))}")
