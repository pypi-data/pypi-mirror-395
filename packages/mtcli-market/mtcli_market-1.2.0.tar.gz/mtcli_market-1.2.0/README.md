# mtcli-market

Plugin para o **mtcli** que calcula e exibe o **Market Profile** de um ativo no MetaTrader 5 (MT5), em formato **totalmente textual e acessível** — ideal para uso com leitores de tela como **NVDA** ou **JAWS**.

O plugin segue rigorosamente o padrão **MVC (Model–View–Controller)**:
- O **Model** realiza todos os cálculos técnicos (TPO, POC, Value Area, HVN, LVN, IB etc.);
- O **Controller** apenas orquestra o fluxo de dados;
- A **View** apresenta o resultado em texto puro, sem caracteres gráficos.

---

## 📦 Instalação

Assumindo que o `mtcli` e seus módulos estão instalados no mesmo ambiente Python:

```bash
pip install -e .
````

Ou, se o projeto estiver em repositório separado:

```bash
pip install git+https://github.com/seuusuario/mtcli-market.git
```

---

## 🚀 Uso

O comando principal é `mtcli-market profile` (ou `python -m mtcli_market.profile`).

Exemplo:

```bash
mtcli market --symbol WINZ25 --bars 500 --by volume --block 5 --timeframe 15m
```

### Exemplo em modo verboso (detalhado):

```bash
mtcli market --symbol WDOZ25 --by ticks --timeframe H1 --verbose
```

### Exemplo em modo compacto (ideal para automação ou leitura programática):

```bash
mtcli market --symbol PETR4 --by volume --compact
```

---

## ⚙️ Opções disponíveis

| Opção                 | Descrição                                                                  | Padrão                              |
| --------------------- | -------------------------------------------------------------------------- | ----------------------------------- |
| `--symbol`, `-s`      | Código do ativo (ex: WINZ25, WDOZ25, PETR4)                                | Configuração em `mtcli_market.conf` |
| `--bars`, `-b`        | Número de candles a considerar                                             | 100                                 |
| `--block`, `-k`       | Tamanho do bloco de preço (em pontos)                                      | 5                                   |
| `--by`                | Base de cálculo: `time`, `ticks` ou `volume`                               | `time`                              |
| `--timeframe`         | Timeframe: `M1`, `M5`, `H1`, `D1` ou customizado (`2m`, `45m`, `2h`, `3d`) | `M1`                                |
| `--ib-minutes`        | Duração do Initial Balance (em minutos)                                    | 30                                  |
| `--va-percent`        | Percentual da Value Area (0.7 = 70%)                                       | 0.7                                 |
| `--compact/--verbose` | Saída compacta (curta) ou detalhada                                        | `False`                             |

---

## 📊 Métricas Calculadas

O **Market Profile** textual exibe as seguintes informações:

| Sigla         | Nome                   | Descrição                                                       |
| ------------- | ---------------------- | --------------------------------------------------------------- |
| **POC**       | Point of Control       | Nível de preço com maior volume ou TPO                          |
| **TPO**       | Time Price Opportunity | Quantidade de vezes que o preço foi negociado                   |
| **VAH / VAL** | Value Area High / Low  | Faixa de preços que cobre cerca de 70% da atividade             |
| **HVN**       | High Volume Nodes      | Áreas de alto volume — zonas de aceitação                       |
| **LVN**       | Low Volume Nodes       | Áreas de baixo volume — zonas de rejeição                       |
| **IB**        | Initial Balance        | Faixa de preço dos primeiros minutos definidos (ex: 30 minutos) |

---

## ♿ Acessibilidade

* Todo o output é **texto puro** (sem gráficos ou caracteres de formatação).
* Compatível com **NVDA**, **JAWS** e outros leitores de tela.
* Ideal para usuários com deficiência visual que operam no mercado financeiro via terminal.

---

## 🧱 Estrutura do Projeto

```
mtcli_market/
├── profile.py                # CLI principal
├── controllers/
│   └── profile_controller.py # Orquestra o fluxo MVC
├── models/
│   └── profile_model.py      # Cálculos de POC, VA, HVN, LVN, IB, etc.
└── views/
    └── profile_view.py       # Saída textual e acessível
```

---

## 🧩 Integração com outros plugins

O `mtcli-market` pode ser combinado com outros plugins do ecossistema **mtcli**, como:

* `mtcli-rvo`: volume relativo
* `mtcli-trade`: execução e controle de posições
* `mtcli-volume`: análise de volume e saldo de agressão

---

## 🧪 Testes

O projeto usa **pytest**:

```bash
pytest -v
```

Testes simulam conexões MT5 e validam cálculos de POC, VA, HVN, LVN e IB.

---

## 📄 Licença

Este projeto é licenciado sob a **GPL-3.0**.

---

## 🧠 Autor

Desenvolvido por **Valmir França** — parte do projeto **mtcli**, uma suíte de ferramentas em linha de comando para análise e automação no **MetaTrader 5**.

```

