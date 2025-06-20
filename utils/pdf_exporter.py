from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

def export_record_to_pdf(record):
    # Create PDF document
    filename = f"record_{record.id}_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Content container
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        alignment=1,  # Center aligned
        spaceAfter=20
    )

    # Add title
    elements.append(Paragraph("Dental Center - Record Report", title_style))

    # Record information
    elements.append(Paragraph("<b>Record Information</b>", styles['Heading2']))

    record_data = [
        ["Record ID:", str(record.id)],
        ["Doctor:", f"{record.doctor.name} ({record.doctor.specialty or 'No specialty'})"],
        ["Patient:", record.patient.name],
        ["Created At:", record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else "N/A"]
    ]

    record_table = Table(record_data, colWidths=[1.5*inch, 4*inch])
    record_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
    ]))

    elements.append(record_table)
    elements.append(Spacer(1, 0.3*inch))

    # Treatments section
    elements.append(Paragraph("<b>Treatments</b>", styles['Heading2']))

    treatment_data = [["Date", "Treatment", "Cost", "Notes"]]
    for treatment in record.get_treatments():
        treatment_date = treatment.treatment_date.strftime("%Y-%m-%d") if treatment.treatment_date else ""
        treatment_data.append([
            treatment_date,
            treatment.treatment_name,
            f"${treatment.cost:.2f}",
            treatment.notes or ""
        ])

    treatment_table = Table(treatment_data, colWidths=[1*inch, 2*inch, 0.8*inch, 2.2*inch])
    treatment_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,1), (2,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))

    elements.append(treatment_table)
    elements.append(Spacer(1, 0.3*inch))

    # Payments section
    elements.append(Paragraph("<b>Payments</b>", styles['Heading2']))

    payment_data = [["Date", "Amount", "Method", "Notes"]]
    for payment in record.get_payments():
        payment_date = payment.payment_date.strftime("%Y-%m-%d") if payment.payment_date else ""
        payment_data.append([
            payment_date,
            f"${payment.amount:.2f}",
            payment.payment_method,
            payment.notes or ""
        ])

    payment_table = Table(payment_data, colWidths=[1*inch, 0.8*inch, 0.8*inch, 2.4*inch])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))

    elements.append(payment_table)
    elements.append(Spacer(1, 0.3*inch))

    # Balance section
    balance = record.get_balance()
    if balance > 0:
        balance_text = f"<b>Balance Due:</b> ${balance:.2f}"
    elif balance < 0:
        balance_text = f"<b>Credit:</b> ${-balance:.2f}"
    else:
        balance_text = "<b>Balance:</b> $0.00"

    elements.append(Paragraph(balance_text, styles['Heading2']))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1  # Center aligned
    )
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", footer_style))

    # Build the PDF
    doc.build(elements)
    return filename
