import csv
import io
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from clientes.querying import ClienteFilterSpec, apply_cliente_filters, apply_cliente_ordering
from clientes.services import format_phone, mask_document


HEADERS = ["Nome", "Tipo", "Documento", "Telefone", "E-mail", "Cidade", "Estado", "Situação", "Criado em"]


def filtered_queryset(queryset, cleaned):
    spec = ClienteFilterSpec.from_cleaned_data(cleaned, default_active=False)
    return apply_cliente_ordering(apply_cliente_filters(queryset, spec), spec)


def report_rows(queryset):
    return [[c.nome, c.get_tipo_display(), mask_document(c.documento), format_phone(c.telefone), c.email, c.cidade, c.estado, c.get_situacao_display(), c.criado_em.strftime("%Y-%m-%d") if c.criado_em else ""] for c in queryset]


def safe_cell(value):
    text = "" if value is None else str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


def export_csv(queryset):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(HEADERS)
    for row in report_rows(queryset):
        writer.writerow([safe_cell(v) for v in row])
    response = HttpResponse("\ufeff" + output.getvalue(), content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="clientes-relatorio.csv"'
    return response


def export_xlsx(queryset):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Dados"
    sheet.append(HEADERS)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for row in report_rows(queryset):
        sheet.append([safe_cell(v) for v in row])
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for column in sheet.columns:
        letter = column[0].column_letter
        sheet.column_dimensions[letter].width = min(36, max(12, max(len(str(c.value or "")) for c in column) + 2))
    output = io.BytesIO()
    workbook.save(output)
    response = HttpResponse(output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="clientes-relatorio.xlsx"'
    return response


def export_pdf(queryset):
    output = io.BytesIO()
    document = SimpleDocTemplate(output, pagesize=landscape(A4), rightMargin=10 * mm, leftMargin=10 * mm, topMargin=12 * mm, bottomMargin=12 * mm)
    styles = getSampleStyleSheet()
    rows = [HEADERS] + report_rows(queryset)
    table = Table(rows, repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")), ("FONTSIZE", (0, 0), (-1, -1), 7), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story = [Paragraph("Relatório de clientes", styles["Title"]), Paragraph(f"Gerado em {datetime.now().astimezone().isoformat(timespec='minutes')}", styles["Normal"]), Spacer(1, 8), table]
    document.build(story)
    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="clientes-relatorio.pdf"'
    return response
