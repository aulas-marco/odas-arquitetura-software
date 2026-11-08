"""Executa o monólito modular com os módulos Agenda e Faturamento."""

from agenda.api import AgendaAPI
from faturamento.relatorio import RelatorioFaturamento
from faturamento.relatorio_com_atalho import RelatorioFaturamentoComAtalho


def reais(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    agenda = AgendaAPI()
    print("== Agenda: consultas do dia ==")
    a = agenda.reservar("Maria Santos", "Consulta clínica", 250.00)
    b = agenda.reservar("João Lima", "Eletrocardiograma", 200.00)
    c = agenda.reservar("Ana Costa", "Consulta clínica", 250.00)
    agenda.registrar_realizacao(a)
    agenda.registrar_realizacao(b)
    agenda.cancelar(c)
    print("  3 reservas: 2 realizadas e 1 cancelada")

    print("\n== Faturamento pelo contrato público (faturamento/relatorio.py) ==")
    quantidade, total = RelatorioFaturamento(agenda).gerar()
    print(f"  {quantidade} consulta(s) faturável(is), total {reais(total)}")

    print("\n== Faturamento pelo atalho (faturamento/relatorio_com_atalho.py) ==")
    quantidade, total = RelatorioFaturamentoComAtalho().gerar()
    print(f"  {quantidade} consulta(s) faturável(is), total {reais(total)}")


if __name__ == "__main__":
    main()
